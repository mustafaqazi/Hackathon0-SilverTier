# LinkedIn Post Skill

## Purpose
Create real LinkedIn posts using browser automation with Playwright.

## Usage
```
python scripts/post_linkedin.py --message "Your post content here"
```

## Requirements
Set environment variables:
- `LINKEDIN_EMAIL` - Your LinkedIn email
- `LINKEDIN_PASSWORD` - Your LinkedIn password

## Parameters
- `--message` (required) - Post content (text only)
- `--headless` (default: true) - Run in headless mode
- `--timeout` (default: 30000ms) - Timeout for operations

## Output
Success: `LINKEDIN_POSTED: [timestamp] | Message length: [chars]`
Error: `LINKEDIN_ERROR: [error message]`

## Installation
Requires Playwright: `pip install playwright`
Then: `playwright install chromium`

## Notes
- Creates text posts only (no media/links in this version)
- Waits for feed to load before posting
- Handles LinkedIn's dynamic layout
- Respects LinkedIn's rate limiting
- Timeout after 5 minutes max

## Security
- Credentials taken from env variables only
- No credential storage or logging
- Browser closes after completion
