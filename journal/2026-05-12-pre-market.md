# Pre-Market Research — 2026-05-12 (Experiment Day 12, Week 3)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:33 AM ET
**Week number:** 3

---

## Market Status
Trading day. Opens 9:30 AM ET, closes 4:00 PM ET. No early close.
Current time: 8:33 AM ET — pre-market window.

---

## Regime: MIXED — 7/12 universe tickers BULLISH
BULLISH: QQQ, AAPL, AMZN, GOOGL, LLY, NVDA, BRK.B
BEARISH: XLV, XLE, MSFT, META, JPM

Regime unchanged from 5/11. Target cash 25–40%. Be selective.

---

## Portfolio State (live pre-market)
- Equity: $9,984.64 | Cash: $3,967.71 (~39.7%)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, NVDA, QQQ)
- Agent cum return: −0.154% | SPY cum: +3.361% | Delta: **−3.515 pp** (agent trailing)
  - Equity declined from $10,028.55 (EOD 5/11) → $9,984.64 pre-market (−$43.91 = pre-market price softness)

---

## Stop-Loss & Trailing Stop Audit (Step 6)

**AMZN avg_entry discrepancy noted:** position-highs.json had entry_price $266.733; Alpaca live shows $270.257.
Explanation: 5/11 FIFO trim sold 1.81 lowest-cost lots; remaining lots at higher avg. Alpaca is authoritative.
Updated position-highs.json AMZN entry_price → $270.257 (hard stop recomputed: $248.64).

| Ticker | Avg Entry | Hard Stop | Trailing Threshold | Pre-Mkt Price | Effective Stop | Status |
|--------|-----------|-----------|-------------------|---------------|----------------|--------|
| AAPL | $273.908 | $252.00 | >$301.30 (inactive) | $292.16 | $252.00 | PASS (+13.9%) |
| AMZN | $270.257 | $248.64 | >$297.28 (inactive) | $266.96 | $248.64 | PASS (+7.4%) |
| GOOGL | $373.299 | $343.44 | >$410.63 (inactive) | $385.01 | $343.44 | PASS (+12.2%) |
| LLY | $987.435 | $908.44 | >$1,086.18 (inactive) | $962.99 | $908.44 | PASS (+6.0%) |
| NVDA | $216.630 | $199.30 | >$238.29 (inactive) | $217.49 | $199.30 | PASS — GTC live; SELL QUEUED |
| QQQ | $678.381 | $624.11 | >$746.22 (inactive) | $706.55 | $624.11 | PASS (+13.2%) |

No stops triggered. Warning proximity:
- LLY: warning zone $938.06, gap $24.93 (−2.48% unrealized). Watch closely.
- AMZN: −1.22% unrealized; warning zone $256.74, gap $10.22. Above threshold but soft pre-market.

---

## Signal Table (SMA_13 — 13 bars: 4/23 → 5/11; SPY_10d_ROC = +3.361%)

**Note:** SMA_20 unavailable — only 13 bars returned. Labeled SMA_13. All closes significantly above SMA_13 for held positions (no BORDERLINE trend signals from proxy usage).

| Ticker | SMA_13 | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|--------|-------|-------|---------|-----------|-----------|------------|--------|
| SPY | $722.04 | $739.20 | BULLISH | +3.361% | — | — | benchmark | — |
| AAPL | $278.92 | $292.66 | BULLISH | +9.385% | **+6.024%** | 0.83 | Very High (>5%) | HOLD |
| AMZN | $266.89 | $268.98 | BULLISH | +3.039% | **−0.322%** | 0.72 | NEUTRAL | HOLD/WATCH |
| GOOGL | $374.00 | $388.64 | BULLISH | +10.946% | **+7.585%** | 0.83 | Very High (>5%) | HOLD (RS_DETERIORATING) |
| LLY | $933.09 | $967.16 | BULLISH | +11.393% | **+8.032%** | 0.74 | Very High (>5%) | HOLD |
| NVDA | $207.21 | $219.45 | BULLISH | +1.344% | **−2.017%** | 0.86 | — | **SELL** |
| QQQ | $677.68 | $713.37 | BULLISH | +7.392% | **+4.031%** | 0.94 | High (3–5%) | HOLD |
| XLV | $144.49 | $143.03 | BEARISH | −0.293% | −3.654% | — | — | NO ENTRY |
| XLE | $57.74 | $57.18 | BEARISH | +0.669% | −2.692% | — | — | NO ENTRY |
| MSFT | $417.60 | $412.62 | BEARISH | −2.904% | −6.265% | — | — | NO ENTRY |
| META | $632.83 | $598.71 | BEARISH | −11.760% | −15.121% | — | — | NO ENTRY |
| JPM | $309.10 | $299.81 | BEARISH | −3.815% | −7.176% | — | — | NO ENTRY |
| BRK.B | $472.87 | $479.59 | BULLISH | +1.417% | −1.944% | — | — | NO ENTRY (RS NEG) |

No non-held universe tickers eligible for new entry. All BEARISH trend or NEGATIVE RS.

---

## Step 7c — position-highs.json Updates
All 5/11 closes below prior recorded high_close values:
- AAPL: $292.66 < $293.15 — no update
- AMZN: $268.98 < $276.36 — no update
- GOOGL: $388.64 < $400.67 — no update
- LLY: $967.16 < $991.945 — no update
- NVDA: $219.45 < $220.85 — no update (selling today)
- QQQ: $713.37 < $713.81 — no update

AMZN entry_price updated to $270.257 (Alpaca authoritative, FIFO correction).

---

## Step 7d — RS Momentum Decay Check (held positions only)

| Ticker | 5/6 EOD RS | 5/8 EOD RS | 5/11 EOD RS | Trend | Flag |
|--------|-----------|-----------|------------|-------|------|
| AAPL | +2.07% | +4.86% | +6.024% | ↑↑↑ | None |
| AMZN | +4.51% | −0.05% | −0.322% | ↓↓↓ | RS_MOMENTUM_DECAY ACTIVE (existing) |
| GOOGL | +14.06% | +13.06% | +7.585% | ↓↓↓ | **RS_DETERIORATING — NEW FLAG** |
| LLY | +3.95% | +4.00% | +8.032% | ↑ then ↑↑ | None |
| QQQ | +3.02% | +3.81% | +4.031% | ↑↑↑ | None |
| NVDA | (selling) | — | — | — | — |

**GOOGL — RS_DETERIORATING (new):**
- 3 consecutive declining EOD sessions: +14.06% → +13.06% → +7.585%
- RS still strongly POSITIVE (+7.585%) and BULLISH trend. NOT an exit signal.
- Actions: do NOT add to GOOGL; be ready to exit at first signal failure (trend break or RS turns NEGATIVE or 2-session NEUTRAL confirmation).
- Logged to behavioral-flags.jsonl.

---

## Step 7e — Earnings & News Check

**Earnings (confirmed):**
| Ticker | Next Date | Days Until | Flag |
|--------|-----------|-----------|------|
| AAPL | 2026-07-30 | 79 | None |
| AMZN | 2026-07-30 | 79 | None |
| GOOGL | 2026-07-23 | 72 | None |
| LLY | 2026-08-05 | 85 | None |
| NVDA | 2026-05-20 | 8 | None (>7d threshold; selling today) |
| QQQ | ETF | N/A | None (404 expected) |

No earnings constraints on any held position.

**News (significant headlines only):**
- GOOGL: Waymo recalls 3,800+ robotaxis due to software issue (mild negative — Waymo is AV moonshot, not core GOOGL revenue). Does not override hold signal; noted given RS_DETERIORATING context.
- QQQ/macro: Trump says Iran ceasefire "on life support" → geopolitical risk. Nasdaq futures soft pre-market. CPI expected 3.7% YoY (inflation concern, Fed cut timing pushed out). Consistent with soft equity pre-market open.
- LLY: RFK deprescribing push (ongoing pharma headwind; no LLY-specific catalyst). IVF benefit expansion positive. Net: neutral.
- AAPL: TSMC Arizona beats expectations (positive supply chain). Trump-Xi summit (positive for AAPL supply chain). No negative catalyst.
- AMZN: No AMZN-specific catalysts. OpenAI-MSFT deal (AMZN as AWS/Claude competitor — background noise). Neutral.

News conclusion: Macro headwinds (Iran, CPI) favor a cautious session open. No signals overridden. GOOGL Waymo recall tips toward extra caution given RS_DETERIORATING flag.

---

## Intents for 2026-05-12 Execution

### 1. NVDA — SELL 2.00 shares (CRITICAL — first action at 9:45 AM)
- RS 2-session NEGATIVE: SESSION 1 mid-session 5/11 (−1.50%) + SESSION 2 EOD 5/11 (−2.017%)
- GTC stop order `216377a3-76e3-486c-86a9-3206bc12e956` is live backstop; cancel BEFORE placing market sell
- Rationale: 2-session RS NEGATIVE confirmed per exit rules. Earnings 5/20 (8 days). No re-entry before earnings.
- Post-sell: ~$435 added to cash → cash ~$4,403 (~44.1% of remaining equity)

### 2. AAPL — HOLD at 8.35%
- RS +6.024% Very High. BULLISH. Vol_ratio 0.83 (weak).
- Below Very High tier floor (13%). Add conditional: price ≥ $294 at 9:45 AM AND market opens strong.
- Pre-market $292.16 < $294. Macro headwinds suggest soft open. No committed add today.
- If conditions met at 9:45 (unlikely): consider 0.3–0.5 shares (~$88–$148) → toward 9–10% equity.

### 3. AMZN — HOLD/WATCH at 7.91%
- RS −0.322% NEUTRAL. RS_MOMENTUM_DECAY active. Vol_ratio 0.72 (weak).
- BULLISH trend. No trim trigger (RS not < −1%).
- Counter resets ONLY at RS > 0%. Hold. Do NOT add.
- Pre-market price $266.96 (slightly below EOD $268.98). AMZN avg_entry $270.257 (Alpaca). Unrealized −1.22%.

### 4. GOOGL — HOLD at 16.74% — RS_DETERIORATING
- RS +7.585% Very High. BULLISH trend. But 3-session RS decay.
- Rationale: BULLISH trend intact, RS strongly positive despite decay. No exit signal yet.
- Do NOT add. Exit gate: Trend break (close < SMA_13 $374.00) OR RS turns NEGATIVE OR 2-session RS NEUTRAL confirmation.
- Waymo recall noted — not a sell signal but adds caution.
- Trailing activation: high_close $400.67 vs threshold $410.63 (gap $9.96). Unlikely to activate today given soft open.

### 5. LLY — HOLD at 12.73%
- RS +8.032% Very High. BULLISH. Vol_ratio 0.74 (weak).
- Pre-market $962.99. Warning zone $938.06 (gap $24.93). Hard stop $908.44.
- No add (weak volume, MIXED regime).
- Monitor closely: LLY is −2.48% unrealized; a continuation lower pushes toward warning zone.

### 6. QQQ — HOLD at 10.31%
- RS +4.031% High tier. BULLISH. Vol_ratio 0.94 (neutral).
- Macro headwinds today (Iran + CPI). No add. Hold.

### 7. Cash — ~39.7% pre-sell; ~44% post-NVDA-sell
- MIXED regime target 25–40%.
- Post-sell cash 44% slightly exceeds MIXED target. No qualifying tickers for new entries.
- Cash accumulation documented: No BEARISH→BULL transition; no non-held universe tickers with BULLISH trend + POSITIVE RS. This is a known constraint, not silent accumulation.
- Exception would be AAPL or QQQ adds, but both have weak volume and macro headwinds today. Deferred to execution assessment at 9:45 AM.

### No new entries
All non-held universe tickers BEARISH or NEGATIVE RS. Zero eligible candidates.

---

## Sector Concentration (post-NVDA-sell)
| Sector | Tickers | Approx % Equity |
|--------|---------|-----------------|
| Information Technology | AAPL | ~8.4% |
| Consumer Discretionary | AMZN | ~7.9% |
| Communication Services | GOOGL | ~16.7% |
| Health Care | LLY | ~12.8% |
| ETF | QQQ | ~10.4% |
| Cash | — | ~44% |

No sector concentration issues (all well below 40% limit).

---

## Carry-Forward from Last Session (5/11 EOD)

1. **NVDA SELL** — carried forward and confirmed. RS 2-session NEGATIVE. Action at 9:45 AM.
2. **AMZN RS_MOMENTUM_DECAY** — continues. RS −0.322% (NEUTRAL). No trim. Counter reset only at RS > 0%.
3. **GOOGL RS_DETERIORATING** — newly flagged today. RS still positive. Do not add. Watch.
4. **GOOGL trailing** — high_close $400.67 vs threshold $410.63. Gap $9.96. Unlikely to activate today.
5. **LLY** — stable but watch. Warning zone gap $24.93. Recover to $991.945 needed for trailing activation.
6. **AAPL** — conditional add gate ($294) not met pre-market. Assess at 9:45 AM.
7. **Week labeling** — Week 3. Confirmed against experiment-config.json.
8. **5/11 contradiction resolved** — AMZN trim on 5/11 was directionally correct. Process failure (pre-market didn't reconcile weekly-review carry-forward) was flagged by EOD 5/11. Noted.
9. **AMZN avg_entry discrepancy resolved** — Alpaca FIFO recalculation after trim. Updated position-highs.json entry_price to $270.257. Hard stop updated to $248.64.
