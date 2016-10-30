from re import match, search
from os import pardir
import os.path

file = os.path.join(os.path.dirname(__file__), pardir, "eclb.py")

def parseOption(string):
	return match(r'@click.option\((.+)\)', string)


def parseOptionIndex(string):
	return search(r'\'(.+?)\'', string)


def getOptionType(string):
	optionType = search(r'type=(.+?),', string)
	if(optionType):
		return optionType.group(1)
	else:
		return None


def getOptionDefault(string):
	defaultType = search(r'default=(.+?),', string)
	if(defaultType):
		return defaultType.group(1)
	else:
		return None


def stringToElements(string):
	## Todo: Return an object with attributes for each part of the option
	##	(ex. command[], type, default, helpText)
	elements = []

	optionType = getOptionType(string)
	optionDefault = getOptionDefault(string)

	parsed = parseOptionIndex(string)
	groupEnd = False
	while(not groupEnd):
		try:
			elements.append(parsed.group(1))
			string = string[parsed.end():]
			parsed = parseOptionIndex(string)
		except (IndexError, AttributeError):
			groupEnd = True

	return (elements, optionType, optionDefault)


def main():
	## I'm aware that this is ugly and bad... I'll fix it later.
	with open(file, 'r') as f:
		for line in f:
			option = parseOption(line)
			if(option):
				optionElements = stringToElements(option.group(1))

				helpText = optionElements[0][-1]
				if(optionElements[0][1] != helpText):
					command = optionElements[0][0] + "`, `" + optionElements[0][1]
				else:
					command = optionElements[0][0]
				optionType = ""
				if(optionElements[1] and not "click" in optionElements[1]):
					optionType = " - " + optionElements[1].upper()
				optionDefault = ""
				if(optionElements[2]):
					optionDefault = " Defaults to `" + optionElements[2] + "`."

				print("`{0}`{1} - {2}{3}  ".format(command, optionType, helpText, optionDefault))


if(__name__ == '__main__'):
	main()
