import sys
import os.path
import inspect
import unittest

## Assumes this file is at /electronic-component-label-builder/testing/testRunner.py
## Then, it just adds the /electronic-component-label-builder/ directory to the PYTHONPATH so the tests can be run
sys.path.append(os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2]))

import componentBuilderTest
import dataInputTest
import sheetBuilderTest

def discoverTestCases():
	testCases = []
	for moduleName, module in inspect.getmembers(sys.modules[__name__], inspect.ismodule):
		for clsName, cls in inspect.getmembers(module, inspect.isclass):
			if(unittest.TestCase.__name__ in [base.__name__ for base in cls.__bases__] and moduleName != unittest.__name__):
				testCases.append(cls)
	
	if(not testCases):
		print("Didn't find any test cases. Are they in the correct directory, and are they built with Python's unittest module?")

	return testCases


def buildTestSuite(testCases):
	suite = unittest.TestSuite()
	for testCase in testCases:
		suite.addTest(unittest.makeSuite(testCase))

	return suite


def main():
	runner = unittest.TextTestRunner()
	runner.run(buildTestSuite(discoverTestCases()))

if __name__ == "__main__":
	main()