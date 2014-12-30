from PIL import Image, ImageDraw, ImageFont

## Using Avery 8593 White File-Folder Labels

## Sheet dimensions
SHEET_W = 8.5
SHEET_H = 11

## Sheet margins
UPPER_MARGIN = 0.472
LOWER_MARGIN = 0.472
LEFT_MARGIN = 0.512
RIGHT_MARGIN = 0.512

## Width of middle separator (between columns of labels)
MIDDLE_DIV = 0.551

## Label dimensions
LABEL_W = 3.438
LABEL_H = 0.666

## Font size
FONT = 18

## Text padding inside the labels
PADDING = .2

## Number of labels to split each label into
SUBLABELS = 2 ## TODO ADD WORKING SUBLABEL FUNCTIONALITY

## Number of rows in each label column
ROWS = 15

## Number of columns in each sheet
COLUMNS = 2

## Modifier for all scale values (should produce a higher resolution image)
SCALE_MOD = 100

## Resistor values to generate labels for
##RESISTORS = [1, 2.2, 4.7, 5.6, 7.5, 8.2, 10, 15, 22, 27,
##             33, 39, 47, 56, 68, 75, 82, 100, 120, 150,
##             180, 220, 270, 330, 390, 470, 510, 680, 820,
##             1000, 1500, 2200, 3300, 3900, 4700, 5600,
##             6800, 7500, 8200, 10000, 15000, 22000, 33000,
##             39000, 47000, 56000, 68000, 75000, 82000,
##             10000, 150000, 180000, 220000, 330000, 470000,
##             560000, 680000, 1000000, 1500000, 2000000,
##             3300000, 4700000, 5600000, 10000000]

## My container only has 24 slots, so we're going to use the 24 smallest resistors.
RESISTORS = [1, 2.2, 4.7, 5.6, 7.5, 8.2, 10, 15, 22, 27,
             33, 39, 47, 56, 68, 75, 82, 100, 120, 150,
             180, 220, 270, 330]

## Resistor band colors (index in list cooresponds to digit)
DIGIT = ["black", "brown", "red", "orange", "yellow", "green",
         "blue", "purple", "gray", "white"]

## Resistor band color map to multiplier
MULTIPLIER = {"black":1, "brown":10, "red":100, "orange":1000,
              "yellow":10000, "green":100000, "blue":1000000,
              "purple":10000000, "gray":100000000,
              "white":1000000000, "gold":0.1, "silver":0.01}

def int_list_to_int( int_list ):
    return int(filter(str.isdigit, repr(int_list)))

## Builds 5 band color code
def create_resistor_bands( ohms ):
    ohmList = [str(i) for i in str(ohms)]

    firstBand = DIGIT[int(ohmList[0])]
    multiBand = 0

    if len(ohmList) == 1:
        secondBand = "black"
        thirdBand = "black"
        multiBand = 0.01

    elif ohmList[1] == ".":
        multiBand = 0.1
        secondBand = DIGIT[int(ohmList[2])]
        if( len(ohmList) <= 3 ):
            thirdBand = "black"
        else:
            thirdBand = DIGIT[int(ohmList[3])]
    else:
        if( len(ohmList) <= 1 ):
            secondBand = "black"
            thirdBand = "black"
            multiBand = 0.01
        elif( len(ohmList) == 2 ):
            secondBand = DIGIT[int(ohmList[1])]
            thirdBand = "black"
            multiBand = 0.1
        elif( len(ohmList) >= 3 ):
            secondBand = DIGIT[int(ohmList[1])]
            thirdBand = DIGIT[int(ohmList[2])]

    if( multiBand == 0 ):
        ohmList_sliced = [1] + ohmList[3:]
        multiBand = int_list_to_int(ohmList_sliced)
        
    for i in MULTIPLIER:
        if( multiBand == MULTIPLIER[i] ):
            multiBand = i

    tolBand = "brown"

    bands = [firstBand, secondBand, thirdBand, multiBand, tolBand]

    return bands

def get_offset(column, row, sublabel, width, height):

    ## TODO: ADD BETTER SUPPORT FOR COLUMNS
    if( column == 1 ):
        leftOffset = (LEFT_MARGIN + LABEL_W/2)*SCALE_MOD
    elif( column == 2 ):
        leftOffset = (LEFT_MARGIN + LABEL_W + MIDDLE_DIV + LABEL_W / 2)*SCALE_MOD
    else:
        leftOffset = 0

    ## TODO: ADD BETTER SUPPORT FOR SUBLABELS
    if( sublabel == 1 ):
        leftOffset = leftOffset - (LABEL_W*SCALE_MOD)/4 - width/2
    elif( sublabel == 2 ):
        leftOffset = leftOffset + (LABEL_W*SCALE_MOD)/4 - width/2

    upperOffset = UPPER_MARGIN*SCALE_MOD + LABEL_H*SCALE_MOD * (row - 1) + (LABEL_H*SCALE_MOD)/2

    return leftOffset, upperOffset
        
def shorten_name( name ):
    nameList = [str(i) for i in str(name)]

    if( len(nameList) >= 2 ):
        if( nameList[1] != "." ):
            num = int_list_to_int(nameList)
            if( num % 1000000 == 0 ):
                return str(num/1000000) + "M"
            elif( num % 1000 == 0 ):
                return str(num/1000) + "K"

    return name

def create_image( filetype ):
    imgFiles = []
    
    size = (int(SHEET_W*SCALE_MOD), int(SHEET_H*SCALE_MOD))
    img = Image.new('RGB', size, "white")
    draw = ImageDraw.Draw(img)

    fontPath = "ARIAL.ttf"
    ttf = ImageFont.truetype(fontPath, FONT)

    currColumn = 1
    currSublabel = 1
    currRow = 1

    ## Draws gridlines -- useful for debugging
##    draw.rectangle(((LEFT_MARGIN*SCALE_MOD, UPPER_MARGIN*SCALE_MOD),((SHEET_W-RIGHT_MARGIN)*SCALE_MOD,
##                                                                     (SHEET_H-LOWER_MARGIN)*SCALE_MOD)),
##                                                                      fill=None, outline="black")
##    draw.rectangle((((LEFT_MARGIN+LABEL_W)*SCALE_MOD, UPPER_MARGIN*SCALE_MOD),
##                    ((LEFT_MARGIN+LABEL_W+MIDDLE_DIV)*SCALE_MOD,(SHEET_H-LOWER_MARGIN)*SCALE_MOD)),
##                   fill=None, outline="black")
##    
##    for i in range(ROWS):
##        draw.rectangle(((LEFT_MARGIN*SCALE_MOD,UPPER_MARGIN*SCALE_MOD+LABEL_H*SCALE_MOD*i),
##                        ((SHEET_W-RIGHT_MARGIN)*SCALE_MOD,SCALE_MOD+LABEL_H*SCALE_MOD*(i+LABEL_H*SCALE_MOD))),fill=None, outline="black")
    ##
    
    for i in RESISTORS:
        ohms = str(shorten_name(i))
        if( len(ohms) <= 1 ):
            ohms += " Ohm"
        else:
            ohms += " Ohms"
        bands = create_resistor_bands(i)
        
        font_w, font_h = ttf.getsize(ohms)
        font_x, font_y = get_offset(currColumn, currRow, currSublabel, font_w, font_h)
        font_y -= 1.5*font_h

        draw.text((font_x, font_y), ohms, font=ttf, fill="black")

        shape_w, shape_h = (SHEET_W*SCALE_MOD)/10, font_h
        shape_x, shape_y = get_offset(currColumn, currRow, currSublabel, shape_w, shape_h)

        shapeMod = shape_w/5

        for n in bands:
            draw.rectangle(((shape_x, shape_y),(shape_x+shapeMod, shape_y+shapeMod)), fill=n, outline="white")
            shape_x = shape_x + shapeMod

        currSublabel += 1

        if( currSublabel > SUBLABELS ):
            currSublabel = 1
            currRow += 1

        if( currRow > ROWS ):
            currRow = 1
            currColumn += 1

        if( currColumn > COLUMNS ):
            currColumn = 1
            currRow = 1
            currSublabel = 1

            imgFiles.append(img)

            img = Image.new('RGB', size, "white")
            draw = ImageDraw.Draw(img)

    imgFiles.append(img)

    for i in range(0,len(imgFiles)):
        imgFiles[i].show()
        imgFiles[i].save("ResistorLabels"+str(i)+filetype)

    print "Success"

def main():
    create_image(".png")

main()
    
    
