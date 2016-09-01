import helpers

## Default sheet dimensions and layout
HEIGHT = 11
WIDTH = 8.5
UPPER_MARGIN = 0.505
LEFT_MARGIN = 0.517
MIDDLE_PADDING = 0.552
LABEL_HEIGHT = 0.662
LABEL_WIDTH = 3.436
ROWS = 15
COLUMNS = 2

class SheetConfig:
	def __init__(self, **kwargs):
		self.sheetHeight = helpers.kwargExists("sheetHeight", kwargs)
		self.sheetWidth = helpers.kwargExists("sheetWidth", kwargs)
		self.upperMargin = helpers.kwargExists("upperMargin", kwargs)
		self.leftMargin = helpers.kwargExists("leftMargin", kwargs)
		self.middlePadding = helpers.kwargExists("middlePadding", kwargs)
		self.labelHeight = helpers.kwargExists("labelHeight", kwargs)
		self.labelWidth = helpers.kwargExists("labelWidth", kwargs)
		self.rows = helpers.kwargExists("rows", kwargs)
		self.cols = helpers.kwargExists("columns", kwargs)

	## Properties

	@property
	def sheetHeight(self):
		return self._sheetHeight
	
	@sheetHeight.setter
	@helpers.isPositive
	@helpers.isNotNegative
	def sheetHeight(self, value):
		self._sheetHeight = value or HEIGHT

	@property
	def sheetWidth(self):
		return self._sheetWidth
	
	@sheetWidth.setter
	@helpers.isPositive
	def sheetWidth(self, value):
		self._sheetWidth = value or WIDTH

	@property
	def upperMargin(self):
		return self._upperMargin
	
	@upperMargin.setter
	@helpers.isNotNegative
	def upperMargin(self, value):
		self._upperMargin = value or UPPER_MARGIN

	@property
	def leftMargin(self):
		return self._leftMargin

	@leftMargin.setter
	@helpers.isNotNegative
	def leftMargin(self, value):
		self._leftMargin = value or LEFT_MARGIN

	@property
	def middlePadding(self):
		return self._middlePadding
	
	@middlePadding.setter
	@helpers.isNotNegative
	def middlePadding(self, value):
		self._middlePadding = value or MIDDLE_PADDING

	@property
	def labelHeight(self):
		return self._labelHeight
	
	@labelHeight.setter
	@helpers.isPositive
	def labelHeight(self, value):
		self._labelHeight = value or LABEL_HEIGHT

	@property
	def labelWidth(self):
		return self._labelWidth

	@labelWidth.setter
	@helpers.isPositive
	def labelWidth(self, value):
		self._labelWidth = value or LABEL_WIDTH

	@property
	def rows(self):
		return self._rows

	@rows.setter
	@helpers.isPositive
	def rows(self, value):
		self._rows = value or ROWS

	@property
	def cols(self):
		return self._cols
		
	@cols.setter
	@helpers.isPositive
	def cols(self, value):
		self._cols = value or COLUMNS