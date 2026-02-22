# Gmail Send Skill

## Purpose
Send real emails via SMTP using Gmail or any SMTP provider.

## Usage
```
python scripts/send_email.py --to recipient@example.com --subject "Subject" --body "Email body"
```

## Requirements
Set environment variables:
- `EMAIL_ADDRESS` - Your email address
- `EMAIL_PASSWORD` - App password or SMTP password

## Parameters
- `--to` (required) - Recipient email address
- `--subject` (required) - Email subject
- `--body` (required) - Email body text
- `--cc` (optional) - CC email addresses (comma-separated)
- `--smtp-host` (default: smtp.gmail.com)
- `--smtp-port` (default: 587)

## Output
Success: `EMAIL_SENT: recipient@example.com | Subject: [subject]`
Error: `EMAIL_ERROR: [error message]`

## Notes
- For Gmail: Use App Passwords, not regular password
- Supports both text and plaintext emails
- Errors include detailed messages for debugging
