# Gmail Watcher Setup Guide

## Overview
Gmail Watcher monitors unread + important Gmail emails and creates action files in `vault/Needs_Action` for the Silver Tier AI Employee project.

## Features
✓ Monitors only unread + important emails (`is:unread is:important`)
✓ Creates markdown action files: `EMAIL_[message_id].md`
✓ YAML frontmatter + markdown content format
✓ Tracks processed emails (no duplicates)
✓ Infinite loop with 120-second checks
✓ Comprehensive logging (console + file)
✓ Exception handling for all errors
✓ OAuth2 authentication with token caching

---

## Prerequisites

### 1. Python Packages
Install required dependencies:

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

Or use the requirements.txt (if available in project):

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (e.g., "AI Employee Gmail Watcher")
3. Enable the Gmail API:
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2: Create OAuth 2.0 Credentials
1. Go to "Credentials" in Google Cloud Console
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Choose "Desktop application"
4. Click "Create" and then "Download JSON"
5. Name it: `gmail_credentials.json`

#### Step 3: Place Credentials File
Copy the downloaded `gmail_credentials.json` to:

```
AI_Employee/vault/gmail_credentials.json
```

**Important:** Do NOT commit this file to Git (it's already in .gitignore)

---

## File Structure

```
AI_Employee/
├── vault/
│   ├── gmail_credentials.json        ← OAuth credentials (private, not committed)
│   ├── .gmail_token.json             ← Auto-generated token (first run)
│   ├── .processed_email_ids.json     ← Tracks processed emails
│   ├── gmail_watcher_log.txt         ← Log file
│   └── Needs_Action/
│       ├── EMAIL_[id_1].md           ← Generated action files
│       ├── EMAIL_[id_2].md
│       └── ...
├── scripts/
│   ├── gmail_watcher.py              ← Main watcher script
│   └── GMAIL_WATCHER_SETUP.md        ← This file
```

---

## Running the Gmail Watcher

### Option 1: Direct Execution

```bash
cd AI_Employee/scripts
python gmail_watcher.py
```

### Option 2: Background Execution (Windows)

Create a batch file `run_watcher.bat`:

```batch
@echo off
cd AI_Employee\scripts
python gmail_watcher.py
```

Then run it without blocking:
```bash
start run_watcher.bat
```

### Option 3: Task Scheduler (Windows)

Schedule the script to run at startup:

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "At startup"
4. Action: Start a program
5. Program: `C:\path\to\python.exe`
6. Arguments: `C:\path\to\AI_Employee\scripts\gmail_watcher.py`

---

## First Run Authentication

### On First Run:
1. Script will check for existing token
2. If none found, opens browser for OAuth login
3. Gmail login required
4. Grant permissions to "see Gmail inbox"
5. Token automatically saved to `vault/.gmail_token.json`
6. Subsequent runs use cached token (no login needed)

### If Token Expires:
- Script automatically refreshes token
- No user action required

---

## Output Files

### Action Files: `EMAIL_[message_id].md`

Example: `EMAIL_abc123xyz789.md`

**Format:**
```markdown
---
type: email
from: sender@example.com
to: your@gmail.com
subject: Email Subject
received: 2026-02-19T10:30:45.123456
priority: high
status: pending
message_id: abc123xyz789
---

## Email Content

**From:** sender@example.com
**Subject:** Email Subject
**Received:** 2026-02-19T10:30:45.123456

### Preview
Email snippet/preview text...

## Suggested Actions
- [ ] Reply
- [ ] Forward
- [ ] Archive
- [ ] Mark as Read
```

### Log File: `vault/gmail_watcher_log.txt`

Shows all checks, created files, errors:

```
2026-02-19 10:30:45 - GmailWatcher - INFO - Gmail Watcher initialized
2026-02-19 10:30:45 - GmailWatcher - INFO - Loaded 5 previously processed email IDs
2026-02-19 10:30:46 - GmailWatcher - INFO - Successfully authenticated with Gmail API
2026-02-19 10:30:48 - GmailWatcher - INFO - [Check #1] Checking for new emails...
2026-02-19 10:30:50 - GmailWatcher - INFO - Found 2 unread important emails
2026-02-19 10:30:51 - GmailWatcher - INFO - ✓ Created action file: EMAIL_abc123.md
```

---

## Configuration

### Check Interval
Default: 120 seconds (2 minutes)

To change, edit in `gmail_watcher.py`:
```python
time.sleep(120)  # Change 120 to desired seconds
```

### Email Query
Default: `is:unread is:important`

To modify, edit in `check_for_updates()`:
```python
query = 'is:unread is:important'  # Modify as needed
```

Other query options:
```python
'is:unread'                    # All unread emails
'is:important'                 # All important (starred) emails
'from:boss@company.com'        # From specific sender
'subject:urgent'               # Keywords in subject
```

### Max Results per Check
Default: 10

To change:
```python
maxResults=10  # Change to desired number
```

---

## Troubleshooting

### Issue: "Credentials file not found"

**Solution:**
1. Download credentials from Google Cloud Console
2. Place at: `AI_Employee/vault/gmail_credentials.json`
3. Restart script

### Issue: "Gmail service not initialized"

**Solution:**
1. Check internet connection
2. Check logs: `vault/gmail_watcher_log.txt`
3. Restart script

### Issue: No action files created

**Possible causes:**
1. No unread important emails (check Gmail directly)
2. Emails already processed (check `.processed_email_ids.json`)
3. Check logs for errors

**Debug:**
- Manually mark some emails as important in Gmail
- Restart watcher
- Monitor logs in real-time

### Issue: Token expired

**Solution:**
- Script auto-refreshes tokens
- If problems persist, delete `vault/.gmail_token.json`
- Script will re-authenticate on next run

---

## Security Notes

⚠️ **DO NOT COMMIT:**
- `gmail_credentials.json` (OAuth credentials)
- `.gmail_token.json` (Access token)
- `.processed_email_ids.json` (optional, but private data)

✓ **ALREADY GITIGNORED** in `.gitignore`

---

## Logs and Debugging

### View Live Logs

**Windows:**
```bash
type AI_Employee\vault\gmail_watcher_log.txt
```

**Unix/Mac:**
```bash
tail -f AI_Employee/vault/gmail_watcher_log.txt
```

### Debug Mode

Add to `gmail_watcher.py` for verbose output:
```python
logger.setLevel(logging.DEBUG)  # Instead of logging.INFO
```

---

## Performance

- **Check interval:** 2 minutes (adjustable)
- **Max results per check:** 10 (prevents rate limiting)
- **Memory usage:** ~50-100 MB
- **CPU usage:** Minimal (only during checks)
- **Network:** ~1-2 requests per check

---

## Common Queries

### Monitor Only Flagged Emails
```python
query = 'is:unread is:starred'
```

### Monitor From Specific Person
```python
query = 'is:unread is:important from:boss@company.com'
```

### Monitor With Keywords
```python
query = 'is:unread is:important subject:urgent'
```

### Exclude Certain Senders
```python
query = 'is:unread is:important -from:newsletter@company.com'
```

---

## Next Steps

1. ✓ Install dependencies
2. ✓ Setup Google Cloud project
3. ✓ Download credentials.json
4. ✓ Place in `vault/` folder
5. ✓ Run script: `python gmail_watcher.py`
6. ✓ Authorize in browser (first run only)
7. ✓ Monitor logs and action files

---

## Support

For issues:
1. Check `vault/gmail_watcher_log.txt`
2. Verify `gmail_credentials.json` location
3. Ensure internet connection
4. Check Gmail API is enabled in Google Cloud
5. Try deleting token and re-authenticating

---

**Last Updated:** 2026-02-19
**Version:** 1.0
**Status:** Production Ready
