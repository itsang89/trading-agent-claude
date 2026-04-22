# Notes for Operator

Append-only. Each note starts with `## [YYYY-MM-DD HH:MM ET]`.

---

## [2026-04-22 Build Phase]

**Build complete.** All scaffolding per INSTRUCTIONS.md Section 10 has been produced. Summary of what was built:

### Artifacts Created

- `.gitignore` — excludes `.env`, `.lock`, `__pycache__`, `state/*.json`
- `.env.example` — template with `ALPACA_API_KEY`, `ALPACA_API_SECRET`, `ALPACA_BASE_URL`, `EXPERIMENT_START_DATE`
- `requirements.txt` — `alpaca-py`, `python-dotenv`, `pandas`, `pytz`, `requests`
- `README.md` — setup and usage guide
- `CLAUDE.md` — operational brief (concise, under 200 lines)
- `MEMORY.md` — full memory layout documentation

### Directory Scaffold
- `state/` — positions.json and account.json excluded from git (re-fetched from Alpaca); `universe.json` initialized with week-1 stub (SPY + QQQ only)
- `trades/trades.csv` — initialized with headers, append-only
- `metrics/daily-metrics.csv` — initialized with headers, append-only
- `logs/behavioral-flags.jsonl` — empty, append-only
- `journal/` — empty, populated per routine run

### Tool Layer (`tools/`)
- `tools/lib/alpaca_client.py` — shared Alpaca client (TradingClient + StockHistoricalDataClient)
- `tools/lib/validator.py` — deterministic guardrail enforcement (all 7 rules from Section 3)
- `tools/get_account.py`
- `tools/get_positions.py`
- `tools/get_bars.py`
- `tools/get_quote.py`
- `tools/get_market_status.py`
- `tools/get_spy_benchmark.py`
- `tools/validate_order.py`
- `tools/place_order.py`
- `tools/cancel_order.py`
- `tools/append_metrics.py`

### Makefile Targets
- `make test-tools` — tests all read-only tools
- `make run-premarket` / `run-execution` / `run-eod` / `run-weekly`
- `run-eod` also calls `append_metrics.py` automatically
- `make reset-state` — clears state files with confirmation

---

### Design Decisions You Should Know

1. **Alpaca SDK:** Using `alpaca-py` (the current maintained SDK), not the deprecated `alpaca-trade-api`. API docs: https://docs.alpaca.markets/

2. **Stop-loss enforcement:** Fully LLM-managed. The agent checks every position each routine and places a market-sell if loss ≥8%. No standing Alpaca stop orders. This means: if a routine doesn't run, stops don't trigger. You own the operational reliability.

3. **Week-1 universe stub:** `state/universe.json` has `"tickers": ["SPY", "QQQ"]` and `"locked": false`. After you review `universe-proposal.md` (written by the first pre-market run), update `state/universe.json` with the full list and set `"locked": true`. Then update the universe section in `CLAUDE.md`.

4. **Model for weekly-review:** INSTRUCTIONS.md says "Claude Opus 4.7". The current latest Opus model ID is `claude-opus-4-6`. The Makefile uses `claude-opus-4-6`. Update when 4.7 is available.

5. **No-trade window for sells:** The validator only blocks BUY orders during the 9:30–9:45 and 15:45–16:00 windows. SELL orders (including stop-loss sells) are always allowed — this is intentional to ensure stop-losses can execute at any time.

6. **append_metrics.py:** This is called by `make run-eod` after the LLM routine finishes. It queries Alpaca directly and does not rely on any LLM output. The LLM does not write to `metrics/daily-metrics.csv`.

7. **Sector concentration check:** The validator uses prices from the current `positions` list to estimate post-trade sector value. If a ticker is being bought for the first time and has no current position, the price estimate is 0 and the sector check is effectively skipped for that order. For a full check, use `validate_order.py` which fetches live positions.

---

### Pre-Flight Checklist (Before First Live Run)

- [ ] Copy `.env.example` to `.env` and fill in Alpaca paper credentials
- [ ] Run `make test-tools` — all tools should return valid JSON
- [ ] Confirm `python tools/validate_order.py SPY buy 1 market` returns `{"passed": true}` (or expected rejection)
- [ ] Confirm `.env` is not tracked by git: `git status` should not show `.env`
- [ ] Set `EXPERIMENT_START_DATE` in `.env` to the first live trading day
- [ ] Review and run `make run-premarket` manually on the first morning to generate `universe-proposal.md`
- [ ] Review `universe-proposal.md`, update `state/universe.json`, lock the universe
- [ ] Update the universe section in `CLAUDE.md` before week-2 begins
