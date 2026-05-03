#!/usr/bin/env python3
"""
place_order.py — Place an order through the validator, then Alpaca.
All orders pass through the guardrail validator before reaching Alpaca.

Usage:
    python tools/place_order.py <TICKER> <side> <qty> <order_type> [limit_price] [--stop-pct PCT]

Examples:
    python tools/place_order.py GOOGL buy 2 market
    python tools/place_order.py GOOGL buy 2 market --stop-pct 0.08
    python tools/place_order.py GOOGL buy 2 limit 380.00 --stop-pct 0.08
    python tools/place_order.py GOOGL sell 2 market

For BUY orders with --stop-pct: immediately places a matching GTC stop-sell order
at price_basis * (1 - stop_pct). Returns stop_order_id and stop_price in result.
If stop placement fails, result includes stop_order_warning (non-blocking).

Returns JSON with order details or structured rejection.
Appends successful orders to trades/trades.csv.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import pytz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.validator import validate
from tools.lib.alpaca_client import get_trading_client, get_data_client
from tools.get_positions import get_data as get_positions_data
from tools.get_account import get_data as get_account_data
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.enums import DataFeed

_REPO_ROOT = Path(__file__).resolve().parents[1]
_TRADES_CSV = _REPO_ROOT / "trades" / "trades.csv"
_ET = pytz.timezone("America/New_York")


def _append_trade(row: dict):
    """Append a trade row to trades/trades.csv."""
    fieldnames = ["date", "time", "ticker", "side", "qty", "price", "order_id", "status", "routine"]
    file_exists = _TRADES_CSV.exists() and _TRADES_CSV.stat().st_size > 1

    with open(_TRADES_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Place an order through the validator, then Alpaca.",
        add_help=False,
    )
    parser.add_argument("ticker", type=str)
    parser.add_argument("side", type=str, choices=["buy", "sell"])
    parser.add_argument("qty", type=float)
    parser.add_argument("order_type", type=str, choices=["market", "limit"])
    parser.add_argument("limit_price", nargs="?", type=float, default=None)
    parser.add_argument(
        "--stop-pct",
        type=float,
        default=None,
        metavar="PCT",
        help="BUY only: place a GTC stop-sell at fill_price*(1-PCT) after the buy fills (e.g. 0.08 for 8%%)",
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        print(
            "Usage: python tools/place_order.py <TICKER> <side> <qty> <order_type> [limit_price] [--stop-pct PCT]",
            file=sys.stderr,
        )
        sys.exit(1)

    ticker = args.ticker.upper()
    side = args.side.lower()
    qty = args.qty
    order_type = args.order_type.lower()
    limit_price = args.limit_price
    stop_pct = args.stop_pct

    if order_type == "limit" and limit_price is None:
        result = {
            "passed": False,
            "rule": "MISSING_LIMIT_PRICE",
            "current": None,
            "limit": None,
            "detail": "Limit orders require a limit_price argument.",
        }
        print(json.dumps(result, indent=2))
        return result

    # Fetch live account and positions
    try:
        account = get_account_data()
        positions = get_positions_data()
    except Exception as e:
        result = {"error": f"Failed to fetch account/position data: {e}. Order not placed."}
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)

    # Price basis: limit price if known, otherwise fetch live quote
    if limit_price:
        estimated_price = limit_price
    else:
        try:
            data_client = get_data_client()
            quote_req = StockLatestQuoteRequest(symbol_or_symbols=ticker, feed=DataFeed.IEX)
            quotes = data_client.get_stock_latest_quote(quote_req)
            q = quotes[ticker]
            estimated_price = float(q.ask_price) if q.ask_price else float(q.bid_price) if q.bid_price else None
        except Exception:
            estimated_price = None

    # Run validator
    validation = validate(
        ticker=ticker,
        side=side,
        qty=qty,
        order_type=order_type,
        account=account,
        positions=positions,
        estimated_price=estimated_price,
    )

    if not validation["passed"]:
        print(json.dumps(validation, indent=2))
        return validation

    # Place primary order via Alpaca
    client = get_trading_client()
    alpaca_side = OrderSide.BUY if side == "buy" else OrderSide.SELL

    try:
        if order_type == "market":
            request = MarketOrderRequest(
                symbol=ticker,
                qty=qty,
                side=alpaca_side,
                time_in_force=TimeInForce.DAY,
            )
        else:
            request = LimitOrderRequest(
                symbol=ticker,
                qty=qty,
                side=alpaca_side,
                time_in_force=TimeInForce.DAY,
                limit_price=limit_price,
            )

        order = client.submit_order(request)

        now_et = datetime.now(_ET)
        result = {
            "passed": True,
            "order_id": str(order.id),
            "ticker": ticker,
            "side": side,
            "qty": qty,
            "order_type": order_type,
            "limit_price": limit_price,
            "status": str(order.status),
            "submitted_at": order.submitted_at.isoformat() if order.submitted_at else None,
        }

        # Log to trades.csv
        _append_trade({
            "date": now_et.strftime("%Y-%m-%d"),
            "time": now_et.strftime("%H:%M:%S"),
            "ticker": ticker,
            "side": side,
            "qty": qty,
            "price": limit_price or "",
            "order_id": str(order.id),
            "status": str(order.status),
            "routine": os.environ.get("CURRENT_ROUTINE", ""),
        })

        # Place paired GTC stop-sell if requested (BUY orders only)
        if stop_pct is not None and side == "buy":
            if estimated_price is None:
                result["stop_order_warning"] = "stop order not placed — could not determine price basis (no quote)"
            else:
                stop_price = round(estimated_price * (1 - stop_pct), 2)
                try:
                    stop_request = StopOrderRequest(
                        symbol=ticker,
                        qty=qty,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.GTC,
                        stop_price=stop_price,
                    )
                    stop_order = client.submit_order(stop_request)
                    result["stop_order_id"] = str(stop_order.id)
                    result["stop_price"] = stop_price
                except Exception as e:
                    result["stop_order_warning"] = f"stop order placement failed: {e}"

        print(json.dumps(result, indent=2))
        return result

    except Exception as e:
        result = {"error": f"Alpaca order submission failed: {e}"}
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
