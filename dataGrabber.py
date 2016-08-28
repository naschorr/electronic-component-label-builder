import helpers

class Data:
	def __init__(self, pathToData):
		self.pathToData = pathToData
		self.dataLines = self.getDataLinesFromFile(self.pathToData)

	## Properties

	@property
	def pathToData(self):
		return self._pathToData
	
	@pathToData.setter
	def pathToData(self, value):
		self._pathToData = value

	@property
	def dataLines(self):
		return self._dataLines
	
	@dataLines.setter
	def dataLines(self, value):
		self._dataLines = value

	## Methods

	def getDataLinesFromFile(self, file):
		data = []
		for line in file:	# File opened via click
			data.append(helpers.formatString(line))
		return data
