# LLM Trading Agent

A 4-week paper-trading experiment where a Claude-model-driven agent trades US equities on an Alpaca paper account. The stated goal is to beat SPY over 4 weeks. The real goal is behavioral observation.

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure credentials**
```bash
cp .env.example .env
# Edit .env and fill in your Alpaca paper trading API key and secret
# Set EXPERIMENT_START_DATE to the first live trading day (YYYY-MM-DD)
```

**3. Verify tools work**
```bash
make test-tools
```

## Running Routines

Routines are triggered manually or via Claude Desktop automation:

| Command | Schedule | Purpose |
|---|---|---|
| `make run-premarket` | 8:30 AM ET, Mon–Fri | Research and form trading intents |
| `make run-execution` | 9:45 AM ET, Mon–Fri | Execute intents, check stops |
| `make run-eod` | 4:30 PM ET, Mon–Fri | Review day, log metrics |
| `make run-weekly` | 5:00 PM ET, Friday | Weekly synthesis (Opus model) |

## Manual Tool Usage

Each tool in `tools/` is independently runnable:

```bash
python tools/get_account.py
python tools/get_positions.py
python tools/get_bars.py SPY 20
python tools/get_quote.py QQQ
python tools/get_market_status.py
python tools/get_spy_benchmark.py
python tools/validate_order.py SPY buy 5 market   # dry run — no order placed
python tools/place_order.py SPY buy 5 market       # places real paper order
python tools/cancel_order.py <order_id>
```

## Project Structure

```
state/        — live position/account snapshots (re-fetched each routine)
trades/       — append-only trade log (CSV)
journal/      — per-routine narrative entries (date-stamped markdown)
metrics/      — daily P&L vs SPY benchmark (CSV, written by script)
logs/         — behavioral event log (JSONL)
tools/        — all Alpaca wrappers + guardrail validator
CLAUDE.md     — operational brief read by Claude every session
MEMORY.md     — memory layout documentation
```

## Guardrails

All orders are validated before reaching Alpaca:
- Max single position: 10% of portfolio equity
- Stop-loss: 8% below avg entry (LLM-managed each routine)
- Max concurrent positions: 8
- Minimum cash reserve: 20%
- No-trade windows: 9:30–9:45 ET and 15:45–16:00 ET
- Universe whitelist only
- Market and limit orders only

## Week-1 Setup

1. Run `make run-premarket` on the first trading morning
2. Claude will propose a universe → written to `universe-proposal.md`
3. Operator reviews proposal, approves, and updates `state/universe.json`
4. Full-universe trading begins Monday of week 2

## Reset

```bash
make reset-state    # clears state/positions.json and state/account.json (asks for confirmation)
```
