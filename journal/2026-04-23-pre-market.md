# Pre-Market Research — 2026-04-23

**Routine:** pre-market-research  
**Time:** 8:30 AM ET (executed ~10:54 AM ET)  
**Week:** 1 (experiment start: 2026-04-27)

---

## Portfolio State

- Equity: $10,000.00 | Cash: $10,000.00 (100%) | Positions: 0
- Cumulative return vs SPY: N/A — experiment not yet started (start date: 2026-04-27)
- SPY current price: $711.42 | Benchmark start price: not set (experiment_started: false)

---

## Stop-Loss Status

- No positions held. No stop-loss checks required.

---

## Market Read

- Market: OPEN (no early close)
- SPY: BULLISH. Close $711.42 above SMA_14 $691.45. 10d momentum +4.64%.
- Broad trend is constructive. SPY has been in uptrend for the entire available data window (Apr 6–23).
- Note: only 14 bars returned for 20-day request. SMA computed on 14 bars (SMA_14 proxy). Trend signal robust given close is $19.97 above SMA.
- No macro data reviewed (Week 1: price/technical data only per CLAUDE.md).

---

## Signal Table

| Ticker | SMA_14 | Close | Trend | 10d_ROC | RS_spread | Action |
|---|---|---|---|---|---|---|
| SPY | $691.45 | $711.42 | BULLISH | +4.64% | 0.00% | BENCHMARK ONLY |
| QQQ | $626.98 | $654.92 | BULLISH | +7.36% | +2.72% | BUY INTENT |

- SMA_14 used as proxy for SMA_20 (only 14 bars returned by get_bars).
- QQQ RS_spread = +2.72% → POSITIVE. Trend = BULLISH. Entry criteria satisfied.
- RS_spread 2.72% < 3%: standard sizing (not high-conviction).

---

## Intents

**QQQ — BUY — 5% of equity — $500 notional**
- Rationale: Trend BULLISH + RS POSITIVE. Satisfies all Week-1 entry criteria.
- Sizing: default 5% ($500). RS_spread 2.72% < 3% → no high-conviction upsize.
- Share quantity at $654.92: ~0.76 shares (fractional). Confirm Alpaca fractional support at execution.
- Condition: only execute on 2026-04-27 (experiment start). Do NOT execute before then.
- If QQQ signals degrade by Monday (Trend BEARISH or RS NEGATIVE), hold cash.

**Cash target:** ≥25% after entry. Post-buy: ($10,000 − $500) / $10,000 = 95% cash. Well above floor.

---

## Carry-Forward from Last Session (last-session.md, 2026-04-22)

- Prior context: build phase, no positions, no prior trades.
- Prior note said experiment starts "Monday 2026-04-28" — corrected: experiment-config.json shows start_date 2026-04-27 (Monday).
- No contradictions to resolve. First live pre-market run.

---

## Week-1 First Run Actions

- Universe proposal written to `universe-proposal.md`. 12 tickers, 6 GICS sectors, 3 ETFs.
- Operator must review and lock `state/universe.json` before Week 2.

---

## Notes

- Experiment has not officially started (experiment_started: false, start_date: 2026-04-27).
- Pre-market routine triggered on 2026-04-23 (Thursday, 4 days before start).
- No orders placed today — execution routine should only run from 2026-04-27 onward.
- All signals valid and constructive for Monday entry if conditions hold.
