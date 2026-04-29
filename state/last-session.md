# Last Session Summary

**Written by:** market-open-execution
**Date:** 2026-04-29 (Wednesday — Experiment Day 3)
**Time (ET):** ~11:21 AM ET
**Week number:** 1

---

## Portfolio State (post-execution, live from Alpaca)

- Equity: $10,015.43
- Cash: $6,022.05 (~60.1%)
- Positions held: 7
- Cumulative return: +0.15% vs SPY −0.49% from the morning benchmark snapshot

## Executed Orders

1. MSFT buy 1.17 market
   Order ID: `85f78a7a-e9f2-4a0c-988a-4e84c938cfa7`
   Result: position increased from 1.18 to 2.35 shares; new avg entry = $422.195234
2. AAPL buy 1.86 market
   Order ID: `50c072e9-7b70-4f05-94fc-c0a8801ed377`
   Result: new position opened at 1.86 shares; avg entry = $268.81

## Open Positions (live prices after execution)

| Ticker | Qty | Avg Entry | Current Price | Market Value | Unrlzd P&L | Hard Stop |
|--------|-----|-----------|---------------|--------------|------------|-----------|
| AAPL | 1.86 | $268.81 | $268.75 | $499.88 | −$0.11 | $247.31 |
| AMZN | 1.91 | $260.99 | $263.47 | $503.23 | +$4.74 | $240.11 |
| GOOGL | 1.44 | $346.55 | $351.85 | $506.66 | +$7.63 | $318.83 |
| META | 0.73 | $675.94 | $670.09 | $489.17 | −$4.27 | $621.86 |
| MSFT | 2.35 | $422.20 | $424.52 | $997.62 | +$5.46 | $388.42 |
| NVDA | 2.38 | $209.45 | $210.86 | $501.85 | +$3.36 | $192.69 |
| QQQ | 0.75 | $661.81 | $659.84 | $494.88 | −$1.48 | $608.87 |

## RS_spread Carry-Forward (for EOD decay tracking)

Intraday execution did not refresh bar history; carry forward the 2026-04-29 pre-market RS values until EOD recomputation.

| Ticker | RS_spread | Prior | Trend | Counter |
|--------|-----------|-------|-------|---------|
| AAPL | +2.15% | n/a | New position | 0 |
| AMZN | +1.78% | +4.54% | Declining | 0 |
| GOOGL | +2.58% | +4.76% | Declining | 0 |
| META | −1.15% | +2.63% | RS NEGATIVE | 1 |
| MSFT | +6.76% | +6.32% | Improving | 0 |
| NVDA | +5.98% | +10.18% | Declining | 0 |
| QQQ | +2.12% | +3.35% | Declining | 0 |

## Regime

- BULL — 10/12 universe tickers BULLISH from the 2026-04-29 pre-market scan
- Cash remains above the soft 10% minimum after adding risk

## Trailing Stop State

- No trailing stops active.
- `state/position-highs.json` updated:
  - MSFT `entry_price` reset to $422.195234; `high_close` kept at $429.40
  - AAPL initialized with `high_close = entry_price = $268.81`

## Carry-Forward Context for EOD

1. Recompute RS_spread for all 7 holdings at EOD; META remains the key watch item with counter = 1 and requires another RS < −1% reading to trigger next-execution soft exit.
2. Confirm whether AAPL and MSFT closes set new `high_close` values for trailing-stop maintenance.
3. No stop-losses, no winner trims, and no guardrail rejections during execution.

## Open Contradictions

None.
