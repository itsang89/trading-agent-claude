# Mid-Session Check — 2026-05-08 (Experiment Day 10 — Friday)
**Routine:** mid-session-check
**Model:** claude-sonnet-4-6
**Time (ET):** ~1:40 PM ET
**Week number:** 2

---

## Market Status
Open. 9:30–16:00 ET. No early close.

---

## Portfolio State (~1:40 PM)
- Equity: $10,049.34 | Cash: $3,473.57 (34.55%) | Positions: 6

---

## Step 5 — Stop-Loss & Trailing Stop Audit

All stops computed with live prices from get_positions.

| Ticker | Avg Entry | Hard Stop | High Close | Trailing Thr | Trailing Active | Eff. Stop | Current | Status |
|--------|-----------|-----------|------------|--------------|-----------------|-----------|---------|--------|
| AAPL | $273.908 | $252.20 | $288.79 | >$301.30 | No | $252.20 | $292.42 | PASS |
| AMZN | $266.733 | $245.39 | $276.36 | >$293.41 | No | $245.39 | $272.43 | PASS |
| GOOGL | $373.299 | $343.44 | $397.89 | >$410.63 | No | $343.44 | $398.06 | PASS |
| LLY | $987.435 | $908.44 | $991.945 | >$1,086.18 | No | $908.44 | $956.50 | PASS |
| NVDA | $216.63 | $199.30 | $216.63 | >$238.29 | No | $199.30 | $215.57 | PASS |
| QQQ | $678.381 | $624.11 | $695.62 | >$746.22 | No | $624.11 | $709.88 | PASS |

No stops triggered.

---

## Step 6 — Signal Check on Held Positions

SMA_15 used (15 bars returned). SPY_10d_ROC = +3.289% (bars[-1]=$737.455, bars[-11]=4/24 $713.97).
Note: reference period shifted from 4/23 to 4/24 vs pre-market (which used 5/7 bars with 4/23 ref). RS_spreads not directly comparable to this morning's values.

| Ticker | SMA_15 | Close | Trend | 10d_ROC | RS_spread | Status |
|--------|--------|-------|-------|---------|-----------|--------|
| AAPL | $276.34 | $292.53 | BULLISH | +7.929% | +4.640% | HOLD |
| AMZN | $263.60 | $272.455 | BULLISH | +3.218% | −0.071% | HOLD — WATCH (RS crossed <0%) |
| GOOGL | $365.26 | $398.15 | BULLISH | +15.630% | +12.341% | HOLD |
| LLY | $927.59 | $956.61 | BULLISH | +8.210% | +4.921% | HOLD |
| NVDA | $205.26 | $215.35 | BULLISH | +3.444% | +0.155% | HOLD — WATCH (Borderline) |
| QQQ | $669.43 | $709.95 | BULLISH | +6.933% | +3.644% | HOLD |

**AMZN:** RS_spread −0.071% = NEUTRAL (in [−1%, 0%]). NOT < −1% → no RS exit condition. This is the first session below 0% (not a 2-session confirmation). WATCH at EOD. Execution journal this morning showed RS +3.017% (not < −1%), so no 2-session confirmation possible today.

**NVDA:** RS_spread +0.155% = BORDERLINE POSITIVE (still > 0%). Reference period shift (4/23→4/24) moved denominator from $199.68 to $208.18, compressing the ROC. No exit triggered. Monitor at EOD — if RS < 0%, flag as first NEGATIVE session.

**LLY:** RS_spread jumped to +4.921% due to reference period shift (4/24 was $884.02, a weak day vs 4/23 $917.29). Reassesses the 2-session declining pattern — carry forward LLY RS chain analysis to EOD with updated reference.

---

## position-highs.json Updates

- AAPL: $292.53 > old high $288.79 → updated to $292.53 (trailing threshold $301.30 — still inactive)
- GOOGL: $398.15 > old high $397.89 → updated to $398.15 (trailing threshold $410.63 — still inactive)
- QQQ: $709.95 > old high $695.62 → updated to $709.95 (trailing threshold $746.22 — still inactive)
- AMZN: $272.455 < $276.36 → no update
- LLY: $956.61 < $991.945 → no update
- NVDA: $215.35 < $216.63 → no update

---

## Sells Executed
None.

## Sells Aborted
None.

## No action
No exit conditions met. All 6 positions Trend BULLISH, RS POSITIVE.

---

## GOOGL Conditional Add Check
Gate: $401.87. Today's intraday high: $401.31. Gate NOT met. GOOGL add deferred to EOD.

---

## RS First-Session Warnings
- **AMZN**: RS_spread −0.071% (NEUTRAL). First session below 0% today. RS_MOMENTUM_DECAY already active. Carry-forward trim trigger (<3%) confirmed hit. EOD decision: trim AMZN toward Standard ceiling (~8% equity, ~$820 notional) if RS remains < 3% at EOD bars.
- **NVDA**: RS_spread +0.155% (BORDERLINE). Dropped from +2.686% this morning due to reference period shift. Still positive. Flag if RS < 0% at EOD.

---

## Errors / Flags
None. All tools ran cleanly.
