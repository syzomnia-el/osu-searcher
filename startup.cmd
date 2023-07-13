@echo off
set root=%cd%
cd /d "%~dp0/src" || exit
python main.py || pause
cd /d %root% || exit
@echo on
