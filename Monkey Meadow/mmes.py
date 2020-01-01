#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2019-12-30
Date     : 2019-12-29
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *

# CONSTS
ADORA: TOWER = TOWER(x = 474, y = 406, location = (1754, 215), mType = 'HERO', name = 'Adora', currentMonkey = False, placementRegion = (397, 286), placementValues = RGB(140, 190, 40))
DART: TOWER = TOWER(x = 591, y = 403, location = (1888, 215), mType = 'NORMAL', name = 'Dart Monkey', currentMonkey = True, placementRegion = (665, 349), placementValues = RGB(140, 190, 40), path = (0, 3, 2), currentUpgrades = [0, 0, 0])
SUPER: TOWER = TOWER(x = 616, y = 513, location = (1751, 313), mType = 'MAGIC', name = 'Super Monkey', currentMonkey = False, placementRegion = (741, 531), placementValues = RGB(150, 195, 40), path = (2, 0, 4), currentUpgrades = [0, 0, 0])
TACK: TOWER = TOWER(x = 476, y = 495, location = (1749, 533), mType = 'NORMAL', name = 'Tack Shooter', currentMonkey = False, placementRegion = (395, 528), placementValues = RGB(160, 205, 40), path = (2, 0, 5), currentUpgrades = [0, 0, 0])
VILLAGE: TOWER = TOWER(x = 382, y = 513, location = (1745, 794), mType = 'SUPPORT', name = 'Monkey Village', currentMonkey = False, placementRegion = (255, 529), placementValues = RGB(150, 200, 40), path = (3, 2, 0), currentUpgrades = [0, 0, 0])
ALCHEMIST: TOWER = TOWER(x = 463, y = 551, location = (1745, 467), mType = 'MAGIC', name = 'Alchemist', currentMonkey = False, placementRegion = (266, 537), placementValues = RGB(165, 200, 40), path = (5, 0, 2), currentUpgrades = [0, 0, 0])
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

# Place down Adora
def adora() -> None:
    nextTower(ADORA)
        
    while (not determineMonkey(ADORA)):
        pass
        
    setCurrentMonkey(ADORA, ALLTOWERS)
    placing(ADORA)
    
    while (not determinePlacement(ADORA)):
        gamePress('u', 1)
        gameClick(ADORA, 2)
        
    gameSafeClick()

# Place and upgrade the Dart Monkey
def dart() -> None:
    nextTower(DART)
    
    while (not determineMonkey(DART)):
        pass
    
    setCurrentMonkey(DART, ALLTOWERS)
    placing(DART)
    
    while (not determinePlacement(DART)):
        gamePress('q', 1)
        gameClick(DART, 2)
    
    levelUp: gameThread = levelThread(ALLTOWERS)
    
    if (DART.path is not None and DART.currentUpgrades is not None):
        for i in range(DART.path[1]):
            nextUpgrade(DART, 1)
            
            while (not determineMove('mid')):
                pass
            
            DART.currentUpgrades[1] += 1
            upgrades(DART)
            gamePress('.', 1)
            
        for i in range(DART.path[2]):
            nextUpgrade(DART, 2)
            
            while (not determineMove('low')):
                pass
            
            DART.currentUpgrades[2] += 1
            upgrades(DART)
            gamePress('/', 1)
            
    killThread(levelUp)
    gameSafeClick()
    
# Place and upgrade the Super Monkey
def superMonkey(call: int) -> None:
    if (call == 1):
        gameScroll(-1)
        gameSafeClick()
        
        levelUp: gameThread = levelThread(ALLTOWERS)
        
        nextTower(SUPER)
        
        while (not determineMonkey(SUPER)):
            pass
        
        killThread(levelUp)
        
        setCurrentMonkey(SUPER, ALLTOWERS)
        placing(SUPER)
        
        while (not determinePlacement(SUPER)):
            gamePress('s', 1)
            gameClick(SUPER, 2)
        
        levelUp = levelThread(ALLTOWERS)
        
        if (SUPER.path is not None and SUPER.currentUpgrades is not None):
            for i in range(SUPER.path[2] - 2):
                nextUpgrade(SUPER, 2)
                
                while (not determineMove('low')):
                    pass
                
                SUPER.currentUpgrades[2] += 1
                upgrades(SUPER)
                gamePress('/', 1)
            
            for i in range(SUPER.path[0]):
                nextUpgrade(SUPER, 0)
                
                while (not determineMove('top')):
                    pass
            
                SUPER.currentUpgrades[0] += 1
                upgrades(SUPER)
                gamePress(',', 1)
                
        killThread(levelUp)
        gameSafeClick()
    else:
        gameClick(SUPER, 1)
        setCurrentMonkey(SUPER, ALLTOWERS)
        
        levelUp = levelThread(ALLTOWERS)
        
        if (SUPER.path is not None and SUPER.currentUpgrades is not None):
            for i in range(SUPER.path[2] - 2):
                nextUpgrade(SUPER, 2)
                
                while (not determineMove('low')):
                    pass
                
                SUPER.currentUpgrades[2] += 1
                upgrades(SUPER)
                gamePress('/', 1)
        
        killThread(levelUp)
        gameSafeClick()

# Place and upgrade the Tack Shooter
def tack() -> None:
    gameScroll(1)
    
    levelUp: gameThread = levelThread(ALLTOWERS)
    
    nextTower(TACK)
    
    while (not determineMonkey(TACK)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(TACK, ALLTOWERS)
    placing(TACK)
    
    while (not determinePlacement(TACK)):
        gamePress('r', 1)
        gameClick(TACK, 2)
    
    levelUp = levelThread(ALLTOWERS)
    
    if (TACK.path is not None and TACK.currentUpgrades is not None):
        for i in range(TACK.path[0]):
            nextUpgrade(TACK, 0)
            
            while (not determineMove('top')):
                pass
            
            TACK.currentUpgrades[0] += 1
            upgrades(TACK)
            gamePress(',', 1)
        
        for i in range(TACK.path[2]):
            nextUpgrade(TACK, 2)
            
            while (not determineMove('low')):
                pass
            
            TACK.currentUpgrades[2] += 1
            upgrades(TACK)
            gamePress('/', 1)
            
        killThread(levelUp)
        gameSafeClick()

# Place and upgrade the Monkey Village
def village() -> None:
    gameScroll(-1)
    
    levelUp: gameThread = levelThread(ALLTOWERS)
    
    nextTower(VILLAGE)
    
    while (not determineMonkey(VILLAGE)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(VILLAGE, ALLTOWERS)
    placing(VILLAGE)
    
    while (not determinePlacement(VILLAGE)):
        gamePress('k', 1)
        gameClick(VILLAGE, 2)
    
    levelUp = levelThread(ALLTOWERS)
    
    if (VILLAGE.path is not None and VILLAGE.currentUpgrades is not None):
        for i in range(VILLAGE.path[0]):
            nextUpgrade(VILLAGE, 0)
            
            while (not determineMove('top')):
                pass
            
            VILLAGE.currentUpgrades[0] += 1
            upgrades(VILLAGE)
            gamePress(',', 1)
        
        for i in range(VILLAGE.path[1]):
            nextUpgrade(VILLAGE, 1)
            
            while (not determineMove('mid')):
                pass
        
            VILLAGE.currentUpgrades[1] += 1
            upgrades(VILLAGE)
            gamePress('.', 1)
            
        killThread(levelUp)
        gameSafeClick()

# Place and upgrade the Alchemist Monkey
def alchemist() -> None:
    gameScroll(-1)
    
    levelUp: gameThread = levelThread(ALLTOWERS)
    
    nextTower(ALCHEMIST)
    
    while (not determineMonkey(ALCHEMIST)):
        pass
    
    killThread(levelUp)
    
    setCurrentMonkey(ALCHEMIST, ALLTOWERS)
    placing(ALCHEMIST)
    
    while (not determinePlacement(ALCHEMIST)):
        gamePress('f', 1)
        gameClick(ALCHEMIST, 2)
    
    levelUp = levelThread(ALLTOWERS)
    
    if (ALCHEMIST.path is not None and ALCHEMIST.currentUpgrades is not None):
        for i in range(ALCHEMIST.path[0] - 1):
            nextUpgrade(ALCHEMIST, 0)
            
            while (not determineMove('top')):
                pass
            
            ALCHEMIST.currentUpgrades[0] += 1
            upgrades(ALCHEMIST)
            gamePress(',', 1)
        
        for i in range(ALCHEMIST.path[2]):
            nextUpgrade(ALCHEMIST, 2)
            
            while (not determineMove('low')):
                pass
            
            ALCHEMIST.currentUpgrades[2] += 1
            upgrades(ALCHEMIST)
            gamePress('/', 1)
            
        for i in range(ALCHEMIST.path[0] - 4):
            nextUpgrade(ALCHEMIST, 0)
            
            while (not determineMove('top')):
                pass
            
            ALCHEMIST.currentUpgrades[0] += 1
            upgrades(ALCHEMIST)
            gamePress(',', 1)
        
    killThread(levelUp)
    gameSafeClick()

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
        
        ability = abilityThread(ABILITIES)
        
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
        
        ability = abilityThread(ABILITIES)
        
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