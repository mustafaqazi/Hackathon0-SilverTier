# Gmail Watcher - Complete Documentation

**Version:** 1.0
**Status:** Production Ready
**Project:** Silver Tier AI Employee
**Created:** 2026-02-19

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [File Formats](#file-formats)
8. [Logging](#logging)
9. [API Reference](#api-reference)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Gmail Watcher?

Gmail Watcher is a production-ready Python application that:

- **Monitors** Gmail inbox for unread + important emails
- **Creates** action files in `vault/Needs_Action/` for each new email
- **Tracks** processed emails to prevent duplicates
- **Logs** all activity to console + file
- **Runs** continuously with configurable check intervals
- **Handles** errors gracefully without stopping

### Key Features

✓ **Selective Monitoring**: Only unread AND important (starred) emails
✓ **Automated File Creation**: Markdown action files with YAML frontmatter
✓ **Duplicate Prevention**: Tracks processed email IDs
✓ **Smart Authentication**: OAuth2 with token caching
✓ **Robust Logging**: Console + file with timestamps
✓ **Error Resilience**: Continues on API errors
✓ **Configurable**: Easy to modify queries, intervals, output
✓ **Production Ready**: Full documentation, tests, setup guides

---

## Architecture

### System Design

```
┌─────────────────────────────────────────┐
│        Gmail Watcher Application        │
└─────────────────────────────────────────┘
           │
           ├─► Gmail API Client
           │   ├─ OAuth2 Authentication
           │   ├─ Token Management
           │   └─ Email Retrieval
           │
           ├─► Vault Management
           │   ├─ Path Resolution
           │   ├─ File I/O
           │   └─ ID Tracking
           │
           └─► Logging System
               ├─ Console Output
               └─ File Logging

       vault/
       ├─ gmail_credentials.json    (OAuth config)
       ├─ .gmail_token.json         (Cached token)
       ├─ .processed_email_ids.json (Processed IDs)
       ├─ gmail_watcher_log.txt     (Log output)
       └─ Needs_Action/
           ├─ EMAIL_[id1].md
           ├─ EMAIL_[id2].md
           └─ ...
```

### Class Structure

```python
GmailWatcher
├── __init__()
│   ├─ Setup vault paths
│   ├─ Load processed IDs
│   ├─ Setup logging
│   └─ Authenticate
│
├── _authenticate()
│   ├─ Load existing token
│   ├─ Refresh if expired
│   ├─ Run OAuth2 flow if needed
│   └─ Build Gmail service
│
├── check_for_updates()
│   ├─ Query Gmail API
│   ├─ Filter new emails
│   └─ Process each email
│
├── create_action_file()
│   ├─ Extract headers
│   ├─ Generate YAML frontmatter
│   ├─ Create markdown content
│   └─ Write file
│
├── _load_processed_ids()
├── _save_processed_ids()
├── _extract_email_headers()
├── _parse_received_date()
│
└── run()
    └─ Infinite loop with sleep(120)
```

---

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to scripts directory
cd AI_Employee/scripts

# Install packages
pip install -r requirements.txt
```

### 2. Setup Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download JSON file
6. Save to: `AI_Employee/vault/gmail_credentials.json`

### 3. Run Watcher

```bash
# Using Python directly
python gmail_watcher.py

# Or using batch file (Windows)
run_gmail_watcher.bat
```

### 4. First Authentication

- Browser opens automatically
- Sign in to Gmail
- Grant "Read your Gmail inbox" permission
- Token saved for future use

### 5. Monitor Output

- Check console for activity
- View logs: `vault/gmail_watcher_log.txt`
- Check created files: `vault/Needs_Action/`

---

## Detailed Setup

### Step 1: Install Python

**Windows:**
- Download from [python.org](https://www.python.org)
- Install with "Add Python to PATH" checked
- Verify: `python --version`

**Mac/Linux:**
```bash
# Using Homebrew (Mac)
brew install python3

# Using apt (Linux)
sudo apt-get install python3 python3-pip
```

### Step 2: Clone/Setup Project

```bash
# Navigate to project
cd AI_Employee

# Create scripts directory if needed
mkdir scripts
cd scripts
```

### Step 3: Install Dependencies

```bash
# Option A: Using requirements.txt
pip install -r requirements.txt

# Option B: Install individually
pip install google-api-python-client
pip install google-auth-oauthlib
pip install google-auth-httplib2
```

### Step 4: Google Cloud Setup

**Detailed Steps:**

1. **Create Project**
   - Visit: https://console.cloud.google.com
   - Click "Select a Project" → "NEW PROJECT"
   - Name: "AI Employee Gmail"
   - Click "CREATE"

2. **Enable Gmail API**
   - Search: "Gmail API"
   - Click on it
   - Click "ENABLE"

3. **Create OAuth Credentials**
   - Go to "Credentials" (left sidebar)
   - Click "CREATE CREDENTIALS"
   - Choose "OAuth client ID"
   - Select "Desktop application"
   - Click "CREATE"
   - Click "DOWNLOAD JSON" (downloads credentials.json)

4. **Place Credentials File**
   - Rename downloaded file to: `gmail_credentials.json`
   - Move to: `AI_Employee/vault/`

### Step 5: Verify Setup

```bash
# Run test script
python test_gmail_watcher.py

# Should output: ✓ ALL TESTS PASSED!
```

### Step 6: Run Watcher

```bash
# Start the watcher
python gmail_watcher.py

# Expected output:
# ======================================================================
# Gmail Watcher initialized
# Loaded 0 previously processed email IDs
# Successfully authenticated with Gmail API
# STARTING GMAIL WATCHER
# ...
```

---

## Usage

### Basic Usage

```bash
cd AI_Employee/scripts
python gmail_watcher.py
```

### Stop the Watcher

- Press `Ctrl+C`
- Watcher gracefully shuts down
- Logs summary to file

### Run in Background (Windows)

```bash
# Create batch file
start run_gmail_watcher.bat

# Or use Python subprocess
python -m pythonw gmail_watcher.py
```

### Run in Background (Mac/Linux)

```bash
# Using nohup
nohup python gmail_watcher.py > /dev/null 2>&1 &

# Or using screen
screen -S watcher
python gmail_watcher.py
# Press Ctrl+A then D to detach
```

### Monitor in Real-Time

```bash
# Windows - Follow log file
Get-Content vault\gmail_watcher_log.txt -Wait

# Mac/Linux
tail -f vault/gmail_watcher_log.txt
```

---

## Configuration

### Modify Check Interval

**Current:** 120 seconds (2 minutes)

Edit `gmail_watcher.py`, in `run()` method:

```python
time.sleep(120)  # Change to desired seconds
```

Examples:
```python
time.sleep(60)    # Check every minute
time.sleep(300)   # Check every 5 minutes
time.sleep(3600)  # Check every hour
```

### Modify Email Query

**Current:** `is:unread is:important`

Edit `check_for_updates()` method:

```python
query = 'is:unread is:important'
```

**Other Query Examples:**

```python
# All unread emails
query = 'is:unread'

# All important emails
query = 'is:important'

# From specific person
query = 'is:unread is:important from:boss@example.com'

# Keywords in subject
query = 'is:unread subject:urgent'

# Multiple conditions
query = 'is:unread is:important (from:team@company.com OR from:boss@company.com)'

# Exclude certain senders
query = 'is:unread is:important -from:newsletter@example.com'

# Specific label
query = 'label:important-clients is:unread'
```

### Modify Max Results

**Current:** 10 per check

Edit `check_for_updates()` method:

```python
maxResults=10  # Change to desired number
```

### Modify Log Level

**Current:** INFO

Edit `setup_logging()` function:

```python
logger.setLevel(logging.DEBUG)  # For verbose output
# or
logger.setLevel(logging.WARNING)  # For minimal output
```

---

## File Formats

### Action File: EMAIL_[message_id].md

**Location:** `vault/Needs_Action/EMAIL_[message_id].md`

**Example:** `EMAIL_abc123xyz789def.md`

**Content Structure:**

```markdown
---
type: email
from: sender@example.com
to: recipient@example.com
subject: Important: Project Update
received: 2026-02-19T10:30:45.123456+00:00
priority: high
status: pending
message_id: abc123xyz789def
---

## Email Content

**From:** sender@example.com
**Subject:** Important: Project Update
**Received:** 2026-02-19T10:30:45.123456+00:00

### Preview
This is the email preview/snippet that gets extracted from Gmail...

## Suggested Actions
- [ ] Reply
- [ ] Forward
- [ ] Archive
- [ ] Mark as Read

---
*Generated by Gmail Watcher on 2026-02-19T10:30:51.123456*
```

### Processed IDs File: .processed_email_ids.json

**Location:** `vault/.processed_email_ids.json`

**Purpose:** Tracks which emails have been processed to prevent duplicates

**Content:**
```json
{
  "processed_ids": [
    "abc123xyz789def",
    "def456xyz123abc",
    "ghi789xyz456def"
  ]
}
```

### Log File: gmail_watcher_log.txt

**Location:** `vault/gmail_watcher_log.txt`

**Format:**
```
2026-02-19 10:30:45 - GmailWatcher - INFO - Gmail Watcher initialized
2026-02-19 10:30:45 - GmailWatcher - INFO - Vault root: C:\Users\...\AI_Employee\vault
2026-02-19 10:30:46 - GmailWatcher - INFO - Successfully authenticated with Gmail API
2026-02-19 10:30:48 - GmailWatcher - INFO - [Check #1] Checking for new emails...
2026-02-19 10:30:50 - GmailWatcher - INFO - Found 2 unread important emails
2026-02-19 10:30:51 - GmailWatcher - INFO - ✓ Created action file: EMAIL_abc123.md
2026-02-19 10:30:51 - GmailWatcher - INFO - From: sender@example.com
2026-02-19 10:30:51 - GmailWatcher - INFO - Subject: Important: Project Update
```

---

## Logging

### Log Levels

| Level | Purpose | Example |
|-------|---------|---------|
| DEBUG | Detailed diagnostic info | Token refresh details |
| INFO | General informational | File created, check performed |
| WARNING | Something unexpected | Failed to parse date |
| ERROR | Error occurred | API failed, file write failed |
| CRITICAL | Severe error | Cannot access vault |

### Log Locations

**Console:** Real-time output while running

**File:** `vault/gmail_watcher_log.txt` - Persisted after exit

### Sample Log Output

```
======================================================================
Gmail Watcher initialized
======================================================================
Vault root: C:\Users\Mustafa\AI_Employee\vault
Needs_Action folder: C:\Users\Mustafa\AI_Employee\vault\Needs_Action
Loaded 5 previously processed email IDs

Successfully authenticated with Gmail API

======================================================================
STARTING GMAIL WATCHER
======================================================================
Monitoring: unread + important emails
Check interval: 120 seconds (2 minutes)
Output folder: C:\Users\Mustafa\AI_Employee\vault\Needs_Action
======================================================================

[Check #1] Checking for new emails...
Found 2 unread important emails
✓ Created action file: EMAIL_msg_123.md
  From: boss@company.com
  Subject: Q1 Planning - Action Required
✓ Created action file: EMAIL_msg_456.md
  From: team@company.com
  Subject: Project Status Update

Waiting 120 seconds until next check...
```

---

## API Reference

### GmailWatcher Class

#### `__init__()`

Initialize Gmail Watcher. Sets up paths, logging, and authentication.

```python
watcher = GmailWatcher()
```

**Raises:**
- `FileNotFoundError`: If credentials file not found
- `Exception`: If authentication fails

---

#### `run()`

Run the watcher in infinite loop, checking every 120 seconds.

```python
watcher.run()
```

**Behavior:**
- Checks for new emails every 120 seconds
- Creates action files for new unread important emails
- Handles KeyboardInterrupt (Ctrl+C) gracefully
- Logs all activity

---

#### `check_for_updates()`

Query Gmail API for new unread important emails.

```python
watcher.check_for_updates()
```

**Query:** `is:unread is:important`
**Max Results:** 10
**Returns:** None (processes emails as side effect)

---

#### `create_action_file(message: dict)`

Create markdown action file for an email.

```python
# Typically called internally
watcher.create_action_file(message)
```

**Parameters:**
- `message`: Gmail message object from API

**Output:** Creates `EMAIL_[message_id].md` in `Needs_Action/`

---

### Module-Level Functions

#### `setup_logging(log_file_path: Path) -> logging.Logger`

Setup logging to console and file.

```python
logger = setup_logging(Path('vault/gmail_watcher_log.txt'))
```

**Returns:** Configured logger instance

---

## Troubleshooting

### Issue: "Credentials file not found"

**Cause:** `gmail_credentials.json` not in vault folder

**Solution:**
1. Download from Google Cloud Console
2. Place at: `AI_Employee/vault/gmail_credentials.json`
3. Restart watcher

---

### Issue: "Gmail service not initialized"

**Cause:** Authentication failed

**Check:**
1. Internet connection working?
2. Google Cloud project created?
3. Gmail API enabled?
4. Credentials file valid?

**Fix:**
1. Check logs: `vault/gmail_watcher_log.txt`
2. Verify credentials file: `vault/gmail_credentials.json`
3. Restart watcher

---

### Issue: "Browser not opening for authorization"

**Cause:** OAuth2 flow needs user interaction

**Solution:**
1. Go to console output URL
2. Or manually open: `http://localhost:8080`
3. Sign in and grant permissions
4. Token will be saved

---

### Issue: No action files created

**Check:**
1. Do you have unread important emails in Gmail?
   - Go to Gmail
   - Mark some emails as important/starred
   - Wait for next check

2. Are emails already processed?
   - Check: `vault/.processed_email_ids.json`
   - Delete if you want to reprocess

3. Check logs for errors
   - `vault/gmail_watcher_log.txt`

---

### Issue: Token expired

**Symptoms:** "Invalid token" errors in logs

**Fix:**
1. Delete: `vault/.gmail_token.json`
2. Restart watcher
3. Re-authorize in browser

---

### Issue: Script runs but doesn't check

**Cause:** Wrong query or no matching emails

**Debug:**
1. Manually check Gmail for unread important emails
2. Add test email and mark as important
3. Restart watcher and watch logs
4. Monitor `vault/Needs_Action/` for new files

---

### Issue: Performance/Memory Issues

**Optimization:**
1. Increase check interval (currently 120 seconds)
2. Reduce max results (currently 10)
3. Narrow query (more specific keywords)

Example - Check every 5 minutes:
```python
time.sleep(300)  # Instead of 120
```

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review action files in `Needs_Action/`
- Clean up processed emails
- Check log file for warnings

**Monthly:**
- Archive old action files
- Review processed IDs (consider resetting)
- Check for API quota usage

### Backup Important Files

Keep backups of:
- `.processed_email_ids.json` (tracks processed emails)
- `gmail_watcher_log.txt` (activity history)

### Resetting the Watcher

**Clear processed emails (reprocess all):**
```bash
# Delete the processed IDs file
rm vault/.processed_email_ids.json

# Restart watcher
python gmail_watcher.py
```

**Clear authentication (re-authorize):**
```bash
# Delete token file
rm vault/.gmail_token.json

# Restart watcher - will prompt for authorization
python gmail_watcher.py
```

---

## Performance Metrics

**Resource Usage:**
- **Memory:** ~50-100 MB
- **CPU:** ~1-5% during checks, <1% idle
- **Network:** ~1-2 API calls per check (~10KB each)
- **Disk:** ~1-5 KB per email file

**Recommended Settings:**
- **Check interval:** 120-300 seconds (2-5 minutes)
- **Max results:** 5-10 per check
- **Log rotation:** Monthly

---

## Security

### Private Files (Do NOT Commit)

Already in `.gitignore`:
- `gmail_credentials.json` - OAuth configuration
- `.gmail_token.json` - Access token
- `.processed_email_ids.json` - Internal tracking

### Best Practices

✓ Keep credentials file private
✓ Never share token files
✓ Use service account for production
✓ Rotate credentials regularly
✓ Monitor API usage
✓ Log suspicious activity

---

## Support & Resources

### Documentation Files

1. **GMAIL_WATCHER_README.md** - This file (complete documentation)
2. **GMAIL_WATCHER_SETUP.md** - Setup guide
3. **requirements.txt** - Dependencies list

### Python Files

1. **gmail_watcher.py** - Main application
2. **test_gmail_watcher.py** - Verification script
3. **run_gmail_watcher.bat** - Windows launcher

### External Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com)

---

## Version History

**v1.0 - 2026-02-19**
- Initial production release
- Complete Gmail monitoring
- Action file generation
- OAuth2 authentication
- Full logging and error handling

---

## License & Attribution

**Project:** Silver Tier AI Employee
**Component:** Gmail Watcher
**Status:** Production Ready
**Last Updated:** 2026-02-19

---

**Questions? Issues? Refer to the troubleshooting section or check the logs!**
