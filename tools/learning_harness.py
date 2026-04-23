#!/usr/bin/env python3
"""
learning_harness.py — Manual fallback for lesson extraction.

The weekly-review routine (make run-weekly) now performs lesson extraction
directly as Step 9 and writes the LEARNED BEHAVIORS block itself.

Only run this script manually if the Friday weekly-review routine failed to
complete Step 9 (e.g. the session was interrupted before lesson extraction).

    python3 tools/learning_harness.py

No ANTHROPIC_API_KEY required — delegates to the local `claude` CLI.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_JOURNAL_DIR = _REPO_ROOT / "journal"
_FLAGS_LOG = _REPO_ROOT / "logs" / "behavioral-flags.jsonl"
_METRICS_CSV = _REPO_ROOT / "metrics" / "daily-metrics.csv"
_LEARNINGS_DIR = _REPO_ROOT / "learnings"
_HARNESS_LOG = _REPO_ROOT / "logs" / "learning-harness.jsonl"
_CONFIG_PATH = _REPO_ROOT / "state" / "experiment-config.json"

_START_MARKER = "<!-- LEARNED_BEHAVIORS:START -->"
_END_MARKER = "<!-- LEARNED_BEHAVIORS:END -->"


def _get_week_number() -> int:
    if _CONFIG_PATH.exists():
        config = json.loads(_CONFIG_PATH.read_text())
        return config.get("current_week", 1)
    return 1


def _get_this_week_journals() -> str:
    """Read all journal files from the past 7 calendar days."""
    cutoff = date.today() - timedelta(days=7)
    entries = []
    for f in sorted(_JOURNAL_DIR.glob("*.md")):
        try:
            file_date = date.fromisoformat(f.name[:10])
            if file_date >= cutoff:
                entries.append(f"### {f.name}\n{f.read_text()}")
        except (ValueError, IndexError):
            continue
    return "\n\n---\n\n".join(entries) if entries else "(No journal entries found this week)"


def _get_recent_flags(n: int = 60) -> str:
    """Read last n lines of behavioral-flags.jsonl."""
    if not _FLAGS_LOG.exists():
        return "(No behavioral flags)"
    lines = _FLAGS_LOG.read_text().strip().splitlines()
    recent = lines[-n:] if len(lines) > n else lines
    return "\n".join(recent) if recent else "(No behavioral flags)"


def _get_recent_metrics(n: int = 5) -> str:
    """Read last n rows of daily-metrics.csv."""
    if not _METRICS_CSV.exists():
        return "(No metrics data)"
    lines = _METRICS_CSV.read_text().strip().splitlines()
    if len(lines) <= 1:
        return "(No metric rows yet)"
    header = lines[0]
    data = lines[-n:] if len(lines) > n + 1 else lines[1:]
    return header + "\n" + "\n".join(data)


def _extract_current_learned_behaviors() -> str:
    """Extract the current LEARNED_BEHAVIORS block from CLAUDE.md."""
    content = _CLAUDE_MD.read_text()
    if _START_MARKER not in content or _END_MARKER not in content:
        return "(No existing learned behaviors)"
    start_idx = content.index(_START_MARKER) + len(_START_MARKER)
    end_idx = content.index(_END_MARKER)
    return content[start_idx:end_idx].strip()


def _build_extraction_prompt(
    week: int,
    journals: str,
    flags: str,
    metrics: str,
    existing_rules: str,
) -> str:
    return f"""You are a behavioral analyst reviewing the trading logs of an LLM agent.

Your task: extract durable, actionable rules the agent should follow in future sessions based on this week's evidence.

## Week {week} journal entries
{journals}

## Week {week} behavioral flags (JSONL)
{flags}

## Week {week} performance metrics (CSV)
{metrics}

## Rules already in CLAUDE.md (do not duplicate these):
{existing_rules}

---

## Instructions

Extract 2–8 NEW behavioral rules that are:
1. **Durable** — they will apply in future weeks, not just this week
2. **Actionable** — a future session reading the rule knows exactly what to do differently
3. **Evidence-based** — you can cite a specific event from the logs above as the source
4. **Scoped** — one rule = one behavior. No compound rules.

Do NOT extract rules about:
- Specific price levels or exact dollar values (they expire)
- Current macro conditions that will change (e.g. "market is choppy this week")
- Anything already covered by the existing rules list above

Rule format — use EXACTLY this format, one rule per line:
- [W{week}|CONFIDENCE] Rule text here.
  Source: One sentence citing the specific log event.

CONFIDENCE levels:
- HIGH — behavior appeared in 3+ separate journal entries or flags
- MEDIUM — appeared 1–2 times, pattern is clear
- LOW — single instance, worth noting, provisional

Organize rules under one of these headers:
### Sizing and Risk
### Execution Patterns
### Market Regime Awareness
### Behavioral Failure Modes

If you find no new durable rules this week, respond with exactly the word: NO_NEW_RULES

Do not add any commentary, preamble, or explanation outside the rule list and headers."""


def _update_claude_md(new_rules_text: str) -> tuple[str, str]:
    """
    Replace the LEARNED_BEHAVIORS block in CLAUDE.md with new_rules_text.
    Returns (hash_before, hash_after).
    Writes atomically.
    """
    content = _CLAUDE_MD.read_text()
    hash_before = hashlib.md5(content.encode()).hexdigest()

    if _START_MARKER not in content or _END_MARKER not in content:
        raise ValueError(
            f"CLAUDE.md missing delimiters {_START_MARKER} / {_END_MARKER}. "
            "Cannot update learned behaviors."
        )

    before = content[:content.index(_START_MARKER) + len(_START_MARKER)]
    after = content[content.index(_END_MARKER):]

    updated = before + "\n" + new_rules_text + "\n\n" + after

    # Atomic write
    tmp = _CLAUDE_MD.with_suffix(".tmp")
    tmp.write_text(updated)
    os.replace(tmp, _CLAUDE_MD)

    hash_after = hashlib.md5(updated.encode()).hexdigest()
    return hash_before, hash_after


def _call_claude_cli(prompt: str, model: str = "claude-sonnet-4-6") -> str:
    """Invoke `claude --print` as a subagent and return the response text."""
    result = subprocess.run(
        ["claude", "--print", "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        cwd=str(_REPO_ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude CLI exited {result.returncode}:\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


def _write_learnings_file(week: int, rules_text: str):
    """Write learnings/YYYY-WW.md with the extracted rules."""
    today = date.today()
    iso_week = today.isocalendar()[1]
    filename = _LEARNINGS_DIR / f"{today.year}-W{iso_week:02d}-week{week}.md"
    content = f"""# Learnings — Week {week} ({today.isoformat()})

Extracted by learning_harness.py (via claude CLI)

---

{rules_text}
"""
    filename.write_text(content)
    return filename


def _append_audit_log(entry: dict):
    """Append a JSON line to logs/learning-harness.jsonl."""
    with open(_HARNESS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    week = _get_week_number()
    print(f"Learning harness — Week {week}")
    print("Reading journals, flags, and metrics...")

    journals = _get_this_week_journals()
    flags = _get_recent_flags()
    metrics = _get_recent_metrics()
    existing_rules = _extract_current_learned_behaviors()

    print(f"  Journals: {len(journals)} chars")
    print(f"  Flags: {len(flags)} chars")
    print(f"  Metrics: {len(metrics)} chars")

    prompt = _build_extraction_prompt(week, journals, flags, metrics, existing_rules)

    print("Invoking claude CLI for rule extraction...")
    try:
        rules_text = _call_claude_cli(prompt)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if rules_text == "NO_NEW_RULES":
        print("No new durable rules found this week.")
        _append_audit_log({
            "date": date.today().isoformat(),
            "week": week,
            "rules_extracted": 0,
            "rules_added": 0,
            "no_new_rules": True,
            "model": "claude-sonnet-4-6",
        })
        return

    rule_count = rules_text.count(f"[W{week}|")

    learnings_file = _write_learnings_file(week, rules_text)
    print(f"  Learnings written to: {learnings_file.name}")

    prior_rules = existing_rules if "(No existing" not in existing_rules else ""
    full_block = ""
    if prior_rules:
        full_block += prior_rules.strip() + "\n\n---\n\n"
    full_block += f"*Week {week} lessons added {date.today().isoformat()} by learning_harness.py*\n\n"
    full_block += rules_text

    hash_before, hash_after = _update_claude_md(full_block)
    print(f"  CLAUDE.md updated (md5: {hash_before[:8]} → {hash_after[:8]})")
    print(f"  {rule_count} new rule(s) added.")

    _append_audit_log({
        "date": date.today().isoformat(),
        "week": week,
        "rules_extracted": rule_count,
        "rules_added": rule_count,
        "no_new_rules": False,
        "model": "claude-sonnet-4-6",
        "claude_md_hash_before": hash_before,
        "claude_md_hash_after": hash_after,
        "learnings_file": learnings_file.name,
    })

    print("\nDone. Review CLAUDE.md changes before next session:")
    print("  git diff CLAUDE.md")
    print(f"  cat {learnings_file}")


if __name__ == "__main__":
    main()
