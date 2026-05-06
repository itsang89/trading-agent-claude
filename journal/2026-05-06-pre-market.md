# Pre-Market Research — 2026-05-06 (Experiment Day 8)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:35 AM ET (pre-market, opens 9:30 AM)
**Week number:** 2

---

## Market Status
Trading day. Market opens 9:30 AM, closes 4:00 PM ET. No early close.

## Regime: MIXED — 6/12 universe tickers BULLISH
5-7 range: be selective. Limit new entries to top 3 RS per session (applies to new entries; adds to existing positions are unrestricted).

BULLISH: QQQ, XLE, AAPL, GOOGL, LLY, AMZN
BEARISH: XLV, NVDA, MSFT, META, JPM, BRK.B

## Portfolio State
- Equity: $10,044.36
- Cash: $5,277.06 (52.5%)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, QQQ, XLE)
- Cumulative vs SPY: agent +0.44% vs SPY +1.19% (delta −0.75 pp; agent trailing SPY)
- SPY start: $715.165 (2026-04-27); latest close: $723.71

## Stop-Loss & Trailing Stop Audit

Hard stops and trailing checks (pre-market prices from get_positions):

| Ticker | Avg Entry | Hard Stop | Trailing | Threshold | PM Price | Status |
|--------|-----------|-----------|----------|-----------|----------|--------|
| AAPL | $268.81 | $247.31 | No | >$295.69 | $281.90 | PASS |
| AMZN | $264.95 | $243.76 | No | >$291.45 | $274.45 | PASS |
| GOOGL | $366.98 | $337.62 | No | >$403.68 | $395.00 | PASS |
| LLY | $981.72 | $903.18 | No | >$1,079.89 | $990.50 | PASS |
| QQQ | $661.81 | $608.87 | No | >$727.99 | $689.78 | PASS |
| XLE | $59.02 | $54.30 | No | >$64.922 | $57.14 | PASS |

No trailing stops active. No stop triggers. No warning zones (all above avg_entry × 0.95).

**XLE FLAG:** Pre-market price $57.14 is below SMA_13 $57.48. If XLE closes below SMA_13 today → Trend BEARISH → queue sell for 5/7 execution. Oil prices are FALLING per news (ceasefire premium unwinding). Do NOT add XLE.

## Signal Table (SMA_13 — 13 bars available; Learned Behavior rule applies)
10d reference: 2026-04-21 (bars[-11]). SPY_10d_ROC = +2.814% (benchmark denominator).
Bars: 13 sessions (2026-04-17 through 2026-05-05).

| Ticker | SMA_13 | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|--------|-------|-------|---------|-----------|-----------|------------|--------|
| SPY | $713.50 | $723.71 | BULLISH | +2.81% | — | 1.02 | — | benchmark |
| AAPL | $272.91 | $284.18 | BULLISH | +6.77% | +3.96% | 1.11 | High | ADD |
| AMZN | $260.46 | $273.56 | BULLISH | +9.49% | +6.67% | 0.84 | Very High | ADD |
| GOOGL | $355.90 | $388.41 | BULLISH | +16.88% | +14.07% | 0.92 | Very High | ADD (conditional) |
| LLY | $917.07 | $988.50 | BULLISH | +9.48% | +6.66% | 1.06 | Very High | ADD |
| QQQ | $660.74 | $681.53 | BULLISH | +5.79% | +2.97% | 0.54 | Standard | HOLD |
| XLE | $57.48 | $59.45 | BULLISH | +6.43% | +3.61% | 0.60 | High | WATCH |
| XLV | $145.39 | $145.31 | BEARISH | −0.43% | −3.24% | — | — | NO ENTRY |
| NVDA | $203.53 | $196.50 | BEARISH | −1.66% | −4.47% | — | — | NO ENTRY |
| MSFT | $420.33 | $411.33 | BEARISH | −3.00% | −5.81% | — | — | NO ENTRY |
| META | $653.25 | $604.92 | BEARISH | −9.54% | −12.35% | — | — | NO ENTRY |
| JPM | $311.43 | $309.36 | BEARISH | −1.16% | −3.98% | — | — | NO ENTRY |
| BRK.B | $471.36 | $465.49 | BEARISH | −0.63% | −3.44% | — | — | NO ENTRY |

## position-highs.json Updates (Step 7c)
- AAPL: close $284.18 > prior high_close $282.66 → UPDATED to $284.18
- GOOGL: close $388.41 > prior high_close $385.79 → UPDATED to $388.41
- AMZN: close $273.56 < high_close $273.72 → no update
- LLY: close $988.50 < high_close $991.945 → no update
- QQQ: close $681.53 < high_close $681.55 → no update
- XLE: close $59.45 < high_close $59.63 → no update

Trailing activation rechecks after updates:
- AAPL new high_close $284.18 < threshold $295.69 → still inactive
- GOOGL new high_close $388.41 < threshold $403.68 → still inactive

## RS Momentum Decay Check (Step 7d)
Comparing 5/5 mid-session RS (Apr 21 reference, same window) vs today:

| Ticker | 5/5 mid RS | Today RS | Trend | Flag |
|--------|-----------|---------|-------|------|
| AAPL | +3.35% | +3.96% | ↑ | None |
| AMZN | +6.70% | +6.67% | ↔ | None |
| GOOGL | +13.06% | +14.07% | ↑ | None |
| LLY | +7.01% | +6.66% | ↓ 1 session | Monitor |
| QQQ | +2.94% | +2.97% | ↑ | None |
| XLE | +3.75% | +3.61% | ↓ 1 session | Monitor (oil falling) |

No RS_MOMENTUM_DECAY flags. Only 1 session of same-reference comparison available.
LLY and XLE show slight RS decline — one session, not 3 consecutive. Monitor only.

## Earnings Check (Step 7e — active 2026-05-05)
- AAPL: next 2026-07-30 (85 days) — no flag
- AMZN: next 2026-07-30 (85 days) — no flag
- GOOGL: next 2026-07-23 (78 days) — no flag
- LLY: next 2026-08-05 (91 days) — no flag
- QQQ, XLE: ETFs, no earnings data
No EARNINGS_IMMINENT or EARNINGS_THIS_WEEK constraints.

## News Check (Step 7e)
- **AAPL:** Beat-and-raise earnings triple play list (positive). AI/chip supply chain diversification. No negative catalyst.
- **AMZN:** "Earnings mirage" analyst piece warns OpenAI/Anthropic drive 50% of cloud backlog in circular loop (bear case debate, not company-specific negative). Other coverage bullish on AI/cloud. Signals remain BULLISH; bear article is not a sell catalyst.
- **GOOGL:** OpenAI executives departing for Google (positive talent signal). Google testing "Remy" AI agent (positive). Included in AI winners list. No negative catalyst.
- **LLY:** Omvoh 4-year IBD disease clearance data (positive, supports GLP-1/biologic pipeline). RFK Jr. psychiatric drug initiative (not relevant to LLY's GLP-1 focus). No negative catalyst.
- **QQQ:** Third-largest 21-day inflows on record (strongly positive). Nasdaq 100 hit fresh record on 5/5. Trump pausing "Project Freedom" → futures rising today. No negative catalyst.
- **XLE:** KEY NEGATIVE — "S&P 500 Hits New High As Oil Prices Fall" confirms oil premium unwinding (Iran ceasefire talks resolving). Brent was $114+ on 5/4; now declining. This explains XLE's pre-market drop from $59.45 to $57.14 (−3.88%). XLE Trend at risk today. Signals are borderline with news tipping toward caution.

**News conclusion:** No exit catalysts for AAPL/AMZN/GOOGL/LLY/QQQ. XLE oil-driven decline is a meaningful negative timing signal. Do not add XLE. Monitor Trend break at EOD.

## Intents for 2026-05-06 Execution

Cash commentary: 52.5% cash in MIXED regime with 4 Very-High/High conviction positions is excessive. Adds to AAPL, LLY, and AMZN are overdue. GOOGL conditional add would bring cash to ~35%.

### 1. LLY ADD ~0.81 shares (Very High conviction)
- RS +6.66%, Trend BULLISH. Position at 5.03% of equity vs 13-20% Very High tier.
- RS concern from 5/5 AM (+3.88%) fully cleared — 5/5 mid recovered to +7.01%; today +6.66%.
- Dollar add: 13% × $10,044 = $1,305 target − $505 current = $800. At ~$990.50 → 0.81 shares.
- New avg_entry est.: (0.51 × $981.72 + 0.81 × $990.50) / 1.32 ≈ $987.12
- New hard stop: $987.12 × 0.92 ≈ $908.15
- Earnings 91 days out. News positive. Vol_ratio 1.06 supports tier.
- RATIONALE: LLY is deeply undersized for its conviction tier. First-session decline flag from 5/5 AM fully resolved. Strong positive fundamental (Omvoh data). No near-term risk events.
- Post-add: ~1.32 shares, ~$1,305, ~13.0% of equity.

### 2. AAPL ADD ~1 share (High conviction)
- RS +3.96%, Trend BULLISH. Position at 5.22% vs 8-13% High tier.
- Vol_ratio 1.11 (near normal, supports High tier). Earnings 85 days out.
- Dollar add: 8% × $10,044 = $804 target − $524 current = $280. At ~$281.90 → ~0.99 shares → round to 1 share.
- New avg_entry est.: (1.86 × $268.81 + 1 × $284.18) / 2.86 ≈ $274.19
- New hard stop: $274.19 × 0.92 ≈ $252.25
- Post-add: 2.86 shares, ~$808, ~8.04% of equity.

### 3. AMZN ADD ~0.85 shares (Very High conviction)
- RS +6.67%, Trend BULLISH. Position at 10.68% vs 13-20% Very High tier.
- Vol_ratio 0.84 (below 1.0 but above 0.8; no tier downgrade per strategy).
- "Earnings mirage" article is a valuation debate, not a signal change.
- Dollar add: 13% × $10,044 = $1,306 target − $1,073 current = $233. At ~$274.45 → 0.85 shares.
- New avg_entry est.: (3.91 × $264.954 + 0.85 × $274.45) / 4.76 ≈ $266.69
- New hard stop: $266.69 × 0.92 ≈ $245.35
- No trailing stop active (high_close $273.72 < threshold $291.45). No stop to cancel.
- AMZN stop order will FAIL again (fractional/DAY order error — documented in notes-for-operator.md). Manual enforcement continues.
- Post-add: 4.76 shares, ~$1,306, ~13.0% of equity.
- RATIONALE: AMZN is undersized for Very High conviction tier. Adding to tier floor. Fundamentals remain strong (AWS, AI demand). No earnings for 85 days.

### 4. GOOGL ADD ~0.91 shares — CONDITIONAL on price up >1% at 9:45 AM (Very High conviction)
- RS +14.07%, Trend BULLISH. Highest RS in universe. Position at 13.41% vs 13-20% tier.
- Pre-market shows +$6.59 (+1.70% from $388.41 close to $395.00) — condition appears met.
- Confirm at execution: if price ≥ $392.29 (>1% above yesterday close), add.
- Target: 17% × $10,044 = $1,708 − $1,347 current = $361. At ~$395 → 0.91 shares.
- New avg_entry est.: (3.41 × $366.978 + 0.91 × $395.00) / 4.32 ≈ $372.88
- New hard stop: $372.88 × 0.92 ≈ $343.05
- New trailing threshold: $372.88 × 1.10 = $410.17 (deactivated; prior deactivated threshold was $403.68; new threshold rises to $410.17)
- RATIONALE (≥10%): GOOGL at +14.07% RS_spread is the strongest position in portfolio. Very High tier (>5% RS) + price up >1% condition both met. Adding from 13.41% to ~17% fills to tier midpoint. OpenAI talent departing to Google + new AI agent "Remy" reinforce positive outlook. MIXED regime requires selectivity — adding to #1 RS position satisfies that constraint.
- Post-add: 4.32 shares, ~$1,708, ~17.0% of equity.

### 5. QQQ HOLD
- RS +2.97% (Standard tier), vol_ratio 0.54 (weak). Position 5.15% at Standard tier floor. No add given weak volume.

### 6. XLE WATCH — DO NOT ADD
- Pre-market $57.14 < SMA_13 $57.48. Oil falling per news. Trend potentially breaking today.
- XLE at $57.14 estimated RS: (57.14 - 55.86) / 55.86 = +2.29%, RS_spread = 2.29% - 2.81% = -0.52% (NEUTRAL).
- If EOD close < SMA_13 $57.48 → flag Trend BEARISH → queue sell for 5/7.
- If EOD close > SMA_13 AND RS_spread > 0% → clear flag, remain HOLD.
- XLE stop_order_id: 9c12ad6b at $54.30 — cancel before any sell.

### Cash Projection Post-Adds (estimated):
| Add | Est. Cost |
|-----|----------|
| LLY +0.81 | ~$802 |
| AAPL +1 | ~$282 |
| AMZN +0.85 | ~$233 |
| GOOGL +0.91 | ~$360 |
| **Total** | **~$1,677** |

Cash after: $5,277 − $1,677 = ~$3,600 (~35.8% of equity). Within MIXED target 25-40%.

## Sector Concentration Check (post-adds)
- IT (AAPL): ~8.0% — fine
- Consumer Disc (AMZN): ~13.0% — fine
- Comm Services (GOOGL): ~17.0% — fine
- Health Care (LLY): ~13.0% — fine
- ETF (QQQ): ~5.2%, ETF (XLE): ~8.0% — fine
No sector exceeds 40%.

## Carry-Forward from Last Session (5/5 mid-session)
1. AMZN stop order failure (fractional issue) — still no stop_order_id; hard stop $243.76 manual. After today's add, new hard stop ~$245.35.
2. AAPL, GOOGL, LLY, QQQ — no stop_order_id; manual enforcement continues.
3. XLE — stop_order_id: 9c12ad6b at $54.30 ✓ (still valid; cancel before any sell).
4. AAPL WATCH from 5/5 AM cleared (+0.083% → +3.35% mid-session → +3.96% today).
5. LLY first RS decline concern from 5/5 AM (+3.88%) fully cleared (+7.01% mid-session → +6.66% today).
6. GOOGL trailing threshold remains deactivated; new threshold after today's add will be $410.17.

## Errors / Flags
None. All tools returned successfully.
