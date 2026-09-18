#!/usr/bin/env python3
"""Convert a prior question→study map into ordinary capability observations.

This tool does not create a second learner model. It translates a simple historical map
such as "Q13 -> slope capability -> uncertain" into the observation contract already used
by learner routing. It prints records; writing them into Learners/observations remains an
explicit caller action.

If a worksheet-map is supplied, a row may omit capability_ref only when its question maps
to exactly one capability. A multi-capability question is deliberately ambiguous: the
importer refuses to guess which capability the historical note was evidence about.

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


def _worksheet_index(worksheet_map: dict | None) -> dict[str, list[str]]:
    if not worksheet_map:
        return {}
    found: dict[str, list[str]] = {}
    for row in worksheet_map.get("questions", []):
        qid = row.get("question_id")
        primary = row.get("primary_capability_ref")
        secondary = list(row.get("secondary_capability_refs") or [])
        if qid:
            found[qid] = [cap for cap in [primary, *secondary] if cap]
    return found


def _resolve_capability(row: dict, index: int,
                        worksheet_index: dict[str, list[str]]) -> str:
    capability = row.get("capability_ref")
    question = row.get("question_ref")
    mapped = worksheet_index.get(question, []) if question else []

    if capability:
        if mapped and capability not in mapped:
            raise ValueError(
                f"row {index} capability_ref {capability} is not among the mapped "
                f"capabilities for {question}: {', '.join(mapped)}"
            )
        return capability

    if not question:
        raise ValueError(
            f"row {index} requires capability_ref, or question_ref plus a worksheet map"
        )
    if not mapped:
        raise ValueError(
            f"row {index} question_ref {question} has no mapping in the supplied worksheet map"
        )
    if len(mapped) != 1:
        raise ValueError(
            f"row {index} question_ref {question} maps to multiple capabilities "
            f"({', '.join(mapped)}); supply capability_ref rather than guessing"
        )
    return mapped[0]


def convert(payload: dict, when: str,
            worksheet_map: dict | None = None) -> list[dict]:
    study_map_id = payload.get("study_map_id")
    if not study_map_id:
        raise ValueError("study_map_id is required")
    if not when:
        raise ValueError("when is required")

    mapped_questions = _worksheet_index(worksheet_map)
    observations = []
    for index, row in enumerate(payload.get("rows", []), start=1):
        capability = _resolve_capability(row, index, mapped_questions)
        observed = row.get("observed")
        result = row.get("suggested_state")
        if not observed:
            raise ValueError(f"row {index} requires observed")
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
    parser.add_argument(
        "--worksheet-map",
        type=Path,
        help=(
            "optional worksheet capability map; permits capability_ref omission only "
            "for questions with exactly one mapped capability"
        ),
    )
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    worksheet_map = (
        json.loads(args.worksheet_map.read_text(encoding="utf-8"))
        if args.worksheet_map else None
    )
    print(json.dumps(
        convert(payload, args.when, worksheet_map),
        indent=2,
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
