"""
WhatsApp Web Watcher Script for Silver Tier AI Employee
Monitors WhatsApp Web for important messages with keywords and creates action files
Uses Playwright for automation with persistent session storage
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
    logger = logging.getLogger('WhatsAppWatcher')
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
# WHATSAPP WATCHER CLASS
# ============================================================================

class WhatsAppWatcher:
    """Monitor WhatsApp Web for important messages and create action files."""

    # Keywords to monitor for
    KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'sales', 'quote']

    # WhatsApp Web URL
    WHATSAPP_URL = 'https://web.whatsapp.com'

    # Selectors for WhatsApp elements
    CHAT_LIST_SELECTOR = '[role="main"]'  # Main chat list container
    UNREAD_CHAT_SELECTOR = '[aria-label*="unread"]'  # Unread chats

    def __init__(self):
        """
        Initialize WhatsApp Watcher.
        Sets up vault paths, logging, and browser context.
        """
        # ========== VAULT PATHS (Hard-coded) ==========
        self.vault_root = Path.home() / "AI_Employee" / "vault"
        self.needs_action_folder = self.vault_root / "Needs_Action"
        self.session_folder = self.vault_root / "whatsapp_session"
        self.log_file = self.vault_root / "whatsapp_watcher_log.txt"
        self.processed_messages_file = self.vault_root / ".whatsapp_processed_messages.json"

        # Create necessary directories
        self.vault_root.mkdir(parents=True, exist_ok=True)
        self.needs_action_folder.mkdir(parents=True, exist_ok=True)
        self.session_folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = setup_logging(self.log_file)
        self.logger.info("="*70)
        self.logger.info("WhatsApp Watcher initialized")
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
        No QR code needed after first authentication.
        """
        try:
            self.logger.info("Setting up Playwright browser...")

            # Launch Playwright
            self.playwright = sync_playwright().start()
            self.logger.info("✓ Playwright started")

            # Ensure session folder exists
            self.session_folder.mkdir(parents=True, exist_ok=True)

            # Firefox user profile directory (better for persistent sessions)
            firefox_profile_dir = str(self.session_folder / "firefox_profile")

            # Check if this is first run
            first_run = not (self.session_folder / "firefox_profile").exists()

            if first_run:
                self.logger.info("⚠ First run detected - QR code scan will be required")
            else:
                self.logger.info("✓ Loading existing WhatsApp session...")

            # Use Firefox instead of Chromium (better session persistence, avoids automation detection)
            self.logger.info("Launching Firefox browser (avoids Chrome automation detection)...")
            self.browser = self.playwright.firefox.launch_persistent_context(
                firefox_profile_dir,
                headless=False,  # Show browser for QR code
                ignore_https_errors=True
            )

            self.logger.info("✓ Firefox browser launched with persistent profile")
            self.logger.info(f"  Profile path: {firefox_profile_dir}")

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
        # Persistent context automatically saves all state
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

    # ========== PRIVATE METHODS: WHATSAPP INTERACTION ==========

    def _navigate_to_whatsapp(self) -> bool:
        """
        Navigate to WhatsApp Web and wait for login/chat list.

        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            self.logger.info("Navigating to WhatsApp Web...")

            # Inject stealth script to hide Playwright detection
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });
                window.chrome = {
                    runtime: {}
                };
            """)

            self.page.goto(self.WHATSAPP_URL, wait_until='networkidle', timeout=60000)

            # Wait for chat list to appear
            try:
                self.page.wait_for_selector(self.CHAT_LIST_SELECTOR, timeout=60000)
                self.logger.info("✓ WhatsApp chat list loaded (using saved session)")
                time.sleep(2)  # Wait for page to stabilize
                return True
            except PlaywrightTimeoutError:
                self.logger.warning("WhatsApp chat list not found - QR code scan required")
                self.logger.info("Waiting up to 2 minutes for QR code scan...")
                self.logger.info("👉 Please scan the QR code shown in the browser window with your phone")
                self.logger.info("ℹ️  Session will be saved for automatic login on next run")

                try:
                    self.page.wait_for_selector(self.CHAT_LIST_SELECTOR, timeout=120000)
                    self.logger.info("✓ QR code scanned and authenticated successfully!")
                    time.sleep(3)  # Wait for session to stabilize
                    self.logger.info("✓ Session saved to Firefox profile (auto-saved)")

                    return True
                except PlaywrightTimeoutError:
                    self.logger.error("Timeout - QR code not scanned or authentication failed")
                    return False

        except Exception as e:
            self.logger.error(f"Error navigating to WhatsApp: {e}")
            return False

    def _extract_unread_chats(self) -> List[Dict[str, str]]:
        """
        Extract information about unread chats.

        Returns:
            List of dictionaries with chat information
        """
        chats_info = []

        try:
            # Wait for chat items to be present
            try:
                self.page.wait_for_selector('[role="button"]', timeout=10000)
            except PlaywrightTimeoutError:
                self.logger.debug("No chat buttons found")
                return []

            # Find all elements with unread indicator
            unread_elements = self.page.query_selector_all('[aria-label*="unread"]')
            self.logger.debug(f"Found {len(unread_elements)} unread chat elements")

            for elem in unread_elements:
                try:
                    # Get aria-label which contains chat info
                    aria_label = elem.get_attribute('aria-label') or ''

                    # Extract chat name from aria-label
                    # Format is usually: "Chat Name (unread messages)"
                    chat_name = aria_label.split('(')[0].strip() if '(' in aria_label else aria_label

                    if not chat_name or 'unread' not in aria_label.lower():
                        continue

                    # Try to get message preview text
                    span_elem = elem.query_selector('span')
                    preview_text = span_elem.text_content() if span_elem else ''

                    if chat_name:
                        chats_info.append({
                            'name': chat_name,
                            'preview': preview_text.strip() if preview_text else '',
                            'aria_label': aria_label
                        })
                        self.logger.debug(f"Found unread chat: {chat_name}")

                except Exception as e:
                    self.logger.debug(f"Error extracting chat info: {e}")
                    continue

            return chats_info

        except Exception as e:
            self.logger.error(f"Error extracting unread chats: {e}")
            return []

    def _check_keywords(self, text: str) -> List[str]:
        """
        Check if text contains any monitored keywords.

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
            if keyword.lower() in text_lower:
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
        # Replace spaces with underscores
        safe_text = re.sub(r'\s+', '_', safe_text)
        # Remove consecutive underscores
        safe_text = re.sub(r'_+', '_', safe_text)
        # Limit length
        safe_text = safe_text[:50]
        return safe_text

    def create_action_file(
        self,
        chat_name: str,
        message_text: str,
        matched_keywords: List[str]
    ) -> None:
        """
        Create a markdown action file for an important WhatsApp message.

        Args:
            chat_name: Name of the WhatsApp chat
            message_text: The message content
            matched_keywords: Keywords that matched
        """
        try:
            if not message_text or not matched_keywords:
                return

            # Generate unique message ID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            message_id = f"{self._sanitize_filename(chat_name)}_{timestamp}"

            # Skip if already processed
            if message_id in self.processed_messages:
                self.logger.debug(f"Message already processed: {message_id}")
                return

            # ========== CREATE YAML FRONTMATTER ==========
            received_iso = datetime.now().isoformat()

            frontmatter = f"""---
type: whatsapp_message
from_chat: {chat_name}
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

**From Chat:** {chat_name}
**Received:** {received_iso}
**Keywords Matched:** {', '.join(matched_keywords)}

### Message
{message_preview}

## Suggested Actions
- [ ] Reply
- [ ] Escalate
- [ ] Log

---
*Generated by WhatsApp Watcher on {datetime.now().isoformat()}*
"""

            # Combine frontmatter and content
            file_content = frontmatter + markdown_content

            # ========== WRITE FILE ==========
            sanitized_name = self._sanitize_filename(chat_name)
            filename = f"WHATSAPP_{sanitized_name}_{timestamp}.md"
            file_path = self.needs_action_folder / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            # Mark as processed
            self.processed_messages.add(message_id)
            self._save_processed_messages()

            # Log success
            self.logger.info(f"✓ Created action file: {filename}")
            self.logger.info(f"  From: {chat_name}")
            self.logger.info(f"  Keywords: {', '.join(matched_keywords)}")

        except Exception as e:
            self.logger.error(f"Failed to create action file: {e}")

    # ========== PUBLIC METHODS: MAIN LOGIC ==========

    def check_for_updates(self) -> None:
        """
        Check WhatsApp Web for new important messages.

        - Extracts unread chats
        - Checks message content for keywords
        - Creates action files for important messages
        - Updates processed messages cache
        """
        try:
            if not self.page:
                self.logger.error("Page not initialized - skipping check")
                return

            self.logger.debug("[Check] Scanning WhatsApp for important messages...")

            # Try to stay on WhatsApp page
            try:
                if self.page.url != self.WHATSAPP_URL:
                    self.page.goto(self.WHATSAPP_URL, wait_until='networkidle', timeout=30000)
            except Exception:
                pass  # Continue anyway

            # Extract unread chats
            chats = self._extract_unread_chats()

            if not chats:
                self.logger.debug("No unread chats found")
                return

            self.logger.info(f"Found {len(chats)} unread chats")

            # Check each chat for keywords
            for chat in chats:
                chat_name = chat['name']
                preview_text = chat['preview']

                # Check keywords in preview first (quick check)
                matched_keywords = self._check_keywords(preview_text)

                if matched_keywords:
                    self.logger.info(f"✓ Found keywords in: {chat_name}")
                    self.logger.debug(f"  Keywords: {matched_keywords}")
                    self.logger.debug(f"  Preview: {preview_text[:100]}")
                    self.create_action_file(chat_name, preview_text, matched_keywords)

        except PlaywrightTimeoutError:
            self.logger.error("Timeout during check_for_updates")
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")

    def run(self) -> None:
        """
        Run the WhatsApp Watcher in infinite loop.

        - Checks for new important messages every 60 seconds
        - Handles KeyboardInterrupt for graceful shutdown
        - Continues on errors and logs them
        """
        self.logger.info("="*70)
        self.logger.info("STARTING WHATSAPP WATCHER")
        self.logger.info("="*70)
        self.logger.info("Monitoring: WhatsApp Web unread chats")
        self.logger.info(f"Check interval: 60 seconds")
        self.logger.info(f"Keywords: {', '.join(self.KEYWORDS)}")
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
                # Navigate to WhatsApp
                if not self._navigate_to_whatsapp():
                    self.logger.error("Failed to navigate to WhatsApp Web")
                    return

                self.logger.info("✓ WhatsApp Web ready for monitoring")

                while True:
                    check_count += 1
                    self.logger.info(f"\n[Check #{check_count}] Checking for important messages...")

                    try:
                        # Check for updates
                        self.check_for_updates()
                    except Exception as e:
                        self.logger.error(f"Error during check: {e}")
                        # Continue to next check even if this one failed

                    # Wait 60 seconds before next check
                    self.logger.debug("Waiting 60 seconds until next check...")
                    time.sleep(60)

            except KeyboardInterrupt:
                self.logger.info("\n" + "="*70)
                self.logger.info("WhatsApp Watcher stopped by user (Ctrl+C)")
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
        watcher = WhatsAppWatcher()
        watcher.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Failed to start WhatsApp Watcher: {e}")
        print(f"Check log file for details")
        exit(1)
