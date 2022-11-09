@echo off
cd /d "%cd%/src" || exit
python main.py
cd ../
@echo on
