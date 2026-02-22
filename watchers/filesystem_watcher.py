#!/usr/bin/env python3
"""
filesystem_watcher.py
Bronze Tier - Monitors Inbox and prepares files for AI processing

This script watches the vault/Inbox folder for new files, copies them to
vault/Needs_Action, and creates metadata files for AI processing.

Features:
- Monitors file creation events only
- Ignores temporary/partial files
- Creates metadata files with YAML frontmatter
- Comprehensive logging to console and file
- Error handling with graceful continuation
"""

import os
import sys
import logging
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent


# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Vault root path - Change this if your vault location is different
VAULT_ROOT = Path("E:/GH-Q4/Hackathon0-FTE/AI_Employee/vault")

# Folder paths
INBOX_FOLDER = VAULT_ROOT / "Inbox"
NEEDS_ACTION_FOLDER = VAULT_ROOT / "Needs_Action"
LOG_FILE = VAULT_ROOT / "watcher_log.txt"

# File patterns to ignore (temporary, partial, hidden files)
IGNORE_PATTERNS = {'.tmp', '.part', '~$', '.DS_Store', 'Thumbs.db', '.~'}

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging to both console and file"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Log format: timestamp - level - message
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File handler (append mode)
    try:
        file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create file logger: {e}")

    return logger


logger = setup_logging()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def should_ignore_file(filename):
    """Check if file should be ignored"""
    # Check for temporary/partial file patterns
    for pattern in IGNORE_PATTERNS:
        if filename.startswith(pattern) or filename.endswith(pattern):
            return True
    return False


def get_file_size(file_path):
    """Get file size in bytes and KB"""
    try:
        size_bytes = os.path.getsize(file_path)
        size_kb = round(size_bytes / 1024, 2)
        return size_bytes, size_kb
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0, 0.0


def generate_metadata(original_filename, source_path, dest_path):
    """Generate metadata file content in YAML + Markdown format"""
    size_bytes, size_kb = get_file_size(source_path)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Remove extension from filename for metadata file naming
    base_name = Path(original_filename).stem

    metadata_content = f"""---
type: file_drop
original_name: {original_filename}
size_bytes: {size_bytes}
size_kb: {size_kb}
detected_at: {timestamp}
copied_to: {dest_path}
status: pending
---

# New File Detected

**Original File:** {original_filename}
**Size:** {size_kb} KB
**Detected:** {timestamp}
**Status:** Pending Processing

## File Information
- Original Path: {source_path}
- Copy Location: {dest_path}
- Detection Time: {timestamp}

## Next Steps
- [ ] Analyze content
- [ ] Categorize type
- [ ] Archive if needed

## Processing Notes
Add your notes here...
"""

    return base_name, metadata_content


def process_file(file_path):
    """Process a newly created file"""
    filename = os.path.basename(file_path)

    # Check if file should be ignored
    if should_ignore_file(filename):
        logger.info(f"Ignoring temporary file: {filename}")
        return False

    # Wait a moment for file to be fully written
    import time
    time.sleep(0.5)

    try:
        # Check if file still exists (it might have been moved/deleted)
        if not os.path.exists(file_path):
            logger.warning(f"File no longer exists: {file_path}")
            return False

        # Ensure Needs_Action folder exists
        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)

        # Copy file to Needs_Action with metadata preservation
        dest_path = NEEDS_ACTION_FOLDER / filename
        shutil.copy2(file_path, dest_path)
        logger.info(f"Copied file to Needs_Action: {dest_path}")

        # Generate and create metadata file
        base_name, metadata_content = generate_metadata(filename, file_path, str(dest_path))
        metadata_filename = f"META_{base_name}.md"
        metadata_path = NEEDS_ACTION_FOLDER / metadata_filename

        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(metadata_content)
        logger.info(f"Created metadata file: {metadata_path}")

        logger.info(f"Successfully processed: {filename}")
        return True

    except Exception as e:
        logger.error(f"Error processing file {filename}: {e}")
        return False


# ============================================================================
# FILE SYSTEM EVENT HANDLER
# ============================================================================

class InboxFileSystemEventHandler(FileSystemEventHandler):
    """Custom handler for file system events in Inbox folder"""

    def on_created(self, event):
        """Handle file creation events"""
        # Ignore directories, only process files
        if event.is_directory:
            logger.debug(f"Ignoring directory: {event.src_path}")
            return

        filename = os.path.basename(event.src_path)
        logger.info(f"New file detected in Inbox: {filename}")

        # Process the file
        process_file(event.src_path)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to start the file watcher"""
    logger.info("=" * 70)
    logger.info("FileSystem Watcher - Bronze Tier Started")
    logger.info("=" * 70)

    # Verify vault structure
    try:
        # Check if vault root exists
        if not VAULT_ROOT.exists():
            logger.error(f"Vault root path does not exist: {VAULT_ROOT}")
            logger.error("Please create the vault folder structure first")
            return False

        # Create Inbox folder if it doesn't exist
        INBOX_FOLDER.mkdir(parents=True, exist_ok=True)
        logger.info(f"Inbox folder: {INBOX_FOLDER}")

        # Create Needs_Action folder if it doesn't exist
        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)
        logger.info(f"Needs_Action folder: {NEEDS_ACTION_FOLDER}")

        logger.info(f"Log file: {LOG_FILE}")
        logger.info("-" * 70)

    except Exception as e:
        logger.error(f"Error initializing folders: {e}")
        return False

    # Set up file system observer
    event_handler = InboxFileSystemEventHandler()
    observer = Observer()

    try:
        # Schedule the observer to watch the Inbox folder
        observer.schedule(event_handler, str(INBOX_FOLDER), recursive=False)
        logger.info(f"Watching folder: {INBOX_FOLDER}")
        logger.info("Waiting for new files... (Press Ctrl+C to stop)")
        logger.info("-" * 70)

        # Start the observer
        observer.start()

        # Keep the script running
        while True:
            pass

    except KeyboardInterrupt:
        logger.info("Shutdown signal received (Ctrl+C)")
        observer.stop()
        logger.info("FileSystem Watcher stopped")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        observer.stop()
        return False

    finally:
        observer.join()
        logger.info("=" * 70)
        logger.info("FileSystem Watcher terminated")
        logger.info("=" * 70)

    return True


if __name__ == "__main__":
    # Run the watcher
    success = main()
    sys.exit(0 if success else 1)
