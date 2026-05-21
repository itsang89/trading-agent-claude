# LLM Trading Agent — Full Experiment Report

**Experiment:** Paper-trade US equities on Alpaca, mandate to beat SPY over 4 weeks
**Capital:** $10,000 notional
**Start:** 2026-04-27 | **Halted:** 2026-05-12 (Day 12 of planned 20)
**Model:** claude-sonnet-4-6 (primary), with some sessions on other models

---

## 1. Final Performance Snapshot

| Metric | Agent | SPY Benchmark |
|--------|-------|---------------|
| Cumulative return | **+0.30%** (+$30) | **+3.36%** |
| Week 1 return | −0.068% | +0.745% |
| Week 2 return | +0.560% | +2.368% |
| Week 3 (partial, 2 days) | ~−0.20% | ~+0.225% |
| Delta vs SPY at halt | **−3.1 pp** | — |
| Total trades placed | 27 (20 buys, 7 sells) | — |
| Validator rejections | 0 | — |
| Hard stop-losses triggered | 1 (META) | — |
| Soft exits (trend/RS) | 4 (MSFT, NVDA, XLE, NVDA re-entry) | — |

**The agent failed its mandate.** SPY gained +3.36% over 12 days; the agent gained +0.30%, trailing by ~3.1 percentage points at halt.

---

## 2. Trade History & Position Timeline

### Opening Positions (2026-04-27, Day 1)
Six positions opened simultaneously: MSFT, AMZN, NVDA, GOOGL, META, QQQ. Portfolio went from 100% cash to ~30% cash overnight.

### Week 1 Exits (2026-04-28–05-01)
| Date | Ticker | Reason | Loss/Gain |
|------|--------|--------|-----------|
| 4/30 | META | Hard stop (−10.62%, overnight gap) | −$49 realized |
| 4/30 | MSFT | Trend break (price < SMA) | −4.9% |
| 4/30 | NVDA | Trend break (price < SMA) | −4.3% |

All three exits were from positions opened only 3 days earlier. Cash freed: ~$1,500. New entries the same day: AMZN add, XLE.

### Week 2 Entries & Exits
Added to AAPL (4/29), LLY (5/1), AMZN (5/5, 5/6), AAPL (5/6), GOOGL (5/6), QQQ (5/7), NVDA re-entry (5/8). XLE sold 5/6 on trend break (oil price catalyst + technical). Cash ranged from 40–56% throughout.

### Week 3 (Partial)
AMZN trimmed 5/11 (RS deterioration). NVDA sold 5/12 (RS 2-session negative). Experiment halted same day.

### Final Positions at Halt (5/12 post-execution)
| Ticker | Qty | Avg Entry | Last Price | Unrealized | % Equity |
|--------|-----|-----------|-----------|-----------|---------|
| AAPL | 2.86 | $273.91 | ~$293 | +6.8% | 8.4% |
| AMZN | 2.95 | $270.26 | ~$265 | −1.9% | 7.8% |
| GOOGL | 4.32 | $373.30 | ~$388 | +4.1% | 16.7% |
| LLY | 1.32 | $987.44 | ~$967 | −2.1% | 12.9% |
| QQQ | 1.45 | $678.38 | ~$709 | +5.2% | 10.3% |
| Cash | — | — | — | — | ~44% |

---

## 3. What Caused the Underperformance — Root Cause Analysis

### A. Cash Drag (Primary Driver, ~2.5 pp impact)
Throughout both full weeks, the portfolio carried 40–56% cash. In a bull market where SPY gained +3.36%, every dollar in cash is a dollar not compounding. The invested portion of the portfolio performed reasonably — GOOGL, QQQ, and AAPL were all positive. But half the capital was sitting idle.

**Why the cash was so high:**
- Week 1: Three exits on Day 4 (META, MSFT, NVDA) freed ~$1,500. Redeployment was slow — AAPL and LLY were added 4 days later.
- Week 2: Regime was classified as MIXED (5–7/12 universe bullish), which calls for 25–40% cash conservatism. Even when BULL confirmed on Day 7, only QQQ was added that day. The weekly review explicitly flagged this as a sizing error.
- The strategy's cash accountability rule said "every idle dollar is a decision" — but the agent consistently explained the cash rather than deploying it.

### B. Early Exits from Winners (Week 1)
MSFT and NVDA were sold on a mid-session trend check (4/30) after only 3 days of holding. Both tickers recovered in subsequent weeks. NVDA was re-entered on 5/8 at a higher price ($216.63 vs original $209.45). The rules were followed correctly, but the strategy's trend filter can whipsaw positions in volatile conditions.

### C. META Overnight Gap (Execution Risk)
META's 8% hard stop should have capped loss at ~$49. Instead, the stock gapped overnight from ~$669 to ~$609 — a $60 gap — and the realized loss was −10.62%. This is inherent market risk, not a rule failure, but it reveals that the 8% stop doesn't protect against opening gaps on news events.

### D. Strategy's Signal Lag
The 10-day Relative Strength calculation looks backward. By the time a ticker shows RS_spread > 5% (very high conviction), much of the move may already have happened. GOOGL peaked near $400 and the RS was still showing +14% — but the stock was already deteriorating. The signal is good at confirming trends, less good at timing.

---

## 4. What the Agent Did Well

### Rule Adherence Was Near-Perfect
Every exit rule was executed without hesitation. META's stop triggered — sold immediately at open, no rationalization to hold. MSFT and NVDA trend broke — sold same session. XLE showed news-aligned technical break — sold mid-session. NVDA hit 2-session RS negative — sold next morning. The agent never argued against its own rules.

### Self-Awareness and Contradiction Tracking
The agent correctly flagged its own contradictions (e.g., the AMZN trim was executed at RS=−0.05% when the pre-market journal said trigger at −1%). It logged this to behavioral-flags.jsonl, explained the root cause (pre-market failed to reconcile weekly-review carry-forward), and moved on.

### Trailing Stop and RS Counter Mechanics
The RS_MOMENTUM_DECAY flags were written before exits triggered, in sequence. The 2-session confirmation window was respected — no premature sells on single-session drops. The NEUTRAL zone (−1% to 0%) was correctly distinguished from NEGATIVE (<−1%), preventing false exits (LLY recovered after touching −0.215%).

### News Integration (From 5/5 onward)
XLE's sell was the clearest example: oil price decline + Iran ceasefire talks confirmed the technical break that was forming. The agent correctly weighted news as a secondary confirming signal rather than overriding the technical signal.

### Sizing Rationale Was Documented
Every ≥10% position included written rationale. The GOOGL add-and-trailing-stop-deactivation issue (a subtle mechanical interaction) was caught and logged.

---

## 5. Operational / Infrastructure Issues

These are separate from trading decisions but significantly affected the experiment quality:

| Issue | Severity | Impact |
|-------|----------|--------|
| **Fractional stop orders rejected by Alpaca** (GTC not supported for fractional shares) | HIGH | All 6 positions had manual-only stops. If a routine missed, zero automatic downside protection. |
| **Midsession routine missing on most days** | HIGH | Ran only 1/5 days in Week 1, 3/5 in Week 2. Intraday signals unmonitored most of the time. |
| **EOD routine running late or missing** | MEDIUM | Metrics CSV incomplete. Daily equity timestamped to wrong date. |
| **Git push failures** (403 errors, branch conflicts) | MEDIUM | Remote history lagged local state; hard to audit externally. |
| **Email tool permanently broken** | LOW | 100% failure rate across all 6+ attempts. Non-blocking per learned behavior. |
| **Model inconsistency** (some sessions ran `opencode/hy3-preview-free`) | LOW | No observable behavioral differences, but consistency unverified. |
| **Metrics CSV only had 3 rows** (out of 12 trading days) | MEDIUM | No automated quantitative tracking. All analysis reconstructed from journals. |

---

## 6. Behavioral Observations — What This Experiment Reveals About LLM Trading Agents

### Finding 1: LLMs Follow Rules Extremely Well, But Don't Adapt to Market Context
The agent applied the strategy mechanically and correctly. It never broke a rule. But it also couldn't adapt when the rule was producing the wrong outcome. High cash in a bull market is the textbook example — the strategy said "MIXED regime = 25–40% cash," and the agent documented this correctly every session, even as SPY ran +2.4% in a week.

A human trader would override their own framework and deploy. The agent wrote good commentary about why it wasn't deploying.

### Finding 2: Overnight Gap Risk Is Structural, Not Solvable by Rules
The META loss was −10.62% against an 8% stop. No rule change fixes this — it's a property of markets. Any strategy that holds single equities through news events will face this. The experiment added a "consider trimming at RS session 1 negative" rule as a mitigation, but the core risk remains: market-sell stops don't protect against gap opens.

### Finding 3: The Strategy's Best Signal Was RS Momentum Decay
The behavioral flag system — tracking 3-session declining RS_spread — was the most predictive forward indicator in the dataset. META, MSFT, NVDA, XLE, AMZN were all flagged by RS_MOMENTUM_DECAY before their exits triggered. This is where the alpha actually lives in this strategy: the warning is early enough to act before the hard rule forces a sell.

### Finding 4: Cash Drag Beats Alpha Generation in Bull Markets
The individual position selections were reasonable (GOOGL +7%, AAPL +7%, QQQ +5% unrealized at halt). The problem is that 40–56% of the portfolio was not in those positions. A simple strategy of staying fully invested in QQQ alone would have beaten this result.

For an LLM agent, "decide to deploy cash" is harder than "execute an exit rule" — exits are reactive, deploys are proactive and require conviction. The agent lacked a mechanism to force itself to deploy when signals were marginal but regime was bullish.

### Finding 5: Cross-Session Memory Is Genuinely a Problem
Each routine started cold. The AMZN trim contradiction (pre-market said hold at RS > −1%, but execution trimmed at RS = −0.05% based on weekly-review carry-forward) shows how cross-session state management fails. The agent wrote the correct intent in the weekly review on Friday, but by Monday's pre-market it had "forgotten" and needed to re-derive it.

The `last-session.md` handoff file helped, but wasn't always read or reconciled carefully. This is a fundamental limitation of stateless LLM sessions.

### Finding 6: Infrastructure Reliability Is Load-Bearing
The Alpaca fractional stop order bug meant that all 6 positions had zero automatic downside protection for most of the experiment. If a routine had missed, positions could have fallen 15%+ with no stop. The experiment got lucky — the manual checks caught everything. But this is the kind of operational risk that silently accumulates in AI trading systems.

### Finding 7: The LLM Is a Good Analyst, A Mediocre Trader
The weekly reviews and pre-market analyses are genuinely good writing. The signal table, contradiction tracking, carry-forward flags — these are well-structured. But "good analysis" doesn't translate to "good P&L" when the underlying edge is thin and cash drag dominates.

---

## 7. Quantitative Summary

| Stat | Value |
|------|-------|
| Total experiment days | 12 of planned 20 |
| Total trades | 27 |
| Winning closed positions | 0 (XLE −3%, MSFT −4.9%, NVDA −4.3%, META −10.6%) |
| Open positions in profit at halt | 3/5 (AAPL, GOOGL, QQQ) |
| Largest single loss | META −10.62% (overnight gap) |
| Best unrealized position | GOOGL +4.1% |
| Peak equity | ~$10,067.97 (2026-05-06) |
| Lowest equity | ~$9,984.64 (pre-market 2026-05-12) |
| Average cash % held | ~42% |
| Stop order placement success rate | ~10% (only whole-share positions; all fractional failed) |
| Behavioral flag events | 18 (JSONL entries) |

---

## 8. Takeaways for Future LLM Trading Agent Designs

**1. Cash deployment is harder than stop execution.**
Build an explicit forcing function — if cash > X% in a bull regime and N signals are valid, the agent should be required to act, not just document why it isn't.

**2. Alpaca's fractional share support has critical gaps.**
GTC stop orders don't work for fractional positions. Test your full execution stack before relying on it for risk management. Use DAY orders for fractional stops, or round all positions to whole shares.

**3. Cross-session state management needs a dedicated mechanism.**
`last-session.md` + weekly rules is not enough. Important carry-forward actions (pending trims, staged sells) need to be in a structured state file the agent reads at the top of every routine and explicitly reconciles before forming intents.

**4. The 2-session RS exit confirmation is good but has overnight gap exposure.**
For higher-volatility positions, a session-1-RS-negative trim rule reduces tail risk during the confirmation window.

**5. The midsession routine is disproportionately valuable.**
The MSFT/NVDA catch on 4/30 and the XLE sell on 5/6 both came from midsession checks. If you're running scheduled routines, the 1:30 PM intraday check is worth more than its share of session count suggests.

**6. LLM rule-following is a feature, not a bug — but only if the rules are right.**
The agent followed every rule correctly. The underperformance came from the strategy design (cash conservatism in MIXED regime) and market structure (overnight gaps, early whipsaws). The LLM itself is not the bottleneck.

**7. RS Momentum Decay is the sharpest signal in this framework.**
Flag early (3-session declining RS), act on the first clear confirmation, and don't wait for the hard exit trigger. This was the most predictive pattern across all 12 days.

---

## 9. Conclusion

The experiment ran for 12 of 20 planned days. The portfolio was not in loss (+$30 absolute) but significantly underperformed its mandate — trailing SPY by 3.1 percentage points.

The strategy works mechanically. The agent followed rules without failure and self-reported contradictions accurately. The underperformance is structural: too much cash in a bull market, early whipsaws from positions that recovered, and one overnight gap that blew through the intended stop level.

The most important observation is behavioral: **an LLM is excellent at executing rules it has been given, and poor at exercising discretion when those rules produce suboptimal outcomes**. The agent knew, every session, that 42% cash in a bull market was costing return. It documented this correctly. It didn't fix it.

That is the real finding of this experiment.
