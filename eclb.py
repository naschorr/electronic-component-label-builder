import dataGrabber
import componentBuilder
import sheetConfig
import sheetBuilder

DATA_PATH = 'resources/resistors.txt'

def main():
	data = dataGrabber.Data(DATA_PATH)
	labels = componentBuilder.Component(data, 'Ω').labels
	sheetConf = sheetConfig.SheetConfig()
	sheet = sheetBuilder.SheetBuilder(sheetConf, labels)

if __name__ == '__main__':
	main()