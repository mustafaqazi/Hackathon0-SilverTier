#!/usr/bin/env python3
"""
TaskAnalyzer Skill
==================
Analyzes tasks, identifies types, detects sensitive content, and routes appropriately.

Category: Task Analysis & Workflow Management
Tier: Bronze
Status: Available
"""

import os
import sys
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Enable UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TaskAnalyzer:
    """Analyzes tasks, detects sensitivity, and routes to appropriate folders."""

    # Task type patterns (filename and content matching)
    TASK_TYPE_PATTERNS = {
        'file_drop': [r'drop', r'upload', r'file.*transfer', r'attachment'],
        'data_processing': [r'data', r'process', r'parse', r'import', r'export'],
        'documentation': [r'doc(?!$)', r'readme', r'guide', r'manual', r'write'],
        'meeting_notes': [r'meeting', r'notes', r'standup', r'sync', r'discussion'],
        'bug_report': [r'bug', r'issue', r'error', r'fix', r'crash'],
        'feature_request': [r'feature', r'request', r'enhancement', r'improvement'],
        'configuration': [r'config', r'setup', r'install', r'deploy', r'environment'],
    }

    # Sensitive keywords by category
    SENSITIVE_KEYWORDS = {
        'financial': [r'payment', r'refund', r'money', r'financial', r'invoice',
                      r'transaction', r'account', r'currency', r'amount'],
        'confidential': [r'confidential', r'secret', r'private', r'proprietary',
                        r'classified', r'restricted', r'sensitive'],
        'approval': [r'approve', r'approval', r'permission', r'access', r'delete',
                     r'authorization', r'authorize', r'grant'],
        'urgent': [r'critical', r'urgent', r'emergency', r'asap', r'immediately',
                   r'time.*sensitive', r'deadline'],
        'security': [r'password', r'credential', r'token', r'api.*key', r'security',
                     r'encrypt', r'hash', r'auth'],
        'personal': [r'personal', r'private data', r'pii', r'ssn', r'phone',
                     r'email.*address', r'home.*address'],
    }

    # Action plan steps by task type (Ralph Wiggum Loop pattern)
    ACTION_STEPS = {
        'file_drop': [
            ('Receive File', 'Accept the file and verify it was uploaded correctly'),
            ('Verify Integrity', 'Check file format, size, and ensure no corruption'),
            ('Extract Metadata', 'Parse file headers and extract key information'),
            ('Store Appropriately', 'Archive file in correct location with documentation'),
        ],
        'data_processing': [
            ('Parse Data', 'Read and parse the data in appropriate format'),
            ('Validate Format', 'Verify data structure matches expected schema'),
            ('Process Records', 'Apply transformations and business logic'),
            ('Generate Report', 'Create summary of processed data with results'),
        ],
        'documentation': [
            ('Review Content', 'Read full document and verify technical accuracy'),
            ('Check Formatting', 'Ensure consistent style, headers, and structure'),
            ('Verify Accuracy', 'Cross-check examples, code, and references'),
            ('Publish', 'Deploy to appropriate documentation platform'),
        ],
        'meeting_notes': [
            ('Summarize Points', 'Extract key discussion points and decisions'),
            ('Extract Actions', 'Identify all action items with owners and dates'),
            ('Assign Owners', 'Verify each action has clear owner and deadline'),
            ('Schedule Follow-up', 'Set calendar reminders and next meeting date'),
        ],
        'bug_report': [
            ('Reproduce Issue', 'Verify the bug occurs in test environment'),
            ('Identify Root Cause', 'Trace code to find underlying problem'),
            ('Create Fix', 'Implement solution and test locally'),
            ('Test Resolution', 'Verify fix works and add test coverage'),
        ],
        'feature_request': [
            ('Analyze Requirement', 'Understand scope and acceptance criteria'),
            ('Design Solution', 'Plan implementation approach and architecture'),
            ('Implement Feature', 'Write code following design specifications'),
            ('Test Thoroughly', 'Verify all requirements and edge cases'),
        ],
        'configuration': [
            ('Gather Settings', 'Collect all required configuration parameters'),
            ('Configure System', 'Apply settings to target environment'),
            ('Validate Setup', 'Test that everything works as expected'),
            ('Document', 'Record configuration details and troubleshooting steps'),
        ],
        'unknown': [
            ('Understand Task', 'Read and comprehend what needs to be done'),
            ('Plan Approach', 'Identify steps needed to complete task'),
            ('Execute Plan', 'Follow the planned approach step by step'),
            ('Verify Completion', 'Confirm task is done and meets requirements'),
        ],
    }

    def __init__(self, base_path: str = None):
        """Initialize TaskAnalyzer."""
        if base_path is None:
            base_path = os.getcwd()

        self.base_path = Path(base_path)
        self.needs_action_folder = self.base_path / "vault" / "Needs_Action"
        self.pending_approval_folder = self.base_path / "vault" / "Pending_Approval"
        self.plans_folder = self.base_path / "vault" / "Plans"
        self.dashboard_file = self.base_path / "vault" / "Dashboard.md"

        self.analysis_log = []
        self.analyzed_count = 0
        self.approval_required_count = 0
        self.error_count = 0

    def log_analysis(self, status: str, message: str):
        """Log analysis operation."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{status}] {timestamp} - {message}"
        self.analysis_log.append(log_entry)

        status_emoji = {
            'ANALYZE': '🔍',
            'SENSITIVE': '⚠️',
            'OK': '✅',
            'LOOP': '🔄',
            'ERROR': '❌',
            'WARN': '⚠️',
            'INFO': 'ℹ️',
            'APPROVE': '📋'
        }
        emoji = status_emoji.get(status, '📝')
        print(f"{emoji} {log_entry}")

    def ralph_wiggum_loop(self, steps: List[Tuple[str, str]]) -> str:
        """
        Implement Ralph Wiggum Loop pattern for multi-step tasks.
        "I'm in danger" → "I'm in a loop" → "Simple repeating check"
        """
        loop_content = "### Ralph Wiggum Loop (Step-by-Step Process)\n\n"
        loop_content += "Simple iterative approach for task processing:\n\n"

        for i, (step_title, step_desc) in enumerate(steps, 1):
            loop_content += f"**Step {i}: {step_title}**\n"
            loop_content += f"- [ ] {step_desc}\n"
            if i < len(steps):
                loop_content += f"- [ ] Verify {step_title} complete before next step\n"
            loop_content += "\n"

        return loop_content

    def analyze_file_type(self, filename: str, content: str) -> str:
        """Identify task type from filename and content."""
        # Check filename first (higher priority)
        filename_lower = filename.lower()

        for task_type, patterns in self.TASK_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower, re.IGNORECASE):
                    self.log_analysis('ANALYZE', f"Task type identified: {task_type} (from filename)")
                    return task_type

        # Check content for headers and keywords
        content_lower = content.lower()
        for task_type, patterns in self.TASK_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    self.log_analysis('ANALYZE', f"Task type identified: {task_type} (from content)")
                    return task_type

        self.log_analysis('ANALYZE', "Task type: unknown (generic task)")
        return 'unknown'

    def check_approval_needed(self, filename: str, content: str) -> Tuple[bool, List[str]]:
        """Check if task requires approval based on sensitive keywords."""
        sensitive_keywords_found = []
        content_lower = content.lower()
        filename_lower = filename.lower()

        # Search in both filename and content
        for category, keywords in self.SENSITIVE_KEYWORDS.items():
            for keyword in keywords:
                if re.search(keyword, content_lower) or re.search(keyword, filename_lower):
                    sensitive_keywords_found.append(f"{keyword} ({category})")

        if sensitive_keywords_found:
            self.log_analysis('SENSITIVE', f"Found sensitive keywords: {', '.join(sensitive_keywords_found[:3])}")
            return True, sensitive_keywords_found

        self.log_analysis('OK', "No sensitive keywords detected - no approval needed")
        return False, []

    def create_action_plan(self, filename: str, task_type: str, content: str,
                         approval_needed: bool) -> Optional[str]:
        """Create task-specific action plan."""
        try:
            # Ensure Plans folder exists
            self.plans_folder.mkdir(parents=True, exist_ok=True)

            # Generate plan filename
            clean_name = filename.replace('.md', '').replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            plan_filename = f"ActionPlan_{task_type}_{timestamp}.md"
            plan_file_path = self.plans_folder / plan_filename

            # Extract title from content
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else filename.replace('.md', '').title()

            # Get action steps for this task type
            steps = self.ACTION_STEPS.get(task_type, self.ACTION_STEPS['unknown'])

            # Create Ralph Wiggum Loop
            ralph_loop = self.ralph_wiggum_loop(steps)

            # Build action plan
            approval_marker = "\n🔴 **[!] PENDING APPROVAL REQUIRED**\n" if approval_needed else ""

            plan_content = f"""# Action Plan: {task_type.replace('_', ' ').title()}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source File:** {filename}
**Task Type:** {task_type}
**Approval Required:** {'YES' if approval_needed else 'NO'}{approval_marker}

## Task Overview

Title: **{title}**

## Task Workflow

{ralph_loop}

## Checkpoint Verification

Use this section to track completion:

- [ ] All steps in Ralph Wiggum Loop completed
- [ ] Each step marked as complete in loop above
- [ ] No blockers or issues remaining
- [ ] Quality review passed
- [ ] Task ready for final approval

## Approval Status

{"⚠️ **AWAITING APPROVAL** - This task contains sensitive content. Requires manager approval, security review, and/or compliance check before proceeding." if approval_needed else "✅ **APPROVED FOR PROCESSING** - No sensitive content detected. Ready to proceed with execution."}

## Notes

- This action plan is task-type specific
- Follow the Ralph Wiggum Loop pattern for consistent execution
- Update checkboxes as you progress through each step
- Document any issues or blockers in this section
- Reach out for clarification if any step is unclear

---
**Status:** {"PENDING APPROVAL" if approval_needed else "READY FOR EXECUTION"}
**Handler:** TaskAnalyzer Skill v1.0
**Pattern:** Ralph Wiggum Loop (Simple repeating check pattern)
"""

            # Write plan file
            with open(plan_file_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            self.log_analysis('LOOP', f"Created action plan: {plan_filename}")
            return plan_filename

        except Exception as e:
            self.log_analysis('ERROR', f"Failed to create action plan: {str(e)}")
            return None

    def move_to_pending_approval(self, filename: str) -> bool:
        """Copy sensitive task to Pending_Approval folder."""
        try:
            source_file = self.needs_action_folder / filename

            # Ensure Pending_Approval folder exists
            self.pending_approval_folder.mkdir(parents=True, exist_ok=True)

            dest_file = self.pending_approval_folder / filename

            # Copy file (don't move - keep original in Needs_Action)
            if source_file.exists():
                shutil.copy2(str(source_file), str(dest_file))
                self.log_analysis('APPROVE', f"Copied to Pending_Approval: {filename}")
                return True
            else:
                self.log_analysis('WARN', f"Source file not found: {filename}")
                return False

        except Exception as e:
            self.log_analysis('ERROR', f"Failed to copy to Pending_Approval: {str(e)}")
            return False

    def update_dashboard(self, filename: str, task_type: str, approval_needed: bool,
                        plan_filename: str):
        """Update Dashboard.md with analysis results."""
        if not self.dashboard_file.exists():
            self.log_analysis('WARN', "Dashboard file not found, skipping update")
            return False

        try:
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_content = f.read()

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            approval_status = "YES" if approval_needed else "NO"

            entry = f"- Analyzed: {filename} - Type: {task_type} - Approval: {approval_status} | Plan: {plan_filename} | Analyzed at {timestamp}"

            # Find TaskAnalyzer Execution Log section or Recent Activity
            log_pattern = r'(## TaskAnalyzer Execution Log.*?\n)'
            recent_pattern = r'(## Recent Activity\n)'

            match = re.search(log_pattern, dashboard_content)
            if not match:
                match = re.search(recent_pattern, dashboard_content)

            if match:
                insertion_point = match.end()
                new_content = (
                    dashboard_content[:insertion_point] +
                    entry + '\n' +
                    dashboard_content[insertion_point:]
                )

                with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.log_analysis('OK', f"Dashboard updated for {filename}")
                return True

            self.log_analysis('WARN', "No suitable section found in Dashboard")
            return False

        except Exception as e:
            self.log_analysis('ERROR', f"Failed to update Dashboard: {str(e)}")
            return False

    def analyze_task(self, filename: str) -> Dict:
        """Execute complete analysis workflow for a single task."""
        print(f"\n{'='*60}")
        print(f"Analyzing: {filename}")
        print(f"{'='*60}")

        # Step 1: Read file
        file_path = self.needs_action_folder / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.log_analysis('OK', f"Read file: {filename}")
        except Exception as e:
            self.log_analysis('ERROR', f"Failed to read {filename}: {str(e)}")
            self.error_count += 1
            return {'success': False, 'error': str(e)}

        # Step 2: Analyze task type
        task_type = self.analyze_file_type(filename, content)

        # Step 3: Check for sensitive content
        approval_needed, sensitive_keywords = self.check_approval_needed(filename, content)
        if approval_needed:
            self.approval_required_count += 1

        # Step 4: Create action plan
        plan_filename = self.create_action_plan(filename, task_type, content, approval_needed)
        if not plan_filename:
            self.error_count += 1

        # Step 5: Route to Pending_Approval if needed
        if approval_needed:
            self.move_to_pending_approval(filename)

        # Step 6: Update Dashboard
        self.update_dashboard(filename, task_type, approval_needed, plan_filename or "N/A")

        self.analyzed_count += 1

        return {
            'success': True,
            'filename': filename,
            'task_type': task_type,
            'approval_needed': approval_needed,
            'sensitive_keywords': sensitive_keywords,
            'plan_filename': plan_filename
        }

    def analyze_all_tasks(self) -> Dict:
        """Analyze all tasks in Needs_Action folder."""
        print("\n" + "="*60)
        print("🚀 TaskAnalyzer Skill Execution")
        print("="*60)

        # Clear log
        self.analysis_log = []
        self.analyzed_count = 0
        self.approval_required_count = 0
        self.error_count = 0

        # Find markdown files
        if not self.needs_action_folder.exists():
            self.log_analysis('ERROR', f"Needs_Action folder not found")
            return {
                'status': 'FAILED',
                'analyzed': 0,
                'approval_required': 0,
                'errors': 1,
                'log': self.analysis_log
            }

        md_files = sorted([f.name for f in self.needs_action_folder.glob('*.md')])
        self.log_analysis('INFO', f"Found {len(md_files)} .md files to analyze")

        # Analyze each file
        analysis_results = []
        for filename in md_files:
            result = self.analyze_task(filename)
            if result['success']:
                analysis_results.append(result)

        # Print summary
        print("\n" + "="*60)
        print("📊 Analysis Summary")
        print("="*60)
        print(f"✅ Total tasks analyzed: {self.analyzed_count}")
        print(f"⚠️  Tasks requiring approval: {self.approval_required_count}")
        print(f"❌ Errors encountered: {self.error_count}")
        print(f"📁 Plans created in: {self.plans_folder}")
        print(f"📋 Sensitive tasks routed: {self.pending_approval_folder}")
        print("="*60 + "\n")

        return {
            'status': 'COMPLETE',
            'analyzed': self.analyzed_count,
            'approval_required': self.approval_required_count,
            'errors': self.error_count,
            'results': analysis_results,
            'log': self.analysis_log
        }


def main():
    """Main entry point for the skill."""
    analyzer = TaskAnalyzer()
    result = analyzer.analyze_all_tasks()
    return result


if __name__ == '__main__':
    main()
