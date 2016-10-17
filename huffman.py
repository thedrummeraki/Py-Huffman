#!/usr/bin/python

from heap_priority_list import *
from letter_frequencies import *
from io import BytesIO

# This class represents the huffman tree as a whole
class HuffmanTree:
	
	def __init__(self, letter_frequencies):
		if not isinstance(letter_frequencies, LetterFrequency):
			raise StandardError("Only LetterFrequency may be used")

		freqs = letter_frequencies.get_frequencies()
		letters = letter_frequencies.get_letters()
		self._root = self._build_tree(freqs=freqs, letters=letters)

	def print_tree(self):
		print("*** HuffmanTree: character codes ***")
		if self._root is not None:
			self._traverse_order(self._root, "")
		else:
			print("The tree is empty. Nothing to show.")
		print("************************************")

	def encode(self, string):
		bio = BytesIO()
		for c in string:
			bio.write(self._encode_character(c))
		bio.seek(0)
		return bio.read()

	def _build_tree(self, freqs, letters):
		queue = HeapPriorityQueue(len(freqs)+1)
		leaf_where_letter_is = list()
		i = 0
		while i < len(freqs):
			if freqs[i] > 0:
				node = HuffmanNode(letter=letters[i], frequency=freqs[i])
				leaf_where_letter_is.insert(ord(letters[i]), node)
				queue.insert(node, node)
				node = None
			i += 1
		
		eot = 0xffff
		eot = unichr(eot)
		special_node = HuffmanNode(letter=eot, frequency=0)
		queue.insert(special_node, special_node)

		while True:
			e1 = queue.remove_min()
			e2 = queue.remove_min()

			new_node = HuffmanNode()
			left = e1.get_value()
			right = e2.get_value()

			if left > right:
				temp = right
				right = left
				left = temp

			new_node.set_frequency(left.get_frequency() + right.get_frequency())
			new_node.set_letter(chr(0))
			new_node.set_left_child(left)
			new_node.set_right_child(right)
			left.set_parent(new_node)
			right.set_parent(new_node)

			queue.insert(new_node, new_node)
			if queue.size() < 2:
				break

		return queue.remove_min().get_value()

	def _encode_character(self, c):
		current = self._root
		if current is None:
			return ''

		return self._do_encode_character(c, current, "")

	def _do_encode_character(self, c, current, path):
		r = None
		if current == None:
			return r

		if current.is_leaf():
			if current.get_letter() == c:
				return path
		else:
			r = self._do_encode_character(c, current.left_child(), path+"0")
			if r is None:
				r = self._do_encode_character(c, current.right_child(), path+"1")

		return r
	
	def _traverse_order(self, current, c):
		if current.is_leaf():
			try:
				print("%c: %s" % (current.get_letter(), c))
			except:
				print("endOfText: %s" % c)
		else:
			self._traverse_order(current.left_child(), c+"0")
			self._traverse_order(current.right_child(), c+"1")

class HuffmanNode:

	def __init__(self, letter=0, frequency=-1, parent=None, left=None, right=None):
		self._letter = letter
		self._frequency = frequency
		self._parent = parent
		self._left = left
		self._right = right

	def is_leaf(self):
		return self._left == None and self._right == None

	def left_child(self):
		return self._left

	def right_child(self):
		return self._right

	def parent(self):
		return self._parent

	def get_letter(self):
		return self._letter

	def set_letter(self, new_letter):
		self._letter = new_letter

	def get_frequency(self):
		return self._frequency

	def set_frequency(self, new_frequency):
		self._frequency = new_frequency

	def set_left_child(self, new_left):
		self._left = new_left

	def set_right_child(self, new_right):
		self._right = new_right

	def set_parent(self, new_parent):
		self._parent = new_parent

	def __eq__(self, node):
		if node == None:
			return False
		if not isinstance(node, HuffmanNode):
			return False
		return self._letter == node._letter and self._frequency == node._frequency

	def __lt__(self, node):
		if node == None:
			return False
		if not isinstance(node, HuffmanNode):
			return False
		if self._frequency == node._frequency:
			return self._letter < node._letter
		return self._frequency < node._frequency

	def __gt__(self, node):
		if node == None:
			return False
		if not isinstance(node, HuffmanNode):
			return False
		if self._frequency == node._frequency:
			return self._letter > node._letter
		return self._frequency > node._frequency

	def __str__(self):
		return "Node %s (%s): [CL: %s | CR: %s]" % (self._letter, self._frequency, self._left, self._right)


def usage(arg):
	return "Usage: '%s' -f [filename] -t [your text here]\nUse one or both of the options.\n" \
			"Add tag -p to print the code of the tree (will not print the result). \nAdd -a (--all) to print everything. \nAdd -s (--size) to see the size in bytes of the encoded text.\n" \
			"-h (--help) prints this message" % arg


if __name__ == "__main__":
	import sys
	args = sys.argv

	if len(args) < 2:
		print usage(args[0])
		sys.exit(0)

	if '-f' in args:
		try:
			file_to_enc = args[args.index('-f')+1]
		except:
			print "You forgot to specify a file."
			sys.exit(1)
	else:
		file_to_enc = None

	if '-t' in args:
		try:
			text_to_enc = ""
			index = args.index('-t') + 1
			while index < len(args):
				found = args[index]
				if found.startswith('-'):
					break
				text_to_enc += found
				if index != len(args)-2:
					text_to_enc += ' '
				index += 1
		except:
			print "You forgot to specify some text."
			sys.exit(1)
	else:
		text_to_enc = None

	wants_help = '-h' in args or '--help' in args
	if wants_help:
		print(usage(args[0]))
		sys.exit(0)

	see_size = '-s' in args or '--size' in args
	wants_to_print = '-p' in args
	print_either_way = '-a' in args or '--all' in args

	if file_to_enc is None and text_to_enc is None:
		print usage(args[0])
		sys.exit(1)

	if text_to_enc:
		try:
			lf = LetterFrequency(text_to_enc)
			h = HuffmanTree(lf)
			res = h.encode(text_to_enc)
			if wants_to_print:
				print("Text: '%s'" % text_to_enc)
			if print_either_way and wants_to_print:
				print(res)
			if wants_to_print:
				h.print_tree()
			else:
				print(res)
			if see_size:
				print("Size: %s byte(s) of encoded text vs %s byte(s) of original text" % (len(res), len(text_to_enc)))

		except BaseException, e:
			print "There was some sort of issue: %s" % e
			sys.exit(1)

	if file_to_enc:
		try:
			text_to_enc = open(file_to_enc).read()
			lf = LetterFrequency(text_to_enc)
			h = HuffmanTree(lf)
			res = h.encode(text_to_enc)
			#if wants_to_print:
			#	print("Text: '%s'" % text_to_enc)
			if print_either_way and wants_to_print:
				print(res)
			if wants_to_print:
				h.print_tree()
			else:
				print(res)
			if see_size:
				print("Size: %s byte(s) of encoded text vs %s byte(s) of original text" % (len(res), len(text_to_enc)))

		except BaseException, e:
			print "There was some sort of issue: %s" % e
			sys.exit(1)
