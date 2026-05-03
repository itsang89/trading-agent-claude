# Tools Reference

All tools live in `tools/`. Run from repo root. Each prints JSON to stdout.

```
python tools/get_account.py                                        # equity, cash, buying power
python tools/get_positions.py                                      # current holdings with P&L
python tools/get_bars.py <TICKER> [days]                           # OHLCV history (default 20d)
python tools/get_quote.py <TICKER>                                 # latest bid/ask
python tools/get_market_status.py                                  # open/closed, holiday, early close
python tools/get_spy_benchmark.py                                  # SPY return since experiment start
python tools/validate_order.py <T> <side> <qty>                    # dry-run guardrail check
python tools/place_order.py <T> <side> <qty> <type> [--stop-pct P] # validator → Alpaca; BUY + --stop-pct places GTC stop-sell at price*(1-P)
python tools/place_stop_order.py <T> <qty> <stop_price>            # place/replace GTC stop-sell (use when updating stop after an add)
python tools/cancel_order.py <order_id>                            # cancel open order (use before any sell to cancel standing stop)
```

### place_order.py — stop order behavior

`--stop-pct 0.08` (BUY only): after the primary order is submitted, immediately places a GTC stop-sell at `ask_price * (1 - 0.08)`. Returns `stop_order_id` and `stop_price` on success, or `stop_order_warning` on failure (non-blocking — primary order still succeeds).

Store `stop_order_id` and `stop_price` in `state/position-highs.json` for lifecycle management.

### Stop order lifecycle summary

| Event | Action |
|---|---|
| New BUY | `place_order.py --stop-pct 0.08` → store stop_order_id |
| ADD to position | cancel old stop → place add → `place_stop_order.py` for total qty → store new stop_order_id |
| Any SELL | `cancel_order.py <stop_order_id>` → then sell |
| Missing stop_order_id | `place_stop_order.py` at avg_entry × 0.92 immediately |

**If any tool returns an error, log it and stop the routine.** Do not retry. Do not improvise.
