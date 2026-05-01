# Mid-Session Check — 2026-04-30 (Experiment Day 4)

**Routine:** mid-session-check
**Model:** Hy3 preview Free  
**Time (ET):** ~1:30 PM ET
**Market:** Open, normal close 16:00 ET

---

## Positions Checked: 7 (pre-sell) → 5 (post-sell)

## Trailing Stops Checked


| Ticker | Avg Entry | Current | Hard Stop | Trailing Active | Effective Stop | Status                 |
| ------ | --------- | ------- | --------- | --------------- | -------------- | ---------------------- |
| AAPL   | $268.81   | $273.57 | $247.31   | No              | $247.31        | PASS                   |
| AMZN   | $260.56   | $259.90 | $239.71   | No              | $239.71        | PASS                   |
| GOOGL  | $346.55   | $383.01 | $318.83   | No              | $318.83        | PASS                   |
| MSFT   | $422.20   | $401.57 | $388.42   | No              | $388.42        | **SOLD — TREND BREAK** |
| NVDA   | $209.45   | $200.55 | $192.69   | No              | $192.69        | **SOLD — TREND BREAK** |
| QQQ    | $661.81   | $665.56 | $608.87   | No              | $608.87        | PASS                   |
| XLE    | $58.98    | $59.45  | $54.26    | No              | $54.26         | PASS                   |


## Signal Check (SMA_13, 14 bars available)


| Ticker | SMA_13  | Close   | Trend   | 10d_ROC | RS_spread | Action   |
| ------ | ------- | ------- | ------- | ------- | --------- | -------- |
| AAPL   | $267.96 | $273.74 | BULLISH | +3.96%  | +1.83%    | HOLD     |
| AMZN   | $254.19 | $259.88 | BULLISH | +4.08%  | +1.95%    | HOLD     |
| GOOGL  | $340.95 | $383.04 | BULLISH | +14.01% | +11.88%   | HOLD     |
| MSFT   | $418.70 | $401.55 | BEARISH | -4.42%  | -6.55%    | **SOLD** |
| NVDA   | $202.59 | $201.45 | BEARISH | +1.61%  | -0.52%    | **SOLD** |
| QQQ    | $648.29 | $665.93 | BULLISH | +3.98%  | +1.85%    | HOLD     |
| XLE    | $56.75  | $59.32  | BULLISH | +4.80%  | +2.67%    | HOLD     |


## Sells Executed


| Ticker | Reason                                                    | Qty  | Est Price | Order ID                             |
| ------ | --------------------------------------------------------- | ---- | --------- | ------------------------------------ |
| MSFT   | SOFT_EXIT_TREND_BREAK (BEARISH, SMA_13 $418.70 > $401.55) | 2.35 | ~$401.55  | 90f8af65-4c08-4ac8-b3b4-01529386e198 |
| NVDA   | SOFT_EXIT_TREND_BREAK (BEARISH, SMA_13 $202.59 > $201.45) | 2.38 | ~$200.55  | b4f8ace9-c9a4-4077-b91b-ea4cee9a7757 |


## Sells Aborted

None.

## RS First-Session Warnings

- **MSFT**: RS_spread -6.55% < -1% for the FIRST time today (was +1.59% at pre-market). Flag WATCH — if RS stays < -1% tomorrow, 2-session exit triggers.

## No Action

None — 2 positions sold via trend-break soft exit.

## Position-Highs.json Updates

- AAPL: updated high_close 270.15 → 273.74
- GOOGL: updated high_close 350.27 → 383.04
- QQQ: updated high_close 661.81 → 665.93
- XLE: updated high_close 59.01 → 59.32
- MSFT: removed (sold)
- NVDA: removed (sold)

## Errors / Flags

None. All tools completed successfully.