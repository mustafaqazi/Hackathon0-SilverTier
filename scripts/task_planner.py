#!/usr/bin/env python3
"""
task_planner.py - Task Planner Agent Skill (SILVER Tier)

Reads tasks from the Inbox folder, analyzes their requirements, and generates
structured execution plans. Each plan is saved with clear steps, priorities,
dependencies, and approval requirements.
"""

import os
import sys
import json
import logging
import time
import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Vault paths
SCRIPT_DIR = Path(__file__).parent
VAULT_ROOT = SCRIPT_DIR.parent / "vault"
INBOX_FOLDER = VAULT_ROOT / "Inbox"
NEEDS_ACTION_FOLDER = VAULT_ROOT / "Needs_Action"
LOG_DIR = SCRIPT_DIR / "logs"
ACTIONS_LOG = LOG_DIR / "planning.log"
TASK_REGISTRY = LOG_DIR / "task_registry.json"

# Planning configuration
CHECK_INTERVAL = 15
FILE_EXTENSION = ".md"
PLAN_PREFIX = "ActionPlan"

# Default planning values
DEFAULT_PRIORITY_KEYWORDS = {
    "critical": "Critical",
    "urgent": "Critical",
    "asap": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "bug": "High",
    "feature": "Medium",
    "documentation": "Low",
}


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging to both console and file"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(ACTIONS_LOG, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create file logger: {e}", file=sys.stderr)

    return logger


logger = setup_logging()


# ============================================================================
# REGISTRY MANAGEMENT
# ============================================================================

class TaskRegistry:
    """Manage registry of planned tasks"""

    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.data: Dict = {}
        self.load()

    def load(self) -> None:
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    logger.debug(f"Loaded registry with {len(self.data)} entries")
            else:
                self.data = {}
                logger.info("Registry file not found, creating new registry")
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
            self.data = {}

    def save(self) -> None:
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving registry: {e}")

    def is_planned(self, filename: str) -> bool:
        return filename in self.data

    def add_task(self, filename: str, plan_file: str, priority: str) -> None:
        self.data[filename] = {
            "detected_at": datetime.now().isoformat(),
            "plan_file": plan_file,
            "priority": priority,
            "status": "planned"
        }
        self.save()

    def get_stats(self) -> Dict:
        return {
            "total": len(self.data),
            "critical": sum(1 for t in self.data.values() if t.get("priority") == "Critical"),
            "high": sum(1 for t in self.data.values() if t.get("priority") == "High"),
            "medium": sum(1 for t in self.data.values() if t.get("priority") == "Medium"),
            "low": sum(1 for t in self.data.values() if t.get("priority") == "Low"),
        }


# ============================================================================
# TASK ANALYSIS
# ============================================================================

def extract_task_metadata(content: str, filename: str) -> Dict:
    """Extract metadata from task content"""
    lines = content.split('\n')

    title = filename.replace('.md', '')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    description = ''
    in_description = False
    for line in lines:
        if line.startswith('# '):
            in_description = True
            continue
        if in_description:
            if line.strip() == '':
                continue
            if line.startswith('#'):
                break
            description += line + ' '
            if len(description) > 300:
                break

    return {
        'title': title,
        'description': description.strip()[:300],
        'content': content,
        'filename': filename
    }


def detect_priority(metadata: Dict) -> str:
    """Detect priority level from task content"""
    content = (metadata['title'] + ' ' + metadata['description']).lower()

    for keyword, priority in DEFAULT_PRIORITY_KEYWORDS.items():
        if keyword in content:
            return priority

    if 'bug' in content:
        return 'High'
    elif 'feature' in content:
        return 'Medium'
    else:
        return 'Medium'


def analyze_task_intent(metadata: Dict) -> Dict:
    """Analyze task intent and goals"""
    content = metadata['content']

    return {
        'primary_goal': extract_goal(content),
        'success_criteria': extract_success_criteria(content),
        'affected_systems': extract_systems(content),
        'constraints': extract_constraints(content)
    }


def extract_goal(content: str) -> str:
    """Extract primary goal from content"""
    for line in content.split('\n'):
        if 'goal' in line.lower() or 'objective' in line.lower():
            return line.replace('Goal:', '').replace('Objective:', '').strip()
    return "Complete the requested task"


def extract_success_criteria(content: str) -> List[str]:
    """Extract success criteria"""
    criteria = []
    for line in content.split('\n'):
        if line.strip().startswith('-') or line.strip().startswith('•'):
            criteria.append(line.strip()[1:].strip())
    return criteria if criteria else ["Task completed successfully", "No errors or warnings"]


def extract_systems(content: str) -> List[str]:
    """Identify affected systems"""
    systems = set()
    keywords = ['vault', 'script', 'database', 'api', 'ui', 'documentation', 'configuration']
    for keyword in keywords:
        if keyword in content.lower():
            systems.add(keyword.capitalize())
    return list(systems) if systems else ["Internal Systems"]


def extract_constraints(content: str) -> List[str]:
    """Extract any constraints"""
    constraints = []
    for line in content.split('\n'):
        if 'deadline' in line.lower() or 'constraint' in line.lower() or 'requirement' in line.lower():
            constraints.append(line.strip())
    return constraints


def break_into_steps(metadata: Dict) -> List[Dict]:
    """Break task into execution steps"""
    steps = []
    title = metadata['title'].lower()

    if 'bug' in title or 'fix' in title:
        steps = [
            {'step': 1, 'description': 'Identify and reproduce the bug', 'effort': '1-2 hours'},
            {'step': 2, 'description': 'Analyze root cause', 'effort': '1-2 hours'},
            {'step': 3, 'description': 'Implement fix', 'effort': '2-4 hours'},
            {'step': 4, 'description': 'Test fix thoroughly', 'effort': '1-2 hours'},
            {'step': 5, 'description': 'Deploy and verify', 'effort': '1 hour'},
        ]
    elif 'feature' in title or 'add' in title or 'implement' in title:
        steps = [
            {'step': 1, 'description': 'Design implementation approach', 'effort': '1-2 hours'},
            {'step': 2, 'description': 'Set up development environment', 'effort': '1 hour'},
            {'step': 3, 'description': 'Implement feature', 'effort': '4-8 hours'},
            {'step': 4, 'description': 'Write tests', 'effort': '2-4 hours'},
            {'step': 5, 'description': 'Code review and refinement', 'effort': '1-2 hours'},
            {'step': 6, 'description': 'Deployment', 'effort': '1 hour'},
        ]
    elif 'document' in title or 'write' in title:
        steps = [
            {'step': 1, 'description': 'Gather information', 'effort': '1-2 hours'},
            {'step': 2, 'description': 'Outline structure', 'effort': '30 minutes'},
            {'step': 3, 'description': 'Write content', 'effort': '2-4 hours'},
            {'step': 4, 'description': 'Review and edit', 'effort': '1 hour'},
            {'step': 5, 'description': 'Publish', 'effort': '30 minutes'},
        ]
    else:
        steps = [
            {'step': 1, 'description': 'Analyze requirements', 'effort': '1 hour'},
            {'step': 2, 'description': 'Plan approach', 'effort': '1 hour'},
            {'step': 3, 'description': 'Execute work', 'effort': '2-4 hours'},
            {'step': 4, 'description': 'Verify completion', 'effort': '1 hour'},
        ]

    return steps


def identify_risks(metadata: Dict, steps: List[Dict]) -> List[Dict]:
    """Identify risks and mitigations"""
    risks = [
        {
            'risk': 'Requirements may be unclear or incomplete',
            'mitigation': 'Request clarification before starting implementation'
        },
        {
            'risk': 'Unexpected dependencies or conflicts',
            'mitigation': 'Review system dependencies thoroughly during planning'
        },
    ]

    if 'critical' in metadata['title'].lower():
        risks.append({
            'risk': 'Critical nature requires careful execution',
            'mitigation': 'Implement thorough testing and validation'
        })

    return risks


def check_approval_needed(metadata: Dict, priority: str) -> Dict:
    """Determine if human approval is needed"""
    approval_needed = False
    approval_type = "None"

    if priority in ['Critical', 'High']:
        approval_needed = True
        approval_type = "Technical Review"

    if 'budget' in metadata['title'].lower() or 'cost' in metadata['title'].lower():
        approval_needed = True
        approval_type = "Budget"

    if 'scope' in metadata['title'].lower() or 'change' in metadata['title'].lower():
        approval_needed = True
        approval_type = "Scope"

    return {
        'required': approval_needed,
        'type': approval_type,
        'approver': 'Human Reviewer',
        'deadline': (datetime.now().isoformat() if approval_needed else None)
    }


# ============================================================================
# PLAN GENERATION
# ============================================================================

def estimate_hours(steps: List[Dict]) -> str:
    """Estimate total hours from steps"""
    total = 0
    for step in steps:
        effort = step['effort']
        if '-' in effort:
            low, high = effort.split('-')
            hours = int(high.split()[0])
        else:
            hours = int(effort.split()[0])
        total += hours
    return f"{total}-{int(total*1.5)}"


def estimate_completion_date(steps: List[Dict]) -> str:
    """Estimate completion date"""
    hours = 20
    days = max(1, hours // 8)
    completion = datetime.now() + timedelta(days=days)
    return completion.strftime("%Y-%m-%d")


def generate_action_plan(metadata: Dict, priority: str, analysis: Dict,
                        steps: List[Dict], risks: List[Dict],
                        approval: Dict) -> Tuple[str, str]:
    """Generate structured action plan document"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_name = re.sub(r'[^a-z0-9]', '_', metadata['title'].lower())[:30]

    plan_content = f"""# ActionPlan: {metadata['title']}

## Task Metadata
- **Source:** {metadata['filename']}
- **Received:** {datetime.now().isoformat()}
- **Priority:** {priority}
- **Est. Hours:** {estimate_hours(steps)}
- **Type:** {'bugfix' if 'bug' in metadata['title'].lower() else 'feature' if 'feature' in metadata['title'].lower() else 'other'}

## Task Summary
{metadata['description']}

## Goals & Success Criteria
- **Primary Goal:** {analysis['primary_goal']}
- Success Criteria:
"""

    for criterion in analysis['success_criteria']:
        plan_content += f"  - {criterion}\n"

    plan_content += f"\n## Execution Steps\n"

    for step in steps:
        plan_content += f"\n### Step {step['step']}: {step['description']}\n"
        plan_content += f"- **Estimated Time:** {step['effort']}\n"
        if step['step'] > 1:
            plan_content += f"- **Dependencies:** Step {step['step']-1}\n"
        plan_content += f"- **Acceptance Criteria:** Task completed successfully\n"

    plan_content += f"\n## Risks & Mitigations\n"
    for risk in risks:
        plan_content += f"\n**Risk:** {risk['risk']}\n"
        plan_content += f"**Mitigation:** {risk['mitigation']}\n"

    plan_content += f"\n## Systems & Dependencies\n"
    plan_content += f"- **Affected Systems:** {', '.join(analysis['affected_systems'])}\n"
    plan_content += f"- **External Dependencies:** System dependencies as needed\n"
    plan_content += f"- **Internal Dependencies:** None identified\n"

    plan_content += f"\n## Human Approval\n"
    plan_content += f"- **Approval Required:** {'Yes' if approval['required'] else 'No'}\n"
    plan_content += f"- **Type:** {approval['type']}\n"
    if approval['required']:
        plan_content += f"- **Approver:** {approval['approver']}\n"
        plan_content += f"- **Status:** Pending Review\n"

    plan_content += f"\n## Notes\n"
    plan_content += f"- Plan generated: {datetime.now().isoformat()}\n"
    plan_content += f"- Estimated completion: {estimate_completion_date(steps)}\n"
    plan_content += f"- Status: Ready for review\n"

    return plan_content, f"{PLAN_PREFIX}_{task_name}_{timestamp}.md"


# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_task(task_path: Path, registry: TaskRegistry) -> bool:
    """Process a single task and generate action plan"""
    filename = task_path.name

    try:
        if registry.is_planned(filename):
            logger.debug(f"Task already planned: {filename}")
            return False

        with open(task_path, 'r', encoding='utf-8') as f:
            content = f.read()

        logger.info(f"Processing task: {filename}")

        metadata = extract_task_metadata(content, filename)
        analysis = analyze_task_intent(metadata)
        steps = break_into_steps(metadata)
        priority = detect_priority(metadata)
        approval = check_approval_needed(metadata, priority)
        risks = identify_risks(metadata, steps)

        plan_content, plan_filename = generate_action_plan(
            metadata, priority, analysis, steps, risks, approval
        )

        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)

        plan_path = NEEDS_ACTION_FOLDER / plan_filename
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(plan_content)

        registry.add_task(filename, plan_filename, priority)

        logger.info(f"Plan generated: {plan_filename} (Priority: {priority})")

        return True

    except Exception as e:
        logger.error(f"Error processing task {filename}: {e}")
        return False


def scan_inbox(registry: TaskRegistry) -> int:
    """Scan inbox folder for new tasks"""
    new_plans = 0

    try:
        if not INBOX_FOLDER.exists():
            logger.warning(f"Inbox folder does not exist: {INBOX_FOLDER}")
            return 0

        md_files = list(INBOX_FOLDER.glob(f"*{FILE_EXTENSION}"))

        if not md_files:
            return 0

        for task_path in md_files:
            if not task_path.is_file() or task_path.name.startswith('.'):
                continue

            if process_task(task_path, registry):
                new_plans += 1

        return new_plans

    except Exception as e:
        logger.error(f"Error scanning inbox: {e}")
        return 0


# ============================================================================
# MONITORING LOOP
# ============================================================================

def run_monitoring_loop(check_interval: int = CHECK_INTERVAL, single_pass: bool = False) -> None:
    """Main monitoring loop"""
    registry = TaskRegistry(TASK_REGISTRY)

    logger.info("=" * 70)
    logger.info("Task Planner Started")
    logger.info(f"Monitoring: {INBOX_FOLDER}")
    logger.info(f"Output: {NEEDS_ACTION_FOLDER}")
    logger.info(f"Check interval: {check_interval} seconds")
    logger.info("=" * 70)

    if single_pass:
        logger.info("Running in single-pass mode")
        plans_generated = scan_inbox(registry)
        logger.info(f"Scan complete. Plans generated: {plans_generated}")
        return

    try:
        logger.info("Running in continuous monitoring mode (Ctrl+C to stop)")
        logger.info("-" * 70)

        iteration = 0
        while True:
            iteration += 1
            new_plans = scan_inbox(registry)

            if new_plans > 0:
                logger.info(f"[{iteration}] Scan complete. New plans: {new_plans}")
            else:
                if iteration % 10 == 0:
                    stats = registry.get_stats()
                    logger.debug(f"[{iteration}] No new tasks. Registry: {stats}")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        logger.info("\nShutdown signal received (Ctrl+C)")
    except Exception as e:
        logger.error(f"Error in monitoring loop: {e}")
    finally:
        logger.info("=" * 70)
        logger.info("Task Planner stopped")
        logger.info("=" * 70)


# ============================================================================
# HEALTH CHECK
# ============================================================================

def health_check() -> bool:
    """Perform health check"""
    print("\n[HEALTH CHECK] Task Planner Diagnostics")
    print("=" * 70)

    checks_passed = 0
    checks_total = 0

    checks_total += 1
    if VAULT_ROOT.exists():
        print("[OK] Vault root exists:", VAULT_ROOT)
        checks_passed += 1
    else:
        print("[FAIL] Vault root does not exist:", VAULT_ROOT)

    checks_total += 1
    if INBOX_FOLDER.exists():
        print("[OK] Inbox folder exists:", INBOX_FOLDER)
        checks_passed += 1
    else:
        print("[WARN] Inbox folder does not exist:", INBOX_FOLDER)
        checks_passed += 1

    checks_total += 1
    try:
        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)
        print("[OK] Needs_Action folder writable:", NEEDS_ACTION_FOLDER)
        checks_passed += 1
    except Exception as e:
        print(f"[FAIL] Needs_Action folder not writable: {e}")

    checks_total += 1
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        test_file = LOG_DIR / ".write_test"
        test_file.touch()
        test_file.unlink()
        print("[OK] Log directory is writable:", LOG_DIR)
        checks_passed += 1
    except Exception as e:
        print(f"[FAIL] Log directory not writable: {e}")

    checks_total += 1
    try:
        registry = TaskRegistry(TASK_REGISTRY)
        stats = registry.get_stats()
        print(f"[OK] Registry loaded. Stats: {stats}")
        checks_passed += 1
    except Exception as e:
        print(f"[FAIL] Registry error: {e}")

    print("=" * 70)
    print(f"\nHealth Check Result: {checks_passed}/{checks_total} checks passed\n")
    return checks_passed >= (checks_total - 1)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Task Planner - Generate execution plans')
    parser.add_argument('--once', action='store_true', help='Run single scan and exit')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--interval', type=int, default=CHECK_INTERVAL, help='Check interval in seconds')
    parser.add_argument('--health', action='store_true', help='Run health check and exit')
    parser.add_argument('--check', action='store_true', help='Run health check (alias)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    if args.health or args.check:
        success = health_check()
        sys.exit(0 if success else 1)

    if args.interval < 1 or args.interval > 300:
        print("Error: Check interval must be between 1 and 300 seconds", file=sys.stderr)
        sys.exit(1)

    run_monitoring_loop(check_interval=args.interval, single_pass=args.once)


if __name__ == "__main__":
    main()
