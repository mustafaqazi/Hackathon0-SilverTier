# LinkedIn Watcher - Setup Guide

## Quick Start (2 minutes)

### Step 1: Install Playwright
```bash
pip install playwright
playwright install
```

### Step 2: Run the Watcher
**Windows:**
```bash
run_linkedin_watcher.bat
```

**Mac/Linux:**
```bash
python scripts/linkedin_watcher.py
```

### Step 3: First-Time Login
- A browser window will appear
- Login to LinkedIn manually with your credentials
- The script will detect successful login and save your session
- Click the terminal to continue

**That's it!** The watcher is now running and will:
- ✅ Check for unread messages every 5 minutes
- ✅ Detect sales keywords automatically
- ✅ Create action files in `vault/Needs_Action/`
- ✅ Log all activity to `vault/linkedin_watcher_log.txt`

---

## Detailed Setup

### System Requirements
- **Python:** 3.8 or higher
- **OS:** Windows, Mac, or Linux
- **Browser:** Chromium (auto-installed by Playwright)
- **Internet:** Required for LinkedIn access
- **Disk:** ~500MB for Chromium + session

### Prerequisites Check
```bash
# Check Python version
python --version  # Must be 3.8+

# Check if pip is available
pip --version

# Check if git (optional but helpful)
git --version
```

---

## Installation Steps

### 1. Navigate to AI_Employee Directory
```bash
cd path/to/AI_Employee
```

### 2. Install Dependencies
```bash
pip install playwright
```

### 3. Install Playwright Browsers
```bash
playwright install chromium
```

This downloads Chromium (~300MB) - only needs to run once.

### 4. Verify Installation
```bash
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright installed')"
```

Expected output: `✓ Playwright installed`

---

## First Run

### Starting the Watcher

**Option A: Using Batch File (Windows)**
```bash
scripts\run_linkedin_watcher.bat
```

**Option B: Using Python (All Platforms)**
```bash
python scripts/linkedin_watcher.py
```

### What Happens

```
2026-02-19 15:30:45 - LinkedInWatcher - INFO - =======================================================================
2026-02-19 15:30:45 - LinkedInWatcher - INFO - LinkedIn Watcher initialized
2026-02-19 15:30:45 - LinkedInWatcher - INFO - Vault root: C:\Users\[user]\AI_Employee\vault
2026-02-19 15:30:45 - LinkedInWatcher - INFO - Session folder: C:\Users\[user]\AI_Employee\vault\linkedin_session
2026-02-19 15:30:46 - LinkedInWatcher - INFO - Loaded 0 previously processed messages
2026-02-19 15:30:47 - LinkedInWatcher - INFO - ✓ Playwright started
2026-02-19 15:30:48 - LinkedInWatcher - INFO - ✓ Chromium browser launched with persistent profile
2026-02-19 15:30:50 - LinkedInWatcher - INFO - ✓ Browser page initialized
2026-02-19 15:30:51 - LinkedInWatcher - INFO - Navigating to LinkedIn messaging...
2026-02-19 15:30:55 - LinkedInWatcher - INFO - ❌ LinkedIn login required!
2026-02-19 15:30:55 - LinkedInWatcher - INFO - 👉 Please login to LinkedIn in the browser window that appeared
2026-02-19 15:30:55 - LinkedInWatcher - INFO - ℹ️  Session will be saved for automatic login on next run
```

At this point:
1. **A browser window opens**
2. **Login to LinkedIn manually** (username/password)
3. **Wait for confirmation** in terminal
4. Script continues automatically once logged in

---

## Configuration Files

### Vault Structure (Auto-Created)

```
vault/
├── linkedin_session/
│   ├── chrome_user_data/
│   │   ├── Default/
│   │   ├── Local Storage/
│   │   ├── Cookies/
│   │   └── ... (browser profile)
│   └── .gitignore  (prevents committing session)
├── Needs_Action/
│   ├── LINKEDIN_John_Smith_20260219_153045.md
│   └── LINKEDIN_Sarah_Jones_20260219_154230.md
├── linkedin_watcher_log.txt
└── .linkedin_processed_messages.json
```

### Configuration

All settings are in `linkedin_watcher.py`:

#### 1. Check Interval (Default: 300 seconds / 5 minutes)
**Line 546:**
```python
time.sleep(300)  # Change to 60 for 1 minute, 600 for 10 minutes
```

#### 2. Sales Keywords (Default: 15 keywords)
**Lines 79-81:**
```python
KEYWORDS = [
    'lead', 'opportunity', 'sales', 'meeting', 'proposal',
    'connect', 'interested', 'quote', 'partnership', 'collaboration',
    'business', 'deal', 'contract', 'enquiry', 'request'
]
```

Add or remove keywords as needed.

#### 3. Priority Level (Default: medium)
**Line 465:**
```python
priority: medium  # Change to 'high' or 'low'
```

#### 4. Browser Mode (Default: Headless)
**Line 197:**
```python
headless=True,  # Set to False to see the browser window
```

---

## Running the Watcher

### Normal Start
```bash
python scripts/linkedin_watcher.py
```

### With Visible Browser (Debugging)
Edit line 197 in `linkedin_watcher.py`:
```python
headless=False,  # Show browser window while running
```

### Running in Background

**Windows (Command Prompt):**
```bash
start /B python scripts/linkedin_watcher.py
```

**Windows (PowerShell):**
```powershell
Start-Process python -ArgumentList "scripts/linkedin_watcher.py" -WindowStyle Hidden
```

**Mac/Linux:**
```bash
nohup python scripts/linkedin_watcher.py > vault/linkedin_watcher_output.log 2>&1 &
```

### Stopping the Watcher
```
Press Ctrl+C in the terminal
```

The script will:
1. Finish current check
2. Close browser gracefully
3. Save session
4. Exit cleanly

---

## Testing

### Manual Test - Check if Setup Works

```bash
# Test 1: Import check
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright OK')"

# Test 2: Run watcher (will require manual LinkedIn login)
python scripts/linkedin_watcher.py
```

### What to Look For

✅ **Success indicators:**
- Browser window opens
- LinkedIn loads
- You can see messaging page
- Script shows "✓ LinkedIn ready for monitoring"
- New checks happen every 5 minutes

❌ **Error indicators:**
- Browser doesn't open
- "Timeout" errors
- "Login required" after 2nd run
- Permission errors on file creation

---

## Troubleshooting

### Issue 1: "Playwright not installed"
```bash
# Solution:
pip install playwright
playwright install chromium
```

### Issue 2: "Browser didn't open"
Possible causes:
- Chromium not installed: `playwright install chromium`
- Insufficient system resources: Close other apps
- Display server issues (Linux): May need `DISPLAY=:0` set

### Issue 3: "Timeout loading LinkedIn"
- Check internet connection
- LinkedIn may be blocking automated access
- Try again - sometimes temporary

### Issue 4: "Login required" on 2nd run
Session may have expired:
```bash
# Delete session and start fresh:
rm -r vault/linkedin_session/

# Run again (will need manual login):
python scripts/linkedin_watcher.py
```

### Issue 5: "No messages found"
This is normal! Means:
- No new unread messages
- All messages already processed
- Script will keep checking every 5 minutes

### Issue 6: "Permission denied on vault/"
```bash
# Fix permissions (Windows):
icacls vault /grant:r "%USERNAME%":F /t

# Fix permissions (Mac/Linux):
chmod -R 755 vault/
```

---

## Monitoring the Watcher

### Check Logs
```bash
# View recent log entries
tail -f vault/linkedin_watcher_log.txt

# Windows (PowerShell):
Get-Content vault/linkedin_watcher_log.txt -Tail 20 -Wait
```

### Check Processed Messages
```bash
# View tracked message IDs
cat vault/.linkedin_processed_messages.json | python -m json.tool
```

### Check Action Files Created
```bash
# Count action files
ls vault/Needs_Action/LINKEDIN_*.md | wc -l

# View newest action file
ls -lt vault/Needs_Action/LINKEDIN_*.md | head -1
```

---

## Performance Tips

### 1. Optimize Check Interval
- Too frequent (60s): Higher CPU/bandwidth usage
- Too infrequent (600s): May miss urgent messages
- **Recommended:** 300 seconds (5 minutes)

### 2. Run as Service (Optional)

**Windows Scheduler:**
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "scripts/linkedin_watcher.py"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LinkedInWatcher"
```

**Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add this line to run at startup:
@reboot cd /path/to/AI_Employee && python scripts/linkedin_watcher.py > vault/linkedin_watcher.log 2>&1 &
```

### 3. System Resources
- **RAM:** ~150MB when running
- **CPU:** ~5% average (spikes to 15% during checks)
- **Disk:** ~2-5KB per action file

---

## Integration with Other Tools

### Combined with Gmail Watcher
```bash
# Terminal 1
python scripts/gmail_watcher.py

# Terminal 2
python scripts/linkedin_watcher.py

# Terminal 3
python scripts/whatsapp_watcher.py
```

All three feed into `vault/Needs_Action/` for unified task management.

### Integrate with Task Runner
The action files created can be:
- ✅ Manually reviewed and acted upon
- ✅ Fed into task planning system
- ✅ Integrated with CRM tools
- ✅ Used to trigger automations

---

## FAQ

**Q: Do I need to login every time?**
A: No! Session is saved after first login. Only needs manual login if:
- Session expires (rare)
- You delete the session folder
- LinkedIn logs you out (very rare)

**Q: Can I run multiple instances?**
A: Not recommended. Only one instance should monitor the same account.

**Q: Will it work on headless servers?**
A: Yes! Set `headless=True` (default). Requires `xvfb` on Linux servers.

**Q: How are keywords case-handled?**
A: All keywords are checked case-insensitively. "Lead", "LEAD", "lead" all match.

**Q: Can I customize action file format?**
A: Yes! Edit the `create_action_file()` method in `linkedin_watcher.py` (line 460+)

**Q: Does it track which messages it's already processed?**
A: Yes! Uses `.linkedin_processed_messages.json` to prevent duplicates.

**Q: What if LinkedIn changes their page layout?**
A: Selectors may need adjustment. Edit lines 87-90 with new selectors.

---

## Next Steps

1. ✅ Complete setup above
2. ✅ Run the watcher: `python scripts/linkedin_watcher.py`
3. ✅ Complete manual LinkedIn login on first run
4. ✅ Monitor `vault/linkedin_watcher_log.txt` for activity
5. ✅ Check `vault/Needs_Action/` for created action files
6. ✅ Set up task automation to process action files
7. ✅ (Optional) Run as a scheduled service for always-on monitoring

---

## Support

For issues:
1. Check `vault/linkedin_watcher_log.txt` for detailed error messages
2. Review the **Troubleshooting** section above
3. Verify all prerequisites are installed
4. Try deleting session folder and starting fresh

---

**Happy monitoring! 🚀**
