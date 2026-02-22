# Bronze Tier Agent Skills Usage Guide

## Overview
Two core Agent Skills are now available for the Bronze Tier AI Employee system.

---

## Skill 1: Basic File Handler

**Location:** `skills/basic_file_handler.py`

### Purpose
Processes markdown files from the Needs_Action folder, summarizes content, creates action plans, and moves completed files to Done folder.

### Features
✅ Reads any .md file from /Needs_Action
✅ Summarizes content with headers and key points
✅ Creates Plan.md with simple checkboxes
✅ Verifies Company_Handbook.md rules before action
✅ Moves processed files to /Done folder
✅ Detailed success logging with full paths

### Usage

**As a Python Module:**
```python
from skills.basic_file_handler import BasicFileHandler

handler = BasicFileHandler()
handler.process_file("your_task.md")
handler.print_log()
```

**As Command Line:**
```bash
cd AI_Employee
python -m skills.basic_file_handler
```

### Workflow
1. Scans `/Needs_Action` for markdown files
2. Loads Company_Handbook.md to verify rules
3. Reads each file and extracts key information
4. Creates summarized action plan in `/Plans` folder
5. Moves original file to `/Done` folder
6. Outputs success message with full file paths

### Output Example
```
[OK] Company_Handbook.md loaded - Rules verified
[OK] Read file: vault/Needs_Action/task.md
[OK] Content summarized
[OK] Plan created: vault/Plans/Plan_task_20260215_124923.md
[OK] Moved to Done: vault/Done/task.md
[SUCCESS] File processed successfully!
[RESULT] Plan created at: vault/Plans/Plan_task_20260215_124923.md
```

---

## Skill 2: Task Analyzer

**Location:** `skills/task_analyzer.py`

### Purpose
Analyzes tasks in Needs_Action folder, identifies task types, creates detailed action plans, and routes sensitive tasks to approval queue.

### Features
✅ Automatic task type identification (file_drop, data_processing, documentation, etc.)
✅ Analyzes content for sensitive keywords
✅ Creates detailed action plans with multi-step workflows
✅ Implements Ralph Wiggum Loop for multi-step tasks
✅ Routes sensitive tasks to /Pending_Approval folder
✅ Approval requirement detection
✅ Comprehensive logging and reporting

### Task Types Detected
- **file_drop** - New file uploads
- **data_processing** - Data processing tasks
- **documentation** - Documentation needs
- **meeting_notes** - Meeting summaries
- **bug_report** - Bug reports
- **feature_request** - Feature requests
- **configuration** - Configuration tasks
- **unknown** - Unclassified tasks

### Sensitive Keywords
Triggers approval routing if detected:
- payment, refund, money, financial
- confidential, secret, private, secure
- approve, permission, access, delete
- critical, urgent, emergency

### Ralph Wiggum Loop
Simple iterative pattern for multi-step tasks:
- Processes each step sequentially
- Verifies completion at each stage
- Maintains checklist of all steps
- Ideal for complex workflows

### Usage

**As a Python Module:**
```python
from skills.task_analyzer import TaskAnalyzer

analyzer = TaskAnalyzer()
analyzer.analyze_task("payment_request.md")
analyzer.print_log()
```

**As Command Line:**
```bash
cd AI_Employee
python -m skills.task_analyzer
```

### Workflow
1. Scans `/Needs_Action` for markdown files
2. Analyzes filename and content
3. Identifies task type automatically
4. Checks for sensitive keywords
5. Creates detailed action plan in `/Plans`
6. Implements Ralph Wiggum Loop for steps
7. Routes to `/Pending_Approval` if sensitive
8. Outputs comprehensive analysis report

### Output Example
```
[START] Analyzing task: payment_request.md
[ANALYZE] Task type identified: feature_request
[SENSITIVE] Found sensitive keyword: 'payment'
[LOOP] Entering Ralph Wiggum Loop for multi-step task
[LOOP-1] Processing: Analyze requirement
[LOOP-2] Processing: Design solution
[LOOP-3] Processing: Implement feature
[LOOP-4] Processing: Test thoroughly
[SUCCESS] Analysis complete!
[RESULT] Task Type: feature_request
[RESULT] Approval Needed: True
[RESULT] Plan at: vault/Plans/ActionPlan_feature_request_20260215.md
```

---

## Skill Workflow Comparison

### @Basic File Handler
**Best for:** Simple file processing and document organization
- Input: Tasks in Needs_Action/
- Process: Read → Summarize → Create Plan
- Output: Plans/ and Done/
- Time: ~1-2 seconds per file

### @Task Analyzer
**Best for:** Complex task analysis and approval routing
- Input: Tasks in Needs_Action/
- Process: Analyze → Type → Detect Sensitivity → Route
- Output: Plans/ and Pending_Approval/
- Time: ~1-2 seconds per file

---

## Combined Usage Example

**Scenario:** Processing a new task file

### Step 1: Use Task Analyzer
```bash
python -m skills.task_analyzer
```
Output: Identifies task type, detects if approval needed, creates ActionPlan

### Step 2: If Approved, Use Basic File Handler
```bash
python -m skills.basic_file_handler
```
Output: Creates detailed plan with checkboxes, moves to Done

---

## Directory Structure After Skill Usage

```
vault/
├── Inbox/                          [Incoming items]
├── Needs_Action/                   [Tasks to process]
├── Done/                           [Processed files]
│   ├── file_drop_task.md
│   ├── documentation_task.md
│   └── ...
├── Pending_Approval/               [Sensitive tasks]
│   ├── payment_request.md
│   ├── confidential_task.md
│   └── ...
├── Plans/                          [Generated plans]
│   ├── ActionPlan_file_drop_*.md
│   ├── ActionPlan_feature_request_*.md
│   ├── Plan_task_*.md
│   └── ...
├── Dashboard.md
├── Company_Handbook.md
└── SKILLS.md
```

---

## Best Practices

### Using Basic File Handler
1. ✅ Use for straightforward document processing
2. ✅ Verify handbook rules are loaded
3. ✅ Check Plans/ folder for generated outputs
4. ✅ Archive old plans regularly

### Using Task Analyzer
1. ✅ Run on new files for initial categorization
2. ✅ Review Pending_Approval/ for sensitive items
3. ✅ Get manager approval before executing sensitive plans
4. ✅ Use Ralph Wiggum Loop outputs for complex tasks

### Combined Workflow
1. Drop task file in Needs_Action/
2. Run Task Analyzer first (categorizes + detects sensitive)
3. If sensitive → get approval from Pending_Approval/
4. If approved → run Basic File Handler (summarizes + moves)
5. Check Done/ folder for completion

---

## Troubleshooting

**Problem:** Files not being found
- **Solution:** Ensure files are in `/Needs_Action` folder with .md extension

**Problem:** Company_Handbook.md not loading
- **Solution:** Verify file exists in `/vault` folder

**Problem:** Approval not triggered
- **Solution:** Check if content contains sensitive keywords from the keyword list

**Problem:** Plans folder not created
- **Solution:** Ensure `/vault/Plans` directory exists (created automatically)

---

## Extending the Skills

### Adding New Task Types (Task Analyzer)
Edit `skills/task_analyzer.py`, add to `analyze_file_type()` method:
```python
elif 'your_keyword' in filename_lower:
    task_type = "your_type"
```

### Adding New Sensitive Keywords (Task Analyzer)
Edit the `SENSITIVE_KEYWORDS` list:
```python
SENSITIVE_KEYWORDS = [
    'existing_keyword',
    'your_new_keyword'  # Add here
]
```

### Customizing Action Plan Template
Modify the `create_action_plan()` or `create_plan()` methods to change output format.

---

## Generated Files Reference

### From Basic File Handler
- **Format:** `Plan_{original_filename}_{timestamp}.md`
- **Location:** `vault/Plans/`
- **Contains:** Summary, checklist, source reference

### From Task Analyzer
- **Format:** `ActionPlan_{task_type}_{timestamp}.md`
- **Location:** `vault/Plans/`
- **Contains:** Task analysis, multi-step plan, approval status

---

## Skill Status: ✅ READY FOR PRODUCTION

Both skills have been tested with sample files and are ready for full deployment.

**Last Updated:** 2026-02-15
**Version:** Bronze Tier v1.0
