import re


class TextValidator:
	def __init__(self, min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+'):
		self.min = min
		self.max = max
		self.regexp = regexp


	def check(self, text: str):
		if re.sub(regexp, '', text) != '':
			return False
		if len(text) > max or len(text) < min:
			return False
		return True