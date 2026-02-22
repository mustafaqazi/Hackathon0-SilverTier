# Human Approval Skill

## Purpose
Implement human-in-the-loop approval for sensitive actions. Creates approval request file and waits for human decision.

## Usage
```
python scripts/request_approval.py --action "Send email to john@example.com" --reason "Customer inquiry response"
```

## Parameters
- `--action` (required) - Description of action to approve
- `--reason` (required) - Why this action needs approval
- `--timeout` (default: 3600) - Timeout in seconds (1 hour)
- `--vault-path` - Path to vault (default: ./AI_Employee_Vault/)

## Output
Approved: `APPROVAL_GRANTED: [action] | Approved at [timestamp]`
Rejected: `APPROVAL_REJECTED: [action] | Rejected at [timestamp]`
Timeout: `APPROVAL_TIMEOUT: [action] | No response after [seconds]s`

## Workflow
1. Creates file: `Needs_Approval/REQUEST_[uuid].md`
2. File contains action details and approval instructions
3. Waits for human to modify file with APPROVED/REJECTED
4. Returns status and deletes request file
5. Logs all approvals to approval.log

## Human Instructions
To approve: Edit file, change STATUS to APPROVED
To reject: Edit file, change STATUS to REJECTED

## Notes
- Uses UUID for unique request IDs
- Polls every 2 seconds for updates
- Generates readable approval request documents
- Keeps audit trail in approval.log
- Safe: requires explicit human action
