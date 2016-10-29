from re import match, search
from os import pardir
import os.path

file = os.path.join(os.path.dirname(__file__), pardir, "eclb.py")

def parseOptionIndex(string):
	return search(r'\'(.+?)\'', string)


def parseOption(string):
	return match(r'@click.option\((.+)\)', string)


def stringToList(string):
	indecies = []

	parsed = parseOptionIndex(string)
	groupEnd = False
	while(not groupEnd):
		try:
			indecies.append(parsed.group(1))
			string = string[parsed.end():]
			parsed = parseOptionIndex(string)
		except (IndexError, AttributeError):
			groupEnd = True

	return indecies


def main():
	with open(file, 'r') as f:
		for line in f:
			option = parseOption(line)
			if(option):
				optionList = stringToList(option.group(1))

				if(optionList[1] != optionList[-1]):
					command = optionList[0] + "`, `" + optionList[1]
				else:
					command = optionList[0]
				print("`{0}` - {1}  ".format(command, optionList[-1]))

if(__name__ == '__main__'):
	main()
