# Execution Journal — 2026-05-06 (Experiment Day 8)
**Routine:** market-open-execution
**Model:** claude-sonnet-4-6
**Time (ET):** ~9:47 AM ET
**Week number:** 2

---

## Market Status
Open. No early close. Executed at 9:47 AM ET (past 9:30–9:45 no-trade window).

## Stop-Loss & Trailing Stop Audit (Step 6)

| Ticker | Avg Entry | Hard Stop | Current | Trailing Active | Status |
|--------|-----------|-----------|---------|-----------------|--------|
| AAPL | $268.81 | $247.31 | $282.72 | No | PASS |
| AMZN | $264.954 | $243.76 | $274.44 | No | PASS |
| GOOGL | $366.978 | $337.62 | $395.97 | No | PASS |
| LLY | $981.72 | $903.18 | $991.56 | No | PASS |
| QQQ | $661.814 | $608.87 | $689.97 | No | PASS |
| XLE | $59.02 | $54.30 | $57.57 | No | PASS |

No stops triggered.

## Winner Trim Check (Step 6b)
All positions below 25% of equity. No trims.

## Signal Re-Validation (Step 7)

| Ticker | Ask at 9:47 | SMA_13 | Condition | Decision |
|--------|-------------|--------|-----------|----------|
| LLY | $1,000.00 | $917.07 | ask > SMA | PROCEED |
| AAPL | $282.92 | $272.91 | ask > SMA | PROCEED |
| AMZN | $275.50 | $260.46 | ask > SMA | PROCEED |
| GOOGL | $396.93 | $355.90 | ask > SMA AND $396.93 > $392.29 conditional | PROCEED |

All intents confirmed. GOOGL conditional (price ≥ $392.29) met at $396.93.

---

## Orders Placed

| Ticker | Side | Qty | Type | Order ID | Fill Est. | Conviction | % Equity |
|--------|------|-----|------|----------|-----------|------------|----------|
| LLY | buy (add) | 0.81 | market | ead2dc16-48e9-4546-acc5-3fefe3cee48f | ~$990.97 | Very High | 13.0% post-add |
| AAPL | buy (add) | 1.0 | market | 5dba4dcd-389a-4dd5-9080-74c5f740bbee | ~$283.38 | High | 8.1% post-add |
| AMZN | buy (add) | 0.85 | market | bbbc5e67-9882-4ae4-9fdd-435ddaeafc02 | ~$274.92 | Very High | 13.0% post-add |
| GOOGL | buy (add) | 0.91 | market | db878e09-8f88-4e45-9bc3-724f38ec1476 | ~$397.04 | Very High | 17.0% post-add |

## Orders Rejected
None.

## Buy Intents Aborted
None. All 4 buy intents passed signal re-validation.

## Stop-Loss Actions
None triggered.

## Winner Trims
None.

---

## Sizing Rationale (positions ≥10% of equity)

**AMZN (13.0% post-add):** Very High conviction tier (RS +6.67%, Trend BULLISH). Add from 10.68% brings to tier floor (13%). Vol_ratio 0.84 — below 1.0 but above 0.8 threshold; no downgrade. No earnings 85+ days. Fundamentals strong (AWS/AI demand). No stop_order_id (fractional order limitation) — hard stop $245.39 manual enforcement.

**GOOGL (17.0% post-add):** Very High conviction tier (RS +14.07%, highest in universe). Conditional on price ≥ $392.29 at execution — confirmed at $396.93. Add from 13.41% to tier midpoint. Price +2.2% from prior close at execution. OpenAI talent departing to Google + new AI agent "Remy" — supportive news, not a sell catalyst. New trailing threshold $410.63 (inactive; high_close $388.41 < threshold). No stop_order_id (fractional limitation) — hard stop $343.44 manual enforcement.

**LLY (13.0% post-add):** Very High conviction tier (RS +6.66%, Trend BULLISH). Position was 5.03% (deeply undersized vs 13-20% tier). First-session RS decline flag from 5/5 AM fully resolved. Omvoh biologic data positive. Earnings 91 days out. Hard stop $908.44 manual enforcement.

---

## Stop Order Attempts Post-Add

All 4 stop orders failed with `{"code":42210000,"message":"fractional orders must be DAY orders"}`. Logged to notes-for-operator.md. position-highs.json updated without stop fields for AAPL/AMZN/GOOGL/LLY.

Manual hard stops (avg_entry × 0.92):
- AAPL: $252.20 | AMZN: $245.39 | GOOGL: $343.44 | LLY: $908.44
- XLE: $54.30 (stop_order_id 9c12ad6b — active)

---

## Final Confirmation Quotes

| Ticker | Ask at ~9:48 | vs Fill Est. |
|--------|-------------|-------------|
| LLY | $996.15 | +$5.18 above fill — within normal spread |
| AAPL | $284.27 | +$0.89 above fill — reasonable |
| AMZN | $275.04 | +$0.12 above fill — fine |
| GOOGL | $397.29 | +$0.25 above fill — fine |

All fills reasonable.

---

## Post-Execution Portfolio State

- **Equity:** $10,062.32
- **Cash:** $3,595.99 (35.7%)
- **Positions:** 6

| Ticker | Qty | New Avg Entry | Hard Stop | Trailing Threshold | % Equity |
|--------|-----|---------------|-----------|-------------------|---------|
| AAPL | 2.86 | $273.908 | $252.20 | >$301.30 (inactive) | 8.1% |
| AMZN | 4.76 | $266.733 | $245.39 | >$293.41 (inactive) | 13.0% |
| GOOGL | 4.32 | $373.299 | $343.44 | >$410.63 (inactive) | 17.0% |
| LLY | 1.32 | $987.435 | $908.44 | >$1,086.18 (inactive) | 13.0% |
| QQQ | 0.75 | $661.814 | $608.87 | >$727.99 (inactive) | 5.1% |
| XLE | 14.0 | $59.02 | $54.30 | >$64.92 (inactive) | 8.0% |

Cash target range (MIXED regime): 25–40%. Actual 35.7% — within target.

## XLE Carry-Forward
- Pre-market $57.14 < SMA_13 $57.48. Current $57.57 — slightly above SMA at execution time, but close.
- Do NOT add. Monitor EOD close vs SMA_13 $57.48.
- If EOD close < SMA_13 → flag Trend BEARISH → queue sell for 5/7 execution.
- stop_order_id: 9c12ad6b at $54.30 — active.
