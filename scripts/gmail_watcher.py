"""
Gmail Watcher Script for Silver Tier AI Employee
Monitors Gmail for unread + important emails and creates action files in vault/Needs_Action
"""

import os
import logging
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Set, Optional, Dict
from email.utils import parsedate_to_datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_file_path: Path) -> logging.Logger:
    """
    Setup logging to both console and file.

    Args:
        log_file_path: Path to the log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('GmailWatcher')
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatter with timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not setup file logging: {e}")

    return logger


# ============================================================================
# GMAIL WATCHER CLASS
# ============================================================================

class GmailWatcher:
    """Monitor Gmail for unread important emails and create action files."""

    # Gmail API scope for read-only access
    GMAIL_SCOPE = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        """
        Initialize Gmail Watcher.
        Sets up vault paths, logging, and authenticates with Gmail API.
        """
        # ========== VAULT PATHS (Hard-coded) ==========
        import os
        from pathlib import Path
        self.vault_root = Path(
        os.getenv("VAULT_PATH", r"E:\GH-Q4\Hackathon0-FTE\AI_Employee\vault")
        )
        self.needs_action_folder = self.vault_root / "Needs_Action"
        self.log_file = self.vault_root / "gmail_watcher_log.txt"
        self.credentials_file = self.vault_root / "gmail_credentials.json"
        self.token_file = self.vault_root / ".gmail_token.json"
        self.processed_ids_file = self.vault_root / ".processed_email_ids.json"

        # Create necessary directories
        self.vault_root.mkdir(parents=True, exist_ok=True)
        self.needs_action_folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = setup_logging(self.log_file)
        self.logger.info("="*70)
        self.logger.info("Gmail Watcher initialized")
        self.logger.info(f"Vault root: {self.vault_root}")
        self.logger.info(f"Needs_Action folder: {self.needs_action_folder}")

        # Load processed email IDs to track what we've already processed
        self.processed_ids: Set[str] = self._load_processed_ids()
        self.logger.info(f"Loaded {len(self.processed_ids)} previously processed email IDs")

        # Initialize Gmail service (will be set during authentication)
        self.service = None

        # Authenticate with Gmail API
        self._authenticate()

    # ========== PRIVATE METHODS: ID TRACKING ==========

    def _load_processed_ids(self) -> Set[str]:
        """
        Load previously processed email IDs from cache file.
        This prevents creating duplicate action files.

        Returns:
            Set of processed email IDs
        """
        try:
            if self.processed_ids_file.exists():
                with open(self.processed_ids_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            return set()
        except Exception as e:
            self.logger.warning(f"Failed to load processed IDs: {e}")
            return set()

    def _save_processed_ids(self) -> None:
        """
        Save processed email IDs to cache file.
        This persists the tracking across script restarts.
        """
        try:
            with open(self.processed_ids_file, 'w', encoding='utf-8') as f:
                json.dump({'processed_ids': list(self.processed_ids)}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save processed IDs: {e}")

    # ========== PRIVATE METHODS: AUTHENTICATION ==========

    def _authenticate(self) -> None:
        """
        Authenticate with Gmail API using OAuth2 credentials.

        Supports:
        - Loading existing token from .gmail_token.json
        - Creating new token from gmail_credentials.json via OAuth2 flow
        - Refreshing expired tokens

        Raises:
            FileNotFoundError: If credentials file not found
            Exception: If authentication fails
        """
        try:
            creds = None

            # Load existing token if available
            if self.token_file.exists():
                try:
                    creds = Credentials.from_authorized_user_file(
                        self.token_file,
                        scopes=self.GMAIL_SCOPE
                    )
                    self.logger.info("Loaded existing Gmail token")
                except Exception as e:
                    self.logger.warning(f"Failed to load token: {e}")

            # If no valid token, get new one
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Refresh expired token
                    try:
                        creds.refresh(Request())
                        self.logger.info("Refreshed Gmail token")
                    except Exception as e:
                        self.logger.warning(f"Token refresh failed: {e}")
                        creds = None

                # If still no valid token, use credentials file for new OAuth flow
                if not creds:
                    if not self.credentials_file.exists():
                        error_msg = (
                            f"Credentials file not found: {self.credentials_file}\n"
                            f"Please download it from Google Cloud Console and place it at:\n"
                            f"{self.credentials_file}"
                        )
                        self.logger.error(error_msg)
                        raise FileNotFoundError(error_msg)

                    # Run OAuth2 flow to get new credentials
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file,
                        scopes=self.GMAIL_SCOPE
                    )
                    creds = flow.run_local_server(port=0)
                    self.logger.info("Completed OAuth2 authorization flow")

                # Save the credentials for next time
                try:
                    with open(self.token_file, 'w', encoding='utf-8') as token:
                        token.write(creds.to_json())
                    self.logger.info("Saved Gmail token for future use")
                except Exception as e:
                    self.logger.warning(f"Failed to save token: {e}")

            # Build Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Successfully authenticated with Gmail API")

        except FileNotFoundError as e:
            self.logger.error(f"Credentials file error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise

    # ========== PRIVATE METHODS: FILE CREATION ==========

    def _extract_email_headers(self, message: dict) -> Dict[str, str]:
        """
        Extract important headers from Gmail message.

        Args:
            message: Gmail message object from API

        Returns:
            Dictionary with email metadata
        """
        headers = message['payload'].get('headers', [])

        # Extract specific headers
        email_dict = {
            'from': next(
                (h['value'] for h in headers if h['name'] == 'From'),
                'Unknown Sender'
            ),
            'subject': next(
                (h['value'] for h in headers if h['name'] == 'Subject'),
                '(No Subject)'
            ),
            'date': next(
                (h['value'] for h in headers if h['name'] == 'Date'),
                datetime.now().isoformat()
            ),
            'to': next(
                (h['value'] for h in headers if h['name'] == 'To'),
                'Unknown'
            ),
        }

        return email_dict

    def _parse_received_date(self, date_str: str) -> str:
        """
        Parse email date string to ISO format.

        Args:
            date_str: Date string from email header

        Returns:
            ISO format datetime string
        """
        try:
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except Exception as e:
            self.logger.warning(f"Failed to parse date '{date_str}': {e}")
            return datetime.now().isoformat()

    def create_action_file(self, message: dict) -> None:
        """
        Create a markdown action file for an email in Needs_Action folder.

        File format:
        - Filename: EMAIL_[message_id].md
        - Content: YAML frontmatter + markdown with email details and action items

        Args:
            message: Gmail message object from API
        """
        try:
            message_id = message['id']

            # Extract email details
            email_headers = self._extract_email_headers(message)
            received_iso = self._parse_received_date(email_headers['date'])

            # Get email snippet (preview text)
            snippet = message.get('snippet', 'No content available')

            # Clean up snippet for markdown
            snippet = snippet.replace('\n', ' ').strip()
            if len(snippet) > 500:
                snippet = snippet[:500] + "..."

            # ========== CREATE YAML FRONTMATTER ==========
            frontmatter = f"""---
type: email
from: {email_headers['from']}
to: {email_headers['to']}
subject: {email_headers['subject']}
received: {received_iso}
priority: high
status: pending
message_id: {message_id}
---
"""

            # ========== CREATE MARKDOWN CONTENT ==========
            markdown_content = f"""
## Email Content

**From:** {email_headers['from']}
**Subject:** {email_headers['subject']}
**Received:** {received_iso}

### Preview
{snippet}

## Suggested Actions
- [ ] Reply
- [ ] Forward
- [ ] Archive
- [ ] Mark as Read

---
*Generated by Gmail Watcher on {datetime.now().isoformat()}*
"""

            # Combine frontmatter and content
            file_content = frontmatter + markdown_content

            # ========== WRITE FILE ==========
            filename = f"EMAIL_{message_id}.md"
            file_path = self.needs_action_folder / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            # Log success
            self.logger.info(f"✓ Created action file: {filename}")
            self.logger.info(f"  From: {email_headers['from']}")
            self.logger.info(f"  Subject: {email_headers['subject']}")

        except Exception as e:
            self.logger.error(f"Failed to create action file for {message_id}: {e}")

    # ========== PUBLIC METHODS: MAIN LOGIC ==========

    def check_for_updates(self) -> None:
        """
        Check Gmail for new unread + important emails.

        - Queries Gmail API with: is:unread is:important
        - Processes each new email (not in processed cache)
        - Creates action file in vault/Needs_Action
        - Updates processed IDs cache

        Handles HTTP errors gracefully and logs all activity.
        """
        try:
            if not self.service:
                self.logger.error("Gmail service not initialized - skipping check")
                return

            # Gmail query: unread AND important emails
            query = 'is:unread is:important'

            # Call Gmail API
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10  # Limit to 10 per check to avoid rate limiting
            ).execute()

            messages = results.get('messages', [])

            if messages:
                self.logger.info(f"Found {len(messages)} unread important emails")

                # Process each message
                for message in messages:
                    message_id = message['id']

                    # Skip if already processed
                    if message_id in self.processed_ids:
                        continue

                    # Get full message details and create action file
                    try:
                        msg = self.service.users().messages().get(
                            userId='me',
                            id=message_id,
                            format='full'
                        ).execute()

                        # Create action file in vault
                        self.create_action_file(msg)

                        # Mark as processed
                        self.processed_ids.add(message_id)
                        self._save_processed_ids()

                    except HttpError as e:
                        self.logger.error(f"Gmail API error for message {message_id}: {e}")
                    except Exception as e:
                        self.logger.error(f"Failed to process message {message_id}: {e}")
            else:
                self.logger.info("No new unread important emails at this time")

        except HttpError as e:
            self.logger.error(f"Gmail API error during check_for_updates: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error checking for updates: {e}")

    def run(self) -> None:
        """
        Run the Gmail Watcher in infinite loop.

        - Checks for emails every 120 seconds (2 minutes)
        - Handles KeyboardInterrupt for graceful shutdown
        - Continues on errors and logs them
        """
        self.logger.info("="*70)
        self.logger.info("STARTING GMAIL WATCHER")
        self.logger.info("="*70)
        self.logger.info("Monitoring: unread + important emails")
        self.logger.info(f"Check interval: 120 seconds (2 minutes)")
        self.logger.info(f"Output folder: {self.needs_action_folder}")
        self.logger.info("="*70)

        check_count = 0

        try:
            while True:
                check_count += 1
                self.logger.info(f"\n[Check #{check_count}] Checking for new emails...")

                # Check for updates
                self.check_for_updates()

                # Wait 120 seconds before next check
                self.logger.info("Waiting 120 seconds until next check...")
                time.sleep(120)

        except KeyboardInterrupt:
            self.logger.info("\n" + "="*70)
            self.logger.info("Gmail Watcher stopped by user (Ctrl+C)")
            self.logger.info(f"Total checks performed: {check_count}")
            self.logger.info(f"Total processed emails: {len(self.processed_ids)}")
            self.logger.info("="*70)

        except Exception as e:
            self.logger.error("="*70)
            self.logger.error(f"FATAL ERROR in watcher loop: {e}")
            self.logger.error("="*70)
            raise


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        watcher = GmailWatcher()
        watcher.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Failed to start Gmail Watcher: {e}")
        print(f"Check log file for details")
        exit(1)
