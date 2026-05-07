# Pre-Market Research — 2026-05-07 (Experiment Day 9)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:32 AM ET
**Week number:** 2

---

## Market Status
Trading day. Market opens 9:30 AM, closes 4:00 PM ET. No early close.
Current time: 8:32 AM ET — pre-market.

---

## Regime: BULL — 8/12 universe tickers BULLISH
**Shift from MIXED (6/12) → BULL (8/12). Session 1 of transitional period.**
Transitional cap: limit new entries to top 3 RS per session (no new non-held tickers eligible anyway).
BULLISH: AAPL, AMZN, GOOGL, LLY, QQQ, XLV, NVDA, JPM
BEARISH: XLE, MSFT, META, BRK.B

Notable shifts from yesterday's MIXED regime:
- NVDA: BEARISH→BULLISH (close $207.67 > SMA_13 $204.00; but RS NEUTRAL at −0.58% — NOT eligible for entry)
- JPM: BEARISH→BULLISH (close $314.87 > SMA_13 $311.78; but RS NEGATIVE at −2.57% — NOT eligible for entry)
- XLV: BEARISH→BULLISH (close $145.38 > SMA_13 $145.13; marginal +0.17% above SMA; RS NEGATIVE at −3.83% — NOT eligible)

---

## Portfolio State
- Equity: $10,093.31 (pre-market Alpaca)
- Cash: $4,394.12 (43.56%)
- Positions: 5 (AAPL, AMZN, GOOGL, LLY, QQQ)
- Cumulative: agent +0.93% vs SPY +2.60% → delta −1.67 pp (agent trailing)
  - Agent cum = ($10,093.31 − $10,000) / $10,000 = +0.933%
  - SPY cum: start $715.165 (4/27), latest close $733.77 = +2.60%

**CASH ACCOUNTABILITY (BULL regime, cash > 35%):**
Cash 43.56% exceeds BULL target 10–25%. Diagnostic: ≥2 universe tickers have RS > 2% → sizing error check required.
Reason cash remains elevated after intents below: (1) AMZN RS_MOMENTUM_DECAY prohibits add; (2) LLY at tier ceiling with weak vol (0.79); (3) AAPL RS dropped to Standard tier, at ceiling; (4) no new eligible non-held tickers (all BEARISH or NEUTRAL RS). Only QQQ and conditional GOOGL can absorb cash.
Post-intent cash estimate: ~$3,623 (35.9%) — above BULL target but constrained by conviction and decay rules.

---

## Stop-Loss & Trailing Stop Audit (Step 6)

Position prices from get_positions (8:32 AM pre-market):
| Ticker | Avg Entry | Hard Stop | Trailing Threshold | PM Price | Effective Stop | Status |
|--------|-----------|-----------|-------------------|----------|----------------|--------|
| AAPL | $273.908 | $252.20 | >$301.30 (inactive) | $288.59 | $252.20 | PASS |
| AMZN | $266.733 | $245.39 | >$293.41 (inactive) | $275.42 | $245.39 | PASS |
| GOOGL | $373.299 | $343.44 | >$410.63 (inactive) | $401.51 | $343.44 | PASS |
| LLY | $987.435 | $908.44 | >$1,086.18 (inactive) | $989.50 | $908.44 | PASS |
| QQQ | $661.814 | $608.87 | >$727.99 (inactive) | $696.23 | $608.87 | PASS |

No stops triggered. No positions in warning zone (all above avg_entry × 0.95).
GOOGL pre-market $401.51 approaching trailing threshold $410.63 — gap ~$9.12. Watch today.
All stops manual — fractional GTC order failure persists (notes-for-operator.md).

---

## Signal Table (SMA_13 — 13 bars; 10d ref: 4/22 close $711.20; SPY_ROC: +3.173%)

| Ticker | SMA_13 | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|--------|-------|-------|---------|-----------|-----------|------------|--------|
| SPY | $715.32 | $733.77 | BULLISH | +3.17% | — | — | — | benchmark |
| AAPL | $274.24 | $287.46 | BULLISH | +5.24% | +2.07% | 1.00 | Standard | HOLD |
| AMZN | $262.35 | $274.98 | BULLISH | +7.68% | +4.51% | 0.96 | High | HOLD (decay) |
| GOOGL | $360.22 | $397.83 | BULLISH | +17.23% | +14.06% | 1.04 | Very High | ADD (conditional) |
| LLY | $921.68 | $987.02 | BULLISH | +7.12% | +3.95% | 0.79 | High | HOLD (ceiling, low vol) |
| QQQ | $664.35 | $695.62 | BULLISH | +6.19% | +3.02% | 1.16 | High | ADD |
| XLV | $145.13 | $145.38 | BULLISH | −0.66% | −3.83% | — | — | NO ENTRY |
| XLE | $57.63 | $56.98 | BEARISH | +0.80% | −2.38% | — | — | NO ENTRY |
| NVDA | $204.00 | $207.67 | BULLISH | +2.59% | −0.58% | — | — | NO ENTRY (NEUTRAL RS) |
| MSFT | $419.65 | $413.82 | BEARISH | −4.38% | −7.55% | — | — | NO ENTRY |
| META | $647.42 | $612.62 | BEARISH | −9.22% | −12.40% | — | — | NO ENTRY |
| JPM | $311.78 | $314.87 | BULLISH | +0.60% | −2.57% | — | — | NO ENTRY |
| BRK.B | $471.00 | $469.75 | BEARISH | +0.95% | −2.22% | — | — | NO ENTRY |

All 5 held positions: Trend BULLISH, RS POSITIVE. No soft exit conditions.
No new eligible non-held tickers (Trend BULLISH + RS POSITIVE): zero candidates.

---

## position-highs.json — Step 7c Update
Bars[-1] = 2026-05-06 close (same data as EOD 5/6; no new session bar yet).
- AAPL: 287.46 = stored high_close 287.46 → no update
- AMZN: 274.98 < stored high_close 276.36 → no update
- GOOGL: 397.83 = stored high_close 397.83 → no update
- LLY: 987.02 < stored high_close 991.945 → no update
- QQQ: 695.62 = stored high_close 695.62 → no update

No file update needed.

---

## RS Momentum Decay Check — Step 7d
No new bars today (pre-market bars = yesterday's closes). RS values unchanged from EOD 5/6.

| Ticker | 5/4 EOD RS | 5/5 mid RS | 5/6 EOD RS | 5/7 PM RS | Trend |
|--------|-----------|-----------|-----------|-----------|-------|
| AAPL | +0.08% | +3.35% | +2.07% | +2.07% (same data) | Not 3-consecutive ↓ |
| AMZN | +8.26% | +6.70% | +4.51% | +4.51% (same data) | ↓↓↓ RS_MOMENTUM_DECAY (active) |
| GOOGL | +12.25% | +13.06% | +14.06% | +14.06% (same data) | ↑ Strong |
| LLY | +3.88% | +7.01% | +3.95% | +3.95% (same data) | Mixed (up then down) |
| QQQ | +2.71% | +2.94% | +3.02% | +3.02% (same data) | ↑ Improving |

AMZN RS_MOMENTUM_DECAY flag: active from 5/6 EOD. Persists today. Do NOT add.

---

## Earnings & News Check — Step 7e (active 2026-05-05)

**Earnings:**
- AAPL: 2026-07-30 (84 days) — no flag
- AMZN: 2026-07-30 (84 days) — no flag
- GOOGL: 2026-07-23 (77 days) — no flag
- LLY: 2026-08-05 (90 days) — no flag
- QQQ: ETF — no earnings check
No earnings constraints on any position.

**News:**
- AAPL: Foldable phone design news (positive product signal). TSMC $56B AI expansion (positive supply chain). No negative catalyst.
- AMZN: Cramer defends $1.1T AI capex for Amazon/MSFT (positive). No negative catalyst.
- GOOGL: Pentagon Scale AI contract ($500M) benefits cloud providers incl. Google. AI spending broadly defended. No negative catalyst.
- LLY: $4.5B Indiana manufacturing expansion announced today — STRONGLY POSITIVE (domestic manufacturing/tariff hedge). Trump drug pricing headline is broad pharma, not LLY-specific. RFK psychiatric push irrelevant to GLP-1/biologics. Net: positive.
- QQQ: S&P 500/Nasdaq smash records 5/6, Dow futures up today. Trump celebrating market gains. No negative catalyst.

News conclusion: No negative catalysts for any held position. LLY and GOOGL have positive-leaning headlines today.

---

## Intents for 2026-05-07 Execution

### 1. QQQ ADD ~0.70 shares (High conviction)
- RS +3.02% (High tier 3–5%), vol_ratio 1.16. Position at 5.17% ($522), target 10% ($1,009).
- Add $487 at ~$696 = 0.70 shares.
- New avg_entry est.: (0.75 × $661.814 + 0.70 × $696) / 1.45 = ($496.36 + $487.20) / 1.45 = $678.32
- New hard stop: $678.32 × 0.92 = $624.05
- Trailing threshold: $678.32 × 1.10 = $746.15 (inactive; current high_close $695.62 < $746.15)
- Post-add: 1.45 shares, ~$1,009, ~10.0% of equity.
- RATIONALE: QQQ under-positioned at 5.17% vs 8–13% High tier target. RS crossed into High tier (>3%). Vol_ratio 1.16 supports. No earnings/news concerns. Regime shift to BULL reinforces broad market ETF exposure.

### 2. GOOGL ADD ~0.71 shares — CONDITIONAL on price ≥ $401.81 at 9:45 AM (Very High conviction)
- RS +14.06% (Very High tier >5%). Condition: price up >1% from $397.83 close = ≥$401.81.
- Pre-market $401.51 (+0.92%) — NOT yet met. Very close; confirm at execution.
- If condition met: add from 17.18% toward 20%. Target $2,019 − $1,735 = $284 add → 0.71 shares at ~$401.
- New avg_entry est.: ($373.299 × 4.32 + $401 × 0.71) / 5.03 = ($1,612.65 + $284.71) / 5.03 = $377.22
- New hard stop: $377.22 × 0.92 = $347.04
- New trailing threshold: $377.22 × 1.10 = $414.94
- GOOGL pre-market $401.51 vs trailing activation $410.63 — gap narrowing to ~$9.12. After add, new threshold rises to $414.94 — watch whether GOOGL reaches that today.
- Post-add: 5.03 shares, ~$2,019, ~20.0% of equity.
- RATIONALE (≥10%): GOOGL has strongest RS in portfolio (+14.06%, Very High). Adding from 17.18% to 20% fills to tier ceiling. Positive news (Pentagon AI contract). No earnings concern. BULL regime confirms aggression warranted for top-RS position. Condition gate ensures momentum is confirmed before add.

### 3. AAPL — HOLD
- RS dropped to Standard tier (+2.07% vs +3.96% yesterday). Position 8.18% is just above Standard ceiling (8%).
- Per strategy: "consider trimming to tier ceiling." Difference is $18 (negligible). Skip trim.
- No add — RS would need >3% to justify adding toward High tier. Signal intact but weakened.

### 4. AMZN — HOLD
- RS_MOMENTUM_DECAY flag active. Do NOT add regardless of tier position.
- Position 12.99% at High tier ceiling. Monitor: if RS_spread < 3% at next routine, trim toward 8–10%.

### 5. LLY — HOLD
- High tier (RS +3.95%), at tier ceiling 12.94%. Vol_ratio 0.79 (<0.80 threshold).
- Strategy: "vol_ratio < 0.8 → prefer lower end of tier range." Already at ceiling, no add.
- Positive news (Indiana expansion) — hold with confidence.

### Cash projection post-intents:
| Action | Est. cost |
|--------|-----------|
| QQQ +0.70 | ~$487 |
| GOOGL +0.71 (conditional) | ~$284 |
| **Total** | **~$771** |

Cash after: $4,394 − $771 = ~$3,623 (~35.9% of equity)
Still above BULL target 25% but fully explained: no new eligible entries, AMZN decay, LLY ceiling/low-vol, AAPL RS-tier drop.

---

## Sector Concentration (post-intents)
- IT (AAPL): ~8.2% — fine
- Consumer Disc (AMZN): ~13.0% — fine
- Comm Services (GOOGL): ~20.0% — fine
- Health Care (LLY): ~12.9% — fine
- ETF (QQQ): ~10.0%
No sector exceeds 40%.

---

## Carry-Forward from Last Session (EOD 5/6)
1. **GOOGL trailing threshold** — gap narrowed to $9.12 (high_close $397.83 vs threshold $410.63). Very close. If GOOGL adds today, new threshold rises to $414.94. Monitor.
2. **Stop orders still failing** — all 5 positions without standing stop orders. Manual enforcement every routine. Notes-for-operator.md has details.
3. **No stop triggers** — all positions well above hard stops. Confirmed.
4. **Regime shift MIXED→BULL** — recount confirmed 8/12 BULLISH today vs 6/12 yesterday.
5. **Cash 43.6%** — deploying via QQQ add and conditional GOOGL add; residual cash explained above.
6. **AMZN RS decay** — flag persists. Position at 13.0% High tier ceiling. Trim toward 8–10% if RS_spread < 3% at next routine.
7. **XLE sold 5/6** — confirmed removed from position-highs.json. No carry-forward.

---

## Errors / Flags
None. All tools returned successfully.
Stop order placement failures continue for all fractional positions — ongoing operational issue logged in notes-for-operator.md; manual enforcement active.
