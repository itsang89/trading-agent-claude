#!/usr/bin/env python3
"""
get_earnings.py — Return next earnings date for a ticker.

Usage:
    python tools/get_earnings.py <TICKER>

Flags in output:
    EARNINGS_IMMINENT  — earnings within 2 calendar days (cap position, do not add)
    EARNINGS_THIS_WEEK — earnings within 7 calendar days (prefer lower end of conviction tier)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/get_earnings.py <TICKER>", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()

    try:
        import yfinance as yf
    except ImportError:
        print(json.dumps({"ticker": ticker, "error": "yfinance not installed — run pip install yfinance"}))
        return

    try:
        t = yf.Ticker(ticker)
        cal = t.calendar

        if cal is None or (hasattr(cal, '__len__') and len(cal) == 0):
            print(json.dumps({"ticker": ticker, "next_earnings_date": None, "days_until": None, "flag": None, "note": "no earnings data available"}))
            return

        earnings_dates = cal.get("Earnings Date", [])

        if not earnings_dates:
            print(json.dumps({"ticker": ticker, "next_earnings_date": None, "days_until": None, "flag": None, "note": "no upcoming earnings found"}))
            return

        today = datetime.now(timezone.utc).date()
        future_dates = []
        for d in earnings_dates:
            dt = d.date() if hasattr(d, "date") else d
            if dt >= today:
                future_dates.append(dt)

        if not future_dates:
            print(json.dumps({"ticker": ticker, "next_earnings_date": None, "days_until": None, "flag": None, "note": "no future earnings found"}))
            return

        next_date = min(future_dates)
        days_until = (next_date - today).days

        if days_until <= 2:
            flag = "EARNINGS_IMMINENT"
        elif days_until <= 7:
            flag = "EARNINGS_THIS_WEEK"
        else:
            flag = None

        print(json.dumps({
            "ticker": ticker,
            "next_earnings_date": next_date.isoformat(),
            "days_until": days_until,
            "flag": flag,
        }, indent=2))

    except Exception as e:
        print(json.dumps({"ticker": ticker, "error": str(e)}))


if __name__ == "__main__":
    main()
