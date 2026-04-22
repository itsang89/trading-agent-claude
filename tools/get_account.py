#!/usr/bin/env python3
"""
get_account.py — Return cash, equity, and buying power from the Alpaca account.

Usage:
    python tools/get_account.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.lib.alpaca_client import get_trading_client


def get_data() -> dict:
    client = get_trading_client()
    acct = client.get_account()
    return {
        "equity": float(acct.equity),
        "cash": float(acct.cash),
        "buying_power": float(acct.buying_power),
        "portfolio_value": float(acct.portfolio_value),
        "currency": acct.currency,
        "account_number": acct.account_number,
        "status": str(acct.status),
    }


def main():
    result = get_data()
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
