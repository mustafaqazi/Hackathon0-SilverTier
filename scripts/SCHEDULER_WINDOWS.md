# AI Employee Scheduler - Windows Task Scheduler Setup

Complete guide to set up automatic AI Employee task processing on Windows using Task Scheduler.

## Overview

The AI Employee Scheduler will:
- Run every 5 minutes automatically
- Check Inbox for new tasks
- Process tasks with task-planner
- Log all operations
- Run in the background

## Prerequisites

- Windows 10/11 with Administrator access
- Python 3.10+ installed and in PATH
- AI Employee project folder with scripts
- Task Scheduler (built-in to Windows)

## Step-by-Step Setup

### Step 1: Verify Python Installation

Open Command Prompt and verify Python is accessible:

```cmd
python --version
```

**Expected Output:**
```
Python 3.10.x or higher
```

If not found, add Python to PATH or specify full path to python.exe.

### Step 2: Find Your Project Path

Note the full path to your AI Employee project:

```
C:\Users\YourUsername\Documents\AI_Employee
```

Replace `YourUsername` with your actual Windows username.

### Step 3: Create Batch Script

Create a batch file that will be executed by Task Scheduler.

**File:** `C:\Users\YourUsername\Documents\AI_Employee\scripts\run_scheduler.bat`

**Contents:**
```batch
@echo off
REM AI Employee Scheduler - Windows Batch Script
REM Run scheduler every 5 minutes

setlocal
set PYTHON_PATH=C:\Users\YourUsername\AppData\Local\Programs\Python\Python310\python.exe
set SCRIPT_PATH=C:\Users\YourUsername\Documents\AI_Employee\scripts\run_ai_employee.py
set VAULT_PATH=C:\Users\YourUsername\Documents\AI_Employee\vault

REM Change to script directory
cd /d "C:\Users\YourUsername\Documents\AI_Employee\scripts"

REM Run scheduler in single-pass mode
"%PYTHON_PATH%" "%SCRIPT_PATH%" --once --interval 300

REM Exit with success code
exit /b 0
```

**Important:** Replace:
- `YourUsername` with your actual Windows username
- Paths to match your installation
- Python path if using different version

### Step 4: Open Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc`
3. Click OK

Or search for "Task Scheduler" in Windows Start menu.

### Step 5: Create New Task

1. In Task Scheduler, click **"Create Task..."** (right side panel)

2. **General Tab:**
   - **Name:** `AI Employee Scheduler`
   - **Description:** `Automatically process AI Employee inbox tasks every 5 minutes`
   - Check: "Run with highest privileges" (for write access)
   - **Configure for:** Windows 10 or Windows 11

3. **Triggers Tab:**
   - Click **"New..."**
   - **Begin the task:** At startup
   - **Recur every:** 5 minutes
   - Click **"Repeat task every:"**
   - **For a duration of:** Indefinitely
   - Click OK

4. **Actions Tab:**
   - Click **"New..."**
   - **Action:** Start a program
   - **Program/script:**
     ```
     C:\Users\YourUsername\Documents\AI_Employee\scripts\run_scheduler.bat
     ```
   - **Start in (optional):**
     ```
     C:\Users\YourUsername\Documents\AI_Employee\scripts
     ```
   - Click OK

5. **Conditions Tab:**
   - ✓ Wake the computer to run this task
   - ✓ Run the task as soon as possible after a scheduled start is missed

6. **Settings Tab:**
   - ✓ Allow task to be run on demand
   - ✓ If the task fails, restart every: 5 minutes
   - Retry count: 3
   - ✓ Stop the task if it runs longer than: 10 minutes

7. Click **OK** to create the task

### Step 6: Test the Task

1. In Task Scheduler, find **"AI Employee Scheduler"**
2. Right-click and select **"Run"**
3. Check that it executes without errors

**Verify by checking logs:**
```cmd
type C:\Users\YourUsername\Documents\AI_Employee\scripts\logs\scheduler.log
```

### Step 7: Enable/Disable Scheduler

**To disable:**
1. Right-click "AI Employee Scheduler" in Task Scheduler
2. Click "Disable"

**To enable:**
1. Right-click "AI Employee Scheduler" in Task Scheduler
2. Click "Enable"

## Monitoring

### View Log File

Open Command Prompt and view the scheduler log:

```cmd
type C:\Users\YourUsername\Documents\AI_Employee\scripts\logs\scheduler.log
```

Or follow the log in real-time using:
```cmd
powershell Get-Content -Path "C:\Users\YourUsername\Documents\AI_Employee\scripts\logs\scheduler.log" -Wait
```

### View Registry

Check scheduler statistics:

```cmd
type C:\Users\YourUsername\Documents\AI_Employee\scripts\logs\scheduler_registry.json
```

### Check Running Tasks

View what's currently scheduled:

```cmd
tasklist | findstr python
```

## Troubleshooting

### Issue: Task won't start

**Solution:**
1. Check that Python path is correct (get it with `where python`)
2. Verify batch file path is correct
3. Check "Run with highest privileges" is enabled
4. Try running batch file manually to test

### Issue: Task runs but nothing happens

**Solution:**
1. Check logs: `scheduler.log`
2. Run manually to see errors:
   ```cmd
   python "C:\Users\YourUsername\Documents\AI_Employee\scripts\run_ai_employee.py" --once --verbose
   ```
3. Verify vault folder exists:
   ```cmd
   dir "C:\Users\YourUsername\Documents\AI_Employee\vault"
   ```

### Issue: Permission denied errors

**Solution:**
1. Right-click batch file → Properties → Security
2. Ensure current user has full control
3. In Task Scheduler task:
   - Check "Run with highest privileges"
   - Change user to your username

### Issue: Task runs too frequently

**Solution:**
- Edit task in Task Scheduler
- Adjust "Repeat task every" to desired interval (5, 10, 15, 30 minutes)

### Issue: Task doesn't run at startup

**Solution:**
- In Task Scheduler, ensure trigger is set to "At startup"
- May need to add additional trigger for first run

## Advanced Configuration

### Custom Interval

To change from 5 minutes to different interval:

Edit the batch file and change:
```batch
"%PYTHON_PATH%" "%SCRIPT_PATH%" --once --interval 300
```

Where 300 is seconds:
- 300 seconds = 5 minutes
- 600 seconds = 10 minutes
- 900 seconds = 15 minutes
- 1800 seconds = 30 minutes

### Verbose Logging

For more detailed logs, modify batch file:

```batch
"%PYTHON_PATH%" "%SCRIPT_PATH%" --once --interval 300 --verbose
```

### Manual Trigger

To also allow running manually:

1. Create another task named "AI Employee Scheduler (Manual)"
2. Remove all triggers
3. Just have the same action
4. Right-click and "Run" whenever you want

## Performance Notes

- Each run takes 1-3 seconds
- Minimal CPU usage
- Minimal memory usage
- Logs are appended (rotate manually if >100MB)

## Uninstall

To remove the scheduled task:

1. Open Task Scheduler
2. Right-click "AI Employee Scheduler"
3. Click "Delete"
4. Confirm deletion

## Verification

### Verify Task Created Successfully

```cmd
tasklist /fo list /v | findstr "AI Employee"
```

### Check Next Run Time

1. Open Task Scheduler
2. Select "AI Employee Scheduler"
3. View "Next Run Time" in Details pane

### Test with Verbose Output

```cmd
cd C:\Users\YourUsername\Documents\AI_Employee\scripts
python run_ai_employee.py --once --verbose
```

## Log Rotation

Over time, logs can grow large. Periodically rotate them:

```batch
REM Archive old log
ren C:\Users\YourUsername\Documents\AI_Employee\scripts\logs\scheduler.log scheduler_%date%.log
```

## Integration with Other Tasks

You can also create related tasks:

1. **Vault Watcher** - Monitor vault changes
2. **Approval Notifier** - Alert on pending approvals
3. **Daily Report** - Send status email daily
4. **Cleanup Task** - Archive old completed tasks

## Support

For issues:
1. Check scheduler.log for errors
2. Run with --health flag to check system status
3. Review Task Scheduler history (right-click task → View All Properties)

---

**Setup Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready
