#!/usr/bin/env python3
"""
Send email via Gmail SMTP.
Requires GMAIL_USER and GMAIL_APP_PASSWORD in environment (or .env).

Usage:
  python3 tools/send_email.py --subject "Subject" --body "Body text"
  python3 tools/send_email.py --subject "Subject" --body-file /tmp/email.txt
  echo "Body" | python3 tools/send_email.py --subject "Subject"

Network notes:
  - Tries STARTTLS on port 587 first, falls back to SSL on port 465.
  - Prefers IPv6 sockets to work in IPv6-only environments (e.g. CCR cloud).
  - Avoids smtplib private attributes (_GLOBAL_DEFAULT_TIMEOUT) that differ
    across Python versions by using isinstance() to detect real timeouts.
"""
import argparse
import os
import smtplib
import socket
import ssl
import sys
from email.mime.text import MIMEText

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class _RobustSMTP(smtplib.SMTP):
    """SMTP that connects IPv6-first, avoiding smtplib private-sentinel access."""

    def _get_socket(self, host, port, timeout):
        # smtplib passes its internal sentinel object as `timeout` when no
        # timeout was set.  That sentinel is a private attribute that does NOT
        # exist on the smtplib module in all Python builds, so we must NOT
        # compare against it by name.  Use isinstance instead: a real caller-
        # supplied timeout will be int or float; anything else (sentinel, None)
        # means "leave the socket in its default (blocking) mode".
        real_timeout = timeout if isinstance(timeout, (int, float)) else None

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
                    if real_timeout is not None:
                        sock.settimeout(real_timeout)
                    sock.connect(sa)
                    return sock
                except OSError as e:
                    err = e
                    if sock is not None:
                        try:
                            sock.close()
                        except Exception:
                            pass
        raise err if err is not None else OSError("No reachable SMTP address found")


class _RobustSMTP_SSL(smtplib.SMTP_SSL, _RobustSMTP):
    """SSL/TLS variant with the same IPv6-first socket logic (port 465)."""
    pass


def _send(user, password, msg):
    """Try port 587 STARTTLS, fall back to port 465 SSL. Returns error string or None."""
    # Attempt 1: STARTTLS on 587
    try:
        with _RobustSMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.send_message(msg)
        return None  # success
    except Exception as e587:
        pass

    # Attempt 2: SSL on 465
    try:
        ctx = ssl.create_default_context()
        with _RobustSMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
            server.login(user, password)
            server.send_message(msg)
        return None  # success
    except Exception as e465:
        return f"587 error: {e587!r} | 465 error: {e465!r}"


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

    error = _send(user, password, msg)
    if error:
        print(f"ERROR sending email: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Email sent: {args.subject}")


if __name__ == "__main__":
    main()
