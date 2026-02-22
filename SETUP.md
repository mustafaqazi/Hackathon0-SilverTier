# Agent Skills Setup Guide

Complete installation and configuration guide for all 4 production-level Agent Skills.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Git (optional)

## Installation Steps

### Step 1: Create Vault Directory

```bash
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Needs_Approval,Done}
```

### Step 2: Install Dependencies

#### For all skills:
```bash
pip install --upgrade pip
```

#### For LinkedIn Posting (optional):
```bash
pip install playwright
playwright install chromium
```

#### For Gmail (built-in):
No additional packages needed - uses Python's `smtplib`

### Step 3: Configure Environment Variables

Create `.env` file in project root:

```env
# Gmail Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your_app_password

# LinkedIn Configuration (optional)
LINKEDIN_EMAIL=your-linkedin-email@gmail.com
LINKEDIN_PASSWORD=your_linkedin_password

# Vault Configuration
VAULT_PATH=./AI_Employee_Vault/
```

### Step 4: Load Environment Variables

**On Linux/Mac:**
```bash
export $(cat .env | xargs)
```

**On Windows (PowerShell):**
```powershell
Get-Content .env | ForEach-Object {
    $parts = $_ -split '='
    if ($parts.Length -eq 2) {
        [Environment]::SetEnvironmentVariable($parts[0], $parts[1])
    }
}
```

**Or manually:**
```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
# ... etc
```

## Skill Configuration

### 1. Gmail Send - Detailed Setup

**Get App Password for Gmail:**
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" (left sidebar)
3. Enable "2-Step Verification"
4. Go back to Security → App passwords
5. Select "Mail" and "Windows Computer"
6. Copy the generated 16-character password
7. Use as EMAIL_PASSWORD

**Test Gmail:**
```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to test@example.com \
  --subject "Test Email" \
  --body "This is a test email"
```

### 2. LinkedIn Post - Detailed Setup

**Install Playwright:**
```bash
pip install playwright
playwright install chromium
```

**Important Notes:**
- LinkedIn may request additional verification on first login
- Keep browser window visible with `--headless false` if login fails
- LinkedIn occasionally changes UI - adjust selectors if needed
- Posts are subject to LinkedIn's terms of service

**Test LinkedIn:**
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Hello from my AI Employee!" \
  --headless false
```

### 3. Vault File Manager - Setup

No additional setup needed. Just verify vault directory exists:

```bash
ls -la AI_Employee_Vault/
```

**Test:**
```bash
# Create a test file
echo "test content" > AI_Employee_Vault/Inbox/test.md

# List files
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action list \
  --folder Inbox

# Move file
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action move \
  --source Inbox \
  --destination Needs_Action \
  --file test.md
```

### 4. Human Approval - Setup

No additional setup needed.

**Test:**
```bash
# In terminal 1: Request approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Test action" \
  --reason "Testing approval workflow" \
  --timeout 60

# In terminal 2 (within 60 seconds): Edit the request file
# 1. Go to AI_Employee_Vault/Needs_Approval/REQUEST_*.mdcls
# 2. Change "## Status\nPENDING" to "## Status\nAPPROVED"
# 3. Save file
# 4. Script in terminal 1 will detect change and complete
```

## Verification Checklist

- [ ] Python 3.10+ installed: `python --version`
- [ ] Vault directories created: `ls -la AI_Employee_Vault/`
- [ ] Environment variables set: `echo $EMAIL_ADDRESS`
- [ ] Gmail credentials verified with App Password
- [ ] Playwright installed (if using LinkedIn): `pip show playwright`
- [ ] All skill scripts present: `.claude/skills/*/scripts/*.py`
- [ ] Test email sending works
- [ ] Vault file manager moves files correctly
- [ ] Human approval request file created correctly

## Directory Structure

After setup, you should have:

```
.
├── .claude/
│   └── skills/
│       ├── README.md
│       ├── SETUP.md
│       ├── gmail-send/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── send_email.py
│       ├── linkedin-post/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── post_linkedin.py
│       ├── vault-file-manager/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── move_task.py
│       └── human-approval/
│           ├── SKILL.md
│           └── scripts/
│               └── request_approval.py
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Needs_Approval/
│   ├── Done/
│   ├── vault.log
│   └── approval.log
└── .env (do not commit to git)
```

## Security Best Practices

1. **Never commit .env file** - Add to .gitignore:
   ```
   .env
   *.log
   AI_Employee_Vault/Needs_Approval/*
   ```

2. **Use App Passwords** - Never use your real account password

3. **Restrict File Permissions** - Keep .env readable only by you:
   ```bash
   chmod 600 .env
   ```

4. **Rotate Credentials** - Change passwords periodically

5. **Review Approval Requests** - Always review before approving

## Troubleshooting

### Gmail: "Authentication failed"
**Solution:**
- Verify EMAIL_ADDRESS is correct
- Use app-specific password, not account password
- Check 2-Step Verification is enabled

### Gmail: "Connection refused"
**Solution:**
- Check SMTP settings: `--smtp-host smtp.gmail.com --smtp-port 587`
- Verify firewall allows outbound port 587
- Try alternative SMTP: `--smtp-host smtp.gmail.com --smtp-port 465` with TLS

### LinkedIn: "Login failed"
**Solution:**
- Run with `--headless false` to see what's happening
- Check credentials in .env file
- LinkedIn may require additional verification - follow prompts

### LinkedIn: "Post button not found"
**Solution:**
- LinkedIn UI changes frequently
- Increase timeout: `--timeout 60000`
- Run with `--headless false` to debug
- May need to update selectors in script

### Vault: "File not found"
**Solution:**
- Verify vault path: `ls -la AI_Employee_Vault/`
- Check file exists in source folder
- Use absolute path with `--vault-path /full/path/to/vault`

### Approval: "Timeout waiting"
**Solution:**
- Check Needs_Approval folder for request file
- Ensure you change STATUS to APPROVED/REJECTED
- Increase timeout: `--timeout 600` (10 minutes)

## Usage in Claude Code

These skills can be invoked from Claude Code using the Skill tool:

```python
# Example: In Claude conversation
# "@claude-code /skill gmail-send --to user@example.com ..."
```

## Advanced Configuration

### Custom SMTP Server

Use with any SMTP provider (not just Gmail):

```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to user@example.com \
  --subject "Test" \
  --body "Testing" \
  --smtp-host mail.company.com \
  --smtp-port 587
```

### Custom Vault Location

Set VAULT_PATH to any location:

```bash
export VAULT_PATH=/path/to/custom/vault
```

### LinkedIn Headless Mode

Debug LinkedIn issues by running with visible browser:

```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Test" \
  --headless false \
  --timeout 60000
```

## Support

For issues or questions:
1. Check logs: `tail -f AI_Employee_Vault/*.log`
2. Run health checks for each skill
3. Review error messages - they're descriptive
4. Check environment variables: `env | grep EMAIL`

---

**Setup Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready
