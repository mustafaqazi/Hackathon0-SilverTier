@echo off
REM LinkedIn Watcher - Quick Start Script
REM Silver Tier Implementation for Sales Lead Monitoring

REM Set script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================================
echo  LinkedIn Watcher - Silver Tier
echo ============================================================================
echo.
echo Starting LinkedIn sales message monitor...
echo.
echo Features:
echo  - Monitors LinkedIn messaging for sales keywords
echo  - Creates action files in vault/Needs_Action/
echo  - Persistent session (login once, uses saved session)
echo  - Checks every 5 minutes (300 seconds)
echo.
echo Keywords monitored:
echo  lead, opportunity, sales, meeting, proposal, connect, interested, quote
echo.
echo Vault structure:
echo  vault/linkedin_session/ ........ persistent login session
echo  vault/Needs_Action/ ............ action files created here
echo  vault/linkedin_watcher_log.txt . detailed activity log
echo.
echo ============================================================================
echo.

REM Check if Playwright is installed
python -c "import playwright" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Playwright not installed
    echo.
    echo Please install Playwright first:
    echo   pip install playwright
    echo   playwright install
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "linkedin_watcher.py" (
    echo ❌ Error: linkedin_watcher.py not found in current directory
    echo.
    echo Current directory: %cd%
    echo.
    pause
    exit /b 1
)

echo ✓ Playwright installed
echo ✓ Script found
echo.
echo ============================================================================
echo IMPORTANT:
echo - First run: You must manually login to LinkedIn in the browser window
echo - Future runs: Session is saved, automatic login happens
echo - Press Ctrl+C to stop the watcher
echo ============================================================================
echo.
pause

REM Run the LinkedIn Watcher
python linkedin_watcher.py

REM Check if it exited with error
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo ❌ Error: LinkedIn Watcher failed to start
    echo.
    echo Check the error above and review:
    echo   vault/linkedin_watcher_log.txt
    echo.
    echo Common issues:
    echo   - Playwright not installed: pip install playwright && playwright install
    echo   - LinkedIn login required: First run needs manual login
    echo   - No internet connection: Check your network
    echo ============================================================================
    pause
    exit /b 1
)

exit /b 0
