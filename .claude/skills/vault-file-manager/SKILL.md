# Vault File Manager Skill

## Purpose
Manage task workflow files across vault folders (Inbox → Needs_Action → Done).

## Usage
```
python scripts/move_task.py --source Inbox --destination Needs_Action --file task.md
python scripts/move_task.py --action list --folder Inbox
```

## Parameters
- `--action` - "move", "list", "copy" (default: move)
- `--source` - Source folder: Inbox|Needs_Action|Done
- `--destination` - Target folder: Inbox|Needs_Action|Done
- `--file` - Filename to move (required for move/copy)
- `--folder` - Folder to list (for --action list)
- `--vault-path` - Path to vault (default: ./AI_Employee_Vault/)

## Output
Move: `TASK_MOVED: task.md | From: Inbox → To: Needs_Action`
List: `TASKS_IN_[FOLDER]: count | [file1.md, file2.md, ...]`
Error: `VAULT_ERROR: [error message]`

## Vault Structure
```
AI_Employee_Vault/
  ├── Inbox/          (new tasks)
  ├── Needs_Action/   (tasks awaiting review)
  ├── Done/           (completed tasks)
  └── Needs_Approval/ (awaiting approval)
```

## Notes
- Supports relative and absolute paths
- Preserves file modification times
- Logs operations to vault.log
- Creates folders if they don't exist
- Safe: prevents overwriting by default
