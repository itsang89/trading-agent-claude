# Pre-Market Research — 2026-05-08 (Experiment Day 10 — Friday)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:40 AM ET
**Week number:** 2

---

## Market Status
Trading day. Market opens 9:30 AM, closes 4:00 PM ET. No early close.
Current time: 8:40 AM ET — pre-market.

---

## Regime: BULL — 8/12 universe tickers BULLISH
**Transitional period Day 2 (BULL regime confirmed 5/7). Cap: top 3 new entries per session (only 1 eligible today).**

BULLISH: AAPL, AMZN, GOOGL, LLY, QQQ, NVDA, MSFT, BRK.B
BEARISH: XLV, XLE, META, JPM

Notes:
- MSFT: close $420.79 > SMA_14 $419.73 — barely BULLISH (+$1.06). RS NEGATIVE (−2.04%) → not eligible.
- BRK.B: BULLISH trend but RS NEGATIVE (−2.38%) → not eligible.
- NVDA: BULLISH trend, RS POSITIVE (+2.69%) → NEW eligible entry candidate.

---

## Portfolio State
- Equity: $10,061.45 (pre-market Alpaca)
- Cash: $3,906.83 (38.83%)
- Positions: 5 (AAPL, AMZN, GOOGL, LLY, QQQ)
- Cumulative: agent +0.614% vs SPY +2.288% → delta −1.674 pp (agent trailing)

**CASH ACCOUNTABILITY (BULL regime, cash > 35%):**
38.83% cash exceeds BULL target 10–25%. Deploying via NVDA entry (~$503) and conditional GOOGL add (~$284 if gate met).
Post-intent cash estimate: ~$3,117–$3,403 (31–33.8%) — still above BULL target but constrained:
(1) AMZN RS_MOMENTUM_DECAY — no add; (2) LLY at High tier ceiling; (3) AAPL at Standard ceiling; (4) QQQ at floor; (5) Only NVDA is new eligible entry.

---

## Stop-Loss & Trailing Stop Audit (Step 6)

| Ticker | Avg Entry | Hard Stop | Trailing Threshold | PM Price | Effective Stop | Status |
|--------|-----------|-----------|-------------------|----------|----------------|--------|
| AAPL | $273.908 | $252.20 | >$301.30 (inactive) | $290.90 | $252.20 | PASS |
| AMZN | $266.733 | $245.39 | >$293.41 (inactive) | $272.29 | $245.39 | PASS |
| GOOGL | $373.299 | $343.44 | >$410.63 (inactive) | $398.20 | $343.44 | PASS |
| LLY | $987.435 | $908.44 | >$1,086.18 (inactive) | $976.34 | $908.44 | PASS |
| QQQ | $678.381 | $624.11 | >$746.22 (inactive) | $701.69 | $624.11 | PASS |

No stops triggered. No positions in warning zone (all > avg_entry × 0.95).
LLY pre-market $976.34 = −1.12% from avg_entry — below entry but above 95% floor ($938.06). No warning.
All stops manual — fractional GTC error persists (notes-for-operator.md).

---

## Signal Table (SMA_14 — 14 bars; bars[-1]=5/7 close; bars[-11]=4/23; SPY_ROC=+3.264%)

| Ticker | SMA_14 | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Tier | Action |
|--------|--------|-------|-------|---------|-----------|-----------|------|--------|
| SPY | $716.48 | $731.53 | BULLISH | +3.264% | — | 0.967 | — | benchmark |
| AAPL | $275.18 | $287.40 | BULLISH | +5.086% | +1.822% | 0.895 | Standard | HOLD |
| AMZN | $262.97 | $271.08 | BULLISH | +6.281% | +3.017% | 0.873 | High | HOLD (decay) |
| GOOGL | $362.91 | $397.89 | BULLISH | +17.420% | +14.157% | 0.863 | Very High | ADD (conditional) |
| LLY | $925.52 | $975.35 | BULLISH | +6.330% | +3.066% | 0.851 | High | HOLD (watch) |
| QQQ | $666.53 | $694.93 | BULLISH | +6.683% | +3.419% | 1.119 | High | HOLD |
| XLV | $145.11 | $144.76 | BEARISH | −0.992% | −4.255% | N/A | — | NO ENTRY |
| XLE | $57.51 | $55.96 | BEARISH | −1.764% | −5.028% | N/A | — | NO ENTRY |
| NVDA | $204.53 | $211.56 | BULLISH | +5.950% | +2.686% | 0.988 | Standard | BUY (new) |
| MSFT | $419.73 | $420.79 | BULLISH | +1.221% | −2.043% | N/A | — | NO ENTRY (RS NEG) |
| META | $645.22 | $616.58 | BEARISH | −6.458% | −9.722% | N/A | — | NO ENTRY |
| JPM | $311.39 | $306.32 | BEARISH | −1.729% | −4.993% | N/A | — | NO ENTRY |
| BRK.B | $471.27 | $474.89 | BULLISH | +0.888% | −2.376% | N/A | — | NO ENTRY (RS NEG) |

All 5 held positions: Trend BULLISH, RS POSITIVE. No soft exit conditions.
New eligible entry: NVDA only (Trend BULLISH + RS POSITIVE +2.686%).

---

## position-highs.json — Step 7c Update
bars[-1] = 5/7 close. No new highs vs stored values:
- AAPL: $287.40 < stored $288.79 → no update
- AMZN: $271.08 < stored $276.36 → no update
- GOOGL: $397.89 = stored $397.89 → no update
- LLY: $975.35 < stored $991.945 → no update
- QQQ: $694.93 < stored $695.62 → no update

No file update needed.

---

## RS Momentum Decay Check — Step 7d

Today's pre-market uses same 5/7 bars. No new session data.

| Ticker | 5/4 EOD | 5/5 mid | 5/6 EOD | 5/7 mid | 5/7 EOD | 5/8 PM | Trend |
|--------|---------|---------|---------|---------|---------|--------|-------|
| AAPL | +0.08% | +3.35% | +2.07% | +2.41% | +1.824% | +1.822% | Mixed |
| AMZN | +8.26% | +6.70% | +4.51% | +3.32% | +3.016% | +3.017% | ↓↓↓↓↓ DECAY (active) |
| GOOGL | +12.25% | +13.06% | +14.06% | +13.58% | +14.157% | +14.157% | Strong ↑ |
| LLY | +3.88% | +7.01% | +3.95% | +2.73% | +3.065% | +3.066% | ↓↓ Watch (2 sessions) |
| QQQ | +2.71% | +2.94% | +3.02% | +3.35% | +3.418% | +3.419% | ↑ Improving |

- **AMZN RS_MOMENTUM_DECAY**: Active from 5/6 EOD. Today flat (same bars). Do NOT add. Flag remains active.
- **LLY Watch**: 2 consecutive EOD-to-EOD declining sessions. Not yet 3. No new decay flag today (no new session bar).

---

## Earnings & News Check — Step 7e

**Earnings:**
| Ticker | Next Earnings | Days | Flag |
|--------|-------------|------|------|
| AAPL | 2026-07-30 | 83 | none |
| AMZN | 2026-07-30 | 83 | none |
| GOOGL | 2026-07-23 | 76 | none |
| LLY | 2026-08-05 | 89 | none |
| QQQ | ETF | — | none |
| NVDA | 2026-05-20 | 12 | none (>7 days) |

NVDA earnings 12 days out — no formal flag, but noted in sizing rationale below.

**News (held positions):**
- AAPL: Apple CEO invited on Trump's China trade visit — positive diplomatic signal. No negative catalyst.
- AMZN: AI drove 2/3 of Q1 2026 GDP growth (positive macro). EU considering restricting US cloud providers for sensitive government data — potential headwind for AWS; signals say hold.
- GOOGL: AI GDP growth positive. TikTok gained web traffic in April while Google declined — mild negative. EU cloud restriction concern (same as AMZN). Signals say hold; not a sell trigger.
- LLY: $4.5B Indiana manufacturing expansion (positive, confirmed from 5/7). No new negative catalyst.
- QQQ: US-Iran exchange near Hormuz Strait — minor geopolitical risk. Jobs report today (Friday). Futures rising pre-market.

News conclusion: No sell-triggering negative catalysts for any held position.

---

## Intents for 2026-05-08 Execution

### 1. NVDA BUY ~2.38 shares (~$503, Standard tier) — NEW POSITION
- RS +2.686% (Standard tier 1–3%), vol_ratio 0.988 (neutral), Trend BULLISH
- Target: 5% of $10,061 = ~$503 at ~$211.56 → ~2.38 shares
- Hard stop: $211.56 × 0.92 = $194.64
- Trailing threshold: $211.56 × 1.10 = $232.72 (inactive on entry)
- RATIONALE: Only new eligible entry in BULL regime. BULL regime + cash 38.83% obligates cash deployment check. RS fresh (Session 1 confirmed positive). Sizing at lower Standard range (5%) rather than upper (8%) given: (a) earnings 12 days out on 5/20 — outside 7-day flag but close; (b) Friday entry with no weekend monitoring; (c) vol_ratio neutral. News strongly positive (AI GDP, TSMC April sales strong, Trump China visit with NVDA CEO included). Earnings proximity limits further adds — do not scale above 6% unless RS_spread climbs above 3% before 5/16.
- Sector: IT. Post-add IT concentration: AAPL 8.27% + NVDA 5.0% = 13.27% — well below 40% limit.

### 2. GOOGL ADD ~0.71 shares — CONDITIONAL on price ≥ $401.87 at 9:45 ET (Very High conviction)
- RS +14.157% (Very High). Position 17.10% ($1,720). Target: 20% ($2,012).
- Gate: close_yesterday $397.89 × 1.01 = $401.87. Pre-market $398.20 — NOT met.
- If condition met: add $284 → 5.03 shares total, ~$2,004, ~19.9% equity.
- New avg_entry est.: ($373.299 × 4.32 + $401.87 × 0.71) / 5.03 = ($1,612.65 + $285.33) / 5.03 = $377.39
- New hard stop: $377.39 × 0.92 = $347.20
- New trailing threshold: $377.39 × 1.10 = $415.13
- RATIONALE (≥10%): Highest RS in portfolio by wide margin (+14.16%). Filling to Very High tier ceiling. Conditional gate confirms intraday momentum before adding. EU cloud concern is noted but signals primary. This intent unchanged from 5/7.

### 3. AAPL — HOLD
- RS +1.822%, Standard tier. Position 8.27% at Standard ceiling. Vol_ratio 0.895.
- No add (RS would need >3% for High tier). No trim (negligible difference, ~$18).
- Apple CEO on Trump China visit — mildly positive catalyst.

### 4. AMZN — HOLD
- RS +3.017%, High tier (barely above 3% floor). RS_MOMENTUM_DECAY active.
- Position 12.88%, at High tier ceiling. Do NOT add.
- Trim trigger unchanged: If RS_spread < 3% at any routine → trim toward Standard ceiling (~$800, ~8% equity).
- EU cloud/AI capex news tracked but not sell-triggering.

### 5. LLY — HOLD
- RS +3.066%, High tier. Position 12.81%. Vol_ratio 0.851.
- 2 consecutive declining RS sessions. Monitor at execution/EOD: if 3rd decline → flag RS_MOMENTUM_DECAY, no further adds.
- No add (at ceiling, vol_ratio borderline).

### 6. QQQ — HOLD
- RS +3.419%, High tier. Position 10.11%. Vol_ratio 1.119.
- Strong signals. No add urgency — position already at High floor/mid-range.
- Geopolitical risk (Hormuz) noted; no action.

### Cash projection post-intents:
| Action | Est. cost |
|--------|-----------|
| NVDA BUY | ~$503 |
| GOOGL ADD (conditional) | ~$284 |
| **Total** | **~$787** |

Cash after: $3,907 − $787 = ~$3,120 (~31% if both execute; ~33.8% if only NVDA)

### Sector concentration (post-intents, if both execute):
- IT (AAPL + NVDA): 8.27% + 5.0% = 13.27% ✓
- Consumer Disc (AMZN): 12.88% ✓
- Comm Services (GOOGL): 19.9% ✓
- Health Care (LLY): 12.81% ✓
- ETF (QQQ): 10.11% ✓
- No sector exceeds 40% ✓

---

## Carry-Forward from Last Session (EOD 5/7)
1. **AMZN RS trim trigger**: RS +3.017% today (≥3% → HOLD). Trigger unchanged: trim if RS < 3% at any routine. ✓
2. **GOOGL conditional add**: Gate $401.87, pre-market not met ($398.20). Re-check at 9:45. ✓
3. **LLY decay watch**: 2 consecutive declining — needs 3 for decay flag. Monitor at execution/EOD. ✓
4. **AAPL trim consideration**: At ceiling 8.27%. Skip trim (negligible). ✓
5. **Stop orders manual**: All 5 positions no GTC stop orders (fractional error persists). Manual enforcement. ✓
6. **Cash elevated (38.83%)**: Deploying via NVDA new entry. Post-intents: 31–33.8%. ✓
7. **NVDA signal shift**: Was NEUTRAL RS on 5/7, now POSITIVE +2.686% on 5/8. RS crossed into Standard tier with BULLISH trend. Eligible for new entry. ✓
8. **Friday weekly-review**: Runs at 5:00 PM ET today. EOD runs first at 4:30 PM.

---

## Errors / Flags
- Stop order placement failures: all 5 positions have no GTC stop orders (fractional DAY error persists). Manual enforcement each routine. notes-for-operator.md has full history.
- No tool errors this routine.
