# Approval Workflow - How to Use

**Status:** ✅ **READY FOR APPROVAL**
**Date:** 2026-02-20

---

## 📋 Current Approval Status

### Pending Approvals

```
Pending Approval Items: 12
  - APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161143.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161143.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161143.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161356.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161356.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161414.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161414.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161414.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161430.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161430.md
  - APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161430.md

Already Approved: 3
  - APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356_APPROVED.md ✓
  - APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161356_APPROVED.md ✓
  - APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161356_APPROVED.md ✓
```

---

## 🎯 How to Approve an Action

### Step 1: Review Pending Request

Open: `vault/Pending_Approval/APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356.md`

Read:
- [ ] Request ID
- [ ] Email recipient
- [ ] Email subject
- [ ] Number of action items
- [ ] Source plan/log

Example content:
```
Request ID: EMAIL_ai-employee_0_20260220_161356
Type: Email Send
Recipient: ai-employee@example.com
Subject: Action Summary: Reasoning Plan: ActionPlan: Add Dark Mode Toggle Feature
Action Items: 61
```

### Step 2: Verify Approval Checklist

Before approving, confirm:

- [ ] Recipient email address is correct: ai-employee@example.com
- [ ] Subject line is appropriate
- [ ] All action items are accurate (61 items)
- [ ] No sensitive data will be exposed
- [ ] Email timing is appropriate
- [ ] No duplicate sends
- [ ] Recipient has permission to receive this

### Step 3: Create Approval File

**File to Create:**
```
vault/Approved/APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356_APPROVED.md
```

**Naming Format:**
```
APPROVAL_REQUEST_[REQUEST_ID]_APPROVED.md
```

**Content Template:**
```markdown
# Approval Granted

**Request ID:** EMAIL_ai-employee_0_20260220_161356
**Type:** Email Send
**Approved By:** [Your Name]
**Approved At:** [Date and Time]
**Reason:** [Brief reason for approval]

---

## Approval Verification

- ✓ Recipient email is correct
- ✓ Subject line is appropriate
- ✓ All action items are accurate
- ✓ No sensitive data exposed
- ✓ Email timing is appropriate
- ✓ No duplicate sends
- ✓ Recipient has permission

Status: ✅ APPROVED
```

### Step 4: Run ApprovalChecker to Trigger

```bash
python -m skills.approval_checker
```

ApprovalChecker will:
1. Detect your approval file
2. Match it with the pending request
3. Trigger the email send action
4. Archive files to Completed/
5. Log the action

---

## 🚫 How to Reject an Action

### Option: Reject Instead of Approve

If you find issues with an approval request:

**File to Create:**
```
vault/Rejected/APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356_REJECTED.md
```

**Content:**
```markdown
# Approval Rejected

**Request ID:** EMAIL_ai-employee_0_20260220_161356
**Type:** Email Send
**Rejected By:** [Your Name]
**Rejected At:** [Date and Time]
**Reason:** [Clear reason for rejection]

---

## Rejection Details

Issue Found: [Describe the issue]

How to Fix: [Suggest fixes]

Resubmit: [Instructions for resubmission]
```

Then:
- Request is marked as rejected
- Can be corrected and resubmitted
- Not moved to Completed/

---

## 📊 Example: Approve Multiple Requests

### Scenario: Batch Approve 3 Similar Requests

**Request 1:** EMAIL_ai-employee_0_20260220_161414
**Request 2:** EMAIL_ai-employee_1_20260220_161414
**Request 3:** EMAIL_ai-employee_2_20260220_161414

### Steps:

1. **Review All 3**
   - All for same action type (email send)
   - All to same recipient (ai-employee@example.com)
   - All appear correct

2. **Create 3 Approval Files**
   ```
   vault/Approved/APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161414_APPROVED.md
   vault/Approved/APPROVAL_REQUEST_EMAIL_ai-employee_1_20260220_161414_APPROVED.md
   vault/Approved/APPROVAL_REQUEST_EMAIL_ai-employee_2_20260220_161414_APPROVED.md
   ```

3. **Run ApprovalChecker**
   ```bash
   python -m skills.approval_checker
   ```

4. **Result**
   - All 3 actions triggered
   - All archived to Completed/
   - All logged in audit trail

---

## 🔄 Complete Approval Workflow

### Flow Diagram

```
1. ReasoningPlanner
   ↓ Generates plans with actions

2. EmailSender
   ↓ Creates emails from plans

3. ApprovalChecker (Step 1)
   ↓ Creates approval requests
   ↓ Saves to Pending_Approval/

4. HUMAN DECISION
   ↓ Reviews request file
   ↓ Checks approval checklist
   ↓ Creates APPROVED file
   ↓ Saves to Approved/

5. ApprovalChecker (Step 2)
   ↓ Detects approval file
   ↓ Matches with pending request
   ↓ Triggers action (send email)
   ↓ Archives to Completed/

6. Email MCP Server
   ↓ Executes approved action
   ↓ Sends email
   ↓ Complete ✓
```

---

## 📝 Request ID Format

Each approval request has a unique ID:

```
EMAIL_ai-employee_0_20260220_161356
 ↑     ↑             ↑        ↑
 │     │             │        └─ Timestamp (HHmmss)
 │     │             └─────────── Date (YYYYMMDD)
 │     └───────────────────────── Index (0, 1, 2...)
 └────────────────────────────── Action Type (EMAIL)
```

### Format Rule

**Approval file name must include:**
- Exact Request ID
- Followed by _APPROVED or _REJECTED
- File extension .md

Example:
```
✓ APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356_APPROVED.md
✗ APPROVAL_REQUEST_EMAIL_ai-employee_0_APPROVED.md (missing ID)
✗ APPROVAL_REQUEST_EMAIL_ai-employee_0_20260220_161356_APPROVED.txt (wrong extension)
```

---

## 📊 Checking Status

### View Pending Approvals

```bash
ls vault/Pending_Approval/ | grep APPROVAL_REQUEST
```

### View Approved Items

```bash
ls vault/Approved/ | grep APPROVAL_REQUEST
```

### View Completed Actions

```bash
ls vault/Completed/ | grep APPROVAL_REQUEST
```

### View Rejection

```bash
ls vault/Rejected/ | grep APPROVAL_REQUEST
```

### Check Approval Log

```bash
cat vault/approval_check_log_*.json | jq .
```

---

## ⚡ Quick Approval Script

### To quickly approve all pending requests of type EMAIL:

1. **List pending:**
   ```bash
   ls vault/Pending_Approval/APPROVAL_REQUEST_EMAIL*
   ```

2. **For each file, extract ID:**
   ```bash
   grep "Request ID:" vault/Pending_Approval/APPROVAL_REQUEST_EMAIL_*.md | head -1
   # Output: Request ID: EMAIL_ai-employee_0_20260220_161356
   ```

3. **Create approval file with that ID**

4. **Run ApprovalChecker**

---

## 🔐 Security Reminders

✓ **Never approve without reviewing**
  - Always check email recipient
  - Verify subject line
  - Confirm timing

✓ **Check for sensitive data**
  - No passwords in request
  - No credit cards
  - No personal information

✓ **Verify recipient**
  - Is email address correct?
  - Does recipient need this?
  - Is it the right timing?

✓ **Keep approval file**
  - Save for audit trail
  - Proof of decision
  - Compliance record

---

## ❓ FAQ

### Q: What if I don't approve?
**A:** Approval request stays in Pending_Approval/ indefinitely. After 7 days, it auto-expires (future feature).

### Q: Can I change my approval?
**A:** Move from Approved/ back to Pending_Approval/ and modify. Or reject and resubmit.

### Q: What happens to rejected requests?
**A:** Moved to Rejected/ folder. Can be fixed and resubmitted as new request.

### Q: How long does execution take?
**A:** ~1-2 seconds from approval detection to action trigger.

### Q: Can I batch approve?
**A:** Yes! Create multiple APPROVED files, then run ApprovalChecker once.

### Q: Is there a limit on pending approvals?
**A:** No limit, but it's better to keep them moving. Review and approve regularly.

---

## 🎯 Next Actions

### To Complete Approval Workflow:

1. **Review 12 Pending Requests**
   ```bash
   ls vault/Pending_Approval/APPROVAL_REQUEST*
   ```

2. **Choose to Approve or Reject Each**

3. **For Each Approval, Create APPROVED File**
   ```
   vault/Approved/APPROVAL_REQUEST_[ID]_APPROVED.md
   ```

4. **Run ApprovalChecker to Trigger**
   ```bash
   python -m skills.approval_checker
   ```

5. **Start Email MCP Server (when ready to send)**
   ```bash
   cd email-mcp-server
   npm start
   ```

6. **Emails Delivered**
   - All approved actions execute
   - Complete audit trail maintained

---

## 📞 Support

### If You Need to:

**Check a specific request:**
```bash
cat vault/Pending_Approval/APPROVAL_REQUEST_EMAIL_ai-employee_0_*.md
```

**See all pending:**
```bash
ls -lah vault/Pending_Approval/
```

**See approval status:**
```bash
cat vault/approval_check_log_*.json
```

**Review completed actions:**
```bash
ls vault/Completed/APPROVAL_REQUEST*
```

---

## ✨ Summary

**Approval Workflow:**
1. ✅ ApprovalChecker creates requests
2. ⏳ Human reviews and decides
3. ✅ ApprovalChecker detects approval
4. ✅ Action triggered automatically
5. ✅ Complete audit trail maintained

**Your Next Step:**
Create APPROVED files for the 12 pending requests you want to approve!

---

**Instructions Version:** 1.0
**Date:** 2026-02-20
**Status:** 🟢 Ready to Use

Good luck with your approvals! 🔒✨
