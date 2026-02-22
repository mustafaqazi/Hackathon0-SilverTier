@echo off
REM Setup Email Credentials for Gmail-Send Skill

echo.
echo ======================================
echo Gmail Send Skill - Credential Setup
echo ======================================
echo.

echo To use the gmail-send skill, you need:
echo 1. Your Gmail address
echo 2. An App Password (NOT your regular password)
echo.

echo Step 1: Get Gmail App Password
echo ================================
echo 1. Go to: https://myaccount.google.com
echo 2. Click "Security" (left sidebar)
echo 3. Enable "2-Step Verification" if not enabled
echo 4. Go back to Security
echo 5. Find "App passwords"
echo 6. Select "Mail" and "Windows Computer"
echo 7. Copy the 16-character password
echo.

set /p EMAIL="Enter your Gmail address (e.g., your.email@gmail.com): "
set /p PASSWORD="Enter your App Password (16 characters): "

echo.
echo Setting environment variables...
setx EMAIL_ADDRESS "%EMAIL%"
setx EMAIL_PASSWORD "%PASSWORD%"

echo.
echo ======================================
echo Credentials Set Successfully!
echo ======================================
echo.
echo EMAIL_ADDRESS: %EMAIL%
echo EMAIL_PASSWORD: (hidden)
echo.
echo You can now use the gmail-send skill!
echo.
echo Example command:
echo   python .claude/skills/gmail-send/scripts/send_email.py ^
echo     --to recipient@example.com ^
echo     --subject "Test Email" ^
echo     --body "This is a test"
echo.
pause
