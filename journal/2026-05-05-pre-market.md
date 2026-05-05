# Pre-Market Research — 2026-05-05 (Experiment Day 7)
**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:34 AM ET (pre-market, opens 9:30 AM)
**Week number:** 2

---

## Regime: MIXED — 6/12 universe tickers BULLISH
5-7 range: be selective. Not bear. Limit new entries to top 3 by RS_spread; applies to new entries (not adds to existing positions).

BULLISH: QQQ, XLE, AAPL, GOOGL, LLY, AMZN
BEARISH: XLV, NVDA, MSFT, META, JPM, BRK.B

## Portfolio State
- Equity: $10,007.16
- Cash: $5,614.35 (56.1%)
- Positions: 6 (AAPL, AMZN, GOOGL, LLY, QQQ, XLE)
- Cumulative vs SPY: agent +0.072% vs SPY +0.409% (delta −0.337 pp; improved from −0.481 pp at EOD 5/4 due to pre-market price recovery)
- Market status: trading day, pre-market

## Stop-Loss Status
All positions PASS. No trailing stops active. No warning zones.

| Ticker | Avg Entry | Current | Hard Stop | Trailing Active | Threshold | Unrealized | Status |
|--------|-----------|---------|-----------|-----------------|-----------|------------|--------|
| AAPL | $268.81 | $275.77 | $247.31 | No | >$295.69 | +$12.95 (+2.59%) | PASS |
| AMZN | $260.56 | $273.55 | $239.71 | No | >$286.62 | +$37.81 (+4.99%) | PASS |
| GOOGL | $366.98 | $384.51 | $337.62 | No* | >$403.68 | +$59.78 (+4.78%) | PASS |
| LLY | $981.72 | $965.38 | $903.18 | No | >$1,079.89 | −$8.33 (−1.66%) | PASS |
| QQQ | $661.81 | $677.85 | $608.87 | No | >$727.99 | +$12.03 (+2.42%) | PASS |
| XLE | $58.98 | $59.38 | $54.26 | No | >$64.88 | +$5.20 (+0.68%) | PASS |

*GOOGL trailing deactivated after 5/1 add (high_close $385.79 < threshold $403.68).

## Signal Table (SMA_13 — 13 bars available; per Learned Behavior rule)
10d reference date: 2026-04-20 (bars[-11]). SPY_10d_ROC = +1.312% (benchmark denominator).

| Ticker | SMA_13 | Close | Trend | 10d_ROC | RS_spread | Vol_ratio | Conviction | Action |
|--------|--------|-------|-------|---------|-----------|-----------|------------|--------|
| SPY | $711.79 | $718.09 | BULLISH | +1.31% | — | 0.85 | — | benchmark |
| AAPL | $271.31 | $276.87 | BULLISH | +1.40% | +0.08% | 1.03 | Borderline | HOLD |
| AMZN | $258.63 | $272.10 | BULLISH | +9.57% | +8.26% | 0.86 | Very High | ADD |
| GOOGL | $351.87 | $383.21 | BULLISH | +13.56% | +12.25% | 0.95 | Very High | HOLD |
| LLY | $910.56 | $968.18 | BULLISH | +5.19% | +3.88% | 0.97 | High | HOLD |
| QQQ | $657.58 | $672.78 | BULLISH | +4.02% | +2.71% | 0.56 | Standard | HOLD |
| XLE | $57.26 | $59.41 | BULLISH | +7.87% | +6.56% | 0.88 | Very High | HOLD |
| XLV | $145.50 | $144.78 | BEARISH | −1.80% | −3.11% | 1.61 | — | NO ENTRY |
| NVDA | $203.67 | $198.56 | BEARISH | −1.76% | −3.07% | 0.95 | — | NO ENTRY |
| MSFT | $421.01 | $413.64 | BEARISH | −1.07% | −2.38% | 0.84 | — | NO ENTRY |
| META | $658.79 | $610.30 | BEARISH | −9.04% | −10.35% | 0.84 | — | NO ENTRY |
| JPM | $311.46 | $307.71 | BEARISH | −2.96% | −4.27% | 0.83 | — | NO ENTRY |
| BRK.B | $472.09 | $468.47 | BEARISH | −0.74% | −2.06% | 1.58 | — | NO ENTRY |

Note: All BULLISH tickers are currently held. No new entry candidates available.

## RS Momentum Decay Check (Step 7d)
3-session RS trends (4/30 EOD → 5/1 EOD → 5/4 EOD per prior journals):
- AAPL: +0.56% → +2.43% → +0.08% — not 3-session declining (V-shape, then down)
- AMZN: +3.73% → +0.68% → +8.26% — strongly recovered
- GOOGL: +12.18% → +8.88% → +12.25% — stable/strong
- LLY: N/A → +11.93% → +3.88% — only 2 sessions; 1 decline
- QQQ: +1.84% → +0.64% → +2.71% — recovered
- XLE: +2.94% → −1.64% → +6.56% — strongly recovered

**No RS_MOMENTUM_DECAY flags.**

Watch (not flagged): AAPL RS barely positive (+0.083%). If RS drops below 0% at EOD 5/5, flag WATCH — RS FIRST SESSION NEUTRAL/NEGATIVE.
Watch: LLY first RS decline (+11.93% → +3.88%). Monitor session 2 before exit consideration.

## position-highs.json Update
No updates needed — all current closes (bars[-1]) are below respective high_close values:
- AAPL: close $276.87 < high_close $280.75
- AMZN: close $272.10 = high_close $272.10 (equal, no update)
- GOOGL: close $383.21 < high_close $385.79
- LLY: close $968.18 < high_close $981.72
- QQQ: close $672.78 < high_close $674.85
- XLE: close $59.41 < high_close $59.63

## Earnings Check (Step 7e — active 2026-05-05)
- AAPL: next earnings 2026-07-30 (86 days) — no flag
- AMZN: next earnings 2026-07-30 (86 days) — no flag
- GOOGL: next earnings 2026-07-23 (79 days) — no flag
- LLY: no future earnings found — no flag
- QQQ/XLE: ETFs, no earnings data — no flag
No EARNINGS_IMMINENT or EARNINGS_THIS_WEEK constraints. AMZN add is not blocked by earnings.

## News Check (Step 7e — active 2026-05-05)
Scanning for negative catalysts on held positions:
- AAPL: iPhone 17 world's best-selling smartphone (positive). Exploring Intel/Samsung chip suppliers to reduce TSMC reliance (supply chain diversification, neutral-to-positive). No negative catalyst.
- AMZN: BNP Paribas raises PT to $345, citing 50% AWS backlog surge and AI demand (positive). Amazon logistics expansion displacing FedEx/UPS (positive for AMZN). No negative catalyst.
- GOOGL: Congresswoman disclosed selling GOOGL in April (minor institutional signal; not a negative catalyst for signal purposes). OpenAI AI phone competitor article (minor tech competition context). No material negative catalyst.
- LLY: Deloitte note on GLP-1 boom driving rising competition (sector-level, not company-specific; cautionary but not actionable). LLY acquired Profluent for $2.2B (R&D, neutral). No negative catalyst.
- QQQ: Iran struck UAE port (5/4), oil +5%, market dropped. US-Iran ceasefire talks mentioned for 5/5 (risk-off reduction). Macro volatility context noted.
- XLE: Oil at $114+ Brent (strongly positive for XLE). OPEC+ adds 188K bpd starting June (mild headwind). Iran-ceasefire talks today may reduce geopolitical oil premium — monitor.

**News conclusion:** No negative catalysts that tip borderline signals toward exit. AMZN catalyst is strongly positive; XLE near-term tailwind but oil premium may unwind on ceasefire.

## Intents for 2026-05-05 Execution

1. **AAPL HOLD** — RS +0.083% (Borderline). Trend BULLISH. Do not add (RS < 1%, vol ratio near 1 but RS too weak). Monitor: if close < 0% RS at EOD, flag WATCH-FIRST-NEGATIVE. News positive; no exit catalyst.

2. **AMZN ADD ~1.85 shares** (Very High conviction)
   - RS +8.26%, Trend BULLISH. Position at 7.95% equity vs 13–20% Very High tier.
   - Target: 13% × $10,007 = $1,301. Current MV $796. Dollar add ≈ $505. Shares ≈ 1.85 at ~$273.55.
   - After add: ~4.76 shares, new avg_entry ~$265.61, new hard stop ~$244.36.
   - Catalyst: BNP $345 PT, 50% AWS backlog surge, AI demand. No earnings for 86 days.
   - Vol_ratio 0.86 (above 0.8, no tier downgrade). MIXED regime supports selective adds to highest-conviction existing positions.
   - No trailing stop to cancel (trailing inactive; no stop_order_id in position-highs.json).
   - Execution: use place_order.py (no --stop-pct since add); after fill, place new stop via place_stop_order.py at new_avg_entry × 0.92; update position-highs.json.
   - RATIONALE: AMZN is the clearest add candidate — underweighted vs signal strength, strong fundamental catalyst today, and 10d return durability confirmed (window-roll concern from EOD 5/4 resolved: signal genuine, not purely artifact).

3. **GOOGL HOLD** — RS +12.25% (Very High). Position at 13.1% equity, within 13–20% tier. Trailing stop deactivated (needs high_close >$403.68). Could add toward ceiling but Very High tier requires price +>1% today (unverifiable pre-market) and trailing is deactivated. Hold at current size.

4. **LLY HOLD** — RS +3.88% (High). Position at 4.92% equity (below High tier floor of 8%). First RS decline session (+11.93% → +3.88%). Do NOT add per monitoring stance until RS re-confirms for 1 session. 2-session exit rule does not apply (RS still POSITIVE). LLY undersized for tier but first-session RS decline warrants caution.

5. **QQQ HOLD** — RS +2.71% (Standard). Vol_ratio 0.56 (weak volume confirmation). Position at 5.08% equity, within Standard tier (5-8%). No add given weak volume signal.

6. **XLE HOLD / reassess at mid-session** — RS +6.56% (Very High). Position at 7.71% equity vs 13–20% tier. Oil spike (+5%) is positive but OPEC+ supply increase starting June is a near-term headwind, and US-Iran ceasefire talks may deflate geopolitical oil premium today. Vol_ratio 0.88 (near normal). Defer add decision to 1:30 PM mid-session after observing oil price action and XLE's intraday performance. If oil holds above $110 and XLE is BULLISH with strong volume, add ~1.85 shares at mid-session.

## Cash Commentary
Cash at 56.1% exceeds MIXED regime target of 25–40%. After AMZN add (~$505), cash drops to ~$5,109 (51%). Still elevated. XLE add (if executed at mid-session) would bring cash to ~$4,604 (46%). Both adds are warranted by signal quality; MIXED regime selectivity is satisfied (limiting to top-2 highest RS additions). Silent cash accumulation in a 6/12 BULLISH universe with high-conviction positions is not acceptable per strategy framework.

## Carry-Forward from Last Session (EOD 5/4, market-open-execution 5/4)
- RS values at EOD 5/4 match today's computed values (same close data, expected).
- AMZN and XLE RS confirmed post-window-roll as genuine — not pure artifact (10d return robust from 4/20 base).
- AAPL RS +0.084% → today +0.083% (marginal drift, below Borderline minimum of 1%; no add warranted).
- LLY: first RS decline confirmed (+11.93% → +3.88%). 2-session rule clock starts today.
- GOOGL trailing threshold $403.68 not breached; still deactivated.
- Missing execution routine pattern from 5/4 noted in notes-for-operator.md.

## Sector Concentration Check
Post-AMZN add (estimated):
- Information Technology: AAPL ~5.1% — no issue
- Communication Services: GOOGL ~13.1%
- Consumer Discretionary: AMZN ~13.0% (after add)
- Health Care: LLY ~4.9%
- ETFs: QQQ ~5.1%, XLE ~7.7%
No sector exceeds 40%. IT+CommSvc+CD+HealthCare all well below limit.

## Errors / Flags
None. All tools completed successfully. News tools operational (first day active per 2026-05-05 activation date).
