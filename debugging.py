from PIL import ImageGrab, Image
from globals import *
from pytesseract import image_to_string, pytesseract
from keyboard import add_hotkey
from os import _exit
from fuzzywuzzy.fuzz import partial_ratio, ratio
from pyautogui import moveTo, click
from mouse import get_position
from time import sleep
import sys


def position() -> None:
    while True:
        print(get_position())


def ocr() -> None:
    pytesseract.tesseract_cmd = "./Tesseract/tesseract"
    checkFor: str = "Level"
    image: Image.Image = ImageGrab.grab(LEVELTEXTPOSITION)
    image.save("test.png")

    name = image_to_string(image).replace("\n", "").lower().strip().title()

    print(f"{name=}")

    print(
        "Ratio:",
        ratio(name.lower(), checkFor.lower()),
        checkFor.lower() in name.lower(),
    )

    print(
        "Partial Ratio:",
        partial_ratio(name.lower(), checkFor.lower()),
        checkFor.lower() in name.lower(),
    )


def mouseClick() -> None:
    moveTo(0, 0)
    click(0, 0)


def mouseClicks() -> None:
    positions: list[tuple[int, int]] = [(1046, 391), (1229, 380), (473, 138)]

    while True:
        for position in positions:
            moveTo(position[0], position[1])
            click(position[0], position[1])
            sleep(0.2)


def main() -> None:
    arguments = sys.argv[1:]

    validCommands: list[str] = ["position", "image", "click", "clicks"]

    # Determine valid argument
    if (len(arguments) != 1) or arguments[0].lower() not in validCommands:
        print("Invalid argument. Must be either 'image'")
        print("Example: python debugging.py x")
        print("position -> Print position of the mouse")
        print(
            "image -> Crop an image, save it as a .png, and run the Tesseract OCR against it"
        )
        print("click -> Move the mouse to and click on an a spot")
        print(
            "clicks -> Move to an area, click it, and then more to another area and click it, etc."
        )
        sys.exit(0)

    add_hotkey("ctrl+c", lambda: _exit(1))

    match arguments[0].lower():
        case "position":
            position()
        case "image":
            ocr()
        case "click":
            mouseClick()
        case "clicks":
            mouseClicks()


if __name__ == "__main__":
    main()
