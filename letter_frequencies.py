class LetterFrequency:

	def __init__(self, input_string):
		if not isinstance(input_string, str):
			raise StandardError("Only strings can be used for instanciating letter frequencies")

		couples = list()
		letters = list()

		index = 0
		while index < len(input_string):
			current = input_string[index]
			if current in letters:
				amount = None
				found_index = 0
				for c in couples:
					if c[0] == current:
						amount = c[1]
						break
					found_index += 1
				amount += 1
				couples[found_index] = (current, amount)
			else:
				letters.append(current)
				couples.append((current, 1))
			index += 1

		self._l = []
		self._f = []
		for couple in couples:
			self._l.append(couple[0])
			self._f.append(couple[1])


	def get_letters(self):
		return self._l

	def get_frequencies(self):
		return self._f