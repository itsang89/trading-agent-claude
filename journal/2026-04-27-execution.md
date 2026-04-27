# Execution — 2026-04-27 (Experiment Day 1)

**Routine:** market-open-execution
**Model:** claude-sonnet-4-6
**Time (ET):** ~9:47 AM ET
**Market status:** OPEN (normal session, close 16:00 ET)

---

## Stop-Loss Actions

- No positions held at routine start. No stop-loss checks required.

---

## Orders Placed

| # | Ticker | Side | Qty | Type | Order ID | Fill est. |
|---|--------|------|-----|------|----------|-----------|
| 1 | MSFT | buy | 1.18 | market | 2b620530-e485-4f7d-921c-21ba99bd5042 | ~$422.00 = ~$498 |
| 2 | AMZN | buy | 1.91 | market | f605e2ef-8b19-4314-a693-36f43017e14d | ~$261.00 = ~$499 |
| 3 | NVDA | buy | 2.38 | market | bae2f510-0e5c-42df-b028-f843af72ce6f | ~$209.59 = ~$499 |
| 4 | QQQ | buy | 0.75 | market | b9e2029b-ca75-4f89-89c7-e6cd15c695a0 | ~$661.99 = ~$496 |
| 5 | GOOGL | buy | 1.44 | market | 3c3f5d2d-8a34-426e-9ba7-e05b6c67f374 | ~$346.10 = ~$498 |
| 6 | META | buy | 0.73 | market | 517a64e6-8e97-4476-95d7-fba52dd510c9 | ~$676.20 = ~$494 |

All 6 orders: `passed: true`, status `PENDING_NEW` at submission.

---

## Orders Rejected

None.

---

## Intents Not Executed

None. All 6 pre-market intents executed.

---

## Sizing Rationale

- All positions at **5% default** (~$500 each).
- High-conviction upsize (7%) was NOT applied — revalidated at 9:45 AM:
  - MSFT: −0.81% vs Friday close (required > +1%) ✗
  - AMZN: −0.88% vs Friday close ✗
  - NVDA: +0.59% vs Friday close (below +1% threshold) ✗
  - QQQ: −0.29% vs Friday close ✗
  - GOOGL: +0.65% vs Friday close ✗
  - Criteria not met → default 5% applied to all.
- META included as 6th position (optional from pre-market). RS_spread +2.06% (standard, not high-conviction). Deployed at 5% standard.

---

## Signal Reconfirmation at 9:45 AM

Trend signal: All 6 tickers confirmed above SMA_13 at time of execution.
RS_spread: Pre-market spreads remain well above 0% entry threshold (minimum META +2.06%).
Signal drift from Friday close: All within normal intraday range, no threshold crossings.
→ All entry signals valid. Proceed as planned.

---

## Post-Execution State (estimated)

- **Total deployed:** ~$2,984 (~29.8%)
- **Cash remaining:** ~$7,016 (~70.2%) — above 25% floor ✓, above 20% hard floor ✓
- **Positions:** 6 (within 4–8 range ✓)
- **Max single position:** ~5% (below 10% limit ✓)

Sector concentration:
- IT (MSFT + NVDA): ~10% ✓
- Communication Services (GOOGL + META): ~10% ✓
- Consumer Discretionary (AMZN): ~5% ✓
- ETF (QQQ): ~5% ✓
- All sectors under 40% limit ✓

---

## Errors / Flags

- None. All tools returned clean output.
- 0 stop-loss triggers, 0 guardrail rejections, 0 tool errors.
