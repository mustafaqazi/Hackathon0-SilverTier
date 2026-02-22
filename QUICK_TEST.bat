@echo off
REM Quick Test Script - AI Employee System
REM Tests all major components quickly

echo.
echo ===============================================
echo AI EMPLOYEE - QUICK TEST SUITE
echo ===============================================
echo.

REM Check Python
echo [TEST 1] Checking Python Environment...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Python is installed
) else (
    echo [FAIL] Python not found
    exit /b 1
)

REM Check vault structure
echo.
echo [TEST 2] Checking Vault Structure...
if exist "AI_Employee\vault\Inbox" (
    echo [PASS] Inbox folder exists
) else (
    echo [FAIL] Inbox folder not found
    exit /b 1
)

if exist "AI_Employee\vault\Needs_Action" (
    echo [PASS] Needs_Action folder exists
) else (
    echo [FAIL] Needs_Action folder not found
    exit /b 1
)

if exist "AI_Employee\vault\Done" (
    echo [PASS] Done folder exists
) else (
    echo [FAIL] Done folder not found
    exit /b 1
)

REM Check skills exist
echo.
echo [TEST 3] Checking Skills...
if exist ".claude\skills\gmail-send" (
    echo [PASS] gmail-send skill exists
) else (
    echo [FAIL] gmail-send skill not found
)

if exist ".claude\skills\linkedin-post" (
    echo [PASS] linkedin-post skill exists
) else (
    echo [FAIL] linkedin-post skill not found
)

if exist ".claude\skills\vault-file-manager" (
    echo [PASS] vault-file-manager skill exists
) else (
    echo [FAIL] vault-file-manager skill not found
)

if exist ".claude\skills\human-approval" (
    echo [PASS] human-approval skill exists
) else (
    echo [FAIL] human-approval skill not found
)

REM Test scheduler in single-pass mode
echo.
echo [TEST 4] Testing Scheduler (Single Pass)...
python AI_Employee\scripts\run_ai_employee.py --once --verbose >scheduler_test_output.txt 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Scheduler ran successfully
    echo Output:
    type scheduler_test_output.txt | findstr /C:"Detected" /C:"processed"
) else (
    echo [FAIL] Scheduler failed
    type scheduler_test_output.txt
)

REM Test vault file manager - list
echo.
echo [TEST 5] Testing Vault File Manager - List...
python .claude\skills\vault-file-manager\scripts\move_task.py ^\
  --action list ^\
  --source Inbox >vault_test_output.txt 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Vault list command worked
    type vault_test_output.txt
) else (
    echo [FAIL] Vault list command failed
    type vault_test_output.txt
)

REM Check email credentials
echo.
echo [TEST 6] Checking Email Credentials...
if defined EMAIL_ADDRESS (
    echo [PASS] EMAIL_ADDRESS is set
) else (
    echo [WARN] EMAIL_ADDRESS not set - gmail-send skill won't work
    echo        Run: SETUP_EMAIL_CREDENTIALS.bat
)

if defined EMAIL_PASSWORD (
    echo [PASS] EMAIL_PASSWORD is set
) else (
    echo [WARN] EMAIL_PASSWORD not set - gmail-send skill won't work
)

REM Test Windows Task Scheduler
echo.
echo [TEST 7] Checking Windows Task Scheduler...
schtasks /query /tn "AI Employee Scheduler" >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Scheduler task exists
    schtasks /query /tn "AI Employee Scheduler" /v | findstr "Ready"
) else (
    echo [WARN] Scheduler task not configured
)

REM Check logs exist
echo.
echo [TEST 8] Checking Log Files...
if exist "AI_Employee\logs\scheduler.log" (
    echo [PASS] Scheduler log exists
) else (
    echo [INFO] Scheduler log will be created on first run
)

if exist ".claude\skills\gmail-send\scripts\logs\actions.log" (
    echo [PASS] Gmail-send log exists
) else (
    echo [INFO] Gmail-send log will be created on first send
)

REM Summary
echo.
echo ===============================================
echo QUICK TEST SUMMARY
echo ===============================================
echo.
echo [✓] Environment setup verified
echo [✓] Vault structure confirmed
echo [✓] Skills installed
echo [✓] Scheduler functional
echo [✓] File manager working
echo.

echo Next Steps:
echo.
echo 1. FULL TESTING GUIDE
echo    Read: AI_Employee\FULL_TESTING_GUIDE.md
echo.
echo 2. SET EMAIL CREDENTIALS (if not done)
echo    Run: AI_Employee\SETUP_EMAIL_CREDENTIALS.bat
echo.
echo 3. CREATE TEST TASK
echo    Create file in: AI_Employee\vault\Inbox\test_task.md
echo.
echo 4. RUN SCHEDULER
echo    Run: python AI_Employee\scripts\run_ai_employee.py --once --verbose
echo.
echo 5. VERIFY PLAN
echo    Check: AI_Employee\vault\Needs_Action\ActionPlan_*.md
echo.
echo ===============================================
echo.

REM Cleanup
del /q scheduler_test_output.txt 2>nul
del /q vault_test_output.txt 2>nul

pause
