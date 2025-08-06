@echo off
REM JSearch Windows Launcher
REM This batch file makes it easier to run jsearch on Windows

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ and add it to your PATH
    pause
    exit /b 1
)

REM Run jsearch with all passed arguments
python "%SCRIPT_DIR%jsearch.py" %*

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo JSearch encountered an error. Press any key to exit...
    pause >nul
)
