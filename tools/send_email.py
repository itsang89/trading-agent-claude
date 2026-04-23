#!/usr/bin/env python3
"""
Send email via SendGrid HTTP API (port 443 / HTTPS).
SMTP ports 25/465/587 are firewalled in the CCR sandbox; only HTTPS works.

Required env var:
  SENDGRID_API_KEY  — SendGrid API key (free tier: 100 emails/day)
  SENDGRID_FROM     — verified sender address on your SendGrid account

Optional env var:
  EMAIL_TO          — override default recipient (default: tsangyatlongit@gmail.com)

Usage:
  python3 tools/send_email.py --subject "Subject" --body "Body text"
  python3 tools/send_email.py --subject "Subject" --body-file /tmp/email.txt
  echo "Body" | python3 tools/send_email.py --subject "Subject"
"""
import argparse
import json
import os
import sys

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"
DEFAULT_TO = "tsangyatlongit@gmail.com"


def send_via_sendgrid(api_key, from_addr, to_addr, subject, body):
    """POST to SendGrid v3 mail/send over HTTPS. Returns (ok: bool, detail: str)."""
    payload = {
        "personalizations": [{"to": [{"email": to_addr}]}],
        "from": {"email": from_addr},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            SENDGRID_API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=30,
        )
        if resp.status_code in (200, 202):
            return True, f"HTTP {resp.status_code}"
        return False, f"HTTP {resp.status_code}: {resp.text[:300]}"
    except requests.RequestException as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Send email via SendGrid HTTPS API")
    parser.add_argument("--to", default=os.environ.get("EMAIL_TO", DEFAULT_TO))
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

    api_key = os.environ.get("SENDGRID_API_KEY")
    from_addr = os.environ.get("SENDGRID_FROM")

    if not api_key:
        print("ERROR: SENDGRID_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    if not from_addr:
        print("ERROR: SENDGRID_FROM not set in environment", file=sys.stderr)
        sys.exit(1)

    ok, detail = send_via_sendgrid(api_key, from_addr, args.to, args.subject, body)
    if ok:
        print(f"Email sent: {args.subject} ({detail})")
    else:
        print(f"ERROR sending email: {detail}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
