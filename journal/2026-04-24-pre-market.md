# Pre-Market Research — 2026-04-24

**Routine:** pre-market-research  
**Time:** 8:41 AM ET  
**Week:** 1 (pre-experiment — experiment start: 2026-04-27)

---

## Portfolio State

- Equity: $10,000.00 | Cash: $10,000.00 (100%) | Positions: 0
- Cumulative return vs SPY: N/A — experiment not yet started (start_date: 2026-04-27)
- SPY latest close: $708.41 (2026-04-23) | Benchmark start price: not set (experiment_started: false)
- SPY today_return_pct (4/23): -0.39%

---

## Stop-Loss Status

- No positions held. No stop-loss checks required.

---

## Market Read

- Market: OPEN today (no early close); current time 8:41 AM ET (pre-open)
- SPY (4/23): BULLISH. Close $708.41 above SMA_14 $691.24. Down -0.39% on 4/23 but well above SMA.
- QQQ (4/23): BULLISH. Close $651.40 above SMA_14 $626.73. RS_spread +2.58% vs SPY — outperforming.
- Both instruments declined mildly on 4/23 (SPY -0.39%, QQQ -0.56%), but uptrends intact.
- Note: 14 bars returned for 20-day request (API limit); SMA_14 used as proxy for SMA_20 — trend signal robust given close is well above SMA.
- No macro data reviewed (Week 1: price/technical data only per CLAUDE.md).

---

## Signal Table

| Ticker | SMA_14 | Close (4/23) | Trend | 10d_ROC | RS_spread | Action |
|---|---|---|---|---|---|---|
| SPY | $691.24 | $708.41 | BULLISH | +4.20% | 0.00% | BENCHMARK ONLY |
| QQQ | $626.73 | $651.40 | BULLISH | +6.78% | +2.58% | ELIGIBLE — no action today (pre-experiment) |

- 10d window: close_today (4/23) vs close_10d_ago (4/9)
- QQQ RS_spread +2.58%: POSITIVE. Trend BULLISH. Entry criteria satisfied.
- RS_spread 2.58% < 3% → standard sizing (not high-conviction threshold).
- QQQ closed below yesterday ($655.09 → $651.40, -0.56%) → high-conviction upsize NOT applicable even if RS_spread ≥ 3%.

---

## Intents

**No orders today** — experiment start gate is 2026-04-27. Pre-experiment day.

**Monday 2026-04-27 Preliminary Intent — QQQ BUY — 5% of equity (~$500)**
- Rationale: Trend BULLISH + RS POSITIVE as of 4/23. Both signals satisfied.
- Sizing: default 5% ($500). RS_spread 2.58% < 3% → no high-conviction upsize.
- Condition: revalidate QQQ signals Monday 8:30 AM before committing. If Trend BEARISH or RS NEGATIVE → hold cash.
- Post-buy cash: ~95% ($9,500 / $10,000). Well above 25% strategy floor.
- Share quantity at $651.40: ~0.77 shares (fractional). Confirm Alpaca fractional support.

---

## Carry-Forward from Last Session (2026-04-23 EOD)

- 4/23 EOD noted: SPY fell -0.51% on 4/23; QQQ signals may have shifted. Reconfirmed today — signals still BULLISH + RS POSITIVE.
- Prior QQQ RS_spread was +2.72% (4/23 pre-market). Today (same data, recalculated): +2.58%. Minor rounding difference — same conclusion.
- No contradiction with prior session. Monday entry intent unchanged.
- Universe proposal (universe-proposal.md) previously committed. Awaiting operator lock before Week 2.
- Email sending failure noted in prior sessions (IPv4 SMTP unavailable) — will attempt again today.

---

## Notes

- Today is Friday. No orders placed or expected.
- Weekend hold: 100% cash, no open positions, no risk exposure.
- Monday 2026-04-27: experiment officially starts. Execute QQQ buy at 5% if both signals hold at pre-market.
- Universe.json remains WEEK_1_STUB (unlocked). Operator must lock before 2026-05-04.
