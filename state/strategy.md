# Strategy Reference — Relative Strength + Trend Filter

**Read-only during routines. Operator edits only.**
Last updated: 2026-04-28 (operator-authorized revision)

---

## Core Premise

Beat SPY by concentrating in the universe assets that are already outperforming SPY in an uptrend.
Do NOT hold SPY itself — it cannot beat itself.
Cash is a residual, not a target. Every idle dollar costs return when the market is trending up.

---

## Signal Computation

Run after `get_bars <TICKER> 20` for each ticker (held + universe). Always run for SPY.

```
bars          = get_bars output, sorted oldest → newest
close_today   = bars[-1]["close"]
close_10d_ago = bars[-11]["close"]   # 10 trading days back
sma_20        = mean of bars[-20]["close"] through bars[-1]["close"]
close_yesterday = bars[-2]["close"]

ticker_10d_ROC = (close_today - close_10d_ago) / close_10d_ago * 100
spy_10d_ROC    = same calculation for SPY
RS_spread      = ticker_10d_ROC - spy_10d_ROC
```

**Signal 1 — Trend:**
```
BULLISH if close_today > sma_20
BEARISH if close_today <= sma_20
```

**Signal 2 — Relative Strength (RS):**
```
POSITIVE if RS_spread > 0%
NEUTRAL  if RS_spread in [-1%, 0%]
NEGATIVE if RS_spread < -1%
```

---

## Entry Rules

All three conditions must be true to open a new position:

1. Ticker is in `state/universe.json`
2. Trend = BULLISH (close_today > sma_20)
3. RS = POSITIVE (RS_spread > 0%)

**Ranking:** When multiple tickers qualify, rank by RS_spread descending. Buy highest conviction first.
**Selectivity:** RS_spread 0–1% is borderline — only enter if the portfolio is lightly invested and no better signal exists. Prefer to skip borderline entries.

---

## Exit Rules (priority order)

| Priority | Trigger | Action |
|---|---|---|
| 1 | Loss ≥ 8% from avg_entry | Hard stop — market-sell immediately this session |
| 2 | Trend breaks: close_today drops below sma_20 | Flag at EOD — sell at next morning execution |
| 3 | RS_spread < −1% for 2 consecutive sessions | Flag at EOD — sell at next morning execution |

**RS Counter Reset Rule:** The 2-session RS exit counter resets ONLY when RS_spread > 0%. A bounce to −0.8% does NOT reset the counter. A ticker must show genuine relative strength (positive spread) to clear the warning.

**Trailing stop:** Tracked in `state/position-highs.json`. Logic:
```
hard_stop_price     = avg_entry * 0.92                        # always active
trailing_active     = high_close > avg_entry * 1.10           # activates once up >10%
trailing_stop_price = high_close * 0.90 if trailing_active    # 10% below peak
effective_stop      = max(hard_stop_price, trailing_stop_price)

if current_price < effective_stop:
    → market-sell immediately
    → log TRAILING_STOP_TRIGGERED if trailing_stop_price > hard_stop_price, else STOP_LOSS_TRIGGERED
```
Check effective_stop in every routine's stop-loss audit step.

**Winner trimming:** If a position grows beyond 25% of portfolio equity via appreciation (not a new purchase), trim back to ~20%. Prevents one winner from creating unmanageable single-stock risk.

---

## Sizing — Conviction Tiers

No fixed default or maximum. Size reflects signal strength and regime context.

| Tier | RS_spread | Additional condition | Target size | Notes |
|---|---|---|---|---|
| Borderline | 0–1% | — | 3–5% | Enter only if portfolio lightly invested; prefer to skip |
| Standard | 1–3% | — | 5–8% | Normal entry range |
| High conviction | 3–5% | — | 8–13% | Must document rationale in journal |
| Very high conviction | >5% | price up >1% today | 13–20% | Must document thoroughly; note regime |

**Adding to a winner:** If a held position is below its conviction-tier target AND both signals are still positive, scale up toward the tier ceiling. Recalculate avg_entry and stop-loss trigger after adding. After adding shares, update `state/position-highs.json` entry_price to the new avg_entry (keep high_close unchanged if it's higher).

**Trailing stop preservation on adds:** Before adding to a position with an ACTIVE trailing stop, compute `preserved_floor = max(hard_stop_price, current_trailing_stop_price)`. After the add raises avg_entry and deactivates the trailing stop, record `preserved_floor` as a `stop_floor` field in `state/position-highs.json` for that ticker. Treat `stop_floor` as the minimum effective stop until the trailing stop reactivates (high_close exceeds new threshold). Log explicitly in the sizing rationale that the trailing stop was deactivated and what the preserved floor is.

**Sizing down:** If a held position's RS_spread falls into a lower tier, consider trimming to the new tier ceiling rather than waiting for a full exit signal.

**Always document:** Any position sized ≥10% requires explicit written rationale in the journal.

---

## Portfolio Shape and Cash

**Position count:** No hard minimum or maximum. Use as many positions as signal quality and conviction allow. Natural range given 12-ticker universe: 3–7 positions. Prefer fewer high-conviction positions over many borderline ones.

**Cash:** Residual after positions. Self-imposed soft minimum ~10% for redeployment flexibility. Cash level should reflect regime:

| Regime | Universe above SMA_20 | Target cash |
|---|---|---|
| Bull | ≥8 of 12 tickers | 10–25% — be aggressive |
| Mixed | 5–7 of 12 tickers | 25–40% — be selective |
| Bear | <5 of 12 tickers | 50%+ — mostly cash, only highest RS names |

**Sector concentration:** Hard code limit — ≤40% of equity in one GICS sector. Note: NVDA + MSFT + AAPL are all Information Technology; combined they cannot exceed 40%.

---

## position-highs.json Maintenance

This file is the source of truth for trailing stop calculations. Every routine must keep it current.

**Schema:**
```json
{
  "NVDA": {"high_close": 215.50, "entry_price": 209.45, "last_updated": "2026-04-28"}
}
```

**Rules:**
- **On new position open (execution routine):** Add entry with `high_close = fill_price`, `entry_price = fill_price`.
- **On adding shares (execution):** Update `entry_price` to new avg_entry from get_positions. Keep `high_close` unchanged if it's already higher than the new avg_entry.
- **On price update (pre-market, mid-session, EOD):** After running get_bars, if `bars[-1]["close"] > high_close`, update `high_close` and `last_updated`.
- **On position close (any routine):** Remove the ticker's entry from the file.
- **If ticker missing from file but in positions:** Re-initialize using avg_entry_price from positions.json as both `high_close` and `entry_price`.

---

## Risk Management

- If 3+ positions hit stop-loss in the same calendar week: pause all new entries; write regime assessment in that day's journal before any buys resume.
- If portfolio is down >10% from experiment start ($10,000 notional): defensive posture — max 2–3 small positions, mostly cash, until signals recover.
- If bear regime is confirmed (< 5/12 universe above SMA_20): hold only positions with RS_spread > 3% and strong trend; exit anything below conviction threshold.

---

## Regime Assessment (write this every pre-market)

Count universe tickers with Trend = BULLISH. Classify regime. Use regime to calibrate aggression.

---

## Journal Signal Table (write this every pre-market)

| Ticker | SMA_N | Close | Trend | 10d_ROC | RS_spread | Conviction Tier | Action |
|---|---|---|---|---|---|---|---|
| QQQ | $X | $X | BULLISH | +2.1% | +1.4% | Standard | HOLD |
| NVDA | $X | $X | BEARISH | -0.5% | -1.2% | — | WATCH |

Always include this table. Note the SMA period used (SMA_20 if ≥20 bars available; otherwise SMA_N with actual N).

---

## News Tools

- **Until 2026-05-04:** Price and technical data only. No news.
- **From 2026-05-05:** News tools permitted for timing decisions (macro calendar, earnings dates, Fed events). Technical signals remain primary. Use news to avoid holding through known binary events without a view; do not use it to override signal exits.

---

## Week 1 Special Rules (historical — kept for reference)

- Universe was {SPY, QQQ} only until operator locked on 2026-04-26.
- QQQ was the ONLY valid position.
- SMA_20 proxy (SMA_14) was used due to insufficient bar history — see Learned Behaviors.
