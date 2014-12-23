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

## Number of labels to split each label into
SUBLABELS = 2

## Resistor values to generate labels for
RESISTORS = [1, 2.2, 4.7, 5.6, 7.5, 8.2, 10, 15, 22, 27,
             33, 39, 47, 56, 68, 75, 82, 100, 120, 150,
             180, 220, 270, 330, 390, 470, 510, 680, 820,
             1000, 1500, 2200, 3300, 3900, 4700, 5600,
             6800, 7500, 8200, 10000, 15000, 22000, 33000,
             39000, 47000, 56000, 68000, 75000, 82000,
             10000, 150000, 180000, 220000, 330000, 470000,
             560000, 680000, 1000000, 1500000, 2000000,
             3300000, 4700000, 5600000, 10000000]

## Resistor band colors (index in list cooresponds to digit)
DIGIT = ["black", "brown", "red", "orange", "yellow", "green",
         "blue", "violet", "gray", "white"]

## Resistor band color map to multiplier
MULTIPLIER = {"black":1, "brown":10, "red":100, "orange":1000,
              "yellow":10000, "green":100000, "blue":1000000,
              "violet":10000000, "gray":100000000,
              "white":1000000000, "gold":0.1, "silver":0.01}

## Resistor tolerance (mine are all +- 1%)
TOLERANCE = 1

## Builds 5 band color code
def gen_resistor_bands( ohms ):
    ohmList = [str(i) for i in str(ohms)]

    firstBand = DIGIT[int(ohmList[0])]
    multiBand = 0

    if ohmList[1] == ".":
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
        ohmList_sliced = [1] + ohmList[2:]
        ohmList_temp = filter(str.isdigit, repr(ohmList_sliced))
        multiBand = int(ohmList_temp)
        
    for i in MULTIPLIER:
        if( multiBand == MULTIPLIER[i] ):
            multiBand = i

    tolBand = "brown"

    return firstBand, secondBand, thirdBand, multiBand, tolBand
            
a,b,c,d,e = gen_resistor_bands(RESISTORS[13])

print a
print b
print c
print d
print e
    
    
