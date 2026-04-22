#!/bin/bash
# run-routine.sh — Run a Claude routine using its prompt file.
# Usage: ./scripts/run-routine.sh <routine-name> [--model <model-id>]
#
# Example:
#   ./scripts/run-routine.sh pre-market-research
#   ./scripts/run-routine.sh weekly-review --model claude-opus-4-6

set -euo pipefail

ROUTINE=$1
PROMPT_FILE="$(dirname "$0")/../prompts/${ROUTINE}.md"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

LOCK_FILE="$(dirname "$0")/../.lock"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Concurrency guard: check for fresh lock file (<30 min)
if [ -f "$LOCK_FILE" ]; then
  if [[ "$(uname)" == "Darwin" ]]; then
    LOCK_MTIME=$(stat -f %m "$LOCK_FILE")
  else
    LOCK_MTIME=$(stat -c %Y "$LOCK_FILE")
  fi
  LOCK_AGE=$(( $(date +%s) - LOCK_MTIME ))
  if [ "$LOCK_AGE" -lt 1800 ]; then
    echo "ERROR: Lock file exists and is ${LOCK_AGE}s old (<30 min). Another routine may be running." >&2
    echo "If no routine is running, delete .lock and retry." >&2
    exit 1
  fi
fi

# Write lock file
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $ROUTINE" > "$LOCK_FILE"

# Cleanup lock on exit
trap 'rm -f "$LOCK_FILE"' EXIT

PROMPT_CONTENT=$(cat "$PROMPT_FILE")

export CURRENT_ROUTINE="$ROUTINE"

# Pass additional args (e.g. --model)
shift
exec claude -p "$@" "$PROMPT_CONTENT"
