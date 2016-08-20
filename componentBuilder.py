import inflect
import label

## Defaults
TOLERANCE = 5.0
BAND_COUNT = 5
UNITS = ""
CONDENSE_VALUE = True

## Band information
METRIC_PREFIXES = ["p", "n", "µ", "m", "", "k", "M", "G", "T"]
COLORS = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "gray", "white"]
RESISTOR_MULTIS = {1:"black", 10:"brown", 100:"red", 1000:"orange", 10000:"yellow", 100000:"green", 1000000:"blue", 10000000:"purple", 100000000:"gray", 1000000000:"white", 0.1:"gold", 0.01:"silver"}
RESISTOR_TOLS = {1:"brown", 2:"red", 0.5:"green", 0.25:"blue", 0.1:"purple", 0.05:"gray", 5:"gold", 10:"silver"}
INDUCTOR_MULTIS = {1:"black", 10:"brown", 100:"red", 1000:"orange", 10000:"yellow", 0.1:"gold", 0.01:"silver"}
INDUCTOR_TOLS = {20:"black", 1:"brown", 2:"red", 5:"green", 10:"white"}
CAPACITOR_MULTIS = {1:"black", 10:"brown", 100:"red", 1000:"orange", 10000:"yellow", 100000:"green", 1000000:"blue", 10000000:"purple"}
CAPACITOR_TOLS = {20:"black", 1:"brown", 2:"red", 3:"orange", 4:"yellow", 5:"gold", 10:"silver"}

class Component:
	def __init__(self, dataObj, **kwargs):

		def kwargExists(kwarg):
			if kwarg in kwargs:
				return kwargs[kwarg]
			else:
				return False

		self.dataObj = dataObj
		self.unitName = kwargExists("unitName") or UNITS
		self.tolerance = kwargExists("tolerance") or TOLERANCE
		self.bandCount = kwargExists("bandCount") or BAND_COUNT
		self.condense = kwargExists("condense") or CONDENSE_VALUE

		self._labels = []

		for value in self.dataObj.dataLines:
			text, colorCode = self.buildResistorLabel(value)
			self.labels.append(label.Label(text, colorCode))

	## Properties

	@property
	def dataObj(self):
		return self._dataObj

	@dataObj.setter
	def dataObj(self, value):
		self._dataObj = value

	@property
	def unitName(self):
		return self._unitName
	
	@unitName.setter
	def unitName(self, value):
		self._unitName = value

	@property
	def tolerance(self):
		return self._tolerance
	
	@tolerance.setter
	def tolerance(self, value):
		self._tolerance = value

	@property
	def bandCount(self):
		return self._bandCount
	
	@bandCount.setter
	def bandCount(self, value):
		self._bandCount = value

	@property
	def condense(self):
		return self._condense

	@condense.setter
	def condense(self, value):
		self._condense = value
	
	@property
	def labels(self):
		return self._labels

	@labels.setter
	def labels(self, value):
		self._labels = value

	## Methods

	def condenseValue(self, value):
		value = float(value)

		count = 0
		## Count how many thousands are in a given value, as well as divide the 
		##		value down to its final stage (This count will be used to pick the 
		##		appropriate metric prefix for the value).
		if(value >= 1000):
			while(value / 1000 >= 1):
				count += 1
				value /= 1000
		elif(value < 1):
			while(value * 1000 <= 1):
				count -= 1
				value *= 1000

		## If the floating point is meaningless, then remove it and the last zero.
		if(value == int(value)):
			value = str(value)[:-2]

		## Return formatted string, as well as appropriate metric prefix. Notice 
		##		how it starts in the middle of the METRIC_PREFIXES list, and then 
		##		the count variable modifies the position.
		return str(value) + METRIC_PREFIXES[count + int(len(METRIC_PREFIXES)/2)]


	def buildResistorLabel(self, data):
		p = inflect.engine()
		integer = int(float(data))
		fractional = round(float(data) % 1, 1)
		stringData = str(integer)[:3]
		if(fractional != 0.0):
			stringData += str(fractional)[2:]

		if(self.condense):
			name = self.condenseValue(data)
		else:
			name = data

		if(float(data) > 1 and not any(ord(char) < 32 or ord(char) > 126 for char in self.unitName)):
			name += " " + p.plural(self.unitName)
		else:
			name += " " + self.unitName

		while(len(stringData) < 3):
			stringData += "0"

		bands = self.bandCount*["black"]
		for index in range(3):
			bands[index] = COLORS[int(stringData[index])]
		bands[-1] = RESISTOR_TOLS[float(self.tolerance)]

		bands[-2] = RESISTOR_MULTIS[round((integer + fractional) / int(stringData), 2)]

		return name, bands