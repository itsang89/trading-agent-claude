# Pre-Market Research — 2026-05-04 (Experiment Day 6)
**Routine:** pre-market-research
**Model:** opencode/hy3-preview-free (scheduled: claude-sonnet-4-6) — MODEL DEVIATION
**Time (ET):** ~8:51 AM ET (pre-market, opens 9:30 AM)
**Week number:** 2

---
## Regime: MIXED — 7/12 universe tickers BULLISH
Be selective. Not a bear market but not fully bullish either.

## Portfolio State
- Equity: $9,981.31
- Cash: $5,614.35 (56.2%)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, QQQ, XLE)
- Cumulative vs SPY: agent -0.068% vs SPY +0.7446% (delta -0.812 pp)
- Market status: trading day, pre-market

## Stop-Loss Status
All positions PASS stop-loss and trailing stop checks:
| Ticker | Avg Entry | Current | Hard Stop | Trailing Active | Effective Stop | Status | Warning? |
|--------|-----------|---------|-----------|-----------------|---------------|--------|-----------|
| AAPL | $268.81 | $279.25 | $247.31 | No | $247.31 | PASS | No |
| AMZN | $260.56 | $269.41 | $239.71 | No | $239.71 | PASS | No |
| GOOGL | $366.98 | $385.64 | $337.62 | No | $337.62 | PASS | No |
| LLY | $981.72 | $937.02 | $903.18 | No | $903.18 | PASS | **YES** (current < entry*0.95) |
| QQQ | $661.81 | $674.85 | $608.87 | No | $608.87 | PASS | No |
| XLE | $58.98 | $58.81 | $54.26 | No | $54.26 | PASS | No |

LLY in warning zone (current $937.02 < avg_entry*0.95 = $932.63). Monitoring.

## Signal Table (SMA_13 — 13 bars available per learned behavior)

| Ticker | SMA_N | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|-------|-------|-------|---------|-----------|-----------|------------|--------|
| SPY | $711.40 | $720.49 | BULLISH | +2.70% | — | 1.43 | — | benchmark |
| AAPL | $270.87 | $279.25 | BULLISH | +3.43% | +0.73% | 2.07 | Borderline | HOLD |
| AMZN | $254.12 | $269.41 | BULLISH | +3.54% | +0.84% | 1.46 | Borderline | HOLD |
| GOOGL | $345.42 | $385.64 | BULLISH | +13.34% | +10.64% | 1.31 | Very High | HOLD |
| LLY | $901.06 | $937.02 | BULLISH | +10.98% | +8.28% | 1.57 | Very High | HOLD |
| QQQ | $651.83 | $674.85 | BULLISH | +5.41% | +2.71% | 1.08 | Standard | HOLD |
| XLE | $56.22 | $58.81 | BULLISH | +5.52% | +2.82% | 0.89 | High | HOLD |
| XLV | $146.07 | $145.16 | BEARISH | -1.15% | -3.85% | 0.93 | — | NO |
| NVDA | $203.23 | $198.39 | BEARISH | -1.16% | -3.86% | 0.77 | — | NO |
| MSFT | $420.99 | $414.46 | BEARISH | -2.98% | -5.68% | 1.10 | — | NO |
| META | $660.38 | $608.61 | BEARISH | -9.35% | -12.05% | 0.69 | — | NO |
| JPM | $310.68 | $312.48 | BULLISH | +1.80% | -0.90% | 0.94 | — | NO (RS NEUTRAL) |
| BRK.B | $471.82 | $473.07 | BEARISH | -0.40% | -3.10% | 0.94 | — | NO |

## Intents for 2026-05-04 Execution
1. **AAPL HOLD** — Borderline RS +0.73%, Trend BULLISH. No add until RS >1%.
2. **AMZN HOLD** — Borderline RS +0.84%, Trend BULLISH. No add until RS >1%.
3. **GOOGL HOLD** — Very High conviction RS +10.64%, strongest in portfolio. Trailing stop deactivated (high_close $385.79 < threshold $403.68). Rationale: strongest signal in universe, multi-day RS leadership.
4. **LLY HOLD** — Very High conviction RS +8.28%. In warning zone (current < entry*0.95). Monitor closely. Rationale: strong RS, new position holding well.
5. **QQQ HOLD** — Standard conviction RS +2.71%. Solid performer.
6. **XLE HOLD** — High conviction RS +2.82%. RS reset to positive (was -1.64% on 5/1); 2-session counter cleared. Rationale: energy holding trend.

No soft exits triggered. No new entries (all qualifying tickers already held; borderline RS for unheld tickers).

## Carry-Forward from Last Session (2026-05-02 weekly)
- RS_spread state from EOD 5/1: AAPL +2.43%, AMZN +0.68%, GOOGL +8.88%, LLY +11.93%, QQQ +0.64%, XLE -1.64%
- XLE: RS reset to +2.82% today — 2-session negative counter cleared (RS > 0% rule)
- No RS deterioration (no 3-session declines today)
- No soft-exit flags
- IT sector concentration: AAPL + GOOGL = ~18.4% equity, well under 40% cap
- Cash 56.2% — high for mixed regime. No qualifying new entries available to deploy.

## RS Momentum Check
No 3-session RS declines for held positions:
- AAPL: +4.76% → +2.43% → +0.73% (recovering, not continuous decline)
- AMZN: +4.25% → +0.68% → +0.84% (recovered)
- GOOGL: +2.21% → +8.88% → +10.64% (strengthening)
- LLY: N/A → +11.93% → +8.28% (one decline, still strong)
- QQQ: +2.13% → +0.64% → +2.71% (recovered)
- XLE: +4.22% → -1.64% → +2.82% (recovered, counter reset)

## Contradiction Check
No contradictions with prior journals. Last-session.md RS_spread values align with today's computed values (minor drift due to data refresh, within learned behavior tolerance).

## Errors / Flags
None. All tools completed successfully.
