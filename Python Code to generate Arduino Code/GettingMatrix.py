from PIL import Image, ImageSequence
from PIL import GifImagePlugin
import webcolors
import pandas as pd
import webcolors
import numpy as np
from matplotlib import pyplot as plt
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def getHexValues(column, row):
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    imageObject = Image.open(filename)
    i = 0
    for frame in ImageSequence.Iterator(imageObject):
        frame = frame.resize((column, row))
        frame = frame.convert(palette=Image.WEB)
        frame.save("Gif's Frames/" + str(i) + ".png", format="PNG", lossless=True)
        i += 1

    arduinoCode = open("Arduino Code.txt", "w")
    arduinoCode.write(
        "#include " + '"FastLED.h"' + "\n#include <avr/pgmspace.h>\n#define NUM_LEDS 1100\n#define DATA_PIN 5\nCRGB leds[NUM_LEDS];\nvoid setup() {\n\tdelay(200);\n\tFastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);\n\tFastLED.setBrightness(96);\n\tFastLED.clear();\n}\n")
    hexValues = []

    # if imageObject.n_frames is AttributeError: frame_nums = imageObject.n_frames
    try:
        for i in range(imageObject.n_frames):

            # arduinoCode.write("const long pic"+str(i)+"[] PROGMEM = ")
            eachhex = []
            img = "Gif's Frames/" + str(i) + ".png"
            img = Image.open(img)
            for y in range(img.height):
                for x in range(img.width):
                    if y % 2 == 0:
                        pix = img.getpixel((28 - x - 1, y))
                        eachhex.append(webcolors.rgb_to_hex(pix[0:3]))
                    else:
                        pix = img.getpixel((x, y))
                        eachhex.append(webcolors.rgb_to_hex(pix[0:3]))

            hexValues.append(eachhex)
            with open('HexValuesList.txt', 'w') as f:
                print(eachhex, file=f)
            with open('HexValuesList.txt', 'r') as file:
                hexVals = file.read()
            hex_to_long = hexVals.replace("]", "};")
            hex_to_long = hex_to_long.replace("[", "{")  # const long pic1[] PROGMEM =
            hex_to_long = hex_to_long.replace("'", "")
            hex_to_long = hex_to_long.replace("#", "0x")

            arduinoCode.write("const long pic" + str(i) + "[] PROGMEM = " + hex_to_long)
        arduinoCode.write("void loop() {\n\t")
        for j in range(imageObject.n_frames):
            arduinoCode.write(
                "\nFastLED.clear();\n\tfor(int i = 0; i < NUM_LEDS; i++) {\n\t\tleds[i] = pgm_read_dword(&(pic" + str(
                    j) + "[i]));\n\t\t}\n\tFastLED.show();\n\tdelay(100);\n\t")
        arduinoCode.write("}")
        arduinoCode.close()

    except AttributeError:
        for i in range(1):

            # arduinoCode.write("const long pic"+str(i)+"[] PROGMEM = ")
            eachhex = []
            img = "Gif's Frames/" + str(i) + ".png"
            img = Image.open(img)
            for x in range(img.width):
                for y in range(img.height):
                    pix = img.getpixel((x, y))

                    eachhex.append(webcolors.rgb_to_hex(pix[0:3]))
            hexValues.append(eachhex)

            with open('HexValuesList.txt', 'w') as f:
                print(eachhex, file=f)

            with open('HexValuesList.txt', 'r') as file:
                hexVals = file.read()
            hex_to_long = hexVals.replace("]", "};")
            hex_to_long = hex_to_long.replace("[", "{")  # const long pic1[] PROGMEM =
            hex_to_long = hex_to_long.replace("'", "")
            hex_to_long = hex_to_long.replace("#", "0x")

            arduinoCode.write("const long pic" + str(i) + "[] PROGMEM = " + hex_to_long)
        arduinoCode.write("void loop() {\n\t")
        for j in range(1):
            arduinoCode.write(
                "\nFastLED.clear();\n\tfor(int i = 0; i < NUM_LEDS; i++) {\n\t\tleds[i] = pgm_read_dword(&(pic" + str(
                    j) + "[i]));\n\t\t}\n\tFastLED.show();\n\tdelay(300);\n\t")
            arduinoCode.write("}")
            arduinoCode.close()

    return hexValues

print(getHexValues(28, 39))

("'", "")