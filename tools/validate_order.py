#!/usr/bin/env python3
"""
validate_order.py — CLI wrapper for the guardrail validator.
Does NOT place any order. Use to check if an order would be allowed.

Usage:
    python tools/validate_order.py <TICKER> <side> <qty> [order_type]

Examples:
    python tools/validate_order.py SPY buy 10
    python tools/validate_order.py SPY buy 10 limit
    python tools/validate_order.py SPY sell 5 market
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.validator import validate
from tools.lib.alpaca_client import get_data_client
from tools.get_positions import get_data as get_positions_data
from tools.get_account import get_data as get_account_data
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.enums import DataFeed


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python tools/validate_order.py <TICKER> <side> <qty> [order_type]",
            file=sys.stderr,
        )
        sys.exit(1)

    ticker = sys.argv[1].upper()
    side = sys.argv[2].lower()
    qty = float(sys.argv[3])
    order_type = sys.argv[4].lower() if len(sys.argv) > 4 else "market"

    # Fetch live account and positions for full validation
    try:
        account = get_account_data()
        positions = get_positions_data()
    except Exception as e:
        # If we can't fetch account data, do partial validation (no size/cash checks)
        print(
            json.dumps({"warning": f"Could not fetch account data: {e}. Running partial validation."}),
            file=sys.stderr,
        )
        account = None
        positions = None

    # Fetch a live quote for price estimate (needed for new tickers not in positions)
    estimated_price = None
    if side == "buy" and account is not None:
        try:
            data_client = get_data_client()
            quote_req = StockLatestQuoteRequest(symbol_or_symbols=ticker, feed=DataFeed.IEX)
            quotes = data_client.get_stock_latest_quote(quote_req)
            q = quotes[ticker]
            estimated_price = float(q.ask_price) if q.ask_price else float(q.bid_price) if q.bid_price else None
        except Exception:
            pass  # Validator will handle missing price

    result = validate(
        ticker=ticker,
        side=side,
        qty=qty,
        order_type=order_type,
        account=account,
        positions=positions,
        estimated_price=estimated_price,
    )
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
