# Pre-Market Research — 2026-04-27 (Experiment Day 1)

**Routine:** pre-market-research
**Model:** claude-sonnet-4-6
**Time (ET):** ~8:45 AM ET
**Experiment status:** STARTED — Day 1 of 4-week window (ends 2026-05-22)

---

## Portfolio State

- **Equity:** $10,000.00 | **Cash:** $10,000.00 (100%) | **Positions:** 0
- **Cumulative return (agent):** 0.00%
- **SPY cumulative return:** +0.39% (start_price 711.20 → current 713.97, per benchmark tool)
- **Delta vs SPY:** −0.39% (agent was in cash pre-experiment; tracking begins today)

---

## Stop-Loss Audit

- No positions held. Nothing to check. No stop-losses triggered.

---

## Data Notes

- All 12 universe tickers + SPY returned **13 bars** (2026-04-08 → 2026-04-24). Requested 20.
- Using **SMA_13** as proxy for SMA_20 per learned behavior rule [W1|MEDIUM].
- Per rule: if close is within ~2% of SMA_13, treat trend as BORDERLINE. All eligible tickers are >2.5% above SMA_13 → signal is robust, not borderline.
- First session with ≥20 bars: switch to SMA_20 immediately and note.

---

## Universe Status

- **state/universe.json status: LOCKED** (operator locked 2026-04-26, before Day 1).
- Per strategy.md: "Universe = {SPY, QQQ} only **until operator locks**." Operator has locked.
- Full 12-ticker universe is active from Day 1. SPY remains benchmark only, not a position.

---

## Signal Table (SMA_13 proxy — not SMA_20)

SPY benchmark 10d_ROC: **+5.097%** (bars[-1]=713.97, bars[-11]=679.35 on 4/10)

| Ticker | SMA_13 | Close (4/24) | Trend | 10d_ROC | RS_spread | RS Status | Action |
|--------|--------|-------------|-------|---------|-----------|-----------|--------|
| MSFT | $404.99 | $424.59 | BULLISH | +14.48% | +9.38% | POSITIVE | BUY |
| AMZN | $246.43 | $263.96 | BULLISH | +10.71% | +5.61% | POSITIVE | BUY |
| NVDA | $196.26 | $208.18 | BULLISH | +10.38% | +5.28% | POSITIVE | BUY |
| QQQ | $635.45 | $663.92 | BULLISH | +8.63% | +3.54% | POSITIVE | BUY |
| GOOGL | $331.88 | $344.33 | BULLISH | +8.53% | +3.43% | POSITIVE | BUY |
| META | $657.95 | $674.93 | BULLISH | +7.16% | +2.06% | POSITIVE | BUY (6th, optional) |
| AAPL | $265.73 | $271.04 | BULLISH | +4.07% | −1.02% | NEGATIVE | NO ENTRY |
| XLE | $56.47 | $56.89 | BULLISH | −0.09% | −5.18% | NEGATIVE | NO ENTRY |
| LLY | $921.72 | $884.02 | BEARISH | −5.88% | −10.98% | NEGATIVE | NO ENTRY |
| JPM | $310.91 | $308.27 | BEARISH | −0.52% | −5.61% | NEGATIVE | NO ENTRY |
| BRK.B | $474.77 | $469.32 | BEARISH | −2.22% | −7.31% | NEGATIVE | NO ENTRY |
| XLV | $147.41 | $144.20 | BEARISH | −2.13% | −7.22% | NEGATIVE | NO ENTRY |

**High-conviction eligible** (RS_spread > 3% AND prior-day return > 1% — per strategy.md sizing rule):
- MSFT: RS_spread +9.38%, prior-day (4/24) return +2.13% ✓
- AMZN: RS_spread +5.61%, prior-day (4/24) return +3.49% ✓
- NVDA: RS_spread +5.28%, prior-day (4/24) return +4.26% ✓
- QQQ: RS_spread +3.54%, prior-day (4/24) return +1.92% ✓
- GOOGL: RS_spread +3.43%, prior-day (4/24) return +1.61% ✓
- META: RS_spread +2.06% — below 3% threshold. Standard only.

Note: High-conviction criteria are evaluated on Friday (4/24) closes. Execution routine must reconfirm at 9:45 AM today. If today's open gaps down, signals may not hold; default to 5% sizing unless confirmed.

---

## Market Read

- SPY trend: BULLISH (SMA_13 $697.94, close $713.97, +2.3% above SMA).
- Broad uptrend in evidence: 9 of 12 universe tickers are BULLISH (above SMA_13).
- Defensives weak: LLY, XLV, JPM, BRK.B all below SMA_13. Risk-on environment.
- Tech/growth leading: MSFT, NVDA, AMZN show strongest RS_spread (>5%).
- No early-close today. Normal session.

---

## Intents

**Primary buys (top 5 by RS_spread — execution routine to confirm at 9:45 AM):**

| # | Ticker | Action | Size | Rationale |
|---|--------|--------|------|-----------|
| 1 | MSFT | BUY | 5% (~$500) | RS_spread +9.38%, BULLISH — strongest RS in universe |
| 2 | AMZN | BUY | 5% (~$500) | RS_spread +5.61%, BULLISH — e-commerce/cloud outperforming |
| 3 | NVDA | BUY | 5% (~$500) | RS_spread +5.28%, BULLISH — momentum leader |
| 4 | QQQ | BUY | 5% (~$500) | RS_spread +3.54%, BULLISH — tech ETF beta |
| 5 | GOOGL | BUY | 5% (~$500) | RS_spread +3.43%, BULLISH — AI/search momentum |

**Optional 6th (lower conviction):**

| # | Ticker | Action | Size | Rationale |
|---|--------|--------|------|-----------|
| 6 | META | BUY | 5% (~$500) | RS_spread +2.06%, BULLISH — eligible but below high-conviction threshold |

**Default sizing: 5% each.** All 5 primary + 1 optional at 5% = 30% deployed, 70% cash → above 25% floor ✓.

**High-conviction upsize to 7%:** Eligible for MSFT, AMZN, NVDA, QQQ, GOOGL IF execution routine reconfirms: (a) both signals still hold at 9:45 AM, AND (b) today's open vs yesterday's close still > 1% gain. Do NOT upsize pre-emptively. If upsized, must document in execution journal.

**Sector concentration check (at 5% × 5 positions):**
- IT (MSFT + NVDA): 10% — under 40% ✓
- CommSvc (GOOGL): 5% — under 40% ✓
- ConsDisc (AMZN): 5% — under 40% ✓
- ETF (QQQ): 5% — under 40% ✓

**Not entering:** AAPL (RS NEGATIVE −1.02%), XLE (RS NEGATIVE), LLY/JPM/BRK.B/XLV (Trend BEARISH + RS NEGATIVE).

---

## Carry-Forward from Last Session

- Last session (weekly review 2026-04-24) flagged: "Revalidate QQQ — SPY rallied +0.78% on 4/24, which may compress QQQ RS_spread."
  - Resolution: QQQ RS_spread is +3.54% as of 4/24. SPY's strong Friday did compress the spread from ~+2.58% (4/23 prior session estimate), but the signal remains strongly POSITIVE. No concern.
- Universe locked by operator on 2026-04-26 — noted and applied. Full 12-ticker universe active from Day 1. This resolves the "week 1 SPY/QQQ only" restriction.
- SPY benchmark start_price = 711.2 per tool (appears to reference a recent SPY close used as baseline). Agent starts at $10,000 / 0.00% vs SPY +0.39%. Pre-experiment gap — not a trading failure.
- Weekly review flagged: fractional share support for Alpaca to be confirmed. At $10k equity with 5% = $500 per position: QQQ ~0.75 shares, MSFT ~1.18 shares, AMZN ~1.89 shares, NVDA ~2.40 shares, GOOGL ~1.45 shares — all fractional. Execution routine should confirm validator accepts fractional quantities; if not, use whole-share floor.

---

## Errors / Flags

- None. All tools returned clean output.
