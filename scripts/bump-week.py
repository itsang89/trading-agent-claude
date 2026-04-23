#!/usr/bin/env python3
"""Increment current_week in experiment-config.json. Run every Monday before pre-market."""
import json
import sys
from pathlib import Path

CONFIG = Path(__file__).parent.parent / "state" / "experiment-config.json"

data = json.loads(CONFIG.read_text())
week = data.get("current_week", 1)

if week >= 4:
    print(f"current_week already at {week} (max 4), no change.", file=sys.stderr)
    sys.exit(0)

data["current_week"] = week + 1
CONFIG.write_text(json.dumps(data, indent=2) + "\n")
print(f"current_week: {week} → {week + 1}")
