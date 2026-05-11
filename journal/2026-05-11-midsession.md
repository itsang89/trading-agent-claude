# Mid-Session Check — 2026-05-11 (Experiment Day 11)
**Routine:** mid-session-check
**Model:** claude-sonnet-4-6
**Time (ET):** ~1:35 PM ET
**Week number:** 3

---

## Market Status
Open. Regular session. Close time 4:00 PM ET. No early close.

## Portfolio State (Live ~1:35 PM ET)
- Equity: $10,063.56 | Cash: $3,967.72 (39.4%)
- Positions held: 6 (AAPL, AMZN, GOOGL, LLY, NVDA, QQQ)

---

## Positions Checked: 6

---

## Step 5 — Stop-Loss & Trailing Stop Audit

| Ticker | Avg Entry | Hard Stop | Trailing Active | Trailing Stop | Effective Stop | Live Price | Result |
|--------|-----------|-----------|-----------------|---------------|----------------|-----------|--------|
| AAPL | $273.908 | $252.00 | No (<$301.30) | — | $252.00 | $291.94 | PASS |
| AMZN | $266.733 | $245.39 | No (<$293.41) | — | $245.39 | $270.86 | PASS |
| GOOGL | $373.299 | $343.44 | No (<$410.63) | — | $343.44 | $393.40 | PASS |
| LLY | $987.435 | $908.44 | No (<$1,086.18) | — | $908.44 | $974.02 | PASS |
| NVDA | $216.630 | $199.30 | No (<$238.29) | — | $199.30 | $220.90 | PASS (stop order live) |
| QQQ | $678.381 | $624.11 | No (<$746.22) | — | $624.11 | $713.85 | PASS |

No stops triggered.

---

## Step 6 — Signal Check (14 bars available; using SMA_14 proxy)

SPY_10d_ROC: (740.14 − 715.165) / 715.165 × 100 = **+3.49%** (bars[-1]=5/11 $740.14, bars[-11]=4/27 $715.165)

| Ticker | SMA_14 | Close (5/11) | Trend | 10d_ROC | RS_spread | Signal | Flag |
|--------|--------|-------------|-------|---------|-----------|--------|------|
| AAPL | $278.46 | $291.97 | BULLISH | +9.13% | **+5.64%** | POSITIVE | None |
| AMZN | $266.21 | $270.76 | BULLISH | +3.72% | **+0.23%** | POSITIVE | RS_MOMENTUM_DECAY fading (was −0.05% at execution) |
| GOOGL | $371.78 | $393.27 | BULLISH | +12.27% | **+8.78%** | POSITIVE | None |
| LLY | $932.61 | $974.12 | BULLISH | +12.20% | **+8.71%** | POSITIVE | None |
| NVDA | $206.97 | $220.85 | BULLISH | +1.99% | **−1.50%** | **NEGATIVE** | RS_NEGATIVE SESSION 1 |
| QQQ | $676.10 | $713.81 | BULLISH | +7.46% | **+3.97%** | POSITIVE | None |

### NVDA — RS NEGATIVE (Session 1):
- RS_spread turned NEGATIVE (−1.50%) mid-session from +0.08% at execution.
- Root cause: bars[-11] rolls from 4/24 ($208.18) to 4/27 ($216.54) as 5/11 bar is added, compressing the 10d gain.
- Sized at 4.37% equity (Borderline tier, below Standard floor). Per strategy: "Standard or below: no trim; monitor and wait for session-2 confirmation."
- **ACTION: FLAG WATCH only. No sell. Confirm at EOD.**
- Earnings 5/20 (9 days). NEGATIVE RS flag + earnings approaching adds risk.

### AMZN — RS_MOMENTUM_DECAY status update:
- RS_spread +0.23% today (vs −0.05% at execution). Moved back to POSITIVE.
- Per RS counter reset rule: counter resets only when RS_spread > 0%. Today's intraday bar shows +0.23%. Formal reset assessment at EOD.
- DO NOT reset counter until EOD bar confirmed. Hold WATCH status intraday.

---

## position-highs.json Updates
- NVDA: high_close $216.63 → **$220.85** (new intraday high for 5/11)
  - Trailing threshold: $238.29 — still inactive (gap $17.44)
- QQQ: high_close $711.12 → **$713.81** (new intraday high for 5/11)
  - Trailing threshold: $746.22 — still inactive (gap $32.41)
- AAPL: close $291.97 < $293.15 — no update
- AMZN: close $270.76 < $276.36 — no update
- GOOGL: close $393.27 < $400.67 — no update
- LLY: close $974.12 < $991.945 — no update

---

## Sells Executed
None.

## Sells Aborted
None.

## No Action
No exit conditions met. No trend breaks. No 2-session RS confirmations. No hard stop breaches.

## RS First-Session Warnings
- **NVDA: RS_spread = −1.50% (NEGATIVE, session 1)**. Execution this morning was +0.08% (POSITIVE). No trim required (position <5%). Monitor at EOD for 2-session confirmation.

---

## EOD Carry-Forward
1. **NVDA RS NEGATIVE (session 1)** — if RS_spread < −1% at EOD → session-2 exit confirmed → sell at next execution (5/12). If RS > 0% at EOD → counter resets.
2. **AMZN RS_MOMENTUM_DECAY** — if RS_spread > 0% at EOD close → counter resets; flag cleared. If RS < −1% → session-1 trim triggers (~2.95 → 8%).
3. **GOOGL trailing** — high_close still $400.67; threshold $410.63 (gap $9.96). Update if today's final close > $410.63.
4. **LLY** — close $974.12, above warning zone ($938.06). Gap $36.06. Stable.
5. **NVDA stop order** — live at $199.30 (`216377a3-76e3-486c-86a9-3206bc12e956`). high_close updated to $220.85; trailing still inactive.
6. **Cash 39.4%** — appropriate for MIXED regime.
