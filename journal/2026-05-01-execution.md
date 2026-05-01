# Execution — 2026-05-01 (Experiment Day 5)
**Routine:** market-open-execution
**Model:** opencode/hy3-preview-free (scheduled: claude-sonnet-4-6)
**Time (ET):** ~9:53 AM ET
**Week number:** 1

---
## Orders Placed
| Ticker | Side | Qty | Type | Order ID | Fill Estimate | Conviction | % of Equity |
|--------|------|-----|------|-----------|---------------|------------|-------------|
| LLY | buy | 0.51 | market | ba55d074-72fb-4cf8-a2e1-cdad4237c4c8 | ~$981.72 | Standard (RS +1.02%) | 4.99% |
| GOOGL | buy | 1.97 | market | 565f5f5c-a813-4be5-9e2e-3c894ae7befc | ~$366.98 avg | Very High (RS +12.16%) | 13.03% |

## Orders Rejected
None.

## Buy Intents Aborted
None. Both LLY and GOOGL current prices > pre-market SMA (signal re-validation passed).

## Stop-Loss Actions
None. All positions passed stop-loss and trailing stop checks:
- AAPL: current $283.90 > effective stop $247.31
- AMZN: current $267.04 > effective stop $239.71
- GOOGL: current $382.02 > effective stop $346.49 (trailing active, high_close $384.99)
- LLY: current $979.26 > effective stop $903.18 (new position)
- QQQ: current $672.89 > effective stop $608.87
- XLE: current $59.25 > effective stop $54.26

## Winner Trims
None. No position >25% of equity (GOOGL highest at 13.03%).

## Sizing Rationale (positions ≥10%)
- **GOOGL (13.03%)**: Very High conviction. RS_spread +12.16% (highest in universe), 10d_ROC +14.57%, volume_ratio 2.35 elevated. Price up >10% from entry, trailing stop active. Adding toward 13-20% tier ceiling per strategy.md. Rationale: strongest signal in universe, multi-day RS leadership.

## Portfolio After Execution
- Equity: $10,000.07
- Cash: $6,867.39 (68.7%)
- Positions: 6 (AAPL 5.28%, AMZN 7.77%, GOOGL 13.03%, LLY 4.99%, QQQ 5.05%, XLE 7.70%)
- IT sector concentration: AAPL only (~5.28%), well under 40% cap

## Errors / Flags
None. All tools completed successfully.
