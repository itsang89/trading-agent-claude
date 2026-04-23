# Universe Proposal — Week 1

**Proposed by:** pre-market-research routine  
**Date:** 2026-04-23  
**Status:** Pending operator review and lock into `state/universe.json`

---

## Proposed Universe (12 tickers)

| Ticker | GICS Sector | Role | Market Cap |
|---|---|---|---|
| QQQ | ETF | Tech/growth beta proxy | N/A (ETF) |
| XLV | ETF | Healthcare defensive | N/A (ETF) |
| XLE | ETF | Energy/commodity exposure | N/A (ETF) |
| NVDA | Information Technology | Highest momentum potential | >$10B ✓ |
| MSFT | Information Technology | Quality + AI anchor | >$10B ✓ |
| AAPL | Information Technology | Large-cap stability | >$10B ✓ |
| GOOGL | Communication Services | AI/search exposure | >$10B ✓ |
| META | Communication Services | Ad revenue momentum | >$10B ✓ |
| LLY | Health Care | GLP-1 growth, low market correlation | >$10B ✓ |
| JPM | Financials | Rate-sensitive quality | >$10B ✓ |
| BRK.B | Financials | Defensive quality | >$10B ✓ |
| AMZN | Consumer Discretionary | Cloud + e-commerce | >$10B ✓ |

---

## Validation Checklist

- Ticker count: 12 ✓ (within 10–15)
- GICS sectors: 6 ✓ (≥3 required) — IT, Communication Services, Health Care, Financials, Consumer Discretionary, ETF
- ETFs: 3 ✓ (≥2 required) — QQQ, XLV, XLE
- Market cap >$10B: ✓ all qualify
- US-listed only: ✓
- No leveraged/inverse ETFs: ✓
- No options, crypto, OTC: ✓
- SPY excluded from position universe: ✓ (SPY is RS benchmark only)

---

## Sector Concentration Check (equal-weight estimate)

| Sector | Tickers | Weight at 5% each |
|---|---|---|
| Information Technology | NVDA, MSFT, AAPL | ~15% |
| Communication Services | GOOGL, META | ~10% |
| Health Care | LLY + XLV | ~10% |
| Financials | JPM, BRK.B | ~10% |
| Consumer Discretionary | AMZN | ~5% |
| ETF (multi-sector) | QQQ, XLE | ~10% |

No single GICS sector exceeds 40% at maximum position sizes. ✓

---

## Rationale

- **QQQ** replaces SPY as the Week-1 position (SPY cannot beat itself as benchmark).
- **XLV/XLE** provide defensive and commodity diversification against tech concentration.
- **NVDA/MSFT/AAPL** are the highest-quality, highest-liquidity IT names for momentum strategy.
- **GOOGL/META** capture AI/ad revenue theme without overlapping too heavily with QQQ.
- **LLY** is uncorrelated to market beta, offers growth + defensive blend.
- **JPM/BRK.B** give rate-sensitive and value exposure for portfolio balance.
- **AMZN** captures cloud growth narrative alongside e-commerce optionality.

---

## Operator Action Required

1. Review this proposal.
2. If approved, update `state/universe.json`:
   - Set `"status": "LOCKED"`, `"locked": true`, `"locked_at": "<date>"`
   - Replace tickers array with approved list
   - Update sector_map with full GICS mappings
3. Update experiment-config.json `current_week` to 2 when Week 2 begins.
4. Full-universe trading begins Week 2 after lock confirmation.
