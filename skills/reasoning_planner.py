"""
ReasoningPlanner Agent Skill
Reads files from Needs_Action, performs step-by-step reasoning (think, plan, actions),
and saves detailed reasoning plans to Plans/ with checkboxes and Ralph Wiggum Loop.
"""

import os
import sys
from datetime import datetime
from pathlib import Path


class ReasoningPlanner:
    """Agent skill for step-by-step reasoning planning with Ralph Wiggum Loop."""

    def __init__(self):
        self.vault_path = Path(__file__).parent.parent / "vault"
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.plans_path = self.vault_path / "Plans"
        self.log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def add_log(self, level, message):
        """Add message to log."""
        log_entry = f"[{level}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def run(self):
        """Main execution: scan, analyze, and generate reasoning plans."""
        self.add_log("INIT", "ReasoningPlanner Skill initialized")

        if not self.needs_action_path.exists():
            self.add_log("ERROR", f"Needs_Action folder not found: {self.needs_action_path}")
            return None

        self.plans_path.mkdir(parents=True, exist_ok=True)
        self.add_log("OK", f"Scanning {self.needs_action_path} for files...")

        md_files = list(self.needs_action_path.glob("*.md"))
        if not md_files:
            self.add_log("WARN", "No markdown files found in Needs_Action/")
            return None

        processed_count = 0
        for file_path in md_files:
            plan_path = self._process_file(file_path)
            if plan_path:
                processed_count += 1
                self.add_log("OK", f"Generated reasoning plan: {plan_path.name}")

        self.add_log("SUCCESS", f"Processed {processed_count} file(s)")

        if processed_count > 0:
            self.add_log("COMPLETE", "ReasoningPlanner execution finished")
            return self.plans_path

        return None

    def _process_file(self, file_path):
        """Process a single file and generate reasoning plan."""
        try:
            filename = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                self.add_log("SKIP", f"File is empty: {file_path.name}")
                return None

            # Extract title and description
            title = self._extract_title(content)
            description = self._extract_description(content)

            # Generate reasoning steps
            reasoning = self._generate_reasoning(title, description, content)

            # Create plan document with Ralph Wiggum Loop
            plan_content = self._create_plan_document(
                filename, title, description, reasoning, content
            )

            # Save plan
            plan_filename = f"plan_{filename}_{self.timestamp}.md"
            plan_path = self.plans_path / plan_filename

            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            return plan_path

        except Exception as e:
            self.add_log("ERROR", f"Failed to process {file_path.name}: {str(e)}")
            return None

    def _extract_title(self, content):
        """Extract title from content."""
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                return line.lstrip('#').strip()
            elif line and not line.startswith('-'):
                return line
        return "Untitled Task"

    def _extract_description(self, content):
        """Extract description from content."""
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        # Skip metadata
        start_idx = 0
        if lines and lines[0].startswith('---'):
            for i, line in enumerate(lines):
                if i > 0 and line.startswith('---'):
                    start_idx = i + 1
                    break

        # Get first meaningful paragraph
        for line in lines[start_idx:]:
            if not line.startswith('#') and not line.startswith('-') and len(line) > 10:
                return line[:200]

        return "Task to be analyzed"

    def _generate_reasoning(self, title, description, content):
        """Generate step-by-step reasoning."""
        reasoning = {
            "think": self._generate_thinking(title, description),
            "plan": self._generate_planning(title, description, content),
            "actions": self._generate_actions(title, description)
        }
        return reasoning

    def _generate_thinking(self, title, description):
        """Generate thinking/analysis step."""
        thoughts = [
            f"✓ Understanding task: {title}",
            f"✓ Analyzing: {description}",
            "✓ Identifying key requirements",
            "✓ Evaluating scope and complexity",
            "✓ Determining dependencies"
        ]
        return thoughts

    def _generate_planning(self, title, description, content):
        """Generate planning step."""
        plans = [
            "Phase 1: Requirements Analysis",
            "  → Review all input files and metadata",
            "  → Identify blockers and dependencies",
            "Phase 2: Design Approach",
            "  → Create step-by-step workflow",
            "  → Define success criteria",
            "Phase 3: Execution Planning",
            "  → Assign tasks and sequence",
            "  → Allocate resources",
            "Phase 4: Validation",
            "  → Setup testing and verification",
            "  → Create completion checklist"
        ]
        return plans

    def _generate_actions(self, title, description):
        """Generate actionable steps."""
        actions = [
            "1. Gather all relevant information",
            "2. Document current state",
            "3. Define success criteria",
            "4. Execute Phase 1: Requirements",
            "5. Execute Phase 2: Design",
            "6. Execute Phase 3: Implementation",
            "7. Perform Phase 4: Validation",
            "8. Document results",
            "9. Complete post-action review",
            "10. Mark task as complete"
        ]
        return actions

    def _create_plan_document(self, filename, title, description, reasoning, content):
        """Create comprehensive reasoning plan document."""
        doc = f"""# Reasoning Plan: {title}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source File:** {filename}.md
**Plan ID:** plan_{filename}_{self.timestamp}

---

## Executive Summary

**Task Title:** {title}

**Description:** {description}

**Status:** 📋 Reasoning Analysis Complete - Ready for Action

---

## Step 1: THINK 🤔 (Analysis Phase)

### What We're Analyzing
The task requires careful analysis and strategic thinking to ensure successful execution.

### Key Thinking Points

"""
        for thought in reasoning["think"]:
            doc += f"- [ ] {thought}\n"

        doc += f"""
### Insights Generated
- Clarity on objectives achieved
- Dependencies identified
- Resource requirements understood
- Potential challenges assessed

---

## Step 2: PLAN 📋 (Planning Phase)

### Strategic Planning Approach

"""
        for plan in reasoning["plan"]:
            indent = "  " if "→" in plan else ""
            doc += f"- [ ] {indent}{plan}\n"

        doc += f"""
### Ralph Wiggum Loop 🔄 (The Silly-Smart Cycle)
*"I'm in danger... but in a GOOD way!"*

This task will iterate through the following loop until completion:

1. **Ralph Says:** "I'm not sure what I'm doing..."
   - Assess current situation
   - Identify knowledge gaps
   - Ask clarifying questions

2. **Ralph Realizes:** "Oh, I get it now!"
   - Connect the dots
   - Understand relationships
   - See the bigger picture

3. **Ralph Acts:** "Let's go do that thing!"
   - Execute planned steps
   - Monitor progress
   - Adjust as needed

4. **Ralph Checks:** "Did I do it right?"
   - Verify completion
   - Validate against criteria
   - Confirm success

5. **Ralph Repeats:** "Let's go again!" 🔄
   - Move to next phase
   - Apply lessons learned
   - Continue iteration

*Loop will cycle until task reaches "COMPLETE" status*

---

## Step 3: ACTIONS ⚡ (Execution Phase)

### Action Items Checklist

"""
        for action in reasoning["actions"]:
            doc += f"- [ ] {action}\n"

        doc += f"""
---

## Execution Tracking

### Phase Progress

- [ ] **Phase 1 Start:** Requirements Analysis
  - [ ] Review source files
  - [ ] Identify all requirements
  - [ ] Document constraints
  - [ ] **Phase 1 Complete**

- [ ] **Phase 2 Start:** Design & Planning
  - [ ] Create solution design
  - [ ] Define workflow steps
  - [ ] Allocate resources
  - [ ] **Phase 2 Complete**

- [ ] **Phase 3 Start:** Implementation
  - [ ] Execute planned steps
  - [ ] Track progress
  - [ ] Adjust as needed
  - [ ] **Phase 3 Complete**

- [ ] **Phase 4 Start:** Validation & Testing
  - [ ] Test all components
  - [ ] Verify success criteria
  - [ ] Document results
  - [ ] **Phase 4 Complete**

---

## Success Criteria

- [ ] All thinking points addressed
- [ ] Planning phases completed
- [ ] All actions executed
- [ ] Ralph Wiggum Loop completed
- [ ] Results validated
- [ ] Documentation complete
- [ ] Task marked complete

---

## Ralph Wiggum Loop Status

**Current Cycle:** Ready to Start
**Iteration Count:** 0
**Loop Status:** 🟡 Pending

### Loop History Log
```
[READY] Reasoning plan created
[WAITING] Loop execution pending
[INFO] Use this checklist to track loop iterations
```

---

## Final Approval Checklist

- [ ] Reasoning analysis reviewed
- [ ] Planning steps validated
- [ ] Action items understood
- [ ] Ralph Wiggum Loop understood
- [ ] Success criteria confirmed
- [ ] Ready for execution
- [ ] **TASK READY FOR IMPLEMENTATION**

---

## Task Metadata

**Source File:** {filename}.md
**Plan Generated:** {self.timestamp}
**Task Type:** Reasoning & Analysis
**Completion Status:** 📋 Draft - Ready for Review

**Next Steps:**
1. Review this reasoning plan
2. Approve or modify action items
3. Begin executing Phase 1
4. Track progress using checkboxes
5. Complete Ralph Wiggum Loop cycles
6. Mark task as complete when done

---

**Generated by:** ReasoningPlanner Agent Skill v1.0
**Location:** vault/Plans/plan_{filename}_{self.timestamp}.md
"""
        return doc

    def print_log(self):
        """Print execution log."""
        print("\n" + "="*60)
        print("REASONING PLANNER EXECUTION LOG")
        print("="*60)
        for entry in self.log:
            print(entry)
        print("="*60 + "\n")


def main():
    """Command-line entry point."""
    planner = ReasoningPlanner()
    planner.run()
    planner.print_log()


if __name__ == "__main__":
    main()
