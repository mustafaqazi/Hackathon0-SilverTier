# Testing Workflow - Practical Step-by-Step

Quick, practical testing workflow you can execute right now.

---

## Pre-Testing Checklist

Before starting, verify:
- [ ] You have Python 3.10+ installed
- [ ] You're in the project root: `E:\GH-Q4\Hackathon0-FTE`
- [ ] All skills folder exist in `.claude/skills/`
- [ ] All vault folders exist in `AI_Employee/vault/`

**Quick Setup Check:**
```bash
python --version
dir .claude\skills\
dir AI_Employee\vault\
```

---

## Testing Path 1: Scheduler & Task Planner (5 minutes)

### 1.1 Run Scheduler in Single-Pass Mode
```bash
cd E:\GH-Q4\Hackathon0-FTE
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Watch for these messages:**
```
[INFO] Running in single-pass mode
[INFO] Vault path: E:\GH-Q4\Hackathon0-FTE\AI_Employee\vault
[INFO] Detected X new task(s) in Inbox
[INFO] Task planner completed: X tasks processed
[INFO] Successfully processed X task(s)
```

**Result:** ✓ PASS if you see "Successfully processed"

### 1.2 Check Generated Plans
```bash
dir AI_Employee\vault\Needs_Action\ActionPlan*.md
```

**Result:** ✓ PASS if files were generated

### 1.3 View a Generated Plan
```bash
type AI_Employee\vault\Needs_Action\ActionPlan_*.md | more
```

**Verify it contains:**
- Task title
- Priority level
- Success criteria
- Execution steps
- Time estimates

**Result:** ✓ PASS if plan is comprehensive

---

## Testing Path 2: Gmail-Send Skill (10 minutes)

### 2.1 Set Email Credentials

**Option A: Interactive Setup**
```bash
AI_Employee\SETUP_EMAIL_CREDENTIALS.bat
```

**Option B: Manual Setup (Command Prompt)**
```bash
setx EMAIL_ADDRESS "your.email@gmail.com"
setx EMAIL_PASSWORD "your_app_password"
```

Then **close and reopen Command Prompt** for changes to take effect.

**Verify credentials are set:**
```bash
echo %EMAIL_ADDRESS%
echo %EMAIL_PASSWORD%
```

**Result:** ✓ PASS if both variables show values

### 2.2 Send Test Email

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "AI Employee Test Email" ^\
  --body "This is a test email from the AI Employee system."
```

**Expected Output:**
```
EMAIL_SENT: your.email@gmail.com | Subject: AI Employee Test Email
```

**Result:** ✓ PASS if you see "EMAIL_SENT"

### 2.3 Verify Email Arrives

1. Check your email inbox (wait 1-2 minutes)
2. Look for subject: "AI Employee Test Email"
3. Verify sender is your email address
4. Verify body content

**Result:** ✓ PASS if email appears in inbox

### 2.4 Test Error Handling

```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to invalid-email ^\
  --subject "Test" ^\
  --body "Test"
```

**Expected:**
```
EMAIL_ERROR: [error message]
```

**Result:** ✓ PASS if error is handled gracefully

---

## Testing Path 3: Vault File Manager (5 minutes)

### 3.1 List Files
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action list ^\
  --source Inbox
```

**Expected Output:**
```
VAULT_LIST: Inbox contains X files:
- filename1.md
- filename2.md
```

**Result:** ✓ PASS if list is displayed

### 3.2 Create Test File
```bash
type > AI_Employee\vault\Inbox\test_file.md < nul
echo Test content >> AI_Employee\vault\Inbox\test_file.md
```

### 3.3 Copy File
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action copy ^\
  --source Inbox ^\
  --destination Needs_Approval ^\
  --file test_file.md
```

**Expected:**
```
TASK_COPIED: test_file.md | From: Inbox -> To: Needs_Approval
```

**Verify:**
```bash
dir AI_Employee\vault\Needs_Approval\test_file.md
```

**Result:** ✓ PASS if file appears in destination

### 3.4 Move File
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action move ^\
  --source Needs_Approval ^\
  --destination Done ^\
  --file test_file.md
```

**Expected:**
```
TASK_MOVED: test_file.md | From: Needs_Approval -> To: Done
```

**Verify:**
```bash
dir AI_Employee\vault\Done\test_file.md
dir AI_Employee\vault\Needs_Approval\test_file.md
```

**Result:** ✓ PASS if file moved, not in original location

---

## Testing Path 4: Human Approval Skill (5 minutes)

### 4.1 Request Approval
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Send customer emails" ^\
  --reason "Testing approval workflow" ^\
  --timeout 120
```

**Expected:**
```
APPROVAL_REQUESTED: [UUID] | Action: Send customer emails
Waiting for approval (timeout: 120 seconds)...
```

Write down the UUID for next step.

### 4.2 Check Approval File
In another command prompt window:
```bash
dir AI_Employee\vault\Needs_Approval\approval_*.json
type AI_Employee\vault\Needs_Approval\approval_*.json
```

**Expected JSON structure:**
```json
{
  "id": "...",
  "action": "Send customer emails",
  "status": "PENDING",
  ...
}
```

**Result:** ✓ PASS if approval file created

### 4.3 Grant Approval (Simulate)

Edit the JSON file:
1. Find `"status": "PENDING"`
2. Change to `"status": "APPROVED"`
3. Add: `"approved_by": "tester"`
4. Save file

Return to first command prompt - it should now show:
```
APPROVAL_GRANTED: [UUID]
```

**Result:** ✓ PASS if approval was detected

### 4.4 Test Timeout

```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Test timeout" ^\
  --reason "Testing" ^\
  --timeout 5
```

Wait 10 seconds without approving. Expected:
```
APPROVAL_TIMEOUT: [UUID]
```

**Result:** ✓ PASS if timeout occurred

---

## Testing Path 5: LinkedIn-Post Skill (10 minutes)

### 5.1 Set LinkedIn Credentials

**Option A: Manual Setup**
```bash
setx LINKEDIN_EMAIL "your.email@linkedin.com"
setx LINKEDIN_PASSWORD "your_password"
```

Close and reopen Command Prompt.

**Verify:**
```bash
echo %LINKEDIN_EMAIL%
echo %LINKEDIN_PASSWORD%
```

**Result:** ✓ PASS if both show values

### 5.2 Test LinkedIn Post
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "Testing AI Employee skill integration. Post from automation system."
```

**Expected:**
```
LINKEDIN_POSTED: 2026-02-18T12:34:56 | Message length: 123
```

**Result:** ✓ PASS if you see "LINKEDIN_POSTED"

### 5.3 Verify Post Appears
1. Go to LinkedIn
2. Check your profile feed
3. Look for your test message
4. Verify content and timestamp

**Result:** ✓ PASS if post visible on LinkedIn

---

## Testing Path 6: End-to-End Workflow (15 minutes)

### 6.1 Create Complete Email Task

Create file: `AI_Employee/vault/Inbox/e2e_email_test.md`

Content:
```markdown
# Send Test Email Campaign

Send a test email to verify end-to-end workflow.

Recipients:
- test1@example.com
- test2@example.com

Subject: E2E Test Email
Body: This email verifies the complete workflow.

Success Criteria:
- [ ] Task created in Inbox
- [ ] Scheduler detected task
- [ ] Plan generated in Needs_Action
- [ ] Emails sent to both recipients
- [ ] Verification completed
- [ ] Task archived in Done
```

### 6.2 Run Scheduler
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Verify:**
- Task detected: ✓
- Plan generated: Check `Needs_Action/` folder ✓

### 6.3 Request Approval
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Send test emails to 2 recipients" ^\
  --reason "E2E workflow testing" ^\
  --timeout 300
```

### 6.4 Simulate Approval
In another window, edit the approval JSON to set status: "APPROVED"

### 6.5 Send Emails
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to test1@example.com ^\
  --subject "E2E Test Email" ^\
  --body "This email verifies the complete workflow."

python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to test2@example.com ^\
  --subject "E2E Test Email" ^\
  --body "This email verifies the complete workflow."
```

**Verify:**
- Both show "EMAIL_SENT" ✓

### 6.6 Move Task to Done
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action move ^\
  --source Inbox ^\
  --destination Done ^\
  --file e2e_email_test.md
```

**Verify all steps completed:**
- [ ] Task created ✓
- [ ] Scheduler detected ✓
- [ ] Plan generated ✓
- [ ] Approval requested ✓
- [ ] Approval granted ✓
- [ ] Emails sent ✓
- [ ] Task moved to Done ✓

**Result:** ✓ PASS if all steps complete successfully

---

## Quick Test Results Log

Use this template to record your results:

```
TEST DATE: [Date]
ENVIRONMENT: Windows 11, Python 3.10.x

PATH 1: Scheduler & Task Planner
  [ ] Scheduler single-pass: PASS/FAIL
  [ ] Plans generated: PASS/FAIL
  [ ] Plan contains details: PASS/FAIL
  Notes: _________________________________

PATH 2: Gmail-Send Skill
  [ ] Credentials set: PASS/FAIL
  [ ] Test email sent: PASS/FAIL
  [ ] Email arrives: PASS/FAIL
  [ ] Error handling: PASS/FAIL
  Notes: _________________________________

PATH 3: Vault File Manager
  [ ] List command: PASS/FAIL
  [ ] Copy command: PASS/FAIL
  [ ] Move command: PASS/FAIL
  [ ] Audit log: PASS/FAIL
  Notes: _________________________________

PATH 4: Human Approval
  [ ] Request created: PASS/FAIL
  [ ] Approval detected: PASS/FAIL
  [ ] Timeout works: PASS/FAIL
  Notes: _________________________________

PATH 5: LinkedIn-Post Skill
  [ ] Credentials set: PASS/FAIL
  [ ] Post created: PASS/FAIL
  [ ] Post visible: PASS/FAIL
  Notes: _________________________________

PATH 6: End-to-End
  [ ] Complete workflow: PASS/FAIL
  [ ] All tasks complete: PASS/FAIL
  Notes: _________________________________

OVERALL: PASS / FAIL / PARTIAL
```

---

## Troubleshooting During Testing

### Problem: "Python command not found"
```bash
# Make sure Python is in PATH
python --version
# If this fails, reinstall Python or add to PATH
```

### Problem: "Module not found" error
```bash
# Install required packages
pip install requests
pip install playwright
playwright install
```

### Problem: "EMAIL_ERROR: Authentication failed"
```bash
# Verify credentials
echo %EMAIL_ADDRESS%
echo %EMAIL_PASSWORD%

# Make sure you're using Gmail App Password, not regular password
# Get it from: https://myaccount.google.com/security
```

### Problem: "LINKEDIN_ERROR" messages
```bash
# Verify LinkedIn credentials
echo %LINKEDIN_EMAIL%
echo %LINKEDIN_PASSWORD%

# Make sure 2FA is not blocking automation
```

### Problem: Vault operations fail
```bash
# Check vault folder exists
dir AI_Employee\vault\

# Verify folder permissions
# Make sure you have read/write access to all vault folders
```

### Problem: Scheduler doesn't detect tasks
```bash
# Check vault path
dir AI_Employee\vault\Inbox\

# Verify file size (minimum 10 bytes)
dir /-N AI_Employee\vault\Inbox\

# Delete empty files and try again
```

---

## Success Criteria

Your testing is complete when:

✓ **Scheduler & Task Planner:**
- Detects tasks in Inbox
- Generates comprehensive plans
- Plans include all required sections

✓ **Gmail-Send:**
- Sends emails successfully
- Emails arrive in inbox
- Error handling works

✓ **Vault File Manager:**
- Lists files correctly
- Copies files successfully
- Moves files successfully

✓ **Human Approval:**
- Creates approval requests
- Detects approvals/rejections
- Timeouts work correctly

✓ **LinkedIn-Post:**
- Posts appear on profile
- Content is correct
- Timestamps are accurate

✓ **End-to-End:**
- Complete workflow executes
- All skills integrate properly
- Audit trail is maintained

---

## Next Steps

After passing all tests:

1. **Set up Windows Task Scheduler** (if not done)
   ```bash
   python AI_Employee/scripts/run_ai_employee.py --setup-scheduler
   ```

2. **Start monitoring** - Scheduler runs automatically every 5 minutes

3. **Create real tasks** - Use the vault to create actual work tasks

4. **Monitor logs** - Check `AI_Employee/logs/scheduler.log` regularly

5. **Expand skills** - Create additional skills for other tasks

---

**Quick Reference:**

| Test | Command | Time |
|------|---------|------|
| Scheduler | `python AI_Employee/scripts/run_ai_employee.py --once --verbose` | 30sec |
| Gmail | `python .claude/skills/gmail-send/scripts/send_email.py --to X --subject Y --body Z` | 5sec |
| Vault | `python .claude/skills/vault-file-manager/scripts/move_task.py --action list --source Inbox` | 2sec |
| LinkedIn | `python .claude/skills/linkedin-post/scripts/post_linkedin.py --message X` | 10sec |
| Approval | `python .claude/skills/human-approval/scripts/request_approval.py --action X --reason Y` | 5sec |

---

**Status:** Ready for Testing
**Last Updated:** 2026-02-18
