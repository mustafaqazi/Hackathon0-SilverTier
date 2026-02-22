# ProcessIncomingItem Skill - Quick Start Guide

## Overview
ProcessIncomingItem automatically processes items from `vault/Needs_Action/` folder and updates your Dashboard with summaries and action items.

---

## Quick Setup

### 1. **Folder Structure**
Ensure this directory structure exists:
```
AI_Employee/
├── vault/
│   ├── Needs_Action/        ← Item files go here (.md files)
│   ├── Dashboard.md          ← Gets updated with entries
│   └── ...
├── .claude/
│   └── skills/
│       └── process-incoming-items/
│           ├── ProcessIncomingItem.py
│           ├── SKILL.md
│           └── QUICK_START.md
```

### 2. **Run the Skill**
```bash
cd AI_Employee
python .claude/skills/process-incoming-items/ProcessIncomingItem.py
```

### 3. **Check Results**
Open `vault/Dashboard.md` and look at **Recent Activity** section

---

## File Format

Items in `vault/Needs_Action/` should be `.md` files with optional YAML frontmatter:

```markdown
---
subject: Clear Title Here
type: financial | email | feature_request | bug_report | documentation | approval_request
priority: CRITICAL | HIGH | MEDIUM | LOW
---

## Description

Your item description here...
```

---

## What It Does

| Step | Action |
|------|--------|
| 1️⃣ | Scans `vault/Needs_Action/` for all `.md` files |
| 2️⃣ | Extracts title, type, priority from YAML metadata |
| 3️⃣ | Creates 1-2 sentence summary from content |
| 4️⃣ | Suggests 3-4 action items based on file type |
| 5️⃣ | Updates `vault/Dashboard.md` Recent Activity section |

---

## Output Example

```
🚀 ProcessIncomingItem Skill Execution
============================================================
📁 Found 5 .md files in Needs_Action

📄 Processing: payment_request_001.md
   Title: Client Payment Processing
   Type: financial
   Priority: CRITICAL

✅ Dashboard updated with 5 new entries

📊 Processing Summary
✅ Total items found: 5
✅ Total items processed: 5
✅ Dashboard updated: YES
```

Dashboard entries added:
```markdown
- 🔴 **Client Payment Processing** - Processing urgent payment... | Actions: [ ] Review payment details [ ] Verify approval [ ] Process transaction
- 🟠 **Security Alert** - Email from Google about account security | Actions: [ ] Read email [ ] Identify action [ ] Respond
- ...
```

---

## Item Type Actions

### 📋 Financial
- [ ] Review payment details and amounts
- [ ] Verify authorization/approval status
- [ ] Process payment transaction
- [ ] Send confirmation to recipient

### 📧 Email
- [ ] Read email content completely
- [ ] Identify action required
- [ ] Compose response if needed
- [ ] Archive or file email

### 💡 Feature Request
- [ ] Analyze feature requirements
- [ ] Check feasibility and dependencies
- [ ] Create implementation plan
- [ ] Schedule development

### 🐛 Bug Report
- [ ] Reproduce the issue
- [ ] Document root cause
- [ ] Implement fix
- [ ] Test and verify resolution

### 📚 Documentation
- [ ] Review documentation needs
- [ ] Draft content
- [ ] Get review and approval
- [ ] Publish and update index

### ✅ Approval Request
- [ ] Review all attached documents
- [ ] Verify all required information
- [ ] Make approval decision
- [ ] Document and notify requester

---

## Scheduling (Automated Execution)

### Windows (Task Scheduler)
```batch
python C:\path\to\AI_Employee\.claude\skills\process-incoming-items\ProcessIncomingItem.py
```
Schedule to run: Every 6 hours

### Linux/Mac (Cron)
```bash
0 */6 * * * cd /path/to/AI_Employee && python .claude/skills/process-incoming-items/ProcessIncomingItem.py
```

---

## Priority Indicators

| Emoji | Priority | Use When |
|-------|----------|----------|
| 🔴 | CRITICAL | Urgent, blocking work |
| 🟠 | HIGH | Important, needs soon |
| 🟡 | MEDIUM | Regular priority |
| 🟢 | LOW | Nice to have |

---

## Common Tasks

### ✨ Add New Item to Process
1. Create `.md` file in `vault/Needs_Action/`
2. Add YAML metadata (optional):
   ```markdown
   ---
   subject: My New Task
   type: feature_request
   priority: HIGH
   ---
   ```
3. Run skill: `python ProcessIncomingItem.py`
4. Check Dashboard Recent Activity

### 🔄 Process Multiple Items
- Just drop `.md` files in `vault/Needs_Action/`
- Run skill once - it processes all files
- Adds all to Dashboard in one batch

### ✅ Mark Action Complete
In Dashboard Recent Activity:
- Find the item's action checkboxes
- Change `[ ]` to `[x]` when you complete it

### 🎯 Find High Priority Items
Look for 🔴 (CRITICAL) emoji in Dashboard Recent Activity

---

## Troubleshooting

**Q: Dashboard not updating?**
A: Check that `vault/Dashboard.md` exists and has `## Recent Activity` section

**Q: Items not found?**
A: Verify files are in `vault/Needs_Action/` with `.md` extension

**Q: Actions don't match item type?**
A: Add `type:` field to YAML frontmatter

**Q: Title extracting incorrectly?**
A: Add `subject:` field to YAML frontmatter, or use `# Title` as first line

---

## Advanced: Integration with Python

```python
from ProcessIncomingItem import ProcessIncomingItem

# Create processor
processor = ProcessIncomingItem(base_path="path/to/AI_Employee")

# Process all items
result = processor.process_all_items()

# Access results
print(f"Processed: {result['processed']} items")
print(f"Total found: {result['total_items']}")

if result['dashboard_updated']:
    print("✅ Dashboard updated successfully")
```

---

## Files Included

- **ProcessIncomingItem.py** - Main skill code
- **SKILL.md** - Full documentation
- **QUICK_START.md** - This file

---

## Next Steps

1. ✅ Create `.md` files in `vault/Needs_Action/`
2. ✅ Run `python ProcessIncomingItem.py`
3. ✅ Check `vault/Dashboard.md` Recent Activity
4. ✅ Work through suggested actions
5. ✅ Move completed items to `vault/Done/`

---

**Version:** 1.0 | **Tier:** Bronze | **Status:** Ready to Use ✅
