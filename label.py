class Label:
	def __init__(self, text, colorCode=None):
		self._text = text
		self._colorCode = colorCode

	## Properties

	@property
	def text(self):
	    return self._text

	@text.setter
	def text(self, value):
		self._text = value

	@property
	def colorCode(self):
	    return self._colorCode

	@colorCode.setter
	def colorCode(self, value):
		self._colorCode = value