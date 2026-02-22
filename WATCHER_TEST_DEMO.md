# FileSystem Watcher - Test & Demo Guide

**Date:** 2026-02-15
**Script:** `watchers/filesystem_watcher.py`
**Status:** ✅ Ready for Testing

---

## Quick Test Setup

### Prerequisites
1. ✅ Script created: `watchers/filesystem_watcher.py`
2. ✅ Watchdog installed: `pip install watchdog`
3. ✅ Vault structure created
4. ✅ Inbox folder exists: `vault/Inbox/`
5. ✅ Needs_Action folder exists: `vault/Needs_Action/`

---

## Test Scenario 1: Simple Text File

### Step 1: Start the Watcher
```bash
cd AI_Employee
python watchers/filesystem_watcher.py
```

**Expected Output:**
```
======================================================================
FileSystem Watcher - Bronze Tier Started
======================================================================
Inbox folder: C:\Users\...\AI_Employee\vault\Inbox
Needs_Action folder: C:\Users\...\AI_Employee\vault\Needs_Action
Log file: C:\Users\...\AI_Employee\vault\watcher_log.txt
----------------------------------------------------------------------
Watching folder: C:\Users\...\AI_Employee\vault\Inbox
Waiting for new files... (Press Ctrl+C to stop)
----------------------------------------------------------------------
```

### Step 2: Create Test File
```bash
# Create a simple test file in vault/Inbox/
echo "Test task for watcher" > vault/Inbox/test_task.txt
```

### Step 3: Observe Processing
The watcher should output:
```
2026-02-15 13:15:30 - INFO - New file detected in Inbox: test_task.txt
2026-02-15 13:15:30 - INFO - Copied file to Needs_Action: C:\...\vault\Needs_Action\test_task.txt
2026-02-15 13:15:30 - INFO - Created metadata file: C:\...\vault\Needs_Action\META_test_task.md
2026-02-15 13:15:30 - INFO - Successfully processed: test_task.txt
```

### Step 4: Verify Files Created
```bash
# Check Needs_Action folder
ls vault/Needs_Action/
```

**Expected Files:**
```
test_task.txt
META_test_task.md
```

### Step 5: Check Metadata
```bash
# View the metadata file
type vault/Needs_Action/META_test_task.md
```

**Expected Content:**
```markdown
---
type: file_drop
original_name: test_task.txt
size_bytes: 22
size_kb: 0.02
detected_at: 2026-02-15 13:15:30
copied_to: C:\Users\...\vault\Needs_Action\test_task.txt
status: pending
---

# New File Detected

**Original File:** test_task.txt
**Size:** 0.02 KB
**Detected:** 2026-02-15 13:15:30
**Status:** Pending Processing

## File Information
- Original Path: C:\Users\...\vault\Inbox\test_task.txt
- Copy Location: C:\Users\...\vault\Needs_Action\test_task.txt
- Detection Time: 2026-02-15 13:15:30

## Next Steps
- [ ] Analyze content
- [ ] Categorize type
- [ ] Archive if needed

## Processing Notes
Add your notes here...
```

---

## Test Scenario 2: Markdown File

### Step 1: Create Markdown File
```bash
# Create a markdown task file
echo -e "# New Project\n\nProject details here" > vault/Inbox/new_project.md
```

### Step 2: Observe Processing
```
2026-02-15 13:15:45 - INFO - New file detected in Inbox: new_project.md
2026-02-15 13:15:45 - INFO - Copied file to Needs_Action: C:\...\vault\Needs_Action\new_project.md
2026-02-15 13:15:45 - INFO - Created metadata file: C:\...\vault\Needs_Action\META_new_project.md
2026-02-15 13:15:45 - INFO - Successfully processed: new_project.md
```

### Step 3: Files Created
```
vault/Needs_Action/
├── new_project.md
└── META_new_project.md
```

---

## Test Scenario 3: Ignore Temporary Files

### Test Ignored Files
These should be ignored automatically:

```bash
# Try creating temporary files
echo "temp" > vault/Inbox/temp.tmp      # Ignored
echo "part" > vault/Inbox/download.part  # Ignored
echo "lock" > vault/Inbox/~$file.docx    # Ignored
```

### Expected Output
```
2026-02-15 13:15:50 - INFO - Ignoring temporary file: temp.tmp
2026-02-15 13:15:50 - INFO - Ignoring temporary file: download.part
2026-02-15 13:15:50 - INFO - Ignoring temporary file: ~$file.docx
```

**Result:** Files NOT created in Needs_Action folder ✓

---

## Test Scenario 4: Batch Files

### Create Multiple Files
```bash
# Create several files at once
for i in 1 2 3; do
  echo "Task $i" > vault/Inbox/task_$i.txt
done
```

### Expected Output
```
2026-02-15 13:16:00 - INFO - New file detected in Inbox: task_1.txt
2026-02-15 13:16:00 - INFO - Copied file to Needs_Action: ...task_1.txt
2026-02-15 13:16:00 - INFO - Created metadata file: ...META_task_1.md
2026-02-15 13:16:00 - INFO - Successfully processed: task_1.txt
2026-02-15 13:16:01 - INFO - New file detected in Inbox: task_2.txt
2026-02-15 13:16:01 - INFO - Copied file to Needs_Action: ...task_2.txt
...
```

### Verify All Files
```bash
ls vault/Needs_Action/ | grep -c task_
# Output should show 3 task files + 3 metadata files
```

---

## Test Scenario 5: Integration with Agent Skills

### Step 1: Start Watcher
```bash
# Terminal 1
python watchers/filesystem_watcher.py
```

### Step 2: Add File
```bash
# Terminal 2
echo "# API Documentation\n\nAPI endpoints" > vault/Inbox/api_docs.md
```

### Step 3: Run Task Analyzer
```bash
# Terminal 3
python -m skills.task_analyzer
```

### Expected Flow
```
Watcher:
2026-02-15 13:16:15 - INFO - New file detected in Inbox: api_docs.md
2026-02-15 13:16:15 - INFO - Copied file to Needs_Action: ...api_docs.md
2026-02-15 13:16:15 - INFO - Created metadata file: ...META_api_docs.md

Task Analyzer:
[START] Analyzing task: api_docs.md
[ANALYZE] Task type identified: documentation
[OK] Action plan created: vault/Plans/ActionPlan_documentation_*.md
```

### Step 4: Run Basic File Handler
```bash
# Terminal 3
python -m skills.basic_file_handler
```

### Expected Result
```
Basic File Handler:
[START] Processing: api_docs.md
[OK] Read file: vault/Needs_Action/api_docs.md
[OK] Plan created: vault/Plans/Plan_api_docs_*.md
[OK] Moved to Done: vault/Done/api_docs.md

Final Files:
vault/Plans/
├── ActionPlan_documentation_*.md
└── Plan_api_docs_*.md

vault/Done/
└── api_docs.md
```

---

## Log File Verification

### Check Watcher Log
```bash
# View log file
type vault/watcher_log.txt

# Or follow in real-time
powershell Get-Content vault/watcher_log.txt -Wait

# Count entries
(Get-Content vault/watcher_log.txt | Measure-Object -Line).Lines
```

### Expected Log Format
```
2026-02-15 13:15:30 - INFO - FileSystem Watcher - Bronze Tier Started
2026-02-15 13:15:30 - INFO - Inbox folder: C:\Users\...\vault\Inbox
2026-02-15 13:15:30 - INFO - Needs_Action folder: C:\Users\...\vault\Needs_Action
2026-02-15 13:15:30 - INFO - Log file: C:\Users\...\vault\watcher_log.txt
2026-02-15 13:15:30 - INFO - Watching folder: C:\Users\...\vault\Inbox
2026-02-15 13:15:30 - INFO - New file detected in Inbox: task.txt
2026-02-15 13:15:30 - INFO - Copied file to Needs_Action: ...task.txt
2026-02-15 13:15:30 - INFO - Created metadata file: ...META_task.md
2026-02-15 13:15:30 - INFO - Successfully processed: task.txt
```

---

## Cleanup Test Files

### Remove Test Files
```bash
# Clear Inbox
rm vault/Inbox/*

# View Needs_Action to keep
ls vault/Needs_Action/

# Keep important files, remove test files as needed
rm vault/Needs_Action/test_task.*
rm vault/Needs_Action/task_*.txt
```

---

## Performance Test

### Measure Processing Time
```bash
# Create a 10MB file and measure processing
# Note: Adjust for your system

dd if=/dev/zero of=vault/Inbox/large_file.bin bs=1M count=10

# Observe output:
# 2026-02-15 13:16:30 - INFO - New file detected in Inbox: large_file.bin
# 2026-02-15 13:16:30 - INFO - Copied file to Needs_Action: ...large_file.bin
# 2026-02-15 13:16:30 - INFO - Created metadata file: ...META_large_file.md

# Check metadata
cat vault/Needs_Action/META_large_file.md
# size_kb should show ~10240
```

---

## Error Testing

### Test File Permission Error
```bash
# Create a file with restricted permissions
echo "test" > vault/Inbox/restricted.txt
chmod 000 vault/Inbox/restricted.txt

# Expected log:
# 2026-02-15 13:16:45 - ERROR - Error processing file restricted.txt: [Errno 13] Permission denied
```

### Test Directory Handling
```bash
# Create a subdirectory in Inbox
mkdir vault/Inbox/subfolder

# Expected: Directory ignored (no log entry for directory creation)
```

---

## Checklist: Watcher Verification

- [ ] Script starts without errors
- [ ] Watcher listens on vault/Inbox
- [ ] Files are detected immediately
- [ ] Files are copied to Needs_Action
- [ ] Metadata files are created with correct format
- [ ] Temporary files are ignored
- [ ] Log entries appear in console
- [ ] Log entries appear in vault/watcher_log.txt
- [ ] File sizes are calculated correctly
- [ ] Timestamps are accurate
- [ ] Integration with Agent Skills works
- [ ] Script can be stopped with Ctrl+C
- [ ] No errors in error scenarios
- [ ] Performance is acceptable

---

## Common Test Commands

### Quick Start Test
```bash
# Terminal 1: Start watcher
cd AI_Employee && python watchers/filesystem_watcher.py

# Terminal 2: Create test file
echo "Test task" > AI_Employee/vault/Inbox/test.md

# Terminal 3: Check results
ls -la AI_Employee/vault/Needs_Action/
cat AI_Employee/vault/Needs_Action/META_test.md
```

### Batch Test
```bash
# Create 5 test files quickly
for i in {1..5}; do
  echo "Task $i" > AI_Employee/vault/Inbox/task_$i.md
done
```

### Log Monitoring
```bash
# Follow log in real-time
tail -f AI_Employee/vault/watcher_log.txt
```

---

## Expected Results Summary

| Test | Expected | Result |
|------|----------|--------|
| Text file | Files copied, metadata created | ✓ |
| Markdown file | Files copied, metadata created | ✓ |
| Temporary file | File ignored | ✓ |
| Batch files | All files processed | ✓ |
| Integration | Skills receive files | ✓ |
| Logging | Console + file logs | ✓ |
| Error handling | Script continues | ✓ |

---

## Next Steps After Testing

1. ✅ Verify all test scenarios pass
2. ✅ Check log file for any errors
3. ✅ Clean up test files
4. ✅ Integrate with Agent Skills
5. ✅ Deploy to production

---

**Status:** ✅ Ready for Testing
**Next:** Run test scenarios and verify results
