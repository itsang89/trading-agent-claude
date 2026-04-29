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

# Set authenticated remote URL so pushes never rely on the local proxy.
# The local_proxy issues read-only tokens for some sessions; GITHUB_TOKEN
# (or a gh CLI token) is always write-capable. Do this here (not in the
# prompt) so Claude cannot skip it.
if [ -z "${GITHUB_TOKEN:-}" ] && command -v gh &>/dev/null; then
  GITHUB_TOKEN=$(gh auth token 2>/dev/null || true)
fi

if [ -n "${GITHUB_TOKEN:-}" ]; then
  git -C "$REPO_ROOT" remote set-url origin \
    "https://x-access-token:${GITHUB_TOKEN}@github.com/itsang89/trading-agent-claude.git"
else
  echo "WARNING: GITHUB_TOKEN not set and gh CLI unavailable — git push may fail if local proxy is read-only." >&2
fi

PROMPT_CONTENT=$(cat "$PROMPT_FILE")

export CURRENT_ROUTINE="$ROUTINE"

# In CI (GitHub Actions), skip interactive permission prompts
CI_FLAGS=()
if [ "${CI:-}" = "true" ]; then
  CI_FLAGS+=(--dangerously-skip-permissions)
fi

# Pass additional args (e.g. --model) plus CI flags
shift
exec claude -p "${CI_FLAGS[@]}" "$@" "$PROMPT_CONTENT"
