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
		self.sheetHeight = helpers.kwargExists("sheetHeight", kwargs) or HEIGHT
		self.sheetWidth = helpers.kwargExists("sheetWidth", kwargs) or WIDTH
		self.upperMargin = helpers.kwargExists("upperMargin", kwargs) or UPPER_MARGIN
		self.leftMargin = helpers.kwargExists("leftMargin", kwargs) or LEFT_MARGIN
		self.middlePadding = helpers.kwargExists("middlePadding", kwargs) or MIDDLE_PADDING
		self.labelHeight = helpers.kwargExists("labelHeight", kwargs) or LABEL_HEIGHT
		self.labelWidth = helpers.kwargExists("labelWidth", kwargs) or LABEL_WIDTH
		self.rows = helpers.kwargExists("rows", kwargs) or ROWS
		self.cols = helpers.kwargExists("columns", kwargs) or COLUMNS

	## Properties

	@property
	def sheetHeight(self):
		return self._sheetHeight
	
	@sheetHeight.setter
	def sheetHeight(self, value):
		self._sheetHeight = value

	@property
	def sheetWidth(self):
		return self._sheetWidth
	
	@sheetWidth.setter
	def sheetWidth(self, value):
		self._sheetWidth = value

	@property
	def upperMargin(self):
		return self._upperMargin
	
	@upperMargin.setter
	def upperMargin(self, value):
		self._upperMargin = value

	@property
	def leftMargin(self):
		return self._leftMargin

	@leftMargin.setter
	def leftMargin(self, value):
		self._leftMargin = value

	@property
	def middlePadding(self):
		return self._middlePadding
	
	@middlePadding.setter
	def middlePadding(self, value):
		self._middlePadding = value

	@property
	def labelHeight(self):
		return self._labelHeight
	
	@labelHeight.setter
	def labelHeight(self, value):
		self._labelHeight = value

	@property
	def labelWidth(self):
		return self._labelWidth

	@labelWidth.setter
	def labelWidth(self, value):
		self._labelWidth = value

	@property
	def rows(self):
		return self._rows

	@rows.setter
	def rows(self, value):
		self._rows = value

	@property
	def cols(self):
		return self._cols
		
	@cols.setter
	def cols(self, value):
		self._cols = value