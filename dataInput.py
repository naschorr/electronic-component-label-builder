from re import match
from sys import exit

import helpers

## Prefix data
METRIC_PREFIX_VALUES = {"p":0.000000000001, "n":0.000000001, "µ":0.000001, 
						"u":0.000001, "m":0.001, "":1, "k":1000, "M":1000000, 
						"G":1000000000, "T":1000000000000}

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
			data.append(self.parseValueFormat(line))
		return data


	def parseValueFormat(self, value):
		value = helpers.strip(value)
		## Integer/floating portion of number = group 1
		## Metric prefix = group 2
		tokens = match(r'([0-9]+\.?[0-9]*)\s?([a-zA-Z]?)', value)
		try:
			componentValue = float(tokens.group(1))
			prefixValue = METRIC_PREFIX_VALUES[tokens.group(2)]
		except AttributeError as ae:
			alert = "Invalid value for the input '{0}'. Input should be of the form <number> <metric prefix> where the number is a float or integer. Quitting now."
			print(alert.format(value))
			exit()
		except KeyError as ke:
			alert = "Invalid metric prefix for the input '{0}'. Input should be of the form <number> <metric prefix> where the prefix is in the list {1}. Quitting now."
			print(alert.format(value, [prefix for prefix in METRIC_PREFIX_VALUES]))
			exit()

		return int(componentValue * prefixValue)