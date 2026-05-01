Your stated requirements:
1. Learning Harness Purpose: Test if the AI agent can learn from experience/mistakes and improve itself — core experiment goal.
2. Change Criteria: Allowed self-edits (strategy, soft rules); disallowed changes (hard limits, tools) need operator proposal with rationale. All changes must boost SPY-beating performance.
3. Review Goal: Read all logged data, find flaws/gaps, implement allowed fixes, propose disallowed changes, persist learnings. This is the experiment's most critical component.

---
1. Does the updated weekly-review.md do the job of testing if the agent can learn from experience/mistakes and improve?
It covers ~80% of the core requirements for your experiment goal:
- ✅ Identifies execution/strategy/routine/technical gaps via cross-referenced performance + behavioral data
- ✅ Allows self-implementation of allowed changes (edits to state/strategy.md for signal rules, sizing, exits)
- ✅ Persists learning across sessions via CLAUDE.md LEARNED_BEHAVIORS updates
- ✅ Proposes disallowed changes (hard limits, tools, config) to you with linked rationale
Critical gaps for proving learning exist:
- ❌ No check on whether changes made in prior weekly reviews actually improved SPY outperformance (missing "did my fix work?" step)
- ❌ No backtesting of proposed strategy changes against historical data to validate they would improve returns
- ❌ No tracking of repeated mistakes (e.g., a flaw fixed in Week 2 reoccurring in Week 3)
- ❌ No requirement to measure the impact of each change in subsequent weeks
---
2. What do I think about the weekly review frequency?
Weekly (Fridays 5PM) is appropriate for your 4-week experiment:
- 4 total review cycles align with the experiment window, giving enough iterations to demonstrate learning progression (Week 1: baseline → Week 2: first changes → Week 3: measure Week 2 changes → Week 4: final adjustments)
- Each review has 5 trading days of data, enough to make meaningful, low-noise changes
- More frequent (e.g., every 3 days) would have more iterations but noisier data; less frequent (bi-weekly) would only have 2 cycles, insufficient to show learning
Minor recommendation: Keep weekly frequency, but add a requirement to log urgent critical flaws (e.g., repeated stop-loss triggers from a broken rule) to notes-for-operator.md mid-week for out-of-cycle review if needed.
---
Plan to Fix Gaps (Ready for Execution Post-Plan Mode)
No edits will be made now per Plan Mode rules. Below is the structured plan to update prompts/weekly-review.md to close the learning loop:
Step 1: Add Prior Change Efficacy Check (New Step 6.5)
Insert between current Step 6 (Contradiction Audit) and Step 7 (Flaw & Gap Analysis):
### Step 6.5 — Prior Change Impact Check
Read all prior `learnings/{YYYY}-W{WW}-week{N}.md` files and `CLAUDE.md` LEARNED_BEHAVIORS rules from previous weeks.
For every strategy change (Step 11 Part A) or behavioral rule added in prior weekly reviews:
1. Compare the week-over-week SPY outperformance before vs after the change was implemented
2. Flag any change that *reduced* SPY outperformance or had no effect
3. Propose reverting or adjusting ineffective changes in Step 11
4. Log results in the new "Prior Changes Impact" journal section (Step 9)
Step 2: Add Backtesting Requirement for Strategy Changes (Update Step 11 Part A)
Add to the allowed self-implementation rules:
For each strategy.md change:
1. Use `python tools/get_bars.py <TICKER> 20` to fetch historical data for held/universe tickers
2. Backtest the new rule against past 20 days of data vs the old rule
3. Include backtest results (expected return improvement) in the change rationale
4. Only implement changes with positive backtest results
Step 3: Add Repeated Mistake Tracking (Update Step 8 Flaw & Gap Analysis)
Add to Step 8:
5. **Repeated Mistakes**: Check if any identified flaw matches a prior week's LEARNED_BEHAVIOR rule or fixed gap. If a flaw repeats across 2+ weeks, mark as CRITICAL severity and require a more aggressive fix (e.g., rule update + strategy change).
Step 4: Expand Journal Requirements (Update Step 9)
Add a new required section to the weekly journal:
- **Prior Changes Impact**: Summary of whether changes from previous weeks improved/hurt SPY outperformance, with data backing
Step 5: Expand Proposal Scope (Update Step 11 Part B)
Add prompt files to allowed proposal targets, since they are part of the agent's operational logic:
Proposal format now also accepts:
- `prompts/*.md` (routine prompts, if flaws are found in instruction clarity or workflow gaps)
---
Verification Plan (Post-Edit)
After making the above changes, run a dry-run test:
1. Simulate a Week 2 review with a fake strategy change from Week 1
2. Verify the agent checks if the Week 1 change improved SPY return
3. Verify backtesting is attempted for new strategy changes
4. Confirm repeated mistakes are flagged as CRITICAL