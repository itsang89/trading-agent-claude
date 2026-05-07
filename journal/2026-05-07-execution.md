# Market-Open Execution — 2026-05-07 (Experiment Day 9)
**Routine:** market-open-execution
**Model:** claude-sonnet-4-6
**Time (ET):** ~9:47 AM ET
**Week number:** 2

---

## Pre-Execution State
- Equity: $10,056.60 | Cash: $4,394.12 (43.7%) | Positions: 5
- Regime: BULL (8/12 BULLISH)

---

## Orders Placed

| Ticker | Side | Qty | Type | Order ID | Fill Est. | Conviction Tier | % Equity |
|--------|------|-----|------|----------|-----------|-----------------|---------|
| QQQ | BUY (ADD) | 0.70 | market | e4fa7017-33a6-403f-8fcf-d8856112e023 | ~$696 | High | ~10.0% |

**QQQ sizing rationale (≥10% position):**
Position was 5.19% (0.75 shares) — significantly below High tier target of 8–13%. RS +3.02% (High tier), vol_ratio 1.16, regime BULL. Bringing to ~10.04% is the floor of the High tier range, not an aggressive overweight. BULL regime shift (day 1) reinforces broad market ETF exposure. Add brings avg_entry from $661.814 → $678.381, hard stop from $608.87 → $624.11. High_close $695.62 unchanged (above new avg_entry; trailing threshold now $746.15, inactive).

---

## Orders Rejected
None.

---

## Buy Intents Aborted

| Ticker | Reason |
|--------|--------|
| GOOGL | Conditional gate not met. Required price ≥ $401.81 at 9:45 AM. Actual ask: $397.42. SMA_13 check passed ($397.42 > $360.22) but price-momentum condition unmet. HOLD. |

---

## Stop-Loss Actions
None. Stop-loss audit (9:45 AM):

| Ticker | Current Price | Hard Stop | Trailing Stop | Effective Stop | Status |
|--------|--------------|-----------|---------------|----------------|--------|
| AAPL | $289.44 | $252.20 | Inactive (<$301.30) | $252.20 | PASS |
| AMZN | $274.09 | $245.39 | Inactive (<$293.41) | $245.39 | PASS |
| GOOGL | $397.34 | $343.44 | Inactive (<$410.63) | $343.44 | PASS |
| LLY | $978.85 | $908.44 | Inactive (<$1,086.18) | $908.44 | PASS |
| QQQ | $695.66→$696.12 | $624.11* | Inactive (<$746.15) | $624.11 | PASS |

*QQQ hard stop updated post-add from $608.87 → $624.11.

All stop orders manual (fractional GTC error persists — notes-for-operator.md).

---

## Winner Trims
None. No position exceeded 25% of equity.

---

## Post-Execution State

| Ticker | Qty | Avg Entry | Hard Stop | % Equity |
|--------|-----|-----------|-----------|---------|
| AAPL | 2.86 | $273.908 | $252.20 | 8.23% |
| AMZN | 4.76 | $266.733 | $245.39 | 12.97% |
| GOOGL | 4.32 | $373.299 | $343.44 | 17.07% |
| LLY | 1.32 | $987.435 | $908.44 | 12.85% |
| QQQ | 1.45 | $678.381 | $624.11 | 10.04% |

- Equity: $10,056.14 | Cash: $3,906.83 (38.85%) | Positions: 5
- Cumulative: agent +0.561% vs SPY ~+2.6% (pre-market reference) → delta ~−2.04 pp (agent trailing)

---

## Errors / Flags
- **STOP ORDER FAILURE (QQQ):** `place_stop_order.py QQQ 1.45 624.11` returned `placed: false` — same fractional-order DAY error as prior sessions. Logged to notes-for-operator.md. Manual hard stop $624.11.
- GOOGL: pre-market $401.51 / 9:45 AM $397.42 — conditional gate NOT met. Watching for price ≥ $401.81 intraday. Will flag at mid-session if conditions change.
- AMZN RS_MOMENTUM_DECAY: active, no add.
