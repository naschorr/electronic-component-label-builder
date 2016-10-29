import inflect

import label
import helpers

## Defaults (Set to default to a generic resistor)
TOLERANCE = 5.0
SIG_BAND_COUNT = 3
RESISTOR_UNITS = 'Ω'
CAPACITOR_UNITS = 'F'
INDUCTOR_UNITS = 'H'
CONDENSE_VALUE = True
SHOW_COLOR_CODES = True
SHOW_TOLERANCE = True
VOLTAGE = 100		# Voltage limit (Capacitor)
TEMPERATURE = 70	# Operating temperature (Capacitor) (-55 to 70)

## Prefixes
METRIC_PREFIXES = ["p", "n", "µ", "m", "", "k", "M", "G", "T"]

## Color Name Strings
BLACK = "black"
BROWN = "brown"
RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
BLUE = "blue"
PURPLE = "purple"
GRAY = "gray"
WHITE = "white"
GOLD = "gold"
SILVER = "silver"

## RGB Color Configuration
RGB_COLORS = {BLACK:(0, 0, 0), BROWN:(165, 42, 42), RED:(255, 0, 0), 
			  ORANGE:(255, 165, 0), YELLOW:(255, 255, 0), GREEN:(53, 169, 7), 
			  BLUE:(0, 0, 255), PURPLE:(128, 0, 128), GRAY:(95, 95, 95), 
			  WHITE:(255, 255, 255), GOLD:(212, 175, 55), SILVER:(175, 175, 175)}

## Band information
COLORS = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, GRAY, WHITE]
MULTIPLIERS = {1:BLACK, 10:BROWN, 100:RED, 1000:ORANGE, 10000:YELLOW, 100000:GREEN, 
			   1000000:BLUE, 10000000:PURPLE, 100000000:GRAY, 1000000000:WHITE, 
			   0.1:GOLD, 0.01:SILVER}
RESISTOR_TOLS = {1:BROWN, 2:RED, 0.5:GREEN, 0.25:BLUE, 0.1:PURPLE, 0.05:GRAY, 
				 5:GOLD, 10:SILVER}
LC_TOLS = {20:BLACK, 1:BROWN, 2:RED, 3:ORANGE, 4:YELLOW, 5:GOLD, 10:SILVER}	# Inductor and Capacitor tolerance colors
VOLTAGE_COLORS = {0:BLACK, 100:BROWN, 200:RED, 300:ORANGE, 400:YELLOW, 500:GREEN, # Voltages checked against: http://www.pmel.org/Handbook/HBpage26.htm
			   600:BLUE, 700:PURPLE, 800:GRAY, 900:WHITE, 1000:GOLD, 2000:SILVER}
TEMPERATURE_COLORS = {70:BLACK, 85:RED, 125:YELLOW, 150:BLUE}	# MAXIMUM -- Temperatures checked against: https://en.wikipedia.org/wiki/Electronic_color_code#Capacitor_color-coding

## Supported components
RESISTOR_STR = "resistor"
CAPACITOR_STR = "capacitor"
INDUCTOR_STR = "inductor"
COMPONENTS = [RESISTOR_STR, CAPACITOR_STR, INDUCTOR_STR]

class Component:
	def __init__(self, dataObj, **kwargs):
		self.dataObj = dataObj
		self.kwargs = kwargs
		self.bandCount = helpers.kwargExists("bandCount", kwargs)
		self.condense = helpers.setBoolKwarg("condense", kwargs, CONDENSE_VALUE)
		self.showColorCodes = helpers.setBoolKwarg("showColorCodes", kwargs, SHOW_COLOR_CODES)
		self.showTolerance = helpers.setBoolKwarg("showTolerance", kwargs, SHOW_TOLERANCE)
		self.voltage = helpers.kwargExists("voltage", kwargs)
		self.temperature = helpers.kwargExists("temperature", kwargs)

		## With all other data set, try to guess which component it is.
		self.component = helpers.kwargExists("component", kwargs) or self.guessComponent()

		## With the component set, set the tolerance and then apply the user's units or pick them based off of the component.
		self.tolerance = helpers.kwargExists("tolerance", kwargs)
		self.unitName = helpers.kwargExists("unitName", kwargs) or self.setUnits()

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
	def kwargs(self):
		return self._kwargs

	@kwargs.setter
	def kwargs(self, value):
		self._kwargs = value

	@property
	def unitName(self):
		return self._unitName

	@unitName.setter
	@helpers.isStr
	def unitName(self, value):
		self._unitName = value or RESISTOR_UNITS

	@property
	def tolerance(self):
		return self._tolerance

	@tolerance.setter
	@helpers.isFloat
	@helpers.isPositive
	def tolerance(self, value):
		if(value is not None):
			if(self.component == INDUCTOR_STR or self.component == CAPACITOR_STR):
				validTolerances = [key for key in LC_TOLS]
			else:
				validTolerances = [key for key in RESISTOR_TOLS]
			self._tolerance = helpers.testForRange(value, validTolerances, "tolerance")
		else:
			self._tolerance = TOLERANCE

	@property
	def bandCount(self):
		return self._bandCount

	@bandCount.setter
	@helpers.isInt
	@helpers.isPositive
	def bandCount(self, value):
		self._bandCount = value or SIG_BAND_COUNT

	@property
	def condense(self):
		return self._condense

	@condense.setter
	@helpers.isBool
	def condense(self, value):
		self._condense = value if value is not None else CONDENSE_VALUE

	@property
	def showColorCodes(self):
		return self._showColorCodes

	@showColorCodes.setter
	@helpers.isBool
	def showColorCodes(self, value):
		self._showColorCodes = value if value is not None else SHOW_COLOR_CODES

	@property
	def showTolerance(self):
		return self._showTolerance

	@showTolerance.setter
	@helpers.isBool
	def showTolerance(self, value):
		self._showTolerance = value if value is not None else SHOW_TOLERANCE

	@property
	def voltage(self):
		return self._voltage

	@voltage.setter
	@helpers.isFloat
	@helpers.isPositive
	def voltage(self, value):
		if(value is not None):
			self._voltage = helpers.testForRange(value, [key for key in VOLTAGE_COLORS], "voltage")
		else:
			self._voltage = VOLTAGE

	@property
	def temperature(self):
		return self._temperature

	@temperature.setter
	@helpers.isInt
	@helpers.isPositive
	def temperature(self, value):
		if(value is not None):
			self._temperature = helpers.testForRange(value, [key for key in TEMPERATURE_COLORS], "temperature")
		else:
			self._temperature = TEMPERATURE

	@property
	def labels(self):
		return self._labels

	@labels.setter
	def labels(self, value):
		self._labels = value

	@property
	def component(self):
		return self._component

	@component.setter
	@helpers.isStr
	def component(self, value):
		if(value in COMPONENTS):
			self._component = value
		## Default to resistor
		else:
			self._component = RESISTOR_STR

	## Methods

	def guessComponent(self):
		if(helpers.kwargExists("voltage", self.kwargs) or helpers.kwargExists("temperature", self.kwargs)):
			return CAPACITOR_STR
		else:
			return RESISTOR_STR


	def setUnits(self):
		if(self.component == CAPACITOR_STR):
			return CAPACITOR_UNITS
		elif(self.component == INDUCTOR_STR):
			return INDUCTOR_UNITS
		else:
			return RESISTOR_UNITS


	def getFractionalDigitCount(self, value):
		if(value == 0.0):
			return 0

		count = 0
		while(value * 10 <= 1):
			value *= 10
			count += 1

		return count


	def condenseValue(self, value):
		if(value == 0.0):
			return "0", 0

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
		return str(value), count


	def getLeadingDigits(self, value, numDigits=None):
		numDigits = numDigits if numDigits else self.bandCount

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
			digitCounter += 1

		## If (3) digits aren't found, pad it out with 0s
		while(len(leadingDigits) < numDigits):
			leadingDigits += '0'

		return int(leadingDigits)


	def buildLabelName(self, value):
		## Condense the name (ex. 10000 -> 10) if the user has allowed it
		if(self.condense):
			name, exponent = self.condenseValue(value)

			if(self.component == CAPACITOR_STR):
				name += ' ' + METRIC_PREFIXES[exponent]
			elif(self.component == INDUCTOR_STR):
				name += ' ' + METRIC_PREFIXES[exponent + 2]
			else:
				name += ' ' + METRIC_PREFIXES[int(len(METRIC_PREFIXES)/2) + exponent]
		else:
			name = str(value)

		## Make sure that there is a unitname to append
		if(len(self.unitName) > 0):
			## Pluralize the name if it's not singular, and doesn't contain special characters
			if(float(value) > 1 and len(self.unitName) > 1 and not any(ord(char) < 32 or ord(char) > 126 for char in self.unitName)):
				name += inflect.engine().plural(self.unitName)
			else:
				name += self.unitName

		return name


	def buildBaseColorCode(self, value, leadingDigits):
		## Ppopulate the first 3 indecies with the appropriate colors
		bands = []
		for digit in str(leadingDigits):
			bands.append(RGB_COLORS[COLORS[int(digit)]])

		## Populate the multiplier band with its color
		multiplierIndex = round(float(value) / leadingDigits, 2)

		try:
			bands.append(RGB_COLORS[MULTIPLIERS[multiplierIndex]])
		except KeyError as ke:
			helpers.eclbPrint("KeyError", ke, "Ignoring bands for this label.")
			return None

		if(self.showTolerance):
			if(self.component == CAPACITOR_STR or self.component == INDUCTOR_STR):
				tolerance = RGB_COLORS[LC_TOLS[float(self.tolerance)]]
			else:
				tolerance = RGB_COLORS[RESISTOR_TOLS[float(self.tolerance)]]
			bands.append(tolerance)

		return bands


	def buildOptionsColorCode(self):
		optionBands = []
		if(self.component == CAPACITOR_STR):
			## Check to make sure that the user specified their own values, and don't just append the defaults in.
			if(helpers.kwargExists("voltage", self.kwargs)):
				optionBands.append(RGB_COLORS[VOLTAGE_COLORS[self.voltage]])
			if(helpers.kwargExists("temperature", self.kwargs)):
				optionBands.append(RGB_COLORS[TEMPERATURE_COLORS[self.temperature]])

		return optionBands


	def buildLabelColorCode(self, value, leadingDigits):
		bands = self.buildBaseColorCode(value, leadingDigits)
		bands.extend(self.buildOptionsColorCode())

		return bands


	def buildComponentLabel(self, data):
		leadingDigits = self.getLeadingDigits(data)

		name = self.buildLabelName(data)

		if(self.showColorCodes):
			bands = self.buildLabelColorCode(data, leadingDigits)
		else:
			bands = None

		return name, bands
