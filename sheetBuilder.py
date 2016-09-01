from math import ceil
from PIL import Image, ImageDraw, ImageFont

import helpers

## Defaults
OUTPUT_TYPE = ".png"
FONT = "resources/Arial.ttf"
FONT_SIZE = 100
BOX_SIZE = 0.15
BOX_SPACER_WIDTH = 0.05
LABELS_PER_STICKER = 2
LABEL_TEXT_OFFSET = 0.05
LABEL_COLORCODE_OFFSET = -0.05
SCALE = 500
DEBUG = False

class SheetBuilder:
	def __init__(self, sheetConfig, labels, **kwargs):
		## Load scale first so that it can be used to modify other incoming values
		self.scale = helpers.kwargExists("scale", kwargs)
		
		self.sheetConfig = sheetConfig
		self.labels = labels

		self.outputType = helpers.kwargExists("outputType", kwargs)
		self.font = helpers.kwargExists("font", kwargs)
		self.fontSize = helpers.kwargExists("fontSize", kwargs)
		self.boxSize = helpers.kwargExists("boxSize", kwargs)
		self.boxSpacerWidth = helpers.kwargExists("boxSpacerWidth", kwargs)
		self.labelsPerSticker = helpers.kwargExists("labelsPerSticker", kwargs)
		self.labelTextOffset = helpers.kwargExists("labelTextOffset", kwargs)
		self.labelColorCodeOffset = helpers.kwargExists("labelColorCodeOffset", kwargs)
		self.debug = helpers.setBoolKwarg("debug", kwargs, DEBUG)

		self.drawSheet()

	## Properties

	@property
	def scale(self):
		return self._scale

	@scale.setter
	@helpers.isPositive
	def scale(self, value):
		self._scale = value or SCALE

	@property
	def sheetConfig(self):
		return self._sheetConfig
	
	@sheetConfig.setter
	def sheetConfig(self, value):
		## Update the sheetConfig's attributes by scaling up
		value.sheetHeight *= self.scale
		value.sheetWidth *= self.scale
		value.upperMargin *= self.scale
		value.leftMargin *= self.scale
		value.middlePadding *= self.scale
		value.labelHeight *= self.scale
		value.labelWidth *= self.scale
		self._sheetConfig = value

	@property
	def labels(self):
		return self._labels

	@labels.setter
	def labels(self, value):
		self._labels = value

	@property
	def outputType(self):
		return self._outputType
	
	@outputType.setter
	def outputType(self, value):
		self._outputType = value or OUTPUT_TYPE

	@property
	def font(self):
		return self._font

	@font.setter
	def font(self, value):
		self._font = value or FONT

	@property
	def fontSize(self):
		return self._fontSize

	@fontSize.setter
	@helpers.isPositive
	def fontSize(self, value):
		self._fontSize = value or FONT_SIZE

	@property
	def boxSize(self):
		return self._boxSize

	@boxSize.setter
	@helpers.isPositive
	def boxSize(self, value):
		self._boxSize = (value or BOX_SIZE) * self.scale

	@property
	def boxSpacerWidth(self):
		return self._boxSpacerWidth

	@boxSpacerWidth.setter
	@helpers.isNotNegative
	def boxSpacerWidth(self, value):
		self._boxSpacerWidth = (value or BOX_SPACER_WIDTH) * self.scale

	@property
	def labelsPerSticker(self):
		return self._labelsPerSticker

	@labelsPerSticker.setter
	@helpers.isPositive
	def labelsPerSticker(self, value):
		self._labelsPerSticker = value or LABELS_PER_STICKER

	@property
	def labelTextOffset(self):
		return self._labelTextOffset

	@labelTextOffset.setter
	@helpers.isNotNegative
	def labelTextOffset(self, value):
		self._labelTextOffset = (value or LABEL_TEXT_OFFSET) * self.scale
	
	@property
	def labelColorCodeOffset(self):
		return self._labelColorCodeOffset

	@labelColorCodeOffset.setter
	@helpers.isNotNegative
	def labelColorCodeOffset(self, value):
		self._labelColorCodeOffset = (value or LABEL_COLORCODE_OFFSET) * self.scale

	@property
	def debug(self):
		return self._debug

	@debug.setter
	def debug(self, value):
		self._debug = value or DEBUG
	
	## Methods

	def getLabelBounds(self, row, col):
		sc = self.sheetConfig
		topLeftX = sc.leftMargin+col*sc.labelWidth+col*sc.middlePadding
		topLeftY = sc.upperMargin+row*sc.labelHeight
		botRightX = topLeftX+sc.labelWidth-1
		botRightY = topLeftY+sc.labelHeight-1
		return topLeftX, topLeftY, botRightX, botRightY

	def drawColorCode(self, draw, colorCode, centerX, centerY):
		## Determine overall width of the color code boxes, then get the top left corner's coorderinates from that.
		colorCodeWidth = len(colorCode)*self.boxSize+(len(colorCode)-1)*self.boxSpacerWidth
		topLeftX = centerX - colorCodeWidth/2
		topLeftY = centerY - self.boxSize/2
		## Draw the boxes with 
		for box, color in enumerate(colorCode):
			draw.rectangle([topLeftX + box*(self.boxSize+self.boxSpacerWidth), topLeftY, topLeftX + box*(self.boxSize+self.boxSpacerWidth) + self.boxSize, topLeftY + self.boxSize], color, 'black')

	def drawDebug(self, image, draw):
		sc = self.sheetConfig
		## Draw the horizontal and vertical rules on the sheet
		for h in range(0, int(sc.sheetWidth), int(0.5*self.scale)):
			length = 0.4*self.scale
			if(h % 100):
				length = 0.25*self.scale
			draw.line([h, 0, h, length], "black", 1)
		for w in range(0, int(sc.sheetHeight), int(0.5*self.scale)):
			length = 0.4*self.scale
			if(w % 100):
				length = 0.25*self.scale
			draw.line([0, w, length, w], "black", 1)

		## Draw the boundary of the sheet
		draw.rectangle([0, 0, sc.sheetWidth-1, sc.sheetHeight-1], None, 'red')

		## Draw the boundary of the area between the margins
		draw.rectangle([sc.leftMargin, sc.upperMargin, sc.sheetWidth-sc.leftMargin-1, sc.sheetHeight-sc.upperMargin-1], None, 'green')

		## Draw the boundary of the individual stickers
		for row in range(sc.rows):
			for col in range(sc.cols):
				topLeftX, topLeftY, botRightX, botRightY = self.getLabelBounds(row, col)
				draw.rectangle([topLeftX, topLeftY, botRightX, botRightY], None, 'blue')

	def drawLabels(self, image, draw, ttf):
		sc = self.sheetConfig

		sheets = []
		for sheet in range(ceil(len(self.labels)/(sc.rows*sc.cols*self.labelsPerSticker))):
			rowCounter = 0
			while(rowCounter < sc.rows):
				colCounter = 0
				while(colCounter < sc.cols):
					labelCounter = 0
					topLeftX, topLeftY, botRightX, botRightY = self.getLabelBounds(rowCounter, colCounter)
					while(labelCounter < self.labelsPerSticker and len(self.labels) > 0):
						## Determine the label's text and color code positions
						labelText = self.labels[0].text
						textWidth, textHeight = ttf.getsize(labelText)
						
						labelXPositionSection = (sc.labelWidth)/(self.labelsPerSticker*2)
						labelXCenter = topLeftX + labelXPositionSection + labelCounter*(labelXPositionSection*2)

						textYOffset = topLeftY + sc.labelHeight/4 - textHeight/2 + self.labelTextOffset

						if(self.labels[0].colorCode is None):
							textYOffset += sc.labelHeight/4
							## Just draw the label's text, but centered
							draw.text((labelXCenter - textWidth/2, textYOffset), labelText, font=ttf, fill="black")
						else:
							colorCodeYOffset = topLeftY + 3*((sc.labelHeight)/4) + self.labelColorCodeOffset
							## Draw the label's text and color code
							draw.text((labelXCenter - textWidth/2, textYOffset), labelText, font=ttf, fill="black")
							self.drawColorCode(draw, self.labels[0].colorCode, labelXCenter, colorCodeYOffset)

						## Delete the just recently drawn label from the array
						del self.labels[0]
						labelCounter += 1
					colCounter += 1
				rowCounter += 1

			## For every new sheet...
			sheets.append(image)
			sheetSize = (int(self.sheetConfig.sheetWidth), int(self.sheetConfig.sheetHeight))
			image = Image.new('RGB', sheetSize, 'white')
			draw = ImageDraw.Draw(image)

		return sheets

	def saveSheets(self, sheets):
		for counter, image in enumerate(sheets):
			#image.save("eclb_" + str(counter) + self.outputType)
			image.show()

	def drawSheet(self):
		sheetSize = (int(self.sheetConfig.sheetWidth), int(self.sheetConfig.sheetHeight))
		image = Image.new('RGB', sheetSize, 'white')
		draw = ImageDraw.Draw(image)
		ttf = ImageFont.truetype(self.font, self.fontSize)

		if(self.debug):
			self.drawDebug(image, draw)
		sheets = self.drawLabels(image, draw, ttf)
		self.saveSheets(sheets)

		del draw