# Pre-Market Research — 2026-05-11 (Experiment Day 11)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:35 AM ET
**Week number:** 2

---

## Market Status
Trading day. Opens 9:30 AM, closes 4:00 PM ET. No early close.
Current time: 8:35 AM ET — pre-market.

---

## Regime: MIXED — 7/12 universe tickers BULLISH
**Downgrade from BULL (8/12 on 5/7) → MIXED (7/12 today).**
BULLISH: QQQ, AAPL, AMZN, GOOGL, LLY, NVDA, BRK.B
BEARISH: XLV, XLE, MSFT, META, JPM

Regime implication: Target cash 25–40%. Be selective. Transitional regime cap (top 3 RS per session) applies.

---

## STATE DISCREPANCY — NVDA POSITION (OPERATOR FLAG)
NVDA appears in live Alpaca positions (2.0 shares, avg_entry $216.63) but was **NOT** in `last-session.md` (5/7 execution) or `position-highs.json`. No journal exists for 5/8 (Friday). NVDA was purchased between 5/7 execution and 5/11 pre-market without a recorded journal entry.

Action taken:
- Accepting NVDA position as real (Alpaca is authoritative)
- Initialized NVDA in position-highs.json (high_close = entry_price = $216.63)
- Placed stop order at $199.30 (avg_entry × 0.92): stop_order_id = `216377a3-76e3-486c-86a9-3206bc12e956` — SUCCEEDED (whole shares)
- Flagged in notes-for-operator.md

Last-session.md from 5/7 listed 5 positions (AAPL, AMZN, GOOGL, LLY, QQQ). Live now shows 6. Cash difference: $3,906.83 (5/7) → $3,473.57 (5/11), delta −$433.26 ≈ 2 shares × $216.63 = $433.26. Consistent with 2.0 NVDA shares purchased ~5/8.

---

## Portfolio State
- Equity: $10,022.60 | Cash: $3,473.57 (34.6%)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, NVDA, QQQ)
- Cumulative: agent +0.226% vs SPY +3.129% → delta −2.90 pp (agent trailing)
  - Agent cum = ($10,022.60 − $10,000) / $10,000 = +0.226%
  - SPY cum: get_spy_benchmark returns +3.1286% (start $715.165, latest $737.54)

Cash 34.6% is within MIXED regime target (25–40%). No accountability issue.

---

## Stop-Loss & Trailing Stop Audit (Step 6)
Prices from positions.json (pre-market, latest available = 5/8 closes from get_bars):

| Ticker | Avg Entry | Hard Stop | Trailing Threshold | Current Price | Effective Stop | Status |
|--------|-----------|-----------|-------------------|---------------|----------------|--------|
| AAPL | $273.908 | $252.00 | >$301.30 (inactive) | $292.60 | $252.00 | PASS |
| AMZN | $266.733 | $245.39 | >$293.41 (inactive) | $270.80 | $245.39 | PASS |
| GOOGL | $373.299 | $343.44 | >$410.63 (inactive) | $396.50 | $343.44 | PASS |
| LLY | $987.435 | $908.44 | >$1,086.18 (inactive) | $948.66 | $908.44 | PASS |
| NVDA | $216.630 | $199.30 | >$238.29 (inactive) | $214.02 | $199.30 | PASS |
| QQQ | $678.381 | $624.11 | >$746.22 (inactive) | $710.37 | $624.11 | PASS |

No stops triggered. No positions in warning zone (all > avg_entry × 0.95).
- LLY warning zone threshold = $938.06; current $948.66 — gap only $10.60. Watch closely.
- GOOGL trailing activation: high_close $400.67 vs threshold $410.63 — gap $9.96. Very close.
- NVDA stop order placed today (stop_order_id `216377a3-76e3-486c-86a9-3206bc12e956`).
- AAPL, AMZN, GOOGL, LLY, QQQ: no standing stop orders (fractional GTC error persists). Manual enforcement.

---

## Signal Table (SMA_13 — 13 bars; bars[-11] = 4/24; SPY_10d_ROC = +3.30%)

| Ticker | SMA_13 | Close (5/8) | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|--------|-------------|-------|---------|-----------|-----------|------------|--------|
| SPY | $719.66 | $737.54 | BULLISH | +3.30% | — | — | — | benchmark |
| AAPL | $277.42 | $293.15 | BULLISH | +8.16% | **+4.86%** | 1.14 | High→Very High | HOLD |
| AMZN | $265.84 | $272.54 | BULLISH | +3.25% | **−0.05%** | 0.93 | — (NEUTRAL) | HOLD/MONITOR |
| GOOGL | $370.13 | $400.67 | BULLISH | +16.36% | **+13.06%** | 0.81 | Very High | HOLD |
| LLY | $929.42 | $948.51 | BULLISH | +7.30% | **+4.00%** | 0.76 | High | HOLD (weak vol) |
| NVDA | $205.90 | $215.21 | BULLISH | +3.38% | **+0.08%** | 0.88 | Borderline | HOLD |
| QQQ | $673.20 | $711.12 | BULLISH | +7.11% | **+3.81%** | 1.22 | High | HOLD |
| XLV | $144.74 | $143.53 | BEARISH | −0.47% | −3.77% | — | — | NO ENTRY |
| XLE | $57.69 | $55.69 | BEARISH | −2.12% | −5.42% | — | — | NO ENTRY (sold 5/6) |
| MSFT | $419.16 | $414.97 | BEARISH | −2.27% | −5.57% | — | — | NO ENTRY |
| META | $638.69 | $609.55 | BEARISH | −9.69% | −12.99% | — | — | NO ENTRY |
| JPM | $310.12 | $302.10 | BEARISH | −2.00% | −5.30% | — | — | NO ENTRY |
| BRK.B | $471.78 | $475.65 | BULLISH | +1.35% | −1.95% | — | — | NO ENTRY (RS NEG) |

No non-held tickers eligible for new entry (all non-held are BEARISH trend or NEGATIVE RS).

---

## position-highs.json — Step 7c Updates
- AAPL: $287.46 → **$293.15** (5/8 close is new high)
- AMZN: $272.535 < $276.36 → no update
- GOOGL: $397.83 → **$400.67** (5/8 close is new high; trailing gap now $9.96)
- LLY: $948.51 < $991.945 → no update
- QQQ: $695.62 → **$711.12** (5/8 close is new high)
- NVDA: initialized at $216.63 (entry_price = high_close = avg_entry; stop placed)

Trailing activation status:
- AAPL: $293.15 < $301.30 threshold — inactive
- AMZN: $276.36 < $293.41 — inactive
- GOOGL: $400.67 < $410.63 — **WATCH: gap only $9.96** — may activate today if price rallies
- LLY: $991.945 < $1,086.18 — inactive
- QQQ: $711.12 < $746.22 — inactive
- NVDA: $216.63 < $238.29 — inactive

---

## RS Momentum Decay Check — Step 7d

| Ticker | 5/5 RS | 5/6 EOD RS | 5/8 RS | Trend | Flag |
|--------|--------|-----------|--------|-------|------|
| AAPL | +3.35% | +2.07% | +4.86% | ↓ then ↑ | None |
| AMZN | +6.70% | +4.51% | −0.05% | ↓↓↓ (continuing) | RS_MOMENTUM_DECAY ACTIVE |
| GOOGL | +13.06% | +14.06% | +13.06% | ↑ then flat | None |
| LLY | +7.01% | +3.95% | +4.00% | ↓ then flat | None |
| QQQ | +2.94% | +3.02% | +3.81% | ↑↑ | None |
| NVDA | — | — | +0.08% | (new position) | Cannot assess |

AMZN RS_MOMENTUM_DECAY: ACTIVE. RS now turned NEUTRAL (−0.05%). Do NOT add. If RS_spread < −1% at any session → session-1 trim triggers.

---

## Earnings & News Check — Step 7e (active 2026-05-05)

**Earnings:**
| Ticker | Next Date | Days Until | Flag |
|--------|-----------|-----------|------|
| AAPL | 2026-07-30 | 80 | None |
| AMZN | 2026-07-30 | 80 | None |
| GOOGL | 2026-07-23 | 73 | None |
| LLY | 2026-08-05 | 86 | None |
| NVDA | 2026-05-20 | 9 | **None (9d > 7d threshold)** |
| QQQ | ETF | N/A | None |

NVDA earnings 5/20 (9 days) — just above EARNINGS_THIS_WEEK threshold. Approaching. If held at next session, it will be 8 days and still above threshold. Risk: NVDA already borderline RS (+0.08%). Note: do not add to NVDA before 5/20 earnings.

**News:**
- AAPL: Apple-Intel chip partnership (supply chain diversification — mixed: implies supply stress but positive strategic move). No negative catalyst.
- AMZN: Incidentally mentioned in AI/cloud headlines. No negative catalyst for AMZN directly.
- GOOGL: "Alphabet Could Overtake Nvidia As World's Largest Company" — positive sentiment. AI/cloud momentum. No negative catalyst.
- LLY: IVF benefit expansion (positive for pharma). $4.5B Indiana investment from 5/7 still in news. No negative catalyst.
- NVDA: Alphabet-NVDA competition article mentions narrowing valuation gap — mild negative. Earnings in 9 days. No surprise negative catalyst.
- QQQ: Nasdaq futures soft today ("Trump rejects Iran peace proposal"). Market likely opens slightly weak. Ed Yardeni raised S&P target to 8,250 (positive macro). Net: cautious open.

News conclusion: No negative catalysts triggering signal-override. QQQ market-open weakness noted; does not affect hold decisions.

---

## Intents for 2026-05-11 Execution

### 1. GOOGL — HOLD at 17.09%
- RS +13.06%, Very High tier. Pre-market price $396.50 < 5/8 close $400.67 (soft pre-market).
- Very-high-conviction add condition: price up >1% at execution. Would require ≥ $404.68 (1% above 5/8 close). Unlikely given soft pre-market.
- MIXED regime → conservative posture. No conditional add today. Hold at 17.09%.
- Monitor: trailing activation within $9.96 of threshold.

### 2. AAPL — HOLD at 8.35%
- RS jumped +4.86% (near Very High tier threshold of 5%). Vol_ratio 1.14.
- Position at 8.35%, bottom of High tier range (8–13%). Signal strengthened significantly from +2.07% (5/7).
- In MIXED regime, top-3 RS names eligible for consideration. AAPL is #2 by RS_spread.
- Decision: HOLD today. Signal is strong but QQQ news suggests soft open. Re-evaluate add at execution if market opens with strength. If AAPL price ≥ $293.15 × 1.005 = $294.62 at 9:45 AM, consider adding ~0.50 shares to ~10% ($1,002). Not a firm commitment — regime is MIXED.

### 3. QQQ — HOLD at 10.28%
- RS +3.81%, High tier. Vol_ratio 1.22 (elevated). Position within tier range.
- Market ETF may face soft open per news. Hold, no add today.

### 4. LLY — HOLD at 12.49%
- RS +4.00%, High tier, vol_ratio 0.76 (weak). Price declining from high ($991.945 → $948.51).
- LLY is $10.60 above warning zone threshold ($938.06). Monitor closely at execution.
- No add. If price drops below $938.06 at any point, note in journal but do not exit unless stop triggers.

### 5. AMZN — HOLD/MONITOR at 12.86%
- RS NEUTRAL (−0.05%). RS_MOMENTUM_DECAY active. Do NOT add.
- WATCH: if RS_spread crosses below −1% at any session, session-1 trim triggers (trim from 12.86% → 8% High tier ceiling).
- Not an exit yet. Position BULLISH, RS borderline neutral.

### 6. NVDA — HOLD at 4.27%
- RS borderline (+0.08%). Borderline tier (3–5%). Earnings 5/20 (9 days).
- Stop order placed: $199.30, order_id `216377a3-76e3-486c-86a9-3206bc12e956`.
- No add: borderline RS + MIXED regime + earnings approaching.
- Do NOT add before 5/20 earnings.

### No new entries
No non-held universe tickers qualify (all are BEARISH trend or RS NEGATIVE/NEUTRAL).

### Cash management:
Current cash 34.6% is appropriate for MIXED regime (target 25–40%). No forced deployment required.

---

## Sector Concentration (current)
| Sector | Tickers | Approx % Equity |
|--------|---------|-----------------|
| IT | AAPL, NVDA | ~12.6% (8.35% + 4.27%) |
| Consumer Disc | AMZN | ~12.9% |
| Comm Services | GOOGL | ~17.1% |
| Health Care | LLY | ~12.5% |
| ETF | QQQ | ~10.3% |
| Cash | — | ~34.6% |

No sector concentration issue (all well below 40%).

---

## Carry-Forward from Last Session (2026-05-07 execution)
1. **NVDA discrepancy RESOLVED** — NVDA accepted as real position; initialized in position-highs.json; stop placed.
2. **GOOGL conditional add** — original gate $401.81 missed 5/7. Today's pre-market at $396.50. Not re-attempting today given MIXED regime. Will reassess if GOOGL exceeds $404.68 at 9:45 AM.
3. **GOOGL trailing** — gap to activation now $9.96 (high_close $400.67 vs $410.63). Close. Update if GOOGL closes above $410.63.
4. **AMZN RS_MOMENTUM_DECAY** — flag continues. RS now NEUTRAL (−0.05%). One session below −1% triggers trim.
5. **Stop orders** — NVDA now has GTC stop (whole shares work). AAPL, AMZN, GOOGL, LLY, QQQ still manual (fractional GTC error).
6. **May 8 routine gap** — no journals exist for 5/8. Flagged in notes-for-operator.md.

---

## Errors / Flags
- NVDA position discrepancy: flagged in notes-for-operator.md.
- QQQ earnings tool returned 404 (ETF — expected; no earnings data needed).
- All other tools returned successfully.
