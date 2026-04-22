#!/usr/bin/env python3
"""
get_bars.py — Return historical OHLCV bars for a ticker.

Usage:
    python tools/get_bars.py <TICKER> [days]

Examples:
    python tools/get_bars.py SPY
    python tools/get_bars.py AAPL 30
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_data_client
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed
import pytz


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/get_bars.py <TICKER> [days]", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    client = get_data_client()
    end = datetime.now(pytz.UTC)
    start = end - timedelta(days=days)

    request = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed=DataFeed.IEX,
    )
    bars = client.get_stock_bars(request)

    result = []
    for bar in bars[ticker]:
        result.append({
            "timestamp": bar.timestamp.isoformat(),
            "open": float(bar.open),
            "high": float(bar.high),
            "low": float(bar.low),
            "close": float(bar.close),
            "volume": int(bar.volume),
            "vwap": float(bar.vwap) if bar.vwap else None,
        })

    print(json.dumps({"ticker": ticker, "bars": result}, indent=2))
    return result


if __name__ == "__main__":
    main()
