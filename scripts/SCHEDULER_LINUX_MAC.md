# AI Employee Scheduler - Linux/Mac Cron Setup

Complete guide to set up automatic AI Employee task processing on Linux/Mac using cron.

## Overview

The AI Employee Scheduler will:
- Run every 5 minutes automatically via cron
- Check Inbox for new tasks
- Process tasks with task-planner
- Log all operations
- Run silently in the background

## Prerequisites

- Linux (Ubuntu, CentOS, etc.) or macOS
- Python 3.10+ installed
- cron service running (usually default)
- AI Employee project folder with scripts

## Step-by-Step Setup

### Step 1: Verify Python Installation

```bash
python3 --version
```

**Expected Output:**
```
Python 3.10.x or higher
```

If not found:
- **Ubuntu/Debian:** `sudo apt install python3.10`
- **CentOS/RHEL:** `sudo yum install python3.10`
- **macOS:** `brew install python@3.10`

### Step 2: Find Project Path

Determine your AI Employee project path:

```bash
pwd
# Should output something like: /home/username/AI_Employee
# Or: /Users/username/AI_Employee
```

Note this path - you'll need it in the cron job.

### Step 3: Make Script Executable

```bash
chmod +x ~/AI_Employee/scripts/run_ai_employee.py
```

Test it runs:

```bash
python3 ~/AI_Employee/scripts/run_ai_employee.py --health
```

### Step 4: Create Cron Job

Open crontab editor:

```bash
crontab -e
```

This opens your default text editor (usually nano or vim).

### Step 5: Add Cron Schedule

Add this line to the crontab file:

```cron
*/5 * * * * cd /home/username/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Replace:**
- `/home/username/AI_Employee` with your actual project path
- Use `~/` if more convenient (cron expands it)

**What this means:**
- `*/5` - Every 5 minutes
- `*` - Every hour
- `*` - Every day
- `*` - Every month
- `*` - Every day of week
- `cd /path && python3 ... >> logs/cron.log 2>&1` - Run scheduler and log output

### Step 6: Verify Cron Job Added

```bash
crontab -l
```

Should show your new job.

### Step 7: Test the Setup

Wait 5 minutes or manually run:

```bash
cd ~/AI_Employee/scripts
python3 run_ai_employee.py --once --verbose
```

Check if tasks were processed by viewing logs:

```bash
tail -f ~/AI_Employee/scripts/logs/scheduler.log
```

## Monitoring

### View Log File

```bash
tail -f ~/AI_Employee/scripts/logs/scheduler.log
```

Follow in real-time:

```bash
watch -n 1 tail -20 ~/AI_Employee/scripts/logs/scheduler.log
```

### View Cron Job Output

```bash
tail -f ~/AI_Employee/scripts/logs/cron.log
```

### Check Last Run Time

```bash
ls -la ~/AI_Employee/scripts/logs/scheduler.log
stat ~/AI_Employee/scripts/logs/scheduler.log
```

### View Scheduler Statistics

```bash
cat ~/AI_Employee/scripts/logs/scheduler_registry.json | python3 -m json.tool
```

### List All Cron Jobs

```bash
crontab -l
```

## Cron Schedule Examples

**Run every 5 minutes (default):**
```cron
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run every 10 minutes:**
```cron
*/10 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run every 15 minutes:**
```cron
*/15 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run every hour:**
```cron
0 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run every day at 9 AM:**
```cron
0 9 * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run every Monday at 8 AM:**
```cron
0 8 * * 1 cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

**Run twice per hour (every 30 minutes):**
```cron
0,30 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

## Troubleshooting

### Issue: Cron job not running

**Check if cron is running:**
```bash
sudo systemctl status cron
# or on macOS:
sudo launchctl list | grep cron
```

**Start cron if stopped:**
```bash
# Linux
sudo systemctl start cron

# macOS
sudo launchctl start com.vix.cron
```

### Issue: Cron job runs but doesn't work

**Check cron logs:**
```bash
# Linux
sudo tail -f /var/log/syslog | grep CRON

# macOS
log stream --predicate 'eventMessage contains[cd] "cron"' --level debug

# Check cron output
tail -f ~/AI_Employee/scripts/logs/cron.log
```

**Test command manually:**
```bash
cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once --verbose
```

### Issue: Permission denied

**Make script executable:**
```bash
chmod +x ~/AI_Employee/scripts/run_ai_employee.py
```

**Check permissions:**
```bash
ls -la ~/AI_Employee/scripts/run_ai_employee.py
```

Should show: `-rwxr-xr-x` or similar with 'x' flags.

### Issue: Python not found

**Use full Python path:**
```bash
which python3
# Returns something like: /usr/bin/python3
```

Update cron with full path:
```cron
*/5 * * * * cd ~/AI_Employee/scripts && /usr/bin/python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

### Issue: Logs grow too large

**Rotate logs monthly:**
```bash
0 0 1 * * cd ~/AI_Employee/scripts && mv logs/scheduler.log logs/scheduler_$(date +\%Y\%m\%d).log
```

Add this to your crontab to archive logs monthly.

## Advanced Configuration

### Email Notifications on Error

Send email when scheduler encounters errors:

```cron
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1 || echo "AI Employee Scheduler failed" | mail -s "Error" your@email.com
```

### Verbose Logging

For detailed debugging:

```cron
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once --verbose >> logs/cron_verbose.log 2>&1
```

### Custom Interval

Change the interval by modifying the `*/5`:

```cron
# Every 3 minutes
*/3 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1

# Every 20 minutes
*/20 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

### Health Check on Startup

Run health check when system boots:

```cron
@reboot sleep 30 && cd ~/AI_Employee/scripts && python3 run_ai_employee.py --health >> logs/startup_check.log 2>&1
```

### Parallel Scheduling

Run multiple schedulers with different configurations:

```cron
# Fast processing every 5 minutes
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once --interval 300 >> logs/cron_fast.log 2>&1

# Deep processing every 30 minutes
*/30 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once --interval 1800 >> logs/cron_deep.log 2>&1
```

## Environment Variables

If your scheduler needs environment variables, add them before the command:

```cron
*/5 * * * * export PATH=/usr/local/bin:/usr/bin:$PATH && cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

Or set them in crontab:

```cron
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash

*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

## Disabling and Enabling

### Disable temporarily

Comment out the cron line (add `#` at start):

```bash
crontab -e
# Add # to beginning of line:
# */5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

### Enable again

Remove the `#`:

```bash
crontab -e
# Remove # from beginning:
*/5 * * * * cd ~/AI_Employee/scripts && python3 run_ai_employee.py --once >> logs/cron.log 2>&1
```

### Remove cron job completely

```bash
crontab -r
```

Or edit and delete the line:

```bash
crontab -e
# Delete the entire AI Employee Scheduler line
```

## Monitoring Tools

### Check cron history (Ubuntu/Debian)

```bash
sudo journalctl -u cron --since "1 hour ago"
```

### Monitor in real-time

```bash
watch -n 1 'grep CRON /var/log/syslog | tail -10'
```

### Create dashboard script

Save as `~/check_scheduler.sh`:

```bash
#!/bin/bash
echo "=== Cron Job ==="
crontab -l | grep "run_ai_employee"

echo ""
echo "=== Last 5 Runs ==="
tail -5 ~/AI_Employee/scripts/logs/scheduler.log

echo ""
echo "=== Statistics ==="
cat ~/AI_Employee/scripts/logs/scheduler_registry.json | python3 -m json.tool | head -20

echo ""
echo "=== Cron Output ==="
tail -5 ~/AI_Employee/scripts/logs/cron.log
```

Then run: `bash ~/check_scheduler.sh`

## Performance Notes

- Each run takes 1-3 seconds
- Minimal CPU usage
- Minimal memory usage
- Safe to run frequently (even every 1 minute)
- Logs append over time (rotate if needed)

## Uninstall

Remove the scheduler:

```bash
crontab -e
# Delete the AI Employee Scheduler line
# Save and exit
```

Verify it's removed:

```bash
crontab -l
# Should not show the scheduler line
```

## Support

For issues:

1. Check logs: `tail -f ~/AI_Employee/scripts/logs/scheduler.log`
2. Run with verbose: `python3 run_ai_employee.py --once --verbose`
3. Check cron: `crontab -l`
4. Check if cron is running: `sudo systemctl status cron`

---

**Setup Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready
