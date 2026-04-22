#!/usr/bin/env python3
"""
get_quote.py — Return the latest quote for a ticker.

Usage:
    python tools/get_quote.py <TICKER>

Example:
    python tools/get_quote.py SPY
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_data_client
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.enums import DataFeed


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/get_quote.py <TICKER>", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    client = get_data_client()

    request = StockLatestQuoteRequest(symbol_or_symbols=ticker, feed=DataFeed.IEX)
    quotes = client.get_stock_latest_quote(request)
    q = quotes[ticker]

    result = {
        "ticker": ticker,
        "ask_price": float(q.ask_price) if q.ask_price else None,
        "ask_size": int(q.ask_size) if q.ask_size else None,
        "bid_price": float(q.bid_price) if q.bid_price else None,
        "bid_size": int(q.bid_size) if q.bid_size else None,
        "timestamp": q.timestamp.isoformat(),
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
