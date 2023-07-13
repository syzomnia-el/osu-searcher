@echo off
cd /d "%~dp0/src" || exit
python main.py || pause
cd ../
@echo on
