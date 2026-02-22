# TaskAnalyzer Skill - Quick Start Guide

## What It Does

TaskAnalyzer automatically:
1. 🔍 **Identifies task types** (8 different types)
2. ⚠️ **Detects sensitive content** (financial, confidential, etc.)
3. 🔄 **Creates action plans** with Ralph Wiggum Loop pattern
4. 📋 **Routes to approval** if sensitive
5. 📊 **Updates Dashboard** with results

---

## Quick Setup

### 1. **Folder Structure**
```
AI_Employee/
├── vault/
│   ├── Needs_Action/        ← Input: .md files
│   ├── Plans/               ← Output: Action plans
│   ├── Pending_Approval/    ← Output: Sensitive tasks
│   └── Dashboard.md         ← Gets updated
├── .claude/
│   └── skills/
│       └── task-analyzer/
│           ├── TaskAnalyzer.py
│           ├── SKILL.md
│           └── QUICK_START.md
```

### 2. **Run the Skill**
```bash
cd AI_Employee
python .claude/skills/task-analyzer/TaskAnalyzer.py
```

### 3. **Check Results**
- ✅ Plans in `vault/Plans/`
- ✅ Sensitive tasks in `vault/Pending_Approval/`
- ✅ Dashboard updated with analysis

---

## The 8 Task Types

| Type | Patterns | Action Steps |
|------|----------|--------------|
| 📁 **file_drop** | drop, upload, attachment | Receive → Verify → Extract → Store |
| 📊 **data_processing** | data, process, parse, import | Parse → Validate → Process → Report |
| 📄 **documentation** | doc, readme, guide, manual | Review → Check Format → Verify → Publish |
| 📝 **meeting_notes** | meeting, notes, standup, sync | Summarize → Extract → Assign → Schedule |
| 🐛 **bug_report** | bug, issue, error, fix, crash | Reproduce → Identify → Fix → Test |
| 💡 **feature_request** | feature, request, enhancement | Analyze → Design → Implement → Test |
| ⚙️ **configuration** | config, setup, install, deploy | Gather → Configure → Validate → Document |
| ❓ **unknown** | (default for any other task) | Understand → Plan → Execute → Verify |

---

## Sensitive Keywords (Auto-Detected)

If found in file, task needs **approval**:

**Financial:** payment, refund, money, invoice, transaction, account
**Confidential:** secret, private, classified, restricted, proprietary
**Approval:** approve, permission, access, delete, authorize
**Urgent:** critical, emergency, asap, immediately, deadline
**Security:** password, credential, token, api key, encrypt
**Personal:** personal, pii, ssn, phone number, email address

---

## The Ralph Wiggum Loop

Simple repeating pattern for each task:

```
"I'm in danger" → "I'm in a loop" → "Simple repeating check"

For each step:
✅ Do the step
✅ Verify it's done
✅ Move to next step
```

Example (feature_request):
```markdown
**Step 1: Analyze Requirement**
- [ ] Understand scope and acceptance criteria
- [ ] Verify Analyze Requirement complete

**Step 2: Design Solution**
- [ ] Plan implementation approach
- [ ] Verify Design Solution complete

**Step 3: Implement Feature**
- [ ] Write code following design
- [ ] Verify Implement Feature complete

**Step 4: Test Thoroughly**
- [ ] Verify all requirements and edge cases
- [ ] Verify Test Thoroughly complete
```

---

## What Gets Created

### Action Plan Example
```
vault/Plans/ActionPlan_feature_request_20260220_225500.md
├── Task Overview (title, type, priority)
├── Ralph Wiggum Loop
│   ├── Step 1: Analyze Requirement
│   ├── Step 2: Design Solution
│   ├── Step 3: Implement Feature
│   └── Step 4: Test Thoroughly
├── Checkpoint Verification
│   ├── [ ] All steps completed
│   ├── [ ] Quality review passed
│   └─ [ ] Ready for approval
└── Status: READY FOR EXECUTION or PENDING APPROVAL
```

### Approval Status

**If Sensitive (Requires Approval):**
```
🔴 **[!] PENDING APPROVAL REQUIRED**
⚠️ Awaiting manager approval, security review, compliance check
```

**If Not Sensitive (Ready to Process):**
```
✅ **APPROVED FOR PROCESSING**
Ready to proceed with execution
```

---

## Dashboard Entry Example

After running, your Dashboard shows:

```markdown
## TaskAnalyzer Execution Log
- Analyzed: feature_request.md - Type: feature_request - Approval: NO | Plan: ActionPlan_feature_request_...
- Analyzed: payment_request.md - Type: financial - Approval: YES | Plan: ActionPlan_financial_...
```

---

## Example: Analyze a Payment Request

### 1. Create File
```markdown
vault/Needs_Action/payment_request_abc.md
---
type: financial
priority: CRITICAL
---

# Payment Request

Client: ABC Corporation
Amount: ₹150,000
Invoice: INV-2026-001

Processing payment for completed project.
```

### 2. Run Skill
```bash
python TaskAnalyzer.py
```

### 3. Processing Steps
```
🔍 Task type: financial
⚠️ Sensitive keywords found: payment, amount
🔄 Created action plan with 4 financial steps
📋 Routed to Pending_Approval (needs approval)
📊 Dashboard updated
```

### 4. Results
```
vault/Plans/ActionPlan_financial_20260220_225500.md
  ├─ Summary
  ├─ Ralph Wiggum Loop (4 steps)
  └─ Status: [!] PENDING APPROVAL REQUIRED

vault/Pending_Approval/payment_request_abc.md
  └─ Copy for approval process

Dashboard Entry:
  "Analyzed: payment_request_abc.md - Type: financial - Approval: YES"
```

---

## Run Manually
```bash
python .claude/skills/task-analyzer/TaskAnalyzer.py
```

## Run on Schedule

### Windows (Task Scheduler)
```
Schedule: Every 8 hours
Command: python TaskAnalyzer.py
```

### Linux/Mac (Cron)
```bash
0 */8 * * * cd /path/to/AI_Employee && python TaskAnalyzer.py
```

---

## File Patterns

TaskAnalyzer looks at **filename and content**:

```
Filename: feature_request_dark_mode.md
           ↓
Found pattern: "feature", "request"
           ↓
Task Type: feature_request ✅

---

Content: "This is critical... payment needed..."
           ↓
Found patterns: "critical", "payment"
           ↓
Task Type: financial (from content)
Approval: YES (sensitive keywords) ✅
```

---

## Status Codes in Logs

```
🔍 [ANALYZE] - Task type identified
⚠️  [SENSITIVE] - Sensitive keyword found
✅ [OK] - No sensitive content
🔄 [LOOP] - Ralph Wiggum Loop created
📋 [APPROVE] - Routed to Pending_Approval
❌ [ERROR] - Operation failed
⚠️  [WARN] - Warning (non-blocking)
ℹ️  [INFO] - Information message
```

---

## Common Tasks

### ✨ Analyze Single File
1. Create `.md` in `vault/Needs_Action/`
2. Run: `python TaskAnalyzer.py`
3. Check `vault/Plans/` for plan
4. Check `vault/Pending_Approval/` if sensitive

### 🔄 Batch Analyze Multiple Files
1. Add multiple `.md` files to `vault/Needs_Action/`
2. Run skill once - analyzes all
3. Plans created for each
4. Sensitive ones copied to Pending_Approval

### ✅ Follow Action Plan
1. Open action plan file
2. Work through Ralph Wiggum Loop steps
3. Check off [ ] as you complete each step
4. Verify before moving to next step

### 🔐 Handle Sensitive Tasks
1. Review in `vault/Pending_Approval/`
2. Get appropriate approvals (manager, security, compliance)
3. Move to Done when approved
4. Log decision in Dashboard

---

## Approval Workflow

```
Task with sensitive keywords
        ↓
Analysis: "approval_needed = YES"
        ↓
Copy to Pending_Approval/
        ↓
Action Plan marked: [!] PENDING APPROVAL REQUIRED
        ↓
Wait for:
  - Manager approval
  - Security review
  - Compliance check
        ↓
[APPROVED] → Process normally
[REJECTED] → Archive
```

---

## Metadata Fields (Optional)

Add to YAML frontmatter to help classification:

```yaml
---
type: feature_request  (Optional - helps classification)
priority: HIGH         (Optional - for reference)
created: 2026-02-20   (Optional - for tracking)
---
```

---

## Output Details

### Console Output Shows
- ✅ Task types identified
- ✅ Sensitive keywords found
- ✅ Action plans created
- ✅ Approval routing
- ✅ Summary statistics

### Files Created
- Plans: `ActionPlan_[type]_[timestamp].md`
- Approval: `[filename]` copied to Pending_Approval/
- Dashboard: Entry with analysis results

---

## Integration

Works with:
- **ProcessIncomingItem** - Summarizes tasks
- **BasicFileHandler** - Creates detailed plans
- **Approval Workflow** - Routes sensitive work
- **Dashboard** - Tracks all analysis

---

## Best Practices

1. ✅ Run on regular schedule (every 8 hours)
2. ✅ Review created action plans before starting
3. ✅ Check Pending_Approval folder for sensitive tasks
4. ✅ Update checkboxes in plans as you work
5. ✅ Document any blockers or issues
6. ✅ Get proper approvals for sensitive tasks

---

## Troubleshooting

**Q: Task type not detected?**
A: Add keywords to filename or content, or use metadata field

**Q: Sensitive task not routed?**
A: Check if keywords match list (payment, confidential, etc.)

**Q: Action plan not created?**
A: Check Plans/ folder permissions, verify Dashboard.md exists

**Q: Dashboard not updated?**
A: Verify Dashboard.md has "## Recent Activity" or "## TaskAnalyzer Execution Log" section

---

**Version:** 1.0 | **Tier:** Bronze | **Status:** Ready to Use ✅
