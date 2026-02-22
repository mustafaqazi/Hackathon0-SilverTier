#!/usr/bin/env python3
"""
post_linkedin.py - Create LinkedIn posts via browser automation

Usage:
    python post_linkedin.py --message "Your post content"

Environment Variables:
    LINKEDIN_EMAIL - LinkedIn account email
    LINKEDIN_PASSWORD - LinkedIn account password
"""

import argparse
import os
import sys
import asyncio
from datetime import datetime

try:
    from dotenv import load_dotenv
    from playwright.async_api import async_playwright
except ImportError:
    print("LINKEDIN_ERROR: Required packages not installed. Run: pip install python-dotenv playwright")
    sys.exit(1)


async def post_to_linkedin(message, headless=True, timeout=30000):
    """Post to LinkedIn using Playwright"""

    # Load environment variables from .env file
    load_dotenv()
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("LINKEDIN_ERROR: LINKEDIN_EMAIL and LINKEDIN_PASSWORD required")
        sys.exit(1)

    # Validate message
    if not message or len(message.strip()) == 0:
        print("LINKEDIN_ERROR: Message cannot be empty")
        sys.exit(1)

    if len(message) > 3000:
        print("LINKEDIN_ERROR: Message exceeds 3000 character limit")
        sys.exit(1)

    browser = None
    try:
        print(f"[DEBUG] Starting browser launch with headless={headless}")
        async with async_playwright() as p:
            print("[DEBUG] Launching Chromium...")
            browser = await p.chromium.launch(headless=headless)
            print("[DEBUG] Browser launched successfully")
            context = await browser.new_context()
            page = await context.new_page()

            # Set timeout
            page.set_default_timeout(timeout)

            # Navigate to LinkedIn
            print("[DEBUG] Navigating to LinkedIn login page...")
            await page.goto('https://www.linkedin.com/login', wait_until='networkidle')
            print("[DEBUG] LinkedIn page loaded")

            # Login
            print("[DEBUG] Attempting login...")
            await page.fill('input[name="session_key"]', email)
            print("[DEBUG] Email entered")
            await page.fill('input[name="session_password"]', password)
            print("[DEBUG] Password entered")
            await page.click('button[type="submit"]')
            print("[DEBUG] Login button clicked, waiting for feed...")

            # Wait for feed to load
            try:
                await page.wait_for_selector('[data-test-id="feed-container"]', timeout=timeout)
                print("[DEBUG] Feed loaded successfully")
            except:
                # Alternative wait
                print("[DEBUG] Feed selector not found, waiting 3 seconds...")
                await page.wait_for_timeout(3000)
                print("[DEBUG] Timeout completed")

            # Close any popups/modals that might be blocking
            print("[DEBUG] Checking for popups...")
            try:
                # Simple approach: look for any visible close/dismiss buttons and click them
                await page.evaluate("""
                    () => {
                        const buttons = Array.from(document.querySelectorAll('button'));
                        const closeButtons = buttons.filter(b =>
                            b.getAttribute('aria-label')?.includes('Close') ||
                            b.getAttribute('aria-label')?.includes('Dismiss') ||
                            b.textContent?.includes('Dismiss') ||
                            b.textContent?.includes('Close')
                        );
                        closeButtons.forEach(b => {
                            if (b.offsetHeight > 0) b.click();
                        });
                    }
                """)
                await page.wait_for_timeout(500)
                print("[DEBUG] Popup close attempt completed")
            except Exception as e:
                print(f"[DEBUG] Popup close attempt had error (continuing): {str(e)[:50]}")

            # Take screenshot for debugging
            print("[DEBUG] Taking screenshot after popup check...")
            await page.screenshot(path='linkedin_debug.png')
            print("[DEBUG] Screenshot saved to linkedin_debug.png")

            # Click on the "Start a post" button - comprehensive search
            print("[DEBUG] Looking for 'Start a post' button...")

            # Scroll to top
            await page.evaluate('window.scrollTo(0, 0)')
            await page.wait_for_timeout(800)

            clicked = False

            # Try to find and click "Start a post" using comprehensive JavaScript search
            try:
                print("[DEBUG] Searching for 'Start a post' with JavaScript...")
                result = await page.evaluate("""
                    () => {
                        // Search for any element containing "Start a post"
                        const allElements = document.querySelectorAll('*');
                        let found = null;

                        for (let el of allElements) {
                            // Check direct text content
                            if (el.textContent && el.textContent.includes('Start a post')) {
                                // Find the closest clickable element (button, div with role, etc)
                                let clickable = el;
                                while (clickable && clickable !== document.body) {
                                    if (clickable.tagName === 'BUTTON' ||
                                        clickable.getAttribute('role') === 'button' ||
                                        clickable.getAttribute('role') === 'link' ||
                                        clickable.onclick !== null ||
                                        clickable.className.includes('cursor-pointer') ||
                                        clickable.style.cursor === 'pointer') {
                                        found = clickable;
                                        break;
                                    }
                                    clickable = clickable.parentElement;
                                }
                                if (found) break;
                            }
                        }

                        if (found) {
                            console.log('Found Start a post button');
                            found.click();
                            return true;
                        }
                        return false;
                    }
                """)
                if result:
                    print("[DEBUG] Successfully found and clicked 'Start a post'")
                    clicked = True
                    await page.wait_for_timeout(1000)
            except Exception as e:
                print(f"[DEBUG] JavaScript search failed: {str(e)[:80]}")

            if not clicked:
                print("[WARNING] Could not find 'Start a post' button")
                await page.screenshot(path='linkedin_debug_postbox.png')
                print("[DEBUG] Screenshot saved")

                # Try alternative: look for any button and log what we find
                try:
                    buttons = await page.query_selector_all('button')
                    print(f"[DEBUG] Found {len(buttons)} buttons on page")
                    for i, btn in enumerate(buttons[:10]):
                        try:
                            text = await btn.inner_text()
                            if text.strip():
                                print(f"[DEBUG] Button {i}: {text[:50]}")
                        except:
                            pass
                except:
                    pass

            # Wait for text area
            print("[DEBUG] Waiting for text area to appear...")
            await page.wait_for_timeout(1000)

            # Find and fill text area
            print("[DEBUG] Attempting to fill text area...")
            text_area_selectors = [
                'div[contenteditable="true"]',
                'textarea',
                'p[contenteditable="true"]'
            ]

            filled = False
            for selector in text_area_selectors:
                try:
                    print(f"[DEBUG] Trying text area selector: {selector}")
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"[DEBUG] Found {len(elements)} elements matching {selector}")
                        for elem in elements:
                            is_visible = await elem.is_visible()
                            if is_visible:
                                print(f"[DEBUG] Found visible element, typing message...")
                                await elem.focus()
                                await elem.type(message)
                                filled = True
                                print("[DEBUG] Message typed successfully")
                                break
                    if filled:
                        break
                except Exception as e:
                    print(f"[DEBUG] Text area selector failed: {selector} - {str(e)}")
                    continue

            if not filled:
                # Direct input attempt
                print("[DEBUG] Text area not found, attempting direct keyboard input...")
                await page.keyboard.type(message)
                print("[DEBUG] Message typed via keyboard")

            # Find and click post button
            print("[DEBUG] Looking for post button...")
            await page.wait_for_timeout(500)

            post_button_selectors = [
                'button:has-text("Post")',
                'button[aria-label*="post"]',
                '[data-test-id="post-button"]',
                'button:has-text("Share")'
            ]

            posted = False
            for selector in post_button_selectors:
                try:
                    print(f"[DEBUG] Trying post button selector: {selector}")
                    button = await page.query_selector(selector)
                    if button:
                        is_enabled = not await button.is_disabled()
                        print(f"[DEBUG] Button found, enabled: {is_enabled}")
                        if is_enabled:
                            await button.click()
                            posted = True
                            print(f"[DEBUG] Post button clicked successfully")
                            break
                except Exception as e:
                    print(f"[DEBUG] Post button selector failed: {selector} - {str(e)}")
                    continue

            if not posted:
                print("LINKEDIN_ERROR: Could not find or click post button")
                print("[DEBUG] Keeping browser open for inspection (10 seconds)...")
                await page.wait_for_timeout(10000)
                sys.exit(1)

            # Wait for success
            print("[DEBUG] Post submitted, waiting for confirmation...")
            await page.wait_for_timeout(2000)

            # Check if posted
            print("[DEBUG] Checking for success message...")
            success_selectors = [
                'text=Your post was shared',
                'text=Post shared',
                '[role="alert"]'
            ]

            for selector in success_selectors:
                try:
                    print(f"[DEBUG] Waiting for: {selector}")
                    await page.wait_for_selector(selector, timeout=5000)
                    print(f"[DEBUG] Success selector found: {selector}")
                    break
                except:
                    print(f"[DEBUG] Success selector not found: {selector}")
                    continue

            # Output success
            timestamp = datetime.now().isoformat()
            print(f"LINKEDIN_POSTED: {timestamp} | Message length: {len(message)} chars")
            print("[DEBUG] Keeping browser open for 5 seconds...")
            await page.wait_for_timeout(5000)

            await context.close()
            await browser.close()
            return True

    except Exception as e:
        error_msg = str(e).split('\n')[0][:200]
        print(f"LINKEDIN_ERROR: {error_msg}")
        print(f"[DEBUG] Full error: {str(e)}")
        if browser:
            try:
                await browser.close()
            except:
                pass
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Post to LinkedIn')
    parser.add_argument('--message', required=True, help='Post message')
    parser.add_argument('--headless', type=lambda x: x.lower() not in ('false', '0', 'no'), default=True, help='Run headless (default: True)')
    parser.add_argument('--timeout', type=int, default=30000, help='Timeout in ms')

    args = parser.parse_args()

    print(f"[DEBUG] Parsed arguments: message='{args.message}', headless={args.headless}, timeout={args.timeout}")

    asyncio.run(post_to_linkedin(
        message=args.message,
        headless=args.headless,
        timeout=args.timeout
    ))


if __name__ == '__main__':
    main()
