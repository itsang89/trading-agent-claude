SHELL := /bin/bash
.PHONY: test-tools run-premarket run-execution run-midsession run-eod run-weekly run-learning-harness reset-state

# Verify all read-only tools return valid output
test-tools:
	@echo "=== get_account ==="
	python3 tools/get_account.py
	@echo ""
	@echo "=== get_positions ==="
	python3 tools/get_positions.py
	@echo ""
	@echo "=== get_market_status ==="
	python3 tools/get_market_status.py
	@echo ""
	@echo "=== get_spy_benchmark ==="
	python3 tools/get_spy_benchmark.py
	@echo ""
	@echo "=== get_bars SPY 5 ==="
	python3 tools/get_bars.py SPY 5
	@echo ""
	@echo "=== get_quote SPY ==="
	python3 tools/get_quote.py SPY
	@echo ""
	@echo "=== validate_order SPY buy 1 market (dry run) ==="
	python3 tools/validate_order.py SPY buy 1 market
	@echo ""
	@echo "All tools tested."

# Run routines via Claude — each uses its full prompt file from prompts/
run-premarket:
	@bash scripts/run-routine.sh pre-market-research

run-execution:
	@bash scripts/run-routine.sh market-open-execution

run-midsession:
	@bash scripts/run-routine.sh mid-session-check

run-eod:
	@bash scripts/run-routine.sh end-of-day-review
	@echo ""
	@echo "=== Appending daily metrics ==="
	python3 tools/append_metrics.py

run-weekly:
	@bash scripts/run-routine.sh weekly-review --model claude-opus-4-7

# Extract this week's lessons and update CLAUDE.md
# Run manually after reviewing the weekly journal entry
run-learning-harness:
	python3 tools/learning_harness.py
	@echo ""
	@echo "Review CLAUDE.md changes before next session."

# Reset live-state cache files (re-fetched from Alpaca on next routine run)
reset-state:
	@echo "This will delete state/positions.json and state/account.json."
	@echo "They will be re-fetched from Alpaca on the next routine run."
	@read -p "Type 'yes' to confirm: " confirm && [ "$$confirm" = "yes" ]
	rm -f state/positions.json state/account.json
	@echo "State cache cleared."
