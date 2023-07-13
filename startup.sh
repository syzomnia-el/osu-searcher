#!/bin/bash
root=$(pwd)
cd "$(dirname "$0")/src" || exit
python3 main.py
cd "$root" > /dev/null || exit
