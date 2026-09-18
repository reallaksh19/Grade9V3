#!/usr/bin/env python3
"""Tiny deterministic delayed-review policy for one learner.

This is intentionally not a spaced-repetition platform. It answers one practical
question: after this attempt, when should the capability be checked again?

Initial policy:
  INCORRECT             -> +1 day
  CORRECT_WITH_HINT     -> +3 days
  CORRECT_INDEPENDENT   -> +7 days
  TRANSFER_INDEPENDENT  -> +14 days

The policy is isolated here so it can be replaced later without rewriting learner
observations or curriculum records.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

INTERVAL_DAYS = {
    "INCORRECT": 1,
    "CORRECT_WITH_HINT": 3,
    "CORRECT_INDEPENDENT": 7,
    "TRANSFER_INDEPENDENT": 14,
}


def _date(value: str) -> date:
    """Accept an ISO date or timestamp and keep only its calendar date."""
    if not value:
        raise ValueError("when is required")
    return date.fromisoformat(value[:10])


def next_review(outcome: str, when: str) -> str:
    if outcome not in INTERVAL_DAYS:
        raise ValueError(
            f"outcome must be one of {', '.join(sorted(INTERVAL_DAYS))}"
        )
    return (_date(when) + timedelta(days=INTERVAL_DAYS[outcome])).isoformat()


def outcome_from_observation(observation: dict, *, transfer: bool = False) -> str:
    """Map the existing observation contract into the small review policy."""
    result = observation.get("result")
    help_used = observation.get("help", "UNKNOWN")

    if result == "DEMONSTRATED" and help_used == "NONE":
        return "TRANSFER_INDEPENDENT" if transfer else "CORRECT_INDEPENDENT"

    if result == "UNCERTAIN" and help_used in {"HINT", "WORKED_EXAMPLE", "SOLUTION"}:
        return "CORRECT_WITH_HINT"

    return "INCORRECT"


def schedule(observation: dict, *, transfer: bool = False) -> dict:
    outcome = outcome_from_observation(observation, transfer=transfer)
    return {
        "capability_ref": observation.get("capability_ref"),
        "observation_ref": observation.get("observation_id"),
        "outcome": outcome,
        "observed_on": _date(observation["when"]).isoformat(),
        "next_review": next_review(outcome, observation["when"]),
        "policy": "SIMPLE_1_3_7_14",
    }


def due(rows: list[dict], on: str) -> list[dict]:
    """Return due rows in deterministic date/capability order."""
    today = _date(on)
    return sorted(
        [
            row for row in rows
            if _date(row["next_review"]) <= today
        ],
        key=lambda row: (
            row["next_review"],
            str(row.get("capability_ref") or ""),
            str(row.get("observation_ref") or ""),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--transfer", action="store_true")
    args = parser.parse_args()
    observation = json.loads(args.observation.read_text(encoding="utf-8"))
    print(json.dumps(schedule(observation, transfer=args.transfer), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
