def isTest():
	import inspect
	import unittest

	frames = inspect.getouterframes(inspect.currentframe())

	unittestFound = False
	frameIndex = 0
	while(not unittestFound and frameIndex < len(frames)):
		## Lazy, but it works
		if(unittest.__name__ in frames[frameIndex][1]):
			unittestFound = True
		frameIndex += 1
	
	return unittestFound


def eclbPrint(*args):
	if(not isTest()):
		print(*args)


def kwargExists(kwarg, kwargs):
			if kwarg in kwargs:
				if(kwargs[kwarg] is not None):
					return kwargs[kwarg]
			return None


def setBoolKwarg(kwargString, kwargs, defaultValue):
	kwargState = kwargExists(kwargString, kwargs)
	if(kwargState is not None):
		return kwargState
	else:
		return defaultValue


def strip(string):
	return string.rstrip().lstrip()


## Inclusive range
def incRange(first, *args):
	argLen = len(args)

	if(argLen is 0):
		return range(first + 1)
	elif(argLen is 1):
		return range(first, args[0] + 1)
	elif(argLen is 2):
		step = args[1]
		return range(first, args[0] + step, step)
	else:
		## Raise similar exception to the normal range function
		raise TypeError('incRange expected at most 3 arguments, got {0}'.format(argLen + 1))


## Test to see if the value is in the range of values. If not, return a valid value in the list.
def testForRange(value, valueList, valueName='value'):
	if(value in valueList):
		return value
	else:
		## Go ahead and sort the incoming list to prevent it from defaulting to a too high value.
		valueList = sorted(valueList)

		outputString = "Supplied " + valueName + " of " + str(value)
		index = 0
		rangeFound = False
		## Tries to find the smallest number in the list that's bigger than the test value.
		while(index < len(valueList) and not rangeFound):
			thisIndex = valueList[index]
			if(value < thisIndex):
				outputString += " is less than " + str(thisIndex) + ". Defaulting to " + str(thisIndex) + "."
				outputValue = thisIndex
				rangeFound = True
			index += 1

		## If a number wasn't found, then default to the largest number in the list.
		if(not rangeFound):
			thisIndex = valueList[-1]
			outputString += " is greater than " + str(thisIndex) + ". Defaulting to " + str(thisIndex) + "."
			outputValue = thisIndex

		eclbPrint(outputString)
		return outputValue


def checkType(value, desiredType, castableTypes=[]):
	if(value is None):
		return None
	if(isinstance(value, desiredType)):
		return value
	else:
		for typeIndex in castableTypes:
			if(isinstance(value, typeIndex)):
				return desiredType(value)
	return None


## Meant to be used as a decorator
def isInt(func):
	def wrapper(*args):
		self = args[0]
		value = checkType(args[1], int, [float])
		return func(self, value)
	return wrapper


## Meant to be used as a decorator
def isFloat(func):
	def wrapper(*args):
		self = args[0]
		value = checkType(args[1], float, [int])
		return func(self, value)
	return wrapper


## Meant to be used as a decorator
def isBool(func):
	def wrapper(*args):
		self = args[0]
		value = checkType(args[1], bool)
		return func(self, value)
	return wrapper


## Meant to be used as a decorator
def isStr(func):
	def wrapper(*args):
		self = args[0]
		value = checkType(args[1], str)
		return func(self, value)
	return wrapper


## Meant to be used as a decorator
def isPositive(func):
	def wrapper(*args):
		self = args[0]
		value = args[1]
		if(value is not None):
			if(value > 0):
				return func(self, value)
		return func(self, None)
	return wrapper


## Meant to be used as a decorator
def isNotNegative(func):
	def wrapper(*args):
		self = args[0]
		value = args[1]
		if(value is not None):
			if(value >= 0):
				return func(self, value)
		return func(self, None)
	return wrapper
