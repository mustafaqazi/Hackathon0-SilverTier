# Claude Skills Reference

Quick command reference for invoking Agent Skills from Claude Code.

## Skill Commands

### Gmail Send
**Send an email:**
```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to recipient@example.com \
  --subject "Subject Line" \
  --body "Email message body"
```

**With CC:**
```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to recipient@example.com \
  --cc other@example.com,another@example.com \
  --subject "Subject" \
  --body "Body"
```

**Expected Output:**
```
EMAIL_SENT: recipient@example.com | Subject: Subject Line
```

---

### LinkedIn Post
**Create a post:**
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Your post content goes here"
```

**With custom timeout:**
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Your post content" \
  --timeout 60000
```

**Expected Output:**
```
LINKEDIN_POSTED: 2026-02-18T21:18:43.123456 | Message length: 250 chars
```

---

### Vault File Manager
**Move task:**
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action move \
  --source Inbox \
  --destination Needs_Action \
  --file filename.md
```

**List tasks:**
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action list \
  --folder Inbox
```

**Copy task:**
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action copy \
  --source Needs_Action \
  --destination Done \
  --file filename.md
```

**Valid folders:**
- Inbox
- Needs_Action
- Needs_Approval
- Done

**Expected Output:**
```
TASK_MOVED: filename.md | From: Inbox → To: Needs_Action
TASKS_IN_INBOX: 5 | file1.md, file2.md, file3.md, file4.md, file5.md
```

---

### Human Approval
**Request approval:**
```bash
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Describe the action that needs approval" \
  --reason "Explain why this action needs approval" \
  --timeout 3600
```

**With 10-minute timeout:**
```bash
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send email to customer" \
  --reason "Customer support response" \
  --timeout 600
```

**Expected Output:**
```
APPROVAL_GRANTED: REQUEST_abc123 | Approved at 2026-02-18T21:20:15.123456
```

---

## Environment Setup

Before using skills, ensure environment variables are set:

```bash
export EMAIL_ADDRESS="your.email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export LINKEDIN_EMAIL="your.linkedin@gmail.com"
export LINKEDIN_PASSWORD="your_linkedin_password"
export VAULT_PATH="./AI_Employee_Vault/"
```

Or create .env file and load it:
```bash
export $(cat .env | xargs)
```

## Error Codes

All errors follow format: `[SKILL]_ERROR: [message]`

**Examples:**
```
EMAIL_ERROR: Authentication failed. Check credentials
LINKEDIN_ERROR: Could not find post button
VAULT_ERROR: File not found in Inbox/filename.md
APPROVAL_ERROR: Vault not found at ./AI_Employee_Vault/
```

## Output Parsing

All outputs are single-line, easy to parse:

```
[ACTION]_[STATUS]: [primary_info] | [secondary_info]
```

**Examples:**
```
EMAIL_SENT: user@example.com | Subject: Meeting Reminder
LINKEDIN_POSTED: 2026-02-18T21:18:43 | Message length: 245 chars
TASK_MOVED: proposal.md | From: Inbox → To: Needs_Action
APPROVAL_GRANTED: Send email | Approved at 2026-02-18T21:20:15
```

## Workflow Examples

### Example 1: Complete Task Workflow

```bash
# 1. List all inbox tasks
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action list --folder Inbox

# 2. Move task to review
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action move --source Inbox \
  --destination Needs_Action --file task.md

# 3. Send approval notification
python .claude/skills/gmail-send/scripts/send_email.py \
  --to reviewer@example.com \
  --subject "Task Ready for Review" \
  --body "A new task is ready for your review in Needs_Action folder"

# 4. Wait for human approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Complete task.md review" \
  --reason "Task completion approval" \
  --timeout 3600
```

### Example 2: LinkedIn Announcement + Notification

```bash
# 1. Create LinkedIn post
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Excited to announce our new AI Employee system is live! 🚀"

# 2. Email team
python .claude/skills/gmail-send/scripts/send_email.py \
  --to team@company.com \
  --subject "LinkedIn Announcement Posted" \
  --body "The announcement has been posted to LinkedIn"
```

### Example 3: Multi-Email Campaign

```bash
# Send to each email (script should loop)
for email in user1@example.com user2@example.com user3@example.com; do
  python .claude/skills/gmail-send/scripts/send_email.py \
    --to "$email" \
    --subject "Important Update" \
    --body "Please review the attached update"
done
```

## Performance Notes

- **Gmail:** 1-3 seconds per email
- **LinkedIn:** 15-30 seconds per post (browser startup overhead)
- **Vault Manager:** <100ms per operation
- **Approval:** Waits indefinitely until decision (polling every 2 seconds)

## Security Notes for Claude

1. **Never hardcode credentials** - Always use environment variables
2. **Never expose credentials in output** - Scripts clean all logs
3. **Always request approval** - For sensitive actions use human-approval skill
4. **Check file destinations** - Verify vault paths before moving files
5. **Respect rate limits** - Space out emails and posts

## Debugging

### Check environment:
```bash
env | grep EMAIL
env | grep LINKEDIN
env | grep VAULT
```

### Check vault structure:
```bash
ls -la AI_Employee_Vault/
```

### Check logs:
```bash
tail -f AI_Employee_Vault/vault.log
tail -f AI_Employee_Vault/approval.log
```

### Test connectivity:
```bash
python -c "import smtplib; print('SMTP OK')"
python -c "import playwright; print('Playwright OK')"
```

## Skill Limitations

- **Gmail:** Text emails only (no rich formatting)
- **LinkedIn:** Text posts only (no media/links)
- **Vault:** Local filesystem only
- **Approval:** Requires manual file edit (intentional for security)

## Future Enhancement Ideas

- Email templates
- LinkedIn scheduling
- Bulk operations
- Advanced approval workflows
- Webhook integration
- Database logging

---

**Version:** 1.0
**Last Updated:** 2026-02-18
**Status:** Production Ready

For detailed setup, see SETUP.md
For skill documentation, see individual SKILL.md files
