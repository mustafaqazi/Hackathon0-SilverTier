# Email MCP Server - Quick Start Guide

Get your email server running in 5 minutes!

## 1️⃣ Install Dependencies

```bash
cd email-mcp-server
npm install
```

## 2️⃣ Get Gmail App Password

### Quick Steps:

1. Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification" (if not done)

2. Go to: https://myaccount.google.com/apppasswords
   - Select: "Mail" + "Windows Computer"
   - Click: "Generate"
   - Copy: 16-character password

### Example Password Format:
```
xxxx xxxx xxxx xxxx  (remove spaces → xxxxxxxxxxxxxxxx)
```

## 3️⃣ Configure .env

**Option A: Edit .env file directly**

```bash
# Open .env
nano .env

# Change these lines:
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-char-app-password-without-spaces
EMAIL_FROM_EMAIL=your-email@gmail.com
```

**Option B: Copy from example**

```bash
cp .env.example .env
nano .env
```

### Minimal .env Config:

```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=xxxxxxxxxxxx
EMAIL_FROM_EMAIL=your-email@gmail.com
```

## 4️⃣ Test It Works

```bash
npm start
```

You should see:
```
✓ Email transporter initialized successfully
✓ Email MCP Server started successfully
ℹ Available tools: send_email, send_bulk_emails, ...
```

## 5️⃣ Send Your First Email (via Claude)

Ask Claude to:

```
"Send a test email to my-email@gmail.com with subject 'Test Email' and message 'Hello World'"
```

Or manually call:

```
send_email:
to: my-email@gmail.com
subject: Test Email
html: <h1>Hello World</h1>
text: Hello World
```

---

## ✅ Troubleshooting

### "EMAIL_USER or EMAIL_PASS not set"

```bash
# Check .env exists
ls -la .env

# View contents (hide password)
cat .env | grep EMAIL_

# Make sure no .env.example is being used instead
```

### "Invalid login"

```bash
# Use App Password, NOT your Gmail password
# Generate new one at: https://myaccount.google.com/apppasswords

# Remove spaces from password:
# WRONG: xxxx xxxx xxxx xxxx
# RIGHT: xxxxxxxxxxxxxxxx
```

### "Cannot find module @modelcontextprotocol/sdk"

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### "ENOTFOUND smtp.gmail.com"

- Check internet connection
- Check firewall isn't blocking port 587
- Try disabling VPN if using one

---

## 🎯 Common Tasks

### Send Simple Email

```
send_email:
to: user@example.com
subject: Hello
html: <p>Hi there!</p>
```

### Send with CC/BCC

```
send_email:
to: user1@example.com
subject: Meeting Notes
html: <p>See attached notes</p>
cc:
  - user2@example.com
  - user3@example.com
```

### Use Email Template

```
send_email_from_template:
to: user@example.com
subject: Welcome!
template: welcome
data:
  name: John
  company: MyCompany
  cta_text: Get Started
  cta_url: https://example.com
```

### Send to Multiple People

```
send_bulk_emails:
recipients:
  - to: user1@example.com
    subject: Hello User 1
    html: <p>Hi user 1</p>
  - to: user2@example.com
    subject: Hello User 2
    html: <p>Hi user 2</p>
```

### Verify Setup

```
verify_email_config:
```

Should return `"verified": true`

---

## 📁 Project Structure

```
email-mcp-server/
├── index.js              ← Main server code
├── package.json          ← Dependencies
├── .env                  ← Your config (KEEP SECRET!)
├── .env.example          ← Template
├── README.md             ← Full documentation
├── QUICKSTART.md         ← This file
└── templates/
    ├── welcome.html      ← Email template
    └── notification.html ← Email template
```

---

## 🔐 Security Checklist

- [ ] `.env` file created (not `.env.example`)
- [ ] `EMAIL_USER` set to your Gmail
- [ ] `EMAIL_PASS` set to App Password (not regular password)
- [ ] `.gitignore` includes `.env` (so it doesn't get committed)
- [ ] No `.env` file in git history
- [ ] Server runs without errors

---

## 📚 Next Steps

- **Full Documentation:** Read `README.md`
- **Create Custom Templates:** Add HTML files to `templates/` folder
- **Integrate with Claude:** Use the tools in your Claude workflows
- **Monitor Emails:** Check Gmail to see sent emails

---

## 💡 Pro Tips

### Tip 1: Test Configuration First
```
Before sending important emails, always run:
verify_email_config
```

### Tip 2: Use Templates for Consistency
```
Instead of writing HTML in Claude each time,
create a template and reuse it with different data
```

### Tip 3: Batch Send Large Lists
```
Instead of sending individual emails,
use send_bulk_emails for faster processing
```

### Tip 4: Monitor Your App Passwords
```
Go to: https://myaccount.google.com/apppasswords
Delete old app passwords you don't use anymore
```

---

## 🆘 Need Help?

1. **Check Logs** - Look at server output for error messages
2. **Review .env** - Verify all required settings are set
3. **Test Connection** - Run `verify_email_config`
4. **Check Gmail** - Look at Account Security settings
5. **Read Full Docs** - See `README.md` for detailed info

---

## ✨ You're Ready!

Your email MCP server is now:
- ✅ Installed
- ✅ Configured
- ✅ Running
- ✅ Ready to use with Claude

Start sending emails! 🚀

---

**Questions?** See `README.md` for full documentation and troubleshooting.
