# BasicFileHandler Skill - BRONZE Tier

## Skill Overview

**BasicFileHandler** reads markdown files from `vault/Needs_Action/`, analyzes their content, creates action plans with detailed workflows, and automatically archives processed files to `vault/Done/`. This skill is essential for converting incoming tasks into actionable work items.

**Category:** File Management & Task Processing
**Tier:** Bronze
**Status:** Available

---

## How It Works

### Complete Processing Workflow

```
Needs_Action/
    └─ task.md
        ↓
    [STEP 1: Read & Verify]
        ├─ Read markdown content
        ├─ Extract YAML metadata
        └─ Verify handbook rules
        ↓
    [STEP 2: Analyze & Summarize]
        ├─ Extract headers (structure)
        ├─ Extract key points
        └─ Create content summary
        ↓
    [STEP 3: Create Action Plan]
        ├─ Generate Plan_[name]_[timestamp].md
        ├─ Add 5 workflow phases
        ├─ Include checkbox action items
        └─ Save to Plans/
        ↓
    [STEP 4: Archive File]
        ├─ Move task.md to Done/
        ├─ Rename to processed_task.md
        └─ Verify move success
        ↓
    [STEP 5: Update Dashboard]
        ├─ Add completion entry
        ├─ Reference created plan
        └─ Log timestamp
        ↓
Done/
    └─ processed_task.md
Plans/
    └─ Plan_task_[timestamp].md
Dashboard.md
    └─ Recent Activity updated
```

### Step-by-Step Operations

#### Step 1: Check Handbook Rules
- Verifies `vault/Company_Handbook.md` exists
- Loads company rules and policies
- Logs if handbook is missing (non-blocking)

#### Step 2: Read Markdown File
- Opens `.md` file from Needs_Action folder
- Extracts YAML frontmatter metadata
- Captures full content for analysis

#### Step 3: Extract & Summarize Content
- **Headers:** Extracts all H1, H2, H3 headers (structure)
- **Key Points:** Extracts bullet points or first sentences
- **Summary:** Creates formatted markdown summary with both

#### Step 4: Create Action Plan
Generates timestamped plan file with 5 phases:

| Phase | Purpose |
|-------|---------|
| **Understanding** | Review content, identify requirements |
| **Analysis** | Extract objectives, check dependencies |
| **Planning** | Create implementation steps, define success |
| **Execution** | Follow steps, document progress |
| **Completion** | Verify results, archive, update dashboard |

Each phase has 4 checkbox action items.

#### Step 5: Move to Done
- Moves original file from Needs_Action to Done
- Adds `processed_` prefix if needed
- Confirms move was successful

#### Step 6: Update Dashboard
- Adds entry to Recent Activity section
- References the created plan
- Records timestamp

---

## Usage

### Manual Execution

```bash
cd AI_Employee
python .claude/skills/basic-file-handler/BasicFileHandler.py
```

### Automated (Scheduled)

```bash
# Run every 12 hours
0 */12 * * * cd /path/to/AI_Employee && python .claude/skills/basic-file-handler/BasicFileHandler.py
```

### Using in Python Code

```python
from BasicFileHandler import BasicFileHandler

handler = BasicFileHandler(base_path="/path/to/AI_Employee")
result = handler.process_all_files()

# Access results
print(f"Processed: {result['processed']} files")
print(f"Errors: {result['errors']}")
print(f"Operation log: {result['log']}")
```

---

## Input Requirements

### Folder Structure
```
vault/
├── Needs_Action/           ← Input: .md files to process
├── Plans/                  ← Output: Action plans created
├── Done/                   ← Output: Processed files moved
├── Dashboard.md            ← Output: Updated with entries
└── Company_Handbook.md     ← Reference: Rules and policies (optional)
```

### File Format

Markdown files in `vault/Needs_Action/` should follow this format:

```markdown
---
subject: Clear Title of Task
type: feature | bug | documentation | task | other
priority: CRITICAL | HIGH | MEDIUM | LOW
id: unique_identifier (optional)
created: 2026-02-20
---

## Overview

Brief description of what this task is about.

## Requirements

- Requirement 1
- Requirement 2
- Requirement 3

## Details

More detailed information...

## Context

Additional context...
```

### Minimal Format

```markdown
# Task Title

Description of the task...
```

---

## Output Provided

### 1. Console Output

```
🚀 BasicFileHandler Skill Execution
============================================================
✅ [OK] 2026-02-20 10:30:45 - Read file: payment_request_001.md
✅ [OK] 2026-02-20 10:30:45 - Content summarized
✅ [OK] 2026-02-20 10:30:45 - Created plan: Plan_payment_request_001_20260220_103045.md
✅ [OK] 2026-02-20 10:30:45 - Moved to Done: processed_payment_request_001.md
✅ [OK] 2026-02-20 10:30:45 - Dashboard updated for payment_request_001.md

📊 Processing Summary
============================================================
✅ Total files processed: 1
❌ Errors encountered: 0
📁 Plans created in: vault/Plans
📦 Files archived in: vault/Done
```

### 2. Action Plan File

Created in `vault/Plans/Plan_[name]_[timestamp].md`:

```markdown
# Action Plan: Payment Request Processing

**Created:** 2026-02-20 10:30:45
**Source File:** payment_request_001.md
**Type:** financial
**Priority:** CRITICAL

## Summary

### Structure
- Overview
- Requirements
- Details

### Key Points
- Client ABC Corporation
- Amount: ₹150,000
- Invoice-based payment

## Action Steps

### Phase 1: Understanding
- [ ] Review the full file content
- [ ] Read all headers and sections
- [ ] Identify key requirements
- [ ] Note any dependencies

### Phase 2: Analysis
- [ ] Extract main objectives
- [ ] Identify what needs to be done
- [ ] Check for conflicting requirements
- [ ] Document unclear points

### Phase 3: Planning
- [ ] Create implementation steps
- [ ] Define success criteria
- [ ] Estimate effort/timeline
- [ ] Identify required resources

### Phase 4: Execution
- [ ] Follow the planned steps
- [ ] Document progress
- [ ] Handle issues
- [ ] Verify completion

### Phase 5: Completion
- [ ] Verify requirements met
- [ ] Move to Done folder
- [ ] Update Dashboard
- [ ] Archive plan

---
**Status:** PENDING
**Handler:** BasicFileHandler Skill v1.0
```

### 3. File Organization

**Before Processing:**
```
vault/
└── Needs_Action/
    ├── payment_request_001.md
    ├── bug_report_001.md
    └── feature_request_001.md
```

**After Processing:**
```
vault/
├── Needs_Action/          (now empty or has new files)
├── Plans/
│   ├── Plan_payment_request_001_[timestamp].md
│   ├── Plan_bug_report_001_[timestamp].md
│   └── Plan_feature_request_001_[timestamp].md
├── Done/
│   ├── processed_payment_request_001.md
│   ├── processed_bug_report_001.md
│   └── processed_feature_request_001.md
└── Dashboard.md           (Recent Activity updated)
```

### 4. Dashboard Updates

Entries added to `vault/Dashboard.md` Recent Activity:

```markdown
## Recent Activity
- ✅ **[PROCESSED]** payment_request_001.md - Plan created: Plan_payment_request_001_20260220_103045.md at 2026-02-20 10:30:45 | File moved to Done/
- ✅ **[PROCESSED]** bug_report_001.md - Plan created: Plan_bug_report_001_20260220_103050.md at 2026-02-20 10:30:50 | File moved to Done/
- ✅ **[PROCESSED]** feature_request_001.md - Plan created: Plan_feature_request_001_20260220_103055.md at 2026-02-20 10:30:55 | File moved to Done/
```

---

## Output Structure (Return Dictionary)

```python
{
    'status': 'COMPLETE',           # 'COMPLETE' or 'FAILED'
    'processed': 3,                 # Number of files processed
    'errors': 0,                    # Number of errors
    'handbook_loaded': True,        # Whether handbook was loaded
    'log': [                        # Detailed operation log
        '[OK] 2026-02-20 10:30:45 - Read file: payment_request_001.md',
        '[OK] 2026-02-20 10:30:45 - Content summarized',
        '[OK] 2026-02-20 10:30:45 - Created plan: Plan_payment_request_001_...',
        '[OK] 2026-02-20 10:30:45 - Moved to Done: processed_payment_request_001.md',
        '[OK] 2026-02-20 10:30:45 - Dashboard updated for payment_request_001.md'
    ]
}
```

---

## Key Methods

### `check_handbook_rules()`
Verifies Company_Handbook.md and loads rules
- ✅ Returns True if handbook loaded
- ⚠️ Continues if handbook missing (non-blocking)

### `read_markdown_file(file_path)`
Reads markdown file content
- Returns file content string
- Returns None on error

### `summarize_content(content)`
Creates summary from headers and key points
- Extracts all headers (structure)
- Extracts up to 5 key points
- Returns formatted markdown summary

### `create_action_plan(filename, content)`
Generates action plan with 5 phases
- Creates timestamped plan file
- Includes 4 action items per phase
- Returns plan filename

### `move_to_done(filename)`
Archives file and adds processed_ prefix
- Ensures Done folder exists
- Moves source file
- Returns True/False for success

### `update_dashboard(filename, plan_filename, success)`
Updates Dashboard.md Recent Activity
- Adds entry with status
- References created plan
- Records timestamp

### `process_file(filename)`
Complete workflow for single file
- Calls all methods in sequence
- Handles errors gracefully
- Returns success/failure

### `process_all_files()`
Process all files in Needs_Action
- Finds all .md files
- Processes each one
- Returns detailed results

---

## Information Extraction

### Headers Extraction
- Extracts all H1, H2, H3 headers
- Removes YAML frontmatter headers
- Limits to top 5 for summary

### Key Points Extraction
- Looks for bullet points (-, *)
- Falls back to first sentences of paragraphs
- Limits to 5 points maximum
- Limits each point to 150 characters

### Metadata Extraction
From YAML frontmatter:
- `subject` - Task title
- `type` - Task type (feature, bug, documentation, etc.)
- `priority` - Priority level (CRITICAL, HIGH, MEDIUM, LOW)
- `id` - Unique identifier
- `created` - Creation date

---

## File Naming Conventions

### Input Files
```
vault/Needs_Action/
└── [any-name].md
```

### Output Files
```
vault/Plans/
└── Plan_[name]_[YYYYMMDD_HHMMSS].md

vault/Done/
└── processed_[original-name].md
```

### Timestamp Format
`YYYYMMDD_HHMMSS` - Example: `20260220_103045`

---

## Error Handling

| Error | Behavior |
|-------|----------|
| File not found | Logs [ERROR], skips file, continues |
| Non-markdown file | Skipped automatically (glob *.md) |
| Handbook missing | Logs [WARN], continues (non-blocking) |
| Move failure | Logs [ERROR], continues, increments error count |
| Dashboard not found | Logs [WARN], skips update |
| Permission denied | Logs [ERROR], skips operation |

---

## Operation Log Status Codes

| Code | Meaning | Color |
|------|---------|-------|
| `[OK]` | Operation succeeded | ✅ Green |
| `[ERROR]` | Operation failed | ❌ Red |
| `[WARN]` | Warning (non-blocking) | ⚠️ Yellow |
| `[INFO]` | Informational message | ℹ️ Blue |

---

## Integration Notes

- **Works with:** ProcessIncomingItem, TaskAnalyzer, File Watchers
- **Reads from:** vault/Needs_Action/, vault/Company_Handbook.md
- **Writes to:** vault/Plans/, vault/Done/, vault/Dashboard.md
- **Frequency:** Can run multiple times safely (moves only new files)
- **Dependencies:** File system, no external APIs
- **Safe:** All operations are reversible (files in Done can be restored)

---

## Workflow Integration

### With ProcessIncomingItem
1. ProcessIncomingItem scans Needs_Action
2. Summarizes items for Dashboard
3. BasicFileHandler processes same items
4. Creates detailed plans and archives

### With Task Planners
1. BasicFileHandler creates action plans
2. Task planners read plans from Plans/
3. Execute and track progress
4. Archive completed plans

### Scheduled Automation
```bash
# Every 12 hours
0 */12 * * * BasicFileHandler.py
```

---

## Best Practices

1. **Regular Execution** - Run on schedule (12-24 hour intervals)
2. **Review Plans** - Check generated plans before execution
3. **Update Checkboxes** - Mark progress as you work
4. **Archive Properly** - Keep Done folder organized
5. **Dashboard Review** - Check Recent Activity regularly
6. **Handle Errors** - Review [ERROR] entries in logs
7. **Handbook Maintenance** - Keep Company_Handbook.md current

---

## Troubleshooting

**Q: Plans not created?**
A: Check that Plans/ folder can be created. Verify write permissions.

**Q: Files not moving to Done?**
A: Check that Done/ folder exists and has write permissions.

**Q: Dashboard not updating?**
A: Verify Dashboard.md exists and has `## Recent Activity` section.

**Q: Headers not extracted?**
A: Ensure file uses proper markdown header syntax (# H1, ## H2, etc.)

**Q: Handbook rules not loaded?**
A: Check Company_Handbook.md path and "## Rules" section.

---

## Version History

- **v1.0** (2026-02-20) - Initial release
  - Read and summarize markdown files
  - Create action plans with 5 phases
  - Archive processed files
  - Update Dashboard entries
  - Detailed operation logging

---

## Next Steps After Running

1. ✅ Check `vault/Plans/` for created plans
2. ✅ Review plans for accuracy
3. ✅ Open plans and work through phases
4. ✅ Check off action items as completed
5. ✅ Move completed plans to archive
6. ✅ Monitor Dashboard Recent Activity

---

**Skill Type:** File Management | **Execution Mode:** Standalone/Scheduled | **Requires Approval:** NO
