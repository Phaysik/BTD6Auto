#!/bin/bash

main() {
    pyinstaller --onefile gui.py
}

main "$@"