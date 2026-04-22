#!/usr/bin/env python3
"""
cancel_order.py — Cancel an open order by ID.

Usage:
    python tools/cancel_order.py <order_id>

Example:
    python tools/cancel_order.py abc123-def456
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/cancel_order.py <order_id>", file=sys.stderr)
        sys.exit(1)

    order_id = sys.argv[1]
    client = get_trading_client()

    try:
        client.cancel_order_by_id(order_id)
        result = {"cancelled": True, "order_id": order_id}
    except Exception as e:
        result = {"cancelled": False, "order_id": order_id, "error": str(e)}

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
