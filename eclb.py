import dataGrabber
import componentBuilder
import sheetConfig
import sheetBuilder

def main():
	data = dataGrabber.Data('resources/resistors.txt')
	labels = componentBuilder.Component(data, unitName='Ω').labels
	sheetConf = sheetConfig.SheetConfig()
	sheet = sheetBuilder.SheetBuilder(sheetConf, labels)

if __name__ == '__main__':
	main()