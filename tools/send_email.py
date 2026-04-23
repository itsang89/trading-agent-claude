#!/usr/bin/env python3
"""
Send email via Gmail SMTP.
Requires GMAIL_USER and GMAIL_APP_PASSWORD in environment (or .env).

Usage:
  python3 tools/send_email.py --subject "Subject" --body "Body text"
  python3 tools/send_email.py --subject "Subject" --body-file /tmp/email.txt
  echo "Body" | python3 tools/send_email.py --subject "Subject"
"""
import argparse
import os
import smtplib
import sys
from email.mime.text import MIMEText

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description="Send email via Gmail SMTP")
    parser.add_argument("--to", default="motivationmaven89@gmail.com")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", help="Email body text")
    parser.add_argument("--body-file", help="Path to file containing email body")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    elif args.body:
        body = args.body
    else:
        body = sys.stdin.read()

    user = os.environ.get("GMAIL_USER")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not user or not password:
        print("ERROR: GMAIL_USER or GMAIL_APP_PASSWORD not set in environment", file=sys.stderr)
        sys.exit(1)

    msg = MIMEText(body, "plain")
    msg["Subject"] = args.subject
    msg["From"] = user
    msg["To"] = args.to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, password)
            server.send_message(msg)
        print(f"Email sent: {args.subject}")
    except Exception as e:
        print(f"ERROR sending email: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
