# An entry
class Entry:

	def __init__(self, key, value):
		self._k = key
		self._v = value

	def get_key(self):
		return self._k

	def get_value(self):
		return self._v

# Implementation of a heap priority queue
class HeapPriorityQueue:

	def __init__(self, size=100):
		self._storage = list()
		self._limit = size
		self._tail = -1

	def size(self):
		return self._tail + 1

	def is_empty(self):
		return self._tail < 0

	def insert(self, key, value):
		if self._tail == self._limit:
			raise StandardError("Heap Overflow (size: %s, tail: %s)" % (self._limit, self._tail))

		e = Entry(key, value)
		self._tail += 1
		self._storage.insert(self._tail, e)
		self._up_heap(self._tail)
		return e

	def min(self):
		return None if self.is_empty() else self._storage[0]

	def remove_min(self):
		if self.is_empty():
			print("Empty queue")
			return None
		ret = self._storage[0]
		if (self._tail == 0):
			self._tail = -1
			self._storage[0] = None
			return ret

		self._storage[0] = self._storage[self._tail]
		self._tail -= 1
		self._storage.remove(self.min())
		self._down_heap(0)
		return ret

	def _parent(self, location):
		return (location-1)/2

	def _swap(self, l1, l2):
		temp = self._storage[l1]
		self._storage[l1] = self._storage[l2]
		self._storage[l2] = temp

	def _up_heap(self, location):
		if location == 0:
			return None

		parent = self._parent(location)
		if self._storage[parent].get_key() > self._storage[location].get_key():
			self._swap(location, parent)
			self._up_heap(parent)

	def _down_heap(self, location):
		left = (location*2) + 1
		right = (location*2) + 2

		if left > self._tail:
			return None

		if left == self._tail:
			if self._storage[location].get_key() > self._storage[left].get_key():
				self._swap(location, left)
			return None

		to_swap = left if self._storage[left].get_key() < self._storage[right].get_key() else right
		if self._storage[location].get_key() > self._storage[to_swap].get_key():
			self._swap(location, to_swap)
			self._down_heap(to_swap)

