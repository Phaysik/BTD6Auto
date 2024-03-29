#!/usr/bin/env python3
"""
Author   : Matthew Moore
Date     : 12/19/2020
Revision : 01/15/2023
"""

from datetime import date
from typing import IO, TypedDict
from dataclasses import dataclass
from keyboard import wait, on_press, KeyboardEvent
from mouse import on_click, get_position
from math import sqrt
from json import load
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from globals import *


@dataclass
class TOWER:
    x: int
    y: int
    name: str
    currMonkey: bool
    key: str
    sold: bool
    path: list[dict[int, int]] | None = None
    currUpgrades: list[int] | None = None


class JSON(TypedDict):
    authorName: str
    mapName: str
    mapScreen: int
    mapRowCol: list[int]
    difficulty: str
    gameType: str
    gameTypeRowCol: list[int]
    instaMonkey: bool


# Consts
TOWERSKEY: dict[str, str] = {
    "u": "Hero",
    "q": "Dart Monkey",
    "w": "Boomerang Monkey",
    "e": "Bomb Shooter",
    "r": "Tack Shooter",
    "t": "Ice Monkey",
    "y": "Glue Gunner",
    "z": "Sniper Monkey",
    "x": "Monkey Sub",
    "c": "Monkey Bucanneer",
    "v": "Monkey Ace",
    "b": "Heli Pilot",
    "n": "Mortar Monkey",
    "m": "Dartling Gunner",
    "a": "Wizard Monkey",
    "s": "Super Monkey",
    "d": "Ninja Monkey",
    "f": "Alchemist",
    "g": "Druid",
    "h": "Banana Farm",
    "j": "Spike Factory",
    "k": "Monkey Village",
    "l": "Engineer Monkey",
}
MOVESLIST: dict[str, int] = {",": 0, ".": 1, "/": 2}

# Mutable
towerList: list[TOWER] = []
currTower: TOWER | None = None
towerName: str | None = None
gKey: str | None = None
collectPath: dict[int, int] | None = None
currentKeys: dict[int, int] | None = None
towerCount: int = 0
towerPlaceIndex: int = 0
firstMonkey: str = ""
stringTowerList: list[str] = []
monkeyUpgradeOrder: list[dict[str, int]] = []
abilities: list[str] = []
authorName: str = ""
mapName: str = ""
mapScreen: int = 0
mapRowCol: list[int] = []
difficulty: str = ""
gameType: str = ""
gameTypeRowCol: list[int] = []
instaMonkey: bool = False

# Write the boilerplate header and includes for the program
def header(f: IO) -> None:
    global authorName

    f.write("#!/usr/bin/env python3\n")
    f.write('"""\n')
    f.write(f"Author   : {authorName}\n")
    f.write(f'Date     : {date.today().strftime("%m/%d/%Y")}\n')
    f.write(f'Revision : {date.today().strftime("%m/%d/%Y")}\n')
    f.write('"""\n\n')
    f.write("import os, sys\n")
    f.write(
        "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n\n"
    )
    f.write("from main import *\n\n")


def runner(f: IO) -> None:
    global mapScreen
    global mapRowCol
    global instaMonkey
    global difficulty
    global mapName
    global gameType
    global gameTypeRowCol

    f.write("\ndef main() -> None:\n")
    f.write("\titeration: int = 1\n\n")
    f.write("\twhile True:\n")
    f.write("\t\tlevelUp: gameThread = levelThread(ALLTOWERS)\n")
    f.write("\t\tability = abilityThread(ABILITIES)\n\n")
    f.write("\t\tclear()\n\n")
    f.write(f'\t\tprint("Starting {mapName} - {difficulty} - {gameType}")\n')
    f.write('\t\tprint(f"Current iteration: {iteration}")\n\n')
    f.write("\t\tactiveWindow()\n\n")
    f.write("\t\tsleep(1)\n")
    f.write('\t\tgamePress("space", 2)\n\n')

    for monkey in monkeyUpgradeOrder:
        for k, v in monkey.items():
            f.write(f"\t\ttowerManip({v}, {k}, ALLTOWERS)\n")
            if v == -2:
                f.write("\t\tsleep(0.5)\n")
                f.write(
                    f"\t\tgamePress('backspace', 1, \"{k.replace('_', ' ').title()[:-1]}\")\n"
                )
            elif v == -3:
                f.write("\t\tsleep(0.5)\n")
                f.write(
                    f"\t\tgamePress('tab', 1, \"{k.replace('_', ' ').title()[:-1]}\")\n"
                )
            f.write("\t\tsleep(0.5)\n\n")

    f.write("\n\t\tfreeplay()\n\n")
    f.write(
        f"\t\trestart(ALLTOWERS, {mapScreen}, {MAPROWCOLPOSITIONS[mapRowCol[0] - 1][mapRowCol[1] - 1]}, {DIFFICULTYPOSITIONS[difficulty]}, {GAMEMODEPOSITIONS[gameTypeRowCol[0] - 1][gameTypeRowCol[1] - 1]}, \"{'BAD' if instaMonkey else 'RESTART'}\")\n\n"
    )
    f.write("\t\tkillThread(levelUp)\n")
    f.write("\t\tkillThread(ability)\n\n")
    f.write("\t\tsleep(3)\n")
    f.write("\t\titeration += 1\n\n")
    f.write('if __name__ == "__main__":\n')
    f.write("\tmain()")


def writeTower(
    x: int, y: int, name: str, key: str, path: list[dict[int, int]] | None, f: IO
) -> None:
    global towerCount
    global firstMonkey
    global stringTowerList

    current: bool = False
    towerString: str = ""

    if towerCount == 0:
        firstMonkey = name

        if firstMonkey != "Hero":
            current = True

    elif towerCount == 1 and firstMonkey == "Hero":
        current = True

    towerString += f'{name.replace(" ", "_").upper()}{towerCount}: TOWER = TOWER(x = {x}, y = {y}, name = \'{name}\', currMonkey = {current}, key = \'{key}\''

    if name == "Hero":
        towerString += ")\n"
    elif isinstance(path, list):
        towerString += f", path = {path}, currUpgrades = [0, 0, 0])\n"

    f.write(towerString)

    stringTowerList.append(towerString.split(":")[0])

    towerCount += 1


# Handle Keyboard Inputs
def input(x: KeyboardEvent) -> None:
    global towerName
    global towerList
    global gKey
    global collectPath
    global currentKeys
    global abilities
    global currTower
    global monkeyUpgradeOrder
    towerName = None
    hero: bool = False
    top: bool = True
    mid: bool = True
    bottom: bool = True
    topVal: int = 0
    midVal: int = 0
    bottomVal: int = 0

    for key, value in TOWERSKEY.items():
        if x.name == key:
            gKey = key

            if x.name == "u":
                towerName = "Hero"
            else:
                towerName = value

            hero = True
            break

    if not hero:
        if currTower != None and x.name in MOVESLIST.keys():
            for tower in towerList:
                if currTower == tower:
                    if collectPath == None:
                        collectPath = {}
                        currentKeys = {0: 0, 1: 0, 2: 0}

                    if isinstance(currentKeys, dict):
                        for k, v in currentKeys.items():
                            if k == 0:
                                topVal = v
                            elif k == 1:
                                midVal = v
                            else:
                                bottomVal = v

                            if topVal > 0 and midVal > 0:
                                if topVal > 2 and midVal == 2:
                                    mid = False
                                elif midVal > 2 and topVal == 2:
                                    top = False

                                bottom = False
                            elif topVal > 0 and bottomVal > 0:
                                if topVal > 2 and bottomVal == 2:
                                    bottom = False
                                elif bottomVal > 2 and topVal == 2:
                                    top = False

                                mid = False
                            elif midVal > 0 and bottomVal > 0:
                                if midVal > 2 and bottomVal == 2:
                                    bottom = False
                                elif bottomVal > 2 and midVal == 2:
                                    mid = False

                                top = False

                            if v > 5:
                                if k == 0:
                                    top = False
                                elif k == 1:
                                    mid = False
                                elif k == 2:
                                    bottom = False

                        if isinstance(collectPath, dict):
                            if x.name == "," and top:
                                currentKeys[0] += 1
                                if MOVESLIST[x.name] not in collectPath:
                                    collectPath[MOVESLIST[x.name]] = 1
                                else:
                                    collectPath[MOVESLIST[x.name]] += 1
                            elif x.name == "." and mid:
                                currentKeys[1] += 1
                                if MOVESLIST[x.name] not in collectPath:
                                    collectPath[MOVESLIST[x.name]] = 1
                                else:
                                    collectPath[MOVESLIST[x.name]] += 1
                            elif x.name == "/" and bottom:
                                currentKeys[2] += 1
                                if MOVESLIST[x.name] not in collectPath:
                                    collectPath[MOVESLIST[x.name]] = 1
                                else:
                                    collectPath[MOVESLIST[x.name]] += 1
                    break
        elif x.name in [str(x) for x in range(10)]:
            if x.name not in abilities:
                abilities.append(x.name)
        elif isinstance(currTower, TOWER):
            index: int = 0
            action: int = 0

            add: bool = False
            for tower in towerList:
                if tower == currTower:
                    if x.name == "backspace":
                        tower.sold = True
                        action = -2
                        add = True
                    elif x.name == "tab":
                        action = -3
                        add = True
                    break
                index += 1

            if add:
                monkeyUpgradeOrder.append(
                    {f'{currTower.name.replace(" ", "_").upper()}{index}': action}
                )


# Return the distance from the mouse positon and the requested tower position
def distance(x1: int, x2: int, y1: int, y2: int) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Handle Mouse Clicks
def clicker() -> None:
    global towerName
    global gKey
    global towerList
    global currTower
    global collectPath
    global currentKeys
    global monkeyUpgradeOrder
    global towerPlaceIndex
    inList: bool = False
    pos: tuple[int, int] = get_position()
    closest: TOWER | None = None
    trueClosest: TOWER | None = None
    smallestDistance: float = 100000
    towerDistance: float = 0

    for tower in towerList:
        towerDistance = distance(pos[0], tower.x, pos[1], tower.y)
        if tower.sold == False and towerDistance < smallestDistance:
            smallestDistance = towerDistance
            closest = tower

    if smallestDistance < 50:
        inList = True
        trueClosest = closest

    if isinstance(gKey, str) and isinstance(towerName, str) and not inList:
        if gKey == "u":
            towerList.append(TOWER(pos[0], pos[1], towerName, False, gKey, False))
        else:
            towerList.append(
                TOWER(pos[0], pos[1], towerName, False, gKey, False, [], [0, 0, 0])
            )

        monkeyUpgradeOrder.append(
            {f'{towerName.replace(" ", "_").upper()}{towerPlaceIndex}': -1}
        )

        towerPlaceIndex += 1

        towerName = None
        gKey = None
    else:
        index: int = 0

        for tower in towerList:
            if (
                tower == currTower
                and isinstance(tower.path, list)
                and isinstance(collectPath, dict)
                and tower.name != "Hero"
            ):
                tower.path.append(collectPath)
                collectPath = None
                currentKeys = None

                monkeyUpgradeOrder.append(
                    {
                        f'{tower.name.replace(" ", "_").upper()}{index}': len(
                            tower.path
                        )
                        - 1
                    }
                )
                break

            index += 1

        currTower = trueClosest


def main() -> None:
    global authorName
    global mapName
    global mapScreen
    global mapRowCol
    global difficulty
    global gameType
    global gameTypeRowCol
    global instaMonkey

    json: JSON | None = None

    with open("./config.json") as f:
        json = load(f)

    if json:
        authorName = json["authorName"]
        mapName = json["mapName"]
        mapScreen = json["mapScreen"]
        mapRowCol = json["mapRowCol"]
        difficulty = json["difficulty"]
        gameType = json["gameType"]
        gameTypeRowCol = json["gameTypeRowCol"]
        instaMonkey = json["instaMonkey"]

    on_press(input, suppress=False)
    on_click(clicker)

    wait("ctrl+c")

    with open("map.py", "w+") as f:
        header(f)

        for tower in towerList:
            writeTower(tower.x, tower.y, tower.name, tower.key, tower.path, f)

        f.write("ALLTOWERS: list[TOWER] = [\n")

        for name in stringTowerList:
            f.write(f"\t{name},\n")

        f.write("]\n")
        f.write(f"ABILITIES: list[str] = {abilities}\n")

        runner(f)


if __name__ == "__main__":
    main()
