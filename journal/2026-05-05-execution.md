# Execution Journal — 2026-05-05 (Experiment Day 7)
**Routine:** market-open-execution
**Model:** claude-sonnet-4-6
**Time (ET):** ~9:47 AM ET
**Week:** 2

---

## Orders Placed

| Ticker | Side | Qty | Type | Order ID | Fill Est. | Conviction Tier | % Equity |
|--------|------|-----|------|----------|-----------|-----------------|----------|
| AMZN | BUY (ADD) | 1 | market | e80f2bd4-fc3a-4b8a-9a58-a50132077cb7 | ~$277.71 | Very High | ~10.8% post-fill |

## Orders Rejected
None.

## Buy Intents Aborted
None. AMZN signal re-validation: ask $277.71 > SMA_13 $258.63 → PASS.

## Stop-Loss Actions
None triggered. All positions pass:

| Ticker | Avg Entry | Hard Stop | Current | Trailing Active | Status |
|--------|-----------|-----------|---------|-----------------|--------|
| AAPL | $268.81 | $247.31 | $278.90 | No (threshold $295.69) | PASS |
| AMZN | $264.95* | $243.76* | $277.55 | No (threshold $291.45) | PASS |
| GOOGL | $366.98 | $337.62 | $391.20 | No (threshold $403.68) | PASS |
| LLY | $981.72 | $903.18 | $974.84 | No (threshold $1,079.89) | PASS |
| QQQ | $661.81 | $608.87 | $680.35 | No (threshold $727.99) | PASS |
| XLE | $58.98 | $54.26 | $59.28 | No (threshold $64.88) | PASS |

*Post-add values for AMZN.

## Winner Trims
None. No position exceeded 25% of equity.

## Sizing Rationale — AMZN (≥10% of equity)
- Pre-add: 2.91 shares, MV $807.67, 8.03% of equity. AMZN is Very High conviction (RS_spread +8.26%, Trend BULLISH).
- Very High tier target: 13–20% of equity. Floor = 13% × $10,055.64 = $1,307.23.
- Dollar add needed: $1,307.23 − $807.67 = $499.56. At ask $277.71 → floor(1.80) = 1 share.
- Post-add: 3.91 shares, est. MV $1,085.90, ~10.8% of equity — at tier floor.
- Catalyst: BNP Paribas PT $345, 50% AWS backlog surge, AI demand. 86 days to next earnings (no near-term event risk).
- No trailing stop to cancel or deactivate (high_close $272.10 < new threshold $291.45 — trailing never activated).
- AMZN add does NOT deactivate any active trailing stop (trailing was already inactive).

## Stop Order Note
- `place_stop_order.py AMZN 3.91 243.76` returned `placed: false` — error: `fractional orders must be DAY orders`.
- AMZN has NO standing stop order. Hard stop at $243.76 must be enforced manually each routine.
- Logged to notes-for-operator.md. position-highs.json updated without stop fields.

## Portfolio State Post-Execution
- Equity (pre-fill, from get_account): $10,055.64
- Cash pre-fill: $5,614.35 | Post-fill est.: ~$5,336.64 (~53.1% of equity)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, QQQ, XLE)

| Ticker | Qty | Avg Entry | MV | % Equity |
|--------|-----|-----------|-----|----------|
| AAPL | 1.86 | $268.81 | $518.75 | 5.16% |
| AMZN | 3.91 | $264.95 | $1,085.90 | 10.80% |
| GOOGL | 3.41 | $366.98 | $1,333.99 | 13.27% |
| LLY | 0.51 | $981.72 | $498.05 | 4.95% |
| QQQ | 0.75 | $661.81 | $510.26 | 5.07% |
| XLE | 13.0 | $58.98 | $770.64 | 7.67% |

## Regime
MIXED — 6/12 universe BULLISH. Selective adds to highest-conviction existing positions.
