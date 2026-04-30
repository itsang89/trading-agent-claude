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

---

## [2026-04-24 ~17:00 ET — Weekly Review Routine]

**WEEKLY REVIEW COMPLETED — Week 1 (Pre-Experiment)**
- Experiment has not yet started (start date 2026-04-27). Week covered only Thu 4/23 and Fri 4/24.
- 0 trades placed, 0 rejected, 0 stop-losses, 0 behavioral flags. Equity flat at $10,000.
- vs SPY: agent 0.00% vs SPY +0.78% over the 2-day window (expected — pre-experiment).
- Journal written: `journal/2026-04-24-weekly.md`.
- last-session.md updated with Monday (experiment day 1) posture.
- **4 new LEARNED BEHAVIORS added to CLAUDE.md** — 2 HIGH-confidence, 2 MEDIUM-confidence. All operational/epistemic (no trading-skill rules yet).
- Learnings summary: `learnings/2026-W17-week1.md`.
- Learning-harness entry appended: `{"date": "2026-04-24", "week": 1, "rules_extracted": 4, ...}`.

**OPEN OPERATOR ITEMS (carry-forward):**
1. Set `SENDGRID_API_KEY` in environment (email is currently a dead channel — 6/6 routines this week failed to send).
2. Resolve `append_metrics.py` double-write (EOD prompt vs Makefile both invoke it → duplicate row for 2026-04-23).
3. Review `universe-proposal.md` and lock `state/universe.json` before Week 2 (deadline 2026-05-04).
4. Update `current_week` in `state/experiment-config.json` on Monday if the convention is 1-based-from-start.
5. Consider pruning the extra 4/23 row in `metrics/daily-metrics.csv` to keep downstream aggregations honest.

**EMAIL TOOL ERROR — weekly-review routine:** Will attempt at end of routine; expected to fail again (SENDGRID_API_KEY not set). Routine proceeds per new learned behavior rule #4.

**PUSH FAILURE — weekly-review routine:**
- Attempted `git push origin HEAD:main` per CLAUDE.md routine instructions → HTTP 403 "Permission to itsang89/trading-agent-claude.git denied to itsang89" via local proxy (http://127.0.0.1:36359/git/...).
- Fallback `git push -u origin claude/vigilant-edison-AOmrc` → same 403.
- Commit `d8180cf weekly-review: 2026-04-24` created locally but **NOT pushed**.
- This differs from prior routines this week (all EOD/pre-market/execution pushes on 4/23 and 4/24 succeeded to main). Operator should check credential/permission state on the local_proxy.
- Routine continued to email step per "do not block on push failure" discretion. If operator wants the routine to hard-stop on push failure instead, update CLAUDE.md rule #5 scope.

---

## [2026-04-27 ~8:45 ET — Pre-Market Routine]

**PRE-MARKET ROUTINE COMPLETED — 2026-04-27 (Experiment Day 1)**
- Equity: $10,000.00 | Cash: 100% | Positions: 0
- Experiment has officially started. Full 12-ticker universe is active (operator locked 2026-04-26 — noted and applied).
- 6 tickers eligible (MSFT, AMZN, NVDA, QQQ, GOOGL, META). 5 primary buy intents queued for execution at 9:45 AM.
- No errors, no stop-losses, no behavioral flags.
- All 13-bar proxies (SMA_13) in use — closes substantially above SMA_13 for all eligible tickers; signals robust.

**SPY BENCHMARK START_PRICE NOTE:**
- `get_spy_benchmark.py` returns start_price=711.20, start_date=2026-04-27, latest_date=2026-04-24.
- Per bars data, SPY close on 2026-04-22 = 711.20. It appears the benchmark baseline was initialized to the 4/22 close, not the 4/24 close (713.97) or today's 4/27 open.
- As-is, cumulative SPY return = +0.39% at today's open. Agent starts at 0.00%. Agent was in cash pre-experiment so the gap is expected.
- No action needed unless operator wants to reset benchmark to today's actual open price. Using tool output as authoritative per learned behavior [W1|HIGH].

**EMAIL TOOL:** Will attempt at end of routine; expected to fail (SENDGRID_API_KEY not set per prior notes).

---

## [2026-04-29 ~9:45 ET — Execution Routine STOPPED]

**PRE-MARKET ROUTINE DID NOT RUN TODAY**
- `journal/2026-04-29-pre-market.md` does not exist.
- Execution routine cannot proceed without pre-market intents — no buy/sell intents available, no queued stop-loss sells from signal review.
- Routine STOPPED per Step 2 instructions.
- **OPERATOR ACTION REQUIRED:** Run `make run-premarket` manually or investigate why the pre-market routine did not execute at 8:30 AM ET.
- **RISK NOTE:** 6 positions remain open from 2026-04-28 execution (NVDA, MSFT, GOOGL, META, AMZN, QQQ). Stop-loss audit was NOT performed this session. Positions are unmonitored until the next routine runs. If significant drawdown has occurred, manual intervention may be needed.
- Open positions as of last-session.md (2026-04-28 execution): NVDA avg_entry $209.45 (stop $192.69), MSFT $419.91 (stop $386.32), GOOGL $346.55 (stop $318.83), META $675.94 (stop $621.86), AMZN $260.99 (stop $240.11), QQQ $661.81 (stop $608.87).

## [2026-04-28 ~16:30 ET — EOD Routine for 2026-04-27]

**EOD ROUTINE COMPLETED — reviewing Experiment Day 1 (2026-04-27)**
- EOD ran one day late (executed 2026-04-28 instead of 2026-04-27 at 4:30 PM ET).
- Equity at tool-call time: $10,033.63 | Cash: $7,018.71 | Positions: 6
- Day 1 P&L: +$33.63 (+0.34%) vs SPY today +0.17% → agent outperformed by +0.17 pp
- Cumulative: agent +0.34% | SPY 0.00% (experiment-anchored per get_spy_benchmark)
- No stop-loss triggers. No behavioral flags. No contradictions vs execution journal.
- journal/2026-04-27-eod.md written. state/last-session.md updated.

**METRICS DISCREPANCY — append_metrics.py:**
- append_metrics.py wrote row dated 2026-04-28 (today) with equity $10,020.92 — not 2026-04-27 with $10,033.63.
- Cause: routine ran late; tool used current date and live prices at time of execution.
- metrics/daily-metrics.csv now has a 4/28 row instead of a 4/27 row for Day 1 data.
- cum_spy_return in metrics (0.9535%) anchors from 2026-04-23 (first CSV row); get_spy_benchmark anchors from 2026-04-27 (experiment start). Both are internally consistent but tracking different baselines.
- Recommendation: if you need Day 1 close data accurately in the CSV, manually correct the 4/28 row to date=2026-04-27 and equity=$10,033.63. Otherwise, accept 4/28 row as-is and note the late-run gap.

**EMAIL TOOL:** Attempting at end of routine; expected to fail (SENDGRID_API_KEY not set per prior notes).

---

## [2026-04-29 ~8:43 ET — Pre-Market Routine]

**PRE-MARKET ROUTINE COMPLETED — 2026-04-29 (Experiment Day 3)**
- Equity: $10,010.23 | Cash: $7,018.71 (70.1%) | Positions: 6
- Cumulative: agent +0.10% | SPY −0.49% → agent leads by +0.59 pp
- Regime: BULL (10/12 BULLISH)
- META RS_spread = −1.15% — first NEGATIVE session (counter=1). No sell today; watch for 2nd consecutive.
- Intents: BUY AAPL at 5% (~$501), ADD MSFT to 10% (~$500 more). XLE skipped (borderline).
- No stop-loss triggers. All tools returned clean output.

**PUSH FAILURE — pre-market routine:**
- `git push -u origin claude/pensive-bardeen-2M7Rl` → HTTP 403 "Permission to itsang89/trading-agent-claude.git denied to itsang89" via local proxy.
- Commit `pre-market: 2026-04-29` created locally but **NOT pushed** to remote.
- Same 403 error seen on weekly-review 2026-04-24. Operator should verify proxy credential state.
- All journal, state, and position-highs files are committed locally and will push when credentials are restored.

[2026-04-30 execution] git push origin HEAD:main returned 403 (permission denied). All changes are committed and pushed to claude/laughing-cray-2QNn6. Operator action needed to merge to main.
