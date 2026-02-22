# How to Use Gmail-Send Skill

Complete guide to send real emails using the AI Employee gmail-send skill.

## Quick Start (5 minutes)

### 1. Get Gmail App Password

Go to: https://myaccount.google.com/security

**Steps:**
1. Click "Security" in left sidebar
2. Enable "2-Step Verification" (if not enabled)
3. Return to Security page
4. Find "App passwords"
5. Select "Mail" and "Windows Computer"
6. Copy the 16-character password

**Do NOT use your regular Gmail password!**

### 2. Set Environment Variables

**Windows (Command Prompt):**
```batch
setx EMAIL_ADDRESS "your.email@gmail.com"
setx EMAIL_PASSWORD "your_app_password_16_chars"
```

Then close and reopen Command Prompt for changes to take effect.

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("EMAIL_ADDRESS", "your.email@gmail.com", "User")
[Environment]::SetEnvironmentVariable("EMAIL_PASSWORD", "your_app_password_16_chars", "User")
```

### 3. Test the Skill

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to test@example.com ^
  --subject "Test Email" ^
  --body "This is a test email"
```

**Expected Output (Success):**
```
EMAIL_SENT: test@example.com | Subject: Test Email
```

**Expected Output (Error):**
```
EMAIL_ERROR: Authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD
```

---

## Basic Usage

### Send a Simple Email

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to recipient@example.com ^
  --subject "My Subject" ^
  --body "Email body text here"
```

### Send to Multiple Recipients (One at a time)

```bash
# Recipient 1
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to user1@example.com ^
  --subject "Subject" ^
  --body "Body"

# Recipient 2
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to user2@example.com ^
  --subject "Subject" ^
  --body "Body"

# Recipient 3
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to user3@example.com ^
  --subject "Subject" ^
  --body "Body"
```

### Send with CC

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to recipient@example.com ^
  --cc manager@example.com,supervisor@example.com ^
  --subject "Subject" ^
  --body "Body"
```

---

## Advanced Usage

### Custom SMTP Server

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to recipient@example.com ^
  --subject "Subject" ^
  --body "Body" ^
  --smtp-host mail.company.com ^
  --smtp-port 587
```

### Multi-line Email Body

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to recipient@example.com ^
  --subject "Important Update" ^
  --body "Dear Customer,

We have an important update for you.

Key Points:
- Point 1
- Point 2
- Point 3

Best regards,
The Team"
```

### Batch Email Script

Create file `send_emails.bat`:

```batch
@echo off

REM Define recipients
set RECIPIENT1=customer1@example.com
set RECIPIENT2=customer2@example.com
set RECIPIENT3=customer3@example.com

set SUBJECT="Exciting New Feature: Dark Mode"
set BODY="Dear Customer, We're thrilled to announce Dark Mode!"

REM Send to each recipient
python .claude/skills/gmail-send/scripts/send_email.py --to %RECIPIENT1% --subject %SUBJECT% --body %BODY%
python .claude/skills/gmail-send/scripts/send_email.py --to %RECIPIENT2% --subject %SUBJECT% --body %BODY%
python .claude/skills/gmail-send/scripts/send_email.py --to %RECIPIENT3% --subject %SUBJECT% --body %BODY%

echo All emails sent!
```

---

## Real-World Examples

### Example 1: Customer Announcement

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to customer@example.com ^
  --subject "Exciting New Feature: Dark Mode is Now Available!" ^
  --body "Dear Valued Customer,

We're thrilled to announce the launch of our new Dark Mode feature!

Dark Mode reduces eye strain during evening browsing and provides a modern, sleek interface.

Key Benefits:
- Reduces eye strain in low-light environments
- Battery-friendly on OLED screens
- Modern, sleek interface

How to Enable:
1. Go to Settings
2. Select Appearance
3. Toggle Dark Mode ON

Best regards,
The Product Team"
```

### Example 2: Team Notification

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to team@company.com ^
  --cc manager@company.com ^
  --subject "Project Status Update - Week of Feb 18" ^
  --body "Team,

Here's the status update for this week:

Completed:
- Scheduler implementation
- Email skill integration
- Testing suite

In Progress:
- Dark Mode feature
- API optimization

Blockers:
- None currently

See you at Friday standup!

Best,
AI Employee System"
```

### Example 3: Reminder Email

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to user@example.com ^
  --subject "Reminder: Action Plan Review Needed" ^
  --body "Hi,

You have an action plan awaiting review in the AI Employee system.

Task: Add Dark Mode Toggle Feature
Priority: Medium
Deadline: 2026-02-20

Please review and approve at your earliest convenience.

Generated plans location: vault/Needs_Action/

Thanks!"
```

---

## Verification

### Check if Email Was Sent

**Success Output:**
```
EMAIL_SENT: recipient@example.com | Subject: Your Subject
```

**Error Output:**
```
EMAIL_ERROR: [error description]
```

### Verify in Recipient's Inbox

1. Check recipient's inbox (not spam folder)
2. Verify subject line matches
3. Verify body content is correct
4. Check sender is your email address

### Check Email Logs

Logs are saved to: `.claude/skills/gmail-send/scripts/logs/actions.log`

```bash
type .claude/skills/gmail-send/scripts/logs/actions.log
```

---

## Troubleshooting

### Issue: "EMAIL_ERROR: Authentication failed"

**Solution:**
1. Verify EMAIL_ADDRESS is correct
2. Use App Password, NOT regular Gmail password
3. Check 2-Step Verification is enabled on Gmail account
4. Verify credentials are set correctly:
   ```bash
   echo %EMAIL_ADDRESS%
   echo %EMAIL_PASSWORD%
   ```

### Issue: "EMAIL_ERROR: Connection refused"

**Solution:**
1. Check internet connection
2. Verify SMTP port 587 is accessible
3. Try with different SMTP settings
4. Check firewall isn't blocking port 587

### Issue: Emails not appearing in inbox

**Solution:**
1. Check spam/junk folder
2. Wait a few minutes (delayed delivery)
3. Verify recipient email address is correct
4. Check sender email isn't on blocklist
5. Verify email permissions in Gmail

### Issue: "Parameter required: --to, --subject, --body"

**Solution:**
Ensure all required parameters are provided:
```bash
python send_email.py ^
  --to recipient@example.com ^      [REQUIRED]
  --subject "Subject" ^              [REQUIRED]
  --body "Body text" ^               [REQUIRED]
  --cc optional@example.com          [OPTIONAL]
```

---

## Integration with AI Employee

### Send Email from Task Plan

When a task plan is created that involves sending email:

1. **Review the plan** in `vault/Needs_Action/`
2. **Request approval** (optional):
   ```bash
   python .claude/skills/human-approval/scripts/request_approval.py ^
     --action "Send customer notification emails" ^
     --reason "Product announcement"
   ```
3. **Execute the email command** from this guide
4. **Verify delivery** in recipient's inbox
5. **Move task to Done**:
   ```bash
   python .claude/skills/vault-file-manager/scripts/move_task.py ^
     --action move ^
     --source Needs_Action ^
     --destination Done ^
     --file [task_file].md
   ```

---

## Best Practices

### DO:
- ✅ Use App Passwords (not regular password)
- ✅ Test with your own email first
- ✅ Use professional subject lines
- ✅ Keep email body clear and concise
- ✅ Request approval for customer emails
- ✅ Verify delivery after sending
- ✅ Log important emails

### DON'T:
- ❌ Use regular Gmail password
- ❌ Send to invalid email addresses
- ❌ Use offensive or spam content
- ❌ Send too frequently to same recipient
- ❌ Ignore email errors
- ❌ Forget to verify credentials
- ❌ Send to wrong recipients

---

## Security Notes

### Credential Safety
- Environment variables are local to your machine
- Never commit credentials to version control
- Use App Passwords instead of main account password
- Regenerate credentials periodically
- Revoke App Password if compromised

### Email Safety
- Never send sensitive information via email
- Verify recipient email addresses carefully
- Use BCC for large distribution lists
- Keep audit logs of mass emails
- Implement approval gates for customer communications

---

## Support

### Quick Reference

**Skill Location:**
`.claude/skills/gmail-send/`

**Documentation:**
`.claude/skills/gmail-send/SKILL.md`

**Script Location:**
`.claude/skills/gmail-send/scripts/send_email.py`

**Help Command:**
```bash
python .claude/skills/gmail-send/scripts/send_email.py --help
```

---

## Next Steps

1. **Get Gmail App Password** (myaccount.google.com/security)
2. **Set Environment Variables** (use SETUP_EMAIL_CREDENTIALS.bat or manual)
3. **Test with Own Email** (send yourself a test email)
4. **Send Real Emails** (use examples from this guide)
5. **Integrate with Tasks** (combine with task planner)
6. **Automate** (use with scheduler for automated campaigns)

---

**Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready
