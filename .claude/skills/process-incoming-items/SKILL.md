# ProcessIncomingItem Skill - BRONZE Tier

## Skill Overview

**ProcessIncomingItem** automatically scans the `vault/Needs_Action/` folder for markdown files, analyzes each item, creates concise summaries, suggests next actions, and updates the Dashboard with new entries. This skill keeps your task dashboard current and ensures nothing falls through the cracks.

**Category:** Task Management & Automation
**Tier:** Bronze
**Status:** Available

---

## How It Works

### Step 1: Scan Needs_Action Folder
- Finds all `.md` files in `vault/Needs_Action/`
- Logs the total number of files found
- Prepares each file for processing

### Step 2: Analyze Each Item
For every `.md` file, the skill:

1. **Extracts metadata** from YAML frontmatter (if present)
2. **Determines the title** from:
   - YAML `subject` or `title` field (preferred)
   - First H1 or H2 heading
   - Filename (fallback)
3. **Creates a summary** - 1-2 sentence concise description
4. **Suggests actions** - 3-4 checkbox-based next steps tailored to item type

### Step 3: Categorize by Type
Actions are suggested based on the file's `type` field:

| Type | Suggested Actions |
|------|-------------------|
| `financial` | Review details • Verify approval • Process transaction • Send confirmation |
| `email` | Read email • Identify action • Compose response • Archive/file |
| `feature_request` | Analyze requirements • Check feasibility • Create plan • Schedule dev |
| `bug_report` | Reproduce issue • Document root cause • Implement fix • Test solution |
| `documentation` | Review needs • Draft content • Get approval • Publish |
| `approval_request` | Review documents • Verify info • Make decision • Notify requester |
| `general` | Read item • Identify actions • Plan next steps • Execute |

### Step 4: Update Dashboard
Adds formatted entries to `vault/Dashboard.md` Recent Activity section with:
- **Emoji indicator** (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)
- **Item title and summary**
- **Suggested action checkboxes**
- **Timestamp** of processing

---

## Usage

### Manual Execution

```bash
# Run the skill directly
python .claude/skills/process-incoming-items/ProcessIncomingItem.py
```

### Automated (Scheduled)

Add to your scheduler/cron job to run periodically:

```bash
# Run every 6 hours
0 */6 * * * cd /path/to/AI_Employee && python .claude/skills/process-incoming-items/ProcessIncomingItem.py
```

### Using Claude Code Agents

This skill can be invoked by agents to process items:

```python
from ProcessIncomingItem import ProcessIncomingItem

processor = ProcessIncomingItem(base_path="/path/to/AI_Employee")
result = processor.process_all_items()

# Access results
print(f"Processed: {result['processed']} items")
print(f"Dashboard updated: {result['dashboard_updated']}")
```

---

## Input Requirements

**No manual input required.** The skill automatically:
- ✅ Scans `vault/Needs_Action/` folder
- ✅ Reads all `.md` files
- ✅ Extracts metadata from YAML frontmatter
- ✅ Analyzes file content

---

## Output Provided

### Console Output
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
============================================================
✅ Total items found: 5
✅ Total items processed: 5
✅ Dashboard updated: YES

📋 Processed Items:
  - Client Payment Processing [CRITICAL]
  - Bug Report: Login Page [HIGH]
  - Feature Request: Dark Mode [MEDIUM]
  - Documentation Update [LOW]
  - Customer Notification Email [HIGH]
============================================================
```

### Dashboard Updates
New entries are added to `vault/Dashboard.md` Recent Activity:

```markdown
## Recent Activity
- 🔴 **Client Payment Processing** - Processing urgent payment for completed project... | Actions: [ ] Review payment details and amounts [ ] Verify authorization/approval status [ ] Process payment transaction
- 🟠 **Bug Report: Login Page** - Fix login button styling to match design system... | Actions: [ ] Reproduce the issue [ ] Document root cause [ ] Implement fix
- 📋 **Feature Request: Dark Mode** - Add dark theme toggle to UI... | Actions: [ ] Analyze feature requirements [ ] Check feasibility and dependencies [ ] Create implementation plan
- ✅ **ProcessIncomingItem executed** - Processed 3 items at 2026-02-20 10:30:45
```

---

## Output Structure

The skill returns a dictionary:

```python
{
    'status': 'COMPLETE',
    'total_items': 5,
    'processed': 5,
    'dashboard_updated': True,
    'items': [
        {
            'filename': 'payment_request_001.md',
            'title': 'Client Payment Processing',
            'summary': 'Processing urgent payment for completed project deliverables...',
            'priority': 'CRITICAL',
            'type': 'financial',
            'actions': [
                '[ ] Review payment details and amounts',
                '[ ] Verify authorization/approval status',
                '[ ] Process payment transaction',
                '[ ] Send confirmation to recipient'
            ],
            'metadata': {
                'id': 'payment_001',
                'subject': 'Client Payment Processing',
                'type': 'financial',
                'priority': 'CRITICAL',
                'created': '2026-02-16'
            }
        }
    ]
}
```

---

## File Format Requirements

Items in `vault/Needs_Action/` should follow this structure:

### Recommended Format (with YAML Frontmatter)

```markdown
---
id: unique_identifier
subject: Clear Title for the Item
type: financial | email | feature_request | bug_report | documentation | approval_request | general
priority: CRITICAL | HIGH | MEDIUM | LOW
created: 2026-02-20
---

## Description

Detailed description of what needs attention or action.

**Key Details:**
- Detail 1
- Detail 2
- Detail 3

**Next Steps:**
(User-provided suggestions, skill will override with standard actions)
```

### Minimal Format

```markdown
# Item Title

Description of what needs attention...
```

---

## How It Extracts Information

### Title Extraction Priority
1. **YAML `subject` field** (highest priority)
2. **YAML `title` field**
3. **First H1 heading (`#`)**
4. **First H2 heading (`##`)**
5. **Filename** (lowest priority)

### Summary Creation
- Takes first 1-2 meaningful paragraphs from content
- Removes YAML frontmatter
- Limits to ~150 characters
- Filters out headers and empty lines

### Metadata Extraction
- Parses YAML frontmatter automatically
- Looks for `type`, `priority`, `subject`, `id`, `created` fields
- Uses metadata to suggest relevant actions

---

## Priority Indicators

The skill uses emoji to indicate priority in Dashboard entries:

| Emoji | Priority | Color |
|-------|----------|-------|
| 🔴 | CRITICAL | Red |
| 🟠 | HIGH | Orange |
| 🟡 | MEDIUM | Yellow |
| 🟢 | LOW | Green |

---

## Common Use Cases

### Use Case 1: Regular Inbox Processing
Schedule the skill to run every 6 hours. It automatically:
- Discovers new items in Needs_Action
- Creates summaries and action items
- Updates Dashboard for visibility

### Use Case 2: Integration with Workflows
Invoke from other agents/skills:
```python
processor = ProcessIncomingItem()
result = processor.process_all_items()
if result['processed'] > 0:
    # Trigger next workflow step
```

### Use Case 3: Manual Review & Action
Users can:
1. Run the skill to update Dashboard
2. Review Recent Activity entries
3. Copy action items to their todo tracker
4. Check off items as they complete them

---

## Error Handling

| Error | Handling |
|-------|----------|
| Needs_Action folder not found | Gracefully exits, returns 0 items |
| .md file read error | Skips file, logs error, continues |
| Dashboard file not found | Skips dashboard update, logs warning |
| Invalid YAML frontmatter | Uses fallback title extraction |
| Unrecognized item type | Uses generic action suggestions |

---

## Best Practices

1. **Keep titles clear** - Use YAML `subject` field for best results
2. **Add item type** - Helps skill suggest relevant actions
3. **Set priority** - Controls emoji indicator (helps prioritize work)
4. **Use consistent format** - Frontmatter + markdown content works best
5. **Review dashboard regularly** - Check Recent Activity section daily
6. **Check off actions** - Mark [ ] as [x] when completed

---

## Troubleshooting

### Dashboard not updating?
- Verify `vault/Dashboard.md` exists
- Check that `## Recent Activity` section is present
- Ensure write permissions to the file

### Actions don't match item type?
- Check that `type` field is set correctly in YAML frontmatter
- Supported types: `financial`, `email`, `feature_request`, `bug_report`, `documentation`, `approval_request`, `general`

### Title not extracting correctly?
- Add YAML `subject` field for explicit title
- Or use H1 heading (`# Title`) as first line
- Avoid using filename alone - it's the fallback option

### Items not being found?
- Verify files are in `vault/Needs_Action/` folder
- Confirm files have `.md` extension
- Check file read permissions

---

## Integration Notes

- **Works with**: File system watchers, task planners, approval workflows
- **Updates**: Dashboard.md (Recent Activity section)
- **Reads from**: vault/Needs_Action/ folder
- **Frequency**: Can run multiple times without duplication issues
- **Safe**: Appends to dashboard, doesn't overwrite existing content

---

## Version History

- **v1.0** (2026-02-20) - Initial release
  - Scan Needs_Action folder
  - Extract metadata from YAML frontmatter
  - Create summaries and suggest actions
  - Update Dashboard with entries
  - Support for 6 item types
  - Priority-based emoji indicators

---

## Next Steps

After running ProcessIncomingItem:

1. ✅ Check `vault/Dashboard.md` Recent Activity section
2. ✅ Review suggested actions for each item
3. ✅ Identify which items are highest priority
4. ✅ Create action plans for critical items
5. ✅ Move completed items to `vault/Done/` folder
6. ✅ Archive processed items appropriately

---

**Skill Type:** Automation | **Execution Mode:** Standalone/Scheduled | **Requires Approval:** NO
