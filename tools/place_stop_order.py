#!/usr/bin/env python3
"""
place_stop_order.py — Place or replace a GTC stop-sell order for an existing position.
Use this to set/update the standing Alpaca stop after entering or adding to a position.

Usage:
    python tools/place_stop_order.py <TICKER> <qty> <stop_price>

Example:
    python tools/place_stop_order.py GOOGL 3.41 337.62

Returns JSON with stop order details or error.
Failure is non-blocking — caller should log the warning and continue.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client
from alpaca.trading.requests import StopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


def main():
    if len(sys.argv) < 4:
        print("Usage: python tools/place_stop_order.py <TICKER> <qty> <stop_price>", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    qty = float(sys.argv[2])
    stop_price = float(sys.argv[3])

    client = get_trading_client()

    try:
        request = StopOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC,
            stop_price=stop_price,
        )
        order = client.submit_order(request)
        result = {
            "placed": True,
            "stop_order_id": str(order.id),
            "ticker": ticker,
            "qty": qty,
            "stop_price": stop_price,
            "status": str(order.status),
        }
    except Exception as e:
        result = {
            "placed": False,
            "ticker": ticker,
            "qty": qty,
            "stop_price": stop_price,
            "error": str(e),
        }

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
