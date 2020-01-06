#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2020-01-06
Date     : 2019-12-29
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *

# CONSTS
ADORA: TOWER = TOWER(x = 474, y = 406, location = (1754, 215), mType = 'HERO', name = 'Adora', currentMonkey = False, key = 'u')
DART: TOWER = TOWER(x = 591, y = 403, location = (1888, 215), mType = 'NORMAL', name = 'Dart Monkey', currentMonkey = True, key = 'q', path = [{1: 3, 2: 2}], currentUpgrades = [0, 0, 0])
SUPER: TOWER = TOWER(x = 616, y = 513, location = (1751, 313), mType = 'MAGIC', name = 'Super Monkey', currentMonkey = False, key = 's', path = [{2: 2, 0: 2}, {2: 2}], currentUpgrades = [0, 0, 0])
TACK: TOWER = TOWER(x = 476, y = 495, location = (1749, 533), mType = 'NORMAL', name = 'Tack Shooter', currentMonkey = False, key = 'r', path = [{0: 2, 2: 5}], currentUpgrades = [0, 0, 0])
VILLAGE: TOWER = TOWER(x = 382, y = 513, location = (1745, 794), mType = 'SUPPORT', name = 'Monkey Village', currentMonkey = False, key = 'k', path = [{0: 3, 1: 2}], currentUpgrades = [0, 0, 0])
ALCHEMIST: TOWER = TOWER(x = 463, y = 551, location = (1745, 467), mType = 'MAGIC', name = 'Alchemist', currentMonkey = False, key = 'f', path = [{0: 4, 2: 2}, {0: 1}], currentUpgrades = [0, 0, 0])
ALLTOWERS: List[TOWER] = [
    ADORA,
    DART,
    SUPER,
    TACK,
    VILLAGE,
    ALCHEMIST
]
DIM: Tuple[int, int] = (511, 1062)
DIMVALUES: RGB = RGB(r = 51, g = 67, b = 30)
ABILITIES: List[str] = ['1', '3']

# 40 rounds for non-decreased xp
def xp() -> None:
    signal(SIGINT, signal_handler)
    iteration: int = 1
    
    while (True):
        levelUp: gameThread = levelThread(ALLTOWERS)
        
        clear()
        
        print('Starting Monkey Meadow - Easy (Round 40 restart)')
        print(f'Current iteration: {iteration}\n')
        
        activeWindow()
        
        moveTo(1733, 337)
        sleep(1)
        gamePress('space', 2)
        
        gamePlaceTower(0, ADORA, ALLTOWERS)
        
        ability = abilityThread(ABILITIES)
        
        gamePlaceTower(0, DART, ALLTOWERS)     
        gamePlaceTower(0, SUPER, ALLTOWERS)     
        
        freeplay(DIM, DIMVALUES, ALLTOWERS)
        restart(DIM, DIMVALUES, ALLTOWERS, 'RESTART')
        
        killThread(ability)
        killThread(levelUp)
        
        sleep(3)
        iteration += 1

# 100 rounds for a free insta monkey
def insta() -> None:
    signal(SIGINT, signal_handler)
    iteration: int = 1

    while (True):
        levelUp: gameThread = levelThread(ALLTOWERS)
        
        clear()
        
        print('Starting Monkey Meadow - Easy (Round 100 restart)')
        print(f'Current iteration: {iteration}\n')
        
        activeWindow()
        moveTo(1733, 337)
        sleep(1)
        gamePress('space', 2)
        
        gamePlaceTower(0, ADORA, ALLTOWERS)
        
        ability = abilityThread(ABILITIES)
        
        gamePlaceTower(0, DART, ALLTOWERS)
        gamePlaceTower(0, SUPER, ALLTOWERS)
        
        freeplay(DIM, DIMVALUES, ALLTOWERS)
        gamePress('space', 1)
        
        gamePlaceTower(0, TACK, ALLTOWERS)
        gamePlaceTower(0, VILLAGE, ALLTOWERS)
        gamePlaceTower(0, ALCHEMIST, ALLTOWERS)
        gamePlaceTower(1, ALCHEMIST, ALLTOWERS)
        gamePlaceTower(1, SUPER, ALLTOWERS)
        
        restart(DIM, DIMVALUES, ALLTOWERS, 'BAD')
        
        killThread(ability)
        killThread(levelUp)
        
        sleep(3)
        iteration += 1

# Execute the program
def main() -> None:
    arguments = sys.argv[1:]
    
    # Determine valid argument
    if ((len(arguments) != 1) or (arguments[0].lower() != 'x' and arguments[0].lower() != 'i')):
        print('Invalid argument. Must be either a \'x\' or an \'i\'')
        print('Example: python main.py x')
        print('x -> Restart after MOAB')
        print('i -> Restart after BAD')
        sys.exit(0)
    
    arguments[0] = arguments[0].lower()
    # Determine if the user wants to get an insta monkey or just non-decreased xp
    if (arguments[0] == 'x'):
        xp()
    elif (arguments[0] == 'i'):
        insta()

if __name__ == "__main__":
    main()