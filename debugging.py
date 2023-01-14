from PIL import ImageGrab
from globals import *
from pytesseract import image_to_string, pytesseract
from fuzzywuzzy.fuzz import partial_ratio, ratio

pytesseract.tesseract_cmd = "./Tesseract/tesseract"

m = ImageGrab.grab(FREEPLAYBUTTON)
m.save("test.png")

name = image_to_string(m).replace("\n", "").lower().strip().title()

print(f"{name=}")

print(ratio(name.lower(), "Freeplay"), "freeplay" in name.lower())
