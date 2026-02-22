# TaskAnalyzer Skill - BRONZE Tier

## Skill Overview

**TaskAnalyzer** reads tasks from `vault/Needs_Action/`, automatically classifies them by type, detects sensitive content, creates task-specific action plans, and routes sensitive tasks to approval workflow. This skill ensures tasks are properly categorized and sensitive work is handled securely.

**Category:** Task Analysis & Workflow Management
**Tier:** Bronze
**Status:** Available

---

## How It Works

### Complete Task Analysis Workflow

```
Needs_Action/
    task.md
        ↓
    [STEP 1: Read Task]
        ├─ Read markdown content
        ├─ Extract metadata and content
        └─ Prepare for analysis
        ↓
    [STEP 2: Identify Task Type]
        ├─ Check filename patterns
        ├─ Analyze content keywords
        └─ Classify as: file_drop, data_processing, documentation, etc.
        ↓
    [STEP 3: Detect Sensitivity]
        ├─ Scan for financial keywords (payment, refund, money)
        ├─ Scan for confidential keywords (secret, private, classified)
        ├─ Scan for approval keywords (approve, permission, access)
        ├─ Scan for urgent keywords (critical, emergency, asap)
        └─ Determine approval requirement
        ↓
    [STEP 4: Create Action Plan]
        ├─ Generate task-type specific steps
        ├─ Implement Ralph Wiggum Loop pattern
        ├─ Add checkpoint verification
        └─ Save to Plans/ folder
        ↓
    [STEP 5: Route if Sensitive]
        ├─ If approval_needed = TRUE
        │   └─ Copy to Pending_Approval/ folder
        │       └─ Mark [!] **PENDING APPROVAL REQUIRED**
        └─ If approval_needed = FALSE
            └─ Ready for direct processing
        ↓
    [STEP 6: Update Dashboard]
        ├─ Log analysis results
        ├─ Record task type
        ├─ Record approval status
        └─ Reference created plan
        ↓
Plans/
    └─ ActionPlan_[type]_[timestamp].md  (created)
Pending_Approval/
    └─ task.md  (copied if sensitive)
Dashboard.md
    └─ Analysis entry added
```

### Key Analysis Steps

#### Step 1: Task Type Identification
Detects task type from filename and content patterns:

| Task Type | Patterns | Use Case |
|-----------|----------|----------|
| `file_drop` | drop, upload, attachment, transfer | File uploads, attachments |
| `data_processing` | data, process, parse, import, export | Data transformation |
| `documentation` | doc, readme, guide, manual, write | Documentation tasks |
| `meeting_notes` | meeting, notes, standup, sync | Meeting summaries |
| `bug_report` | bug, issue, error, fix, crash | Bug identification |
| `feature_request` | feature, request, enhancement | Feature planning |
| `configuration` | config, setup, install, deploy | System setup |
| `unknown` | (default) | Generic tasks |

#### Step 2: Sensitivity Detection
Scans for sensitive keywords in 6 categories:

| Category | Keywords |
|----------|----------|
| **Financial** | payment, refund, money, financial, invoice, transaction, account |
| **Confidential** | confidential, secret, private, proprietary, classified, restricted |
| **Approval** | approve, permission, access, delete, authorization, grant |
| **Urgent** | critical, emergency, asap, immediately, deadline, time-sensitive |
| **Security** | password, credential, token, api key, encrypt, hash |
| **Personal** | personal, pii, ssn, phone number, email address |

#### Step 3: Ralph Wiggum Loop Pattern
Implements simple, repeating task execution pattern:

```
"I'm in danger" → "I'm in a loop" → "Simple repeating check"

For each step:
  - [ ] Execute step
  - [ ] Verify completion before next step
  Continue to next step...
```

Each step includes:
- Clear title and description
- Checkbox for completion tracking
- Verification before proceeding

#### Step 4: Action Plan Creation
Generates task-type specific action plans:

**Example: file_drop**
- Step 1: Receive File → Verify upload complete
- Step 2: Verify Integrity → Check format and size
- Step 3: Extract Metadata → Parse file headers
- Step 4: Store Appropriately → Archive in correct location

**Example: bug_report**
- Step 1: Reproduce Issue → Verify in test environment
- Step 2: Identify Root Cause → Trace code
- Step 3: Create Fix → Implement solution
- Step 4: Test Resolution → Verify fix works

---

## Supported Task Types

### 1. **file_drop**
**Use For:** File uploads, attachments, document submissions
**Steps:** Receive → Verify → Extract → Store

### 2. **data_processing**
**Use For:** Data parsing, transformation, import/export
**Steps:** Parse → Validate → Process → Report

### 3. **documentation**
**Use For:** Writing docs, guides, readme files
**Steps:** Review → Check Format → Verify → Publish

### 4. **meeting_notes**
**Use For:** Meeting summaries, action item tracking
**Steps:** Summarize → Extract Actions → Assign → Schedule

### 5. **bug_report**
**Use For:** Bug identification, troubleshooting
**Steps:** Reproduce → Identify Cause → Fix → Test

### 6. **feature_request**
**Use For:** Feature design, implementation planning
**Steps:** Analyze → Design → Implement → Test

### 7. **configuration**
**Use For:** System setup, deployment, environment config
**Steps:** Gather Settings → Configure → Validate → Document

### 8. **unknown**
**Use For:** Generic tasks not matching other types
**Steps:** Understand → Plan → Execute → Verify

---

## Sensitive Content & Approval Workflow

### Approval Routes

When sensitive keywords are detected:

```
Task Analysis
    ↓
[Sensitive Keywords Found]
    ↓
Create Action Plan
    ↓
Copy to Pending_Approval/
    ↓
Mark: [!] **PENDING APPROVAL REQUIRED**
    ↓
Await:
  ├─ Manager approval
  ├─ Security review
  └─ Compliance check
    ↓
[APPROVED] → Process normally
[REJECTED] → Archive
```

### Approval Status in Action Plan

**If Sensitive (Approval Needed):**
```markdown
🔴 **[!] PENDING APPROVAL REQUIRED**
⚠️ **AWAITING APPROVAL** - This task contains sensitive content.
Requires manager approval, security review, and/or compliance check.
```

**If Not Sensitive (No Approval Needed):**
```markdown
✅ **APPROVED FOR PROCESSING** - No sensitive content detected.
Ready to proceed with execution.
```

---

## Usage

### Manual Execution

```bash
cd AI_Employee
python .claude/skills/task-analyzer/TaskAnalyzer.py
```

### Automated (Scheduled)

```bash
# Run every 8 hours
0 */8 * * * cd /path/to/AI_Employee && python .claude/skills/task-analyzer/TaskAnalyzer.py
```

### Using in Python Code

```python
from TaskAnalyzer import TaskAnalyzer

analyzer = TaskAnalyzer(base_path="/path/to/AI_Employee")
result = analyzer.analyze_all_tasks()

# Access results
print(f"Analyzed: {result['analyzed']} tasks")
print(f"Approval needed: {result['approval_required']} tasks")
for task in result['results']:
    print(f"  - {task['filename']}: {task['task_type']} ({task['approval_needed']})")
```

---

## Input Requirements

### Folder Structure
```
vault/
├── Needs_Action/           ← Input: .md files to analyze
├── Plans/                  ← Output: Action plans created
├── Pending_Approval/       ← Output: Sensitive tasks copied
└── Dashboard.md            ← Output: Analysis results logged
```

### File Format

Markdown files in `vault/Needs_Action/`:

```markdown
---
type: feature_request (optional - helps with classification)
priority: HIGH (optional)
---

# Feature Request: Dark Mode Support

Add dark theme option to the application.

## Requirements

- Respect system preference
- Persist user selection
- Apply to all components

## Details

This feature would improve usability for users in low-light environments.
```

---

## Output Provided

### 1. Console Output

```
🚀 TaskAnalyzer Skill Execution
============================================================
🔍 [ANALYZE] 2026-02-20 22:55:00 - Task type identified: feature_request
✅ [OK] 2026-02-20 22:55:00 - No sensitive keywords detected
🔄 [LOOP] 2026-02-20 22:55:00 - Created action plan: ActionPlan_feature_request_20260220_225500.md
✅ [OK] 2026-02-20 22:55:00 - Dashboard updated

📊 Analysis Summary
============================================================
✅ Total tasks analyzed: 15
⚠️  Tasks requiring approval: 3
❌ Errors encountered: 0
```

### 2. Action Plan Files

Created in `vault/Plans/ActionPlan_[type]_[timestamp].md`:

```markdown
# Action Plan: Feature Request

**Created:** 2026-02-20 22:55:00
**Source File:** feature_request.md
**Task Type:** feature_request
**Approval Required:** NO

## Task Workflow

### Ralph Wiggum Loop (Step-by-Step Process)

**Step 1: Analyze Requirement**
- [ ] Understand scope and acceptance criteria
- [ ] Verify Analyze Requirement complete before next step

**Step 2: Design Solution**
- [ ] Plan implementation approach and architecture
- [ ] Verify Design Solution complete before next step

**Step 3: Implement Feature**
- [ ] Write code following design specifications
- [ ] Verify Implement Feature complete before next step

**Step 4: Test Thoroughly**
- [ ] Verify all requirements and edge cases
- [ ] Verify Test Thoroughly complete before next step

## Checkpoint Verification
- [ ] All steps completed
- [ ] Each step marked complete
- [ ] No blockers remaining
- [ ] Quality review passed

## Approval Status
✅ **APPROVED FOR PROCESSING** - No sensitive content detected.
```

### 3. Sensitive Task Routing

If sensitive keywords detected, file copied to:
```
vault/Pending_Approval/[filename]
```

With status marked as:
```markdown
🔴 **[!] PENDING APPROVAL REQUIRED**
```

### 4. Dashboard Updates

Entry added to `vault/Dashboard.md`:

```markdown
## TaskAnalyzer Execution Log
- Analyzed: feature_request.md - Type: feature_request - Approval: NO | Plan: ActionPlan_feature_request_...
- Analyzed: payment_request.md - Type: financial - Approval: YES | Plan: ActionPlan_financial_... | Routed: Pending_Approval/
- Analyzed: meeting_notes.md - Type: meeting_notes - Approval: YES | Plan: ActionPlan_meeting_notes_...
```

---

## Output Structure (Return Dictionary)

```python
{
    'status': 'COMPLETE',
    'analyzed': 15,
    'approval_required': 3,
    'errors': 0,
    'results': [
        {
            'success': True,
            'filename': 'feature_request.md',
            'task_type': 'feature_request',
            'approval_needed': False,
            'sensitive_keywords': [],
            'plan_filename': 'ActionPlan_feature_request_20260220_225500.md'
        },
        {
            'success': True,
            'filename': 'payment_request.md',
            'task_type': 'financial',
            'approval_needed': True,
            'sensitive_keywords': ['payment (financial)', 'money (financial)'],
            'plan_filename': 'ActionPlan_financial_20260220_225505.md'
        }
    ],
    'log': [
        '[ANALYZE] 2026-02-20 22:55:00 - Task type identified: feature_request',
        '[OK] 2026-02-20 22:55:00 - No sensitive keywords detected',
        '[LOOP] 2026-02-20 22:55:00 - Created action plan: ActionPlan_feature_request_...'
    ]
}
```

---

## Key Methods

### `analyze_file_type(filename, content)`
Identifies task type from filename and content patterns
- Returns: task type string (file_drop, bug_report, etc.)

### `check_approval_needed(filename, content)`
Detects sensitive keywords requiring approval
- Returns: (approval_boolean, list_of_keywords)

### `ralph_wiggum_loop(steps)`
Creates simple repeating task execution pattern
- Input: List of (title, description) tuples
- Returns: Formatted markdown with checkboxes

### `create_action_plan(filename, task_type, content, approval_needed)`
Generates task-type specific action plan
- Returns: plan filename

### `move_to_pending_approval(filename)`
Copies sensitive task to approval workflow
- Returns: success boolean

### `update_dashboard(filename, task_type, approval_needed, plan_filename)`
Logs analysis results to dashboard
- Returns: success boolean

### `analyze_task(filename)`
Complete analysis workflow for single file
- Returns: results dictionary

### `analyze_all_tasks()`
Analyze all tasks in Needs_Action folder
- Returns: detailed results with summary

---

## Log Status Codes

| Code | Emoji | Meaning |
|------|-------|---------|
| `[ANALYZE]` | 🔍 | Task type identified |
| `[SENSITIVE]` | ⚠️ | Sensitive keyword found |
| `[OK]` | ✅ | No sensitive content |
| `[LOOP]` | 🔄 | Ralph Wiggum Loop created |
| `[APPROVE]` | 📋 | Routed to approval |
| `[ERROR]` | ❌ | Operation failed |
| `[WARN]` | ⚠️ | Warning (non-blocking) |
| `[INFO]` | ℹ️ | Informational |

---

## Integration Notes

- **Works with:** BasicFileHandler, ProcessIncomingItem, Approval workflow
- **Reads from:** vault/Needs_Action/
- **Writes to:** vault/Plans/, vault/Pending_Approval/, vault/Dashboard.md
- **Frequency:** Can run multiple times safely (idempotent)
- **Sensitive Content:** Automatically detected and routed
- **Approval Workflow:** Integrates with Pending_Approval folder

---

## Complete Workflow Example

### Scenario: Payment Request Task

**Input:** `payment_request.md` in Needs_Action/

```markdown
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

**Processing:**
1. ✅ Read file
2. 🔍 Identify type: financial
3. ⚠️ Detect keywords: "payment" (financial), "amount" (financial)
4. 🔄 Create Ralph Wiggum Loop with 4 financial steps
5. 📋 Mark [!] **PENDING APPROVAL REQUIRED**
6. 📋 Copy to Pending_Approval/payment_request.md
7. 📊 Update Dashboard

**Output:**
- ✅ Plan: ActionPlan_financial_20260220_225500.md
- ✅ Copied to: Pending_Approval/payment_request.md
- ✅ Dashboard: "Analyzed: payment_request.md - Type: financial - Approval: YES"

---

## Best Practices

1. **Run Regularly** - Schedule every 8-12 hours
2. **Review Approvals** - Check Pending_Approval folder regularly
3. **Process Safely** - Follow Ralph Wiggum Loop for consistency
4. **Track Progress** - Use checkboxes to mark completion
5. **Document Issues** - Note any blockers in action plans
6. **Verify Classification** - Review task types for accuracy

---

## Troubleshooting

**Q: Task type not detected correctly?**
A: Add explicit metadata or keywords to filename/content

**Q: Sensitive keywords missed?**
A: Check keyword list, add custom patterns if needed

**Q: Files not routed to Pending_Approval?**
A: Verify sensitive keywords match patterns (case-insensitive)

**Q: Dashboard not updated?**
A: Verify Dashboard.md exists and has appropriate sections

---

## Version History

- **v1.0** (2026-02-20) - Initial release
  - Task type identification (8 types)
  - Sensitive keyword detection (6 categories)
  - Ralph Wiggum Loop pattern implementation
  - Task-specific action plan generation
  - Approval routing for sensitive content
  - Dashboard integration

---

**Skill Type:** Analysis | **Execution Mode:** Standalone/Scheduled | **Requires Approval:** NO (but identifies tasks that do)
