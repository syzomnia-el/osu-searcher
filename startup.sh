#!/bin/sh
stty -echo
cd "$(dirname "$0")/src" || exit
py main.py || exit
cd ../
stty echo