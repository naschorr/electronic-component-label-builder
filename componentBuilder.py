import inflect

import label
import helpers

## Defaults
TOLERANCE = 5.0
BAND_COUNT = 5 	# Only supports 4 and 5 band codes so far
UNITS = 'Ω'
CONDENSE_VALUE = True
SHOW_COLOR_CODES = True
SHOW_TOLERANCE = True
VOLTAGE = 100	# Voltage limit. See setter property for more details
TEMPERATURE = 70	# Operating temperature range, from -55c to 70c in this case

## Prefixes
METRIC_PREFIXES = ["p", "n", "µ", "m", "", "k", "M", "G", "T"]

## Band information
COLORS = ["black", "brown", "red", "orange", "yellow", "green", "blue", "purple", "gray", "white"]
MULTIPLIERS = {1:"black", 10:"brown", 100:"red", 1000:"orange", 10000:"yellow", 100000:"green", 1000000:"blue", 10000000:"purple", 100000000:"gray", 1000000000:"white", 0.1:"gold", 0.01:"silver"}
RESISTOR_TOLS = {1:"brown", 2:"red", 0.5:"green", 0.25:"blue", 0.1:"purple", 0.05:"gray", 5:"gold", 10:"silver"}
INDUCTOR_TOLS = {20:"black", 1:"brown", 2:"red", 5:"green", 10:"white"}
CAPACITOR_TOLS = {20:"black", 1:"brown", 2:"red", 3:"orange", 4:"yellow", 5:"gold", 10:"silver"}

## Component identification strings
RESISTOR_ID = ['Ω', 'ohm', 'resist']
INDUCTOR_ID = ['henr', 'induct']
CAPACITOR_ID = ['farad', 'capacit']

class Component:
	def __init__(self, dataObj, **kwargs):
		self.dataObj = dataObj
		self.unitName = helpers.kwargExists("unitName", kwargs) or UNITS
		self.tolerance = helpers.kwargExists("tolerance", kwargs) or TOLERANCE
		self.bandCount = helpers.kwargExists("bandCount", kwargs) or BAND_COUNT
		self.condense = helpers.setBoolKwarg("condense", kwargs, CONDENSE_VALUE)
		self.showColorCodes = helpers.setBoolKwarg("showColorCodes", kwargs, SHOW_COLOR_CODES)
		self.showTolerance = helpers.setBoolKwarg("showTolerance", kwargs, SHOW_TOLERANCE)
		self.voltage = helpers.kwargExists("voltage", kwargs) or VOLTAGE
		self.temperature = helpers.kwargExists("temperature", kwargs) or TEMPERATURE

		self._labels = []

		for value in self.dataObj.dataLines:
			text, colorCode = self.buildComponentLabel(value)
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
		validBands = [4,5]
		self._bandCount = helpers.testForRange(value, validBands, valueName="bandCount")

	@property
	def condense(self):
		return self._condense

	@condense.setter
	def condense(self, value):
		self._condense = value

	@property
	def showColorCodes(self):
		return self._showColorCodes
	
	@showColorCodes.setter
	def showColorCodes(self, value):
		self._showColorCodes = value
	
	@property
	def showTolerance(self):
		return self._showTolerance

	@showTolerance.setter
	def showTolerance(self, value):
		self._showTolerance = value

	@property
	def voltage(self):
		return self._voltage

	@voltage.setter
	def voltage(self, value):
		## Voltages checked against: http://www.pmel.org/Handbook/HBpage26.htm
		voltages = [v for v in helpers.incRange(100, 1000, 100)]
		voltages.append(2000)
		self._voltage = helpers.testForRange(value, voltages, valueName="voltage")

	@property
	def temperature(self):
		return self._temperature

	@temperature.setter
	def temperature(self, value):
		## Temperatures checked against: https://en.wikipedia.org/wiki/Electronic_color_code#Capacitor_color-coding
		temperatures = [70, 85, 125, 150]
		self._temperature = helpers.testForRange(value, temperatures, valueName="temperature")

	@property
	def labels(self):
		return self._labels

	@labels.setter
	def labels(self, value):
		self._labels = value

	## Methods

	def getFractionalDigitCount(self, value):
		count = 0
		while(value * 10 < 1):
			value *= 10
			count += 1

		return count


	def condenseValue(self, value):
		value = float(value)
		fractionalDigits = self.getFractionalDigitCount(value)

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
				value = round(value, fractionalDigits - count * 3)

		## If the floating point is meaningless, then remove it and the last zero.
		if(value == int(value)):
			value = str(value)[:-2]

		## Return formatted string, as well as appropriate metric prefix. Notice 
		##		how it starts in the middle of the METRIC_PREFIXES list, and then 
		##		the count variable modifies the position.
		return str(value) + METRIC_PREFIXES[count + int(len(METRIC_PREFIXES)/2)]


	def getLeadingDigits(self, value, numDigits=None):
		numDigits = numDigits if numDigits else self.bandCount-2

		stringValue = str(value)
		leadingDigits = ""
		digitCounter = 0
		stringIndex = 0
		## Get the first (3) numbers in the string, ignoring any other characters
		while(digitCounter < numDigits and stringIndex < len(stringValue)):
			thisChar = stringValue[stringIndex]
			if(thisChar is '.' or (thisChar is '0' and digitCounter is 0)):
				stringIndex += 1
				continue
			leadingDigits += thisChar
			stringIndex += 1

		## If (3) digits aren't found, pad it out with 0s
		while(len(leadingDigits) < numDigits):
			leadingDigits += '0'

		return int(leadingDigits)


	def buildLabelName(self, value):
		## Condense the name (ex. 10000 -> 10k) if the user has allowed it
		if(self.condense):
			name = self.condenseValue(value)
		else:
			name = value

		## Make sure that there is a unitname to append
		if(len(self.unitName) > 0):
			## Pluralize the name if it's not singular, and doesn't contain special characters
			if(float(value) > 1 and len(self.unitName) > 1 and not any(ord(char) < 32 or ord(char) > 126 for char in self.unitName)):
				name += " " + inflect.engine().plural(self.unitName)
			else:
				name += " " + self.unitName

		return name


	def buildLabelColorCode(self, value, leadingDigits):
		## Ppopulate the first 3 indecies with the appropriate colors
		bands = self.bandCount*["black"]
		for counter, digit in enumerate(str(leadingDigits)):
			bands[counter] = COLORS[int(digit)]

		## Populate the multiplier band with its color
		multiplierIndex = round(float(value) / leadingDigits, 2)

		try:
			if(self.bandCount == 4):
				bands[-2] = MULTIPLIERS[multiplierIndex]
			elif(self.bandCount == 5):
				bands[-2] = MULTIPLIERS[multiplierIndex]
		except KeyError as ke:
			print("KeyError", ke, "Ignoring bands for this label.")
			bands = None

		if(self.showTolerance):
			## Populate the tolerance band with its color
			bands[-1] = RESISTOR_TOLS[float(self.tolerance)]
		else:
			del bands[-1]

		return bands


	def buildComponentLabel(self, data):
		leadingDigits = self.getLeadingDigits(data)

		name = self.buildLabelName(data)

		if(self.showColorCodes):
			bands = self.buildLabelColorCode(data, leadingDigits)
		else:
			bands = None

		return name, bands
			