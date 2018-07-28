from Adafruit_Thermal import *
from PIL import Image

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)

printer.justify('C')
printer.println("Here's a maze!")
printer.feed(1)
printer.printImage(Image.open('maze.png'), True)
printer.feed(2)
