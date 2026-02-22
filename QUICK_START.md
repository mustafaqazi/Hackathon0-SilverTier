# Quick Start - Bronze Tier Agent Skills

## Skills Ready! ✅

Two powerful agent skills are now available for immediate use.

---

## Skill Invocation

### @Basic File Handler
**Purpose:** Read, summarize, and organize task files

**Quick Start:**
```bash
cd AI_Employee
python -m skills.basic_file_handler
```

**What It Does:**
1. Finds all .md files in vault/Needs_Action/
2. Reads and summarizes each file
3. Creates Plan.md with checkboxes
4. Verifies Company_Handbook.md rules
5. Moves files to vault/Done/
6. Logs full paths of all operations

**Output:**
- Generated files: `vault/Plans/Plan_*.md`
- Processed files: `vault/Done/*.md`

---

### @Task Analyzer
**Purpose:** Analyze tasks, identify types, route approvals

**Quick Start:**
```bash
cd AI_Employee
python -m skills.task_analyzer
```

**What It Does:**
1. Finds all .md files in vault/Needs_Action/
2. Identifies task type (8 types)
3. Detects sensitive keywords
4. Creates detailed action plan
5. Uses Ralph Wiggum Loop for multi-step tasks
6. Routes sensitive tasks to vault/Pending_Approval/

**Output:**
- Generated files: `vault/Plans/ActionPlan_*.md`
- Sensitive routing: `vault/Pending_Approval/*.md`

---

## Task Types Detected by @Task Analyzer

| Type | Keywords |
|------|----------|
| file_drop | drop, upload |
| data_processing | data, process |
| documentation | doc, readme |
| meeting_notes | meeting, notes |
| bug_report | bug, issue |
| feature_request | feature, request |
| configuration | config, setup |
| unknown | (unclassified) |

---

## Sensitive Keywords Detected

These keywords trigger approval routing:
- **Financial:** payment, refund, money, financial
- **Security:** confidential, secret, private, secure
- **Access:** approve, permission, access, delete
- **Urgency:** critical, urgent, emergency

---

## Folder Structure

```
vault/
├── Inbox/          ← Put new items here
├── Needs_Action/   ← Put tasks to process here
├── Done/           ← Processed files go here
├── Pending_Approval/  ← Sensitive tasks routed here
└── Plans/          ← Generated plans appear here
```

---

## Typical Workflow

### Option 1: Quick Analysis → Processing

```bash
# Step 1: Analyze (categorize + detect sensitivity)
python -m skills.task_analyzer

# Step 2: If approved, process files
python -m skills.basic_file_handler
```

### Option 2: Direct Processing

```bash
# Just read and process files
python -m skills.basic_file_handler
```

---

## Example Usage Scenarios

### Scenario A: Process a Documentation Request

1. **File Created:** `vault/Needs_Action/api_docs_task.md`
2. **Run Analyzer:** `python -m skills.task_analyzer`
   - Type: documentation
   - Approval: Not needed
   - Plan: Created in Plans/
3. **Run Handler:** `python -m skills.basic_file_handler`
   - Summarized
   - Plan with checkboxes created
   - Moved to Done/

**Result:** Task processed and organized ✅

---

### Scenario B: Process a Payment Request

1. **File Created:** `vault/Needs_Action/payment_request.md`
2. **Run Analyzer:** `python -m skills.task_analyzer`
   - Type: feature_request
   - Approval: NEEDED (contains "payment")
   - Plan: Created in Plans/
   - File: Copied to Pending_Approval/
3. **Get Manager Approval**
4. **Move to Needs_Action:** (after approval)
5. **Run Handler:** `python -m skills.basic_file_handler`
   - Processed and organized

**Result:** Sensitive task properly routed and approved ✅

---

### Scenario C: Multi-Step Complex Task

1. **File Created:** `vault/Needs_Action/complex_project.md`
2. **Run Analyzer:** `python -m skills.task_analyzer`
   - Type: feature_request
   - Ralph Wiggum Loop activated
   - Steps: Analyze → Design → Implement → Test
   - Plan: Created with all steps

**Result:** Complex task broken into manageable steps ✅

---

## Sample Output

### @Basic File Handler Output
```
[START] Processing: documentation_task.md
[OK] Company_Handbook.md loaded - Rules verified
[OK] Read file: vault/Needs_Action/documentation_task.md
[OK] Content summarized
[OK] Plan created: vault/Plans/Plan_documentation_task_20260215.md
[OK] Moved to Done: vault/Done/documentation_task.md
[SUCCESS] File processed successfully!
```

### @Task Analyzer Output
```
[START] Analyzing task: payment_request.md
[OK] File read: vault/Needs_Action/payment_request.md
[ANALYZE] Task type identified: feature_request
[SENSITIVE] Found sensitive keyword: 'payment'
[LOOP] Entering Ralph Wiggum Loop for multi-step task
[LOOP-1] Processing: Analyze requirement
[LOOP-2] Processing: Design solution
[LOOP-3] Processing: Implement feature
[LOOP-4] Processing: Test thoroughly
[OK] Action plan created: vault/Plans/ActionPlan_feature_request.md
[OK] Copied to Pending_Approval: vault/Pending_Approval/payment_request.md
[SUCCESS] Analysis complete!
```

---

## Ralph Wiggum Loop Explained

Simple repeating pattern for complex tasks:

```
Task in
  ↓
Step 1: Check
  ↓
Step 2: Check
  ↓
Step 3: Check
  ↓
Step 4: Check
  ↓
Done ✓
```

Each step is verified before proceeding.
Output format: Interactive checklist.

---

## File Naming Convention

### Plans Generated by @Basic File Handler
```
Plan_{original_filename}_{timestamp}.md
Example: Plan_api_docs_task_20260215_124923.md
```

### Plans Generated by @Task Analyzer
```
ActionPlan_{task_type}_{timestamp}.md
Example: ActionPlan_feature_request_20260215_124914.md
```

---

## Troubleshooting Quick Tips

| Issue | Solution |
|-------|----------|
| Files not found | Ensure they're in `vault/Needs_Action/` |
| .md extension not recognized | Verify files end with `.md` |
| Handbook not loading | Check `vault/Company_Handbook.md` exists |
| Approval not triggered | Check content for sensitive keywords |
| Plans not generated | Verify `vault/Plans/` folder exists |

---

## Key Features Summary

### @Basic File Handler ✅
- ✅ Reads .md files
- ✅ Summarizes content
- ✅ Creates plans with checkboxes
- ✅ Verifies handbook rules
- ✅ Moves files to Done
- ✅ Detailed logging

### @Task Analyzer ✅
- ✅ Identifies task types
- ✅ Detects sensitive keywords
- ✅ Creates action plans
- ✅ Implements Ralph Wiggum Loop
- ✅ Routes to approvals
- ✅ Comprehensive analysis

---

## Full Documentation

For detailed information:
- **Usage Guide:** See `SKILL_USAGE_GUIDE.md`
- **Deployment Status:** See `SKILLS_DEPLOYMENT_STATUS.md`
- **Company Info:** See `vault/Company_Handbook.md`
- **Skills Inventory:** See `vault/SKILLS.md`

---

## Ready to Use! 🚀

Both skills are fully tested and ready for production.

**Start using them now:**
```bash
cd AI_Employee
python -m skills.task_analyzer    # Analyze first
python -m skills.basic_file_handler  # Then process
```

---

Generated: 2026-02-15
Bronze Tier Version: v1.0
Status: ✅ PRODUCTION READY
