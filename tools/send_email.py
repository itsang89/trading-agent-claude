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
import socket
import sys
from email.mime.text import MIMEText


class _IPv6PreferredSMTP(smtplib.SMTP):
    """SMTP subclass that tries IPv6 before IPv4, for IPv6-only CCR environments."""
    def _get_socket(self, host, port, timeout):
        err = None
        for af in (socket.AF_INET6, socket.AF_INET, socket.AF_UNSPEC):
            try:
                addrs = socket.getaddrinfo(host, port, af, socket.SOCK_STREAM)
            except socket.gaierror:
                continue
            for res in addrs:
                af_, socktype, proto, _, sa = res
                sock = None
                try:
                    sock = socket.socket(af_, socktype, proto)
                    if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                        sock.settimeout(timeout)
                    sock.connect(sa)
                    return sock
                except OSError as e:
                    err = e
                    if sock is not None:
                        try:
                            sock.close()
                        except Exception:
                            pass
        raise err if err is not None else OSError("No SMTP addresses reachable")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description="Send email via Gmail SMTP")
    parser.add_argument("--to", default="tsangyatlongit@gmail.com")
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
        with _IPv6PreferredSMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        print(f"Email sent: {args.subject}")
    except Exception as e:
        print(f"ERROR sending email: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
