#!/usr/bin/env python3
"""
Author   : Matthew Moore
Revision : 2020-01-07
Date     : 2020-01-06
"""

from tkinter import *
from tkinter.ttk import Treeview
from typing import List, Dict, Union
from json import loads    

class Maps:
    def __init__(self, master: Tk) -> None:
        self.window: Tk = master
        self.tree: Treeview = Treeview(self.window)
        self.tree.column('#0', width = 250)
        self.tree.heading('#0', text = 'Maps')
        self.tree.pack(side = LEFT, fill = Y)
        self.tree.bind("<Double-1>", self.onDoubleClick)
        self.map: str = ''
        self.easy: str = ''
        self.medium: str = ''
        self.hard: str = ''
        self.easyModes: List[str] = []
        self.mediumModes: List[str] = []
        self.hardModes: List[str] = []
        self.increment: int = 0
        self.frame: LabelFrame = LabelFrame(self.window, padx = 20, pady = 10)
        self.frame.pack(fill = BOTH, padx = 20)
        
    def createMap(self, mapTitle: str) -> None:
        self.map = self.tree.insert('', self.increment, text = mapTitle)
        self.easy = self.tree.insert(self.map, 'end', text = 'Easy')
        self.medium = self.tree.insert(self.map, 'end', text = 'Medium')
        self.hard = self.tree.insert(self.map, 'end', text = 'Hard')

        self.populateDifficulty(self.easy, self.easyModes, 'Easy')
        self.populateDifficulty(self.medium, self.mediumModes, 'Medium')
        self.populateDifficulty(self.hard, self.hardModes, 'Hard')
        
        self.increment += 1
    
    def defaultValues(self) -> None:
        self.easyModes = []
        self.mediumModes = []
        self.hardModes = []
    
    def easyValues(self, gameMode: List[str]) -> None:
        self.easyModes.extend(gameMode)
        
    def mediumValues(self, gameMode: List[str]) -> None:
        self.mediumModes.extend(gameMode)
        
    def hardValues(self, gameMode: List[str]) -> None:
        self.hardModes.extend(gameMode)
            
    def populateDifficulty(self, gameMode: str, gameModeList: List[str], difficulty: str) -> None:
        for mode in gameModeList:
            self.tree.insert(gameMode, 'end', text = mode, tags = [self.tree.item(self.map, "text"), difficulty, mode])

    def onDoubleClick(self, event):
        item = self.tree.focus()
        tags: List[str] = self.tree.item(item, "tags")
        if (len(tags) != 0):
            self.options(tags)
            
    def options(self, tags: List[str]) -> None:
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        name: str = tags[0]
        difficulty: str = tags[1]
        mode: str = tags[2]
        
        label: Label = Label(self.frame, text = f'{name} - {difficulty} - {mode}')
        label.pack()
        
        if (mode == 'Standard'):
            round40: Button = Button(self.frame, text = 'Round 40 restart', command = lambda: self.round40(name, difficulty))
            round100: Button = Button(self.frame, text = 'Round 100 restart', command = lambda: self.round100(name, difficulty))
            round40.pack(side = LEFT)
            round100.pack(side = RIGHT)
            
            # from monkeyMeadow import mmes
            # mmes.xp()
        else:
            execute: Button = Button(self.frame, text = 'Execute program')
            execute.pack()

    def round40(self, name: str, difficulty: str) -> None:
        if (name == 'Monkey Meadow'):
            if (difficulty == 'Easy'):
                from monkeyMeadow.mmes import xp
                xp()
                
    def round100(self, name: str, difficulty: str) -> None:
        if (name == 'Monkey Meadow'):
            if (difficulty == 'Easy'):
                from monkeyMeadow.mmes import insta
                insta()
                
def parseJSON() -> Dict[str, List[Dict[str, Union[str, List[str]]]]]:
    data: str = ''
    
    with open('maps.json', 'r') as maps:
        data = maps.read()
        
    parsedJSON: Dict[str, List[Dict[str, Union[str, List[str]]]]] = loads(data)
    
    return parsedJSON
        
def main() -> None:
    win: Tk = Tk()
    win.title('BTD6 Automation')
    win.geometry('600x600')

    parsedJSON: Dict[str, List[Dict[str, Union[str, List[str]]]]] = parseJSON()
    listOfMaps: List[Dict[str, Union[str, List[str]]]] = parsedJSON['maps']

    maps = Maps(win)
    
    for gameMap in listOfMaps:
        name: str = ''
        easyModes: List[str] = []
        mediumModes: List[str] = []
        hardModes: List[str] = []
        
        if (isinstance(gameMap['name'], str)):
            name = gameMap['name']
            
        if (isinstance(gameMap['easy'], list)):
            easyModes = gameMap['easy']
            
        if (isinstance(gameMap['medium'], list)):
            mediumModes = gameMap['medium']
            
        if (isinstance(gameMap['hard'], list)):
            hardModes = gameMap['hard']
        
        maps.easyValues(easyModes)
        maps.mediumValues(mediumModes)
        maps.hardValues(hardModes)
        maps.createMap(name)

    win.mainloop()

if __name__ == "__main__":
    main()