import unittest
import dataInput
import componentBuilder

class TestComponentBuilder(unittest.TestCase):
	## componentBuilder Needs the dataLines iterable from dataInput, so just build an empty one.
	dataInputObj = dataInput.Data([])

	def test_guessComponent(self):
		assertEqualTuples = [({"voltage":componentBuilder.VOLTAGE}, componentBuilder.CAPACITOR_STR),
							({"temperature":componentBuilder.TEMPERATURE}, componentBuilder.CAPACITOR_STR),
							({"voltage":componentBuilder.VOLTAGE, "temperature":componentBuilder.TEMPERATURE}, componentBuilder.CAPACITOR_STR),
							({}, componentBuilder.RESISTOR_STR)]

		for assertion in assertEqualTuples:
			try:
				self.assertEqual(componentBuilder.Component(self.dataInputObj, **assertion[0]).guessComponent(), assertion[1])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_setUnits(self):
		assertEqualTuples = [({"component":componentBuilder.CAPACITOR_STR}, componentBuilder.CAPACITOR_UNITS),
							({"component":componentBuilder.INDUCTOR_STR}, componentBuilder.INDUCTOR_UNITS),
							({"component":componentBuilder.RESISTOR_STR}, componentBuilder.RESISTOR_UNITS),
							({"component":"invalid"}, componentBuilder.RESISTOR_UNITS),
							({}, componentBuilder.RESISTOR_UNITS)]
		
		for assertion in assertEqualTuples:
			try:
				self.assertEqual(componentBuilder.Component(self.dataInputObj, **assertion[0]).setUnits(), assertion[1])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_getFractionalDigitCount(self):
		componentBuilderObj = componentBuilder.Component(self.dataInputObj)
		assertEqualTuples =    [(1, 0),
								(100, 0),
								(0.0, 0),
								(0.1, 1),
								(0.01, 2),
								(0.00001, 5)]

		for assertion in assertEqualTuples:
			try:
				self.assertEqual(componentBuilderObj.getFractionalDigitCount(assertion[0]), assertion[1])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_condenseValue(self):
		componentBuilderObj = componentBuilder.Component(self.dataInputObj)
		assertEqualTuples =    [(1, "1", 0),
								(100, "100", 0),
								(1000, "1", 1),
								(1000000, "1", 2),
								(100000.123, "100.000123", 1),
								(0.1, "0.1", 0),
								(0.001, "1", -1),
								(0.000001, "1", -2),
								(0.00001234, "0.01234", -1)]

		for assertion in assertEqualTuples:
			try:
				valueStr, count = componentBuilderObj.condenseValue(assertion[0])
				self.assertEqual(valueStr, assertion[1])
				self.assertEqual(count, assertion[2])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_getLeadingDigits(self):
		componentBuilderObj = componentBuilder.Component(self.dataInputObj)
		assertEqualTuples =    [(1, 100),
								(100, 100),
								(10000, 100),
								(220, 220),
								(1.2345, 123),
								(0.123, 123),
								(0, 000)]

		for assertion in assertEqualTuples:
			try:
				self.assertEqual(componentBuilderObj.getLeadingDigits(assertion[0], len(str(assertion[1]))), assertion[1])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_buildLabelName(self):
		## Capacitors start out in the pFarads, inductors start out in the uHenries
		farad = componentBuilder.CAPACITOR_UNITS
		henry = componentBuilder.INDUCTOR_UNITS
		ohm = componentBuilder.RESISTOR_UNITS
		capacitor = componentBuilder.CAPACITOR_STR
		inductor = componentBuilder.INDUCTOR_STR
		resistor = componentBuilder.RESISTOR_STR
		## This is lazy and bad, but i'll fix it later.
		assertEqualTuples =    [(1, "1 p", farad, capacitor),
								(100, "100 p", farad, capacitor),
								(10000, "10 n", farad, capacitor),
								(1000000, "1 µ", farad, capacitor),
								(1.2345, "1.2345 p", farad, capacitor),
								(0, "0 p", farad, capacitor),
								(1, "1 µ", henry, inductor),
								(100, "100 µ", henry, inductor),
								(1000, "1 m", henry, inductor),
								(1000000, "1 ", henry, inductor),
								(0.001, "1 n", henry, inductor),
								(1.2345, "1.2345 µ", henry, inductor),
								(0, "0 ", ohm, resistor),
								(1, "1 ", ohm, resistor),
								(2.2, "2.2 ", ohm, resistor),
								(100, "100 ", ohm, resistor), 
								(1000, "1 k", ohm, resistor),
								(1000000, "1 M", ohm, resistor),
								(1000000000, "1 G", ohm, resistor),
								(0.001, "1 m", ohm, resistor), 
								(0.000001, "1 µ", ohm, resistor),
								(0.000000001, "1 n", ohm, resistor),
								(0.000000000001, "1 p", ohm, resistor)]

		for assertion in assertEqualTuples:
			try:
				self.assertEqual(componentBuilder.Component(self.dataInputObj, condense=True, component=assertion[3]).buildLabelName(assertion[0]), assertion[1] + assertion[2])
				self.assertEqual(componentBuilder.Component(self.dataInputObj, condense=False, component=assertion[3]).buildLabelName(assertion[0]), str(assertion[0]) + assertion[2])
			except AssertionError as ae:
				## Catch the error and dump some useful info, then re-raise it so that the test still fails.
				print("AssertionError: {0} for input {1}".format(ae, assertion))
				raise AssertionError(ae)


	def test_buildBaseColorCode(self):
		pass

	def test_buildOptionsColorCode(self):
		pass

	def test_buildLabelColorCode(self):
		pass

	def test_buildComponentLabel(self):
		pass

if __name__ == '__main__':
	unittest.main()