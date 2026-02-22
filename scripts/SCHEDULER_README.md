# AI Employee Scheduler - Complete Setup Guide

Production-ready scheduler for the AI Employee system. Automatically processes tasks every 5 minutes.

## Quick Start (2 minutes)

### Windows
```cmd
cd AI_Employee\scripts
setup_scheduler.bat
```

### Linux/Mac
```bash
cd AI_Employee/scripts
bash setup_scheduler.sh
```

## Overview

The AI Employee Scheduler:
- ✅ Monitors Inbox for new tasks
- ✅ Runs task-planner automatically
- ✅ Processes tasks every 5 minutes
- ✅ Maintains comprehensive logs
- ✅ Handles errors gracefully
- ✅ Cross-platform (Windows/Linux/Mac)

## What Gets Scheduled

When you enable the scheduler, it will:

1. **Every 5 minutes:**
   - Check if tasks exist in `vault/Inbox/`
   - Run `task_planner.py` to analyze tasks
   - Generate execution plans
   - Move plans to `vault/Needs_Action/`

2. **Log all activity:**
   - `logs/scheduler.log` - Detailed operations
   - `logs/scheduler_registry.json` - Statistics
   - `logs/cron.log` - Cron output (Linux/Mac)

3. **Handle errors:**
   - Retry logic (up to 3 retries)
   - Clear error messages
   - No data loss

## Installation

### Prerequisites

- Python 3.10+
- Windows 10/11 (for Windows) OR Linux/Mac
- Administrator/sudo access (for setup)

### Step 1: Verify Setup

```bash
# Check Python
python3 --version  # Should be 3.10+

# Check scheduler script exists
ls AI_Employee/scripts/run_ai_employee.py
```

### Step 2: Run Setup Script

**Windows (Command Prompt as Administrator):**
```cmd
cd AI_Employee\scripts
setup_scheduler.bat
```

**Linux/Mac (Terminal):**
```bash
cd AI_Employee/scripts
bash setup_scheduler.sh
chmod +x setup_scheduler.sh
```

### Step 3: Verify Installation

The setup script will:
- ✅ Check Python installation
- ✅ Verify scheduler script
- ✅ Run health check
- ✅ Create scheduled task (Windows) or cron job (Linux/Mac)
- ✅ Test the configuration

## Manual Setup

### Windows - Manual Task Scheduler Setup

See `SCHEDULER_WINDOWS.md` for detailed step-by-step instructions.

**Quick version:**
1. Open Task Scheduler (Win+R → taskschd.msc)
2. Create New Task → "AI Employee Scheduler"
3. Set trigger: Repeat every 5 minutes
4. Set action: Run `scripts/run_scheduler.bat`

### Linux/Mac - Manual Cron Setup

See `SCHEDULER_LINUX_MAC.md` for detailed instructions.

**Quick version:**
```bash
crontab -e
# Add: */5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

## Usage

### View Status

```bash
# Check if scheduler is running
# Windows: Task Scheduler → Find "AI Employee Scheduler"
# Linux/Mac: crontab -l

# View logs
tail -f AI_Employee/scripts/logs/scheduler.log
```

### Run Manually

```bash
python AI_Employee/scripts/run_ai_employee.py --once
```

### Test Setup

```bash
python AI_Employee/scripts/run_ai_employee.py --health
```

### Enable/Disable

**Windows:**
1. Open Task Scheduler
2. Right-click "AI Employee Scheduler"
3. Click "Enable" or "Disable"

**Linux/Mac:**
```bash
crontab -e
# Comment/uncomment the line
```

## Command Line Options

```bash
python run_ai_employee.py [OPTIONS]

Options:
  --daemon           Run as daemon (background)
  --once             Run once and exit
  --interval SECS    Check interval (default: 300)
  --health           Run health check
  --verbose          Enable verbose logging
  --help             Show help message
```

## Examples

**Run every 5 minutes continuously:**
```bash
python run_ai_employee.py --daemon
```

**Run once:**
```bash
python run_ai_employee.py --once
```

**Run every 10 minutes:**
```bash
python run_ai_employee.py --daemon --interval 600
```

**Health check:**
```bash
python run_ai_employee.py --health
```

**Verbose debug output:**
```bash
python run_ai_employee.py --once --verbose
```

## Monitoring

### View Live Logs

**Linux/Mac:**
```bash
tail -f AI_Employee/scripts/logs/scheduler.log
```

**Windows:**
```cmd
powershell Get-Content "AI_Employee\scripts\logs\scheduler.log" -Wait
```

### View Statistics

```bash
cat AI_Employee/scripts/logs/scheduler_registry.json
```

### Check Last Run

```bash
ls -la AI_Employee/scripts/logs/scheduler.log
stat AI_Employee/scripts/logs/scheduler.log
```

### Monitor in Real-Time

**Linux/Mac:**
```bash
watch -n 1 tail -10 AI_Employee/scripts/logs/scheduler.log
```

**Windows:**
```cmd
powershell "while($true) { Clear-Host; Get-Content 'AI_Employee\scripts\logs\scheduler.log' -Tail 10; Start-Sleep 1 }"
```

## Troubleshooting

### Scheduler not running

**Windows:**
1. Open Task Scheduler
2. Look for "AI Employee Scheduler"
3. Check "Last Run Time"
4. Check "Last Run Result" (0 = success)

**Linux/Mac:**
```bash
crontab -l | grep run_ai_employee
# Should show the cron job
```

### Check logs

```bash
# View full log
cat AI_Employee/scripts/logs/scheduler.log

# View errors only
grep ERROR AI_Employee/scripts/logs/scheduler.log

# Last 20 lines
tail -20 AI_Employee/scripts/logs/scheduler.log
```

### Test manually

```bash
# Run with verbose output
python AI_Employee/scripts/run_ai_employee.py --once --verbose

# Check if tasks are detected
ls AI_Employee/vault/Inbox/*.md

# Verify output folders exist
ls -la AI_Employee/vault/Needs_Action/
```

### Run health check

```bash
python AI_Employee/scripts/run_ai_employee.py --health
```

## Log Files

Located in `AI_Employee/scripts/logs/`:

- **scheduler.log** - Main scheduler operations
- **scheduler_registry.json** - Statistics and history
- **cron.log** - Cron output (Linux/Mac only)
- **planning.log** - Task planner output
- **vault.log** - Vault file manager operations

## File Structure

```
AI_Employee/
├── scripts/
│   ├── run_ai_employee.py .............. Scheduler script
│   ├── task_planner.py ................ Task planning script
│   ├── setup_scheduler.bat ............ Windows setup (run as admin)
│   ├── setup_scheduler.sh ............. Linux/Mac setup
│   ├── run_scheduler.bat .............. Windows batch runner
│   ├── SCHEDULER_README.md ............ This file
│   ├── SCHEDULER_WINDOWS.md ........... Windows detailed guide
│   ├── SCHEDULER_LINUX_MAC.md ......... Linux/Mac detailed guide
│   └── logs/
│       ├── scheduler.log .............. Main log
│       └── scheduler_registry.json .... Statistics
│
└── vault/
    ├── Inbox/ ......................... New tasks (monitored)
    ├── Needs_Action/ .................. Tasks requiring review
    ├── Needs_Approval/ ................ Tasks awaiting approval
    └── Done/ .......................... Completed tasks
```

## Performance

- **CPU Usage:** Minimal (<1%)
- **Memory Usage:** ~30MB
- **Disk I/O:** Minimal
- **Network:** None (local only)
- **Execution Time:** 1-3 seconds per check
- **Log Growth:** ~1KB per run (rotate if >100MB)

## Changing Schedule

### Change Interval (Default: 5 minutes)

**Windows:**
1. Task Scheduler → AI Employee Scheduler → Triggers
2. Edit trigger → Change "Every 5 minutes" to desired interval

**Linux/Mac:**
```bash
crontab -e
# Change */5 to desired interval
# */5 = every 5 min, */10 = every 10 min, */15 = every 15 min
```

## Disabling Temporarily

**Windows:**
1. Task Scheduler → Right-click "AI Employee Scheduler" → Disable

**Linux/Mac:**
```bash
crontab -e
# Add # to the beginning of the line to comment it out
```

## Removing Scheduler

**Windows:**
1. Task Scheduler → Right-click "AI Employee Scheduler" → Delete

**Linux/Mac:**
```bash
crontab -e
# Delete the entire line
# Or: crontab -r (to remove all cron jobs)
```

## Advanced Configuration

### Multiple Schedulers

Run different schedulers with different intervals:

**Windows:** Create multiple Task Scheduler tasks
**Linux/Mac:** Add multiple cron jobs with different intervals

```bash
# Fast processing (every 5 min)
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/fast.log 2>&1

# Deep processing (every 30 min)
*/30 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/deep.log 2>&1
```

### Email Notifications

**Linux/Mac:**
```bash
crontab -e
# Add: */5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once 2>&1 || mail -s "Error" user@example.com
```

### Log Rotation

**Monthly archive (Linux/Mac):**
```bash
crontab -e
# Add: 0 0 1 * * cd ~/AI_Employee/scripts && mv logs/scheduler.log logs/scheduler_$(date +\%Y\%m\%d).log
```

## Support & Help

**For Windows issues:**
- See `SCHEDULER_WINDOWS.md` for detailed troubleshooting
- Check Task Scheduler History
- Run setup script again with admin privileges

**For Linux/Mac issues:**
- See `SCHEDULER_LINUX_MAC.md` for detailed troubleshooting
- Check cron logs: `journalctl -u cron`
- Run setup script: `bash setup_scheduler.sh`

**General help:**
```bash
# Show all options
python run_ai_employee.py --help

# Run health check
python run_ai_employee.py --health

# View logs
tail -f AI_Employee/scripts/logs/scheduler.log
```

## Statistics

Check how many tasks have been processed:

```bash
python -c "
import json
with open('AI_Employee/scripts/logs/scheduler_registry.json') as f:
    data = json.load(f)
    stats = data.get('stats', {})
    print(f\"Total Runs: {stats.get('total_runs', 0)}\")
    print(f\"Tasks Processed: {stats.get('total_tasks_processed', 0)}\")
    print(f\"Total Errors: {stats.get('total_errors', 0)}\")
"
```

## Next Steps

1. ✅ Run setup script
2. ✅ Verify scheduler is running
3. ✅ Add test tasks to Inbox
4. ✅ Watch logs as tasks are processed
5. ✅ Customize interval if needed

## Questions?

- Windows setup issues → See `SCHEDULER_WINDOWS.md`
- Linux/Mac setup issues → See `SCHEDULER_LINUX_MAC.md`
- Command-line options → Run `python run_ai_employee.py --help`
- General troubleshooting → Run health check: `python run_ai_employee.py --health`

---

**Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready
