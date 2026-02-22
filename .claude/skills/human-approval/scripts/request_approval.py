#!/usr/bin/env python3
"""
request_approval.py - Human-in-the-loop approval system

Usage:
    python request_approval.py --action "Send email" --reason "Customer inquiry"

Environment Variables:
    VAULT_PATH - Path to vault (default: ./AI_Employee_Vault/)
"""

import argparse
import os
import sys
import time
import uuid
import logging
from pathlib import Path
from datetime import datetime


def setup_logging(vault_path):
    """Setup logging to approval.log"""
    log_path = Path(vault_path) / 'approval.log'
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_vault_path():
    """Get vault path from env or default"""
    return Path(os.getenv('VAULT_PATH', './AI_Employee_Vault/'))


def ensure_folder_exists(path):
    """Create folder if it doesn't exist"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"APPROVAL_ERROR: Could not create folder {path}: {str(e)}")
        sys.exit(1)


def create_approval_request(vault_path, action, reason):
    """Create human approval request file"""

    request_id = str(uuid.uuid4())[:8]
    approval_folder = Path(vault_path) / 'Needs_Approval'

    ensure_folder_exists(approval_folder)

    timestamp = datetime.now().isoformat()
    request_file = approval_folder / f"REQUEST_{request_id}.md"

    content = f"""# Approval Request

## Request ID
{request_id}

## Timestamp
{timestamp}

## Action
{action}

## Reason
{reason}

## Status
PENDING

---

## Instructions for Human Reviewer

To **APPROVE** this action:
1. Review the action and reason above
2. Change STATUS above from "PENDING" to "APPROVED"
3. Save this file

To **REJECT** this action:
1. Review the action and reason above
2. Change STATUS above from "PENDING" to "REJECTED"
3. Save this file

Do not modify anything else in this file.

---

## Audit Trail
- Created: {timestamp}
- Request ID: {request_id}
"""

    try:
        with open(request_file, 'w') as f:
            f.write(content)
        logging.info(f"APPROVAL_REQUESTED: {request_id} | Action: {action}")
        return request_file
    except Exception as e:
        print(f"APPROVAL_ERROR: Could not create request file: {str(e)}")
        sys.exit(1)


def wait_for_approval(request_file, timeout=3600, poll_interval=2):
    """Wait for human approval"""

    start_time = time.time()
    request_id = request_file.stem.split('_')[1]

    while True:
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed > timeout:
            logging.warning(f"APPROVAL_TIMEOUT: {request_id} | No response after {timeout}s")
            print(f"APPROVAL_TIMEOUT: {request_file.stem} | No response after {timeout}s")
            # Cleanup
            try:
                request_file.unlink()
            except:
                pass
            sys.exit(1)

        # Read current status
        try:
            with open(request_file, 'r') as f:
                content = f.read()

            # Parse status
            status = None
            for line in content.split('\n'):
                if line.startswith('STATUS') or line.startswith('## Status'):
                    parts = line.split('\n')
                    for part in parts:
                        if 'APPROVED' in part:
                            status = 'APPROVED'
                        elif 'REJECTED' in part:
                            status = 'REJECTED'
                        elif 'PENDING' not in part and part.strip():
                            status = part.strip()

            # Check for status change
            if status and status not in ['PENDING', 'STATUS', '##']:
                if 'APPROVED' in status.upper():
                    logging.info(f"APPROVAL_GRANTED: {request_id}")
                    action_name = request_file.stem
                    print(f"APPROVAL_GRANTED: {action_name} | Approved at {datetime.now().isoformat()}")

                    # Cleanup
                    try:
                        request_file.unlink()
                    except:
                        pass
                    return True

                elif 'REJECTED' in status.upper():
                    logging.info(f"APPROVAL_REJECTED: {request_id}")
                    action_name = request_file.stem
                    print(f"APPROVAL_REJECTED: {action_name} | Rejected at {datetime.now().isoformat()}")

                    # Cleanup
                    try:
                        request_file.unlink()
                    except:
                        pass
                    sys.exit(1)

        except Exception as e:
            print(f"APPROVAL_ERROR: Could not read request file: {str(e)}")
            sys.exit(1)

        # Wait before polling again
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(description='Request human approval')
    parser.add_argument('--action', required=True, help='Action to approve')
    parser.add_argument('--reason', required=True, help='Reason for approval')
    parser.add_argument('--timeout', type=int, default=3600, help='Timeout in seconds')
    parser.add_argument('--vault-path', help='Path to vault')

    args = parser.parse_args()

    vault_path = args.vault_path or os.getenv('VAULT_PATH', r'E:\GH-Q4\Hackathon0-FTE\AI_Employee\vault')
    vault_path = Path(vault_path)

    # Ensure vault exists
    if not vault_path.exists():
        print(f"APPROVAL_ERROR: Vault not found at {vault_path}")
        sys.exit(1)

    setup_logging(vault_path)

    # Create request
    request_file = create_approval_request(vault_path, args.action, args.reason)

    # Wait for approval
    wait_for_approval(request_file, timeout=args.timeout)


if __name__ == '__main__':
    main()
