from math import ceil
from PIL import Image, ImageDraw, ImageFont

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
	def __init__(
			self, sheetConfig, labels, outputType=OUTPUT_TYPE, font=FONT,
			fontSize=FONT_SIZE, boxSize=BOX_SIZE, boxSpacerWidth=BOX_SPACER_WIDTH,
			labelsPerSticker=LABELS_PER_STICKER, labelTextOffset=LABEL_TEXT_OFFSET,
			labelColorCodeOffset=LABEL_COLORCODE_OFFSET, scale=SCALE, debug=DEBUG):
		self._sheetConfig = sheetConfig
		self._labels = labels
		self._outputType = outputType
		self._font = font
		self._fontSize = fontSize
		self._boxSize = boxSize
		self._boxSpacerWidth = boxSpacerWidth
		self._labelsPerSticker = labelsPerSticker
		self._labelTextOffset = labelTextOffset
		self._labelColorCodeOffset = labelColorCodeOffset
		self._scale = scale
		self._debug = debug

		self.drawSheet()

	## Properties

	@property
	def sheetConfig(self):
		return self._sheetConfig
	
	@property
	def labels(self):
		return self._labels

	@property
	def outputType(self):
		return self._outputType
	
	@property
	def font(self):
		return self._font

	@property
	def fontSize(self):
		return self._fontSize

	@property
	def boxSize(self):
		return self._boxSize

	@property
	def boxSpacerWidth(self):
		return self._boxSpacerWidth

	@property
	def labelsPerSticker(self):
		return self._labelsPerSticker

	@property
	def labelTextOffset(self):
		return self._labelTextOffset
	
	@property
	def labelColorCodeOffset(self):
		return self._labelColorCodeOffset
	
	@property
	def scale(self):
		return self._scale

	@property
	def debug(self):
		return self._debug
	
	## Methods

	def getLabelBounds(self, row, col):
		sc = self.sheetConfig
		topLeftX = (sc.leftMargin+col*sc.labelWidth+col*sc.middlePadding)*self.scale
		topLeftY = (sc.upperMargin+row*sc.labelHeight)*self.scale
		botRightX = topLeftX+(sc.labelWidth)*self.scale-1
		botRightY = topLeftY+(sc.labelHeight)*self.scale-1
		return topLeftX, topLeftY, botRightX, botRightY

	def drawColorCode(self, draw, colorCode, centerX, centerY):
		colorCodeWidth = (len(colorCode)*self.boxSize+(len(colorCode)-1)*self.boxSpacerWidth)*self.scale
		colorCodeHeight = self.boxSize*self.scale
		topLeftX = centerX - colorCodeWidth/2
		topLeftY = centerY - colorCodeHeight/2
		scaledBox = self.boxSize*self.scale
		for box, color in enumerate(colorCode):
			draw.rectangle([topLeftX + box*(scaledBox+self.boxSpacerWidth*self.scale), topLeftY, topLeftX + box*(scaledBox+self.boxSpacerWidth*self.scale) + scaledBox, topLeftY + scaledBox], color, 'black')

	def drawDebug(self, image, draw):
		sc = self.sheetConfig
		## Draw the horizontal and vertical rules on the sheet
		for h in range(0, int(sc.sheetWidth*self.scale), int(0.5*self.scale)):
			length = 0.4*self.scale
			if(h % 100):
				length = 0.25*self.scale
			draw.line([h, 0, h, length], "black", 1)
		for w in range(0, int(sc.sheetHeight*self.scale), int(0.5*self.scale)):
			length = 0.4*self.scale
			if(w % 100):
				length = 0.25*self.scale
			draw.line([0, w, length, w], "black", 1)

		## Draw the boundary of the sheet
		draw.rectangle([0, 0, sc.sheetWidth*self.scale-1, sc.sheetHeight*self.scale-1], None, 'red')

		## Draw the boundary of the area between the margins
		draw.rectangle([sc.leftMargin*self.scale, sc.upperMargin*self.scale, (sc.sheetWidth-sc.leftMargin)*self.scale-1, (sc.sheetHeight-sc.upperMargin)*self.scale-1], None, 'green')

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
						labelText = self.labels[0].text
						textWidth, textHeight = ttf.getsize(labelText)
						
						labelXPositionSection = (sc.labelWidth*self.scale)/(self.labelsPerSticker*2)
						labelXCenter = topLeftX + labelXPositionSection + labelCounter*(labelXPositionSection*2)

						textYOffset = topLeftY + (sc.labelHeight*self.scale)/4 - textHeight/2 + self.labelTextOffset*self.scale
						colorCodeYOffset = topLeftY + 3*((sc.labelHeight*self.scale)/4) + self.labelColorCodeOffset*self.scale

						draw.text((labelXCenter - textWidth/2, textYOffset), labelText, font=ttf, fill="black")
						self.drawColorCode(draw, self.labels[0].colorCode, labelXCenter, colorCodeYOffset)

						del self.labels[0]
						labelCounter += 1
					colCounter += 1
				rowCounter += 1

			sheets.append(image)
			sheetSize = (int(self.sheetConfig.sheetWidth*self.scale), int(self.sheetConfig.sheetHeight*self.scale))
			image = Image.new('RGB', sheetSize, 'white')
			draw = ImageDraw.Draw(image)

		return sheets

	def saveSheets(self, sheets):
		for counter, image in enumerate(sheets):
			#image.save("eclb_" + str(counter) + self.outputType)
			image.show()

	def drawSheet(self):
		sheetSize = (int(self.sheetConfig.sheetWidth*self.scale), int(self.sheetConfig.sheetHeight*self.scale))
		image = Image.new('RGB', sheetSize, 'white')
		draw = ImageDraw.Draw(image)
		ttf = ImageFont.truetype(self.font, self.fontSize)

		if(self.debug):
			self.drawDebug(image, draw)
		sheets = self.drawLabels(image, draw, ttf)
		self.saveSheets(sheets)

		del draw