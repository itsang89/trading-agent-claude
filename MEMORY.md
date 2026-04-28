# MEMORY.md — Memory Layout for the LLM Trading Agent

This document defines the memory layout used by all routines. The layout is locked after week 1.

---

## Directory Tree

```
Trading-agent-claude/
├── state/
│   ├── positions.json       # Current holdings (cache from Alpaca — overwrite each routine)
│   ├── account.json         # Account snapshot (overwrite each routine)
│   ├── universe.json        # Locked universe + sector map (set week 1, read-only after)
│   ├── position-highs.json  # Peak close price per held ticker for trailing stop calculation
│   └── strategy.md          # Strategy rules and signal arithmetic (operator edits only, read every session)
│
├── trades/
│   └── trades.csv           # Append-only trade log
│
├── journal/
│   ├── YYYY-MM-DD-pre-market.md
│   ├── YYYY-MM-DD-execution.md
│   ├── YYYY-MM-DD-eod.md
│   └── YYYY-MM-DD-weekly.md
│
├── metrics/
│   └── daily-metrics.csv    # Append-only daily P&L and benchmark (script-written only)
│
├── logs/
│   └── behavioral-flags.jsonl  # Append-only behavioral event log
│
├── notes-for-operator.md    # Append-only; LLM writes here for human attention
└── universe-proposal.md     # Week-1 only: proposed universe for operator review
```

---

## File Purposes and Write/Read Patterns

### `state/positions.json`
- **Purpose:** Cache of current Alpaca positions. Refreshed at the start of each routine.
- **Written by:** Routines (via `get_positions.py` output, saved by the LLM at routine start).
- **Read by:** All routines, stop-loss checks.
- **Write pattern:** Full overwrite each routine.
- **Schema:**
```json
[
  {
    "ticker": "SPY",
    "qty": 10.0,
    "avg_entry_price": 540.12,
    "current_price": 542.00,
    "market_value": 5420.00,
    "unrealized_pl": 18.80,
    "unrealized_plpc": 0.00348,
    "side": "long"
  }
]
```

### `state/account.json`
- **Purpose:** Snapshot of account equity, cash, buying power.
- **Written by:** Routines (overwrite from `get_account.py`).
- **Read by:** All routines, sizing decisions, validator.
- **Write pattern:** Full overwrite each routine.
- **Schema:**
```json
{
  "equity": 10000.00,
  "cash": 5000.00,
  "buying_power": 5000.00,
  "portfolio_value": 10000.00,
  "currency": "USD"
}
```

### `state/position-highs.json`
- **Purpose:** Tracks the peak closing price and original entry price for each held position. Used to compute trailing stop prices each routine.
- **Written by:** Routines — updated whenever a new high is set, and when positions are opened or closed.
- **Read by:** All routines (stop-loss/trailing-stop audit step).
- **Write pattern:** Full overwrite on change. Never append.
- **Schema:**
```json
{
  "NVDA": {"high_close": 215.50, "entry_price": 209.45, "last_updated": "2026-04-28"}
}
```
- **Trailing stop logic:** `effective_stop = max(entry_price * 0.92, high_close * 0.90 if high_close > entry_price * 1.10 else 0)`
- **Maintenance:** Add on new position open; update entry_price on adding shares; update high_close whenever new bars data shows a higher close; remove on position close.

### `state/universe.json`
- **Purpose:** The locked trading universe. Source of truth for the validator whitelist and sector map.
- **Written by:** Operator only (after week-1 review). Routines must never write this.
- **Read by:** `tools/lib/validator.py` (every order), `CLAUDE.md` reference.
- **Write pattern:** Written once at lock. Never overwritten during experiment.
- **Schema:**
```json
{
  "status": "LOCKED",
  "locked": true,
  "locked_at": "2026-05-05",
  "tickers": ["SPY", "QQQ", "AAPL", "..."],
  "sector_map": {
    "SPY": "ETF",
    "QQQ": "ETF",
    "AAPL": "Information Technology"
  }
}
```

### `trades/trades.csv`
- **Purpose:** Permanent record of every order placed (successful or not).
- **Written by:** `tools/place_order.py` (on successful submission). Rejections are NOT logged here — they go to `behavioral-flags.jsonl`.
- **Read by:** `tools/append_metrics.py` (to count daily orders), weekly review.
- **Write pattern:** Append-only. Never overwrite.
- **Schema:**
```
date,time,ticker,side,qty,price,order_id,status,routine
2026-04-28,09:47:00,SPY,buy,5,,abc123,accepted,market-open-execution
```

### `journal/YYYY-MM-DD-<routine>.md`
- **Purpose:** Narrative log per routine run. Human-readable. Terse bullet format.
- **Written by:** The LLM at the end of each routine.
- **Read by:** LLM reads last 3 entries before forming intents (any type). Weekly review reads all entries from the week.
- **Write pattern:** Create new file per run. Never overwrite existing entries.
- **Naming:** `2026-04-28-pre-market.md`, `2026-04-28-execution.md`, `2026-04-28-eod.md`, `2026-04-28-weekly.md`

### `metrics/daily-metrics.csv`
- **Purpose:** Structured daily performance record. The spine of the week-4 retrospective.
- **Written by:** `tools/append_metrics.py` ONLY — NOT the LLM.
- **Read by:** Weekly review, final retrospective.
- **Write pattern:** Append-only. One row per trading day.
- **Schema:**
```
date,equity,cash,day_pnl_abs,day_pnl_pct,spy_close,spy_day_return,cum_return,cum_spy_return,positions_held,orders_placed,orders_rejected
2026-04-28,10050.00,4200.00,50.00,0.5,540.10,0.25,0.50,0.25,3,2,0
```

### `logs/behavioral-flags.jsonl`
- **Purpose:** Machine-parseable log of behavioral events for the experiment retrospective.
- **Written by:** LLM (during routines) and `tools/place_order.py` (validator rejections).
- **Read by:** Weekly review, operator audit, final retrospective.
- **Write pattern:** Append-only JSONL. One JSON object per line.
- **Schema:**
```json
{"date": "2026-04-28", "routine": "market-open-execution", "flag_type": "GUARDRAIL_REJECTION", "ticker": "NVDA", "rule": "UNIVERSE_WHITELIST", "context": "Attempted to buy NVDA which is not in locked universe."}
{"date": "2026-04-28", "routine": "pre-market-research", "flag_type": "STOP_LOSS_TRIGGERED", "ticker": "QQQ", "rule": "STOP_LOSS_8PCT", "context": "QQQ loss reached 8.3%. Queuing market-sell."}
```

**Flag types:**
- `GUARDRAIL_REJECTION` — validator rejected an order
- `STOP_LOSS_TRIGGERED` — position hit 8% loss threshold from entry
- `TRAILING_STOP_TRIGGERED` — position dropped 10% below its peak close (trailing stop)
- `RS_MOMENTUM_DECAY` — RS_spread declining 3 consecutive sessions (early warning)
- `SELF_CONTRADICTION` — LLM reasoning contradicts a prior journal entry
- `HALLUCINATED_TICKER` — LLM referenced a ticker not in the universe
- `TOOL_ERROR` — a tool call returned an error

### `notes-for-operator.md`
- **Purpose:** Async communication from the LLM to the operator. Write here instead of blocking a routine for human input.
- **Written by:** LLM (append-only). Never overwrite.
- **Read by:** Operator between sessions.
- **Write pattern:** Each note starts with `## [YYYY-MM-DD HH:MM ET]`.

### `universe-proposal.md`
- **Purpose:** Week-1 universe proposal for operator review.
- **Written by:** LLM on first pre-market run of week 1.
- **Read by:** Operator (reviews and locks into `state/universe.json`).
- **Write pattern:** Written once. Not updated.

---

## Read/Write Summary Per Routine

| File | pre-market | execution | mid-session | eod | weekly |
|------|-----------|-----------|-------------|-----|--------|
| `state/positions.json` | Read+Write | Read+Write | Read+Write | Read | Read |
| `state/account.json` | Read+Write | Read+Write | Read+Write | Read | — |
| `state/universe.json` | Read | Read | — | — | Read |
| `state/strategy.md` | Read | Read | Read | Read | Read |
| `state/position-highs.json` | Read+Write | Read+Write | Read+Write | Read+Write | — |
| `trades/trades.csv` | — | (via tool) | (via tool) | — | Read |
| `journal/*.md` | Read 3, Write | Read today's, Write | Read today's, Write | Write | Read all week, Write |
| `metrics/daily-metrics.csv` | — | — | — | Read | Read |
| `logs/behavioral-flags.jsonl` | Write (if triggered) | Write (if triggered) | Write (if triggered) | — | Read |
| `notes-for-operator.md` | Write (if needed) | Write (if needed) | Write (if needed) | Write (if needed) | Write (if needed) |
