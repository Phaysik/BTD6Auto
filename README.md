# BTD6Auto

This program can automate running BTD6 maps, and can even record your own run for future playback.

## Requirements

- Download [Python3](https://www.python.org/downloads//)
  - This program was written and tested for 64bit
- This project is tested and written based on:

  - 1920x1080 resolution
  - In-game fullscreen
  - You can change this by altering the values stored in the `globals.py` config file.

    - Please note, that you will most likely have to change all of the values in some way or another if you do decide on a different resolution.
    - In order to determine what values to change to, run

      - ```bash
        python position.py
        ```

    - To determine the x, y coordinates of the mouse

- Program specfic dependencies (Run through command line)

  ```bash
  ./install.sh
  ```

  - You will also need to download the [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and install it to a folder called 'Tesseract' within this directory

## Requirements to run auto run maps

- Please note that some Monkey Knowledge is pobably required in order to successfully run map scripts that I have created
- You must have the game open
- You must be in the map itself

## Requirements when recording your own run of a map

- This version currently does not support:

  - Selling of towers
  - Tower Targeting (First, Last, ...)
  - Towers placed on the right side of the map
    - ![Good Placement](/img/GoodPlacement.png)
    - ![Good Placement](/img/BadPlacement.png)
  - Round 100 (Getting an Insta-Monkey)
  - Any hero other than Adora

- This version currently supports:
  - Placing towers
  - Upgrading towers
    - It's able to distinguish between two towers that are the same and are in close proximity which tower you want to upgrade, based on your mouse position
  - Tower upgrade order
  - Tower placement order

```bash
python record.py
```

### Rules for recording

- Please note that this script requires a lot of perfect inputs from the user

- You must use keybindings to select the tower you want to place
  - After hitting a key, you must then place the tower in an appropriate location. This program does not determine if the tower is placed properly.
- You must use keybindings to upgrade the towers
  - After selecting all the upgrades you want, click in any open space to save those upgrades in the tower's upgrade path list
- If you press any numeric key [0-9]
  - It will assume that those are abilities and will constantly send those keypresses whenever you run the completed script.
  - So make sure to only use abilities that do not require anything other than just pressing the key
- When you have completed the map, the victory screen has shown up, press Ctrl+C in order for the script to recognize the completion of the map, and to then write all the required information to a file called `map.py` in the top-level directory.
  - If you then want to run the script it just created, you must put it in a subfolder because of how the main python file determines the Tesseract executable location

## Running the Program

Open up a command line terminal

```bash
cd path/to/BTD6Auto/map
python map.py [argument]
```

### IMPORTANT

- _DO NOT CHANGE ACTIVE WINDOW OR MESS WITH THE GAME AT ALL._
- _THE PROGRAM MAY FAIL TO EXECUTE PROPERLY IF YOU DO_
- _THE PROGRAM WILL TAKE CONTROL OF YOUR MOUSE DURING CERTAIN TIMES IN EXECUTION_
- _YOU WILL HAVE THREE SECONDS AFTER THE RESTART BUTTON HAS BEEN CLICKED TO CLOSE THE PROGRAM_

## Notes

This thing is probably riddled with bugs, but it's the best I was able to come up with, and it works almost all of the time when I use it.
