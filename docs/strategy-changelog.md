# Strategy Changelog

Append-only record of operator-authorized design changes. Each entry: date, what changed, why.

---

## 2026-04-28 — Full Strategy Redesign (Operator Session)

**Authorized by:** Operator (Isaac). All changes in this entry are operator-directed.

### Constraint Removals

The following hard limits were removed from both `CLAUDE.md` and `tools/lib/validator.py`:

| Removed constraint | Old value | Reason for removal |
|---|---|---|
| MAX_POSITION_SIZE | 10% of equity | Too restrictive for high-conviction names; capped upside |
| MIN_CASH_RESERVE | 20% | Created structural drag; cash floor conflicts with concentration goal |
| MAX_POSITIONS | 8 concurrent positions | Arbitrary; concentration in fewer high-RS names is better strategy |
| MIN_POSITION_SIZE | 5% | Borderline entries at 3% are valid; floor excluded them |

Validator (`tools/lib/validator.py`) still enforces: universe whitelist, order types, no-trade windows (9:30–9:45 ET, 15:45–16:00 ET), sector concentration ≤40%.

### New: Conviction-Based Sizing Tiers (`state/strategy.md`)

Replaced fixed-% defaults with signal-strength tiers:

| Tier | Condition | Size range |
|---|---|---|
| Borderline | RS_spread 0–1% | 3–5% of equity |
| Standard | RS_spread 1–3% | 5–8% |
| High conviction | RS_spread 3–5% | 8–13% |
| Very high conviction | RS_spread >5% AND up >1% today | 13–20% |

Volume ratio (today vol / 20-day avg) used as secondary confidence signal: >1.2 supports upper end of tier, <0.8 supports lower end.

### New: Trailing Stop System

- File: `state/position-highs.json` (new) — tracks `high_close`, `entry_price`, `last_updated` per held ticker
- Logic:
  ```
  hard_stop_price     = avg_entry * 0.92
  trailing_active     = high_close > avg_entry * 1.10
  trailing_stop_price = high_close * 0.90 if trailing_active else 0
  effective_stop      = max(hard_stop_price, trailing_stop_price)
  ```
- Initialized 2026-04-28 with six current positions at avg_entry prices
- Checked every routine; maintained on open/add/close events

### New: Mid-Session-Check Routine

- File: `prompts/mid-session-check.md` (new)
- Schedule: 1:30 PM ET, Mon–Fri (`make run-midsession`)
- Purpose: intraday risk management only — trailing stops, trend breaks, RS 2-session confirmation sells
- Does NOT place buy orders (entries are execution-only at 9:45 AM)
- EOD routine (4:30 PM) is after market close; soft exits flagged at EOD are queued for the following morning — mid-session is the only routine that can actually execute same-day sells

**User action required:** add cron entry:
```
30 13 * * 1-5 cd "/Users/isaac/VibeCode/AI Agent/Trading-agent-claude" && make run-midsession >> logs/midsession.log 2>&1
```
Adjust hour for local timezone (13 = ET, 10 = PT, 12 = CST).

### RS Counter Reset Fix

- Old: RS counter reset when RS_spread > −1%
- New: RS counter reset ONLY when RS_spread > 0% (genuine positive performance)
- Rationale: old rule allowed underperformers at RS −0.8% to indefinitely escape the 2-session exit trigger

### RS Momentum Decay Tracking (new signal)

3-session declining RS_spread (even if still positive) triggers `RS_MOMENTUM_DECAY` flag — do not add shares; be ready to exit at first signal failure. Tracked in `logs/behavioral-flags.jsonl`.

### Re-Entry Rule (new)

Tickers exited in the last 5 sessions must re-enter at borderline tier (3–5%) regardless of RS_spread. After 2 sessions of confirmed signals, may scale to full conviction tier. Prevents chasing re-entries that happened to spike.

### Regime-Based Cash Targets

| Regime | Universe tickers BULLISH | Cash target |
|---|---|---|
| Bull | ≥8/12 | 10–25% |
| Mixed | 5–7/12 | 25–40% |
| Bear | <5/12 | 50%+ |

### Signal Re-Validation at Execution (new step)

Before executing buy intents at 9:45 AM, pull live quote and abort if `current_price < pre-market SMA`. Pre-market analysis at 8:30 AM may be stale by open; prevents buying into a trend that already broke.

### Winner Trim Check (new step in execution)

If any position exceeds 25% of portfolio (due to price appreciation), trim back to ~20%. Prevents a single winner from creating outsized concentration risk.

### Weekly-Review Model Updated

- Old: `claude-opus-4-6`
- New: `claude-opus-4-7`
- Updated in: `Makefile`, `CLAUDE.md`, `state/experiment-config.json`

### News Unlock Date

News tools blocked until 2026-05-05. From that date, macro calendar and earnings dates permitted for timing decisions. Price/technical signals remain primary.

### Files Changed in This Session

| File | Change type |
|---|---|
| `CLAUDE.md` | Multiple section updates (strategy, hard limits, routines, memory layout, behavioral rules) |
| `MEMORY.md` | Added position-highs.json docs, trailing stop flag types, mid-session column |
| `Makefile` | Added run-midsession target; fixed weekly model |
| `state/strategy.md` | Full rewrite |
| `state/position-highs.json` | New file |
| `state/experiment-config.json` | model_weekly updated |
| `tools/lib/validator.py` | Removed 3 constraint checks |
| `prompts/pre-market-research.md` | Full rewrite |
| `prompts/market-open-execution.md` | Full rewrite |
| `prompts/end-of-day-review.md` | Rewrite |
| `prompts/mid-session-check.md` | New file |
