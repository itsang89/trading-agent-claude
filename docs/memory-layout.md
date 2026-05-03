# Memory Layout

```
state/positions.json       — current positions (re-fetched each routine, overwrite)
state/account.json         — account snapshot (overwrite)
state/universe.json        — locked universe + sector map (read-only during routines)
state/position-highs.json  — peak close price per held ticker for trailing stops (overwrite on change)
trades/trades.csv          — append-only trade log
journal/YYYY-MM-DD-*.md    — per-routine narrative entries (never overwrite)
metrics/daily-metrics.csv  — daily P&L and benchmark (written by append_metrics.py, not you)
logs/behavioral-flags.jsonl — append-only behavioral event log
notes-for-operator.md      — append-only; write here instead of stopping for human input
```
