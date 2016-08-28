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