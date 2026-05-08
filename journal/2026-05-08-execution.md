# Execution Journal — 2026-05-08 (Experiment Day 10 — Friday)
**Routine:** market-open-execution
**Model:** claude-sonnet-4-6
**Time (ET):** 9:45 AM ET
**Week number:** 2

---

## Market Status
- Open: YES | Hours: 9:30–16:00 ET | No early close

## Portfolio Before Execution
- Equity: $10,059.87 | Cash: $3,906.83 (38.83%) | Positions: 5

---

## Step 6 — Stop-Loss & Trailing Stop Check

| Ticker | Avg Entry | Hard Stop | High Close | Trailing Active | Eff. Stop | Current | Status |
|--------|-----------|-----------|------------|-----------------|-----------|---------|--------|
| AAPL | $273.908 | $252.20 | $288.79 | No (thr $301.30) | $252.20 | $293.71 | PASS |
| AMZN | $266.733 | $245.39 | $276.36 | No (thr $293.41) | $245.39 | $271.87 | PASS |
| GOOGL | $373.299 | $343.44 | $397.89 | No (thr $410.63) | $343.44 | $399.62 | PASS |
| LLY | $987.435 | $908.44 | $991.945 | No (thr $1,086.18) | $908.44 | $963.92 | PASS |
| QQQ | $678.381 | $624.11 | $695.62 | No (thr $746.22) | $624.11 | $703.78 | PASS |

No stops triggered.

## Step 6b — Winner Trim Check
- All positions < 25% of equity. No trims needed.
  - GOOGL highest at 17.17% ($1,726/equity). Well below 25% threshold.

---

## Step 7 — Signal Re-Validation

| Ticker | Intent | SMA_14 / Gate | Ask at 9:45 | Decision |
|--------|--------|---------------|-------------|----------|
| NVDA | BUY new | SMA_14 $204.53 | $216.75 ≥ SMA ✓ | PROCEED |
| GOOGL | ADD conditional | Gate $401.87 | $399.64 < gate ✗ | ABORT |

**BUY ABORTED — GOOGL**: Conditional gate not met. Ask $399.64 < $401.87. Order not placed.

---

## Orders Placed

| Ticker | Side | Qty | Type | Order ID | Fill Price | Conviction | % Equity |
|--------|------|-----|------|----------|------------|------------|----------|
| NVDA | BUY | 2 | market | 889812df-47e4-437b-8963-aecf18701451 | $216.63 | Standard | 4.31% |

- NVDA fill confirmed by positions API: avg_entry $216.63, market value $433.74.
- Hard stop: $199.30 (× 0.92). Trailing threshold: $238.29 (× 1.10).
- **Stop order WARNING**: `stop_order_warning` returned — "potential wash trade detected. use complex orders." Stop NOT placed. Manual enforcement required. Logged to notes-for-operator.md.
- position-highs.json updated: `{"high_close": 216.63, "entry_price": 216.63, "last_updated": "2026-05-08"}` (no stop fields).

## Orders Rejected
None.

## Buy Intents Aborted
- **GOOGL ADD ~0.71 shares**: Conditional gate $401.87 not met. Ask at 9:45 = $399.64. Intent remains valid — re-check at mid-session (1:30 PM) or EOD if price recovers.

## Stop-Loss Actions
None.

## Winner Trims
None.

---

## Sizing Rationale
- **NVDA 4.31% of equity**: Standard tier (RS +2.686%, range 3–8%). Sized at lower end (~5% target → 4.31% actual fill) due to: (a) earnings 5/20 (12 days out, outside 7-day flag but proximate); (b) Friday entry with no weekend monitoring; (c) vol_ratio neutral (0.988). No position ≥10% — no detailed rationale required by policy.

---

## Portfolio After Execution
- Equity: $10,064.41 | Cash: $3,473.57 (34.51%) | Positions: 6

| Ticker | Qty | Avg Entry | Current | Market Value | % Equity | Hard Stop | Trailing Thr |
|--------|-----|-----------|---------|--------------|----------|-----------|--------------|
| AAPL | 2.86 | $273.908 | $294.275 | $841.63 | 8.36% | $252.20 | $301.30 |
| AMZN | 4.76 | $266.733 | $271.99 | $1,294.67 | 12.87% | $245.39 | $293.41 |
| GOOGL | 4.32 | $373.299 | $399.842 | $1,727.32 | 17.16% | $343.44 | $410.63 |
| LLY | 1.32 | $987.435 | $964.25 | $1,272.81 | 12.65% | $908.44 | $1,086.18 |
| NVDA | 2.00 | $216.63 | $216.87 | $433.74 | 4.31% | $199.30 | $238.29 |
| QQQ | 1.45 | $678.381 | $704.15 | $1,021.02 | 10.14% | $624.11 | $746.22 |

Cash post-execution: 34.51% — above BULL regime target (10–25%). Constrained:
- GOOGL add not met (gate); AMZN decay flag; LLY at ceiling; AAPL at ceiling; NVDA just entered (no add).
- Remaining eligible deployment only via GOOGL (if gate met mid/EOD) or no new entries in BULL regime today.

## Sector Concentration
- IT: AAPL (8.36%) + NVDA (4.31%) = 12.67% ✓
- Consumer Disc: AMZN 12.87% ✓
- Comm Services: GOOGL 17.16% ✓
- Health Care: LLY 12.65% ✓
- ETF: QQQ 10.14% ✓
- No sector > 40% ✓

## RS Momentum Flags
- AMZN RS_MOMENTUM_DECAY: still active. No add.
- LLY Watch (2 consecutive declining EOD-to-EOD): monitor at mid/EOD.
- No new flags triggered at execution.

## Cumulative Performance
- Equity: $10,064.41 (+0.644% from $10,000 notional)
- SPY comparison: continued tracking required at EOD.

## Errors / Flags
- NVDA stop order placement failed: "potential wash trade detected" (stop_order_warning). Same class of error as prior fractional GTC failures. Logged to notes-for-operator.md. Manual enforcement every routine.
