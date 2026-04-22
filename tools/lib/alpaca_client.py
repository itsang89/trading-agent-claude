"""
Shared Alpaca client initialization.
Reads credentials from .env in the repo root.
"""
import os
import warnings
from pathlib import Path

# Suppress urllib3 LibreSSL warning (macOS ships LibreSSL, not OpenSSL)
warnings.filterwarnings("ignore", message=".*urllib3.*OpenSSL.*")

from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

# Load .env from repo root (two levels up from tools/lib/)
_repo_root = Path(__file__).resolve().parents[2]
load_dotenv(_repo_root / ".env")

_API_KEY = os.environ.get("ALPACA_API_KEY")
_API_SECRET = os.environ.get("ALPACA_API_SECRET")
_BASE_URL = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

if not _API_KEY or not _API_SECRET:
    raise EnvironmentError(
        "ALPACA_API_KEY and ALPACA_API_SECRET must be set in .env. "
        "Copy .env.example to .env and fill in your credentials."
    )

_is_paper = "paper" in _BASE_URL


def get_trading_client() -> TradingClient:
    return TradingClient(
        api_key=_API_KEY,
        secret_key=_API_SECRET,
        paper=_is_paper,
    )


def get_data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(
        api_key=_API_KEY,
        secret_key=_API_SECRET,
    )
