#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2020-01-07
Date     : 2020-01-07
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *

# CONSTS
DIM: Tuple[int, int] = (511, 1062)
DIMVALUES: RGB = RGB(r = 51, g = 67, b = 30)

def main() -> None:
    signal(SIGINT, signal_handler)
    iteration: int = 1
    
    while (True):
        levelUp: gameThread = levelThread(ALLTOWERS)
        
        clear()
        
        print('Starting Monkey Meadow - Easy - Primary Monkeys Only')
        print(f'Current iteration: {iteration}\n')
        
        activeWindow()
        
        sleep(1)
        gamePress('space', 2)
    
if __name__ == "__main__":
    main()