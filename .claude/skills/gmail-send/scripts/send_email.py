#!/usr/bin/env python3
"""
send_email.py - Send emails via SMTP

Usage:
    python send_email.py --to recipient@example.com --subject "Subject" --body "Body text"

Environment Variables:
    EMAIL_ADDRESS - Sender email address
    EMAIL_PASSWORD - SMTP password or app password
    SMTP_HOST - SMTP server (default: smtp.gmail.com)
    SMTP_PORT - SMTP port (default: 587)
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parents[4] / ".env"
load_dotenv(env_path)


import argparse
import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to, subject, body, cc=None, smtp_host=None, smtp_port=None):
    """Send email via SMTP"""

    # Get credentials from environment
    sender = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')

    if not sender or not password:
        print("EMAIL_ERROR: EMAIL_ADDRESS and EMAIL_PASSWORD environment variables required")
        sys.exit(1)

    # Get SMTP config
    if smtp_host is None:
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    if smtp_port is None:
        smtp_port = int(os.getenv('SMTP_PORT', '587'))

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = cc
            recipients = [to] + [e.strip() for e in cc.split(',')]
        else:
            recipients = [to]

        # Attach body
        msg.attach(MIMEText(body, 'plain'))

        # Connect and send
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())

        # Success output
        print(f"EMAIL_SENT: {to} | Subject: {subject}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("EMAIL_ERROR: Authentication failed. Check EMAIL_ADDRESS and EMAIL_PASSWORD")
        sys.exit(1)
    except smtplib.SMTPException as e:
        print(f"EMAIL_ERROR: SMTP error - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"EMAIL_ERROR: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Send email via SMTP')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body')
    parser.add_argument('--cc', help='CC addresses (comma-separated)')
    parser.add_argument('--smtp-host', help='SMTP host')
    parser.add_argument('--smtp-port', type=int, help='SMTP port')

    args = parser.parse_args()

    send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        cc=args.cc,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port
    )


if __name__ == '__main__':
    main()
