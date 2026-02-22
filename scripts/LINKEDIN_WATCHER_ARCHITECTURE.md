# LinkedIn Watcher - Architecture & Flow Documentation

## System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                    LINKEDIN WATCHER ARCHITECTURE                     │
└──────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │  Start Script   │
                        │   __main__()    │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Create Watcher  │
                        │  Instance       │
                        │ __init__()      │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼────┐          ┌────────▼─────────┐      ┌──────▼──────┐
   │ Vault   │          │ Setup Browser    │      │ Load        │
   │ Paths   │          │ _setup_browser() │      │ Processed   │
   │ Config  │          │                  │      │ Messages    │
   └────┬────┘          └────────┬─────────┘      └──────┬──────┘
        │                         │                      │
        │              ┌──────────▼────────────┐         │
        │              │ Persistent Chromium   │         │
        │              │ Browser (headless)    │         │
        │              └──────────┬────────────┘         │
        │                         │                      │
        └────────────────────────┬┴──────────────────────┘
                                 │
                        ┌────────▼────────┐
                        │ Navigate to     │
                        │ LinkedIn        │
                        │ Messaging       │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ First Time:     │
                        │ Manual Login    │ ◄─── Browser shows login
                        │ (wait for user) │      User scans/logs in
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Session Saved   │
                        │ (persistent)    │
                        └────────┬────────┘
                                 │
                    ╔════════════▼════════════╗
                    ║   MAIN LOOP STARTS      ║
                    ║   (runs every 5 min)    ║
                    ╚════════════╤════════════╝
                                 │
                        ┌────────▼────────┐
                        │ Check LinkedIn  │
                        │ Messaging Page  │
                        │ check_for_      │
                        │  updates()      │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼──────────────┐ ┌──────▼────────────┐ ┌─────────▼────────┐
   │ Extract Unread    │ │ Scan for Sales    │ │ Create Action    │
   │ Messages          │ │ Keywords          │ │ Files for Match  │
   │ _extract_unread_  │ │ _check_keywords() │ │ create_action_   │
   │  messages()       │ │                   │ │  file()          │
   └────┬──────────────┘ └──────┬────────────┘ └─────────┬────────┘
        │                       │                        │
        │ Find conversation    │ Match against:         │ Write to:
        │ list items           │ 15 keywords            │ vault/
        │                      │ (case-insensitive)     │ Needs_Action/
        │                      │                        │
        │                      │ lead                   │ MARKDOWN FILE
        │                      │ opportunity            │ ├─ YAML frontmatter
        │                      │ sales                  │ ├─ Sender name
        │                      │ meeting                │ ├─ Keywords matched
        │                      │ proposal               │ ├─ Message content
        │                      │ connect                │ └─ Action checkboxes
        │                      │ interested             │
        │                      │ quote                  │ Track in:
        │                      │ partnership            │ .linkedin_processed_
        │                      │ collaboration          │  messages.json
        │                      │ business               │
        │                      │ deal                   │
        │                      │ contract               │
        │                      │ enquiry                │
        │                      │ request                │
        │                      │                        │
        └─────────────┬────────┴────────────────────────┘
                      │
                ┌─────▼──────┐
                │ Log Results│
                │ to console │
                │ & file     │
                └─────┬──────┘
                      │
                ┌─────▼──────┐
                │ Sleep 300s │  (5 minutes)
                │ (wait)     │
                └─────┬──────┘
                      │
                      │ LOOP BACK ◄────────────────────┐
                      │                                │
                      └────────────────────────────────┘

                   [Ctrl+C pressed? → EXIT]

                        ┌─────────────────┐
                        │ Close Browser   │
                        │ (save session)  │
                        └─────────────────┘
```

---

## Detailed Module Flow

### 1. INITIALIZATION PHASE

```
LinkedInWatcher.__init__()
│
├─ Setup Vault Paths
│  ├─ vault/ (root)
│  ├─ vault/linkedin_session/ (persistent)
│  ├─ vault/Needs_Action/ (output)
│  ├─ vault/linkedin_watcher_log.txt (log)
│  └─ vault/.linkedin_processed_messages.json (tracking)
│
├─ Setup Logging
│  ├─ Console Handler (StreamHandler)
│  └─ File Handler (FileHandler)
│
├─ Load Processed Messages
│  └─ Read .linkedin_processed_messages.json
│      └─ Create Set[str] of message IDs
│
└─ Initialize Browser References
   └─ Set to None (will be initialized in run())
```

---

### 2. BROWSER SETUP PHASE

```
_setup_browser()
│
├─ Launch Playwright
│  └─ start sync_playwright()
│
├─ Create Persistent Context
│  ├─ Use Chromium
│  ├─ Point to: vault/linkedin_session/chrome_user_data/
│  └─ headless=True (background mode)
│
├─ Create Page from Context
│  ├─ Set timeout: 30 seconds
│  └─ Set nav timeout: 60 seconds
│
└─ Inject Stealth Scripts
   └─ Hide Playwright detection
```

---

### 3. NAVIGATION & LOGIN PHASE

```
_navigate_to_linkedin()
│
├─ Go to: https://www.linkedin.com/messaging/
│
├─ Wait for page load
│  └─ wait_until='networkidle' (60s timeout)
│
├─ Check if loaded
│  ├─ YES → Continue to monitoring
│  └─ NO → Check if login needed
│
└─ If login needed:
   ├─ Show message: "Please login manually"
   ├─ Wait for URL change (300s timeout)
   ├─ Once logged in, save session automatically
   └─ Continue to monitoring
```

---

### 4. MAIN MONITORING LOOP

```
run()  [Infinite Loop]
│
├─ While True:
│  │
│  ├─ Increment check counter
│  │
│  ├─ check_for_updates()
│  │  │
│  │  ├─ Verify page initialized
│  │  │
│  │  ├─ Navigate to messaging page
│  │  │
│  │  ├─ _extract_unread_messages()
│  │  │  ├─ Wait for .msg-conversation-listitem elements
│  │  │  ├─ Query all conversation items
│  │  │  ├─ Filter unread conversations
│  │  │  ├─ Extract:
│  │  │  │  ├─ Sender name
│  │  │  │  ├─ Message preview text
│  │  │  │  └─ aria-label (metadata)
│  │  │  └─ Return: List[Dict]
│  │  │
│  │  ├─ For each message:
│  │  │  │
│  │  │  ├─ _check_keywords(message_text)
│  │  │  │  ├─ Convert text to lowercase
│  │  │  │  ├─ Check each keyword with word boundaries
│  │  │  │  └─ Return: List[str] (matched keywords)
│  │  │  │
│  │  │  ├─ If keywords matched:
│  │  │  │  │
│  │  │  │  ├─ create_action_file()
│  │  │  │  │  ├─ Generate message ID
│  │  │  │  │  ├─ Check if already processed
│  │  │  │  │  │  └─ Skip if yes
│  │  │  │  │  │
│  │  │  │  │  ├─ Create YAML frontmatter:
│  │  │  │  │  │  ├─ type: linkedin_message
│  │  │  │  │  │  ├─ from_sender: [name]
│  │  │  │  │  │  ├─ received: [ISO timestamp]
│  │  │  │  │  │  ├─ priority: medium
│  │  │  │  │  │  ├─ status: pending
│  │  │  │  │  │  └─ keywords_matched: [list]
│  │  │  │  │  │
│  │  │  │  │  ├─ Create Markdown content:
│  │  │  │  │  │  ├─ ## Message Content
│  │  │  │  │  │  ├─ From: [sender]
│  │  │  │  │  │  ├─ Received: [time]
│  │  │  │  │  │  ├─ Keywords: [matched]
│  │  │  │  │  │  ├─ ### Message [text]
│  │  │  │  │  │  └─ ## Suggested Actions [checkboxes]
│  │  │  │  │  │
│  │  │  │  │  ├─ Write file to:
│  │  │  │  │  │  └─ vault/Needs_Action/
│  │  │  │  │  │     LINKEDIN_[name]_[timestamp].md
│  │  │  │  │  │
│  │  │  │  │  ├─ Add to processed_messages
│  │  │  │  │  │
│  │  │  │  │  └─ Save processed_messages to JSON
│  │  │  │  │
│  │  │  │  └─ Log success + details
│  │  │
│  │  ├─ Log check results (count, matches)
│  │  │
│  │  └─ Handle errors gracefully
│  │
│  ├─ Log: "Waiting 300 seconds..."
│  │
│  └─ time.sleep(300)  # 5 minutes
│
└─ On Ctrl+C:
   ├─ Log interruption
   ├─ Log statistics (checks, messages processed)
   ├─ Close browser
   └─ Exit gracefully
```

---

## Data Structures

### LinkedInWatcher Instance Variables

```python
class LinkedInWatcher:
    # File Paths
    vault_root: Path                  # vault/ directory
    needs_action_folder: Path         # vault/Needs_Action/
    session_folder: Path              # vault/linkedin_session/
    log_file: Path                    # vault/linkedin_watcher_log.txt
    processed_messages_file: Path     # vault/.linkedin_processed_messages.json

    # Configuration
    KEYWORDS: List[str]               # 15 sales keywords
    LINKEDIN_MESSAGING_URL: str       # URL to monitor
    SELECTORS: Dict[str, str]         # CSS selectors for elements

    # Runtime State
    logger: logging.Logger            # Logger instance
    processed_messages: Set[str]      # Message IDs already processed
    playwright: PlaywrightSync        # Playwright instance
    browser: Optional[Browser]        # Chromium browser
    context: Optional[BrowserContext] # Browser context
    page: Optional[Page]              # Page instance
```

### Message Information Structure

```python
message_info = {
    'sender_name': 'John Smith',      # Extracted from conversation item
    'message_text': 'message content', # Extracted from preview
    'aria_label': 'full aria-label'    # Additional metadata
}
```

### Action File YAML Frontmatter

```yaml
---
type: linkedin_message
from_sender: John Smith
received: 2026-02-19T15:30:45.123456
priority: medium
status: pending
keywords_matched: lead, opportunity
---
```

---

## Error Handling Strategy

```
Error Handling Flow:
│
├─ Timeout Errors
│  ├─ Check page load (60s timeout)
│  ├─ Check element selectors (10s timeout)
│  ├─ Check file operations
│  └─ Log warning + continue to next check
│
├─ Login Errors
│  ├─ Detect login page requirement
│  ├─ Show user message: "Please login manually"
│  ├─ Wait up to 5 minutes for user action
│  ├─ Auto-save session once logged in
│  └─ Continue to monitoring
│
├─ Selector Errors (Missing Elements)
│  ├─ Try to find elements with fallback selectors
│  ├─ Log debug message
│  ├─ Continue with other messages
│  └─ Script continues (doesn't crash)
│
├─ File I/O Errors
│  ├─ Log error (can't create action file)
│  ├─ Continue to next message
│  └─ Retry on next check
│
├─ Network Errors
│  ├─ Timeout during navigation
│  ├─ Log warning
│  ├─ Continue to next check
│  └─ Recover on next iteration
│
└─ Graceful Shutdown
   ├─ Catch KeyboardInterrupt (Ctrl+C)
   ├─ Log statistics
   ├─ Close browser resources
   ├─ Save session state
   └─ Exit cleanly
```

---

## Selector Strategy

```
LinkedIn HTML Structure (Approximate):
│
├─ [role="main"] (main container)
│
├─ .msg-conversation-listitem (each conversation)
│  ├─ [data-unread="true"] (unread indicator)
│  ├─ .msg-s-msg-group__name (sender name)
│  ├─ .msg-s-message-list__content (message text)
│  └─ [aria-label] (full text preview)
│
└─ [aria-label*="unread"] (unread badge)

Selector Selection Logic:
├─ Primary: [data-unread="true"]
├─ Fallback: [aria-label*="unread"]
├─ Parse aria-label: "Name (unread messages)"
└─ Extract message text from multiple possible locations

Note: If LinkedIn updates selectors:
  1. Inspect element in DevTools
  2. Find new selector
  3. Update SELECTORS in code (lines 87-90)
  4. Re-run script
```

---

## Session Persistence

```
Session Saving & Loading:
│
├─ First Run (No Session):
│  ├─ Launch Chromium with chrome_user_data profile
│  ├─ Navigate to LinkedIn
│  ├─ User manually logs in (browser shows login form)
│  ├─ Chromium auto-saves to chrome_user_data/
│  ├─ Session includes: cookies, local storage, indexeddb
│  └─ Script detects successful login via URL change
│
├─ Subsequent Runs (Session Exists):
│  ├─ Launch Chromium with chrome_user_data profile
│  ├─ Chromium auto-loads saved cookies/session
│  ├─ Navigate to LinkedIn
│  ├─ User automatically logged in (no login screen)
│  └─ Proceed directly to monitoring
│
└─ Session Reset:
   ├─ Delete: vault/linkedin_session/chrome_user_data/
   ├─ On next run: Back to "First Run" scenario
   └─ User must login again manually
```

---

## Logging Architecture

```
Logging System:
│
├─ Logger Name: "LinkedInWatcher"
├─ Log Levels: INFO, WARNING, ERROR, DEBUG
│
├─ Formatters: %(asctime)s - %(name)s - %(levelname)s - %(message)s
│
├─ Handlers:
│  ├─ StreamHandler (Console)
│  │  └─ Output: Terminal in real-time
│  │
│  └─ FileHandler (File)
│     └─ Output: vault/linkedin_watcher_log.txt
│
└─ Log Messages:
   ├─ Initialization logs
   ├─ Browser lifecycle logs (start, navigate, close)
   ├─ Check iteration logs
   ├─ Message detection logs
   ├─ File creation logs
   ├─ Error/warning logs
   └─ Statistics logs (on shutdown)
```

---

## Performance Characteristics

```
Resource Usage Timeline:
│
├─ Startup (0-15 seconds)
│  ├─ Memory: grows to ~100MB
│  ├─ CPU: 50-80% (launching browser)
│  └─ Disk: ~50MB (browser cache)
│
├─ Login (if needed)
│  ├─ Memory: ~120MB
│  ├─ CPU: 10-20% (waiting for input)
│  └─ Disk: ~100MB (browser profile)
│
├─ Monitoring Loop (repeating every 5 minutes)
│  │
│  ├─ Idle (waiting):
│  │  ├─ Memory: ~100-120MB
│  │  ├─ CPU: 0-2%
│  │  └─ Network: 0 bytes
│  │
│  └─ During Check (2-5 seconds):
│     ├─ Memory peak: ~150-160MB
│     ├─ CPU: 10-15%
│     └─ Network: ~3-5MB
│
└─ Shutdown (0-5 seconds)
   ├─ Memory: released
   ├─ CPU: 5-10% (cleanup)
   └─ Disk: session saved (~100MB)

Daily Usage (5-minute intervals):
  Checks per day: 288
  Network per day: ~1-1.5GB
  Log file per day: ~1-2MB
  Action files: ~5-50KB (varies)
```

---

## Integration Points

```
LinkedIn Watcher Integration:
│
├─ Input:
│  └─ LinkedIn messaging (via Playwright)
│
├─ Processing:
│  ├─ Keywords matching
│  ├─ Message extraction
│  ├─ Deduplication
│  └─ File generation
│
├─ Output:
│  ├─ Primary: vault/Needs_Action/*.md
│  ├─ Secondary: vault/linkedin_watcher_log.txt
│  └─ Tracking: .linkedin_processed_messages.json
│
└─ Integration with:
   ├─ Gmail Watcher (same output folder)
   ├─ WhatsApp Watcher (same output folder)
   ├─ Task automation (reads Needs_Action/)
   └─ CRM tools (reads action files)
```

---

## State Diagram

```
         ┌──────────────┐
         │ Not Started  │
         └──────┬───────┘
                │ python linkedin_watcher.py
                ▼
         ┌──────────────┐
         │ Initializing │
         └──────┬───────┘
                │
                ▼
         ┌──────────────────┐
         │ Browser Starting │
         └──────┬───────────┘
                │
                ▼
    ┌───────────────────────────┐
    │ Navigate to LinkedIn       │
    │                           │
    │ ┌─ Session exists? ─┐    │
    │ │ YES: Auto-login   │    │
    │ │ NO: Manual login  │    │
    │ └───────────────────┘    │
    └───────────┬───────────────┘
                │
                ▼
        ┌──────────────────┐
        │ Monitoring Active│
        │                  │
        │ Loop every 5min: │
        │ ├─ Check messages│
        │ ├─ Match keywords│
        │ ├─ Create files  │
        │ └─ Log results   │
        │                  │
        │ (Ctrl+C to exit) │
        └──────┬───────────┘
               │ Ctrl+C pressed
               ▼
        ┌──────────────────┐
        │ Shutting Down    │
        │ ├─ Close browser │
        │ ├─ Save session  │
        │ └─ Log stats     │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Stopped          │
        │ (Session saved)  │
        └──────────────────┘
```

---

## File Generated During Execution

```
Action File: vault/Needs_Action/LINKEDIN_John_Smith_20260219_153045_123456.md

Structure:
┌─────────────────────────────────────────────────────┐
│ YAML FRONTMATTER (Lines 1-7)                        │
├─────────────────────────────────────────────────────┤
│ ---                                                 │
│ type: linkedin_message                              │
│ from_sender: John Smith                             │
│ received: 2026-02-19T15:30:45.123456               │
│ priority: medium                                    │
│ status: pending                                     │
│ keywords_matched: lead, opportunity                 │
│ ---                                                 │
├─────────────────────────────────────────────────────┤
│ MARKDOWN CONTENT (Lines 8+)                         │
├─────────────────────────────────────────────────────┤
│ ## Message Content                                  │
│                                                     │
│ **From Sender:** John Smith                         │
│ **Received:** 2026-02-19T15:30:45.123456           │
│ **Keywords Matched:** lead, opportunity             │
│                                                     │
│ ### Message                                         │
│ [Message text/preview here...]                      │
│                                                     │
│ ## Suggested Actions                                │
│ - [ ] Reply with sales pitch                        │
│ - [ ] Schedule call                                 │
│ - [ ] Auto-post related content                     │
│ - [ ] Add to CRM                                    │
│ - [ ] Forward to sales team                         │
│                                                     │
│ ---                                                 │
│ *Generated by LinkedIn Watcher on [timestamp]*      │
└─────────────────────────────────────────────────────┘
```

---

## Next Steps / Enhancement Points

```
Current Implementation:
✅ Basic message monitoring
✅ Keyword matching
✅ File generation
✅ Session persistence
✅ Error handling
✅ Logging

Potential Enhancements:
├─ AI-powered message classification
├─ Automatic lead scoring
├─ CRM integration (Salesforce/HubSpot)
├─ Email response automation
├─ Dashboard for lead tracking
├─ Webhook notifications
├─ Database logging (instead of files)
└─ Advanced natural language processing
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-19
**Status:** Complete
