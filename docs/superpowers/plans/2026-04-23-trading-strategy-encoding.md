# Trading Strategy Encoding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode the Relative Strength + Trend Filter strategy into the agent's operational files so every routine session has explicit signal criteria, entry/exit rules, and a recommended universe.

**Architecture:** Three file changes — create `state/strategy.md` as the authoritative signal reference, add a concise Strategy Framework section to `CLAUDE.md` (read every session), and expand `prompts/pre-market-research.md` to compute signals from bar data. No new tools required — all signals derive from existing `get_bars` output.

**Tech Stack:** Markdown only. No code changes. Verified with grep/cat.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `state/strategy.md` | Full signal arithmetic, entry/exit rules, sizing table, universe |
| Modify | `CLAUDE.md` | Add Strategy Framework section after Mandate (6–8 lines) |
| Modify | `prompts/pre-market-research.md` | Add strategy.md read step; expand Step 7 with signal computation |

---

## Task 1: Create `state/strategy.md`

**Files:**
- Create: `state/strategy.md`

- [ ] **Step 1: Write `state/strategy.md`**

Create the file with this exact content:

```markdown
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
```

- [ ] **Step 2: Verify file was created**

```bash
ls -la state/strategy.md && echo "EXISTS"
```
Expected: file listed, `EXISTS` printed.

- [ ] **Step 3: Verify key sections exist**

```bash
grep -c "Signal Computation\|Entry Rules\|Exit Rules\|Sizing Rules\|Recommended Universe" state/strategy.md
```
Expected: `5`

- [ ] **Step 4: Commit**

```bash
git add state/strategy.md
git commit -m "feat: add strategy reference file (RS + trend filter)"
```

---

## Task 2: Add Strategy Framework section to `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md` (insert after the `## Mandate` section, before `## Universe`)

- [ ] **Step 1: Verify the insertion point exists**

```bash
grep -n "## Universe" CLAUDE.md
```
Expected: line number printed (e.g., `15:## Universe`).

- [ ] **Step 2: Insert the Strategy Framework section**

Open `CLAUDE.md`. Find the `---` separator line between `## Mandate` and `## Universe`. Insert the following block immediately before `## Universe`:

```markdown
## Strategy Framework

**Entry:** Buy when BOTH signals agree: (1) price > 20-day SMA (uptrend) AND (2) ticker's 10-day return > SPY's 10-day return (outperforming benchmark).
**Exit:** Three triggers in priority order: (1) loss ≥ 8% from avg_entry — market-sell immediately; (2) price drops below 20-day SMA — soft exit, sell next execution; (3) RS_spread < −1% for 2 consecutive sessions — soft exit, sell next execution.
**Sizing:** 5% default · 7% high conviction (RS_spread > 3% AND up >1% on day, must document) · 10% maximum.
**Portfolio shape:** 4–6 concurrent positions · ≥25% cash at all times (above the 20% hard floor).
**Never hold SPY as a position.** SPY is only the RS benchmark denominator.
**Full signal arithmetic:** `state/strategy.md` — read this every pre-market session.

---
```

- [ ] **Step 3: Verify the section was inserted**

```bash
grep -n "Strategy Framework\|Never hold SPY\|state/strategy.md" CLAUDE.md
```
Expected: three matching lines with line numbers.

- [ ] **Step 4: Verify CLAUDE.md still has all original sections**

```bash
grep -c "## Mandate\|## Universe\|## Hard Limits\|## Routines\|## Tools\|## Memory Layout\|## Behavioral Rules\|## Learned Behaviors" CLAUDE.md
```
Expected: `8`

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add strategy framework section to CLAUDE.md"
```

---

## Task 3: Update `prompts/pre-market-research.md`

Two changes: (a) add `state/strategy.md` to the Step 1 read list, (b) insert a new Step 7b for signal computation.

**Files:**
- Modify: `prompts/pre-market-research.md`

- [ ] **Step 1: Verify current Step 1 content**

```bash
grep -n "Read your operational brief\|CLAUDE.md" prompts/pre-market-research.md
```
Expected: lines referencing Step 1 and CLAUDE.md.

- [ ] **Step 2: Add strategy.md to Step 1**

In `prompts/pre-market-research.md`, find the Step 1 block:

```
### Step 1 — Read your operational brief
Read CLAUDE.md fully. Pay special attention to the LEARNED BEHAVIORS section at the bottom — these are operator-endorsed rules from prior weeks that carry the same weight as hard limits.
```

Replace it with:

```
### Step 1 — Read your operational brief
Read CLAUDE.md fully. Pay special attention to the LEARNED BEHAVIORS section at the bottom — these are operator-endorsed rules from prior weeks that carry the same weight as hard limits.
Then read `state/strategy.md` — this contains the signal arithmetic, entry/exit rules, sizing table, and recommended universe. You will apply these rules in Step 7b below.
```

- [ ] **Step 3: Verify Step 1 now references strategy.md**

```bash
grep -n "state/strategy.md" prompts/pre-market-research.md
```
Expected: at least one matching line.

- [ ] **Step 4: Insert Step 7b for signal computation**

Find the Step 7 block in `prompts/pre-market-research.md`:

```
### Step 7 — Fetch market data
Run for each held ticker (from positions.json): `python3 tools/get_bars.py <TICKER> 10`
Run for each universe ticker (from state/universe.json): `python3 tools/get_bars.py <TICKER> 5`
Run: `python3 tools/get_spy_benchmark.py`
```

Replace it with:

```
### Step 7 — Fetch market data
Run for SPY: `python3 tools/get_bars.py SPY 20`
Run for each held ticker (from positions.json): `python3 tools/get_bars.py <TICKER> 20`
Run for each universe ticker (from state/universe.json): `python3 tools/get_bars.py <TICKER> 20`
Run: `python3 tools/get_spy_benchmark.py`

### Step 7b — Compute strategy signals
Using bars data from Step 7, compute for SPY first, then for each held and universe ticker:

```
bars          = get_bars output (oldest → newest)
close_today   = bars[-1].close
close_10d_ago = bars[-11].close
sma_20        = mean(bars[-20:].close)

10d_ROC  = (close_today - close_10d_ago) / close_10d_ago * 100
spy_ROC  = SPY's 10d_ROC  ← compute this first, reuse for all RS_spread calculations
RS_spread = ticker_10d_ROC - spy_ROC

Trend = BULLISH if close_today > sma_20, else BEARISH
RS    = POSITIVE if RS_spread > 0%, NEUTRAL if -1% to 0%, NEGATIVE if < -1%
```

**For held positions:** Flag any where Trend = BEARISH or RS = NEGATIVE as soft-exit candidates. Queue sell intents for execution routine if either condition holds.

**For universe tickers:** Tickers eligible for new entry = Trend BULLISH AND RS POSITIVE AND open positions < 5. Rank by RS_spread descending.

Write the signal table in your journal entry (see strategy.md for the table format).
```

- [ ] **Step 5: Verify Step 7b was inserted**

```bash
grep -n "Step 7b\|RS_spread\|spy_ROC\|signal table" prompts/pre-market-research.md
```
Expected: multiple matching lines.

- [ ] **Step 6: Update Step 9 to reference signal outputs**

Find the Step 9 block:

```
### Step 9 — Intent formation
Form your trading views for today. Requirements:
- If changing a prior stated position (from journals), explicitly write why.
- Default new position size: 5% of equity. Max 10%. Document reason for >5%.
- Week 1: Only SPY and QQQ are eligible (universe not yet locked).
- Do not form intents that contradict the LEARNED BEHAVIORS in CLAUDE.md without justifying the exception.
```

Replace it with:

```
### Step 9 — Intent formation
Form your trading views for today using the signal outputs from Step 7b. Requirements:
- **New buys:** Only from Step 7b's eligible list (Trend BULLISH + RS POSITIVE). If no tickers qualify, hold cash — do not force entries.
- **Soft exits:** Any held position flagged in Step 7b (Trend BEARISH or RS NEGATIVE) → add sell intent for execution routine.
- **Hard stops:** Any position with loss ≥ 8% → already queued from Step 6; confirm here.
- **Sizing:** Default 5% of equity. Up to 7% only if RS_spread > 3% AND ticker up >1% today — document the reason. Never exceed 10%.
- **Position count:** Do not add new positions if already at 5 or more open. Do not open new positions if cash would fall below 25%.
- If changing a prior stated position (from journals), explicitly write why.
- Do not form intents that contradict the LEARNED BEHAVIORS in CLAUDE.md without justifying the exception.
- Week 1: Only QQQ is eligible for new positions (holding SPY cannot beat SPY).
```

- [ ] **Step 7: Verify Step 9 was updated**

```bash
grep -n "eligible list\|soft exits\|RS_spread > 3\|25%" prompts/pre-market-research.md
```
Expected: multiple matching lines.

- [ ] **Step 8: Verify file still has all original steps**

```bash
grep -c "### Step" prompts/pre-market-research.md
```
Expected: `12` (original 11 steps + new Step 7b).

- [ ] **Step 9: Commit**

```bash
git add prompts/pre-market-research.md
git commit -m "feat: add signal computation and strategy-driven intent formation to pre-market prompt"
```

---

## Final Verification

- [ ] **Verify all three files are in order**

```bash
echo "=== state/strategy.md ===" && grep -c "##" state/strategy.md
echo "=== CLAUDE.md ===" && grep -n "Strategy Framework" CLAUDE.md
echo "=== pre-market-research.md ===" && grep -n "Step 7b\|state/strategy.md" prompts/pre-market-research.md
```

Expected:
```
=== state/strategy.md ===
8
=== CLAUDE.md ===
<line number>:## Strategy Framework
=== pre-market-research.md ===
<line>:### Step 7b — Compute strategy signals
<line>:Then read `state/strategy.md`
```

- [ ] **Final commit summary**

```bash
git log --oneline -5
```

Expected: three new commits visible — strategy.md, CLAUDE.md, pre-market-research.md.
