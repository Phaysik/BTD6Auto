#!/bin/bash

main() {
    pip install --user pyautogui
    pip install --user pywinauto
    pip install --user pytesseract
    pip install --user Pillow
    pip install --user python-Levenshtein
    pip install --user fuzzywuzzy
    pip install --user keyboard
    pip install --user mouse
    pip install --user pyinstaller
}

main "$@"