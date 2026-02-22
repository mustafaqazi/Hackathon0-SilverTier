#!/usr/bin/env python3

"""
Orchestrator for AI Employee Skills
Coordinates and schedules all agent skills to run together in a workflow.

Skills orchestrated:
1. ReasoningPlanner - Generates reasoning plans from tasks
2. EmailSender - Generates emails from plans
3. ApprovalChecker - Creates approval workflow for sensitive actions

Runs on schedule: Every 15 minutes (configurable)

Usage:
  python orchestrator.py --once                  # Run once and exit
  python orchestrator.py --schedule 15           # Run every 15 minutes
  python orchestrator.py --demand 5 120          # Run 5 times with 120s intervals
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import traceback

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import schedule
except ImportError:
    print("Installing required package: schedule")
    os.system("pip install schedule")
    import schedule

from skills.reasoning_planner import ReasoningPlanner
from skills.email_sender import EmailSender
from skills.approval_checker import ApprovalChecker


class SkillsOrchestrator:
    """Orchestrates and schedules all AI Employee skills."""

    def __init__(self, schedule_interval: int = 15):
        """
        Initialize orchestrator.

        Args:
            schedule_interval: Minutes between runs (default 15)
        """
        self.vault_path = Path(__file__).parent / "vault"
        self.schedule_interval = schedule_interval
        self.run_count = 0
        self.total_runtime = 0.0
        self.logs_path = self.vault_path / "orchestrator_logs"
        self.logs_path.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self._setup_logging()
        self.logger.info(f"Orchestrator initialized - Schedule interval: {schedule_interval} minutes")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for orchestrator."""
        logger = logging.getLogger("SkillsOrchestrator")
        logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        logger.handlers = []

        # File handler
        log_file = self.logs_path / f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def run_all_skills(self) -> Dict:
        """Run all skills in sequence."""
        self.run_count += 1
        run_start = time.time()

        self.logger.info("=" * 80)
        self.logger.info(f"ORCHESTRATOR RUN #{self.run_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 80)

        results = {
            'run_number': self.run_count,
            'timestamp': datetime.now().isoformat(),
            'skills': {}
        }

        # Run skills in sequence
        try:
            # Skill 1: ReasoningPlanner
            self.logger.info("\n" + ">"*40)
            self.logger.info("SKILL 1: ReasoningPlanner")
            self.logger.info("Purpose: Generates reasoning plans from task files")
            self.logger.info(">"*40)
            results['skills']['reasoning_planner'] = self._run_reasoning_planner()

            # Skill 2: EmailSender
            self.logger.info("\n" + ">"*40)
            self.logger.info("SKILL 2: EmailSender")
            self.logger.info("Purpose: Generates emails from plan files")
            self.logger.info(">"*40)
            results['skills']['email_sender'] = self._run_email_sender()

            # Skill 3: ApprovalChecker
            self.logger.info("\n" + ">"*40)
            self.logger.info("SKILL 3: ApprovalChecker")
            self.logger.info("Purpose: Creates approval workflow for sensitive actions")
            self.logger.info(">"*40)
            results['skills']['approval_checker'] = self._run_approval_checker()

            results['status'] = 'SUCCESS'

        except Exception as e:
            self.logger.error(f"[ERROR] Orchestrator error: {str(e)}")
            self.logger.error(traceback.format_exc())
            results['status'] = 'ERROR'
            results['error'] = str(e)

        # Log summary
        run_time = time.time() - run_start
        self.total_runtime += run_time
        results['run_time_seconds'] = run_time

        self.logger.info("\n" + "="*80)
        self.logger.info(f"RUN #{self.run_count} COMPLETE - Duration: {run_time:.2f}s")
        self.logger.info("="*80 + "\n")

        # Save results
        self._save_results(results)

        return results

    def _run_reasoning_planner(self) -> Dict:
        """Run ReasoningPlanner skill."""
        try:
            self.logger.info("Starting ReasoningPlanner...")
            start = time.time()

            planner = ReasoningPlanner()
            result = planner.run()

            duration = time.time() - start

            if result:
                self.logger.info(f"[OK] ReasoningPlanner completed in {duration:.2f}s")
                self.logger.info(f"   Output: {str(result)}")
                return {
                    'status': 'SUCCESS',
                    'duration': duration,
                    'message': 'Plans generated successfully',
                    'output_path': str(result) if result else None
                }
            else:
                self.logger.warning("[WARN] ReasoningPlanner completed with no output")
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': 'No plans generated'
                }

        except Exception as e:
            self.logger.error(f"[ERROR] ReasoningPlanner failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                'status': 'ERROR',
                'message': str(e)
            }

    def _run_email_sender(self) -> Dict:
        """Run EmailSender skill."""
        try:
            self.logger.info("Starting EmailSender...")
            start = time.time()

            sender = EmailSender()
            result = sender.run()

            duration = time.time() - start

            if result:
                self.logger.info(f"[OK] EmailSender completed in {duration:.2f}s")
                self.logger.info(f"   Output: {str(result)}")
                return {
                    'status': 'SUCCESS',
                    'duration': duration,
                    'message': 'Emails generated successfully',
                    'output_path': str(result) if result else None
                }
            else:
                self.logger.warning("[WARN] EmailSender completed with no output")
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': 'No emails generated'
                }

        except Exception as e:
            self.logger.error(f"[ERROR] EmailSender failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                'status': 'ERROR',
                'message': str(e)
            }

    def _run_approval_checker(self) -> Dict:
        """Run ApprovalChecker skill."""
        try:
            self.logger.info("Starting ApprovalChecker...")
            start = time.time()

            checker = ApprovalChecker()
            result = checker.run()

            duration = time.time() - start

            status_report = checker.get_status_report()

            self.logger.info(f"[OK] ApprovalChecker completed in {duration:.2f}s")
            self.logger.info(f"   Pending Approval: {status_report['pending_approval']}")
            self.logger.info(f"   Approved: {status_report['approved']}")
            self.logger.info(f"   Rejected: {status_report['rejected']}")
            self.logger.info(f"   Completed: {status_report['completed']}")

            return {
                'status': 'SUCCESS',
                'duration': duration,
                'message': 'Approvals checked and processed',
                'status_report': status_report,
                'output_path': str(result) if result else None
            }

        except Exception as e:
            self.logger.error(f"[ERROR] ApprovalChecker failed: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                'status': 'ERROR',
                'message': str(e)
            }

    def _save_results(self, results: Dict):
        """Save orchestration results to JSON."""
        try:
            log_file = self.logs_path / f"run_{self.run_count:04d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.debug(f"Results saved to {log_file}")
        except Exception as e:
            self.logger.error(f"Failed to save results: {str(e)}")

    def schedule_recurring(self):
        """Schedule recurring runs."""
        self.logger.info(f"Scheduling skill runs every {self.schedule_interval} minutes")
        self.logger.info("Press Ctrl+C to stop the scheduler\n")

        # Run immediately on first schedule
        self.run_all_skills()

        # Schedule the job
        schedule.every(self.schedule_interval).minutes.do(self.run_all_skills)

        # Run the scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("\n\nOrchestrator stopped by user")
            self.print_stats()

    def run_once(self):
        """Run all skills once immediately."""
        self.logger.info("Running all skills once immediately...")
        return self.run_all_skills()

    def run_on_demand(self, count: int = 1, interval: int = 60):
        """Run skills multiple times with interval."""
        for i in range(count):
            if i > 0:
                self.logger.info(f"\nWaiting {interval} seconds before next run...")
                time.sleep(interval)
            self.run_all_skills()

    def get_stats(self) -> Dict:
        """Get orchestrator statistics."""
        return {
            'runs_completed': self.run_count,
            'total_runtime_seconds': self.total_runtime,
            'average_runtime_seconds': self.total_runtime / self.run_count if self.run_count > 0 else 0,
            'schedule_interval_minutes': self.schedule_interval,
            'logs_directory': str(self.logs_path)
        }

    def print_stats(self):
        """Print orchestrator statistics."""
        stats = self.get_stats()
        self.logger.info("\n" + "="*80)
        self.logger.info("ORCHESTRATOR STATISTICS")
        self.logger.info("="*80)
        self.logger.info(f"Runs Completed:        {stats['runs_completed']}")
        self.logger.info(f"Total Runtime:         {stats['total_runtime_seconds']:.2f}s")
        self.logger.info(f"Average Runtime:       {stats['average_runtime_seconds']:.2f}s")
        self.logger.info(f"Schedule Interval:     {stats['schedule_interval_minutes']} minutes")
        self.logger.info(f"Logs Directory:        {stats['logs_directory']}")
        self.logger.info("="*80 + "\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='AI Employee Skills Orchestrator - Coordinates all agent skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python orchestrator.py --once
    Run all skills once and exit

  python orchestrator.py --schedule 15
    Run all skills every 15 minutes (continuous)

  python orchestrator.py --demand 5 120
    Run all skills 5 times with 120 seconds between runs

SKILLS EXECUTED:
  1. ReasoningPlanner    - Generates reasoning plans from task files
  2. EmailSender         - Generates emails from plan files
  3. ApprovalChecker     - Creates approval workflow for sensitive actions

WORKFLOW:
  Needs_Action/ -> Plans/ -> Pending_Approval/ -> Approved/ -> Email MCP
        """
    )

    parser.add_argument(
        '--once',
        action='store_true',
        help='Run all skills once and exit'
    )

    parser.add_argument(
        '--schedule',
        type=int,
        metavar='MINUTES',
        help='Schedule recurring runs every N minutes'
    )

    parser.add_argument(
        '--demand',
        type=int,
        nargs=2,
        metavar=('COUNT', 'INTERVAL'),
        help='Run skills COUNT times with INTERVAL seconds between runs'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=15,
        help='Default schedule interval in minutes (default: 15)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show orchestrator statistics'
    )

    args = parser.parse_args()

    try:
        # Create orchestrator
        orchestrator = SkillsOrchestrator(schedule_interval=args.interval)

        if args.once:
            # Run once
            orchestrator.run_once()
            orchestrator.print_stats()

        elif args.schedule:
            # Schedule recurring
            orchestrator = SkillsOrchestrator(schedule_interval=args.schedule)
            orchestrator.schedule_recurring()

        elif args.demand:
            # Run on demand
            count, interval = args.demand
            orchestrator.run_on_demand(count=count, interval=interval)
            orchestrator.print_stats()

        elif args.stats:
            # Show stats only
            orchestrator.print_stats()

        else:
            # Default: run once
            print("No arguments provided. Running once. Use --help for options.\n")
            orchestrator.run_once()
            orchestrator.print_stats()

    except KeyboardInterrupt:
        print("\n\nOrchestrator interrupted by user")
        try:
            orchestrator.print_stats()
        except:
            pass
        sys.exit(0)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
