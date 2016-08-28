def kwargExists(kwarg, kwargs):
			if kwarg in kwargs:
				if(kwargs[kwarg] is not None):
					return kwargs[kwarg]
			return None


def setBoolKwarg(kwargString, kwargs, defaultValue):
	kwargState = kwargExists(kwargString, kwargs)
	return kwargState if kwargState is True or kwargState is False else defaultValue


def formatString(string):
		return string.lower().rstrip().lstrip()


def testForRange(value, valueList, **kwargs):
	if(value in valueList):
		return value
	else:
		index = 0
		rangeFound = False
		thisIndex = None
		outputString = "Supplied " + (kwargExists("valueName", kwargs) or 'value') + " of " + str(value)
		outputValue = None
		while(index < len(valueList) and not rangeFound):
			thisIndex = valueList[index]
			if(value < thisIndex):
				outputString += " is less than " + str(thisIndex) + ". Defaulting to " + str(thisIndex) + "."
				outputValue = thisIndex
				rangeFound = True
			index += 1
		if(not rangeFound):
			thisIndex = valueList[-1]
			outputString += " is greater than " + str(thisIndex) + ". Defaulting to " + str(thisIndex) + "."
			outputValue = thisIndex

		print(outputString)
		return outputValue