# Full Testing Guide - AI Employee System

Complete walkthrough to test all skills, scheduler, and integration workflows.

---

## Phase 1: Environment Setup Testing

### Test 1.1: Verify Python Environment
```bash
python --version
# Expected: Python 3.10+

pip list | find "requests"
pip list | find "playwright"
# Both should be installed
```

### Test 1.2: Verify Vault Structure
```bash
cd AI_Employee/vault
dir /s
# Should show:
# - Inbox/
# - Needs_Action/
# - Done/
# - Needs_Approval/
```

### Test 1.3: Verify Skills Exist
```bash
dir .claude/skills/
# Should show:
# - gmail-send/
# - linkedin-post/
# - vault-file-manager/
# - human-approval/
```

---

## Phase 2: Scheduler & Task Planner Testing

### Test 2.1: Start Scheduler (Single Pass)
```bash
cd E:\GH-Q4\Hackathon0-FTE
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Expected Output:**
- `[INFO] Running in single-pass mode`
- `[INFO] Detected X new task(s) in Inbox`
- `[INFO] Task planner completed: X tasks processed`
- `[INFO] Successfully processed X task(s)`

### Test 2.2: Verify Scheduler Registry Created
```bash
type AI_Employee/logs/scheduler_registry.json
```

**Expected Structure:**
- `total_runs`: integer
- `tasks_processed`: integer
- `last_run_time`: timestamp
- `health_checks`: object with status

### Test 2.3: Check Scheduler Log
```bash
type AI_Employee/logs/scheduler.log | tail -20
```

**Expected:**
- Timestamps in ISO format
- Log level indicators ([INFO], [ERROR], etc.)
- Clear status messages

---

## Phase 3: Task Planner Testing

### Test 3.1: Create Test Task - Feature Request
Create file: `AI_Employee/vault/Inbox/test_feature_task.md`

```markdown
# Test Feature: Add User Export Functionality

## Overview
Users need the ability to export their data in multiple formats.

## Requirements
- Export to CSV
- Export to JSON
- Export to Excel
- Include all user fields
- Maintain data integrity

## Success Criteria
- [ ] Export functionality added to UI
- [ ] CSV export works correctly
- [ ] JSON export is valid
- [ ] Excel export opens in Excel
- [ ] All data fields included
- [ ] No data corruption
- [ ] Performance acceptable (<5 seconds)
- [ ] Error handling for large datasets
```

### Test 3.2: Run Scheduler to Process Task
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Expected:**
- Task detected: `test_feature_task.md`
- Plan generated in `Needs_Action/`
- Named: `ActionPlan_test_feature_task_*.md`

### Test 3.3: Verify Generated Plan
```bash
dir AI_Employee/vault/Needs_Action/ActionPlan_test_feature_task*
type AI_Employee/vault/Needs_Action/ActionPlan_test_feature_task*.md
```

**Verify Plan Contains:**
- ✓ Task title extracted correctly
- ✓ Priority assigned (Low/Medium/High)
- ✓ Success criteria extracted (6+ criteria)
- ✓ Execution steps broken down (4+ steps)
- ✓ Time estimate provided
- ✓ Risk identification included

---

## Phase 4: Vault File Manager Skill Testing

### Test 4.1: List Files in Inbox
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action list ^\
  --source Inbox
```

**Expected Output:**
```
VAULT_LIST: Inbox contains 2 files:
- test_feature_task.md
- other_task.md (if exists)
```

### Test 4.2: Copy File (Safe Operation)
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action copy ^\
  --source Inbox ^\
  --destination Needs_Approval ^\
  --file test_feature_task.md
```

**Expected:**
```
TASK_COPIED: test_feature_task.md | From: Inbox -> To: Needs_Approval
```

### Test 4.3: Verify File Was Copied
```bash
dir AI_Employee/vault/Needs_Approval/
# Should now contain: test_feature_task.md
```

### Test 4.4: Move File to Done
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action move ^\
  --source Needs_Approval ^\
  --destination Done ^\
  --file test_feature_task.md
```

**Expected:**
```
TASK_MOVED: test_feature_task.md | From: Needs_Approval -> To: Done
```

### Test 4.5: Verify Move Completed
```bash
dir AI_Employee/vault/Done/
# Should contain: test_feature_task.md

dir AI_Employee/vault/Needs_Approval/
# Should NOT contain: test_feature_task.md
```

### Test 4.6: Check Vault Audit Log
```bash
type .claude/skills/vault-file-manager/logs/vault.log
```

**Expected:**
- Copy operation logged
- Move operation logged
- Timestamps for each operation
- User/source information

---

## Phase 5: Gmail-Send Skill Testing

### Test 5.1: Set Gmail Credentials
```bash
setx EMAIL_ADDRESS "your.email@gmail.com"
setx EMAIL_PASSWORD "your_app_password_16_chars"

# Verify in NEW command prompt window
echo %EMAIL_ADDRESS%
echo %EMAIL_PASSWORD%
```

**Note:** Close and reopen Command Prompt for environment variables to take effect.

### Test 5.2: Test Email to Self
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "Test Email from AI Employee" ^\
  --body "This is a test email sent from the AI Employee system."
```

**Expected Output:**
```
EMAIL_SENT: your.email@gmail.com | Subject: Test Email from AI Employee
```

**Verification:**
- Check your inbox (wait 1-2 minutes)
- Verify subject line matches exactly
- Verify body content is correct
- Verify sender is your email address

### Test 5.3: Test Email with CC
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to recipient1@example.com ^\
  --cc recipient2@example.com ^\
  --subject "Test Email with CC" ^\
  --body "Testing CC functionality"
```

**Expected:** Email received by both To and CC recipients

### Test 5.4: Test Multi-line Email Body
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "Multi-line Test" ^\
  --body "Dear User,

This is a multi-line email.

Key points:
- Point 1
- Point 2
- Point 3

Best regards,
AI Employee"
```

**Verification:**
- Formatting preserved in received email
- Bullet points display correctly
- Line breaks maintained

### Test 5.5: Check Email Logs
```bash
type .claude/skills/gmail-send/scripts/logs/actions.log
```

**Expected:**
- Timestamp of each send attempt
- Recipient email
- Subject line
- Success/Error status

### Test 5.6: Error Handling Test
```bash
# Test with invalid email
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to invalid-email-format ^\
  --subject "Test" ^\
  --body "Test"
```

**Expected:**
```
EMAIL_ERROR: Invalid email address format
```

---

## Phase 6: LinkedIn-Post Skill Testing

### Test 6.1: Set LinkedIn Credentials
```bash
setx LINKEDIN_EMAIL "your.email@linkedin.com"
setx LINKEDIN_PASSWORD "your_linkedin_password"

# Verify (in NEW command prompt)
echo %LINKEDIN_EMAIL%
echo %LINKEDIN_PASSWORD%
```

### Test 6.2: Test LinkedIn Post
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "This is a test post from the AI Employee system. Testing skill integration."
```

**Expected Output:**
```
LINKEDIN_POSTED: 2026-02-18T12:34:56 | Message length: 92
```

**Verification:**
- Check your LinkedIn profile
- Verify post appears in feed (may take a few seconds)
- Verify message content is correct
- Verify timestamp is recent

### Test 6.3: Test Post with Hashtags
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "AI Employee Test #automation #skillintegration #testing"
```

**Verification:**
- Hashtags are clickable
- Message displays correctly
- Engagement is tracked

### Test 6.4: Error Handling Test
```bash
# Test with missing environment variables
set LINKEDIN_EMAIL=
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "Test"
```

**Expected:**
```
LINKEDIN_ERROR: Authentication failed. Check LINKEDIN_EMAIL and LINKEDIN_PASSWORD
```

---

## Phase 7: Human Approval Skill Testing

### Test 7.1: Request Approval
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Send customer notification emails" ^\
  --reason "Product launch announcement" ^\
  --timeout 300
```

**Expected Output:**
```
APPROVAL_REQUESTED: [UUID] | Action: Send customer notification emails
Waiting for approval (timeout: 300 seconds)...
```

### Test 7.2: Check Approval Request File
```bash
dir AI_Employee/vault/Needs_Approval/approval_*.json
type AI_Employee/vault/Needs_Approval/approval_[UUID].json
```

**Expected JSON Structure:**
```json
{
  "id": "uuid-string",
  "action": "Send customer notification emails",
  "reason": "Product launch announcement",
  "status": "PENDING",
  "created_at": "2026-02-18T12:34:56",
  "requested_by": "system"
}
```

### Test 7.3: Grant Approval (Simulate)
Edit the approval JSON file and change:
```json
"status": "PENDING"
```
To:
```json
"status": "APPROVED",
"approved_at": "2026-02-18T12:35:00",
"approved_by": "tester"
```

### Test 7.4: Verify Approval Detected
Go back to running process - should output:
```
APPROVAL_GRANTED: [UUID] | Proceeding with action
```

### Test 7.5: Test Approval Timeout
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Test action" ^\
  --reason "Testing timeout" ^\
  --timeout 5
```

Wait 10 seconds, expect:
```
APPROVAL_TIMEOUT: [UUID] | No approval received within 5 seconds
```

### Test 7.6: Test Approval Rejection
Create approval file and set status to:
```json
"status": "REJECTED",
"rejected_by": "tester"
```

Expected:
```
APPROVAL_REJECTED: [UUID] | Action was rejected
```

---

## Phase 8: End-to-End Workflow Testing

### Test 8.1: Complete Email Campaign Workflow
**Step 1: Create email task**
```bash
# Create: AI_Employee/vault/Inbox/email_campaign_test.md
```

Content:
```markdown
# Send Product Update Email

Send emails to customers about new features.

Recipients:
- test1@example.com
- test2@example.com

Subject: New Features Available
Body: We've added Dark Mode and Export functionality!

Success Criteria:
- [ ] Email sent to all recipients
- [ ] Subject line correct
- [ ] No delivery errors
- [ ] Confirmation received
```

**Step 2: Run scheduler to detect and plan**
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Step 3: Verify plan generated**
```bash
dir AI_Employee/vault/Needs_Action/ActionPlan_email_campaign*
```

**Step 4: Request approval (optional)**
```bash
python .claude/skills/human-approval/scripts/request_approval.py ^\
  --action "Send product update emails to 2 customers" ^\
  --reason "Feature announcement"
```

**Step 5: Execute email sending**
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to test1@example.com ^\
  --subject "New Features Available" ^\
  --body "We've added Dark Mode and Export functionality!"

python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to test2@example.com ^\
  --subject "New Features Available" ^\
  --body "We've added Dark Mode and Export functionality!"
```

**Step 6: Move task to Done**
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action move ^\
  --source Inbox ^\
  --destination Done ^\
  --file email_campaign_test.md
```

**Verification:**
- ✓ Task created in Inbox
- ✓ Scheduler detected it
- ✓ Plan generated in Needs_Action
- ✓ Approval requested and granted
- ✓ Emails sent successfully
- ✓ Task moved to Done
- ✓ Audit trail in logs

### Test 8.2: Complete Feature Request Workflow
**Step 1: Create feature task**
```markdown
# Feature: Dark Mode Toggle

Add dark mode capability to the application.

Requirements:
- Toggle button in settings
- Persist preference
- Apply to all pages
- Smooth transitions

Success Criteria:
- [ ] Dark mode works on all pages
- [ ] Preference persists on refresh
- [ ] Tests pass
- [ ] No accessibility issues
- [ ] Performance acceptable
```

**Step 2: Run full workflow (scheduler -> plan -> execute)**
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Step 3: Verify plan was created**
```bash
type AI_Employee/vault/Needs_Action/ActionPlan_feature_dark_mode*.md
```

**Step 4: Post about feature on LinkedIn**
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py ^\
  --message "Excited to announce Dark Mode is now in development! Coming soon. #feature #darkmode"
```

**Step 5: Archive task**
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py ^\
  --action move ^\
  --source Inbox ^\
  --destination Done ^\
  --file feature_dark_mode_task.md
```

---

## Phase 9: Stress Testing & Edge Cases

### Test 9.1: Multiple Simultaneous Tasks
Create 5 tasks in Inbox:
```bash
type > Inbox/task1.md
type > Inbox/task2.md
type > Inbox/task3.md
type > Inbox/task4.md
type > Inbox/task5.md
```

Run scheduler:
```bash
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Expected:**
- All 5 tasks detected
- All 5 plans generated
- No conflicts or errors

### Test 9.2: Large Email Body
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "Large Email Test" ^\
  --body "This is a very long email body with lots of content... [2000+ characters]"
```

**Verify:** Email sent successfully despite large size

### Test 9.3: Special Characters in Email
```bash
python .claude/skills/gmail-send/scripts/send_email.py ^\
  --to your.email@gmail.com ^\
  --subject "Special Characters: !@#$%^&*()" ^\
  --body "Testing: café, naïve, 你好, emoji 🚀"
```

**Verify:** All characters encoded correctly

### Test 9.4: Empty Task File
```bash
type nul > Inbox/empty_task.md
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Expected:** Empty task skipped (size check: 10 bytes minimum)

### Test 9.5: Scheduler Long-Running Mode
```bash
python AI_Employee/scripts/run_ai_employee.py --verbose
```

Monitor for 10 minutes, create new task in Inbox:
```bash
type > Inbox/late_task.md
```

**Expected:**
- Scheduler detects new task within 5 minutes
- Plan generated automatically
- No crashes or hangs

(Use Ctrl+C to stop)

---

## Phase 10: Integration & Continuous Testing

### Test 10.1: Windows Task Scheduler Verification
```bash
schtasks /query /tn "AI Employee Scheduler" /v
```

**Expected:**
- Status: Ready
- Next Run Time: Within 5 minutes
- Repeat: Every 5 minutes

### Test 10.2: Check All Logs
```bash
# Scheduler log
type AI_Employee/logs/scheduler.log | tail -50

# Email log
type .claude/skills/gmail-send/scripts/logs/actions.log

# Vault log
type .claude/skills/vault-file-manager/logs/vault.log

# LinkedIn log (if exists)
type .claude/skills/linkedin-post/scripts/logs/actions.log
```

### Test 10.3: Verify Statistics
```bash
type AI_Employee/logs/scheduler_registry.json
```

Should show:
- Increasing `total_runs`
- Increasing `tasks_processed`
- Recent `last_run_time`
- All health checks passing

### Test 10.4: Test Recovery After Failure
```bash
# Stop Windows Task Scheduler
schtasks /change /tn "AI Employee Scheduler" /disable

# Wait 30 seconds, then restart it
schtasks /change /tn "AI Employee Scheduler" /enable

# Verify it recovers
python AI_Employee/scripts/run_ai_employee.py --once --verbose
```

**Expected:** System recovers gracefully without errors

---

## Complete Test Checklist

### ✓ Scheduler & Task Planner
- [ ] Scheduler starts in single-pass mode
- [ ] Scheduler detects tasks in Inbox
- [ ] Task planner generates plans
- [ ] Plans contain proper structure
- [ ] Windows Task Scheduler configured
- [ ] Long-running mode works

### ✓ Vault File Manager
- [ ] List command shows files
- [ ] Copy command works
- [ ] Move command works
- [ ] Audit log created
- [ ] File integrity maintained

### ✓ Gmail-Send Skill
- [ ] Credentials set correctly
- [ ] Email to self arrives
- [ ] CC functionality works
- [ ] Multi-line emails preserved
- [ ] Error handling works
- [ ] Logs updated

### ✓ LinkedIn-Post Skill
- [ ] Credentials set correctly
- [ ] Posts appear in feed
- [ ] Message content correct
- [ ] Hashtags work
- [ ] Error handling works

### ✓ Human Approval Skill
- [ ] Approval requests created
- [ ] Status change recognized
- [ ] Timeout works
- [ ] Rejection handling works
- [ ] Approval JSON valid

### ✓ End-to-End Workflows
- [ ] Email campaign works completely
- [ ] Feature request workflow complete
- [ ] Multiple tasks processed
- [ ] Approval gates function
- [ ] Logs audit trail maintained

---

## Test Results Template

Use this to document your test results:

```
TEST RUN: [Date/Time]
Tester: [Name]
Environment: [Windows/Linux/Mac]

SCHEDULER TESTING:
[ ] Single-pass mode: PASS/FAIL
[ ] Task detection: PASS/FAIL
[ ] Plan generation: PASS/FAIL
[ ] Registry updates: PASS/FAIL

SKILL TESTING:
[ ] Gmail-send: PASS/FAIL
[ ] LinkedIn-post: PASS/FAIL
[ ] Vault-file-manager: PASS/FAIL
[ ] Human-approval: PASS/FAIL

END-TO-END:
[ ] Email campaign: PASS/FAIL
[ ] Feature request: PASS/FAIL
[ ] Multi-task: PASS/FAIL

ISSUES FOUND:
- Issue 1: [Description]
- Issue 2: [Description]

NOTES:
[Additional observations]
```

---

## Next Steps After Testing

1. **Fix any issues found** - Create bug reports for failures
2. **Optimize performance** - Monitor logs for bottlenecks
3. **Add more skills** - Create skills for additional tasks
4. **Automate integration** - Create CI/CD pipeline for testing
5. **Production deployment** - Move to production with monitoring
6. **User training** - Train team on using the system

---

**Status:** Complete Testing Guide Ready
**Last Updated:** 2026-02-18
**Version:** 1.0
