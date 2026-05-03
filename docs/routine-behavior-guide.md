# Routine Behavior Guide (summary)

Full step-by-step instructions live in `prompts/<routine>.md`. This file is a high-level summary only.

### pre-market-research
1. Check market status — exit if closed.
2. Read last 3 journal entries (any type).
3. Call `get_account`, `get_positions`, `get_spy_benchmark`, `get_bars` for held tickers + universe.
4. Check every position for stop-loss (current_price < avg_entry * 0.92). Queue sells.
5. Form intents for the day (tickers to buy/sell, sizing rationale).
6. Write journal entry: `journal/YYYY-MM-DD-pre-market.md`
7. Week 1 first run only: write `universe-proposal.md`.

### market-open-execution
1. Check market status — exit if closed.
2. Read today's pre-market journal.
3. Call `get_account`, `get_positions`.
4. Execute stop-loss sells first (use `place_order`).
5. Execute buy/sell intents from pre-market. Size per conviction tier in `state/strategy.md`. Document rationale for any position ≥10%.
6. Write journal: `journal/YYYY-MM-DD-execution.md` — list orders placed, rejections, sizing rationale.

### mid-session-check
1. Check market status — exit if closed (this routine requires an open market for intraday sells).
2. Read today's pre-market and execution journals.
3. Call `get_account`, `get_positions`. Check trailing stop and regular stop for every position.
4. Run `get_bars` for each held ticker. Compute Trend and RS_spread.
5. Execute intraday soft exits: Trend BEARISH → market-sell immediately; RS < -1% AND was also < -1% at execution → market-sell immediately.
6. Write brief journal: `journal/YYYY-MM-DD-midsession.md`. Update last-session.md.

### end-of-day-review
1. Check market status — log if already closed, proceed anyway.
2. Call `get_account`, `get_positions`, `get_spy_benchmark`.
3. Compute day's P&L vs SPY.
4. Note any positions approaching stop-loss (loss >5%, not yet 8%).
5. Run signal check on all held positions (get_bars each ticker). Flag soft exits for next morning execution. Track RS_spread momentum decay (3-session declining trend).
6. Write journal: `journal/YYYY-MM-DD-eod.md` — numbers-forward, bullet points.

### weekly-review (Friday only, claude-opus-4-6)
1. Read all journal entries from the week.
2. Read `metrics/daily-metrics.csv` (last 5 rows).
3. Read `logs/behavioral-flags.jsonl` (last 20 entries).
4. Synthesize: what worked, what didn't, behavioral patterns observed.
5. Write journal: `journal/YYYY-MM-DD-weekly.md`.
