@echo off
REM Hisab Desktop Application Launcher for Windows

echo Starting Hisab Desktop Application...

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python 3 from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: tkinter is not available!
    echo tkinter should be included with Python on Windows
    echo Please reinstall Python from https://python.org
    pause
    exit /b 1
)

REM Run the application
python hisab_app.py
pause