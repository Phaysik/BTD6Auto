#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 12/21/2020
Date     : 12/28/2019
"""

from pyautogui import click, moveTo
from win32gui import EnumWindows, ShowWindow, SetForegroundWindow, GetWindowText
from typing import Optional, Union
from time import sleep
from PIL import ImageGrab, Image
from threading import Thread, currentThread
from os import system, name
from pytesseract import image_to_string
from fuzzywuzzy.fuzz import partial_ratio, ratio
from math import sqrt
from mouse import get_position
from keyboard import send, add_hotkey
from os import _exit
from globals import *

add_hotkey(SIGINT, lambda: _exit(1))


@dataclass
class TOWER:
    x: int
    y: int
    name: str
    currMonkey: bool
    key: str
    path: Optional[list[dict[int, int]]] = None
    currUpgrades: Optional[list[int]] = None


class gameThread(Thread):
    def __init__(self, target, daemon: bool, args: Union[list[TOWER], list[str]]):
        Thread.__init__(self, target=target, args=[args], daemon=daemon)
        self.do_run = True


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, GetWindowText(hwnd)))


# Click in a certain location
def gameClick(location: TOWER, times: int) -> None:
    for i in range(times):
        sleep(0.2)
        moveTo(location.x, location.y)
        click(location.x, location.y)


# Press a certain key
def gamePress(key: str, times: int) -> None:
    for _ in range(times):
        sleep(0.2)
        send(key)


# Click on an empty and safe area of the screen
def gameSafeClick() -> None:
    moveTo(100, 100)
    click(100, 100)


# Return the distance from the mouse positon and the requested tower position
def distance(x1: int, x2: int, y1: int, y2: int) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Place, upgrade, sell towers
def towerManip(index: int, tower: TOWER, allTowers: list[TOWER]) -> None:
    if index == -1:
        nextTower(tower)

        name: str = determinePlacement(tower)
        pos: tuple[int, int] = get_position()
        dist: float = distance(tower.x, pos[0], tower.y, pos[1])

        while (
            ratio(name.lower(), tower.name.lower()) < 80
            and tower.name.lower() not in name.lower()
        ) or dist > 50:
            gamePress(tower.key, 1)
            gameClick(tower, 2)

            name = determinePlacement(tower)

            if DEBUG:
                print(
                    f"DEBUG: {name=} {name.lower()} {tower.name.lower()} {tower.name.lower() not in name.lower()}"
                )

            pos = get_position()
            dist = distance(tower.x, pos[0], tower.y, pos[1])

            if DEBUG:
                print(f"DEBUG: {dist=}")

        placing(tower)
    else:
        if tower.currMonkey == False:
            gameClick(tower, 1)

    setCurrentMonkey(tower, allTowers)

    if (
        tower.path is not None
        and tower.currUpgrades is not None
        and len(tower.path) > 0
        and index >= 0
    ):
        for key, value in tower.path[index].items():
            for i in range(value):
                nextUpgrade(tower, key)

                while not determineMove(MOVESREGION[key]):
                    pass

                tower.currUpgrades[key] += 1
                upgrades(tower)
                gamePress(MOVES[key], 1)

    if index > -2:
        gameSafeClick()
        setCurrentMonkey(tower, allTowers, True)


# Set active window
def activeWindow() -> None:
    top_windows: list[str] = []
    EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "bloonstd6" in i[1].lower():
            ShowWindow(i[0], 5)
            SetForegroundWindow(i[0])
            break


# Get a screenshot of current game state
def getImage() -> Image.Image:
    sleep(0.1)
    return ImageGrab.grab(BOX)


# Determine if an upgrade is available to purchase
def determineMove(region: str) -> bool:
    IMAGE: tuple[int, int, int] = getImage().getpixel(REGION[region])
    return (IMAGE[0] >= MOVE.r) and (IMAGE[1] >= MOVE.g) and (IMAGE[2] <= MOVE.b)


# Determine if the user has leveled up
def determineLevelUp() -> bool:
    return ratio(getTextFromImage(LEVELDIMENSIONS), "Level Up!") >= 90


# Get the towers name from an image
def getTextFromImage(
    box: tuple[int, int, int, int],
    towerXCoords: int = 0,
    towerYCoords: int = 0,
    heroTower: bool = False,
) -> str:
    sleep(0.5)

    if heroTower:
        moveTo(INFOICONLOCATION[0], INFOICONLOCATION[1])
        click(INFOICONLOCATION[0], INFOICONLOCATION[1])
        sleep(0.5)

    grabbedImage: Image.Image = ImageGrab.grab(box)
    grabbedImage.save("test.png")

    if heroTower:
        moveTo(BACKBUTTON[0], BACKBUTTON[1])
        click(BACKBUTTON[0], BACKBUTTON[1])
        sleep(0.5)
        moveTo(towerXCoords, towerYCoords)

    return image_to_string(grabbedImage).replace("\n", "").lower().strip().title()


# Determine if the tower was placed
def determinePlacement(tower: TOWER) -> str:
    match tower.name:
        case "Adora":
            return getTextFromImage(ADORA, tower.x, tower.y, True)
        case _:
            return getTextFromImage(TOWERRIGHTBOXES[tower.name])


# Print out what tower is being bought next
def nextTower(tower: TOWER) -> None:
    print(f"\tWaiting on {tower.name} availability.")


# Print out what tower is being placed at which (x, y)
def placing(tower: TOWER) -> None:
    print(f"\t\tPlacing {tower.name} at ({tower.x}, {tower.y}).")


# Print out the what upgrade is getting bought next
def nextUpgrade(tower: TOWER, currentPath: int) -> None:
    if tower.currUpgrades is not None:
        print(
            f'\tWaiting on {tower.name} {"-".join([str(tower.currUpgrades[i] + 1) if (currentPath == i) else (str(tower.currUpgrades[i])) for i in range(len(tower.currUpgrades))])}.'
        )


# Print out the current upgrade path of the given tower
def upgrades(tower: TOWER) -> None:
    if tower.currUpgrades is not None:
        print(
            f'\t\tUpgrading {tower.name} to {"-".join([str(i) for i in tower.currUpgrades])}.'
        )


# Print out what tower is being sold
def selling(tower: str) -> None:
    pos: tuple[int, int] = get_position()
    print(f"Selling {tower} at ({pos[0]}, {pos[1]})")


# Print out what tower is being sold
def targeting(tower: str) -> None:
    pos: tuple[int, int] = get_position()
    print(f"Changing the targeting of {tower} at ({pos[0]}, {pos[1]})")


# Set all towers currUpgrades attribute back to 0
def defaultUpgrades(towers: list[TOWER]) -> None:
    for monkey in towers:
        if monkey.currUpgrades is not None:
            monkey.currUpgrades = [0, 0, 0]


# Clear the console
def clear():
    system("cls" if name == "nt" else "clear")


# Deal with any potential level ups as they appear
def level(towers: list[TOWER]) -> None:
    t = currentThread()

    while getattr(t, "do_run", True):
        if determineLevelUp():
            print("Level up detected. Attempting to clear and continue program...")

            for tower in towers:
                for i in range(2):
                    sleep(0.2)
                    moveTo(1470, 298)
                    click(1470, 298)

                if tower.currMonkey:
                    gameClick(tower, 1)

                send("space")


# Activate abilities
def gameAbilities(abilities: list[str]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        sleep(0.1)
        for number in abilities:
            send(str(number))


# Create and start the leveling up thread
def levelThread(towers: list[TOWER]) -> gameThread:
    levelUp: gameThread = gameThread(level, True, towers)
    levelUp.start()
    return levelUp


# Create and start the Adora's abilities thread
def abilityThread(abilities: list[str]) -> gameThread:
    ability: gameThread = gameThread(gameAbilities, True, abilities)
    ability.start()
    return ability


# Kill the requested thread
def killThread(thread: gameThread) -> None:
    thread.do_run = False
    thread.join()


# Set the current monkey being upgraded
def setCurrentMonkey(tower: TOWER, towers: list[TOWER], deselect: bool = False) -> None:
    for monkey in towers:
        if tower == monkey and not deselect:
            monkey.currMonkey = True
        else:
            monkey.currMonkey = False


# Deal with the freeplay button
def freeplay() -> None:
    print("Determining if MOAB has been defeated.")

    victory: str = getTextFromImage(NEXTBUTTON)

    while partial_ratio(victory, "Next") < 90:
        victory = getTextFromImage(NEXTBUTTON)

    print("\tMOAB defeated. Determining if VICTORY screen has appeared.")

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
    towers: list[TOWER],
    insta: str = "RESTART",
    map: tuple[int, int] = (0, 0),
    difficulty: tuple[int, int] = (0, 0),
    gamemode: tuple[int, int] = (0, 0),
) -> None:
    if insta == "BAD":
        print("Determining if Insta Monkey screen has appeared.")

        instaMonkey: str = getTextFromImage(INSTATEXT)

        while partial_ratio(instaMonkey, "Insta-Monkey!") < 90:
            instaMonkey = getTextFromImage(INSTATEXT)

        print("\tInsta Monkey acquired. Going into freeplay...")

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
