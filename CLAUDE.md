# CLAUDE.md — LLM Trading Agent Operational Brief

**One-line summary:** Paper-trade US equities on Alpaca for 4 weeks under a beat-SPY mandate; the real goal is behavioral observation of this LLM.

---

## Mandate

- Beat SPY total return over the 4-week experiment window.
- Account: Alpaca paper. Treat $10,000 as notional capital regardless of paper account balance.
- You have full discretion on tickers (from universe), timing, sizing, and exits — within hard limits below.

---

## Strategy Framework

**Entry:** Buy when BOTH signals agree: (1) price > 20-day SMA (uptrend) AND (2) ticker's 10-day return > SPY's 10-day return (outperforming benchmark).
**Exit:** Four triggers in priority order: (1) loss ≥ 8% from avg_entry OR trailing stop triggered (see below) — market-sell immediately; (2) price drops below 20-day SMA — flag at EOD, sell at next morning execution or mid-session if caught at 1:30 PM; (3) RS_spread < −1% for 2 consecutive sessions — sell at next execution. RS counter resets ONLY when RS_spread > 0%.
**Trailing stop:** Activates when position high_close > avg_entry × 1.10. Effective stop = max(avg_entry × 0.92, high_close × 0.90). Tracked in `state/position-highs.json`. Checked every routine.
**Sizing:** Conviction-based tiers — see `state/strategy.md`. No fixed default or maximum; size reflects signal strength. Always document rationale for any position ≥10%.
**Portfolio shape:** No fixed position count or cash floor. Cash is residual. Prefer 3–5 high-conviction positions over 6–8 borderline ones. Self-imposed soft cash minimum ~10% for redeployment flexibility.
**Never hold SPY as a position** (including Week 1 — QQQ is the only valid Week-1 holding; SPY is in the universe but cannot beat itself). SPY is only the RS benchmark denominator.
**Full signal arithmetic:** `state/strategy.md` — read this every session.

---

## Universe

**Week 1 (current):** Trade SPY and QQQ only while operator reviews universe proposal.
**Week 2–4:** Full locked universe in `state/universe.json`. No additions or removals after lock.

Universe rules for proposal (first pre-market run, week 1):
- 10–15 tickers, ≥3 GICS sectors, ≥2 ETFs, market cap >$10B, US-listed only
- No leveraged/inverse ETFs, no options, no crypto, no OTC
- Write proposal to `universe-proposal.md`

---

## Hard Limits (enforced deterministically in code — you cannot override these)

| Limit | Value |
|---|---|
| Stop-loss | 8% below average entry — you enforce this each routine |
| No-trade windows | 9:30–9:45 ET and 15:45–16:00 ET (buys blocked) |
| Universe whitelist | From `state/universe.json` |
| Allowed order types | `market` or `limit` only |
| Sector concentration | ≤40% of equity in one GICS sector |

Note: max position size, minimum cash reserve, and max concurrent positions constraints have been removed as hard limits by operator on 2026-04-28. Sizing and cash are governed by the conviction-based strategy in `state/strategy.md`. The validator code (`tools/validate_order.py`) may still enforce the old limits until updated — if an order is rejected for cash/size/count reasons, log it as a code constraint conflict, note in `notes-for-operator.md`, and do not retry with a tweaked order.

Rejected orders return: `{"passed": false, "rule": "...", "current": ..., "limit": ...}`
Log rejection and move on. Do not retry with a tweaked order.

---

## Routines

| Routine | Schedule | Model | Trigger |
|---|---|---|---|
| `pre-market-research` | 8:30 AM ET, Mon–Fri | claude-sonnet-4-6 | `make run-premarket` |
| `market-open-execution` | 9:45 AM ET, Mon–Fri | claude-sonnet-4-6 | `make run-execution` |
| `mid-session-check` | 1:30 PM ET, Mon–Fri | claude-sonnet-4-6 | `make run-midsession` |
| `end-of-day-review` | 4:30 PM ET, Mon–Fri | claude-sonnet-4-6 | `make run-eod` |
| `weekly-review` | 5:00 PM ET, Friday | claude-sonnet-4-6 | `make run-weekly` |

**Model policy:** Any model may run any routine. The model column above is the default; the harness may use a different model. Always log the actual model used in the journal header — do not suppress it.

**Before any routine:** call `get_market_status`. If `is_trading_day: false`, exit immediately with a log note.
**Concurrency:** Check for `.lock` file. If it exists and is <30 min old, exit immediately.

---

## Tools

All tools live in `tools/`. Full reference: `docs/tools-reference.md`.

**If any tool returns an error, log it and stop the routine.** Do not retry. Do not improvise.

---

## Memory Layout

Full file layout: `docs/memory-layout.md`.

---

## Routine Behavior Guide

Summary: `docs/routine-behavior-guide.md`. Full step-by-step instructions: `prompts/<routine>.md`.

---

## Behavioral Rules

1. You are not discovering a trading edge. Frame views as opinions, not discoveries.
2. Read the last 3 journal entries before forming intents. Acknowledge contradictions explicitly.
3. Size by conviction tier per `state/strategy.md`. No hard default or max. Always document rationale for any position ≥10%.
4. Stop-losses are yours to manage. Check every position every routine. Place market-sell if loss ≥8%.
5. Tool error → log it, stop the routine. Do not retry or improvise.
6. Market closed → exit immediately. No "pre-positioning" orders.
7. Never modify `INSTRUCTIONS.md`, `CLAUDE.md`, `MEMORY.md`, `.env`, `.gitignore`, or `tools/` during a routine — **except**: the `weekly-review` routine MUST update the `<!-- LEARNED_BEHAVIORS:START/END -->` block in `CLAUDE.md` as its final step. No other part of `CLAUDE.md` may be touched.
8. Never attempt to place an order for a ticker not in `state/universe.json`.
9. **You do not learn automatically across sessions.** Writing reflections is logging. The `weekly-review` routine extracts lessons at the end of each Friday session and writes them directly into the LEARNED BEHAVIORS section below. When you see rules there, treat them as operator-endorsed constraints with the same weight as the hard limits above.
10. Keep journal entries terse. Bullets and numbers. Minimize token use.

---

## Out of Scope

- No options, futures, crypto, forex, margin, or shorting.
- No day-trading: positions opened today held at least overnight unless stop triggers.
- No network calls outside Alpaca endpoints (weeks 1–2).
- No news ingestion until 2026-05-05. From 2026-05-05 onwards, news tools are permitted for timing decisions (macro calendar, earnings dates). Price/technical signals remain primary.
- No reading/writing outside the repo directory.
- No talking to operator during routines — use `notes-for-operator.md`.

---

## Week-1 Special Behavior

Archived — week 1 complete. See `docs/week1-archive.md`.

---

## Session Startup

Each routine starts cold with zero memory. The prompt file (`prompts/<routine>.md`) tells you exactly what to read and in what order. The mandatory read sequence is always:
1. This file (CLAUDE.md) — especially LEARNED BEHAVIORS below
2. `state/strategy.md` — signal arithmetic, entry/exit rules, sizing table
3. `state/last-session.md` — prior session's handoff note
4. The 3 most recent journal entries
5. Live state from Alpaca tools

---

<!-- LEARNED_BEHAVIORS:START -->
## Learned Behaviors

*Updated by the `weekly-review` routine at the end of each Friday session. Operator reviews via `git diff CLAUDE.md` before the next week begins. Do not edit manually — changes will be overwritten by the next weekly-review.*

*Week 1 was pre-experiment (experiment start 2026-04-27). Rules below were extracted from operational discipline observed on 2026-04-23 and 2026-04-24, the only two routine-run days of the week. No trading-skill rules yet — only operational and epistemic hygiene.*

### Execution Patterns

- [W1|HIGH] When multiple files disagree on a date or config value, treat `state/experiment-config.json` as authoritative. `state/last-session.md` is a handoff note, not config — do not rely on it for hard dates (experiment start, end, capital, week number). Flag the discrepancy in the current journal and proceed with the config-file value.
  Source: 2026-04-23 pre-market journal corrected the prior session's "experiment starts 2026-04-28" against experiment-config.json's authoritative 2026-04-27.

- [W1|MEDIUM] Minor inter-session drift in continuous signals (e.g., RS_spread +2.72% → +2.58%, SMA a few cents) is data refresh, not a contradiction. Only escalate to a contradiction check if the signal crosses a decision threshold (0% for RS entry, −1% for RS exit warning, 3% for high-conviction). Acknowledge the drift in one line and move on; do not re-derive the prior intent.
  Source: 2026-04-24 pre-market journal handled QQQ RS_spread drift from +2.72% (4/23) to +2.58% (4/24) correctly as "rounding/data refresh" without escalating as a contradiction.

### Market Regime Awareness

- [W1|MEDIUM] When `get_bars <TICKER> 20` returns fewer than 20 bars, compute SMA on what is available and **label the proxy explicitly in the signal table** (e.g., write `SMA_14`, not `SMA_20`). Do not silently substitute. On the first session where ≥20 bars are returned for a ticker, switch to full SMA_20 immediately and note the switch in that day's pre-market journal. If the close is within ~2% of the proxy SMA, treat the trend signal as BORDERLINE and prefer not to open a new position on proxy data alone.
  Source: 2026-04-23 and 2026-04-24 pre-market journals both used SMA_14 as an SMA_20 proxy because `get_bars` returned only 14 bars; trend signal was robust because close was >> SMA, but the proxy was correctly labeled and not silently assumed equivalent.

### Behavioral Failure Modes

- [W1|HIGH] `tools/send_email.py` is unreliable — it failed in all 6 routine runs this week across three distinct error modes (IPv6, smtplib compat, missing SendGrid key). Treat email delivery as a best-effort non-blocking side channel: attempt once at the end of the routine, log any failure to `notes-for-operator.md`, and continue. Never retry email within the same routine, never block journal writing / state updates / git commit on email success, and never create an `operator-flag` in the weekly journal solely for email failure.
  Source: `notes-for-operator.md` entries on 2026-04-23 (×3) and 2026-04-24 (×3) document 6 consecutive email failures; every routine nonetheless committed successfully.

---

*Week 1 (experiment) lessons added 2026-05-02 by weekly-review routine*

### Sizing and Risk

- [W1|MEDIUM] Overnight gaps can cause hard stop fills significantly worse than the stop price. When a position's RS_spread turns negative in session 1 (first NEGATIVE flag), consider proactively trimming toward a lower conviction tier rather than holding full size through the 2-session exit confirmation. The 2-session rule protects against false exits, but does not protect against overnight gap risk on deteriorating names.
  Source: META triggered hard stop at pre-open $609.18 on 4/30 (prior close ~$669, stop $621.86) — a $60 overnight gap resulting in −10.62% realized loss instead of the intended −8% maximum cap.

- [W1|MEDIUM] When adding shares to a position that currently has an ACTIVE trailing stop, document explicitly in the sizing rationale that the add will DEACTIVATE the trailing stop (avg_entry rises → trailing threshold rises above current high_close). State whether you accept losing the trailing protection given current position size and signals. For positions >10% of equity, this deactivation is a meaningful risk increase.
  Source: 5/1 GOOGL add from 1.44→3.41 shares raised avg_entry $346.55→$366.98, moving trailing activation threshold from $381.21 to $403.68 — deactivating an active trailing stop on a 13% position.

### Behavioral Failure Modes

- [W1|HIGH] Always document the actual model used in each journal header. Any model is acceptable for any routine (operator policy 2026-05-03: model flexibility allowed). Never suppress model identity — the operator tracks behavioral consistency across models. Do NOT write a notes-for-operator.md entry solely for a model difference; just log it in the header.
  Source: 5 of 10 routine sessions this week ran under "opencode/hy3-preview-free" instead of claude-sonnet-4-6; deviation was only discoverable via journal headers. Operator subsequently approved open model policy.

---

*Week 2 lessons added 2026-05-09 by weekly-review routine*

### Execution Patterns

- [W2|HIGH] Alpaca does NOT support GTC stop orders for fractional-share positions. All stop enforcement for any fractional-share position is manual and must occur at every routine. This is a persistent platform constraint, not a transient tool error. When checking stops, verify whether stop_order_id is present in position-highs.json — if absent, enforce manually using avg_entry × 0.92. Do not log a notes-for-operator.md entry for each failure after the first week — the failure is known and expected until operator fixes the tool.
  Source: 10+ consecutive stop order placement failures across all fractional positions (AAPL, AMZN, GOOGL, LLY, QQQ, NVDA) throughout Weeks 1–2; only whole-share positions (XLE) had functioning standing stop orders.

- [W2|MEDIUM] When a held position shows RS_spread in the NEUTRAL zone [−1%, 0%] at mid-session, classify as WATCH — do NOT apply the RS session-1 trim rule, which triggers only at NEGATIVE (RS < −1%). Mid-session NEUTRAL is frequently an intraday artifact. Require EOD confirmation before escalating to NEGATIVE flag. This prevents false trims on recoverable positions.
  Source: 5/8 mid-session LLY RS_spread −0.215% correctly classified as WATCH (NEUTRAL, not NEGATIVE); EOD recovered to +3.994%. False trim avoided.

### Market Regime Awareness

- [W2|MEDIUM] When regime confirms BULL (≥8/12 universe tickers BULLISH) and multiple held positions are undersized for their conviction tier, scale ALL eligible undersized positions in that SAME session. Do not spread scaling across 3–4 sessions. The BULL regime cash target (10–25%) is a binding constraint: document explicitly why each undersized position is not scaled if cash remains > 35% in the first BULL session. Silent cash accumulation in a confirmed BULL regime is a sizing error regardless of how many qualifying sessions the agent waits for.
  Source: Cash was 43.6% after regime confirmed BULL on 5/7 (Day 1 of BULL). Only QQQ add executed; residual cash 38.85% through Friday. Primary driver of −1.808 pp weekly underperformance vs SPY (+2.368%).

- [W2|MEDIUM] When holding a commodity ETF (XLE, energy/commodity ETFs) and news confirms a macro catalyst reversal (oil price drop, geopolitical risk premium unwinding), treat the news as a secondary signal that front-runs the likely technical trend break. Monitor intraday more closely; if intraday close drops below SMA at mid-session, execute trend-break sell immediately rather than waiting for EOD confirmation. News does not override signals, but reduces false-exit risk when trend is also breaking.
  Source: 5/5 pre-market news confirmed oil price decline and Iran ceasefire talks; XLE dropped from $59.45 to $57.14 pre-market. 5/6 mid-session close $56.935 < SMA_14 $57.440 — sold immediately. Correct call; 5/7–5/8 prices confirmed further decline ($56.98, $55.96).

<!-- LEARNED_BEHAVIORS:END -->

---

*Do not re-read INSTRUCTIONS.md during routines. This file is the operational truth.*
