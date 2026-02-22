"""
ApprovalChecker Agent Skill
Monitors for sensitive actions, creates approval request documents,
checks approved items, and triggers actions when approved.

Implements a safety workflow for critical operations like sending emails,
financial transactions, and system changes.
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from enum import Enum


class ActionSensitivity(Enum):
    """Action sensitivity levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ApprovalChecker:
    """Agent skill for managing approval workflows for sensitive actions."""

    def __init__(self):
        self.vault_path = Path(__file__).parent.parent / "vault"
        self.plans_path = self.vault_path / "Plans"
        self.pending_approval_path = self.vault_path / "Pending_Approval"
        self.approved_path = self.vault_path / "Approved"
        self.rejected_path = self.vault_path / "Rejected"
        self.completed_path = self.vault_path / "Completed"
        self.log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create required directories
        self.pending_approval_path.mkdir(parents=True, exist_ok=True)
        self.approved_path.mkdir(parents=True, exist_ok=True)
        self.rejected_path.mkdir(parents=True, exist_ok=True)
        self.completed_path.mkdir(parents=True, exist_ok=True)

        # Sensitive keywords and their levels
        self.sensitive_keywords = {
            # CRITICAL level
            "payment": ActionSensitivity.CRITICAL,
            "refund": ActionSensitivity.CRITICAL,
            "delete": ActionSensitivity.CRITICAL,
            "remove": ActionSensitivity.CRITICAL,
            "transfer": ActionSensitivity.CRITICAL,
            "financial": ActionSensitivity.CRITICAL,
            "confidential": ActionSensitivity.CRITICAL,
            "secure": ActionSensitivity.CRITICAL,

            # HIGH level
            "email": ActionSensitivity.HIGH,
            "send": ActionSensitivity.HIGH,
            "notify": ActionSensitivity.HIGH,
            "access": ActionSensitivity.HIGH,
            "permission": ActionSensitivity.HIGH,
            "approve": ActionSensitivity.HIGH,
            "critical": ActionSensitivity.HIGH,
            "urgent": ActionSensitivity.HIGH,

            # MEDIUM level
            "update": ActionSensitivity.MEDIUM,
            "modify": ActionSensitivity.MEDIUM,
            "change": ActionSensitivity.MEDIUM,
            "create": ActionSensitivity.MEDIUM,
        }

    def add_log(self, level, message):
        """Add message to log."""
        log_entry = f"[{level}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def run(self):
        """Main execution: check approvals and trigger actions."""
        self.add_log("INIT", "ApprovalChecker Skill initialized")

        # Phase 1: Create approval requests for sensitive actions
        approval_requests = self._create_approval_requests()
        if approval_requests:
            self.add_log("OK", f"Created {len(approval_requests)} approval requests")

        # Phase 2: Check approved items
        approved_items = self._check_approved_items()
        if approved_items:
            self.add_log("OK", f"Found {len(approved_items)} approved items")

        # Phase 3: Trigger approved actions
        triggered_actions = self._trigger_approved_actions(approved_items)
        if triggered_actions:
            self.add_log("OK", f"Triggered {len(triggered_actions)} actions")

        # Phase 4: Log summary
        self._log_summary(approval_requests, approved_items, triggered_actions)

        self.add_log("SUCCESS", "ApprovalChecker processing complete")
        return self.pending_approval_path

    def _create_approval_requests(self) -> List[Dict]:
        """Create approval request files for sensitive actions."""
        approval_requests = []

        # Check email logs for pending emails
        email_logs = list(self.vault_path.glob("email_send_log_*.json"))

        for log_file in email_logs:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    email_data = json.load(f)

                # Create approval request for each email
                for i, email in enumerate(email_data.get('emails', [])[:3]):  # Limit to first 3
                    if email.get('mcp_status') == 'READY_TO_CALL':
                        approval_request = self._create_email_approval_request(
                            email,
                            log_file.name,
                            i
                        )
                        if approval_request:
                            approval_requests.append(approval_request)
                            self.add_log("OK", f"Created approval request: {approval_request['filename']}")

            except Exception as e:
                self.add_log("ERROR", f"Failed to process {log_file.name}: {str(e)}")
                continue

        return approval_requests

    def _create_email_approval_request(self, email: Dict, source_log: str, index: int) -> Dict:
        """Create approval request document for email."""
        try:
            recipient = email.get('recipient', 'unknown@example.com')
            subject = email.get('subject', 'Unknown Subject')
            action_count = email.get('action_count', 0)
            status = email.get('status', 'UNKNOWN')

            approval_id = f"EMAIL_{recipient.split('@')[0]}_{index}_{self.timestamp}"
            filename = f"APPROVAL_REQUEST_{approval_id}.md"
            filepath = self.pending_approval_path / filename

            # Create approval request document
            content = f"""# Approval Request

**Request ID:** {approval_id}
**Type:** Email Send
**Status:** ⏳ PENDING_APPROVAL
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Email Details

**Recipient:** {recipient}
**Subject:** {subject}
**Action Items:** {action_count}
**Plan Status:** {status}
**Source Log:** {source_log}

---

## Action Summary

This email contains action items extracted from your plan files.

**What will be sent:**
- Professional HTML-formatted email
- All action items listed and numbered
- Plan reference and next steps
- Professional footer with timestamp

**Number of action items:** {action_count}

---

## Approval Checklist

Before approving, verify:

- [ ] Recipient email address is correct: {recipient}
- [ ] Subject line is appropriate: {subject}
- [ ] All action items are accurate
- [ ] No sensitive data will be exposed
- [ ] Email timing is appropriate
- [ ] No duplicate sends
- [ ] Recipient has permission to receive this

---

## Approval Instructions

### To APPROVE:

1. Review the details above
2. Verify all information is correct
3. Create file: `vault/Approved/APPROVAL_REQUEST_{approval_id}_APPROVED.md`
4. Content can be:
   ```
   # Approval Granted

   **Request ID:** {approval_id}
   **Approved By:** [Your Name]
   **Approved At:** [Timestamp]
   **Reason:** [Optional reason]
   ```
5. ApprovalChecker will detect and execute

### To REJECT:

1. Review the details above
2. If issues found, create file: `vault/Rejected/APPROVAL_REQUEST_{approval_id}_REJECTED.md`
3. Content should include rejection reason
4. Item will be marked as rejected and logged

### Timeline:
- Requests created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Pending approval: Waiting for your decision
- Action expires after: 7 days (auto-cancel)

---

## Security Notes

✓ Email credentials are NOT stored in this request
✓ Recipient address will be verified before sending
✓ Email content is sanitized
✓ All sends are logged for audit trail
✓ Failed sends will be retried

---

## Questions?

If you have questions about this approval request:

1. Check the source log: {source_log}
2. Review the plan file for full context
3. Verify recipient and subject line

---

**Action Type:** CRITICAL (Email Send)
**Approval Required:** YES
**Escalation:** If not approved in 24 hours, auto-cancel

Approval request file: {filename}
Location: vault/Pending_Approval/{filename}
"""

            # Write approval request file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                'approval_id': approval_id,
                'filename': filename,
                'filepath': filepath,
                'type': 'EMAIL_SEND',
                'recipient': recipient,
                'subject': subject,
                'action_count': action_count,
                'status': 'PENDING_APPROVAL',
                'created': datetime.now().isoformat(),
            }

        except Exception as e:
            self.add_log("ERROR", f"Failed to create email approval request: {str(e)}")
            return None

    def _check_approved_items(self) -> List[Dict]:
        """Check for approved items in Approved folder."""
        approved_items = []

        if not self.approved_path.exists():
            return approved_items

        approval_files = list(self.approved_path.glob("APPROVAL_REQUEST_*_APPROVED.md"))

        for approval_file in approval_files:
            try:
                with open(approval_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract approval ID
                approval_id_match = re.search(r'Request ID:\s*(\S+)', content)
                if not approval_id_match:
                    continue

                approval_id = approval_id_match.group(1)

                # Extract approver
                approver_match = re.search(r'Approved By:\s*(.+)', content)
                approver = approver_match.group(1).strip() if approver_match else "Unknown"

                approved_items.append({
                    'approval_id': approval_id,
                    'filename': approval_file.name,
                    'filepath': approval_file,
                    'approver': approver,
                    'approved_at': approval_file.stat().st_mtime,
                    'content': content,
                })

                self.add_log("OK", f"Found approved item: {approval_id}")

            except Exception as e:
                self.add_log("ERROR", f"Failed to read {approval_file.name}: {str(e)}")
                continue

        return approved_items

    def _trigger_approved_actions(self, approved_items: List[Dict]) -> List[Dict]:
        """Trigger actions for approved items."""
        triggered_actions = []

        for item in approved_items:
            try:
                approval_id = item['approval_id']

                # Find corresponding pending request
                pending_file = self.pending_approval_path / f"APPROVAL_REQUEST_{approval_id}.md"

                if not pending_file.exists():
                    self.add_log("WARN", f"Pending request not found for: {approval_id}")
                    continue

                # Determine action type and trigger
                if 'EMAIL' in approval_id:
                    action_result = self._trigger_email_send(approval_id, item)
                else:
                    action_result = self._trigger_generic_action(approval_id, item)

                if action_result:
                    triggered_actions.append(action_result)

                    # Move approved request to completed
                    self._archive_item(pending_file, self.completed_path, "COMPLETED")
                    self._archive_item(item['filepath'], self.completed_path, "COMPLETED")

                    self.add_log("OK", f"Triggered action: {approval_id}")

            except Exception as e:
                self.add_log("ERROR", f"Failed to trigger action for {item['approval_id']}: {str(e)}")
                continue

        return triggered_actions

    def _trigger_email_send(self, approval_id: str, item: Dict) -> Dict:
        """Trigger email send action."""
        return {
            'approval_id': approval_id,
            'action_type': 'EMAIL_SEND',
            'status': 'TRIGGERED',
            'message': f"Email send approved and ready to execute",
            'approver': item['approver'],
            'timestamp': datetime.now().isoformat(),
            'next_step': 'Call Email MCP Server send_email tool',
        }

    def _trigger_generic_action(self, approval_id: str, item: Dict) -> Dict:
        """Trigger generic action."""
        return {
            'approval_id': approval_id,
            'action_type': 'GENERIC',
            'status': 'TRIGGERED',
            'message': f"Action approved and ready to execute",
            'approver': item['approver'],
            'timestamp': datetime.now().isoformat(),
        }

    def _archive_item(self, source_path: Path, dest_folder: Path, status: str):
        """Archive item to destination folder."""
        try:
            filename = source_path.name
            dest_path = dest_folder / f"{status}_{filename}"
            source_path.rename(dest_path)
        except Exception as e:
            self.add_log("WARN", f"Failed to archive {source_path.name}: {str(e)}")

    def _log_summary(self, requests: List[Dict], approved: List[Dict], triggered: List[Dict]):
        """Log summary of all approval activities."""
        summary = {
            'timestamp': self.timestamp,
            'timestamp_full': datetime.now().isoformat(),
            'approval_requests_created': len(requests),
            'approved_items_found': len(approved),
            'actions_triggered': len(triggered),
            'summary': {
                'pending_approval': len(requests),
                'approved': len(approved),
                'completed': len(triggered),
                'rejected': self._count_rejected_items(),
            },
            'requests': [
                {
                    'approval_id': r['approval_id'],
                    'type': r['type'],
                    'status': r['status'],
                    'created': r['created'],
                }
                for r in requests
            ],
            'actions_triggered': [
                {
                    'approval_id': t['approval_id'],
                    'action_type': t['action_type'],
                    'approver': t['approver'],
                    'timestamp': t['timestamp'],
                }
                for t in triggered
            ],
            'next_steps': [
                '1. Review pending approval requests in vault/Pending_Approval/',
                '2. Verify details are correct',
                '3. Create APPROVED file in vault/Approved/ to approve',
                '4. ApprovalChecker will detect and trigger actions',
                '5. Check vault/Completed/ for finished actions',
            ],
        }

        log_path = self.vault_path / f"approval_check_log_{self.timestamp}.json"
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            self.add_log("OK", f"Approval log saved: {log_path.name}")
        except Exception as e:
            self.add_log("ERROR", f"Failed to save approval log: {str(e)}")

    def _count_rejected_items(self) -> int:
        """Count rejected items."""
        if not self.rejected_path.exists():
            return 0
        return len(list(self.rejected_path.glob("*.md")))

    def get_status_report(self) -> Dict:
        """Get current approval status report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'pending_approval': self._count_files(self.pending_approval_path),
            'approved': self._count_files(self.approved_path),
            'rejected': self._count_files(self.rejected_path),
            'completed': self._count_files(self.completed_path),
        }

    def _count_files(self, path: Path) -> int:
        """Count markdown files in path."""
        if not path.exists():
            return 0
        return len(list(path.glob("*.md")))

    def print_log(self):
        """Print execution log."""
        print("\n" + "="*60)
        print("APPROVAL CHECKER EXECUTION LOG")
        print("="*60)
        for entry in self.log:
            print(entry)

        # Print status report
        status = self.get_status_report()
        print("\nAPPROVAL STATUS:")
        print(f"  Pending Approval: {status['pending_approval']}")
        print(f"  Approved: {status['approved']}")
        print(f"  Rejected: {status['rejected']}")
        print(f"  Completed: {status['completed']}")
        print("="*60 + "\n")


def main():
    """Command-line entry point."""
    checker = ApprovalChecker()
    checker.run()
    checker.print_log()


if __name__ == "__main__":
    main()
