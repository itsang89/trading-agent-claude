#!/usr/bin/env python3
"""
append_metrics.py — Append a daily metrics row to metrics/daily-metrics.csv.
Called by 'make run-eod' AFTER the LLM end-of-day review routine.
NOT called by the LLM directly.

Usage:
    python tools/append_metrics.py

Reads:
    - Alpaca account (equity, cash)
    - Alpaca positions (count)
    - trades/trades.csv (orders placed and rejected today)
    - SPY bars (today's close and return)
    - metrics/daily-metrics.csv (to compute cumulative return)
    - EXPERIMENT_START_DATE from .env (for cumulative baseline)

Appends one row to metrics/daily-metrics.csv.
"""
import csv
import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import pytz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client, get_data_client
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

_REPO_ROOT = Path(__file__).resolve().parents[1]
_METRICS_CSV = _REPO_ROOT / "metrics" / "daily-metrics.csv"
_TRADES_CSV = _REPO_ROOT / "trades" / "trades.csv"
_ET = pytz.timezone("America/New_York")


def _count_today_trades():
    today = date.today().isoformat()
    placed = 0
    rejected = 0
    if not _TRADES_CSV.exists():
        return placed, rejected
    with open(_TRADES_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("date") == today:
                if row.get("status", "").lower() in ("rejected", "failed"):
                    rejected += 1
                else:
                    placed += 1
    return placed, rejected


def _get_start_equity():
    """Read the first equity value from metrics CSV as the baseline."""
    if not _METRICS_CSV.exists():
        return None
    with open(_METRICS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                return float(row["equity"])
            except (KeyError, ValueError):
                continue
    return None


def _get_start_spy():
    """Read the first SPY close from metrics CSV as the baseline."""
    if not _METRICS_CSV.exists():
        return None
    with open(_METRICS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                return float(row["spy_close"])
            except (KeyError, ValueError):
                continue
    return None


def main():
    trading_client = get_trading_client()
    data_client = get_data_client()

    # Account
    acct = trading_client.get_account()
    equity = float(acct.equity)
    cash = float(acct.cash)

    # Positions
    positions = trading_client.get_all_positions()
    positions_held = len(positions)

    # Orders today
    orders_placed, orders_rejected = _count_today_trades()

    # SPY data
    now_utc = datetime.now(pytz.UTC)
    spy_request = StockBarsRequest(
        symbol_or_symbols="SPY",
        timeframe=TimeFrame.Day,
        start=now_utc - timedelta(days=5),
        end=now_utc,
        feed=DataFeed.IEX,
    )
    spy_bars = data_client.get_stock_bars(spy_request)["SPY"]

    if len(spy_bars) < 2:
        print("ERROR: Not enough SPY bars to compute returns.", file=sys.stderr)
        sys.exit(1)

    spy_close = float(spy_bars[-1].close)
    spy_prev_close = float(spy_bars[-2].close)
    spy_day_return = (spy_close - spy_prev_close) / spy_prev_close * 100

    # Cumulative returns
    start_equity = _get_start_equity() or equity
    start_spy = _get_start_spy() or spy_close

    cum_return = (equity - start_equity) / start_equity * 100
    cum_spy_return = (spy_close - start_spy) / start_spy * 100

    # Previous equity for day P&L (read last row of metrics)
    prev_equity = start_equity
    if _METRICS_CSV.exists():
        with open(_METRICS_CSV) as f:
            rows = list(csv.DictReader(f))
            if rows:
                try:
                    prev_equity = float(rows[-1]["equity"])
                except (KeyError, ValueError):
                    prev_equity = equity

    day_pnl_abs = equity - prev_equity
    day_pnl_pct = day_pnl_abs / prev_equity * 100 if prev_equity else 0

    today_str = date.today().isoformat()
    row = {
        "date": today_str,
        "equity": round(equity, 2),
        "cash": round(cash, 2),
        "day_pnl_abs": round(day_pnl_abs, 2),
        "day_pnl_pct": round(day_pnl_pct, 4),
        "spy_close": round(spy_close, 2),
        "spy_day_return": round(spy_day_return, 4),
        "cum_return": round(cum_return, 4),
        "cum_spy_return": round(cum_spy_return, 4),
        "positions_held": positions_held,
        "orders_placed": orders_placed,
        "orders_rejected": orders_rejected,
    }

    fieldnames = list(row.keys())
    file_exists = _METRICS_CSV.exists() and _METRICS_CSV.stat().st_size > 1
    with open(_METRICS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(json.dumps(row, indent=2))
    return row


if __name__ == "__main__":
    main()
