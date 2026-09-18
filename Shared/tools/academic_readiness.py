#!/usr/bin/env python3
"""Mechanical academic-readiness checks, explicitly separate from human subject review."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402
from Shared.tools import capability_graph, review_authority  # noqa: E402

MECHANICAL_FIELDS = (
    ("entry_assumptions", "ENTRY_ASSUMPTIONS_MISSING"),
    ("inferential_jump", "INFERENTIAL_JUMP_MISSING"),
    ("misconceptions", "MISCONCEPTION_DIAGNOSTIC_MISSING"),
    ("exit_task", "OBSERVABLE_EXIT_MISSING"),
)


def findings(board: dict, mics: dict) -> list[dict]:
    """Check only observable prerequisites of an academic review; never claim truth."""
    found = []
    for row in board.get("rungs", []):
        rung, ref = row.get("rung"), row.get("microtopic_ref")
        mic = mics.get(ref)
        if mic is None:
            # Matrix conformance owns missing records; do not duplicate that finding.
            continue
        for field, point in MECHANICAL_FIELDS:
            value = mic.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                found.append({"point": point, "where": rung,
                              "detail": f"{ref} has no substantive {field}"})
        if not row.get("ceiling"):
            found.append({"point": "VOCABULARY_CEILING_MISSING", "where": rung,
                          "detail": "the rung declares no vocabulary ceiling"})
        if not row.get("controlled_variation"):
            found.append({"point": "CONTROLLED_VARIATION_MISSING", "where": rung,
                          "detail": "the rung declares no controlled variation"})
    return found


def _microtopic_package_paths(subject: str, repo: Path) -> dict[str, str]:
    found = {}
    for path in sorted((repo / subject / "library").glob("*.json")):
        package = load(path)
        for row in package.get("microtopics", []):
            found[row["id"]] = str(path.relative_to(repo))
    return found


def review_state(board: dict, mics: dict, subject: str, repo: Path = REPO) -> dict:
    ids = [row.get("microtopic_ref") for row in board.get("rungs", []) if row.get("microtopic_ref")]
    records = [mics[rid] for rid in ids if rid in mics]
    paths = _microtopic_package_paths(subject, repo)
    authorities = []
    for record in records:
        target = paths.get(record["id"])
        if target:
            authorities.append(
                review_authority.authority_for_record(subject, target, record, repo)
            )
        else:
            authorities.append({
                "state": "NOT_REVIEWED", "record_status": record.get("status", "UNKNOWN"),
                "verified": False, "receipt": None,
                "findings": [{"point": "REVIEW_TARGET_PACKAGE_UNKNOWN",
                              "where": record["id"],
                              "detail": "microtopic package path could not be resolved"}],
            })
    effective = sorted({row["state"] for row in authorities})
    release_backed = bool(records) and all(
        row.get("verified") and row.get("state") in {"REVIEWED", "CURATED"}
        for row in authorities
    )
    return {
        "state": "REVIEWED" if release_backed else "NOT_REVIEWED",
        "record_statuses": sorted({row.get("status", "UNKNOWN") for row in records}),
        "effective_review_states": effective,
        "reviewed_records": sum(
            1 for row in authorities
            if row.get("verified") and row.get("state") in {"REVIEWED", "CURATED"}
        ),
        "records": len(records),
        "authorities": authorities,
        "claim": "Mechanical checks do not establish scientific or pedagogical correctness; release review additionally requires digest-bound promotion receipts.",
    }


def board_report(board: dict, subject: str, repo: Path = REPO) -> dict:
    _, mics = capability_graph.subject_graph(subject, repo)
    found = findings(board, mics)
    review = review_state(board, mics, subject, repo)
    return {
        "bucket": board.get("bucket_id"),
        "mechanical_findings": found,
        "mechanically_reviewable": not found,
        "human_review": review,
        "learner_release_ready": not found and review["state"] == "REVIEWED",
    }


def audit(repo: Path = REPO) -> dict:
    rows = []
    for path in sorted(repo.glob("*/matrices/*.rungs.json")):
        board = load(path)
        row = board_report(board, board.get("subject", ""), repo)
        rows.append({"matrix": str(path.relative_to(repo)), **row})
    return {
        "boards": rows,
        "mechanical_findings": sum(len(row["mechanical_findings"]) for row in rows),
        "passed": all(not row["mechanical_findings"] for row in rows),
        "reviewed_boards": sum(row["human_review"]["state"] == "REVIEWED" for row in rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="enforce mechanical reviewability, never human review status")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
