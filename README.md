# Agent Skills - Production Level (Silver Tier)

Complete set of 4 production-ready agent skills for Personal AI Employee system.

## Skills Overview

| Skill | Purpose | Status | Environment Variables |
|-------|---------|--------|----------------------|
| **gmail-send** | Send real emails via SMTP | ✅ Ready | EMAIL_ADDRESS, EMAIL_PASSWORD |
| **linkedin-post** | Create LinkedIn posts | ✅ Ready | LINKEDIN_EMAIL, LINKEDIN_PASSWORD |
| **vault-file-manager** | Manage task workflow files | ✅ Ready | VAULT_PATH (optional) |
| **human-approval** | Human-in-the-loop decisions | ✅ Ready | VAULT_PATH (optional) |

## Quick Start

### 1. Gmail Send
Send emails from your AI Employee:
```bash
export EMAIL_ADDRESS="your.email@gmail.com"
export EMAIL_PASSWORD="your_app_password"

python .claude/skills/gmail-send/scripts/send_email.py \
  --to recipient@example.com \
  --subject "Subject" \
  --body "Email body"
```

**Note:** For Gmail, use [App Passwords](https://support.google.com/accounts/answer/185833)

### 2. LinkedIn Post
Create LinkedIn posts automatically:
```bash
export LINKEDIN_EMAIL="your.email@linkedin.com"
export LINKEDIN_PASSWORD="your_password"

python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --message "Your post content here"
```

**Setup:** `pip install playwright && playwright install chromium`

### 3. Vault File Manager
Manage task workflow:
```bash
# Move task from Inbox to Needs_Action
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action move \
  --source Inbox \
  --destination Needs_Action \
  --file task.md

# List all tasks in Inbox
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action list \
  --folder Inbox

# Copy task (keep original)
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --action copy \
  --source Needs_Action \
  --destination Done \
  --file task.md
```

### 4. Human Approval
Request human review for sensitive actions:
```bash
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send email to john@example.com" \
  --reason "Customer support response"
```

**Workflow:**
1. Script creates approval request file
2. Human opens file and changes STATUS to APPROVED/REJECTED
3. Script detects change and continues
4. File is cleaned up automatically

## Vault Structure

All tasks are organized in:
```
AI_Employee_Vault/
├── Inbox/              (New tasks - inbox)
├── Needs_Action/       (Awaiting human review)
├── Needs_Approval/     (Awaiting approval)
└── Done/               (Completed tasks)

Logs:
├── vault.log          (File manager operations)
└── approval.log       (Approval decisions)
```

## Environment Setup

Create `.env` file in project root:
```env
# Gmail Configuration
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password

# LinkedIn Configuration
LINKEDIN_EMAIL=your.email@linkedin.com
LINKEDIN_PASSWORD=your_password

# Vault Configuration
VAULT_PATH=./AI_Employee_Vault/
```

Then load: `export $(cat .env | xargs)`

## Architecture

Each skill is **production-ready** and includes:
- ✅ Real functionality (not simulations)
- ✅ Proper error handling
- ✅ Logging and audit trails
- ✅ Clean, parseable output
- ✅ Environment-based configuration
- ✅ Token-efficient design
- ✅ Subprocess-safe execution

## Output Format

All skills use consistent output format:
```
[ACTION]_[STATUS]: [details] | [metadata]
```

Examples:
```
EMAIL_SENT: recipient@example.com | Subject: Meeting Reminder
LINKEDIN_POSTED: 2026-02-18T21:18:43 | Message length: 245 chars
TASK_MOVED: proposal.md | From: Inbox → To: Needs_Action
APPROVAL_GRANTED: Send email | Approved at 2026-02-18T21:20:15
```

## Error Handling

All errors follow pattern:
```
[ACTION]_ERROR: [error description]
```

Scripts exit with code 1 on error for easy error detection.

## Security Notes

1. **Credentials:** Always use environment variables, never hardcode
2. **Passwords:** Use app-specific passwords, not actual account passwords
3. **Logging:** Sensitive data is never logged
4. **Browsers:** Playwright closes browser after completion
5. **Files:** Approval requests stored in vault folder (local only)

## Token Efficiency

These skills are designed to minimize token usage:
- Direct subprocess execution (no streaming)
- Structured output (easy to parse)
- Fast execution (no long waits)
- Minimal logging (critical info only)

Perfect for replacing MCP servers with local executable skills.

## Troubleshooting

### Gmail: "Authentication failed"
- Verify EMAIL_ADDRESS is correct
- Use [App Password](https://support.google.com/accounts/answer/185833) not regular password
- Check SMTP settings (default: smtp.gmail.com:587)

### LinkedIn: "Could not find post button"
- LinkedIn changes UI frequently
- Try with --headless false to see what's happening
- Increase --timeout to 60000ms

### Vault: "File not found"
- Check vault path: `ls -la ./AI_Employee_Vault/`
- Ensure file exists in source folder
- Use --vault-path if vault is in different location

### Approval: "Timeout after waiting"
- Increase --timeout parameter
- Check Needs_Approval folder for request file
- Ensure file status is changed to APPROVED or REJECTED

## Future Enhancements

Planned for future versions:
- [ ] LinkedIn media uploads
- [ ] Gmail attachments
- [ ] Bulk email sending
- [ ] Advanced LinkedIn scheduling
- [ ] Email templates
- [ ] Approval workflows

## License

These skills are part of the Personal AI Employee system.
Production-ready. Use at your own discretion.

---

**Created:** 2026-02-18
**Version:** 1.0
**Status:** Production Ready
"# Hackathon0-SilverTier" 
