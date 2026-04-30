# Pre-Market Research — 2026-04-30 (Experiment Day 4)

**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:21 AM ET
**Experiment status:** Day 4 of 20 (ends 2026-05-22)

---

## Regime

- **BULL — 9/12 universe tickers BULLISH**
- Bullish: QQQ, XLE, NVDA, MSFT, AAPL, GOOGL, META, BRK.B, AMZN
- Bearish: XLV, LLY, JPM
- Bull regime (>=8/12): stay aggressive, but prioritize strongest RS and avoid adding to RS-deteriorating names.

## Portfolio State

- **Equity:** $10,022.16 | **Cash:** $6,022.05 (60.09%) | **Positions:** 7
- **Cumulative agent return:** +0.22% (vs $10,000 notional)
- **SPY cumulative:** -0.50%
- **Delta vs SPY:** +0.72 pp

## Stop-Loss Status

Using live pre-open prices from `state/positions.json` and trailing-stop state from `state/position-highs.json`.

| Ticker | Avg Entry | Current | Hard Stop | Trailing Active | Effective Stop | Status |
|--------|-----------|---------|-----------|-----------------|----------------|--------|
| AAPL | $268.81 | $271.61 | $247.31 | No | $247.31 | PASS |
| AMZN | $260.99 | $272.90 | $240.11 | No | $240.11 | PASS |
| GOOGL | $346.55 | $377.54 | $318.83 | No | $318.83 | PASS |
| META | $675.94 | $609.18 | $621.86 | No | $621.86 | **QUEUE SELL** |
| MSFT | $422.20 | $418.40 | $388.42 | No | $388.42 | PASS |
| NVDA | $209.45 | $210.95 | $192.69 | No | $192.69 | PASS |
| QQQ | $661.81 | $666.31 | $608.87 | No | $608.87 | PASS |

- **META hard stop triggered:** current $609.18 < effective stop $621.86. Queue market-sell for next execution.
- Warning zone: `META` only (also below hard stop).
- No trailing stops active.

## Data Notes

- `get_bars <TICKER> 20` returned **13 bars** (2026-04-13 -> 2026-04-29) for the universe and SPY. Using **SMA_13** proxy and labeling it explicitly per learned behavior.
- SPY benchmark for signal math: **10d_ROC +1.69%**, close $711.59, SMA_13 $705.88, vol_ratio 0.70.
- `state/experiment-config.json` remains authoritative: **week 1**, experiment window **2026-04-27 -> 2026-05-22**.

## Signal Table

| Ticker | SMA_N | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|-------|-------|-------|---------|-----------|-----------|------------|--------|
| QQQ | SMA_13 $647.47 | $661.59 | BULLISH | +3.82% | +2.13% | 0.86 | Standard | HOLD |
| XLV | SMA_13 $146.16 | $142.82 | BEARISH | -3.36% | -5.05% | 1.34 | — | NO ENTRY |
| XLE | SMA_13 $56.56 | $59.06 | BULLISH | +5.91% | +4.22% | 0.81 | High | **BUY** |
| NVDA | SMA_13 $202.75 | $209.35 | BULLISH | +5.28% | +3.59% | 1.06 | High | HOLD |
| MSFT | SMA_13 $417.38 | $424.80 | BULLISH | +3.28% | +1.59% | 0.93 | Standard | HOLD |
| AAPL | SMA_13 $267.93 | $270.15 | BULLISH | +1.44% | -0.25% | 0.59 | — | HOLD |
| GOOGL | SMA_13 $339.36 | $350.27 | BULLISH | +3.90% | +2.21% | 1.24 | Standard | HOLD |
| META | SMA_13 $669.38 | $669.47 | BULLISH | -0.32% | -2.02% | 1.43 | — | **SELL** |
| LLY | SMA_13 $902.15 | $851.48 | BEARISH | -5.96% | -7.66% | 1.28 | — | NO ENTRY |
| JPM | SMA_13 $311.24 | $309.25 | BEARISH | +1.11% | -0.59% | 0.76 | — | NO ENTRY |
| BRK.B | SMA_13 $473.35 | $475.44 | BULLISH | +0.30% | -1.39% | 0.68 | — | NO ENTRY |
| AMZN | SMA_13 $253.40 | $263.22 | BULLISH | +5.94% | +4.25% | 1.57 | High | **ADD** |

## RS / Decay Notes

- **META**: RS_spread < -1% for a second consecutive session (-1.15% -> -2.02%). Soft-exit rule confirmed, but hard stop now has higher priority.
- **GOOGL**: RS DETERIORATING — 4.76% -> 2.58% -> 2.21%. Do not add. Be ready to exit on first signal failure.
- **NVDA**: RS DETERIORATING — 10.18% -> 5.98% -> 3.59%. Do not add. Be ready to exit on first signal failure.
- `AAPL` RS is neutral (-0.25%), but not below the -1% exit threshold. Hold, no add.

## Intents

| # | Ticker | Action | Conviction | Target Size | Rationale |
|---|--------|--------|------------|-------------|-----------|
| 1 | META | **SELL** | — | 0% | Hard stop triggered pre-open: current $609.18 < stop $621.86. Also RS negative for 2 straight sessions (-1.15% -> -2.02%). Highest-priority exit. |
| 2 | AMZN | **ADD** | High | **8%** | Strongest held RS_spread (+4.25%), BULLISH trend, volume_ratio 1.57, and +1.35% day confirms strength. Bull regime and 60% cash support scaling from ~5% toward the low end of the 8-13% High tier. |
| 3 | XLE | **BUY** | High | **8%** | Best non-held eligible name by RS after AMZN (+4.22%), BULLISH trend, +2.30% day. Volume_ratio 0.81 argues for the low end of the High tier rather than a larger starter. Adds sector diversification. |
| 4 | NVDA | HOLD / NO ADD | High | ~5% hold | RS still positive, but 3-session decay (10.18% -> 5.98% -> 3.59%) and a -1.78% day say do not press size here. Hold until first signal failure. |
| 5 | GOOGL | HOLD / NO ADD | Standard | ~5% hold | Trend and RS stay positive, but 3-session RS decay (4.76% -> 2.58% -> 2.21%) overrides the healthy volume_ratio. Hold, do not add. |
| 6 | QQQ | HOLD | Standard | ~5% hold | Trend BULLISH, RS +2.13%, stable vs prior session (+2.12%). No need to resize with stronger opportunities elsewhere. |
| 7 | MSFT | HOLD | Standard | ~10% hold | Prior add already brought size near target. RS remains positive (+1.59%) but materially weaker than yesterday's +6.76%; no fresh add. |
| 8 | AAPL | HOLD / WATCH | — | ~5% hold | Trend BULLISH, but RS slipped to neutral (-0.25%) and volume_ratio is weak (0.59). No add until RS turns positive again. |
| 9 | XLV / LLY / JPM / BRK.B | NO ENTRY | — | — | XLV, LLY, and JPM fail trend; BRK.B fails RS with -1.39% spread despite a bullish trend. Skip. |

## Carry-Forward from Last Session

- **Resolved:** yesterday's `META` soft-exit intent is now upgraded to a **hard-stop sell** because live pre-open price breached the 8% stop.
- **Confirmed:** `GOOGL` and `NVDA` remain RS-deteriorating names. Keep them in hold/no-add status until a stronger signal reset appears.
- **No contradiction:** yesterday's `AAPL` buy and `MSFT` add remain valid holdings; only `AAPL` has cooled from positive RS to neutral, so the posture shifts from add-capable to hold-only.

## Errors / Flags

- None. All required tools completed successfully after the operator-directed Step 0 skip.
