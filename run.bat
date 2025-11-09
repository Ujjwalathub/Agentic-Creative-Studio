@echo off
REM Quick Start Script for Creative Media Co-Pilot
REM Windows Batch File

echo ========================================
echo Creative Media Co-Pilot - Quick Start
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    echo       Virtual environment created!
    echo.
) else (
    echo [1/3] Virtual environment exists
    echo.
)

REM Install dependencies
echo [2/3] Installing dependencies...
venv\Scripts\python.exe -m pip install --quiet --upgrade pip
venv\Scripts\python.exe -m pip install --quiet -r requirements.txt
echo       Dependencies installed!
echo.

REM Run the application
echo [3/3] Running Creative Media Co-Pilot...
echo.
echo ========================================
echo.

venv\Scripts\python.exe main.py

echo.
echo ========================================
echo Run complete!
echo ========================================
pause
