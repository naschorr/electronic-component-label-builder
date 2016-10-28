import unittest
import dataInput

class TestDataInput(unittest.TestCase):
	dataInputObj = dataInput.Data([])	## Needs path to data file that can be iterated through, so just give it an empty array

	def test_getDataLinesFromFile(self):
		pass

	def test_parseValueFormat(self):
		assertEqualTuples =    [("1", 1),	## Good inputs
								("1  ", 1),
								("  1  ", 1),
								("1k", 1000),
								("1 k", 1000),
								("1 M", 1000000),
								("222", 222),
								("222 k", 222000),
								("222M", 222000000),
								("1.234", 1.234),
								("1.234 k", 1234),
								("1.234k", 1234),
								("  1.234  ", 1.234),
								("  1.234k  ", 1234),
								("abc k", None),	## Bad inputs
								("abck", None),
								("100 a", None),
								("10 K", None),
								("10g", None),
								("3.3 v", None),
								("-3.3 volts", None)]

		for assertion in assertEqualTuples:
			try:
				self.assertEqual(self.dataInputObj.parseValueFormat(assertion[0]), assertion[1])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)

if __name__ == '__main__':
	unittest.main()