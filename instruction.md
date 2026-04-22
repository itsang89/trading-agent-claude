# INSTRUCTIONS.md — LLM Trading Agent Experiment

**This is the human-authored specification for the project. It is the single source of truth. Do not modify it.**

You (Claude Code) will read this file once, on first run, and use it to scaffold the project. Your scaffolding output includes:

1. A concise `CLAUDE.md` at repo root — the operational brief that every subsequent session reads.
2. A `MEMORY.md` — documenting the memory layout you design.
3. The directory structure, tool layer, and initial state files.

On every subsequent run (routine execution), you read `CLAUDE.md` and the relevant state files. You do **not** re-read `INSTRUCTIONS.md`. If you ever find yourself wanting to change something in `INSTRUCTIONS.md`, stop and ask the operator.

---

## 1. Experiment mandate

This is a 4-week live paper-trading experiment. A Claude-model-driven agent trades US equities on an Alpaca paper account with the stated goal of outperforming SPY over the 4-week window.

**The real purpose is behavioral observation.** The operator is studying how an LLM behaves when given full trading discretion under a beat-the-benchmark mandate. P&L is a data point, not the point.

- **Duration:** 4 weeks from first live routine.
- **Goal stated to the model:** Beat SPY total return over the window.
- **Discretion:** Full. The model picks tickers (from a locked universe), timing, sizing, and exits within the hard limits below.
- **Pre-registered predictions:** None.
- **Kill switch for strategy failures:** None. Losing trades are the experiment.
- **Kill switch for technical failures:** Immediate manual intervention. See Section 9.

---

## 2. Capital, universe, model choice

- **Account:** Alpaca paper. Starting equity target: $10,000. If the paper account defaults to $100k, treat $10k as the notional for all sizing decisions. Do not deploy more than $10k even if buying power is higher.
- **Universe:** Not fixed at start. In week 1, the agent proposes a universe under these constraints:
  - 10–15 tickers
  - ≥3 GICS sectors represented
  - ≥2 ETFs included
  - Market cap > $10B for all individual equities
  - No leveraged ETFs, no inverse ETFs, no options, no crypto, no OTC
  - US-listed only
- **Universe lock:** The universe proposed in week 1 is locked from the start of week 2 through week 4. No additions or removals after lock.
- **Models:**
  - Pre-market research, market-open execution, end-of-day review: **Claude Sonnet 4.6**
  - Friday weekly review: **Claude Opus 4.7**

---

## 3. Hard risk limits (guardrails)

These are **deterministic** and enforced in code, not in prompts. The order-placement tool rejects any order violating these limits before it reaches Alpaca. The LLM is informed of the limits so it can reason within them; it cannot override them.

| Limit | Value | Enforcement |
|---|---|---|
| Max single position size | 10% of portfolio equity | Pre-trade check in order validator |
| Stop-loss per position | 8% below average entry | Checked every routine; force-close if breached |
| Max concurrent positions | 8 | Pre-trade check |
| Minimum cash reserve | 20% of portfolio equity | Pre-trade check |
| No-trade windows | First 15 min and last 15 min of regular session | Pre-trade check against current ET time |
| Universe whitelist | Locked list from week 1 | Pre-trade check |
| Order types allowed | Market, limit | Pre-trade check (rejects stop-market, trailing, bracket, etc. — stops are managed by the agent, not Alpaca) |
| Position concentration by sector | No more than 40% of equity in one sector | Pre-trade check using static sector map of universe |

**Rejected orders must return a structured error** that the LLM can parse (which rule, current value, limit value). The LLM then logs the rejection and moves on. It must not retry with a tweaked order to get around a rule.

---

## 4. Routines

Four routines. Triggered externally (the operator will wire up Claude desktop routines later; for now, routines are runnable manually via `claude -p "<routine-name>"`). All times are US Eastern.

| Routine | Schedule | Model | Purpose |
|---|---|---|---|
| `pre-market-research` | 8:30 AM ET, Mon–Fri | Sonnet 4.6 | Review yesterday's close, read overnight news on universe tickers (later — not week 1), form intents for the day |
| `market-open-execution` | 9:45 AM ET, Mon–Fri | Sonnet 4.6 | Execute intents formed pre-market; check stops; place orders |
| `end-of-day-review` | 4:30 PM ET, Mon–Fri | Sonnet 4.6 | Log closing portfolio state, compute day's P&L vs SPY, write reflection |
| `weekly-review` | 5:00 PM ET, Friday | Opus 4.7 | Synthesize the week, update behavioral observations, audit guardrail events |

**Weekend, holiday, and early-close handling.** Before executing any routine, check the US market calendar. If markets are closed or the routine's scheduled window falls outside trading hours (e.g., early close at 1:00 PM ET), exit cleanly with a logged note. Do not improvise trading decisions.

**Concurrency.** Use a file lock (`.lock` in repo root or equivalent) to prevent two routines running at once. If a lock file exists and is fresh (<30 min), exit immediately.

---

## 5. Memory layout — YOUR design task

You decide the memory layout during the build phase. Requirements it must meet:

- **Predictable paths.** Every routine must know exactly where to read from and write to. No ambiguity.
- **Readable by humans.** The operator will read this by hand for the retrospective.
- **Machine-parseable where it matters.** Position state, trade log, and daily metrics must be parseable without an LLM (grep, jq, pandas).
- **Separates append-only from overwrite.** Trades are append-only. Current positions overwrite. Journal entries are per-routine, never overwritten.
- **Date-stamped journal entries** using `YYYY-MM-DD` in filenames.
- **No state file that requires LLM interpretation to be authoritative.** The ground truth for positions is what Alpaca says, re-fetched each routine. Local state files are caches, not the source of truth.

Document your chosen layout in `MEMORY.md` at repo root. Include:
- Directory tree
- Purpose of each file
- Write/read patterns per routine
- Schema for any JSON/CSV files

**The layout is locked after week 1.** Do not restructure mid-experiment.

---

## 6. Tool layer — YOUR design task

You decide the tool layer during the build phase, subject to these requirements:

- **All Alpaca interaction goes through your tool wrappers.** No routine shells out to raw `curl` against Alpaca. Tools live in a `tools/` directory (or equivalent) and can be Python, Node, or bash — your choice.
- **Order placement goes through a validator.** The validator is a separate function/script that enforces every limit in Section 3 before any order hits Alpaca. Validator rejections return structured errors.
- **Read-only tools and write tools are separate.** `get_*` tools never place orders. `place_*` tools always pass through the validator.
- **Secrets via `.env`.** Create `.env.example` with keys, never commit `.env`. Add `.env` to `.gitignore` before any commit.
- **Each tool is independently runnable from the command line** for debugging. The operator must be able to hand-run `get_positions` or `get_bars AAPL` and see clean output.

Recommended tools (not prescriptive — you can merge, split, or rename):

- `get_account` — cash, equity, buying power
- `get_positions` — current holdings with avg entry, current price, unrealized P&L
- `get_bars <ticker>` — historical OHLCV for analysis
- `get_quote <ticker>` — latest quote
- `get_market_status` — is the market open, is today a holiday, early close, etc.
- `validate_order <ticker> <side> <qty>` — runs guardrail checks, returns pass/fail + reason
- `place_order <ticker> <side> <qty> <type>` — calls validator then Alpaca; returns order ID or structured rejection
- `cancel_order <id>` — cancel an open order
- `get_spy_benchmark` — SPY price/return for benchmarking

Document the tool layer in `CLAUDE.md`.

---

## 7. Logging, observability, metrics

Beyond the journal entries (narrative) the agent writes per routine, maintain a **structured metrics file** that is written to by a non-LLM script at end-of-day:

- Date
- Portfolio equity
- Cash
- Day's P&L (absolute and %)
- SPY close and SPY day return
- Cumulative return since experiment start
- Cumulative SPY return since experiment start
- Number of positions held
- Number of orders placed today
- Number of orders rejected by validator today

This file is the spine of the week-4 retrospective. Do not let the LLM write it directly — use a script that queries Alpaca and appends a row. The LLM can read it.

**Behavioral log.** In addition to per-routine journal entries, maintain a separate append-only log of behavioral flags:

- Guardrail rejections (ticker, rule violated, context)
- Stop-loss triggers
- Any case where the LLM's stated reasoning in one routine contradicts the previous routine
- Any ticker the LLM referenced that isn't in the locked universe (hallucinated tickers)
- Token usage per routine (read from Claude Code's own reporting if available)

This is the primary artifact of the experiment. Treat it with care.

---

## 8. Rules of behavior for the LLM (go in `CLAUDE.md`)

When you write `CLAUDE.md`, include these rules clearly. The LLM must follow them every session.

1. **You are not discovering a trading edge.** You are executing within hard constraints under a stated mandate. Do not claim to have discovered patterns that beat the market. You may form opinions about individual securities based on public information and your training, but frame them as opinions, not discoveries.

2. **Decisions must reference prior journal entries.** Before forming intents, read the last 3 journal entries. Do not make decisions that contradict recent reasoning without explicitly acknowledging and justifying the change.

3. **Sizing defaults.** When opening a new position, default to 5% of portfolio equity unless there is an explicit reason to go larger (capped at 10%). Document the reason.

4. **Stops are yours to manage.** Alpaca is not holding stops for you. Every routine, check every position's current price against its average entry; if loss exceeds 8%, place a market-sell order that routine.

5. **If a tool returns an error, log and stop the routine.** Do not retry. Do not improvise. The operator investigates.

6. **If the market calendar tool says markets are closed, exit immediately.** Do not place orders "for when it opens."

7. **Never modify `INSTRUCTIONS.md`, `CLAUDE.md`, `MEMORY.md`, `.env`, `.gitignore`, or any file under `tools/` during a routine run.** These are build-phase-only files. If you think one needs to change, write a note to `notes-for-operator.md` and continue.

8. **Never place an order whose ticker is not in the locked universe.** The validator will reject it, but don't attempt it.

9. **You do not have the ability to improve yourself.** Writing reflections is logging, not learning. Do not act as though last week's reflections will change your behavior — they only change your behavior if the operator folds them back into `CLAUDE.md`.

10. **Cost awareness.** Keep journal entries terse. Favor bullet points and numbers over prose. The operator is paying per token.

---

## 9. Technical failure vs strategy failure — the distinction

The experiment has no kill switch for losing trades. It has an immediate kill switch for technical failures. Know the difference.

**Strategy failure (keep running):**
- Portfolio down 12% after 2 weeks
- Eight losing trades in a row
- LLM picks a bad stock
- LLM's stated thesis turns out wrong
- Underperforming SPY badly

**Technical failure (stop, investigate, fix, restart):**
- Duplicate orders being placed
- Orders placed outside market hours
- Validator being bypassed
- Tokens burning at >3x expected rate
- Tool calls failing silently
- State files getting corrupted or inconsistent with Alpaca
- API keys appearing in a journal entry or commit
- Routine running against a non-whitelisted ticker
- Any behavior the operator cannot explain after reading the journal

If a technical failure occurs, the operator will pause routines, fix, reset state to match Alpaca reality, and resume. The experiment window pauses during the fix.

---

## 10. Build-phase checklist (your first run)

On first run, before any trading happens, you must produce:

1. `.gitignore` — including `.env`, `.lock`, any local cache files
2. `.env.example` — with `ALPACA_API_KEY`, `ALPACA_API_SECRET`, `ALPACA_BASE_URL=https://paper-api.alpaca.markets` (and any others needed)
3. `README.md` — a short human-facing readme explaining what the project is and how to run it
4. `CLAUDE.md` — the concise operational brief the LLM reads every session. Must include: mandate, universe rules (pending lock), hard limits, routine definitions, tool list, behavioral rules, memory layout pointers
5. `MEMORY.md` — documenting the memory layout you chose
6. Directory scaffold per your chosen layout
7. Tool layer per Section 6 — with each tool independently runnable
8. A `Makefile` or equivalent with targets: `test-tools`, `run-premarket`, `run-execution`, `run-eod`, `run-weekly`, `reset-state`
9. An empty but initialized journal/ state/ trades/ directory structure
10. A `notes-for-operator.md` — append-only file where you write anything that needs human attention

**Do not place any trades during the build phase.** Do not call `place_order` even as a test. The operator will do an end-to-end dry run manually before enabling the live routines.

---

## 11. Week-1 special behavior

Week 1 is different from weeks 2–4 in two ways:

1. **Universe proposal.** On the first pre-market run of week 1, propose a universe meeting the Section 2 constraints. Write it to `universe-proposal.md`. Continue paper-trading decisions only against SPY and QQQ for the first week while the operator reviews and locks the universe.

2. **No news ingestion yet.** The first week runs on price/technical data only. News tools will be added later if the operator approves.

At the end of week 1, the operator reviews the proposed universe, locks it into `CLAUDE.md`, and full-universe trading begins Monday of week 2.

---

## 12. End of experiment — week-4 deliverable

On the final Friday weekly review, produce `retrospective.md` including:

- Final portfolio equity and cumulative return
- SPY cumulative return over the same window
- Sharpe ratio (daily returns), max drawdown, win rate, avg winner / avg loser
- Count of: trades placed, trades rejected by validator, stop-losses triggered, hallucinated-ticker attempts, self-contradictions flagged
- Narrative summary of the week-by-week behavioral arc
- Three observations about LLM behavior the operator should not miss
- Three observations that surprised you

The operator then decides: iterate, restart, or kill. You do not make that decision.

---

## 13. Things you are explicitly not doing

State these in `CLAUDE.md` to prevent scope creep:

- Not trading options, futures, crypto, forex, or anything other than US equities/ETFs in the locked universe
- Not using margin. Cash account behavior only. Do not short.
- Not day-trading in the pattern-day-trader sense. A position opened today is held at least overnight unless its stop triggers.
- Not reading or writing outside the repo directory
- Not making network calls outside Alpaca endpoints (week 1). News and other data sources require operator approval.
- Not learning in any meaningful sense across sessions. Memory is narrative continuity, not weight updates.
- Not talking to the operator during routines. If you need human input, write to `notes-for-operator.md` and exit the routine.

---

## 14. How to use this file on first run

1. Read this entire file.
2. Ask no clarifying questions unless something is genuinely contradictory — this spec has already been negotiated.
3. Design the memory layout (Section 5) and tool layer (Section 6).
4. Produce every artifact in Section 10.
5. Write `CLAUDE.md` as a concise operational brief — not a copy of this file. Aim for CLAUDE.md to be under 200 lines. It should cover mandate, limits, routines, tools, rules, memory pointers. It should not restate the rationale or the experimental framing beyond a one-line summary.
6. When scaffolding is complete, write a summary to `notes-for-operator.md` listing what you built and anything you weren't sure about.
7. Exit.

The operator will review, then begin manual routine testing.

---

**End of INSTRUCTIONS.md.**