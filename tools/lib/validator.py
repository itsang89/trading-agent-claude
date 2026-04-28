"""
Deterministic order validator — enforces hard risk limits.
Returns structured JSON. No LLM involvement.

Rules enforced:
  1. Universe whitelist
  2. Order type whitelist (market or limit only)
  3. No-trade windows (first/last 15 min of regular session: 9:30-9:45 and 3:45-4:00 ET)
  4. Sector concentration: max 40% of equity in one GICS sector
  5. Stop-loss enforcement is handled by the LLM each routine, not here

Removed as hard limits (operator-authorized 2026-04-28, now strategy-governed):
  - Max single position size (was 10%)
  - Max concurrent positions (was 8)
  - Minimum cash reserve (was 20%)
"""
import json
from datetime import datetime, time
from pathlib import Path
from typing import Optional
import pytz

_REPO_ROOT = Path(__file__).resolve().parents[2]
_UNIVERSE_PATH = _REPO_ROOT / "state" / "universe.json"

_ALLOWED_ORDER_TYPES = {"market", "limit"}
_ALLOWED_SIDES = {"buy", "sell"}
_ET = pytz.timezone("America/New_York")
_MARKET_OPEN = time(9, 30)
_NO_TRADE_WINDOW_OPEN_END = time(9, 45)   # no trades 9:30–9:45
_NO_TRADE_WINDOW_CLOSE_START = time(15, 45)  # no trades 15:45–16:00
_MARKET_CLOSE = time(16, 0)


def _load_universe() -> dict:
    if not _UNIVERSE_PATH.exists():
        return {"tickers": [], "sector_map": {}}
    with open(_UNIVERSE_PATH) as f:
        return json.load(f)


def _fail(rule: str, current, limit, detail: str = "") -> dict:
    return {
        "passed": False,
        "rule": rule,
        "current": current,
        "limit": limit,
        "detail": detail,
    }


def _pass() -> dict:
    return {"passed": True}


def validate(
    ticker: str,
    side: str,
    qty: float,
    order_type: str,
    account: Optional[dict] = None,
    positions: Optional[list] = None,
    check_time: Optional[datetime] = None,
    estimated_price: Optional[float] = None,
) -> dict:
    """
    Validate an order against all hard limits.

    Args:
        ticker: Stock symbol (uppercase)
        side: 'buy' or 'sell'
        qty: Number of shares (positive)
        order_type: 'market' or 'limit'
        account: Dict with keys 'equity' (float), 'cash' (float).
                 Required for size/cash/sector checks. If None, skips those checks.
        positions: List of dicts with keys 'ticker', 'qty', 'market_value', 'sector'.
                   Required for position count and sector checks.
        check_time: datetime to check no-trade window against. Defaults to now (ET).

    Returns:
        Dict with 'passed' (bool), and if failed: 'rule', 'current', 'limit', 'detail'.
    """
    ticker = ticker.upper()
    side = side.lower()
    order_type = order_type.lower()

    # --- Rule 1: Universe whitelist ---
    universe = _load_universe()
    allowed_tickers = [t.upper() for t in universe.get("tickers", [])]
    if ticker not in allowed_tickers:
        return _fail(
            "UNIVERSE_WHITELIST",
            ticker,
            allowed_tickers,
            f"{ticker} is not in the locked universe. Allowed: {allowed_tickers}",
        )

    # --- Rule 2: Order type ---
    if order_type not in _ALLOWED_ORDER_TYPES:
        return _fail(
            "ORDER_TYPE",
            order_type,
            list(_ALLOWED_ORDER_TYPES),
            f"Order type '{order_type}' not allowed. Use 'market' or 'limit'.",
        )

    # --- Rule 3: No-trade windows (buy orders only; allow sells at any time for stop-loss) ---
    if side == "buy":
        now_et = check_time or datetime.now(_ET)
        if isinstance(now_et, datetime) and now_et.tzinfo is None:
            now_et = _ET.localize(now_et)
        t = now_et.time()
        in_open_window = _MARKET_OPEN <= t < _NO_TRADE_WINDOW_OPEN_END
        in_close_window = _NO_TRADE_WINDOW_CLOSE_START <= t < _MARKET_CLOSE
        if in_open_window or in_close_window:
            window = "9:30–9:45 ET" if in_open_window else "15:45–16:00 ET"
            return _fail(
                "NO_TRADE_WINDOW",
                t.strftime("%H:%M ET"),
                f"Outside {window}",
                f"Buy orders not allowed during no-trade window {window}.",
            )

    # --- Account-dependent checks (skipped if account not provided) ---
    if account is not None:
        equity = float(account.get("equity", 0))
        positions = positions or []

        # --- Rule 4: Sector concentration (40% of equity) ---
        if side == "buy" and equity > 0:
            universe_data = _load_universe()
            sector_map = universe_data.get("sector_map", {})
            ticker_sector = sector_map.get(ticker, "Unknown")

            # Sum current market value by sector
            sector_values: dict[str, float] = {}
            for p in positions:
                s = sector_map.get(p["ticker"].upper(), "Unknown")
                sector_values[s] = sector_values.get(s, 0) + float(p.get("market_value", 0))

            # Add the prospective new position value
            price = estimated_price or next(
                (float(p.get("current_price", 0)) for p in positions if p["ticker"].upper() == ticker),
                0,
            )
            estimated_value = qty * price if price > 0 else 0
            sector_values[ticker_sector] = sector_values.get(ticker_sector, 0) + estimated_value

            max_sector_value = equity * 0.40
            current_sector_value = sector_values.get(ticker_sector, 0)
            if current_sector_value > max_sector_value:
                return _fail(
                    "SECTOR_CONCENTRATION",
                    round(current_sector_value, 2),
                    round(max_sector_value, 2),
                    f"Sector '{ticker_sector}' would reach ${current_sector_value:.2f}, exceeding 40% of equity (${max_sector_value:.2f}).",
                )

    return _pass()
