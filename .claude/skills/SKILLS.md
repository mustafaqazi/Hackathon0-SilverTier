# AI Employee Skills & Capabilities

## Bronze Tier Capabilities

### Task Management
- [x] Task creation and tracking
- [x] Priority assignment
- [x] Status updates
- [x] File organization

### Technical Skills
- [x] File system monitoring
- [x] Directory management
- [x] File reading and writing
- [x] Markdown documentation

### Automation
- [x] Filesystem watching
- [x] Event triggering
- [x] Task orchestration (basic)

### Communication
- [x] Clear status reporting
- [x] Documentation creation
- [x] Task logging

## Skill Categories

### Tier 1: Current Skills
| Skill | Level | Status |
|-------|-------|--------|
| File Management | ⭐⭐⭐ | Active |
| Task Tracking | ⭐⭐⭐ | Active |
| Documentation | ⭐⭐⭐ | Active |
| Automation | ⭐⭐ | Active |

### Tier 2: Development Areas
| Skill | Target | Timeline |
|-------|--------|----------|
| Advanced Orchestration | ⭐⭐⭐ | Silver Tier |
| ML Integration | ⭐⭐ | Future |
| API Integration | ⭐⭐⭐ | Future |

## Skill Usage Notes
- All Bronze Tier skills are currently available
- Skills can be combined for complex workflows
- Refer to Company_Handbook.md for usage guidelines

---

## Reusable Agent Skills

### Skill: ProcessIncomingItem

**Description:**
Yeh skill incoming items ko process karta hai Needs_Action folder se. Har item ko analyze karke summary banata hai, next actions suggest karta hai, aur Dashboard ke Recent Activity section mein update karta hai.

**Category:** Task Management & Automation
**Tier:** Bronze
**Status:** Available

**Inputs Required:**
- None (automatically scans Needs_Action folder)

**Outputs Provided:**
- Summary of each item
- 3-4 checkbox-based next actions
- Updated Dashboard.md with entry details

**Prompt Template:**
```
Tu ek AI Employee ho jo incoming items process karte ho.

TASK:
1. Needs_Action folder ke andar sab .md files ko find kar
2. Har file ka full content padh
3. Har item ke liye:
   a) Ek 1-2 sentence summary banao
   b) 3-4 possible next actions suggest kar (checkbox format mein)
   c) Item ka status/priority note kar

4. Sab kuch ko dashboard entry mein format kar:
   - Format: "📋 [Item Name] - [Summary] | Actions: [ ] Action1 [ ] Action2 [ ] Action3"

5. Yeh entry Dashboard.md ke Recent Activity section mein add kar

6. Final output mein yeh dikhao:
   - Total items processed
   - Har item ka summary + suggested actions
   - Updated Dashboard entry

CONSTRAINTS:
- Sirf .md files process kar
- Summary concise rahe (1-2 lines)
- Actions clear aur actionable ho
- Dashboard entry consistent format mein ho
```

**Example Usage:**
```
Skill: ProcessIncomingItem
Input: (automatic scan)
Output:
- Items found: 3
- Processing each with summary and action items
- Dashboard.md updated with new entries
```

**Integration Notes:**
- Har item ke baad Dashboard update hota hai
- Recent Activity section mein timestamp ke saath add hota hai
- Skill ko recurring basis pe run kar sakte ho for continuous monitoring

---

### Skill: BasicFileHandler

**Description:**
BasicFileHandler skill markdown files ko read, summarize, aur organize karta hai. Yeh Needs_Action folder se files padhe, unka summary banaye, Plans folder mein action plans create kare, aur processed files ko Done folder mein move kare.

**Category:** File Management & Task Processing
**Tier:** Bronze
**Status:** Available
**Implementation:** Python class-based (skills/basic_file_handler.py)

**Inputs Required:**
- Markdown files in Needs_Action/ folder
- Company_Handbook.md (for rule verification)

**Outputs Provided:**
- File content summary (headers + key points)
- Action plan with checkboxes in Plans/ folder
- Processed file moved to Done/ folder
- Detailed operation log with status

**Key Operations:**
1. `check_handbook_rules()` - Verify Company_Handbook.md exists and rules are loaded
2. `read_markdown_file()` - Read .md files from Needs_Action folder
3. `summarize_content()` - Extract headers and key points into summary
4. `create_plan()` - Generate Plan_[filename]_[timestamp].md with action steps
5. `move_to_done()` - Move processed file from Needs_Action to Done folder
6. `process_file()` - Execute complete workflow for single file

**Prompt Template:**
```
Tu ek AI Employee ho jo files ko process karta hai.

TASK (BasicFileHandler):
1. Needs_Action folder mein se markdown files ko scan kar
2. Har file ke liye:
   a) Content ko padh aur summarize kar (headers + key points)
   b) Ek action plan banao Plans folder mein
   c) Plan mein checkbox-based next steps add kar
   d) Original file ko Done folder mein move kar
3. Har step ke liye detailed log entry add kar:
   - [OK] Successful operations
   - [ERROR] Failed operations
   - [WARN] Warnings
4. Dashboard.md mein entry add kar:
   - "- Handled: [filename] at [timestamp]"

WORKFLOW:
1. check_handbook_rules() - Verify handbook exists
2. read_markdown_file() - Read from Needs_Action
3. summarize_content() - Extract key information
4. create_plan() - Generate action plan with checkboxes
5. move_to_done() - Archive processed file
6. Log all operations with status

CONSTRAINTS:
- Sirf .md files process kar
- Plans folder mein Plan_[name]_[timestamp].md format use kar
- Handbook rules verify karne ke baad hi action le
- Move operation ke baad Done folder confirm kar
- Log entry descriptive rahe
```

**Example Usage:**
```
Skill: BasicFileHandler
Input: Markdown file in Needs_Action/ (e.g., task_001.md)
Output:
- Summary extracted and logged
- Plan created: Plans/Plan_task_001_20260216_142000.md
- File moved to Done/task_001.md
- Dashboard entry added: "- Handled: task_001.md at 2026-02-16 14:20:00"
- Log shows: [OK] operations completed
```

**Process Flow:**
```
Needs_Action/
    └─ task_001.md
           ↓
    [read & verify]
           ↓
    [summarize content]
           ↓
Plans/
    └─ Plan_task_001_[timestamp].md  (created)
           ↓
    [move to done]
           ↓
Done/
    └─ task_001.md  (moved)
           ↓
Dashboard.md
    └─ Recent Activity updated with "Handled: ..." entry
```

**Integration Notes:**
- Automatically checks Company_Handbook.md before processing
- Creates timestamped action plans for traceability
- Maintains detailed operation logs
- Safe file movement with error handling
- Works with ProcessIncomingItem skill for complete workflow
- Can be run on schedule or on-demand basis

**Error Handling:**
- File not found: Logs [ERROR] and aborts
- Non-markdown files: Skipped automatically
- Handbook missing: Processing aborted
- Move failure: Logs warning but continues

---

### Skill: TaskAnalyzer

**Description:**
TaskAnalyzer skill tasks ko analyze karta hai, unka type identify karta hai, aur approval requirements determine karta hai. Yeh sensitive keywords detect karta hai, task-specific action plans banata hai, aur sensitive tasks ko Pending_Approval folder mein route karta hai.

**Category:** Task Analysis & Workflow Management
**Tier:** Bronze
**Status:** Available
**Implementation:** Python class-based (skills/task_analyzer.py)

**Inputs Required:**
- Markdown files in Needs_Action/ folder
- File content analysis for type and sensitivity detection

**Outputs Provided:**
- Task type identification
- Approval requirement detection
- Task-specific action plans in Plans/ folder
- Sensitive tasks routed to Pending_Approval/ folder
- Detailed analysis log with classification

**Key Operations:**
1. `analyze_file_type()` - Identify task type from filename and content
2. `check_approval_needed()` - Detect sensitive keywords requiring approval
3. `ralph_wiggum_loop()` - Multi-step task iteration pattern
4. `create_action_plan()` - Generate task-specific action plans
5. `move_to_pending_approval()` - Route sensitive tasks for approval
6. `analyze_task()` - Execute complete analysis workflow

**Supported Task Types:**
- `file_drop` - File upload/drop tasks
- `data_processing` - Data parsing and processing
- `documentation` - Document review and publishing
- `meeting_notes` - Meeting summaries and follow-ups
- `bug_report` - Bug identification and fixing
- `feature_request` - Feature design and implementation
- `configuration` - System setup and configuration
- `unknown` - Generic tasks

**Sensitive Keywords Detected:**
- Financial: payment, refund, money, financial
- Confidential: confidential, secret, private, secure
- Approval: approve, permission, access, delete
- Urgent: critical, urgent, emergency

**Prompt Template:**
```
Tu ek AI Employee ho jo tasks ko analyze karta hai.

TASK (TaskAnalyzer):
1. Needs_Action folder mein se files ko scan kar
2. Har file ke liye:
   a) Task type identify kar (file_drop, data_processing, documentation, etc.)
   b) Sensitive keywords check kar (payment, confidential, urgent, etc.)
   c) Task-specific action plan banao
   d) Agar sensitive hai to Pending_Approval folder mein copy kar
3. Har step ke liye detailed log entry add kar:
   - [ANALYZE] Task type identified
   - [SENSITIVE] Keyword found
   - [OK] No sensitive content
   - [LOOP] Multi-step processing
4. Dashboard.md mein analysis entry add kar:
   - "- Analyzed: [filename] - Type: [type] - Approval: [YES/NO]"

WORKFLOW:
1. analyze_file_type() - Detect task category
2. check_approval_needed() - Scan for sensitive keywords
3. ralph_wiggum_loop() - Process multi-step tasks
4. create_action_plan() - Generate type-specific action steps
5. move_to_pending_approval() - Route if needed
6. Log all findings with status

TASK TYPE PATTERNS:
- file_drop: "drop", "upload" in filename
- data_processing: "data", "process" in filename
- documentation: "doc", "readme" in filename
- meeting_notes: "meeting", "notes" in filename
- bug_report: "bug", "issue" in filename
- feature_request: "feature", "request" in filename
- configuration: "config", "setup" in filename

APPROVAL ROUTES:
- If sensitive keywords found → Copy to Pending_Approval/
- Require: Manager approval, Security review, Compliance check
- Mark as: [!] **PENDING APPROVAL REQUIRED**

CONSTRAINTS:
- Markdown files only
- Case-insensitive keyword matching
- Ralph Wiggum Loop for ordered steps
- Preserve original file in Needs_Action if approved needed
- Log entry descriptive aur timestamped rahe
```

**Example Usage:**
```
Skill: TaskAnalyzer
Input: Markdown file in Needs_Action/ (e.g., payment_request.md)

Processing:
1. Task Type: file_drop (detected from content)
2. Sensitive Check: Found keyword "payment" → REQUIRES APPROVAL
3. Action Plan: ActionPlan_file_drop_[timestamp].md created
4. Routing: Copied to Pending_Approval/payment_request.md
5. Log: [SENSITIVE] Found sensitive keyword: 'payment'

Output:
- Plan created: Plans/ActionPlan_file_drop_[timestamp].md
- File routed: Pending_Approval/payment_request.md
- Dashboard entry: "- Analyzed: payment_request.md - Type: file_drop - Approval: YES"
- Status: PENDING APPROVAL REQUIRED
```

**Ralph Wiggum Loop Pattern:**
```
Simple iterative approach for multi-step tasks:
- "I'm in danger" → "I'm in a loop" → "Simple repeating check"

Implementation:
- Verify each step in sequence
- Mark completion with [ ] checkboxes
- Move to next step automatically
- Complete when all steps processed

Example Action Items (for file_drop):
- [ ] Receive file
- [ ] Verify file integrity
- [ ] Extract metadata
- [ ] Store in appropriate folder
```

**Action Plan Structure by Type:**
```
file_drop:
  - Receive file → Verify integrity → Extract metadata → Store

data_processing:
  - Parse data → Validate format → Process records → Generate report

documentation:
  - Review document → Check formatting → Verify accuracy → Publish

meeting_notes:
  - Summarize points → Extract actions → Assign owners → Set follow-ups

bug_report:
  - Reproduce issue → Identify cause → Create fix → Test resolution

feature_request:
  - Analyze requirement → Design solution → Implement → Test

configuration:
  - Gather settings → Configure system → Validate → Document
```

**Integration Notes:**
- Works with BasicFileHandler for complete task processing
- Integrates with Pending_Approval folder for approval workflow
- Sensitive tasks marked with [!] **PENDING APPROVAL REQUIRED**
- Task type determines action plan steps automatically
- Can be combined with ProcessIncomingItem for full workflow
- Maintains audit trail via detailed logs

**Approval Workflow:**
```
Task Analysis
    ↓
[No sensitive keywords]
    ↓
Action Plan created
Ready for processing

[Sensitive keywords found]
    ↓
Action Plan created
    ↓
Copy to Pending_Approval/
    ↓
Await Manager approval
Await Security review
Await Compliance check
    ↓
[APPROVED] → ProcessIncomingItem
[REJECTED] → Archive
```

**Error Handling:**
- File not found: Logs [ERROR] and aborts analysis
- Read failure: Exception caught and logged
- Plan creation failure: Logs [ERROR] without stopping
- Approval routing failure: Logs [WARN] but continues
- Sensitive detection: Automatic, no manual override needed

**Output Format:**
- Plans: `ActionPlan_[tasktype]_[YYYYMMDD_HHMMSS].md`
- Dashboard entries: `- Analyzed: [filename] - Type: [type] - Approval: [YES/NO]`
- Approval routing: Copies to `Pending_Approval/[filename]`
- Logs: Structured with [ANALYZE], [SENSITIVE], [OK], [LOOP], [ERROR], [WARN]

---

*Last Updated: 2026-02-16*
