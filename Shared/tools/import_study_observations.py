#!/usr/bin/env python3
"""Convert a prior question→study map into ordinary capability observations.

This tool does not create a second learner model. It translates a simple historical map
such as "Q13 -> slope capability -> uncertain" into the observation contract already used
by learner routing. It prints records; writing them into Learners/observations remains an
explicit caller action.

The caller must supply the observation date/time. Importing old evidence without knowing
when it was observed would make precedence misleading.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED = {"DEMONSTRATED", "UNCERTAIN", "MISSING"}


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-")
    return cleaned or "ROW"


def convert(payload: dict, when: str) -> list[dict]:
    study_map_id = payload.get("study_map_id")
    if not study_map_id:
        raise ValueError("study_map_id is required")
    if not when:
        raise ValueError("when is required")

    observations = []
    for index, row in enumerate(payload.get("rows", []), start=1):
        capability = row.get("capability_ref")
        observed = row.get("observed")
        result = row.get("suggested_state")
        if not capability or not observed:
            raise ValueError(f"row {index} requires capability_ref and observed")
        if result not in ALLOWED:
            raise ValueError(
                f"row {index} suggested_state must be one of {', '.join(sorted(ALLOWED))}"
            )
        question = row.get("question_ref")
        observation = {
            "observation_id": f'OBS-{_slug(study_map_id)}-{index:03d}',
            "capability_ref": capability,
            "method": f"prior study map {study_map_id}",
            "evidence_kind": "PRIOR_STUDY_MAP",
            "session_ref": study_map_id,
            "observed": observed,
            "result": result,
            "when": when,
            "help": "UNKNOWN",
            "error_stage": row.get("error_stage") or "UNKNOWN",
        }
        if question:
            observation["question_ref"] = question
        observations.append(observation)
    return observations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--when", required=True, help="ISO date/timestamp of the prior evidence")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(convert(payload, args.when), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
