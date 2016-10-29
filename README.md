# electronic-component-label-builder
Generate custom labels for your electronic components with their value and/or color code

### Installation
Clone the repo wherever you would like, then run `pip install -r requirements.txt` from the repo's root directory

### Examples
Note that examples images have been shortened to save space.

Draw the default labels for a set of data (assumes that the components are resistors)
![resistor example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/resistor_example.png?raw=true)
`python eclb.py PATH_TO_COMPONENT_DATA`

Change the units to something else (handy to use with the `--no-color-codes` flag)
![different units example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/units_example.png?raw=true)
`python eclb.py --units Ohm PATH_TO_COMPONENT_DATA` or  
`python eclb.py -u Ohm PATH_TO_COMPONENT_DATA`

Display debug gridlines
![debug example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/debug_example.png?raw=true)
`python eclb.py --debug PATH_TO_COMPONENT_DATA`

Don't display the tolerance band
![no tolerance example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/no_tolerance_example.png?raw=true)
`python eclb.py --no-tolerance PATH_TO_COMPONENT_DATA`

Place three labels on each sticker
![many labels example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/many_labels_example.png?raw=true)
`python eclb.py --labels-per-sticker 3 PATH_TO_COMPONENT_DATA` or  
`python eclb.py -l 3 PATH_TO_COMPONENT_DATA`

Make the text's font size bigger
![big font example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/big_font_example.png?raw=true)
`python eclb.py --font-size 125 PATH_TO_COMPONENT_DATA` or
`python eclb.py -f 125 PATH_TO_COMPONENT_DATA`

Don't display the color code, just the text with a bigger font size
![big font with no color code example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/big_font_no_colors_example.png?raw=true)
`python eclb.py --font-size 150 --no-color-codes PATH_TO_COMPONENT_DATA` or  
`python eclb.py -f 150 --no-color-codes PATH_TO_COMPONENT_DATA`

Change the color code so that it works for resistors with four bands (or, two significant digits)
![bands example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/bands_example.png?raw=true)
`python eclb.py --bands 2 PATH_TO_COMPONENT_DATA` or  
`python eclb.py -b 2 PATH_TO_COMPONENT_DATA`

Assign a temperature value to the component data, and then display each one with two significant digits in the color code (assumes that the component is a capacitor, since temperature is specified)
![capacitor temperature example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/capacitor_temperature_example.png?raw=true)
`python eclb.py --bands 2 --temperature 150 PATH_TO_COMPONENT_DATA` or  
`python eclb.py -b 2 --temperature 150 PATH_TO_COMPONENT_DATA` or, if you manually specify the component  
`python eclb.py --component capacitor --bands 2 --temperature 150 PATH_TO_COMPONENT_DATA` or  
`python eclb.py -c capacitor -b 2 --temperature 150`

Display labels for an inductor with two significant digits in the color code
![inductor example](https://github.com/naschorr/electronic-component-label-builder/blob/master/resources/inductor_example.png?raw=true)
`python eclb.py --bands 2 --component inductor PATH_TO_COMPONENT_DATA` or  
`python eclb.py -b 2 -c inductor PATH_TO_COMPONENT_DATA`

### Commands
`--sheet-height` - The height of the label sheet (inches).  
`--sheet-width` - The width of the label sheet (inches).  
`--upper-margin` - The vertical size of the top-most margin (inches).  
`--left-margin` - The horizontal size of the left-most margin (inches).  
`--middle-padding` - The size of the padding between columns of sticker, if any (inches).  
`--label-height` - The height of an individual sticker (inches).  
`--label-width` - The width of an individual sticker (inches).  
`--rows` - The number of rows on the sticker sheet.  
`--columns` - The number of columns on the sticker sheet.  
`--units`, `-u` - The units of the component to be labeled (Ohm, Ω, Farad, etc).  
`--tolerance`, `-t` - The tolerance of the component to be labeled (in percentage).  
`--bands`, `-b` - The number of bands to use for displaying the significant digits of the component value.  
`--condense/--no-condense` - Choose whether or not to condense the component value down (ex. 1000 -> 1k).  
`--color-codes/--no-color-codes` - Choose to show the color code or not.  
`--show-tolerance/--no-tolerance` - Choose to show a tolerance band in the color code.  
`--voltage` - The voltage rating for the capacitors.  
`--temperature` - The temperature coefficient of the capacitors.  
`--component`, `-c` - Overrides any other options, and tries to make components of that type.  
`--scale`, `-s` - The scale for rendering the sticker sheet. Bigger scale means higher resolution. Might have to play around with this to get the units to work.  
`--output-format`, `-o` - Image type to save the sticker sheet as.  
`--font` - Path to the font to use in label text.  
`--font-size`, `-f` - The size of the font used on the labels (as a percentage, ex. 100 is default).  
`--box-size` - The size of the boxes that hold color bands (inches).  
`--box-spacer-width` - The size of the spacer between the color band boxes (inches).  
`--labels-per-sticker`, `-l` - The number of labels to place in each sticker.  
`--label-text-offset` - The veritcal distance to offset label text (pixels) (Positive values offset it down, and negatives offset it up.)  
`--label-colorcode-offset` - The vertical distance to offset label color codes (pixels) (Positive values offset it down, and negatives offset it up.)  
`--debug/--no-debug` - Choose to render debug gridlines on the sticker sheet (Helps with alignment).  
`--show/--no-show` - Choose to show a preview of the resulting image.  
`--dry-run/--no-dry-run` - Choose to save the resulting images or not.  
