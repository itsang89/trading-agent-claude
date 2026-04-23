# Trading Strategy Design
**Date:** 2026-04-23
**Experiment window:** 2026-04-28 → 2026-05-22 (4 weeks, ~20 trading days)
**Mandate:** Beat SPY total return (long-only, no leverage, paper account)

---

## 1. Philosophy

The only way to beat SPY long-only is to hold things already outperforming SPY. We do not predict — we observe which tickers are outperforming and filter for uptrends, then rotate into them.

**The agent does NOT:**
- Predict macro moves or earnings
- Chase news
- Try to time the broad market
- Hold SPY itself as a position (holding the benchmark can't beat it)

Every decision traces to two mechanical signals computed at pre-market. This produces rich, auditable behavioral data while genuinely targeting the mandate.

---

## 2. Signal Framework

Computed at every pre-market session using `get_bars <TICKER> 20`.

### Signal 1 — Trend
```
20-day SMA = mean of last 20 closing prices
Trend = BULLISH  if current_price > 20-day SMA
        BEARISH  if current_price <= 20-day SMA
```

### Signal 2 — Relative Strength (RS)
```
10-day ROC      = (close_today - close_10d_ago) / close_10d_ago * 100
SPY_10d_ROC     = same calculation for SPY (always compute, even if SPY not held)
RS_spread       = ticker_10d_ROC - SPY_10d_ROC

RS = POSITIVE  if RS_spread > 0%
     NEUTRAL   if RS_spread in [-1%, 0%]
     NEGATIVE  if RS_spread < -1%
```

### Eligibility for new entry
Both must be true: **Trend = BULLISH** AND **RS = POSITIVE**

### Ranking
When multiple tickers are eligible, rank by RS_spread descending — highest relative outperformer first.

---

## 3. Entry Rules

All conditions must pass before placing a buy:

| Condition | Requirement |
|---|---|
| Universe | Ticker in state/universe.json |
| Trend | Price > 20-day SMA |
| Relative Strength | RS_spread > 0% |
| Portfolio size | Fewer than 5 open positions |
| Cash after trade | ≥ 25% of equity (above the 20% hard floor) |

---

## 4. Exit Rules

Three triggers in priority order:

| Trigger | Type | Action |
|---|---|---|
| Loss ≥ 8% from avg_entry | Hard stop | Market-sell immediately, same session |
| Price drops below 20-day SMA | Soft exit | Flag in EOD journal, sell at next execution open |
| RS_spread < −1% for 2 consecutive sessions | Soft exit | Flag in EOD journal, sell at next execution open |

Soft exits prevent panic-selling on a single bad close while getting out before the 8% hard stop triggers.

---

## 5. Sizing Rules

| Condition | Size | Notes |
|---|---|---|
| Default new position | 5% of equity | Always the starting point |
| High conviction | 7% of equity | RS_spread > 3% AND ticker up >1% on the day — must document in journal |
| Maximum | 10% of equity | Hard limit enforced by validator |
| Adding to winner | Up to 7% total | Only if current position <7% AND both signals still positive |
| Target concurrent positions | 4–6 | Preserves ~25–30% cash above the 20% hard floor |

**Rule:** Any position sized ≥7% of equity requires explicit written rationale in the journal entry. Anything at 10% requires the highest conviction and full documentation.

---

## 6. Recommended Universe (Weeks 2–4)

12 tickers across 6 GICS sectors plus 3 ETFs.

| Ticker | Type | GICS Sector | Rationale |
|---|---|---|---|
| QQQ | ETF | ETF | Tech/growth beta — beats SPY in risk-on environments |
| XLV | ETF | ETF | Healthcare defensive — low correlation to broad market |
| XLE | ETF | ETF | Energy/commodity macro exposure |
| NVDA | Stock | Information Technology | Highest momentum potential in universe |
| MSFT | Stock | Information Technology | Quality + AI growth anchor |
| AAPL | Stock | Information Technology | Large cap stability with upside |
| GOOGL | Stock | Communication Services | AI/search, independent revenue stream |
| META | Stock | Communication Services | Ad revenue momentum |
| LLY | Stock | Health Care | GLP-1 growth, independent of market cycle |
| JPM | Stock | Financials | Rate-sensitive, quality proxy |
| BRK.B | Stock | Financials | Defensive quality |
| AMZN | Stock | Consumer Discretionary | Cloud + e-commerce |

**Universe validation:**
- ✅ 12 tickers (10–15 range)
- ✅ 6 GICS sectors: Information Technology, Communication Services, Health Care, Financials, Consumer Discretionary, Energy (via XLE)
- ✅ 3 ETFs (minimum 2)
- ✅ All market cap >$10B
- ✅ No leveraged or inverse ETFs
- ✅ All US-listed

**Sector concentration check:** 3 IT stocks × max 10% each = 30% of equity — stays under the 40% hard cap even at maximum sizing.

---

## 7. Week 1 Specific Behavior

Universe is SPY and QQQ only. Strategy applies identically:

- Compute Trend and RS_spread for both SPY and QQQ each pre-market
- **QQQ is the only valid holding** — holding SPY (the benchmark) cannot beat it
- If QQQ: Trend = BULLISH AND RS = POSITIVE → buy/hold QQQ at 5–7%, rest in cash
- If QQQ fails either signal → hold 100% cash, document reasoning in journal
- SPY bars are always fetched as the RS benchmark denominator, never as a position target
- Use week 1 to write `universe-proposal.md` using the recommended 12-ticker universe above

---

## 8. Files to Create or Modify

Three changes required to encode this strategy:

### 8a. New file: `state/strategy.md`
Full signal arithmetic, entry/exit rules, sizing table, and universe recommendation. Read by the agent once per pre-market session, immediately after CLAUDE.md.

### 8b. Modify: `CLAUDE.md`
Add a "Strategy Framework" section (concise) that:
- Names the two signals (Trend, Relative Strength)
- States the entry criterion (both signals must agree)
- States the three exit triggers
- Points to `state/strategy.md` for arithmetic detail

### 8c. Modify: `prompts/pre-market-research.md`
- Add a read instruction for `state/strategy.md` in the bootstrap sequence
- Expand Step 7 (Fetch market data) to include explicit signal computation:
  - Compute 20-day SMA for each held ticker and universe ticker
  - Compute 10-day ROC for each ticker and for SPY
  - Compute RS_spread for each ticker
  - Rank eligible tickers by RS_spread descending

No new tools required — all signals compute from `get_bars` output already available.

---

## 9. Signal Computation Reference

The agent performs this arithmetic at pre-market from `get_bars <TICKER> 20` output:

```
bars = get_bars output (list of OHLCV, sorted oldest → newest)
close_today   = bars[-1].close
close_10d_ago = bars[-11].close   # 10 trading days back
sma_20        = mean(bars[-20:].close)

ticker_10d_ROC = (close_today - close_10d_ago) / close_10d_ago * 100
spy_10d_ROC    = same for SPY (always computed)
RS_spread      = ticker_10d_ROC - spy_10d_ROC

Trend = BULLISH if close_today > sma_20
RS    = POSITIVE if RS_spread > 0
```

---

## 10. What Success Looks Like

- Agent holds 3–5 positions at a time, each with documented RS and trend rationale
- Journal entries show signal values (SMA, ROC, RS_spread) for held and candidate tickers
- Exits are soft before they become hard stops
- Universe proposal in week 1 matches the 12-ticker recommendation above
- By week 4: behavioral log shows consistent signal-based decisions, not ad hoc choices
