#!/usr/bin/env python3
"""
run_ai_employee.py - AI Employee Scheduler

Production-ready scheduler for the AI Employee system that:
- Monitors Inbox for new tasks
- Runs task-planner automatically
- Processes tasks every 5 minutes
- Works on Windows, Linux, and Mac
- Handles errors gracefully
- Maintains comprehensive logs

Usage:
    python run_ai_employee.py --daemon          # Run as daemon
    python run_ai_employee.py --once            # Run once
    python run_ai_employee.py --health          # Health check
    python run_ai_employee.py --interval 300    # Custom interval (seconds)
"""

import os
import sys
import json
import logging
import time
import argparse
import subprocess
import signal
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
VAULT_ROOT = PROJECT_ROOT / "vault"
INBOX_FOLDER = VAULT_ROOT / "Inbox"
NEEDS_ACTION_FOLDER = VAULT_ROOT / "Needs_Action"
LOG_DIR = SCRIPT_DIR / "logs"
SCHEDULER_LOG = LOG_DIR / "scheduler.log"
TASK_PLANNER_SCRIPT = SCRIPT_DIR / "task_planner.py"

# Default settings
DEFAULT_INTERVAL = 300  # 5 minutes in seconds
CHECK_INTERVAL = 15    # Check every 15 seconds in monitoring mode
MAX_RETRIES = 3
RETRY_DELAY = 5        # seconds

# Performance settings
MIN_TASK_SIZE = 10     # bytes - skip tiny files
MAX_TASKS_PER_RUN = 10 # process max 10 tasks per cycle


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure logging for scheduler"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Log format
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File handler
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(SCHEDULER_LOG, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create file logger: {e}", file=sys.stderr)

    return logger


logger = setup_logging()


# ============================================================================
# SCHEDULER REGISTRY
# ============================================================================

class SchedulerRegistry:
    """Track scheduler runs and statistics"""

    def __init__(self, registry_path: Path = None):
        if registry_path is None:
            registry_path = LOG_DIR / "scheduler_registry.json"
        self.registry_path = registry_path
        self.data: Dict = {}
        self.load()

    def load(self) -> None:
        """Load registry from disk"""
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    "started_at": datetime.now().isoformat(),
                    "runs": [],
                    "stats": {
                        "total_runs": 0,
                        "total_tasks_processed": 0,
                        "total_errors": 0,
                        "last_run": None,
                        "uptime_seconds": 0
                    }
                }
                self.save()
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
            self.data = {}

    def save(self) -> None:
        """Save registry to disk"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving registry: {e}")

    def record_run(self, tasks_found: int, tasks_processed: int, errors: int) -> None:
        """Record scheduler run"""
        try:
            run_record = {
                "timestamp": datetime.now().isoformat(),
                "tasks_found": tasks_found,
                "tasks_processed": tasks_processed,
                "errors": errors,
                "status": "success" if errors == 0 else "partial"
            }

            if "runs" not in self.data:
                self.data["runs"] = []

            self.data["runs"].append(run_record)

            # Keep only last 1000 runs
            self.data["runs"] = self.data["runs"][-1000:]

            # Update stats
            if "stats" not in self.data:
                self.data["stats"] = {}

            self.data["stats"]["total_runs"] = len(self.data["runs"])
            self.data["stats"]["total_tasks_processed"] += tasks_processed
            self.data["stats"]["total_errors"] += errors
            self.data["stats"]["last_run"] = datetime.now().isoformat()

            self.save()
        except Exception as e:
            logger.error(f"Error recording run: {e}")

    def get_stats(self) -> Dict:
        """Get scheduler statistics"""
        if "stats" not in self.data:
            return {}
        return self.data["stats"]


# ============================================================================
# TASK DETECTION
# ============================================================================

def detect_new_tasks() -> List[Path]:
    """Detect new markdown files in Inbox"""
    try:
        if not INBOX_FOLDER.exists():
            return []

        # Find all markdown files
        tasks = []
        for file_path in INBOX_FOLDER.glob("*.md"):
            if not file_path.is_file():
                continue
            if file_path.name.startswith('.'):
                continue

            # Check file size (skip tiny files)
            try:
                size = file_path.stat().st_size
                if size >= MIN_TASK_SIZE:
                    tasks.append(file_path)
            except:
                pass

        # Sort by modification time (newest first)
        tasks.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Limit to max tasks per run
        return tasks[:MAX_TASKS_PER_RUN]

    except Exception as e:
        logger.error(f"Error detecting tasks: {e}")
        return []


# ============================================================================
# TASK PROCESSING
# ============================================================================

def run_task_planner(retry_count: int = 0) -> tuple:
    """Run task-planner script"""

    try:
        if not TASK_PLANNER_SCRIPT.exists():
            logger.error(f"Task planner script not found: {TASK_PLANNER_SCRIPT}")
            return False, 0, "Script not found"

        # Run task planner in single-pass mode
        result = subprocess.run(
            [sys.executable, str(TASK_PLANNER_SCRIPT), "--once"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            if retry_count < MAX_RETRIES:
                logger.warning(f"Task planner failed, retry {retry_count + 1}/{MAX_RETRIES}")
                time.sleep(RETRY_DELAY)
                return run_task_planner(retry_count + 1)
            else:
                logger.error(f"Task planner failed after {MAX_RETRIES} retries: {error_msg}")
                return False, 0, error_msg

        # Parse output to count tasks
        output = result.stdout
        tasks_processed = output.count("Plan generated:")

        logger.info(f"Task planner completed: {tasks_processed} tasks processed")
        return True, tasks_processed, "Success"

    except subprocess.TimeoutExpired:
        logger.error("Task planner timed out (>60 seconds)")
        return False, 0, "Timeout"
    except Exception as e:
        logger.error(f"Error running task planner: {e}")
        return False, 0, str(e)


def process_tasks() -> tuple:
    """Detect and process new tasks"""

    try:
        # Detect new tasks
        tasks = detect_new_tasks()
        tasks_found = len(tasks)

        if tasks_found == 0:
            logger.debug("No new tasks detected in Inbox")
            return 0, 0, 0

        logger.info(f"Detected {tasks_found} new task(s) in Inbox")

        # Run task planner
        success, tasks_processed, message = run_task_planner()

        if success:
            logger.info(f"Successfully processed {tasks_processed} task(s)")
            return tasks_found, tasks_processed, 0
        else:
            logger.warning(f"Task processing failed: {message}")
            return tasks_found, 0, 1

    except Exception as e:
        logger.error(f"Error processing tasks: {e}")
        return 0, 0, 1


# ============================================================================
# SCHEDULER LOOP
# ============================================================================

def run_scheduler_loop(interval: int = DEFAULT_INTERVAL, daemon: bool = False) -> None:
    """Main scheduler loop"""

    registry = SchedulerRegistry()
    shutdown_flag = False

    def signal_handler(signum, frame):
        nonlocal shutdown_flag
        logger.info(f"Shutdown signal received (signal {signum})")
        shutdown_flag = True

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)

    logger.info("=" * 70)
    logger.info("AI Employee Scheduler Started")
    logger.info(f"Vault Path: {VAULT_ROOT}")
    logger.info(f"Inbox Path: {INBOX_FOLDER}")
    logger.info(f"Check Interval: {interval} seconds")
    logger.info(f"Mode: {'Daemon' if daemon else 'Interactive'}")
    logger.info("=" * 70)

    try:
        iteration = 0
        last_run = time.time()

        while not shutdown_flag:
            iteration += 1
            current_time = time.time()

            # Check if it's time to run
            if current_time - last_run >= interval:
                logger.info(f"[{iteration}] Starting scheduled task processing...")

                # Process tasks
                tasks_found, tasks_processed, errors = process_tasks()

                # Record in registry
                registry.record_run(tasks_found, tasks_processed, errors)

                if tasks_found > 0 or tasks_processed > 0:
                    logger.info(
                        f"[{iteration}] Run complete - Found: {tasks_found}, "
                        f"Processed: {tasks_processed}, Errors: {errors}"
                    )

                last_run = current_time

            else:
                # Wait before checking again
                wait_time = min(CHECK_INTERVAL, interval - (current_time - last_run))
                time.sleep(wait_time)

    except KeyboardInterrupt:
        logger.info("\nKeyboard interrupt received")
    except Exception as e:
        logger.error(f"Error in scheduler loop: {e}", exc_info=True)
    finally:
        logger.info("=" * 70)
        logger.info("AI Employee Scheduler stopped")

        # Print final stats
        stats = registry.get_stats()
        logger.info(f"Total runs: {stats.get('total_runs', 0)}")
        logger.info(f"Total tasks processed: {stats.get('total_tasks_processed', 0)}")
        logger.info(f"Total errors: {stats.get('total_errors', 0)}")
        logger.info("=" * 70)


# ============================================================================
# HEALTH CHECK
# ============================================================================

def health_check() -> bool:
    """Perform health check on scheduler"""

    print("\n[HEALTH CHECK] AI Employee Scheduler Diagnostics")
    print("=" * 70)

    checks_passed = 0
    checks_total = 0

    # Check 1: Vault exists
    checks_total += 1
    if VAULT_ROOT.exists():
        print("[OK] Vault root exists:", VAULT_ROOT)
        checks_passed += 1
    else:
        print("[FAIL] Vault root does not exist:", VAULT_ROOT)

    # Check 2: Inbox exists
    checks_total += 1
    if INBOX_FOLDER.exists():
        print("[OK] Inbox folder exists:", INBOX_FOLDER)
        checks_passed += 1
    else:
        print("[WARN] Inbox folder does not exist:", INBOX_FOLDER)
        checks_passed += 1

    # Check 3: Task planner script exists
    checks_total += 1
    if TASK_PLANNER_SCRIPT.exists():
        print("[OK] Task planner script found:", TASK_PLANNER_SCRIPT)
        checks_passed += 1
    else:
        print("[FAIL] Task planner script not found:", TASK_PLANNER_SCRIPT)

    # Check 4: Log directory writable
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

    # Check 5: Registry readable
    checks_total += 1
    try:
        registry = SchedulerRegistry()
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

    parser = argparse.ArgumentParser(
        description='AI Employee Scheduler - Automated task processing'
    )
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run as daemon (background process)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=DEFAULT_INTERVAL,
        help=f'Check interval in seconds (default: {DEFAULT_INTERVAL})'
    )
    parser.add_argument(
        '--health',
        action='store_true',
        help='Run health check and exit'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Run health check (alias for --health)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Enable verbose logging if requested
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    # Health check mode
    if args.health or args.check:
        success = health_check()
        sys.exit(0 if success else 1)

    # Validate interval
    if args.interval < 1 or args.interval > 3600:
        print("Error: Interval must be between 1 and 3600 seconds", file=sys.stderr)
        sys.exit(1)

    # Single run mode
    if args.once:
        logger.info("Running in single-pass mode")
        tasks_found, tasks_processed, errors = process_tasks()
        logger.info(f"Found: {tasks_found}, Processed: {tasks_processed}, Errors: {errors}")
        sys.exit(0 if errors == 0 else 1)

    # Daemon/continuous mode
    run_scheduler_loop(interval=args.interval, daemon=args.daemon)


if __name__ == "__main__":
    main()
