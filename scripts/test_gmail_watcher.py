"""
Test script for Gmail Watcher
Helps verify setup and credentials without running infinite loop
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required packages are installed."""
    print("\n" + "="*70)
    print("TESTING IMPORTS")
    print("="*70)

    try:
        print("✓ Importing googleapiclient...", end=" ")
        from googleapiclient.discovery import build
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False

    try:
        print("✓ Importing google.auth...", end=" ")
        from google.auth.transport.requests import Request
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False

    try:
        print("✓ Importing google.oauth2...", end=" ")
        from google.oauth2.credentials import Credentials
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False

    try:
        print("✓ Importing google_auth_oauthlib...", end=" ")
        from google_auth_oauthlib.flow import InstalledAppFlow
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False

    print("\n✓ All imports successful!")
    return True


def test_paths():
    """Test if vault paths exist and are writable."""
    print("\n" + "="*70)
    print("TESTING VAULT PATHS")
    print("="*70)

    from pathlib import Path
    vault_root = Path(r"E:\GH-Q4\Hackathon0-FTE\AI_Employee\vault")
    needs_action = vault_root / "Needs_Action"
    credentials_file = vault_root / "gmail_credentials.json"

    print(f"\nVault root: {vault_root}")
    print(f"Exists: {vault_root.exists()}")
    if vault_root.exists():
        print(f"Writable: {vault_root.is_dir()}")

    print(f"\nNeeds_Action folder: {needs_action}")
    print(f"Exists: {needs_action.exists()}")

    print(f"\nCredentials file: {credentials_file}")
    print(f"Exists: {credentials_file.exists()}")

    # Try to create test file
    test_file = vault_root / ".test_write"
    try:
        test_file.write_text("test")
        test_file.unlink()
        print(f"Vault folder is writable: YES")
    except Exception as e:
        print(f"Vault folder is writable: NO - {e}")
        return False

    # Check credentials
    if not credentials_file.exists():
        print("\n⚠ WARNING: gmail_credentials.json not found!")
        print(f"Expected at: {credentials_file}")
        print("\nPlease:")
        print("1. Download credentials from Google Cloud Console")
        print("2. Save as: gmail_credentials.json")
        print("3. Place in: AI_Employee/vault/")
        return False
    else:
        print("\n✓ Credentials file found!")

    return True


def test_gmail_watcher_class():
    """Test if GmailWatcher class can be imported and initialized."""
    print("\n" + "="*70)
    print("TESTING GMAIL WATCHER CLASS")
    print("="*70)

    try:
        print("Importing GmailWatcher...", end=" ")
        from gmail_watcher import GmailWatcher
        print("OK")

        print("Initializing GmailWatcher...", end=" ")
        watcher = GmailWatcher()
        print("OK")

        print("\nGmailWatcher attributes:")
        print(f"  - Vault root: {watcher.vault_root}")
        print(f"  - Needs_Action: {watcher.needs_action_folder}")
        print(f"  - Log file: {watcher.log_file}")
        print(f"  - Processed IDs: {len(watcher.processed_ids)}")

        if watcher.service:
            print(f"  - Gmail service: ✓ Connected")
        else:
            print(f"  - Gmail service: ✗ Not connected")
            return False

        return True

    except FileNotFoundError as e:
        print(f"\nFAILED: {e}")
        print("\nPlease download credentials file:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create/select project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download JSON file")
        print("6. Save to: AI_Employee/vault/gmail_credentials.json")
        return False

    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_action_file_format():
    """Test action file creation format (mock)."""
    print("\n" + "="*70)
    print("TESTING ACTION FILE FORMAT")
    print("="*70)

    from datetime import datetime

    # Mock email message
    mock_message = {
        'id': 'test_msg_123',
        'snippet': 'This is a test email snippet',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'test@example.com'},
                {'name': 'To', 'value': 'recipient@example.com'},
                {'name': 'Subject', 'value': 'Test Email Subject'},
                {'name': 'Date', 'value': 'Thu, 19 Feb 2026 10:30:00 +0000'},
            ]
        }
    }

    print("\nMock email message:")
    print(f"  From: {mock_message['payload']['headers'][0]['value']}")
    print(f"  Subject: {mock_message['payload']['headers'][2]['value']}")
    print(f"  ID: {mock_message['id']}")

    # Simulate file content
    frontmatter = f"""---
type: email
from: {mock_message['payload']['headers'][0]['value']}
to: {mock_message['payload']['headers'][1]['value']}
subject: {mock_message['payload']['headers'][2]['value']}
received: {datetime.now().isoformat()}
priority: high
status: pending
message_id: {mock_message['id']}
---
"""

    markdown_content = f"""
## Email Content

**From:** {mock_message['payload']['headers'][0]['value']}
**Subject:** {mock_message['payload']['headers'][2]['value']}
**Received:** {datetime.now().isoformat()}

### Preview
{mock_message['snippet']}

## Suggested Actions
- [ ] Reply
- [ ] Forward
- [ ] Archive
- [ ] Mark as Read
"""

    file_content = frontmatter + markdown_content

    print("\nGenerated file content:")
    print("-" * 70)
    print(file_content)
    print("-" * 70)

    print("\n✓ Action file format is valid")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + " GMAIL WATCHER - SETUP VERIFICATION ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    results = {}

    # Test imports
    results['imports'] = test_imports()

    # Test paths
    if results['imports']:
        results['paths'] = test_paths()
    else:
        print("\n⚠ Skipping path tests (import failed)")
        results['paths'] = False

    # Test Gmail Watcher class
    if results['paths']:
        results['class'] = test_gmail_watcher_class()
    else:
        print("\n⚠ Skipping class tests (path tests failed)")
        results['class'] = False

    # Test action file format
    results['format'] = test_create_action_file_format()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name.upper()}")

    all_passed = all(results.values())

    print("\n" + "="*70)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now run:")
        print("  python gmail_watcher.py")
        print("\nOr use batch file:")
        print("  run_gmail_watcher.bat")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above and try again")

    print("="*70 + "\n")

    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
