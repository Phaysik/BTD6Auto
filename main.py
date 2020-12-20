#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2020-12-19
Date     : 2019-12-28
"""

from pyautogui import click, press, moveTo
import win32gui
from typing import List, Tuple, Dict, Optional, Union
from time import sleep
from PIL import ImageGrab, Image
from dataclasses import dataclass
from threading import Thread, currentThread
from os import system, name
from pytesseract import image_to_string, pytesseract
from fuzzywuzzy.fuzz import partial_ratio


@dataclass
class RGB:
    r: int
    g: int
    b: int


@dataclass
class TOWER:
    x: int
    y: int
    name: str
    currMonkey: bool
    key: str
    path: Optional[List[Dict[int, int]]] = None
    currUpgrades: Optional[List[int]] = None


class gameThread(Thread):
    def __init__(self, target, daemon: bool, args: Union[List[TOWER], List[str]]):
        Thread.__init__(self, target=target, args=[args], daemon=daemon)
        self.do_run = True


# CONSTS
BOX: Tuple[int, int, int, int] = (0, 0, 1920, 1080)
TOPBOX: Tuple[int, int] = (1488, 489)
MIDBOX: Tuple[int, int] = (1488, 636)
LOWBOX: Tuple[int, int] = (1488, 789)
REGION: Dict[str, Tuple[int, int]] = {"top": TOPBOX, "mid": MIDBOX, "low": LOWBOX}
MOVES: Dict[int, str] = {0: ",", 1: ".", 2: "/"}
MOVESREGION: Dict[int, str] = {0: "top", 1: "mid", 2: "low"}
TOWERRIGHTBOXES: Dict[str, Tuple[int, int, int, int]] = {
    "Hero": (1378, 59, 1513, 96),
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
LEVELDIMENSIONS: Tuple[int, int, int, int] = (815, 531, 1087, 611)
NEXTBUTTON: Tuple[int, int, int, int] = (888, 879, 1063, 948)
FREEPLAYBUTTON: Tuple[int, int, int, int] = (1010, 911, 1233, 966)
INSTATEXT: Tuple[int, int, int, int] = (733, 624, 1158, 709)

pytesseract.tesseract_cmd = "../Tesseract/tesseract.exe"


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


# Click in a certain location
def gameClick(location: TOWER, times: int) -> None:
    for i in range(times):
        sleep(0.2)
        moveTo(location.x, location.y)
        click(location.x, location.y)


# Press a certain key
def gamePress(key: str, times: int) -> None:
    for i in range(times):
        sleep(0.2)
        press(key)


# Click on an empty and safe area of the screen
def gameSafeClick() -> None:
    moveTo(100, 100)
    click(100, 100)


# Place and upgrade tower
def gamePlaceTower(index: int, tower: TOWER, allTowers: List[TOWER]) -> None:
    if index == 0:
        nextTower(tower)

        name: str = determinePlacement(tower.name)

        while partial_ratio(name.lower(), tower.name.lower()) < 70:
            gamePress(tower.key, 1)
            gameClick(tower, 2)

            sleep(0.2)
            name = determinePlacement(tower.name)

        placing(tower)
    else:
        gameClick(tower, 1)

    setCurrentMonkey(tower, allTowers)

    if (
        tower.path is not None
        and tower.currUpgrades is not None
        and len(tower.path) > 0
    ):
        for key, value in tower.path[index].items():
            for i in range(value):
                nextUpgrade(tower, key)

                while not determineMove(MOVESREGION[key]):
                    pass

                tower.currUpgrades[key] += 1
                upgrades(tower)
                gamePress(MOVES[key], 1)

    gameSafeClick()


# Set active window
def activeWindow() -> None:
    results: List[str] = []
    top_windows: List[str] = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "bloonstd6" in i[1].lower():
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


# Get a screenshot of current game state
def getImage() -> Image:
    sleep(0.1)
    return ImageGrab.grab(BOX)


# Determine if an upgrade is available to purchase
def determineMove(region: str) -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(REGION[region])
    return (IMAGE[0] >= 60) and (IMAGE[1] >= 200) and (IMAGE[2] <= 20)


# Determine if the user has leveled up
def determineLevelUp() -> bool:
    return partial_ratio(getTextFromImage(LEVELDIMENSIONS), "Level Up!") >= 90


# Get the towers name from an image
def getTextFromImage(box: Tuple[int, int, int, int]) -> str:
    return (
        image_to_string(ImageGrab.grab(box)).replace("\n", "").lower().strip().title()
    )


# Determine if the tower was placed
def determinePlacement(name: str) -> str:
    if name == "Adora":
        return getTextFromImage(TOWERRIGHTBOXES["Hero"])
    else:
        return getTextFromImage(TOWERRIGHTBOXES[name])


# Print out what tower is being bought next
def nextTower(tower: TOWER) -> None:
    print(f"Waiting on {tower.name} availability.")


# Print out what tower is being placed at which (x, y)
def placing(tower: TOWER) -> None:
    print(f"Placing {tower.name} at ({tower.x}, {tower.y}).")


# Print out the what upgrade is getting bought next
def nextUpgrade(tower: TOWER, currentPath: int) -> None:
    if tower.currUpgrades is not None:
        print(
            f'Waiting on {tower.name} {"-".join([str(tower.currUpgrades[i] + 1) if (currentPath == i) else (str(tower.currUpgrades[i])) for i in range(len(tower.currUpgrades))])}.'
        )


# Print out the current upgrade path of the given tower
def upgrades(tower: TOWER) -> None:
    if tower.currUpgrades is not None:
        print(
            f'Upgrading {tower.name} to {"-".join([str(i) for i in tower.currUpgrades])}.'
        )


# Set all towers currUpgrades attribute back to 0
def defaultUpgrades(towers: List[TOWER]) -> None:
    for monkey in towers:
        if monkey.currUpgrades is not None:
            monkey.currUpgrades = [0, 0, 0]


# Clear the console
def clear():
    system("cls" if name == "nt" else "clear")


# Deal with any potential level ups as they appear
def level(towers: List[TOWER]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        if determineLevelUp():
            print("Level up detected. Attempting to clear and continue program...")

            for tower in towers:
                if tower.currMonkey:
                    for i in range(2):
                        sleep(0.2)
                        moveTo(1470, 298)
                        click(1470, 298)

                    gameClick(tower, 1)
                    press("space")


# Activate abilities
def gameAbilities(abilities: List[str]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        sleep(0.1)
        for number in abilities:
            press(str(number))


# Create and start the leveling up thread
def levelThread(towers: List[TOWER]) -> gameThread:
    levelUp: gameThread = gameThread(level, True, towers)
    levelUp.start()
    return levelUp


# Create and start the Adora's abilities thread
def abilityThread(abilities: List[str]) -> gameThread:
    ability: gameThread = gameThread(gameAbilities, True, abilities)
    ability.start()
    return ability


# Kill the requested thread
def killThread(thread: gameThread) -> None:
    thread.do_run = False
    thread.join()


# Set the current monkey being upgraded
def setCurrentMonkey(tower: TOWER, towers: List[TOWER]) -> None:
    for monkey in towers:
        if tower == monkey:
            monkey.currMonkey = True
        else:
            monkey.currMonkey = False


# Deal with the freeplay button
def freeplay() -> None:
    print("Determining if MOAB has been defeated.")

    victory: str = getTextFromImage(NEXTBUTTON)

    while partial_ratio(victory, "Next") < 90:
        victory = getTextFromImage(NEXTBUTTON)

    print("MOAB defeated. Determining if VICTORY screen has appeared.")

    sleep(1)
    moveTo(1000, 920)
    click(1000, 920)

    victory = getTextFromImage(FREEPLAYBUTTON)

    while partial_ratio(victory, "Freeplay") < 80:
        victory = getTextFromImage(FREEPLAYBUTTON)

    print("VICTORY achieved. Going into freeplay...")

    sleep(1)
    moveTo(1036, 906)
    click(1036, 906)
    sleep(1)
    moveTo(1127, 856)
    click(1127, 856)
    sleep(1)
    moveTo(1023, 763)
    click(1023, 763)


# Restart the game
def restart(
    towers: List[TOWER],
    insta: str = "RESTART",
    map: Tuple[int, int] = (0, 0),
    difficulty: Tuple[int, int] = (0, 0),
    gamemode: Tuple[int, int] = (0, 0),
) -> None:
    if insta == "BAD":
        print("Determining if Insta Monkey screen has appeared.")

        instaMonkey: str = getTextFromImage(INSTATEXT)

        while partial_ratio(instaMonkey, "Insta-Monkey!") < 90:
            instaMonkey = getTextFromImage(INSTATEXT)

        print("Insta Monkey acquired. Going into freeplay...")

        sleep(1)
        moveTo(881, 437)
        click(881, 437)

    print("Restarting...")

    defaultUpgrades(towers)

    if insta == "BAD":
        # For some fucking reason you can't get an instant monkey if you restart the map anymore so I have to do this bullshit
        # of leaving the map and then rejoining it
        sleep(1)
        # Settings/Gear Box
        moveTo(1600, 44)
        click(1600, 44)
        sleep(1)
        # Home Box
        moveTo(844, 849)
        click(844, 849)
        sleep(2)
        # Play Button
        moveTo(857, 945)
        click(857, 945)
        sleep(2)
        # Map
        moveTo(map[0], map[1])
        click(map[0], map[1])
        sleep(2)
        # Difficulty
        moveTo(difficulty[0], difficulty[1])
        click(difficulty[0], difficulty[1])
        sleep(2)
        # Gamemode
        moveTo(gamemode[0], gamemode[1])
        click(gamemode[0], gamemode[1])
        sleep(2)
        # Overwrite if needed
        moveTo(1123, 721)
        click(1123, 721)
    else:
        sleep(1)
        # Settings/Gear Box
        moveTo(1600, 44)
        click(1600, 44)
        sleep(1)
        # Restart Box
        moveTo(1102, 833)
        click(1102, 833)
        sleep(1)
        # Confirm Restart
        moveTo(1180, 724)
        click(1180, 724)
