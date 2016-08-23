import click

import dataGrabber
import componentBuilder
import sheetConfig
import sheetBuilder

@click.command()
@click.argument('path-to-component-data', type=click.File('r'))
@click.option('--sheet-height', type=float, help='The height of the label sheet. (inches)')		# sheetConfig
@click.option('--sheet-width', type=float, help='The width of the label sheet. (inches)')
@click.option('--upper-margin', type=float, help='The vertical size of the top-most margin. (inches)')
@click.option('--left-margin', type=float, help='The horizontal size of the left-most margin. (inches)')
@click.option('--middle-padding', type=float, help='The size of the padding between columns of sticker, if any. (inches)')
@click.option('--label-height', type=float, help='The height of an individual sticker. (inches)')
@click.option('--label-width', type=float, help='The width of an individual sticker. (inches)')
@click.option('--rows', type=int, help='The number of rows on the sticker sheet.')
@click.option('--columns', type=int, help='The number of columns on the sticker sheet.')
@click.option('--units', '-u', help='The units of the component to be labeled. (Ohm, Ω, Farad, etc.)')		# componentBuilder
@click.option('--tolerance', '-t', type=float, help='The tolerance of the component to be labeled. (in percentage)')
@click.option('--bands', '-b', type=int, help='The number of color bands on the component to be labeled.')
@click.option('--condense/--no-condense', default=True, help="Choose whether or not to condense the component's value down. (ex. 10000 -> 1k)")
@click.option('--color-codes/--no-color-codes', default=True, help='Choose to show the color code or not.')
@click.option('--scale', '-s', type=int, help='The scale for rendering the sticker sheet. Bigger scale means higher resolution. Might have to play around with this to get the units to work.')		# sheetBuilder
@click.option('--output-format', '-o', help='Image type to save the sticker sheet as.')
@click.option('--font', type=click.Path(exists=True), help='Path to the font to use in label text.')
@click.option('--font-size', '-f', type=int, help='The size of the font used on the labels.')
@click.option('--box-size', type=float, help='The size of the boxes that hold color bands. (inches)')
@click.option('--box-spacer-width', type=float, help='The size of the spacer between the color band boxes. (inches)')
@click.option('--labels-per-sticker', '-l', type=int, help='The number of labels to place in each sticker.')
@click.option('--label-text-offset', type=float, help='The veritcal distance to offset label text. (Positive values offset it down, and negatives offset it up.)')
@click.option('--label-colorcode-offset', type=float, help='The vertical distance to offset label color codes. (Positive values offset it down, and negatives offset it up.)')
@click.option('--debug/--no-debug', default=False, help='Choose to render debug gridlines on the sticker sheet. (Helps with alignment)')
def main(
		path_to_component_data, sheet_height, sheet_width, upper_margin, 
		left_margin, middle_padding, label_height, label_width, rows, columns,
		units, tolerance, bands, condense, color_codes, scale, output_format,
		font, font_size, box_size, box_spacer_width, labels_per_sticker, 
		label_text_offset, label_colorcode_offset, debug):

	sheetConfigArgs = {
		"sheetHeight":sheet_height, "sheetWidth":sheet_width, "upperMargin":upper_margin,
		"leftMargin":left_margin, "middlePadding":middle_padding, "labelHeight":label_height,
		"labelWidth":label_width, "rows":rows, "columns":columns
	}

	componentBuilderArgs = {
		"unitName":units, "tolerance":tolerance, "bandCount":bands, "condense":condense,
		"showColorCodes":color_codes
	}

	sheetBuilderArgs = {
		"scale":scale, "outputType":output_format, "font":font, "fontSize":font_size, 
		"boxSize":box_size, "boxSpacerWidth":box_spacer_width, 
		"labelsPerSticker":labels_per_sticker, "labelTextOffset":label_text_offset, 
		"labelColorCodeOffset":label_colorcode_offset, "debug":debug
	}

	data = dataGrabber.Data(path_to_component_data)
	labels = componentBuilder.Component(data, **componentBuilderArgs).labels
	sheetConf = sheetConfig.SheetConfig(**sheetConfigArgs)
	sheet = sheetBuilder.SheetBuilder(sheetConf, labels, **sheetBuilderArgs)

if __name__ == '__main__':
	main()