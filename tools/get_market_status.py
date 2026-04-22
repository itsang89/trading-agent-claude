#!/usr/bin/env python3
"""
get_market_status.py — Check if the US market is open, closed, or early-close today.

Usage:
    python tools/get_market_status.py

Returns JSON with:
    is_open: bool — market is currently open for trading
    is_trading_day: bool — today is a trading day (not weekend/holiday)
    early_close: bool — today has an early close
    close_time: str — scheduled close time in ET (e.g. "16:00" or "13:00")
    next_open: str — next scheduled open datetime (ISO)
    current_time_et: str — current time in ET
"""
import json
import sys
from datetime import datetime, date
from pathlib import Path

import pytz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client
from alpaca.trading.requests import GetCalendarRequest


def main():
    client = get_trading_client()
    clock = client.get_clock()

    today = date.today()
    calendar_req = GetCalendarRequest(start=str(today), end=str(today))
    calendar = client.get_calendar(calendar_req)

    et = pytz.timezone("America/New_York")
    now_et = datetime.now(et)

    if calendar:
        cal_entry = calendar[0]
        close_str = cal_entry.close.strftime("%H:%M") if hasattr(cal_entry.close, 'strftime') else str(cal_entry.close)
        open_str = cal_entry.open.strftime("%H:%M") if hasattr(cal_entry.open, 'strftime') else str(cal_entry.open)
        early_close = close_str not in ("16:00", "16:00:00")
        is_trading_day = True
    else:
        close_str = None
        open_str = None
        early_close = False
        is_trading_day = False

    result = {
        "is_open": clock.is_open,
        "is_trading_day": is_trading_day,
        "early_close": early_close,
        "open_time": open_str,
        "close_time": close_str,
        "next_open": clock.next_open.isoformat() if clock.next_open else None,
        "next_close": clock.next_close.isoformat() if clock.next_close else None,
        "current_time_et": now_et.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
