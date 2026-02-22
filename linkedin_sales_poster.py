"""
LinkedInSalesPoster Skill
Generates LinkedIn sales posts from Needs_Action folder content
"""

import os
import re
from datetime import datetime
from pathlib import Path


class LinkedInSalesPoster:
    """
    Reads sales-related .md files from Needs_Action folder
    Generates professional LinkedIn posts with hashtags
    Creates plan document with draft posts
    """

    def __init__(self):
        self.base_path = Path("vault")
        self.needs_action_dir = self.base_path / "Needs_Action"
        self.plans_dir = self.base_path / "Plans"
        self.posts = []
        self.log = []

        # Ensure directories exist
        self.plans_dir.mkdir(parents=True, exist_ok=True)

    def add_log(self, message):
        """Add log entry with timestamp"""
        self.log.append(message)
        print(message)

    def is_sales_related(self, filename: str, content: str) -> bool:
        """Check if file is sales-related based on filename and content"""
        sales_keywords = [
            "sales", "customer", "notification", "service", "offer",
            "promotion", "product", "announcement", "feature", "launch",
            "business", "revenue", "invoice", "payment", "deal",
            "closing", "pipeline", "opportunity", "pitch"
        ]

        filename_lower = filename.lower()
        content_lower = content.lower()

        for keyword in sales_keywords:
            if keyword in filename_lower or keyword in content_lower:
                return True
        return False

    def extract_key_info(self, filename: str, content: str) -> dict:
        """Extract key information from file content"""
        info = {
            "filename": filename,
            "title": self._extract_title(content),
            "description": self._extract_description(content),
            "features": self._extract_features(content),
            "cta": self._extract_cta(content),
        }
        return info

    def _extract_title(self, content: str) -> str:
        """Extract title/main heading from content"""
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('#') and not line.startswith('##'):
                return line.replace('#', '').strip()
        return "New Sales Opportunity"

    def _extract_description(self, content: str) -> str:
        """Extract key description from content"""
        # Look for description or summary sections
        if "summary" in content.lower():
            match = re.search(r'summary[:\s]+([^\n]+)', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Get first substantial paragraph
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                return line[:150] + "..." if len(line) > 150 else line

        return "Exciting new business opportunity"

    def _extract_features(self, content: str) -> list:
        """Extract key features/benefits from content"""
        features = []
        lines = content.split('\n')

        in_features = False
        for line in lines:
            if 'feature' in line.lower() or 'benefit' in line.lower():
                in_features = True
            if in_features and (line.strip().startswith('-') or line.strip().startswith('•')):
                feature = line.strip().lstrip('-•').strip()
                if feature and len(feature) > 5:
                    features.append(feature)

        # Also check for bullet points mentioning key attributes
        if not features:
            for line in lines:
                if line.strip().startswith('-') or line.strip().startswith('•'):
                    item = line.strip().lstrip('-•').strip()
                    if item and len(item) > 10:
                        features.append(item)

        return features[:3]  # Return top 3

    def _extract_cta(self, content: str) -> str:
        """Extract call-to-action from content"""
        cta_patterns = [
            r'contact.*?(.*?)(?=\n|$)',
            r'reach out.*?(.*?)(?=\n|$)',
            r'learn more.*?(.*?)(?=\n|$)',
        ]

        for pattern in cta_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Get in touch for more information!"

    def generate_post(self, info: dict) -> str:
        """Generate LinkedIn post from extracted info"""
        title = info.get("title", "New Opportunity")
        description = info.get("description", "")
        features = info.get("features", [])
        cta = info.get("cta", "")

        # Build the post
        lines = [
            "🎯 " + title,
            "",
            description,
            "",
        ]

        # Add features as bullet points
        if features:
            lines.append("Key highlights:")
            for feature in features:
                lines.append(f"✓ {feature}")
            lines.append("")

        # Add CTA and hashtags
        lines.append(cta)
        lines.append("")
        lines.extend([
            "#Sales #Business #Growth #Opportunity #Innovation",
            "#Collaboration #Success #Marketplace",
        ])

        return "\n".join(lines)

    def scan_and_process(self):
        """Scan Needs_Action folder and process sales-related files"""
        if not self.needs_action_dir.exists():
            self.add_log(f"[ERROR] Directory not found: {self.needs_action_dir}")
            return False

        self.add_log(f"[START] Scanning {self.needs_action_dir} for sales-related files...")

        md_files = list(self.needs_action_dir.glob("*.md"))
        if not md_files:
            self.add_log("[WARNING] No .md files found in Needs_Action")
            return False

        processed_count = 0

        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if self.is_sales_related(file_path.name, content):
                    self.add_log(f"[SALES] Processing: {file_path.name}")

                    info = self.extract_key_info(file_path.name, content)
                    post = self.generate_post(info)

                    self.posts.append({
                        "source": file_path.name,
                        "info": info,
                        "post": post,
                    })

                    processed_count += 1
                    self.add_log(f"[OK] Generated LinkedIn post for: {file_path.name}")

            except Exception as e:
                self.add_log(f"[ERROR] Failed to process {file_path.name}: {str(e)}")

        self.add_log(f"[RESULT] Processed {processed_count} sales-related files")
        return processed_count > 0

    def create_plan_document(self) -> str:
        """Create comprehensive plan document with all generated posts"""
        if not self.posts:
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"LinkedInSalesPostPlan_{timestamp}.md"
        plan_path = self.plans_dir / plan_filename

        # Build document
        lines = [
            "# LinkedIn Sales Posts Plan",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Posts:** {len(self.posts)}",
            "",
            "---",
            "",
        ]

        for idx, post_data in enumerate(self.posts, 1):
            lines.extend([
                f"## Post #{idx}",
                f"**Source File:** {post_data['source']}",
                f"**Title:** {post_data['info'].get('title', 'N/A')}",
                f"**Status:** 📋 Draft - Ready for Review",
                "",
                "### Draft Post",
                "",
                "```",
                post_data['post'],
                "```",
                "",
                "### Post Analysis",
                f"- **Description:** {post_data['info'].get('description', 'N/A')}",
                "- **Features Highlighted:** " + ", ".join(post_data['info'].get('features', ['N/A'])),
                f"- **Call-to-Action:** {post_data['info'].get('cta', 'N/A')}",
                "",
                "### Posting Checklist",
                "- [ ] Review post content for accuracy",
                "- [ ] Verify hashtags are relevant",
                "- [ ] Check links and references",
                "- [ ] Confirm tone matches brand voice",
                "- [ ] Schedule post (or post immediately)",
                "- [ ] Monitor engagement",
                "",
                "---",
                "",
            ])

        # Add summary
        lines.extend([
            "## Summary & Next Steps",
            "",
            f"✅ Generated {len(self.posts)} LinkedIn post(s) from sales-related files",
            "",
            "### Recommended Actions",
            "1. Review all draft posts above",
            "2. Adjust content as needed for your brand voice",
            "3. Add specific links or contact information",
            "4. Schedule posts at optimal times",
            "5. Track engagement metrics",
            "",
            "### Best Practices",
            "- Post between 8-10 AM or 5-6 PM on weekdays",
            "- Engage with comments within 1 hour of posting",
            "- Use 3-5 relevant hashtags per post",
            "- Include visuals when possible",
            "",
            f"**Plan saved at:** {plan_path}",
        ])

        # Write file
        try:
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            self.add_log(f"[SUCCESS] Plan created: {plan_path}")
            return str(plan_path)

        except Exception as e:
            self.add_log(f"[ERROR] Failed to create plan: {str(e)}")
            return ""

    def print_log(self):
        """Print all log entries"""
        print("\n" + "=" * 60)
        print("LINKEDIN SALES POSTER - EXECUTION LOG")
        print("=" * 60)
        for entry in self.log:
            print(entry)
        print("=" * 60 + "\n")

    def run(self):
        """Main execution method"""
        self.add_log("[INIT] LinkedInSalesPoster Skill initialized")
        success = self.scan_and_process()

        if success:
            plan_path = self.create_plan_document()
            self.add_log(f"[COMPLETE] Process finished - {len(self.posts)} post(s) created")
            return plan_path
        else:
            self.add_log("[WARNING] No sales-related files processed")
            return None


def main():
    """Command-line entry point"""
    poster = LinkedInSalesPoster()
    result = poster.run()
    poster.print_log()

    if result:
        print(f"[SUCCESS] Plan document created: {result}")
    else:
        print("[WARNING] No plan generated")


if __name__ == "__main__":
    main()
