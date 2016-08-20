class Data:
	def __init__(self, pathToFile):
		self.pathToFile = pathToFile
		self.dataLines = self.getDataLinesFromFile(self.pathToFile)

	## Properties

	@property
	def pathToFile(self):
		return self._pathToFile
	
	@pathToFile.setter
	def pathToFile(self, value):
		self._pathToFile = value

	@property
	def dataLines(self):
		return self._dataLines
	
	@dataLines.setter
	def dataLines(self, value):
		self._dataLines = value

	## Methods

	def formatString(self, string):
		return string.lower().rstrip().lstrip()

	def getDataLinesFromFile(self, file):
		data = []
		with open(file, 'r') as fd:
			for line in fd:
				data.append(self.formatString(line))
		return data
