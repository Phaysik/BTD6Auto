# BTD6Auto

This program can automate running BTD6 maps, and can even record your own run for future playback.

## Program Requirements

- Download [Python3](https://www.python.org/downloads//)
  - This program was written and tested for 64bit with Python 3.10.6
- This project is tested and written based on:
  - 1920x1080 resolution
  - In-game fullscreen
  - You can change this by altering the values stored in the `globals.py` config file.
    - Please note, that you will most likely have to change most of the values in some way or another if you do decide on a different resolution.
    - In order to determine what values to change to, run

      - ```bash
        python debugging.py position
        ```

      - To determine the x, y coordinates of the mouse

- Program specfic dependencies (Run through command line)

  ```bash
  ./install.sh
  ```

  - You will also need to download the [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and install it to a folder called 'Tesseract' within this directory

## My Map Scripts

### Requirements to run my map scripts

- Please note that some Monkey Knowledge is pobably required in order to successfully run map scripts that I have created
- You must have the game open
  - You do not need to be tabbed in the game
    - The script will tab in for you
- You must be in the map itself

### Running my map scripts

```python
  python path/to/map.py
```

- Some scripts may have command line arguments required
  - Upon running the previous command, these scripts will output a menu of argument options the user could use
- To run a script with a command line argument

```python
  python path/to/map.py [argument]
```

### IMPORTANT

- *DO NOT CHANGE ACTIVE WINDOW OR MESS WITH THE GAME AT ALL.*
  - *THE PROGRAM MAY FAIL TO EXECUTE PROPERLY IF YOU DO*
- *THE PROGRAM WILL TAKE CONTROL OF YOUR MOUSE AND KEYBOARD DURING CERTAIN TIMES IN EXECUTION*
  - *YOU CAN EXIT THE PROGRAM AT ANY TIME BY PRESSING THE KEY/KEY COMBINATION FOR **SIGINT** IN **globals.py***
  - *YOU CAN ALSO EXIT BY MOVING YOUR MOUSE TO THE TOP LEFT CORNER OF YOUR MONITOR*

## Recording your own map run

### Supported and Unsupported Features

- This version currently **does** support:
  - Placing towers
  - Upgrading towers
    - It's able to distinguish between two towers that are the same and are in close proximity which tower you want to upgrade, based on your mouse position
  - Tower upgrade order
  - Tower placement order
  - Selling towers
  - Tab Targeting
  - Freeplay
  - Restarts after getting an Insta-Monkey
  - Using Passive Abilities
    - The caveat is that the ability numbers the user hit in the recording will constantly be fired in the resulting script regardless of when the user fired the ability

- This version currently **does not** support:
  - Shift+Tab Targeting
  - Active Abilities

### Rules for recording

- Please note that this script requires a lot of perfect inputs from the user
- You must use keybindings to select the tower you want to place
  - After hitting a key, you must then place the tower in an appropriate location. This program does not determine if the tower is placed properly.
    - Keys and their towers:
      | Key | Tower            |
      | --- | -----------      |
      | u   | Hero             |
      | q   | Dart Monkey      |
      | w   | Boomerang Monkey |
      | e   | Bomb Shooter     |
      | r   | Tack Shooter     |
      | t   | Ice Monkey       |
      | y   | Glue Gunner      |
      | z   | Sniper Monkey    |
      | x   | Monkey Sub       |
      | c   | Monkey Bucanneer |
      | v   | Monkey Ace       |
      | b   | Heli Pilot       |
      | n   | Mortar Monkey    |
      | m   | Dartling Gunner  |
      | a   | Wizard Monkey    |
      | s   | Super Monkey     |
      | d   | Ninja Monkey     |
      | f   | Alchemist        |
      | g   | Druid            |
      | h   | Banana Farm      |
      | j   | Spike Factory    |
      | k   | Monkey Village   |
      | l   | Engineer Monkey  |

- You must use keybindings to upgrade the towers
  - After selecting all the upgrades you want, click in any open space to save those upgrades in the tower's upgrade path list
  - Keys and their upgrade paths
    - Keys and their towers:
      | Key | Upgrade Path |
      | --- | -----------  |
      | ,   | Top Path     |
      | .   | Middle Path  |
      | /   | Bottom Path  |

- You must use `backspace` to sell a tower
- You must use `tab` to change the targeting of a tower
- If you press any numeric key [0-9]
  - It will assume that those are abilities and will constantly send those keypresses whenever you run the completed script.
  - So make sure to only use abilities that do not require anything other than just pressing the key
- When you have completed the map, or you want to end your run, press Ctrl+C in order for the script to recognize the completion of your recording, and to then write all the required information to a file called `map.py` in the `Recording` directory.
  - If you then want to run the script it just created, you must put it in a subfolder of the top-level directory, because of how the main python file determines the Tesseract executable location
- Modify the `config.json` in the `Recording` directory in order to change how the final script will be executed
  - Change author name
  - Change map name
  - Change the map screen
    - This is how many times you hit the right arrow + 1
    - i.e. Monkey Meadow would be *"mapScreen": 1*
      - Zero right arrow presses + 1 = 1
  - Change the map row and column [row, col]
    - This is the position of the row and column in the level select
    - i.e. Monkey Meadow would be *"mapRowCol": [1, 1]*
      - First row = 1
      - First col = 1
  - Change difficulty
    - Only accepts *Easy*, *Medium*, and *Hard*
  - Change game type
  - Change the game type row and column [row, col]
    - *The first row starts with Standard as the first column*
    - i.e. Primaries Only would be *"gameTypeRowCol": [1, 2]*
      - First row = 1
      - Second col = 2
    - i.e. Impoppable would be *"gameTypeRowCol": [2, 2]*
      - Second row = 2
      - Second col = 2
  - Change if you are going for an insta monkey (true/false)

### Running the recording script

```bash
cd path/to/BTD6Auto/Recording
python record.py
```

## Notes

There is some logic to handle a level up, but since I'm too high of a level to consistently test it out, I cannot guarantee it will work.
It may end up stopping your run/recording.
