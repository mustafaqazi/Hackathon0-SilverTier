#!/usr/bin/env python3
"""
ProcessIncomingItem Skill
========================
Scans Needs_Action folder for .md files and processes each item.
Creates summaries, suggests next actions, and updates Dashboard.md.

Category: Task Management & Automation
Tier: Bronze
Status: Available
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# Enable UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class ProcessIncomingItem:
    """Processes incoming items from Needs_Action folder."""

    def __init__(self, base_path: str = None):
        """Initialize with base path."""
        if base_path is None:
            # Default to current working directory
            base_path = os.getcwd()

        self.base_path = Path(base_path)
        self.needs_action_folder = self.base_path / "vault" / "Needs_Action"
        self.dashboard_file = self.base_path / "vault" / "Dashboard.md"
        self.processed_items = []

    def find_md_files(self) -> List[Path]:
        """Find all .md files in Needs_Action folder."""
        if not self.needs_action_folder.exists():
            print(f"❌ Needs_Action folder not found at {self.needs_action_folder}")
            return []

        md_files = sorted(self.needs_action_folder.glob("*.md"))
        print(f"📁 Found {len(md_files)} .md files in Needs_Action")
        return md_files

    def extract_metadata(self, content: str) -> Dict:
        """Extract YAML frontmatter metadata from content."""
        metadata = {}

        # Look for YAML frontmatter
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        return metadata

    def extract_title(self, filename: str, content: str) -> str:
        """Extract title from file."""
        metadata = self.extract_metadata(content)

        # Try metadata first
        if 'subject' in metadata:
            return metadata['subject']
        if 'title' in metadata:
            return metadata['title']

        # Try first H1 or H2
        h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1)

        h2_match = re.search(r'^## (.+)$', content, re.MULTILINE)
        if h2_match:
            return h2_match.group(1)

        # Fallback to filename without extension
        return filename.replace('.md', '').replace('_', ' ').title()

    def create_summary(self, content: str) -> str:
        """Create a concise 1-2 sentence summary."""
        metadata = self.extract_metadata(content)

        # Remove YAML frontmatter
        content_without_meta = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Get first meaningful paragraph
        lines = [l.strip() for l in content_without_meta.split('\n') if l.strip()]

        # Skip headers and empty lines
        meaningful_lines = []
        for line in lines:
            if not line.startswith('#') and line:
                meaningful_lines.append(line)
                if len(meaningful_lines) >= 2:
                    break

        if meaningful_lines:
            summary = ' '.join(meaningful_lines[:2])
            # Limit to ~150 chars
            if len(summary) > 150:
                summary = summary[:147] + '...'
            return summary

        return "Item pending processing"

    def suggest_actions(self, filename: str, metadata: Dict) -> List[str]:
        """Suggest 3-4 next actions based on file type."""
        file_type = metadata.get('type', 'general').lower()
        priority = metadata.get('priority', 'MEDIUM').upper()

        actions = {
            'financial': [
                '[ ] Review payment details and amounts',
                '[ ] Verify authorization/approval status',
                '[ ] Process payment transaction',
                '[ ] Send confirmation to recipient'
            ],
            'email': [
                '[ ] Read email content completely',
                '[ ] Identify action required',
                '[ ] Compose response if needed',
                '[ ] Archive or file email'
            ],
            'feature_request': [
                '[ ] Analyze feature requirements',
                '[ ] Check feasibility and dependencies',
                '[ ] Create implementation plan',
                '[ ] Schedule development'
            ],
            'bug_report': [
                '[ ] Reproduce the issue',
                '[ ] Document root cause',
                '[ ] Implement fix',
                '[ ] Test and verify resolution'
            ],
            'documentation': [
                '[ ] Review documentation needs',
                '[ ] Draft content',
                '[ ] Get review and approval',
                '[ ] Publish and update index'
            ],
            'approval_request': [
                '[ ] Review all attached documents',
                '[ ] Verify all required information',
                '[ ] Make approval decision',
                '[ ] Document and notify requester'
            ]
        }

        # Return type-specific actions or defaults
        default_actions = [
            '[ ] Read item completely',
            '[ ] Identify required actions',
            '[ ] Plan next steps',
            '[ ] Execute plan'
        ]

        return actions.get(file_type, default_actions)

    def process_item(self, file_path: Path) -> Dict:
        """Process a single item file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = self.extract_metadata(content)
            title = self.extract_title(file_path.name, content)
            summary = self.create_summary(content)
            actions = self.suggest_actions(file_path.name, metadata)

            item_data = {
                'filename': file_path.name,
                'title': title,
                'summary': summary,
                'metadata': metadata,
                'actions': actions,
                'priority': metadata.get('priority', 'MEDIUM').upper(),
                'type': metadata.get('type', 'general').lower()
            }

            return item_data

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            return None

    def format_dashboard_entry(self, item: Dict) -> str:
        """Format item as a dashboard entry."""
        title = item['title']
        summary = item['summary']
        actions_text = ' | '.join(item['actions'][:3])  # Take first 3 actions
        priority_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        emoji = priority_emoji.get(item['priority'], '📋')

        entry = f"{emoji} **{title}** - {summary} | Actions: {actions_text}"
        return entry

    def update_dashboard(self, items: List[Dict]) -> bool:
        """Update Dashboard.md with new entries."""
        if not items:
            return True

        if not self.dashboard_file.exists():
            print(f"❌ Dashboard file not found at {self.dashboard_file}")
            return False

        try:
            with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_content = f.read()

            # Find Recent Activity section
            recent_activity_pattern = r'(## Recent Activity\n)'
            match = re.search(recent_activity_pattern, dashboard_content)

            if not match:
                print("⚠️  Recent Activity section not found in Dashboard")
                return False

            # Prepare new entries
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entries = []

            for item in items:
                entry = self.format_dashboard_entry(item)
                new_entries.append(f"- {entry}")

            # Add processing summary
            summary_line = f"- ✅ **ProcessIncomingItem executed** - Processed {len(items)} items at {timestamp}"
            new_entries.append(summary_line)

            # Insert entries after Recent Activity header
            insertion_point = match.end()
            new_content = (
                dashboard_content[:insertion_point] +
                '\n'.join(new_entries) + '\n' +
                dashboard_content[insertion_point:]
            )

            # Write updated content
            with open(self.dashboard_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ Dashboard updated with {len(items)} new entries")
            return True

        except Exception as e:
            print(f"❌ Error updating Dashboard: {str(e)}")
            return False

    def process_all_items(self) -> Dict:
        """Process all items in Needs_Action folder."""
        print("\n" + "="*60)
        print("🚀 ProcessIncomingItem Skill Execution")
        print("="*60)

        # Find all .md files
        md_files = self.find_md_files()

        if not md_files:
            print("\n✅ No items to process")
            return {
                'status': 'COMPLETE',
                'total_items': 0,
                'processed': 0,
                'items': []
            }

        # Process each item
        processed_items = []
        for file_path in md_files:
            print(f"\n📄 Processing: {file_path.name}")
            item = self.process_item(file_path)
            if item:
                processed_items.append(item)
                print(f"   Title: {item['title']}")
                print(f"   Type: {item['type']}")
                print(f"   Priority: {item['priority']}")

        # Update dashboard
        if processed_items:
            self.update_dashboard(processed_items)

        # Generate summary
        print("\n" + "="*60)
        print("📊 Processing Summary")
        print("="*60)
        print(f"✅ Total items found: {len(md_files)}")
        print(f"✅ Total items processed: {len(processed_items)}")
        print(f"✅ Dashboard updated: YES" if processed_items else "⚠️  No items to update")

        # Print processed items summary
        if processed_items:
            print("\n📋 Processed Items:")
            for item in processed_items:
                print(f"  - {item['title']} [{item['priority']}]")

        print("\n" + "="*60)

        return {
            'status': 'COMPLETE',
            'total_items': len(md_files),
            'processed': len(processed_items),
            'items': processed_items,
            'dashboard_updated': len(processed_items) > 0
        }


def main():
    """Main entry point for the skill."""
    processor = ProcessIncomingItem()
    result = processor.process_all_items()
    return result


if __name__ == '__main__':
    main()
