# Strategy Reference — Relative Strength + Trend Filter

**Read-only during routines. Operator edits only.**
Last updated: 2026-04-23

---

## Core Premise

Beat SPY by holding only assets already outperforming SPY in an uptrend.
Do NOT hold SPY itself as a position — it cannot beat itself.

---

## Signal Computation

Run after `get_bars <TICKER> 20` for each ticker (held + universe). Also always run for SPY.

```
bars          = get_bars output, sorted oldest → newest
close_today   = bars[-1]["close"]
close_10d_ago = bars[-11]["close"]   # 10 trading days back (index -11 = 11th from end)
sma_20        = mean of bars[-20]["close"] through bars[-1]["close"]  # last 20 closes

ticker_10d_ROC = (close_today - close_10d_ago) / close_10d_ago * 100
spy_10d_ROC    = same calculation for SPY  ← always compute, even if SPY not held
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

All five conditions must be true to open a new position:

1. Ticker is in `state/universe.json`
2. Trend = BULLISH (close_today > sma_20)
3. RS = POSITIVE (RS_spread > 0%)
4. Current open positions < 5
5. Cash after trade ≥ 25% of equity

**Ranking:** When multiple tickers are eligible, rank by RS_spread descending. Buy highest first.

---

## Exit Rules (priority order)

| Priority | Trigger | Action |
|---|---|---|
| 1 | Loss ≥ 8% from avg_entry | Hard stop — market-sell immediately this session |
| 2 | Trend breaks: close_today drops below sma_20 | Soft exit — flag in EOD journal, sell at next execution open |
| 3 | RS_spread < −1% for 2 consecutive sessions | Soft exit — flag in EOD journal, sell at next execution open |

Soft exits exist to avoid panic-selling on a single bad close. If a soft exit is flagged at EOD, the execution routine sells at open the next day.

---

## Sizing Rules

| Condition | Size | Requirement |
|---|---|---|
| Default new position | 5% of equity | Always the starting point |
| High conviction | 7% of equity | RS_spread > 3% AND close_today > close_yesterday by >1% — must document in journal |
| Maximum | 10% of equity | Hard limit; validator will reject above this |
| Adding to winner | Up to 7% total | Only if current position < 7% AND both signals still positive |
| Target concurrent positions | 4–6 | Keeps ~25–30% cash above the 20% hard floor |

Any position sized ≥ 7% requires explicit written rationale in the journal entry.

---

## Recommended Universe (for week-1 universe proposal)

Propose these 12 tickers in `universe-proposal.md`:

| Ticker | GICS Sector | Role |
|---|---|---|
| QQQ | ETF | Tech/growth beta |
| XLV | ETF | Healthcare defensive |
| XLE | ETF | Energy/commodity exposure |
| NVDA | Information Technology | Highest momentum potential |
| MSFT | Information Technology | Quality + AI anchor |
| AAPL | Information Technology | Large-cap stability |
| GOOGL | Communication Services | AI/search |
| META | Communication Services | Ad revenue momentum |
| LLY | Health Care | GLP-1 growth, low market correlation |
| JPM | Financials | Rate-sensitive quality |
| BRK.B | Financials | Defensive quality |
| AMZN | Consumer Discretionary | Cloud + e-commerce |

Validation: 12 tickers ✓ · 6 GICS sectors ✓ · 3 ETFs ✓ · all market cap >$10B ✓ · no leveraged ETFs ✓

---

## Week 1 Special Rules

- Universe = {SPY, QQQ} only until operator locks
- QQQ is the ONLY valid position (holding SPY cannot beat SPY)
- Compute Trend and RS_spread for QQQ vs SPY each session
- If QQQ: Trend = BULLISH AND RS = POSITIVE → hold at 5–7%, rest cash
- If QQQ fails either signal → 100% cash, document in journal
- SPY is always the RS denominator, never a position

---

## Journal Signal Table (write this every pre-market)

| Ticker | SMA_20 | Close | Trend | 10d_ROC | RS_spread | Action |
|---|---|---|---|---|---|---|
| QQQ | $X | $X | BULLISH | +2.1% | +1.4% | HOLD |
| NVDA | $X | $X | BEARISH | -0.5% | -1.2% | WATCH |

Always include this table in the pre-market journal entry.
