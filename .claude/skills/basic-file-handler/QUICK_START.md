# BasicFileHandler Skill - Quick Start Guide

## What It Does

BasicFileHandler reads tasks from `vault/Needs_Action/`, creates detailed action plans, and archives the files. Perfect for converting incoming tasks into structured work.

---

## Quick Setup

### 1. **Folder Structure**
```
AI_Employee/
├── vault/
│   ├── Needs_Action/        ← Put .md files here
│   ├── Plans/               ← Gets created plans
│   ├── Done/                ← Gets archived files
│   ├── Dashboard.md         ← Gets updated
│   └── Company_Handbook.md  ← (Optional)
├── .claude/
│   └── skills/
│       └── basic-file-handler/
│           ├── BasicFileHandler.py
│           ├── SKILL.md
│           └── QUICK_START.md
```

### 2. **Run the Skill**
```bash
cd AI_Employee
python .claude/skills/basic-file-handler/BasicFileHandler.py
```

### 3. **See Results**
- ✅ Check `vault/Plans/` for created action plans
- ✅ Check `vault/Done/` for archived files
- ✅ Check `vault/Dashboard.md` Recent Activity

---

## The Workflow

```
Needs_Action/
    task.md
        ↓
[Read & Analyze]
        ↓
Plans/
    Plan_task_[time].md  ← Created with 5 phases
        ↓
Done/
    processed_task.md  ← Moved here
        ↓
Dashboard.md  ← Updated with entry
```

---

## File Format

Put markdown files in `vault/Needs_Action/`:

### Full Format (Recommended)
```markdown
---
subject: Clear Title
type: feature | bug | documentation | task
priority: CRITICAL | HIGH | MEDIUM | LOW
---

## Overview
What this task is about...

## Requirements
- Requirement 1
- Requirement 2

## Details
More information...
```

### Minimal Format
```markdown
# Task Title

Description...
```

---

## What Gets Created

### Action Plan Example
```
vault/Plans/Plan_task_20260220_103045.md
├── Summary (extracted headers + key points)
├── Phase 1: Understanding
│   ├── [ ] Review the full file content
│   ├── [ ] Read all headers and sections
│   ├── [ ] Identify key requirements
│   └── [ ] Note any dependencies
├── Phase 2: Analysis
│   ├── [ ] Extract main objectives
│   ├── [ ] Identify what needs to be done
│   ├── [ ] Check for conflicts
│   └── [ ] Document unclear points
├── Phase 3: Planning
│   ├── [ ] Create implementation steps
│   ├── [ ] Define success criteria
│   ├── [ ] Estimate effort/timeline
│   └── [ ] Identify resources
├── Phase 4: Execution
│   ├── [ ] Follow the planned steps
│   ├── [ ] Document progress
│   ├── [ ] Handle issues
│   └── [ ] Verify completion
└── Phase 5: Completion
    ├── [ ] Verify requirements met
    ├── [ ] Move to Done folder
    ├── [ ] Update Dashboard
    └── [ ] Archive plan
```

---

## Example: Process a Payment Request

### 1. Create File
```markdown
vault/Needs_Action/payment_request_001.md
---
subject: Client Payment Processing
type: financial
priority: CRITICAL
---

## Payment Request

**Client:** ABC Corporation
**Amount:** ₹150,000
**Invoice:** INV-2026-001

Process urgent payment for completed deliverables.
```

### 2. Run Skill
```bash
python BasicFileHandler.py
```

### 3. Output
```
✅ Read file: payment_request_001.md
✅ Content summarized
✅ Created plan: Plan_payment_request_001_20260220_103045.md
✅ Moved to Done: processed_payment_request_001.md
✅ Dashboard updated
```

### 4. Results
- ✅ `vault/Plans/Plan_payment_request_001_20260220_103045.md` created
- ✅ `vault/Done/processed_payment_request_001.md` archived
- ✅ Dashboard updated with completion entry

---

## Key Features

| Feature | What It Does |
|---------|--------------|
| 📖 **Read** | Reads .md files from Needs_Action |
| 📝 **Summarize** | Extracts headers and key points |
| 📋 **Plan** | Creates 5-phase action plans |
| ✅ **Checkbox** | 4 action items per phase |
| 🗂️ **Archive** | Moves to Done folder |
| 📊 **Dashboard** | Updates Recent Activity |
| 📋 **Log** | Detailed operation log |

---

## The 5 Phases

Every action plan includes:

1. **Understanding** - Review & understand the task
2. **Analysis** - Extract objectives & identify requirements
3. **Planning** - Create steps & define success
4. **Execution** - Do the work & document progress
5. **Completion** - Verify & finalize

Each phase has 4 checkbox items.

---

## File Paths

### Input Location
```
vault/Needs_Action/task.md
```

### Output Locations
```
vault/Plans/Plan_task_[timestamp].md      (created)
vault/Done/processed_task.md              (moved)
vault/Dashboard.md                        (updated)
```

### Timestamp Format
`YYYYMMDD_HHMMSS` - Example: `20260220_103045`

---

## Run Manually
```bash
python .claude/skills/basic-file-handler/BasicFileHandler.py
```

## Run on Schedule

### Windows (Task Scheduler)
```
Schedule: Every 12 hours
Command: python C:\path\to\BasicFileHandler.py
```

### Linux/Mac (Cron)
```bash
0 */12 * * * cd /path/to/AI_Employee && python BasicFileHandler.py
```

---

## Dashboard Entry Example

After running, your Dashboard.md will have:

```markdown
## Recent Activity
- ✅ **[PROCESSED]** payment_request_001.md - Plan created: Plan_payment_request_001_20260220_103045.md at 2026-02-20 10:30:45 | File moved to Done/
```

---

## Common Tasks

### ✨ Process Single File
1. Create `.md` in `vault/Needs_Action/`
2. Run: `python BasicFileHandler.py`
3. Check `vault/Plans/` for created plan

### 🔄 Process Multiple Files
1. Add multiple `.md` files to `vault/Needs_Action/`
2. Run skill once - processes all
3. Plans created for each in `vault/Plans/`

### ✅ Work Through a Plan
1. Open `Plan_[name]_[timestamp].md`
2. Work through 5 phases
3. Check off items as you complete
4. Save progress

### 📊 Track Progress
- Check Dashboard Recent Activity
- See which files were processed
- See which plans were created

---

## File Types

Supported in Needs_Action folder:
- ✅ `.md` markdown files
- ❌ Other file types (skipped)

Naming doesn't matter:
- ✅ `task.md`
- ✅ `feature_request_001.md`
- ✅ `BUG-2026-001.md`
- ✅ `anything_you_want.md`

---

## Metadata Fields

YAML frontmatter fields (all optional):

```yaml
subject: Title of the task
type: feature | bug | documentation | task | (or any value)
priority: CRITICAL | HIGH | MEDIUM | LOW
id: unique_identifier
created: 2026-02-20
```

If not provided, defaults are used.

---

## Output Details

### Console Output Shows
- ✅ Files read successfully
- ✅ Summaries created
- ✅ Plans generated
- ✅ Files moved
- ✅ Dashboard updated
- ❌ Any errors
- ⚠️ Any warnings

### Operation Log Codes
- `[OK]` - Success
- `[ERROR]` - Failed
- `[WARN]` - Warning
- `[INFO]` - Information

---

## Troubleshooting

**Q: Plan not created?**
A: Check write permissions to Plans/ folder

**Q: File not moved to Done?**
A: Check write permissions to Done/ folder

**Q: Headers not extracted?**
A: Use proper markdown syntax (# H1, ## H2)

**Q: Handbook rules not loaded?**
A: File is optional - skill continues without it

---

## Integration

Works with:
- ProcessIncomingItem (dashboard summary)
- Task Planners (action plans)
- File Watchers (trigger processing)
- Approval Systems (for sensitive files)

---

## Best Practices

1. ✅ Run on regular schedule (every 12-24 hours)
2. ✅ Review created plans before execution
3. ✅ Keep Dashboard.md organized
4. ✅ Archive completed plans
5. ✅ Check operation logs for errors
6. ✅ Use consistent file format

---

## Example Workflow

```
Day 1:
├─ Create task files in Needs_Action/
└─ Run BasicFileHandler.py

Day 2:
├─ Check Plans/ folder for created plans
├─ Review plans for accuracy
└─ Start working through Phase 1

Day 3-5:
├─ Work through phases
├─ Check off completed items
└─ Document progress

Day 6:
├─ Complete Phase 5: Completion
├─ Verify all requirements met
└─ Archive completed plan

Dashboard tracks: Original file → Plan created → File moved to Done
```

---

**Version:** 1.0 | **Tier:** Bronze | **Status:** Ready to Use ✅
