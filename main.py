#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2019-12-29
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
class TOWER:
    x: int
    y: int
    location: Tuple[int, int]
    mType: str
    name: str
    currentMonkey: bool
    path: Optional[Tuple[int, int, int]] = None
    currentUpgrades: Optional[List[int]] = None
    
@dataclass
class RGB:
    r: int
    g: int
    b: int
    
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
    'HERO': RGB(230, 200, 0),
    'NORMAL': RGB(130, 200, 220),
    'MAGIC': RGB(170, 130, 230),
    'SUPPORT': RGB(200, 180, 130),
}
HOME: Tuple[int, int] = (803, 866)
HOMEVALUES: RGB = RGB(20, 210, 240)
BAD: Tuple[int, int] = (1212, 673)
BADVALUES: RGB = RGB(r = 230, g = 105, b = 35)

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

# Scroll the Monkey Window
def gameScroll(value: int) -> None:    
    moveTo(1733, 337)
    sleep(.5)
    
    for i in range(20):
        scroll(value)
        
    sleep(.5)

# Click on an empty and safe area of the screen
def gameSafeClick() -> None:
    moveTo(100, 100)
    click(100, 100)
    
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

# Determine if a monkey is available for purchase
def determineMonkey(monkey: TOWER) -> bool:
    IMAGE: Tuple[int, int, int] = getImage().getpixel(monkey.location)
    return ((IMAGE[0] >= COLORS[monkey.mType].r) and (IMAGE[1] >= COLORS[monkey.mType].g) and (IMAGE[2] >= COLORS[monkey.mType].b))

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
    IMAGE: Tuple[int, int, int] = getImage().getpixel(region)
    return ((IMAGE[0] <= values.r) and (IMAGE[1] <= values.g) and (IMAGE[2] <= values.b))

# Print out what tower is being placed at which (x, y)
def placing(tower: TOWER) -> None:
    print(f'Placing {tower.name} at ({tower.x}, {tower.y})')

# Print out the current upgrade path of the given tower
def upgrades(tower: TOWER) -> None:
    if (tower.currentUpgrades is not None):
        print(f'Upgrading {tower.name} to {"-".join([str(i) for i in tower.currentUpgrades])}')

# Set all towers currentUpgrades attribute back to 0
def defaultUpgrades(towers: List[TOWER]) -> None:
    for monkey in towers:
        if (monkey.currentUpgrades is not None):
            monkey.currentUpgrades = [0, 0, 0]

# Clear the console
def clear():
    system('cls' if name=='nt' else 'clear')

# Deal with any potential level ups as they appear
def level(region: Tuple[int, int], values: RGB, towers: List[TOWER]) -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        if (determineDim(region, values)):
            for tower in towers:
                if (tower.currentMonkey):
                    gameClick(tower, 1)
        
        moveTo(1470, 298)
        click(1470, 298)
        sleep(.2)
        
# Activate Adora's first and third abilities when available
def adoraAbilities() -> None:
    t = currentThread()
    while getattr(t, "do_run", True):
        sleep(.1)
        press('1')
        press('3')

# Create and start the leveling up thread
def levelThread(region: Tuple[int, int], values: RGB, towers: List[TOWER]) -> Thread:
    levelUp = Thread(target = level, args = (region, values, towers), daemon = True)
    levelUp.start()
    return levelUp

# Create and start the Adora's abilities thread
def adoraThread() -> Thread:
    aThread = Thread(target = adoraAbilities, daemon = True)
    aThread.start()
    return aThread

# Kill a thread
def killThread(thread: Thread) -> None:
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
    LEVELUP = levelThread(dimRegion, dimValues, towers)
    
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
        LEVELUP = levelThread(dimRegion, dimValues, towers)
        
        print('Determining if BAD has been defeated.')
        
        while (not determineDim(dimRegion, dimValues)):
            pass
        
        killThread(LEVELUP)
        sleep(.1)
        
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
