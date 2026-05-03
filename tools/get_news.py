#!/usr/bin/env python3
"""
get_news.py — Return recent news headlines for one or more tickers via Alpaca News API.

Usage:
    python tools/get_news.py <TICKER> [count]
    python tools/get_news.py AAPL,MSFT 10

Returns last N headlines (default 5, max 50) from the past 7 days.
News is context for timing decisions only — it does not override price signals.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

_repo_root = Path(__file__).resolve().parents[1]
load_dotenv(_repo_root / ".env")

_API_KEY = os.environ.get("ALPACA_API_KEY")
_API_SECRET = os.environ.get("ALPACA_API_SECRET")

NEWS_URL = "https://data.alpaca.markets/v1beta1/news"


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/get_news.py <TICKER[,TICKER2,...]> [count]", file=sys.stderr)
        sys.exit(1)

    if not _API_KEY or not _API_SECRET:
        print(json.dumps({"error": "ALPACA_API_KEY and ALPACA_API_SECRET must be set in .env"}))
        sys.exit(1)

    symbols = sys.argv[1].upper()
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    headers = {
        "APCA-API-KEY-ID": _API_KEY,
        "APCA-API-SECRET-KEY": _API_SECRET,
    }

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)

    params = {
        "symbols": symbols,
        "limit": min(count, 50),
        "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "include_content": "false",
        "exclude_contentless": "true",
        "sort": "desc",
    }

    try:
        resp = requests.get(NEWS_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(json.dumps({"symbols": symbols, "error": str(e)}))
        sys.exit(1)

    articles = []
    for item in data.get("news", []):
        articles.append({
            "headline": item.get("headline"),
            "summary": item.get("summary", ""),
            "source": item.get("source"),
            "published_at": item.get("created_at"),
            "symbols": item.get("symbols", []),
        })

    print(json.dumps({"symbols": symbols, "count": len(articles), "articles": articles}, indent=2))


if __name__ == "__main__":
    main()
