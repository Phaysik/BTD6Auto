#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2019-12-29
Date     : 2019-12-29
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *

# CONSTS
ADORA: TOWER = TOWER(x = 474, y = 406, location = (1754, 215), mType = 'HERO', name = 'Adora', currentMonkey = False)
DART: TOWER = TOWER(x = 591, y = 403, location = (1888, 215), mType = 'NORMAL', name = 'Dart Monkey', currentMonkey = False, path = (0, 3, 2), currentUpgrades = [0, 0, 0])
SUPER: TOWER = TOWER(x = 616, y = 513, location = (1751, 313), mType = 'MAGIC', name = 'Super Monkey', currentMonkey = False, path = (2, 0, 4), currentUpgrades = [0, 0, 0])
TACK: TOWER = TOWER(x = 476, y = 495, location = (1749, 533), mType = 'NORMAL', name = 'Tack Shooter', currentMonkey = False, path = (2, 0, 5), currentUpgrades = [0, 0, 0])
VILLAGE: TOWER = TOWER(x = 382, y = 513, location = (1745, 794), mType = 'SUPPORT', name = 'Monkey Village', currentMonkey = False, path = (3, 2, 0), currentUpgrades = [0, 0, 0])
ALCHEMIST: TOWER = TOWER(x = 463, y = 551, location = (1745, 467), mType = 'MAGIC', name = 'Alchemist', currentMonkey = False, path = (5, 0, 2), currentUpgrades = [0, 0, 0])
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

# Place down Adora
def adora() -> None:    
    while (not determineMonkey(ADORA)):
        pass
        
    setCurrentMonkey(ADORA, ALLTOWERS)
    placing(ADORA)
    gamePress('u', 1)
    gameClick(ADORA, 1)

# Place and upgrade the Dart Monkey
def dart() -> None:
    while (not determineMonkey(DART)):
        pass
    
    setCurrentMonkey(DART, ALLTOWERS)
    placing(DART)
    gamePress('q', 1)
    gameClick(DART, 2)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    if (DART.path is not None and DART.currentUpgrades is not None):
        for i in range(DART.path[1]):
            while (not determineMove('mid')):
                pass
            
            DART.currentUpgrades[1] += 1
            upgrades(DART)
            gamePress('.', 1)
            
        for i in range(DART.path[2]):
            while (not determineMove('low')):
                pass
            
            DART.currentUpgrades[2] += 1
            upgrades(DART)
            gamePress('/', 1)
            
    killThread(levelUp)
    
# Place and upgrade the Super Monkey
def superMonkey(call: int) -> None:
    if (call == 1):
        gameScroll(-1)
        
        levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
        
        while (not determineMonkey(SUPER)):
            pass
        
        killThread(levelUp)
        
        setCurrentMonkey(SUPER, ALLTOWERS)
        placing(SUPER)
        gamePress('s', 1)
        gameClick(SUPER, 2)
        
        levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
        
        if (SUPER.path is not None and SUPER.currentUpgrades is not None):
            for i in range(SUPER.path[2] - 2):
                while (not determineMove('low')):
                    pass
                
                SUPER.currentUpgrades[2] += 1
                upgrades(SUPER)
                gamePress('/', 1)
            
            for i in range(SUPER.path[0]):
                while (not determineMove('top')):
                    pass
            
                SUPER.currentUpgrades[0] += 1
                upgrades(SUPER)
                gamePress(',', 1)
                
        killThread(levelUp)
    else:
        gameClick(SUPER, 1)
        setCurrentMonkey(SUPER, ALLTOWERS)
        
        levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
        
        if (SUPER.path is not None and SUPER.currentUpgrades is not None):
            for i in range(SUPER.path[2] - 2):
                while (not determineMove('low')):
                    pass
                
                SUPER.currentUpgrades[2] += 1
                upgrades(SUPER)
                gamePress('/', 1)
        
        killThread(levelUp)

# Place and upgrade the Tack Shooter
def tack() -> None:
    gameScroll(1)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    while (not determineMonkey(TACK)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(TACK, ALLTOWERS)
    placing(TACK)
    gamePress('r', 1)
    gameClick(TACK, 2)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    if (TACK.path is not None and TACK.currentUpgrades is not None):
        for i in range(TACK.path[0]):
            while (not determineMove('top')):
                pass
            
            TACK.currentUpgrades[0] += 1
            upgrades(TACK)
            gamePress(',', 1)
        
        for i in range(TACK.path[2]):
            while (not determineMove('low')):
                pass
            
            TACK.currentUpgrades[2] += 1
            upgrades(TACK)
            gamePress('/', 1)
            
        killThread(levelUp)

# Place and upgrade the Monkey Village
def village() -> None:
    gameScroll(-1)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    while (not determineMonkey(VILLAGE)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(VILLAGE, ALLTOWERS)
    placing(VILLAGE)
    gamePress('k', 1)
    gameClick(VILLAGE, 2)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    if (VILLAGE.path is not None and VILLAGE.currentUpgrades is not None):
        for i in range(VILLAGE.path[0]):
            while (not determineMove('top')):
                pass
            
            VILLAGE.currentUpgrades[0] += 1
            upgrades(VILLAGE)
            gamePress(',', 1)
        
        for i in range(VILLAGE.path[1]):
            while (not determineMove('mid')):
                pass
        
            VILLAGE.currentUpgrades[1] += 1
            upgrades(VILLAGE)
            gamePress('.', 1)
            
        killThread(levelUp)

# Place and upgrade the Alchemist Monkey
def alchemist() -> None:
    gameScroll(-1)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
        
    while (not determineMonkey(ALCHEMIST)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(ALCHEMIST, ALLTOWERS)
    placing(ALCHEMIST)
    gamePress('f', 1)
    gameClick(ALCHEMIST, 2)
    
    levelUp = levelThread(DIM, DIMVALUES, ALLTOWERS)
    
    if (ALCHEMIST.path is not None and ALCHEMIST.currentUpgrades is not None):
        for i in range(ALCHEMIST.path[0]):
            while (not determineMove('top')):
                pass
            
            ALCHEMIST.currentUpgrades[0] += 1
            upgrades(ALCHEMIST)
            gamePress(',', 1)
        
        for i in range(ALCHEMIST.path[2]):
            while (not determineMove('low')):
                pass
            
            ALCHEMIST.currentUpgrades[2] += 1
            upgrades(ALCHEMIST)
            gamePress('/', 1)
        
    killThread(levelUp)

# 40 rounds for non-decreased xp
def xp() -> None:
    signal(SIGINT, signal_handler)
    iteration: int = 1
    
    while (True):
        clear()
        
        print('Starting Monkey Meadow - Easy (Round 40 restart)')
        print(f'Current iteration: {iteration}\n')
        
        activeWindow()
        
        moveTo(1733, 337)
        sleep(1)
        gameScroll(1)
        gamePress('space', 2)
        adora()
        
        ability = adoraThread()
        
        dart()        
        superMonkey(1)
        freeplay(DIM, DIMVALUES, ALLTOWERS)
        restart(DIM, DIMVALUES, ALLTOWERS, 'RESTART')
        
        killThread(ability)
        
        sleep(3)
        iteration += 1

# 100 rounds for a free insta monkey
def insta() -> None:
    signal(SIGINT, signal_handler)
    iteration: int = 1

    while (True):
        clear()
        
        print('Starting Monkey Meadow - Easy (Round 100 restart)')
        print(f'Current iteration: {iteration}\n')
        
        activeWindow()
        moveTo(1733, 337)
        sleep(1)
        gameScroll(1)
        gamePress('space', 2)
        adora()
        
        ability = adoraThread()
        
        dart()
        superMonkey(1)
        freeplay(DIM, DIMVALUES, ALLTOWERS)
        gamePress('space', 1)
        tack()
        village()
        alchemist()
        superMonkey(2)
        restart(DIM, DIMVALUES, ALLTOWERS, 'BAD')
        
        killThread(ability)
        
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