## Default sheet dimensions
HEIGHT = 11
WIDTH = 8.5
UPPER_MARGIN = 0.493
LEFT_MARGIN = 0.527
MIDDLE_PADDING = 0.560
LABEL_HEIGHT = 0.659
LABEL_WIDTH = 3.438
ROWS = 15
COLUMNS = 2

class SheetConfig:
	def __init__(
			self, sheetHeight=HEIGHT, sheetWidth=WIDTH, upperMargin=UPPER_MARGIN, 
			leftMargin=LEFT_MARGIN, labelHeight=LABEL_HEIGHT, labelWidth=LABEL_WIDTH, 
			sheetRows=ROWS, sheetColumns=COLUMNS):
		self._sheetHeight = sheetHeight
		self._sheetWidth = sheetWidth
		self._upperMargin = upperMargin
		self._leftMargin = leftMargin
		self._labelHeight = labelHeight
		self._labelWidth = labelWidth
		self._rows = sheetRows
		self._cols = sheetColumns

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