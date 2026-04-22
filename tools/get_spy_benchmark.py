#!/usr/bin/env python3
"""
get_spy_benchmark.py — SPY price and cumulative return since experiment start.

Usage:
    python tools/get_spy_benchmark.py

Reads EXPERIMENT_START_DATE from .env.
Returns:
    current_price: latest SPY close
    start_price: SPY close on EXPERIMENT_START_DATE
    cumulative_return_pct: total return since start
    today_return_pct: today's return (vs prior close)
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_data_client
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed


def main():
    start_date_str = os.environ.get("EXPERIMENT_START_DATE")
    if not start_date_str:
        print(
            json.dumps({"error": "EXPERIMENT_START_DATE not set in .env"}),
            file=sys.stderr,
        )
        sys.exit(1)

    client = get_data_client()
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
    end_dt = datetime.now(pytz.UTC)

    # If experiment hasn't started yet, fetch recent data for current SPY price
    if start_dt >= end_dt:
        fetch_start = end_dt - timedelta(days=10)
        experiment_started = False
    else:
        fetch_start = start_dt - timedelta(days=5)
        experiment_started = True

    request = StockBarsRequest(
        symbol_or_symbols="SPY",
        timeframe=TimeFrame.Day,
        start=fetch_start,
        end=end_dt,
        feed=DataFeed.IEX,
    )
    bars = client.get_stock_bars(request)
    spy_bars = bars["SPY"]

    if not spy_bars:
        print(json.dumps({"error": "No SPY data returned"}), file=sys.stderr)
        sys.exit(1)

    latest_bar = spy_bars[-1]
    prev_bar = spy_bars[-2] if len(spy_bars) > 1 else spy_bars[-1]
    current_price = float(latest_bar.close)
    prev_close = float(prev_bar.close)
    today_return = (current_price - prev_close) / prev_close * 100

    if experiment_started:
        start_bar = next(
            (b for b in spy_bars if b.timestamp.date() >= start_dt.date()), spy_bars[0]
        )
        start_price = float(start_bar.close)
        cumulative_return = (current_price - start_price) / start_price * 100
    else:
        start_price = None
        cumulative_return = None

    result = {
        "ticker": "SPY",
        "current_price": current_price,
        "start_price": start_price,
        "start_date": start_date_str,
        "experiment_started": experiment_started,
        "latest_date": latest_bar.timestamp.date().isoformat(),
        "cumulative_return_pct": round(cumulative_return, 4) if cumulative_return is not None else None,
        "today_return_pct": round(today_return, 4),
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
