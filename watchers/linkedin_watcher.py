"""
LinkedIn Watcher Script for Silver Tier AI Employee
Monitors LinkedIn messaging and notifications for sales-related messages
Uses Playwright for automation with persistent session storage
Creates action files when sales keywords are detected
"""

import os
import logging
import time
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Set, List, Dict, Optional

from playwright.sync_api import (
    sync_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)


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
    logger = logging.getLogger('LinkedInWatcher')
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
# LINKEDIN WATCHER CLASS
# ============================================================================

class LinkedInWatcher:
    """Monitor LinkedIn for sales-related messages and create action files."""

    # Sales-related keywords to monitor
    KEYWORDS = [
        'lead', 'opportunity', 'sales', 'meeting', 'proposal',
        'connect', 'interested', 'quote', 'partnership', 'collaboration',
        'business', 'deal', 'contract', 'enquiry', 'request'
    ]

    # LinkedIn messaging URL
    LINKEDIN_MESSAGING_URL = 'https://www.linkedin.com/messaging/'
    LINKEDIN_NOTIFICATIONS_URL = 'https://www.linkedin.com/notifications/'

    # Selectors for LinkedIn elements (approximate - may need adjustment)
    UNREAD_CONVERSATION_SELECTOR = '[data-unread="true"]'  # Unread conversations
    CONVERSATION_ITEM_SELECTOR = '.msg-conversation-listitem'  # Conversation items
    MESSAGE_TEXT_SELECTOR = '.msg-s-message-list__content'  # Message content
    SENDER_NAME_SELECTOR = '.msg-s-msg-group__name'  # Sender name

    def __init__(self):
        """
        Initialize LinkedIn Watcher.
        Sets up vault paths, logging, and browser context.
        """
        # ========== VAULT PATHS ==========
        self.vault_root = Path.home() / "AI_Employee" / "vault"
        self.needs_action_folder = self.vault_root / "Needs_Action"
        self.session_folder = self.vault_root / "linkedin_session"
        self.log_file = self.vault_root / "linkedin_watcher_log.txt"
        self.processed_messages_file = self.vault_root / ".linkedin_processed_messages.json"

        # Create necessary directories
        self.vault_root.mkdir(parents=True, exist_ok=True)
        self.needs_action_folder.mkdir(parents=True, exist_ok=True)
        self.session_folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = setup_logging(self.log_file)
        self.logger.info("="*70)
        self.logger.info("LinkedIn Watcher initialized")
        self.logger.info(f"Vault root: {self.vault_root}")
        self.logger.info(f"Session folder: {self.session_folder}")
        self.logger.info(f"Needs_Action folder: {self.needs_action_folder}")
        self.logger.info(f"Keywords to monitor: {', '.join(self.KEYWORDS)}")

        # Load processed messages to prevent duplicates
        self.processed_messages: Set[str] = self._load_processed_messages()
        self.logger.info(f"Loaded {len(self.processed_messages)} previously processed messages")

        # Browser and context
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    # ========== PRIVATE METHODS: MESSAGE TRACKING ==========

    def _load_processed_messages(self) -> Set[str]:
        """
        Load previously processed message IDs from cache file.
        This prevents creating duplicate action files.

        Returns:
            Set of processed message IDs
        """
        try:
            if self.processed_messages_file.exists():
                with open(self.processed_messages_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('processed_messages', []))
            return set()
        except Exception as e:
            self.logger.warning(f"Failed to load processed messages: {e}")
            return set()

    def _save_processed_messages(self) -> None:
        """
        Save processed message IDs to cache file.
        This persists the tracking across script restarts.
        """
        try:
            with open(self.processed_messages_file, 'w', encoding='utf-8') as f:
                json.dump({'processed_messages': list(self.processed_messages)}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save processed messages: {e}")

    # ========== PRIVATE METHODS: BROWSER SETUP ==========

    def _setup_browser(self) -> None:
        """
        Setup and launch Playwright browser with persistent session.

        Uses user data directory so session persists across restarts.
        First run requires LinkedIn login, then session is saved for future runs.
        """
        try:
            self.logger.info("Setting up Playwright browser...")

            # Launch Playwright
            self.playwright = sync_playwright().start()
            self.logger.info("✓ Playwright started")

            # Ensure session folder exists
            self.session_folder.mkdir(parents=True, exist_ok=True)

            # Chrome user data directory for persistent session
            chrome_user_data_dir = str(self.session_folder / "chrome_user_data")

            # Check if this is first run
            first_run = not (self.session_folder / "chrome_user_data").exists()

            if first_run:
                self.logger.info("⚠ First run detected - LinkedIn login will be required")
            else:
                self.logger.info("✓ Loading existing LinkedIn session...")

            # Use Chromium with persistent user data directory
            self.logger.info("Launching Chromium browser...")
            self.browser = self.playwright.chromium.launch_persistent_context(
                chrome_user_data_dir,
                headless=True,  # Headless mode for efficiency
                ignore_https_errors=True,
                locale='en-US'
            )

            self.logger.info("✓ Chromium browser launched with persistent profile")
            self.logger.info(f"  Profile path: {chrome_user_data_dir}")

            # The persistent context IS our context
            self.context = self.browser

            # Create page from the persistent context
            self.page = self.context.new_page()
            self.page.set_default_timeout(30000)  # 30 second timeout
            self.page.set_default_navigation_timeout(60000)

            self.logger.info("✓ Browser page initialized")

        except Exception as e:
            self.logger.error(f"Failed to setup browser: {e}")
            raise

    def _save_session_state(self) -> None:
        """Session is auto-saved by persistent context - no action needed."""
        self.logger.debug("Session state auto-saved by persistent context")

    def _close_browser(self) -> None:
        """Close browser and cleanup resources."""
        try:
            if self.page:
                try:
                    self.page.close()
                    self.logger.debug("Page closed")
                except Exception as e:
                    self.logger.debug(f"Error closing page: {e}")

            # For persistent context, we close the context which auto-saves session
            if self.context:
                try:
                    self.context.close()
                    self.logger.debug("Context closed (session auto-saved)")
                except Exception as e:
                    self.logger.debug(f"Error closing context: {e}")

            if self.playwright:
                try:
                    self.playwright.stop()
                    self.logger.debug("Playwright stopped")
                except Exception as e:
                    self.logger.debug(f"Error stopping Playwright: {e}")

            self.logger.info("✓ Browser and resources closed")
        except Exception as e:
            self.logger.debug(f"Error during cleanup: {e}")

    # ========== PRIVATE METHODS: LINKEDIN INTERACTION ==========

    def _navigate_to_linkedin(self) -> bool:
        """
        Navigate to LinkedIn messaging and wait for page to load.

        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            self.logger.info("Navigating to LinkedIn messaging...")

            # Inject stealth script to hide Playwright detection
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });
                window.chrome = {
                    runtime: {}
                };
            """)

            # Navigate to messaging page
            self.page.goto(self.LINKEDIN_MESSAGING_URL, wait_until='networkidle', timeout=60000)
            self.logger.info("✓ LinkedIn messaging page loaded")

            # Wait a moment for content to fully load
            time.sleep(2)
            return True

        except PlaywrightTimeoutError:
            self.logger.warning("Timeout loading LinkedIn messaging page")

            # Check if we need to login
            try:
                # Try to detect login page
                if 'login' in self.page.url.lower():
                    self.logger.error("❌ LinkedIn login required!")
                    self.logger.info("👉 Please login to LinkedIn in the browser window that appeared")
                    self.logger.info("ℹ️  Session will be saved for automatic login on next run")

                    # Wait for user to login and navigate
                    try:
                        self.page.wait_for_url(self.LINKEDIN_MESSAGING_URL, timeout=300000)
                        self.logger.info("✓ Login successful! Session saved.")
                        time.sleep(3)
                        return True
                    except PlaywrightTimeoutError:
                        self.logger.error("Timeout waiting for login")
                        return False
            except Exception as e:
                self.logger.debug(f"Error checking login status: {e}")

            return False

        except Exception as e:
            self.logger.error(f"Error navigating to LinkedIn: {e}")
            return False

    def _extract_unread_messages(self) -> List[Dict[str, str]]:
        """
        Extract information about unread messages from conversation list.

        Returns:
            List of dictionaries with message information
        """
        messages_info = []

        try:
            # Wait for conversation list to be present
            try:
                self.page.wait_for_selector(self.CONVERSATION_ITEM_SELECTOR, timeout=10000)
            except PlaywrightTimeoutError:
                self.logger.debug("No conversations found or conversation list not loaded")
                return []

            # Find all conversation items
            conversation_elements = self.page.query_selector_all(self.CONVERSATION_ITEM_SELECTOR)
            self.logger.debug(f"Found {len(conversation_elements)} total conversation items")

            for elem in conversation_elements:
                try:
                    # Check if conversation is unread
                    # LinkedIn marks unread with specific styling - try multiple approaches
                    aria_label = elem.get_attribute('aria-label') or ''
                    data_unread = elem.get_attribute('data-unread') or ''

                    # Check for unread indicators
                    is_unread = 'unread' in aria_label.lower() or data_unread == 'true'

                    if not is_unread:
                        continue

                    # Extract sender name
                    name_elem = elem.query_selector(self.SENDER_NAME_SELECTOR)
                    sender_name = name_elem.text_content() if name_elem else 'Unknown'

                    # Try to get message preview/snippet
                    # LinkedIn stores message text in various places
                    message_elem = elem.query_selector(self.MESSAGE_TEXT_SELECTOR)
                    if not message_elem:
                        message_elem = elem.query_selector('.msg-conversation-listitem__message')

                    message_text = ''
                    if message_elem:
                        message_text = message_elem.text_content() or ''

                    # Also check aria-label which often contains preview text
                    if not message_text and aria_label:
                        # aria-label might contain: "Name: message preview"
                        if ':' in aria_label:
                            message_text = aria_label.split(':', 1)[1].strip()

                    if sender_name and sender_name != 'Unknown':
                        messages_info.append({
                            'sender_name': sender_name.strip(),
                            'message_text': message_text.strip(),
                            'aria_label': aria_label
                        })
                        self.logger.debug(f"Found unread message from: {sender_name}")

                except Exception as e:
                    self.logger.debug(f"Error extracting message info: {e}")
                    continue

            return messages_info

        except Exception as e:
            self.logger.error(f"Error extracting unread messages: {e}")
            return []

    def _check_keywords(self, text: str) -> List[str]:
        """
        Check if text contains any monitored sales keywords.

        Args:
            text: Text to check

        Returns:
            List of matched keywords
        """
        if not text:
            return []

        matched = []
        text_lower = text.lower()

        for keyword in self.KEYWORDS:
            # Use word boundary to avoid partial matches
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                matched.append(keyword)

        return matched

    # ========== PRIVATE METHODS: FILE CREATION ==========

    def _sanitize_filename(self, text: str) -> str:
        """
        Sanitize text for use in filename.

        Args:
            text: Text to sanitize

        Returns:
            Safe filename string
        """
        # Remove invalid characters
        safe_text = re.sub(r'[<>:"/\\|?*]', '', text)
        # Replace spaces and special chars with underscores
        safe_text = re.sub(r'\s+', '_', safe_text)
        # Remove consecutive underscores
        safe_text = re.sub(r'_+', '_', safe_text)
        # Limit length
        safe_text = safe_text[:50]
        return safe_text

    def create_action_file(
        self,
        sender_name: str,
        message_text: str,
        matched_keywords: List[str]
    ) -> None:
        """
        Create a markdown action file for a sales-related LinkedIn message.

        File format:
        - Filename: LINKEDIN_[sender_name sanitized]_[timestamp].md
        - Content: YAML frontmatter + markdown with message details and action items

        Args:
            sender_name: Name of the sender
            message_text: The message content
            matched_keywords: Keywords that matched
        """
        try:
            if not message_text or not matched_keywords:
                return

            # Generate unique message ID with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            message_id = f"{self._sanitize_filename(sender_name)}_{timestamp}"

            # Skip if already processed
            if message_id in self.processed_messages:
                self.logger.debug(f"Message already processed: {message_id}")
                return

            # ========== CREATE YAML FRONTMATTER ==========
            received_iso = datetime.now().isoformat()

            frontmatter = f"""---
type: linkedin_message
from_sender: {sender_name}
received: {received_iso}
priority: medium
status: pending
keywords_matched: {', '.join(matched_keywords)}
---
"""

            # ========== CLEAN MESSAGE TEXT ==========
            message_preview = message_text.replace('\n', ' ').strip()
            if len(message_preview) > 500:
                message_preview = message_preview[:500] + "..."

            # ========== CREATE MARKDOWN CONTENT ==========
            markdown_content = f"""
## Message Content

**From Sender:** {sender_name}
**Received:** {received_iso}
**Keywords Matched:** {', '.join(matched_keywords)}

### Message
{message_preview}

## Suggested Actions
- [ ] Reply with sales pitch
- [ ] Schedule call
- [ ] Auto-post related content
- [ ] Add to CRM
- [ ] Forward to sales team

---
*Generated by LinkedIn Watcher on {datetime.now().isoformat()}*
"""

            # Combine frontmatter and content
            file_content = frontmatter + markdown_content

            # ========== WRITE FILE ==========
            sanitized_name = self._sanitize_filename(sender_name)
            filename = f"LINKEDIN_{sanitized_name}_{timestamp}.md"
            file_path = self.needs_action_folder / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            # Mark as processed
            self.processed_messages.add(message_id)
            self._save_processed_messages()

            # Log success
            self.logger.info(f"✓ Created action file: {filename}")
            self.logger.info(f"  From: {sender_name}")
            self.logger.info(f"  Keywords: {', '.join(matched_keywords)}")

        except Exception as e:
            self.logger.error(f"Failed to create action file: {e}")

    # ========== PUBLIC METHODS: MAIN LOGIC ==========

    def check_for_updates(self) -> None:
        """
        Check LinkedIn for new important messages with sales keywords.

        - Extracts unread messages from conversation list
        - Checks message content for sales keywords
        - Creates action files for messages with matching keywords
        - Updates processed messages cache
        """
        try:
            if not self.page:
                self.logger.error("Page not initialized - skipping check")
                return

            self.logger.debug("[Check] Scanning LinkedIn for sales messages...")

            # Try to stay on LinkedIn messaging page
            try:
                current_url = self.page.url
                if self.LINKEDIN_MESSAGING_URL not in current_url:
                    self.logger.info("Navigating back to messaging page...")
                    self.page.goto(self.LINKEDIN_MESSAGING_URL, wait_until='networkidle', timeout=30000)
                    time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Error navigating to messaging: {e}")
                return

            # Extract unread messages
            messages = self._extract_unread_messages()

            if not messages:
                self.logger.info("No unread messages found")
                return

            self.logger.info(f"Found {len(messages)} unread messages")

            # Check each message for keywords
            for message in messages:
                sender_name = message['sender_name']
                message_text = message['message_text']

                # Check keywords in message text
                matched_keywords = self._check_keywords(message_text)

                if matched_keywords:
                    self.logger.info(f"✓ Found sales keywords in message from: {sender_name}")
                    self.logger.debug(f"  Keywords: {matched_keywords}")
                    self.logger.debug(f"  Preview: {message_text[:100]}")
                    self.create_action_file(sender_name, message_text, matched_keywords)

        except PlaywrightTimeoutError:
            self.logger.error("Timeout during check_for_updates")
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")

    def run(self) -> None:
        """
        Run the LinkedIn Watcher in infinite loop.

        - Checks for new sales-related messages every 300 seconds (5 minutes)
        - Handles KeyboardInterrupt for graceful shutdown
        - Continues on errors and logs them
        """
        self.logger.info("="*70)
        self.logger.info("STARTING LINKEDIN WATCHER")
        self.logger.info("="*70)
        self.logger.info("Monitoring: LinkedIn messaging for sales leads")
        self.logger.info(f"Check interval: 300 seconds (5 minutes)")
        self.logger.info(f"Sales keywords: {', '.join(self.KEYWORDS)}")
        self.logger.info(f"Output folder: {self.needs_action_folder}")
        self.logger.info("="*70)

        check_count = 0
        browser_closed = False

        try:
            # Setup browser once
            try:
                self._setup_browser()
            except Exception as e:
                self.logger.error(f"Failed to setup browser: {e}")
                return

            try:
                # Navigate to LinkedIn
                if not self._navigate_to_linkedin():
                    self.logger.error("Failed to navigate to LinkedIn")
                    return

                self.logger.info("✓ LinkedIn ready for monitoring")

                while True:
                    check_count += 1
                    self.logger.info(f"\n[Check #{check_count}] Checking for sales messages...")

                    try:
                        # Check for updates
                        self.check_for_updates()
                    except Exception as e:
                        self.logger.error(f"Error during check: {e}")
                        # Continue to next check even if this one failed

                    # Wait 300 seconds (5 minutes) before next check
                    self.logger.info("Waiting 300 seconds (5 minutes) until next check...")
                    time.sleep(300)

            except KeyboardInterrupt:
                self.logger.info("\n" + "="*70)
                self.logger.info("LinkedIn Watcher stopped by user (Ctrl+C)")
                self.logger.info(f"Total checks performed: {check_count}")
                self.logger.info(f"Total processed messages: {len(self.processed_messages)}")
                self.logger.info("="*70)

            except Exception as e:
                self.logger.error("="*70)
                self.logger.error(f"ERROR in watcher loop: {e}")
                self.logger.error("="*70)

        finally:
            # Always close browser (only once)
            if not browser_closed:
                self._close_browser()
                browser_closed = True


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        watcher = LinkedInWatcher()
        watcher.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Failed to start LinkedIn Watcher: {e}")
        print(f"Check log file for details")
        exit(1)
