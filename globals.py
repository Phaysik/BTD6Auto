#!/usr/bin/env python3
"""
Author   : Matthew Moore
Date     : 12/21/2020
Revision : 12/21/2020
"""

from pytesseract import pytesseract
from dataclasses import dataclass


@dataclass
class RGB:
    r: int
    g: int
    b: int


# CONSTS

# The RGB to determine whether the move is availble to purchase
MOVE: RGB = RGB(r=60, g=200, b=20)

# Screen dimensions
BOX: tuple[int, int, int, int] = (0, 0, 1920, 1080)

# Top Upgrade (x, y)
TOPBOX: tuple[int, int] = (1488, 489)

# Middle Upgrade (x, y)
MIDBOX: tuple[int, int] = (1488, 636)

# Bottom Upgrade (x, y)
LOWBOX: tuple[int, int] = (1488, 789)

REGION: dict[str, tuple[int, int]] = {"top": TOPBOX, "mid": MIDBOX, "low": LOWBOX}

MOVES: dict[int, str] = {0: ",", 1: ".", 2: "/"}

MOVESREGION: dict[int, str] = {0: "top", 1: "mid", 2: "low"}

# HERO BOUNDARIES
ADORA: tuple[int, int, int, int] = (160, 18, 540, 115)

# Towers and their text information when placed on the left side of the screen
TOWERRIGHTBOXES: dict[str, tuple[int, int, int, int]] = {
    "Dart Monkey": (1307, 52, 1580, 100),
    "Boomerang Monkey": (1278, 54, 1610, 96),
    "Bomb Shooter": (1304, 51, 1587, 101),
    "Tack Shooter": (1308, 57, 1587, 101),
    "Ice Monkey": (1333, 54, 1558, 99),
    "Glue Gunner": (1312, 52, 1570, 96),
    "Sniper Monkey": (1298, 54, 1589, 98),
    "Monkey Sub": (1322, 55, 1560, 98),
    "Monkey Bucanneer": (1275, 53, 1603, 94),
    "Monkey Ace": (1325, 55, 1559, 97),
    "Heli Pilot": (1343, 54, 1545, 99),
    "Mortar Monkey": (1288, 55, 1599, 100),
    "Dartling Gunner": (1273, 55, 1608, 98),
    "Wizard Monkey": (1274, 51, 1606, 99),
    "Super Monkey": (1302, 55, 1583, 101),
    "Ninja Monkey": (1302, 55, 1583, 101),
    "Alchemist": (1330, 56, 1557, 98),
    "Druid": (1372, 56, 1512, 94),
    "Banana Farm": (1302, 55, 1583, 101),
    "Spike Factory": (1302, 55, 1583, 101),
    "Monkey Village": (1302, 55, 1583, 101),
    "Engineer Monkey": (1271, 52, 1609, 100),
}

# A Box surrounding where the Level Up! text shows up
LEVELDIMENSIONS: tuple[int, int, int, int] = (815, 531, 1087, 611)

# A Box surrounding where the Next button text shows up
NEXTBUTTON: tuple[int, int, int, int] = (888, 879, 1063, 948)

# A Box surrounding where the Freeplay button text shows up
FREEPLAYBUTTON: tuple[int, int, int, int] = (1107, 906, 1331, 966)

# A Box surrounding where the Insta-Monkey! text shows up
INSTATEXT: tuple[int, int, int, int] = (733, 624, 1158, 709)

# Location of the info icon for hero selection
# Click on this to guarantee name even on different hero skins
INFOICONLOCATION: tuple[int, int] = (1307, 174)

# The button to return from the info icon screen
BACKBUTTON: tuple[int, int] = (97, 62)

# Path to the tesseract executable
# Assumes you run a map file from a subdirectory
pytesseract.tesseract_cmd = "../Tesseract/tesseract.exe"

# The key/combination to signal the exit of the program
SIGINT: str = "ctrl+c"

DEBUG: bool = False
