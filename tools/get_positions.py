#!/usr/bin/env python3
"""
get_positions.py — Return all current positions with avg entry, current price, and unrealized P&L.

Usage:
    python tools/get_positions.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client


def get_data() -> list:
    client = get_trading_client()
    positions = client.get_all_positions()
    result = []
    for p in positions:
        result.append({
            "ticker": p.symbol,
            "qty": float(p.qty),
            "avg_entry_price": float(p.avg_entry_price),
            "current_price": float(p.current_price),
            "market_value": float(p.market_value),
            "unrealized_pl": float(p.unrealized_pl),
            "unrealized_plpc": float(p.unrealized_plpc),
            "side": str(p.side),
        })
    return result


def main():
    result = get_data()
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
