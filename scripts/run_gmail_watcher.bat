@echo off
REM Gmail Watcher Quick Start Batch File
REM This script runs the Gmail Watcher in the current window

echo.
echo ================================================
echo     Gmail Watcher for Silver Tier AI Employee
echo ================================================
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if gmail_watcher.py exists
if not exist "gmail_watcher.py" (
    echo ERROR: gmail_watcher.py not found in this directory
    echo Current directory: %cd%
    echo.
    pause
    exit /b 1
)

REM Check if credentials file exists
if not exist "..\vault\gmail_credentials.json" (
    echo WARNING: gmail_credentials.json not found!
    echo.
    echo Expected location: ..\vault\gmail_credentials.json
    echo.
    echo To fix:
    echo 1. Download credentials.json from Google Cloud Console
    echo 2. Place it in: AI_Employee\vault\gmail_credentials.json
    echo.
    echo On first run, you'll be prompted to authorize Gmail access
    echo.
    pause
)

REM Run the Gmail Watcher
echo Starting Gmail Watcher...
echo Log file: ..\vault\gmail_watcher_log.txt
echo.
echo Press Ctrl+C to stop the watcher
echo.
echo ================================================
echo.

python gmail_watcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Gmail Watcher failed to start
    echo Check the log file for details
    pause
    exit /b 1
)

pause
