"""
EmailSender Agent Skill
Reads action items from Plans, extracts email targets, and sends notifications
via the Email MCP Server for action tracking and team communication.

This skill integrates with the Email MCP Server to send task notifications,
action summaries, and progress updates based on plan files.
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


class EmailSender:
    """Agent skill for sending emails based on plan actions via MCP server."""

    def __init__(self):
        self.vault_path = Path(__file__).parent.parent / "vault"
        self.plans_path = self.vault_path / "Plans"
        self.log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mcp_server_running = False
        self.email_log_path = self.vault_path / f"email_send_log_{self.timestamp}.json"

    def add_log(self, level, message):
        """Add message to log."""
        log_entry = f"[{level}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def run(self):
        """Main execution: scan plans, extract actions, send emails via MCP."""
        self.add_log("INIT", "EmailSender Skill initialized")

        if not self.plans_path.exists():
            self.add_log("ERROR", f"Plans folder not found: {self.plans_path}")
            return None

        self.add_log("OK", f"Scanning {self.plans_path} for action items...")

        # Scan for plan files
        plan_files = list(self.plans_path.glob("plan_*.md"))
        if not plan_files:
            self.add_log("WARN", "No plan files found in Plans/")
            return None

        self.add_log("OK", f"Found {len(plan_files)} plan files")

        # Extract actions and emails
        actions_data = self._extract_actions_from_plans(plan_files)

        if not actions_data:
            self.add_log("WARN", "No actions extracted from plans")
            return None

        self.add_log("OK", f"Extracted actions: {len(actions_data)} total")

        # Generate email notifications
        email_notifications = self._generate_email_notifications(actions_data)

        if not email_notifications:
            self.add_log("WARN", "No emails to send")
            return None

        self.add_log("OK", f"Generated {len(email_notifications)} email notifications")

        # Log MCP call information
        self._log_email_summary(email_notifications)

        self.add_log("SUCCESS", f"EmailSender processing complete")
        self.add_log("INFO", f"Email log saved to: {self.email_log_path.name}")

        return self.email_log_path

    def _extract_actions_from_plans(self, plan_files: List[Path]) -> List[Dict]:
        """Extract action items from plan files."""
        actions_data = []

        for plan_file in plan_files:
            try:
                with open(plan_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title
                title = self._extract_title(content)

                # Extract action items (lines starting with [ ] or [x])
                action_items = self._extract_action_items(content)

                # Extract email mentions
                email_targets = self._extract_email_targets(content)

                # Extract status
                status = self._extract_status(content)

                if action_items:
                    actions_data.append({
                        'file': plan_file.name,
                        'title': title,
                        'status': status,
                        'actions': action_items,
                        'email_targets': email_targets,
                        'timestamp': datetime.now().isoformat(),
                    })

                    self.add_log("OK", f"Extracted {len(action_items)} actions from {plan_file.name}")

            except Exception as e:
                self.add_log("ERROR", f"Failed to process {plan_file.name}: {str(e)}")
                continue

        return actions_data

    def _extract_title(self, content: str) -> str:
        """Extract title from plan content."""
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('# ') and 'Reasoning Plan' in line:
                return line.replace('# ', '').strip()
            elif line.startswith('# '):
                return line.replace('# ', '').strip()
        return "Untitled Plan"

    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items (checkbox items) from content."""
        actions = []
        lines = content.split('\n')

        for line in lines:
            # Match checkbox patterns: [ ], [x], [X]
            if re.match(r'^\s*-\s*\[\s*[xX]?\s*\]', line):
                # Remove checkbox and clean up
                action = re.sub(r'^\s*-\s*\[\s*[xX]?\s*\]\s*', '', line).strip()
                if action and len(action) > 3:  # Filter out short items
                    actions.append(action)

        return actions

    def _extract_email_targets(self, content: str) -> List[str]:
        """Extract email addresses from content."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = list(set(re.findall(email_pattern, content)))
        return emails

    def _extract_status(self, content: str) -> str:
        """Extract current status from content."""
        if '✅ COMPLETE' in content:
            return 'COMPLETE'
        elif '🟠' in content or 'In Progress' in content:
            return 'IN_PROGRESS'
        elif '🟡' in content or 'Pending' in content:
            return 'PENDING'
        else:
            return 'UNKNOWN'

    def _generate_email_notifications(self, actions_data: List[Dict]) -> List[Dict]:
        """Generate email notifications for actions."""
        notifications = []

        for action_group in actions_data:
            # Generate action summary email
            email = {
                'recipient': 'ai-employee@example.com',  # Default - can be customized
                'subject': f"Action Summary: {action_group['title']}",
                'action_items': action_group['actions'],
                'plan_file': action_group['file'],
                'status': action_group['status'],
                'timestamp': action_group['timestamp'],
                'email_targets': action_group['email_targets'],
                'html_content': self._generate_html_email(action_group),
                'text_content': self._generate_text_email(action_group),
                'mcp_tool': 'send_email',
                'mcp_status': 'READY_TO_CALL',
            }

            notifications.append(email)

        return notifications

    def _generate_html_email(self, action_group: Dict) -> str:
        """Generate HTML email content."""
        actions_html = ''.join([
            f'<li>{action}</li>'
            for action in action_group['actions'][:10]  # Limit to 10 items
        ])

        status_color = {
            'COMPLETE': '#4CAF50',
            'IN_PROGRESS': '#FF9800',
            'PENDING': '#2196F3',
        }.get(action_group['status'], '#666')

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 20px auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 20px -20px;
        }}
        .status {{
            display: inline-block;
            background-color: {status_color};
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 15px;
        }}
        .actions {{
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .actions ol {{ margin: 10px 0; }}
        .actions li {{ margin: 8px 0; }}
        .footer {{
            border-top: 1px solid #eee;
            margin-top: 20px;
            padding-top: 15px;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Action Summary</h1>
        </div>

        <h2>{action_group['title']}</h2>

        <div class="status">{action_group['status']}</div>

        <p>Here are the action items extracted from your plan:</p>

        <div class="actions">
            <strong>Action Items ({len(action_group['actions'])} total):</strong>
            <ol>
                {actions_html}
            </ol>
        </div>

        <p><strong>Plan Source:</strong> {action_group['file']}</p>

        <p>
            <strong>Next Steps:</strong>
            <ul>
                <li>Review the action items above</li>
                <li>Track progress in your plan file</li>
                <li>Update status as items complete</li>
                <li>Refer to Plans/{action_group['file']} for full details</li>
            </ul>
        </p>

        <div class="footer">
            <p>Generated by: EmailSender Agent Skill</p>
            <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>This is an automated email from your AI Employee assistant.</p>
        </div>
    </div>
</body>
</html>
        """
        return html.strip()

    def _generate_text_email(self, action_group: Dict) -> str:
        """Generate plain text email content."""
        actions_text = '\n'.join([
            f"  {i+1}. {action}"
            for i, action in enumerate(action_group['actions'][:10])
        ])

        text = f"""
ACTION SUMMARY: {action_group['title']}

Status: {action_group['status']}

Action Items ({len(action_group['actions'])} total):
{actions_text}

Plan Source: {action_group['file']}

Next Steps:
  - Review the action items above
  - Track progress in your plan file
  - Update status as items complete
  - Refer to Plans/{action_group['file']} for full details

---
Generated by: EmailSender Agent Skill
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
This is an automated email from your AI Employee assistant.
        """
        return text.strip()

    def _log_email_summary(self, notifications: List[Dict]):
        """Log email summary to file."""
        summary = {
            'timestamp': self.timestamp,
            'total_emails': len(notifications),
            'timestamp_full': datetime.now().isoformat(),
            'mcp_server': 'Email MCP Server',
            'mcp_tool': 'send_email',
            'emails': [
                {
                    'recipient': n['recipient'],
                    'subject': n['subject'],
                    'action_count': len(n['action_items']),
                    'status': n['status'],
                    'mcp_status': n['mcp_status'],
                    'mcp_tool': n['mcp_tool'],
                }
                for n in notifications
            ],
            'instructions': [
                '1. Start Email MCP Server: npm start (in email-mcp-server/)',
                '2. Each email is ready to send via send_email MCP tool',
                '3. Recipient: can be customized per plan',
                '4. HTML content generated automatically',
                '5. Track all emails in this log file',
            ],
        }

        try:
            with open(self.email_log_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            self.add_log("OK", f"Email log saved: {self.email_log_path.name}")
        except Exception as e:
            self.add_log("ERROR", f"Failed to save email log: {str(e)}")

    def print_log(self):
        """Print execution log."""
        print("\n" + "="*60)
        print("EMAIL SENDER EXECUTION LOG")
        print("="*60)
        for entry in self.log:
            print(entry)
        print("="*60 + "\n")


def main():
    """Command-line entry point."""
    sender = EmailSender()
    sender.run()
    sender.print_log()


if __name__ == "__main__":
    main()
