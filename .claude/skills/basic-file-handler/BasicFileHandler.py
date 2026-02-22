#!/usr/bin/env python3
"""
BasicFileHandler Skill
======================
Reads, summarizes, and organizes markdown files.
Processes files from Needs_Action, creates action plans, and archives to Done.

Category: File Management & Task Processing
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


class BasicFileHandler:
    """Handles file processing workflow: read → summarize → plan → archive."""

    def __init__(self, base_path: str = None):
        """Initialize with base path."""
        if base_path is None:
            base_path = os.getcwd()

        self.base_path = Path(base_path)
        self.needs_action_folder = self.base_path / "vault" / "Needs_Action"
        self.done_folder = self.base_path / "vault" / "Done"
        self.plans_folder = self.base_path / "vault" / "Plans"
        self.handbook_file = self.base_path / "vault" / "Company_Handbook.md"
        self.dashboard_file = self.base_path / "vault" / "Dashboard.md"

        self.operation_log = []
        self.handbook_rules = {}
        self.processed_count = 0
        self.error_count = 0

    def log_operation(self, status: str, message: str):
        """Log operation with status."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{status}] {timestamp} - {message}"
        self.operation_log.append(log_entry)

        # Color code for console output
        status_emoji = {
            'OK': '✅',
            'ERROR': '❌',
            'WARN': '⚠️',
            'INFO': 'ℹ️'
        }
        emoji = status_emoji.get(status, '📝')
        print(f"{emoji} {log_entry}")

    def check_handbook_rules(self) -> bool:
        """Verify Company_Handbook.md exists and load rules."""
        if not self.handbook_file.exists():
            self.log_operation('WARN', f"Handbook not found: {self.handbook_file}")
            self.log_operation('INFO', "Proceeding without handbook rules")
            return False

        try:
            with open(self.handbook_file, 'r', encoding='utf-8') as f:
                handbook_content = f.read()

            # Extract key rules from handbook
            if '## Rules' in handbook_content or '## Company Rules' in handbook_content:
                rules_section = re.search(r'## (?:Company )?Rules\n(.*?)(?:\n##|$)',
                                         handbook_content, re.DOTALL)
                if rules_section:
                    self.handbook_rules['found'] = True
                    self.log_operation('OK', "Handbook rules loaded successfully")
                    return True

            self.handbook_rules['found'] = False
            self.log_operation('INFO', "Handbook exists but no rules section found")
            return True

        except Exception as e:
            self.log_operation('ERROR', f"Failed to read handbook: {str(e)}")
            return False

    def read_markdown_file(self, file_path: Path) -> Optional[str]:
        """Read markdown file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.log_operation('OK', f"Read file: {file_path.name}")
            return content
        except Exception as e:
            self.log_operation('ERROR', f"Failed to read {file_path.name}: {str(e)}")
            return None

    def extract_metadata(self, content: str) -> Dict:
        """Extract YAML metadata from content."""
        metadata = {}
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        return metadata

    def extract_headers(self, content: str) -> List[str]:
        """Extract headers from markdown content."""
        headers = []
        lines = content.split('\n')

        for line in lines:
            if line.startswith('#'):
                # Remove frontmatter section headers
                if not line.startswith('---'):
                    # Clean up header
                    clean_header = re.sub(r'^#+\s*', '', line).strip()
                    if clean_header and clean_header != '---':
                        headers.append(clean_header)

        return headers

    def extract_key_points(self, content: str, max_points: int = 5) -> List[str]:
        """Extract key points from content."""
        key_points = []

        # Remove YAML frontmatter
        content_without_meta = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Look for bullet points
        bullets = re.findall(r'^\s*[-*]\s+(.+)$', content_without_meta, re.MULTILINE)
        key_points.extend(bullets[:max_points])

        # If not enough, extract first sentences from paragraphs
        if len(key_points) < max_points:
            paragraphs = [p.strip() for p in content_without_meta.split('\n\n')
                         if p.strip() and not p.strip().startswith('#')]
            for para in paragraphs:
                # Get first sentence
                sentences = re.split(r'(?<=[.!?])\s+', para)
                if sentences:
                    first_sentence = sentences[0]
                    if first_sentence and first_sentence not in key_points:
                        key_points.append(first_sentence[:150])  # Limit length
                        if len(key_points) >= max_points:
                            break

        return key_points[:max_points]

    def summarize_content(self, content: str) -> str:
        """Create summary from headers and key points."""
        headers = self.extract_headers(content)
        key_points = self.extract_key_points(content)

        summary = "## Content Summary\n\n"

        if headers:
            summary += "### Structure\n"
            for header in headers[:5]:  # Top 5 headers
                summary += f"- {header}\n"
            summary += "\n"

        if key_points:
            summary += "### Key Points\n"
            for point in key_points:
                summary += f"- {point}\n"
        else:
            summary += "### Key Points\n- No bullet points found in content\n"

        return summary

    def create_action_plan(self, filename: str, content: str) -> Optional[str]:
        """Create action plan file in Plans folder."""
        try:
            # Ensure Plans folder exists
            self.plans_folder.mkdir(parents=True, exist_ok=True)

            # Generate plan filename with timestamp
            clean_name = filename.replace('.md', '').replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            plan_filename = f"Plan_{clean_name}_{timestamp}.md"
            plan_file_path = self.plans_folder / plan_filename

            # Extract metadata and summary
            metadata = self.extract_metadata(content)
            summary = self.summarize_content(content)

            # Create plan content
            plan_content = f"""# Action Plan: {metadata.get('subject', filename.replace('.md', '').title())}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source File:** {filename}
**Type:** {metadata.get('type', 'general')}
**Priority:** {metadata.get('priority', 'MEDIUM')}

## Summary
{summary}

## Action Steps

### Phase 1: Understanding
- [ ] Review the full file content in Needs_Action/{filename}
- [ ] Read all headers and sections
- [ ] Identify key requirements and constraints
- [ ] Note any dependencies or related files

### Phase 2: Analysis
- [ ] Extract main objectives
- [ ] Identify what needs to be done
- [ ] Check for conflicting requirements
- [ ] Document any unclear points

### Phase 3: Planning
- [ ] Create detailed implementation steps
- [ ] Define success criteria
- [ ] Estimate effort/timeline
- [ ] Identify required resources

### Phase 4: Execution
- [ ] Follow the planned steps
- [ ] Document progress
- [ ] Handle any issues that arise
- [ ] Verify completion against success criteria

### Phase 5: Completion
- [ ] Verify all requirements are met
- [ ] Move original file to Done folder
- [ ] Update Dashboard with completion
- [ ] Archive this plan with results

## Notes
- Original file will be moved to Done/ folder after processing
- This plan provides the workflow for handling the task
- Update checkbox progress as you work

---
**Status:** PENDING
**Handler:** BasicFileHandler Skill v1.0
"""

            # Write plan file
            with open(plan_file_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            self.log_operation('OK', f"Created plan: {plan_filename}")
            return plan_filename

        except Exception as e:
            self.log_operation('ERROR', f"Failed to create plan for {filename}: {str(e)}")
            return None

    def move_to_done(self, filename: str) -> bool:
        """Move processed file from Needs_Action to Done folder."""
        try:
            source_file = self.needs_action_folder / filename

            # Ensure Done folder exists
            self.done_folder.mkdir(parents=True, exist_ok=True)

            # Add processed prefix if not already present
            if not filename.startswith('processed_'):
                done_filename = f"processed_{filename}"
            else:
                done_filename = filename

            dest_file = self.done_folder / done_filename

            # Move file
            if source_file.exists():
                shutil.move(str(source_file), str(dest_file))
                self.log_operation('OK', f"Moved to Done: {done_filename}")
                return True
            else:
                self.log_operation('WARN', f"Source file not found: {filename}")
                return False

        except Exception as e:
            self.log_operation('ERROR', f"Failed to move {filename}: {str(e)}")
            return False

    def update_dashboard(self, filename: str, plan_filename: str, success: bool):
        """Update Dashboard.md with processing entry."""
        if not self.dashboard_file.exists():
            self.log_operation('WARN', "Dashboard file not found, skipping update")
            return False

        try:
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_content = f.read()

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if success:
                entry = f"- ✅ **[PROCESSED]** {filename} - Plan created: {plan_filename} at {timestamp} | File moved to Done/"
            else:
                entry = f"- ⚠️ **[PARTIAL]** {filename} - Encountered issues at {timestamp} | Check logs for details"

            # Find Recent Activity section
            recent_activity_pattern = r'(## Recent Activity\n)'
            match = re.search(recent_activity_pattern, dashboard_content)

            if match:
                insertion_point = match.end()
                new_content = (
                    dashboard_content[:insertion_point] +
                    entry + '\n' +
                    dashboard_content[insertion_point:]
                )

                with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                self.log_operation('OK', f"Dashboard updated for {filename}")
                return True

            self.log_operation('WARN', "Recent Activity section not found in Dashboard")
            return False

        except Exception as e:
            self.log_operation('ERROR', f"Failed to update Dashboard: {str(e)}")
            return False

    def process_file(self, filename: str) -> bool:
        """Execute complete workflow for a single file."""
        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print(f"{'='*60}")

        # Step 1: Read file
        file_path = self.needs_action_folder / filename
        content = self.read_markdown_file(file_path)
        if not content:
            self.error_count += 1
            return False

        # Step 2: Create summary
        summary = self.summarize_content(content)
        self.log_operation('OK', "Content summarized")

        # Step 3: Create action plan
        plan_filename = self.create_action_plan(filename, content)
        if not plan_filename:
            self.error_count += 1
            return False

        # Step 4: Move to Done
        move_success = self.move_to_done(filename)
        if not move_success:
            self.error_count += 1

        # Step 5: Update Dashboard
        self.update_dashboard(filename, plan_filename, move_success)

        self.processed_count += 1
        return move_success

    def process_all_files(self) -> Dict:
        """Process all markdown files in Needs_Action folder."""
        print("\n" + "="*60)
        print("🚀 BasicFileHandler Skill Execution")
        print("="*60)

        # Clear operation log
        self.operation_log = []
        self.processed_count = 0
        self.error_count = 0

        # Check handbook
        self.check_handbook_rules()

        # Find markdown files
        if not self.needs_action_folder.exists():
            self.log_operation('ERROR', f"Needs_Action folder not found: {self.needs_action_folder}")
            return {
                'status': 'FAILED',
                'processed': 0,
                'errors': 1,
                'log': self.operation_log
            }

        md_files = sorted([f for f in self.needs_action_folder.glob('*.md')])
        self.log_operation('INFO', f"Found {len(md_files)} .md files in Needs_Action")

        # Process each file
        for file_path in md_files:
            self.process_file(file_path.name)

        # Print summary
        print("\n" + "="*60)
        print("📊 Processing Summary")
        print("="*60)
        print(f"✅ Total files processed: {self.processed_count}")
        print(f"❌ Errors encountered: {self.error_count}")
        print(f"📁 Plans created in: {self.plans_folder}")
        print(f"📦 Files archived in: {self.done_folder}")
        print("="*60 + "\n")

        return {
            'status': 'COMPLETE',
            'processed': self.processed_count,
            'errors': self.error_count,
            'log': self.operation_log,
            'handbook_loaded': bool(self.handbook_rules.get('found'))
        }


def main():
    """Main entry point for the skill."""
    handler = BasicFileHandler()
    result = handler.process_all_files()
    return result


if __name__ == '__main__':
    main()
