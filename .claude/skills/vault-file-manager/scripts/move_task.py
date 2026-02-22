#!/usr/bin/env python3
"""
move_task.py - Manage task workflow files in vault

Usage:
    python move_task.py --action move --source Inbox --destination Needs_Action --file task.md
    python move_task.py --action list --folder Inbox

Environment Variables:
    VAULT_PATH - Path to vault (default: ./AI_Employee_Vault/)
"""

import argparse
import os
import shutil
import sys
import logging
from pathlib import Path
from datetime import datetime


def setup_logging(vault_path):
    """Setup logging to vault.log"""
    log_path = Path(vault_path) / 'vault.log'
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_vault_path():
    """Get vault path from env or default"""
    return Path(os.getenv('VAULT_PATH', './AI_Employee_Vault/'))


def validate_folder(folder_name):
    """Validate folder name"""
    valid_folders = ['Inbox', 'Needs_Action', 'Done', 'Needs_Approval']
    if folder_name not in valid_folders:
        print(f"VAULT_ERROR: Invalid folder '{folder_name}'. Must be one of: {', '.join(valid_folders)}")
        sys.exit(1)
    return folder_name


def ensure_folder_exists(path):
    """Create folder if it doesn't exist"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"VAULT_ERROR: Could not create folder {path}: {str(e)}")
        sys.exit(1)


def move_task(vault_path, source, destination, filename):
    """Move task file between folders"""

    source = validate_folder(source)
    destination = validate_folder(destination)

    source_path = Path(vault_path) / source
    dest_path = Path(vault_path) / destination

    ensure_folder_exists(source_path)
    ensure_folder_exists(dest_path)

    source_file = source_path / filename
    dest_file = dest_path / filename

    # Validate source exists
    if not source_file.exists():
        print(f"VAULT_ERROR: File not found in {source}/{filename}")
        sys.exit(1)

    # Check if destination exists
    if dest_file.exists():
        print(f"VAULT_ERROR: File already exists in {destination}/{filename}")
        sys.exit(1)

    try:
        shutil.move(str(source_file), str(dest_file))
        logging.info(f"MOVED: {filename} from {source} to {destination}")
        print(f"TASK_MOVED: {filename} | From: {source} -> To: {destination}")
        return True
    except Exception as e:
        print(f"VAULT_ERROR: Move failed - {str(e)}")
        logging.error(f"MOVE_FAILED: {filename} - {str(e)}")
        sys.exit(1)


def copy_task(vault_path, source, destination, filename):
    """Copy task file between folders"""

    source = validate_folder(source)
    destination = validate_folder(destination)

    source_path = Path(vault_path) / source
    dest_path = Path(vault_path) / destination

    ensure_folder_exists(source_path)
    ensure_folder_exists(dest_path)

    source_file = source_path / filename
    dest_file = dest_path / filename

    # Validate source exists
    if not source_file.exists():
        print(f"VAULT_ERROR: File not found in {source}/{filename}")
        sys.exit(1)

    # Check if destination exists
    if dest_file.exists():
        print(f"VAULT_ERROR: File already exists in {destination}/{filename}")
        sys.exit(1)

    try:
        shutil.copy2(str(source_file), str(dest_file))
        logging.info(f"COPIED: {filename} from {source} to {destination}")
        print(f"TASK_COPIED: {filename} | From: {source} -> To: {destination}")
        return True
    except Exception as e:
        print(f"VAULT_ERROR: Copy failed - {str(e)}")
        logging.error(f"COPY_FAILED: {filename} - {str(e)}")
        sys.exit(1)


def list_tasks(vault_path, folder):
    """List all tasks in a folder"""

    folder = validate_folder(folder)
    folder_path = Path(vault_path) / folder

    ensure_folder_exists(folder_path)

    try:
        files = sorted([f.name for f in folder_path.glob('*.md')])
        count = len(files)

        if count == 0:
            print(f"TASKS_IN_{folder.upper()}: 0")
        else:
            files_str = ', '.join(files)
            print(f"TASKS_IN_{folder.upper()}: {count} | {files_str}")

        logging.info(f"LISTED: {count} tasks in {folder}")
        return True
    except Exception as e:
        print(f"VAULT_ERROR: List failed - {str(e)}")
        logging.error(f"LIST_FAILED: {folder} - {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Manage vault task files')
    parser.add_argument('--action', default='move', choices=['move', 'copy', 'list'],
                        help='Action to perform')
    parser.add_argument('--source', help='Source folder')
    parser.add_argument('--destination', help='Destination folder')
    parser.add_argument('--file', help='Filename to move/copy')
    parser.add_argument('--folder', help='Folder to list')
    parser.add_argument('--vault-path', help='Path to vault')

    args = parser.parse_args()

    vault_path = args.vault_path or os.getenv('VAULT_PATH', r'E:\GH-Q4\Hackathon0-FTE\AI_Employee\vault')
    
    vault_path = Path(vault_path)

    # Ensure vault exists
    if not vault_path.exists():
        print(f"VAULT_ERROR: Vault not found at {vault_path}")
        sys.exit(1)

    setup_logging(vault_path)

    # Execute action
    if args.action == 'move':
        if not args.source or not args.destination or not args.file:
            print("VAULT_ERROR: --source, --destination, and --file required for move")
            sys.exit(1)
        move_task(vault_path, args.source, args.destination, args.file)

    elif args.action == 'copy':
        if not args.source or not args.destination or not args.file:
            print("VAULT_ERROR: --source, --destination, and --file required for copy")
            sys.exit(1)
        copy_task(vault_path, args.source, args.destination, args.file)

    elif args.action == 'list':
        if not args.folder:
            print("VAULT_ERROR: --folder required for list")
            sys.exit(1)
        list_tasks(vault_path, args.folder)


if __name__ == '__main__':
    main()
