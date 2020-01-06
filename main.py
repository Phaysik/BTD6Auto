#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2020-01-06
Date     : 2019-12-28
"""

from pyautogui import click, press, hotkey, moveTo, scroll
import win32gui
from typing import List, Tuple, Dict, Optional, Union
from time import sleep
from PIL import ImageGrab, Image
from dataclasses import dataclass
import sys
from signal import signal, SIGINT
from threading import Thread, currentThread
from os import system, name

@dataclass
class RGB:
    r: int
    g: int
    b: int

@dataclass
class TOWER:
    x: int
    y: int
    location: Tuple[int, int]
    mType: str
    name: str
    currentMonkey: bool
    key: str
    path: Optional[List[Dict[int, int]]] = None
    currentUpgrades: Optional[List[int]] = None

class gameThread(Thread):
    def __init__(self, target, daemon: bool, args: Union[List[TOWER], List[str]]):
        Thread.__init__(self, target = target, args = [args], daemon = daemon)
        self.do_run = True

# CONSTS
BOX: Tuple[int, int, int, int] = (0, 0, 1920, 1080)
TOPBOX: Tuple[int, int] = (1424, 520)
MIDBOX: Tuple[int, int] = (1424, 700)
LOWBOX: Tuple[int, int] = (1424, 880)
REGION: Dict[str, Tuple[int, int]] = {
    'top': TOPBOX,
    'mid': MIDBOX,
    'low': LOWBOX
}
COLORS: Dict[str, RGB] = {
    'HERO': RGB(r = 230, g = 200, b = 0),
    'NORMAL': RGB(r = 130, g = 180, b = 180),
    'MAGIC': RGB(r = 170, g = 130, b = 170),
    'SUPPORT': RGB(r = 200, g = 180, b = 130),
}
MOVES: Dict[int, str] = {
    0: ',',
    1: '.',
    2: '/'
}
MOVESREGION: Dict[int, str] = {
    0: 'top',
    1: 'mid',
    2: 'low'
}
HOME: Tuple[int, int] = (803, 866)
HOMEVALUES: RGB = RGB(r = 20, g = 210, b = 240)
BAD: Tuple[int, int] = (1212, 673)
BADVALUES: RGB = RGB(r = 230, g = 105, b = 35)
LEVELMONKEY: Tuple[int, int] = (191, 905)
LEVELMONKEYVALUES: RGB = RGB(r = 140, g = 100, b = 50)
LEVELBANNER: Tuple[int, int] = (1133, 548)
LEVELBANNERVALUES: RGB = RGB(r = 220, g = 100, b = 40)
LEVELSTAR: Tuple[int, int] = (958, 381)
LEVELSTARVALUES: RGB = RGB(r = 230, g = 200, b = 20)
PLACEMENT: Tuple[int, int] = (1207, 56)
PLACEMENTVALUES: RGB = RGB(r = 180, g = 170, b = 110)

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
# Click in a certain location
def gameClick(location: TOWER, times: int) -> None:
    for i in range(times):
        sleep(.2)
        moveTo(location.x, location.y)
        click(location.x, location.y)
    
# Press a certain key
def gamePress(key: str, times: int) -> None:
    for i in range(times):
        sleep(.2)
        press(key)
        
# Click on an empty and safe area of the screen
def gameSafeClick() -> None:
    moveTo(100, 100)
    click(100, 100)

# Place and upgrade tower
def gamePlaceTower(index: int, tower: TOWER, allTowers: List[TOWER]) -> None:
    if (index == 0):
        nextTower(tower)

        while (not determinePlacement()):
            gamePress(tower.key, 1)
            gameClick(tower, 2)

        placing(tower)
    else:
        gameClick(tower, 1)
    
    setCurrentMonkey(tower, allTowers)
    
    if (tower.path is not None and tower.currentUpgrades is not None):
        for key, value in tower.path[index].items():
            for i in range(value):
                nextUpgrade(tower, key)
                
                while (not determineMove(MOVESREGION[key])):
                    pass
                
                tower.currentUpgrades[key] += 1
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
    sleep(.1)
    return ImageGrab.grab(BOX)

# Determine if an upgrade is available to purchase
def determineMove(region: str) -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(REGION[region])
    return ((IMAGE[0] >= 60) and (IMAGE[1] >= 200) and (IMAGE[2] <= 20))

# Determine if the home button is on screen
def determineHome() -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(HOME)
    return ((IMAGE[0] <= HOMEVALUES.r) and (IMAGE[1] >= HOMEVALUES.g) and (IMAGE[2] >= HOMEVALUES.b))

# Determine if the BAD has been defeated
def determineBAD() -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(BAD)
    return ((IMAGE[0] >= BADVALUES.r) and (IMAGE[1] <= BADVALUES.g) and (IMAGE[2] <= BADVALUES.b))

# Determine if the screen has dimmed upon defeating either the MOAB or BAD
def determineDim(region: Tuple[int, int], values: RGB) -> bool:
    if (determineLevelUp()):
        return False
    
    IMAGE: Tuple[int, int, int] = getImage().getpixel(region)
    return (IMAGE[0] <= values.r) and (IMAGE[1] <= values.g) and (IMAGE[2] <= values.b)

# Determine if the user has leveled up
def determineLevelUp() -> bool:
    LEVELIMAGE: Tuple[int, int, int] = getImage().getpixel(LEVELMONKEY)    
    BANNERIMAGE: Tuple[int, int, int] = getImage().getpixel(LEVELBANNER)    
    STARIMAGE: Tuple[int, int, int] = getImage().getpixel(LEVELSTAR)
    return (((LEVELIMAGE[0] >= LEVELMONKEYVALUES.r) and (LEVELIMAGE[1] <= LEVELMONKEYVALUES.g) and (LEVELIMAGE[2] <= LEVELMONKEYVALUES.b)) and ((BANNERIMAGE[0] >= LEVELBANNERVALUES.r) and (BANNERIMAGE[1] <= LEVELBANNERVALUES.g) and (BANNERIMAGE[2] <= LEVELBANNERVALUES.b)) and ((STARIMAGE[0] >= LEVELSTARVALUES.r) and (STARIMAGE[1] >= LEVELSTARVALUES.g) and (STARIMAGE[2] <= LEVELSTARVALUES.b)))

# Determine if the tower was placed
def determinePlacement() -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(PLACEMENT)
    return ((IMAGE[0] >= PLACEMENTVALUES.r) and (IMAGE[1] <= PLACEMENTVALUES.g) and (IMAGE[2] <= PLACEMENTVALUES.b))

# Print out what tower is being bought next
def nextTower(tower: TOWER) -> None:
    print(f'Waiting on {tower.name} availability.')
    
# Print out what tower is being placed at which (x, y)
def placing(tower: TOWER) -> None:
    print(f'Placing {tower.name} at ({tower.x}, {tower.y}).')

# Print out the what upgrade is getting bought next
def nextUpgrade(tower: TOWER, currentPath: int) -> None:
    if (tower.currentUpgrades is not None):
        print(f'Waiting on {tower.name} {"-".join([str(tower.currentUpgrades[i] + 1) if (currentPath == i) else (str(tower.currentUpgrades[i])) for i in range(len(tower.currentUpgrades))])}.')
        
# Print out the current upgrade path of the given tower
def upgrades(tower: TOWER) -> None:
    if (tower.currentUpgrades is not None):
        print(f'Upgrading {tower.name} to {"-".join([str(i) for i in tower.currentUpgrades])}.')

# Set all towers currentUpgrades attribute back to 0
def defaultUpgrades(towers: List[TOWER]) -> None:
    for monkey in towers:
        if (monkey.currentUpgrades is not None):
            monkey.currentUpgrades = [0, 0, 0]

# Clear the console
def clear():
    system('cls' if name=='nt' else 'clear')

# Deal with any potential level ups as they appear
def level(towers: List[TOWER]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        if (determineLevelUp()):
            print('Level up detected. Attempting to clear and continue program...')
            
            for tower in towers:
                if (tower.currentMonkey):
                    for i in range(2):
                        sleep(.2)
                        moveTo(1470, 298)
                        click(1470, 298)
                        
                    gameClick(tower, 1)
                    press('space')
                    
# Activate Adora's first and third abilities when available
def gameAbilities(abilities: List[str]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        sleep(.1)
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
        if (tower == monkey):
            monkey.currentMonkey = True
        else:
            monkey.currentMonkey = False

# Deal with the freeplay button
def freeplay(dimRegion: Tuple[int, int], dimValues: RGB, towers: List[TOWER]) -> None:
    LEVELUP: gameThread = levelThread(towers)
    
    print('Determining if MOAB has been defeated.')
    
    while (not determineDim(dimRegion, dimValues)):
        pass
    
    killThread(LEVELUP)
    
    print('MOAB defeated. Determining if VICTORY screen has appeared.')
    
    while (not determineHome()):
        pass
    
    print('VICTORY achieved. Going into freeplay...')
    
    sleep(1)
    moveTo(1194, 899)
    click(1194, 899)
    sleep(1)
    moveTo(1024, 750)
    click(1024, 750)

# Restart the game
def restart(dimRegion: Tuple[int, int], dimValues: RGB, towers: List[TOWER], insta: str) -> None:
    if (insta == 'BAD'):
        LEVELUP: gameThread = levelThread(towers)
        
        print('Determining if BAD has been defeated.')
        
        while (not determineDim(dimRegion, dimValues)):
            pass
        
        killThread(LEVELUP)
        
        print('BAD defeated. Determining if Insta Monkey screen has appeared.')
        
        while (not determineBAD()):
            pass
        
        print('Insta Monkey acquired. Going into freeplay...')
        
        sleep(1)
        moveTo(881, 437)
        click(881, 437)
        
    print('Restarting...')
    
    defaultUpgrades(towers)
    sleep(1)
    moveTo(1556, 50)
    click(1556, 50)
    sleep(1)
    moveTo(1128, 887)
    click(1128, 887)
    sleep(1)
    moveTo(1196, 748)
    click(1196, 748)

# Close all threads and exit the program on Ctrl + C key combination
def signal_handler(sig, frame) -> None:
    sys.exit(0)  
