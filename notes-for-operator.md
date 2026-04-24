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

---

## [2026-04-23 ~16:34 ET — EOD Routine]

**EOD ROUTINE COMPLETED — 2026-04-23**
- Equity: $10,000.00 | Cash: 100% | Positions: 0 | Day P&L: $0.00
- vs SPY today: agent 0.00% vs SPY -0.51% (agent in cash; pre-experiment period)
- Experiment starts 2026-04-27. No trades executed. No stop-loss events.
- state/last-session.md updated. metrics/daily-metrics.csv appended.
- Committed and pushed to main (commit: eod: 2026-04-23).

**DATA QUALITY NOTE — metrics/daily-metrics.csv double-write:**
- The EOD routine prompt instructs the LLM to run append_metrics.py, but the Makefile also runs it after the LLM finishes (per design note in [2026-04-22]). This causes 2 rows per day for 2026-04-23.
- Recommendation: remove `python3 tools/append_metrics.py` from the EOD prompt, or add date-deduplication to append_metrics.py.

**EMAIL TOOL ERROR — EOD routine:**
- `tools/send_email.py` timed out (>20s). Consistent with prior SMTP failures.
- Email summary not sent. Email cannot be delivered until IPv4 SMTP is available.

---

## [2026-04-23 ~16:30 ET]

**EMAIL TOOL ERROR — end-of-day-review routine**
- `tools/send_email.py` failed: `module 'smtplib' has no attribute '_GLOBAL_DEFAULT_TIMEOUT'`
- This is a Python/smtplib compatibility error (different from prior IPv6 error).
- EOD routine completed successfully. All files committed and pushed.
- Email summaries will not send until send_email.py is fixed or compatible environment provided.

---

## [2026-04-23 ~10:54 ET]

**EMAIL TOOL ERROR — pre-market-research routine**
- `tools/send_email.py` failed: `[Errno 97] Address family not supported by protocol`
- Same IPv6 network error as prior note. Email summaries will not send until network supports IPv4 SMTP (port 587).
- All other routine steps completed successfully.
- Pre-market journal, universe proposal, and state files committed and pushed to main.

**OPERATOR ACTION REQUIRED:**
1. Review `universe-proposal.md` (12 tickers, 6 GICS sectors, 3 ETFs per strategy.md recommendation).
2. If approved, lock `state/universe.json` with full universe before Week 2 (2026-05-04).
3. Experiment start date confirmed: 2026-04-27 (Monday). Execution routine should run that morning.
4. QQQ signals: BULLISH + RS POSITIVE (+2.72%) — buy intent queued for 2026-04-27 at 5% of equity.

---

## [2026-04-24 ~8:41 ET — Pre-Market Routine]

**PRE-MARKET ROUTINE COMPLETED — 2026-04-24**
- Equity: $10,000.00 | Cash: 100% | Positions: 0
- No orders placed. Pre-experiment gate (start_date: 2026-04-27) applies.
- QQQ signals revalidated (4/23 close): Trend BULLISH ($651.40 > SMA_14 $626.73), RS_spread +2.58% (POSITIVE).
- Monday intent: BUY QQQ 5% (~$500) if signals hold at 2026-04-27 pre-market.
- Committed and pushed to main (commit: pre-market: 2026-04-24).

**EMAIL TOOL ERROR — pre-market-research routine:**
- `tools/send_email.py` failed: SENDGRID_API_KEY not set in environment.
- Email summary not sent. Set SENDGRID_API_KEY in .env to enable email delivery.

---

## [2026-04-24 ~9:46 ET — Execution Routine]

**EXECUTION ROUTINE COMPLETED — 2026-04-24**
- Equity: $10,000.00 | Cash: 100% | Positions: 0
- No orders placed. Pre-experiment gate (start_date: 2026-04-27) applies.
- Market was OPEN at 9:45 AM ET. No stop-loss events (no positions held).
- Committed and pushed to main (commit: execution: 2026-04-24).

**EMAIL TOOL ERROR — execution routine:**
- `tools/send_email.py` failed: SENDGRID_API_KEY not set in environment.
- Email summary not sent. Set SENDGRID_API_KEY in .env to enable email delivery.

---

## [2026-04-24 ~16:34 ET — EOD Routine]

**EOD ROUTINE COMPLETED — 2026-04-24**
- Equity: $10,000.00 | Cash: 100% | Positions: 0 | Day P&L: $0.00 (0.00%)
- vs SPY today: agent 0.00% vs SPY +0.78% (SPY close: $713.97). Agent in cash — pre-experiment.
- Cumulative: N/A — experiment starts 2026-04-27.
- No stops triggered. No contradictions. No behavioral flags.
- state/last-session.md updated. metrics/daily-metrics.csv appended. Committed and pushed to main.
- Monday 2026-04-27: Experiment Day 1. QQQ buy intent (5%, ~$500) pending signal revalidation.

**EMAIL TOOL ERROR — EOD routine:**
- `tools/send_email.py` failed: SENDGRID_API_KEY not set in environment.
- Email summary not sent. Set SENDGRID_API_KEY in .env to enable email delivery.

---

## [2026-04-23 ~15:46 ET]

**EXECUTION ROUTINE — no orders placed**
- Routine triggered at 15:46 ET. Two blockers applied:
  1. Experiment gate: start_date = 2026-04-27. Pre-market journal explicit: do not execute before then.
  2. No-trade window: routine ran within 15:45–16:00 ET window (buys blocked).
- Portfolio: $10,000 cash, 0 positions. No stop-loss checks required.
- All files committed and pushed.
- EMAIL TOOL ERROR: send_email.py likely failed again (recurring smtplib issue logged at [2026-04-23 ~16:30 ET]). Email summary not sent.
