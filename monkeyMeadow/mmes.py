#!/usr/bin/env python3
"""
Author   : Matthew Moore
Date     : 12/29/2019
Revision : 01/15/2023
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import *


# CONSTS
Hero: TOWER = TOWER(x=494, y=403, name="Hero", currMonkey=False, key="u")
DART: TOWER = TOWER(
    x=617,
    y=402,
    name="Dart Monkey",
    currMonkey=True,
    key="q",
    path=[{1: 3, 2: 2}],
    currUpgrades=[0, 0, 0],
)
SUPER: TOWER = TOWER(
    x=641,
    y=514,
    name="Super Monkey",
    currMonkey=False,
    key="s",
    path=[{2: 2, 0: 2}, {2: 2}],
    currUpgrades=[0, 0, 0],
)
TACK: TOWER = TOWER(
    x=496,
    y=495,
    name="Tack Shooter",
    currMonkey=False,
    key="r",
    path=[{0: 2, 2: 5}],
    currUpgrades=[0, 0, 0],
)
VILLAGE: TOWER = TOWER(
    x=431,
    y=552,
    name="Monkey Village",
    currMonkey=False,
    key="k",
    path=[{0: 3, 1: 2}],
    currUpgrades=[0, 0, 0],
)
ALCHEMIST: TOWER = TOWER(
    x=422,
    y=400,
    name="Alchemist",
    currMonkey=False,
    key="f",
    path=[{0: 4, 2: 2}, {0: 1}],
    currUpgrades=[0, 0, 0],
)
ALLTOWERS: list[TOWER] = [Hero, DART, SUPER, TACK, VILLAGE, ALCHEMIST]
ABILITIES: list[str] = ["1", "3"]

# 40 rounds for non-decreased xp
def xp() -> None:
    iteration: int = 1

    while True:
        levelUp: gameThread = levelThread(ALLTOWERS)
        ability = abilityThread(ABILITIES)

        clear()

        print("Starting Monkey Meadow - Easy - Standard (Round 40 restart)")
        print(f"Current iteration: {iteration}\n")

        activeWindow()

        sleep(1)
        gamePress("space", 2)

        towerManip(-1, Hero, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, DART, ALLTOWERS)
        sleep(0.5)

        towerManip(0, DART, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, SUPER, ALLTOWERS)
        sleep(0.5)

        towerManip(0, SUPER, ALLTOWERS)
        sleep(0.5)

        freeplay()

        restart(ALLTOWERS)

        killThread(levelUp)
        killThread(ability)

        sleep(3)
        iteration += 1


# 100 rounds for a free insta monkey
def insta() -> None:
    iteration: int = 1

    while True:
        levelUp: gameThread = levelThread(ALLTOWERS)
        ability = abilityThread(ABILITIES)

        clear()

        print("Starting Monkey Meadow - Easy - Standard - (Round 100 restart)")
        print(f"Current iteration: {iteration}\n")

        activeWindow()

        sleep(1)
        gamePress("space", 2)

        towerManip(-1, Hero, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, DART, ALLTOWERS)
        sleep(0.5)

        towerManip(0, DART, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, SUPER, ALLTOWERS)
        sleep(0.5)

        towerManip(0, SUPER, ALLTOWERS)
        sleep(0.5)

        freeplay()

        sleep(1)

        gamePress("space", 1)

        towerManip(-1, TACK, ALLTOWERS)
        sleep(0.5)

        towerManip(0, TACK, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, VILLAGE, ALLTOWERS)
        sleep(0.5)

        towerManip(0, VILLAGE, ALLTOWERS)
        sleep(0.5)

        towerManip(-1, ALCHEMIST, ALLTOWERS)
        sleep(0.5)

        towerManip(0, ALCHEMIST, ALLTOWERS)
        sleep(0.5)

        towerManip(1, ALCHEMIST, ALLTOWERS)
        sleep(0.5)

        towerManip(1, SUPER, ALLTOWERS)
        sleep(0.5)

        restart(
            ALLTOWERS,
            1,
            MAPROWCOLPOSITIONS[0][0],
            DIFFICULTYPOSITIONS["Easy"],
            GAMEMODEPOSITIONS[0][0],
            "BAD",
        )

        killThread(levelUp)
        killThread(ability)

        sleep(3)
        iteration += 1


# Execute the program
def main() -> None:
    arguments = sys.argv[1:]

    # Determine valid argument
    if (len(arguments) != 1) or (
        arguments[0].lower() != "x" and arguments[0].lower() != "i"
    ):
        print("Invalid argument. Must be either a 'x' or an 'i'")
        print("Example: python mmes.py x")
        print("x -> Restart after MOAB")
        print("i -> Restart after BAD")
        sys.exit(0)

    arguments[0] = arguments[0].lower()
    # Determine if the user wants to get an insta monkey or just non-decreased xp
    if arguments[0] == "x":
        xp()
    elif arguments[0] == "i":
        insta()


if __name__ == "__main__":
    main()
