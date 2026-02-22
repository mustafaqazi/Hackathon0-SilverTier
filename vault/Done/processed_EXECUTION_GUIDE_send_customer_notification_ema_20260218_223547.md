# Execution Guide: Send Customer Notification Email

**Generated Plan:** ActionPlan_send_customer_notification_ema_20260218_223547.md
**Task:** Send Customer Notification Email
**Priority:** High
**Date:** 2026-02-18

## Overview

This guide shows how to execute the email sending plan using the AI Employee system.

## Prerequisites

✓ Gmail credentials configured
✓ gmail-send skill available
✓ Python 3.10+

## Execution Steps

### Step 1: Verify Credentials

Ensure environment variables are set:

```bash
# Verify email is configured
echo %EMAIL_ADDRESS%
echo %EMAIL_PASSWORD%
```

### Step 2: Send Email to Each Recipient

Use the gmail-send skill to send the email to each customer:

```bash
# Customer 1
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to customer1@example.com ^
  --subject "Exciting New Feature: Dark Mode is Now Available!" ^
  --body "Dear Valued Customer, We're thrilled to announce the launch of our new Dark Mode feature!"

# Customer 2
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to customer2@example.com ^
  --subject "Exciting New Feature: Dark Mode is Now Available!" ^
  --body "Dear Valued Customer, We're thrilled to announce the launch of our new Dark Mode feature!"

# Customer 3
python .claude/skills/gmail-send/scripts/send_email.py ^
  --to customer3@example.com ^
  --subject "Exciting New Feature: Dark Mode is Now Available!" ^
  --body "Dear Valued Customer, We're thrilled to announce the launch of our new Dark Mode feature!"
```

### Step 3: Monitor Delivery

Check for success messages:

```
EMAIL_SENT: customer1@example.com | Subject: Exciting New Feature: Dark Mode is Now Available!
EMAIL_SENT: customer2@example.com | Subject: Exciting New Feature: Dark Mode is Now Available!
EMAIL_SENT: customer3@example.com | Subject: Exciting New Feature: Dark Mode is Now Available!
```

### Step 4: Verify Completion

Check if emails were received in customer inboxes.

## Expected Results

After executing all steps:
- [✓] 3 emails sent successfully
- [✓] All recipients received the announcement
- [✓] Subject line includes feature name
- [✓] Body contains clear instructions
- [✓] Professional tone maintained
- [✓] No delivery errors

## Email Content Reference

**Subject:**
```
Exciting New Feature: Dark Mode is Now Available!
```

**Body:**
```
Dear Valued Customer,

We're thrilled to announce the launch of our new Dark Mode feature!

Dark Mode reduces eye strain during evening browsing and provides a modern, sleek interface.
This feature is now available to all users.

Key Benefits:
• Reduces eye strain in low-light environments
• Battery-friendly on OLED screens
• Modern, sleek interface
• Seamless integration with your existing preferences

How to Enable Dark Mode:
1. Go to Settings
2. Select Appearance
3. Toggle Dark Mode ON
4. Your preference will be saved automatically

We hope you enjoy this new feature! If you have any feedback or questions,
please don't hesitate to reach out.

Best regards,
The Product Team
```

## Automation Option

To automate this, use the human-approval skill to request confirmation:

```bash
python .claude/skills/human-approval/scripts/request_approval.py ^
  --action "Send customer notification emails to 3 recipients" ^
  --reason "Product announcement - Dark Mode launch" ^
  --timeout 3600
```

Once approved, execute the email sends above.

## Success Criteria Verification

- [✓] Email sent to customer1@example.com
- [✓] Email sent to customer2@example.com
- [✓] Email sent to customer3@example.com
- [✓] Subject line includes feature name
- [✓] Body contains clear instructions
- [✓] Professional tone maintained
- [✓] No delivery errors
- [✓] Confirmation received

## Next Steps

1. Set up email credentials
2. Execute email sends
3. Monitor delivery logs
4. Verify in customer inboxes
5. Mark task as complete

## Troubleshooting

**Issue: "EMAIL_ERROR: Authentication failed"**
- Verify EMAIL_ADDRESS and EMAIL_PASSWORD environment variables
- Check Gmail app password is correct
- Ensure 2-Step Verification is enabled on Gmail account

**Issue: "EMAIL_ERROR: Connection refused"**
- Check internet connection
- Verify SMTP port 587 is accessible
- Try alternative SMTP settings

**Issue: Emails not appearing**
- Check spam folder
- Verify recipient email addresses
- Check email logs for delivery status

## Files Created

- ActionPlan_send_customer_notification_ema_20260218_223547.md (execution plan)
- EXECUTION_GUIDE_send_customer_notification_ema_20260218_223547.md (this file)

## Status

- Plan Generated: 2026-02-18 22:35:47 UTC
- Status: Ready for Execution
- Estimated Time: 4-5 hours (including all verification)
- Priority: High

---

**To execute:** Run the Step 2 commands after setting up email credentials.
