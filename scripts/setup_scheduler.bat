@echo off
REM setup_scheduler.bat - Easy scheduler setup for Windows Task Scheduler

setlocal enabledelayedexpansion

echo.
echo ======================================
echo AI Employee Scheduler Setup
echo Windows Task Scheduler Version
echo ======================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Please run Command Prompt as Administrator and try again
    pause
    exit /b 1
)

REM Get current directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10+ and add to PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Check scheduler script
echo Checking scheduler script...
if not exist "%SCRIPT_DIR%run_ai_employee.py" (
    echo ERROR: Scheduler script not found
    echo Expected: %SCRIPT_DIR%run_ai_employee.py
    pause
    exit /b 1
)
echo [OK] Scheduler script found
echo.

REM Run health check
echo Running health check...
python "%SCRIPT_DIR%run_ai_employee.py" --health
if errorlevel 1 (
    echo ERROR: Health check failed
    pause
    exit /b 1
)
echo [OK] Health check passed
echo.

REM Check if task already exists
echo Checking for existing scheduled task...
tasklist /S localhost /FO LIST /V 2>nul | find /I "AI Employee" >nul
if errorlevel 1 (
    echo Task does not exist yet
) else (
    echo WARNING: Task already exists
    set /p REPLACE="Replace existing task? (y/n): "
    if /i not "!REPLACE!"=="y" (
        echo Setup cancelled
        pause
        exit /b 0
    )
    echo Deleting existing task...
    schtasks /delete /tn "AI Employee Scheduler" /f >nul 2>&1
)
echo.

REM Create the batch file
echo Creating batch runner file...
set BATCH_FILE=%SCRIPT_DIR%run_scheduler.bat

(
    echo @echo off
    echo REM AI Employee Scheduler - Windows Task Scheduler Runner
    echo setlocal
    echo cd /d "%SCRIPT_DIR%"
    echo python run_ai_employee.py --once --interval 300
    echo exit /b %%ERRORLEVEL%%
) > "%BATCH_FILE%"

echo [OK] Batch file created: %BATCH_FILE%
echo.

REM Create scheduled task
echo Creating scheduled task...
schtasks /create ^
    /tn "AI Employee Scheduler" ^
    /tr "%BATCH_FILE%" ^
    /sc minute ^
    /mo 5 ^
    /ru "%USERNAME%" ^
    /rp /f >nul 2>&1

if errorlevel 1 (
    echo ERROR: Failed to create scheduled task
    pause
    exit /b 1
)
echo [OK] Scheduled task created
echo.

REM Verify task was created
echo Verifying scheduled task...
schtasks /query /tn "AI Employee Scheduler" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to verify task
    pause
    exit /b 1
)
echo [OK] Task verified
echo.

REM Show task details
echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Task Details:
schtasks /query /tn "AI Employee Scheduler" /fo LIST /v
echo.

echo Options:
echo 1 - View logs
echo 2 - Run test
echo 3 - Show task details
echo 4 - Delete task
echo 5 - Exit
echo.

set /p CHOICE="Enter choice (1-5): "

if "%CHOICE%"=="1" (
    if exist "%SCRIPT_DIR%logs\scheduler.log" (
        echo.
        echo === Recent Log Entries ===
        powershell -NoProfile -Command "Get-Content '%SCRIPT_DIR%logs\scheduler.log' -Tail 20"
    ) else (
        echo No log file yet (will be created on first run^)
    )
    pause
)

if "%CHOICE%"=="2" (
    echo.
    echo === Running Test ===
    python "%SCRIPT_DIR%run_ai_employee.py" --once --verbose
    pause
)

if "%CHOICE%"=="3" (
    echo.
    echo === Task Details ===
    schtasks /query /tn "AI Employee Scheduler" /fo LIST /v
    pause
)

if "%CHOICE%"=="4" (
    set /p CONFIRM="Delete scheduled task? (y/n): "
    if /i "!CONFIRM!"=="y" (
        schtasks /delete /tn "AI Employee Scheduler" /f >nul 2>&1
        echo [OK] Task deleted
    ) else (
        echo Cancelled
    )
    pause
)

echo.
exit /b 0
