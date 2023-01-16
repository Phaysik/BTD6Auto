#!/usr/bin/env python3
"""
Author   : Matthew Moore
Date     : 12/21/2020
Revision : 01/15/2023
"""

from pytesseract import pytesseract
from dataclasses import dataclass


@dataclass
class RGB:
    r: int
    g: int
    b: int


Position = tuple[int, int]
BoundingBox = tuple[int, int, int, int]


# CONSTS

# The RGB to determine whether the move is availble to purchase
MOVE: RGB = RGB(r=60, g=200, b=20)

# Screen dimensions
BOX: BoundingBox = (0, 0, 1920, 1080)

# The position of the top upgrade when the tower information is on the right
TOPRIGHTBOX: Position = (1488, 489)

# The position of the top upgrade when the tower information is on the left
TOPLEFTBOX: Position = (271, 489)

# The position of the middle upgrade when the tower information is on the right
MIDRIGHTBOX: Position = (1488, 636)

# The position of the middle upgrade when the tower information is on the left
MIDLEFTBOX: Position = (271, 636)

# The position of the bottom upgrade when the tower information is on the right
LOWRIGHTBOX: Position = (1488, 789)

# The position of the bottom upgrade when the tower information is on the left
LOWLEFTBOX: Position = (271, 789)

REGION: dict[str, dict[str, Position]] = {
    "left": {"top": TOPRIGHTBOX, "mid": MIDRIGHTBOX, "low": LOWRIGHTBOX},
    "right": {"top": TOPLEFTBOX, "mid": MIDLEFTBOX, "low": LOWLEFTBOX},
}

MOVES: dict[int, str] = {0: ",", 1: ".", 2: "/"}

MOVESREGION: dict[int, str] = {0: "top", 1: "mid", 2: "low"}

# The position of the level text in the in game hero info screen
LEVELTEXTPOSITION: BoundingBox = (550, 707, 648, 750)

# The x coordinate where tower information will appear on the left side of the screen
MIDPOINT: int = 835

# Towers and their text information when placed on the left side of the screen
TOWERBOXES: dict[str, dict[str, BoundingBox]] = {
    "Dart Monkey": {"left": (1307, 52, 1580, 100), "right": (94, 52, 356, 100)},
    "Boomerang Monkey": {"left": (1278, 54, 1610, 96), "right": (59, 54, 390, 96)},
    "Bomb Shooter": {"left": (1304, 51, 1587, 101), "right": (86, 51, 365, 101)},
    "Tack Shooter": {"left": (1308, 57, 1587, 101), "right": (90, 57, 365, 101)},
    "Ice Monkey": {"left": (1333, 54, 1558, 99), "right": (115, 54, 339, 99)},
    "Glue Gunner": {"left": (1322, 55, 1570, 100), "right": (96, 55, 346, 100)},
    "Sniper Monkey": {"left": (1298, 54, 1589, 98), "right": (80, 54, 367, 98)},
    "Monkey Sub": {"left": (1322, 55, 1560, 98), "right": (107, 55, 340, 98)},
    "Monkey Bucanneer": {"left": (1275, 53, 1603, 94), "right": (61, 53, 386, 94)},
    "Monkey Ace": {"left": (1340, 55, 1550, 100), "right": (107, 55, 344, 100)},
    "Heli Pilot": {"left": (1343, 54, 1545, 99), "right": (126, 54, 323, 99)},
    "Mortar Monkey": {"left": (1288, 55, 1599, 100), "right": (72, 55, 376, 100)},
    "Dartling Gunner": {"left": (1273, 55, 1608, 98), "right": (64, 55, 384, 98)},
    "Wizard Monkey": {"left": (1274, 51, 1606, 99), "right": (75, 51, 372, 99)},
    "Super Monkey": {"left": (1302, 55, 1583, 101), "right": (79, 55, 360, 101)},
    "Ninja Monkey": {"left": (1302, 55, 1583, 101), "right": (82, 55, 357, 101)},
    "Alchemist": {"left": (1330, 56, 1557, 98), "right": (114, 56, 333, 98)},
    "Druid": {"left": (1385, 52, 1510, 100), "right": (152, 52, 289, 100)},
    "Banana Farm": {"left": (1302, 55, 1583, 101), "right": (90, 55, 354, 101)},
    "Spike Factory": {"left": (1302, 55, 1583, 101), "right": (82, 55, 358, 101)},
    "Monkey Village": {"left": (1302, 55, 1583, 101), "right": (70, 55, 374, 101)},
    "Engineer Monkey": {"left": (1271, 52, 1609, 100), "right": (54, 52, 388, 100)},
}

# A Box surrounding where the Level Up! text shows up
LEVELDIMENSIONS: BoundingBox = (815, 531, 1087, 611)

# A Box surrounding where the Next button text shows up
NEXTBUTTON: BoundingBox = (888, 879, 1063, 948)

# A Box surrounding where the Freeplay button text shows up
FREEPLAYBUTTON: BoundingBox = (1107, 906, 1331, 966)

# The position of the next button on the player card victory screen
NEXTVICTORYBUTTONPOSITION: Position = (1000, 920)

# Where the freeplay button is located
FREEPLAYBUTTONPOSITION: Position = (1233, 834)

# The position of the OK button after freeplay is clicked
FREEPLAYOKBUTTONPOSITION: Position = (953, 766)

# A Box surrounding where the Insta-Monkey! text shows up
INSTATEXT: BoundingBox = (753, 624, 1158, 709)

# The place to click after the Insta-Monkey shows up
INSTAMONKEYPOSITION: Position = (981, 522)

# The position of the gearbox icon in the top-left
GEARBOXPOSITION: Position = (1598, 35)

# The position of the restart button in the pause menu
RESTARTBUTTONPOSITION: Position = (1075, 847)

# The position of the confirm restart button
CONFIRMRESTARTBUTTONPOSITION: Position = (1112, 715)

# The position of the home button in the pause menu
HOMEBUTTONPOSITION: Position = (846, 850)

# The position of the play button on the home screen
PLAYBUTTONPOSITION: Position = (836, 934)

# The position of the overwrite save button
OVERWRITEBUTTONPOSITION: Position = (1097, 715)

# The position of the left arrow to move to different map screens
LEFTMAPARROWBUTTONPOSITION: Position = (1636, 430)

# Location of the info icon for hero selection when the infor window is on the right
# Click on this to guarantee name even on different hero skins
RIGHTINFOICONLOCATION: Position = (1307, 174)

# Location of the info icon for hero selection when the info window is on the lefr
# Click on this to guarantee name even on different hero skins
LEFTINFOICONLOCATION: Position = (88, 174)

# The button to return from the info icon screen
BACKBUTTON: Position = (78, 83)

# LEVEL SELECTION OPTIONS

# The position of each of the six levels on each level select screen
# 0 -> Top row 1, top row 2, top row 3
# 1 -> Bottom row 1, bottom row 2, bottom row 3
# i.e:
#   0 -> Monkey Meadow, Tree Stump, Town Center
#   1 -> One Two Tree, Scrapyard, The Cabin
MAPROWCOLPOSITIONS: dict[int, list[Position]] = {
    0: [(571, 277), (1001, 249), (1423, 227)],
    1: [(531, 588), (934, 568), (1382, 548)],
}

# The position of each of the three difficulties after selecting a level
DIFFICULTYPOSITIONS: dict[str, Position] = {
    "Easy": (629, 425),
    "Medium": (968, 408),
    "Hard": (1284, 401),
}

# The positions of each of the game modes for the difficulty levels
# 0 -> Standard, top row 1, top row 2, top row 3
# 1 -> Bottom row 1, bottom row 2, bottom row 3
# i.e on Easy:
#   0 -> Standard, Primary Only, Deflation
#   1 -> Sandbox
GAMEMODEPOSITIONS: dict[int, list[Position]] = {
    0: [(651, 609), (961, 443), (1299, 446), (1610, 443)],
    1: [(1022, 719), (1287, 751), (1599, 732)],
}

# Path to the tesseract executable
# Assumes you run a map file from a subdirectory
pytesseract.tesseract_cmd = "../Tesseract/tesseract.exe"

# The key/combination to signal the exit of the program
SIGINT: str = "ctrl+c"

# For debug log messages
DEBUG: bool = False
