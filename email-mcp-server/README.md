# Email MCP Server

A Model Context Protocol (MCP) server for sending emails via Gmail using Node.js and nodemailer. Claude can invoke this server to send emails on demand.

## Features

✅ **Send Individual Emails** - Send single emails with HTML/text content
✅ **Bulk Email Sending** - Send multiple emails in one batch operation
✅ **Email Templates** - Use HTML templates with variable substitution
✅ **Gmail Integration** - Direct SMTP integration with Gmail
✅ **CC/BCC Support** - Support for carbon copy and blind carbon copy recipients
✅ **Configuration Verification** - Check if email setup is working correctly
✅ **Template Management** - List and manage available email templates
✅ **Error Handling** - Comprehensive error handling and logging

## Prerequisites

- Node.js 16+ (from https://nodejs.org/)
- Gmail account with 2-Factor Authentication enabled
- Gmail App Password (not your regular password)

## Installation

### 1. Clone/Setup the Server

```bash
cd email-mcp-server
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Gmail Credentials

#### Step 1: Enable 2-Factor Authentication

1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not already enabled)

#### Step 2: Generate App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Windows Computer" (or your device type)
4. Click "Generate"
5. Copy the 16-character password shown

#### Step 3: Configure .env File

```bash
# Copy example to actual .env
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Set the following:

```env
EMAIL_SERVICE=gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-char-app-password
EMAIL_FROM_NAME=AI Employee
EMAIL_FROM_EMAIL=your-email@gmail.com
```

**⚠️ IMPORTANT:** Replace spaces in the app password if any. Remove the `xxxx xxxx xxxx xxxx` format.

### 4. Test Configuration

```bash
# Verify email setup works
npm start
```

Then in Claude, run: `verify_email_config`

Expected output:
```json
{
  "verified": true,
  "message": "Email configuration is valid",
  "config": {
    "service": "gmail",
    "from_email": "your-email@gmail.com",
    "from_name": "AI Employee",
    "user": "your-email@gmail.com"
  }
}
```

## Usage

### Starting the Server

```bash
npm start
```

The server will:
- Load credentials from `.env`
- Initialize the email transporter
- Listen for MCP requests from Claude

### Available Tools

#### 1. `send_email` - Send a Single Email

Send an email to one recipient with HTML and/or text content.

**Parameters:**
- `to` (required) - Recipient email address
- `subject` (required) - Email subject
- `html` - HTML content (optional)
- `text` - Plain text fallback (optional)
- `cc` - Array of CC recipients (optional)
- `bcc` - Array of BCC recipients (optional)

**Example (from Claude):**
```
send_email:
to: mustafa.qazi.sef@gmail.com
subject: Welcome to Our Service
html: <h1>Welcome!</h1><p>Thanks for joining us.</p>
text: Welcome! Thanks for joining us.
```

**Response:**
```json
{
  "success": true,
  "messageId": "<abc123@gmail.com>",
  "response": "250 2.0.0 OK",
  "timestamp": "2026-02-20T16:00:00.000Z",
  "to": "customer@example.com",
  "subject": "Welcome to Our Service"
}
```

---

#### 2. `send_bulk_emails` - Send to Multiple Recipients

Send emails to multiple recipients at once.

**Parameters:**
- `recipients` (required) - Array of email objects with:
  - `to` - Recipient email
  - `subject` - Email subject
  - `html` - HTML content
  - `text` - Text fallback
  - `cc` - CC recipients (optional)
  - `bcc` - BCC recipients (optional)

**Example:**
```
send_bulk_emails:
recipients:
  - to: user1@example.com
    subject: Hello User 1
    html: <p>Welcome user 1!</p>
  - to: user2@example.com
    subject: Hello User 2
    html: <p>Welcome user 2!</p>
```

**Response:**
```json
{
  "total": 2,
  "successful": 2,
  "failed": 0,
  "errors": [],
  "timestamp": "2026-02-20T16:00:00.000Z"
}
```

---

#### 3. `send_email_from_template` - Use Email Templates

Send an email using an HTML template with variable substitution.

**Parameters:**
- `to` (required) - Recipient email
- `subject` (required) - Email subject
- `template` (required) - Template name (without .html)
- `data` - Object with variables to replace

**Available Templates:**
- `welcome` - Welcome email template
- `notification` - Notification template

**Example (using welcome template):**
```
send_email_from_template:
to: user@example.com
subject: Welcome to AI Employee
template: welcome
data:
  name: John Doe
  company: AI Corporation
  message: We're excited to have you on board!
  cta_url: https://example.com/onboarding
  cta_text: Start Your Journey
  support_email: support@example.com
  sender_name: AI Employee Team
```

**Template Variables (welcome.html):**
- `{{name}}` - User's name
- `{{company}}` - Company name
- `{{message}}` - Custom message
- `{{cta_url}}` - Call-to-action URL
- `{{cta_text}}` - CTA button text
- `{{support_email}}` - Support email
- `{{sender_name}}` - Sender name

---

#### 4. `verify_email_config` - Check Configuration

Verify that email configuration is correct and working.

**Example:**
```
verify_email_config:
```

**Response (Success):**
```json
{
  "verified": true,
  "message": "Email configuration is valid",
  "config": {
    "service": "gmail",
    "from_email": "your-email@gmail.com",
    "from_name": "AI Employee",
    "user": "your-email@gmail.com"
  }
}
```

**Response (Failure):**
```json
{
  "verified": false,
  "error": "Invalid login. Check your credentials.",
  "config": {
    "service": "gmail",
    "user": "your-email@gmail.com"
  }
}
```

---

#### 5. `list_templates` - List Available Templates

List all available email templates.

**Example:**
```
list_templates:
```

**Response:**
```json
{
  "available": true,
  "count": 2,
  "templates": [
    "welcome",
    "notification"
  ],
  "templatesDir": "/path/to/email-mcp-server/templates"
}
```

---

## Creating Custom Templates

### Add a New Template

1. Create an HTML file in `templates/` directory
2. Name it something descriptive (e.g., `templates/reset-password.html`)
3. Use `{{variable_name}}` format for variables
4. Reference it in `send_email_from_template` tool

### Example Custom Template

Create `templates/reset-password.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 20px auto; }
        .button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Reset Request</h1>
        <p>Hi {{name}},</p>
        <p>We received a request to reset your password.</p>
        <p>Click the button below to reset it:</p>
        <p>
            <a href="{{reset_url}}" class="button">Reset Password</a>
        </p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>Best regards,<br>{{company}} Security Team</p>
    </div>
</body>
</html>
```

Use it with:

```
send_email_from_template:
to: user@example.com
subject: Reset Your Password
template: reset-password
data:
  name: John Doe
  reset_url: https://example.com/reset/abc123
  company: My Company
```

---

## Troubleshooting

### "Invalid login" Error

**Problem:** Email not sending, "Invalid login" message

**Solution:**
1. Verify you're using an **App Password**, not your regular Gmail password
2. Generate a new app password at https://myaccount.google.com/apppasswords
3. Check that 2-Factor Authentication is enabled
4. Remove any spaces from the app password in `.env`

### "Transporter not initialized" Error

**Problem:** Email transporter initialization failed

**Solution:**
1. Check `.env` file exists and has correct values
2. Verify `EMAIL_USER` and `EMAIL_PASS` are set
3. Ensure values don't have extra spaces or quotes
4. Run `verify_email_config` to test connection

### Emails not sending to Gmail recipients

**Problem:** Emails send to other providers but fail for Gmail

**Solution:**
1. Check Gmail spam folder (it might be filtered)
2. Mark sender as trusted in Gmail
3. Verify your Gmail account isn't blocking SMTP access
4. Check Account Security at https://myaccount.google.com/security

### Connection timeout error

**Problem:** "Connection timeout" or "Cannot reach mail server"

**Solution:**
1. Check internet connection
2. Verify firewall isn't blocking port 587
3. Check if your ISP blocks SMTP (some do)
4. Try using a different network if available

---

## Example Workflows

### Workflow 1: Welcome New Customer

```
1. User signs up
2. Claude calls: send_email_from_template
   - template: "welcome"
   - to: new_customer@example.com
   - data: name, company, CTA
3. Email sent to customer
4. Customer receives welcome message
```

### Workflow 2: Bulk Notification Campaign

```
1. Event occurs (feature launch, announcement, etc.)
2. Claude calls: send_bulk_emails
   - recipients: [list of 100 customers]
   - Each with: to, subject, html
3. All 100 emails sent in one batch
4. Report shows: 100 sent, 0 failed
```

### Workflow 3: Verification & Error Handling

```
1. Before sending important emails:
2. Claude calls: verify_email_config
3. If verified=true, proceed with sending
4. If verified=false, report error to user
5. User fixes configuration
6. Retry email sending
```

---

## Security Best Practices

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Never commit .env** - Add `.env` to `.gitignore`
2. **Use App Passwords** - Never use your actual Gmail password
3. **Rotate Credentials** - Change app passwords periodically
4. **Limit Permissions** - Create app passwords just for Mail, not full account
5. **Secure Configuration** - Keep .env file permissions restricted (600)
6. **Monitor Activity** - Check Gmail's "Connected Apps" for suspicious access

### .gitignore

Make sure your `.gitignore` includes:

```
.env
.env.local
node_modules/
*.log
.DS_Store
```

---

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_SERVICE` | No | gmail | Email service provider |
| `EMAIL_HOST` | No | smtp.gmail.com | SMTP server hostname |
| `EMAIL_PORT` | No | 587 | SMTP port |
| `EMAIL_SECURE` | No | false | Use TLS security |
| `EMAIL_USER` | **Yes** | - | Email account username |
| `EMAIL_PASS` | **Yes** | - | Email account password |
| `EMAIL_FROM_NAME` | No | AI Employee | Display name for emails |
| `EMAIL_FROM_EMAIL` | No | EMAIL_USER | From email address |

### Using Custom SMTP

For non-Gmail SMTP servers:

```env
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=username
EMAIL_PASS=password
EMAIL_FROM_NAME=My Company
EMAIL_FROM_EMAIL=noreply@example.com
```

---

## File Structure

```
email-mcp-server/
├── index.js                 # Main MCP server code
├── package.json             # Node dependencies
├── .env                     # Configuration (add to .gitignore!)
├── .env.example            # Configuration template
├── README.md               # This file
├── .gitignore              # Git ignore patterns
└── templates/
    ├── welcome.html        # Welcome email template
    ├── notification.html   # Notification template
    └── [your-custom-templates]
```

---

## Running Tests

### Test Email Sending

```bash
# Start server
npm start

# In another terminal, verify configuration
# Use Claude to call: verify_email_config

# Send test email
# Use Claude to call: send_email with your email
```

### Check Template Rendering

```
list_templates:

# Should show:
# available: true
# templates: ["welcome", "notification"]
```

---

## Support & Troubleshooting

### Common Issues

**Issue:** "ENOTFOUND smtp.gmail.com"
- **Fix:** Check internet connection

**Issue:** "Invalid login"
- **Fix:** Use App Password, not Gmail password

**Issue:** "Mail server is not available"
- **Fix:** Check firewall, ISP SMTP blocking

**Issue:** Emails go to spam
- **Fix:** Add from email to contacts, verify SPF/DKIM

---

## MCP Integration

This server integrates with Claude via the Model Context Protocol (MCP).

### Starting with Claude

To use with Claude Code:

1. Ensure `.env` is configured
2. Run `npm start`
3. Claude can now invoke email tools
4. Use natural language requests like:
   - "Send a welcome email to john@example.com"
   - "Send a notification to our team"
   - "Verify email configuration"

---

## License

MIT

## Author

AI Employee - Email MCP Server

---

**Last Updated:** 2026-02-20
**Version:** 1.0.0
**Status:** Production Ready ✅

For issues or questions, check the troubleshooting section or review your `.env` configuration.
