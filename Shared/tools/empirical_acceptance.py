#!/usr/bin/env python3
"""Report the empirical learner-acceptance evidence layer without fabricating a verdict.

Architectural regression is automatic. Learner acceptance is not: it requires reviewed
observations from an actual learner session. Missing live evidence is therefore PENDING,
not a CI failure. Structural defects in evidence that claims LIVE_LEARNER provenance are
failures because such evidence cannot be reviewed safely.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402

OBSERVATIONS = "Learners/observations"

PENDING = "PENDING_REAL_EVIDENCE"
AVAILABLE = "EMPIRICAL_EVIDENCE_AVAILABLE"
INVALID = "INVALID_EMPIRICAL_EVIDENCE"

LIVE = "LIVE_LEARNER"


def observations(repo: Path = REPO) -> list[dict]:
    root = repo / OBSERVATIONS
    if not root.exists():
        return []
    return [load(path) for path in sorted(root.glob("*.json"))]


def audit(repo: Path = REPO) -> dict:
    rows = observations(repo)
    live = [
        row for row in rows
        if row.get("provenance") == LIVE
        and row.get("evidence_kind") == "DIRECT_ATTEMPT"
    ]
    findings: list[dict] = []

    for row in live:
        oid = row.get("observation_id") or "UNKNOWN"
        if not row.get("session_ref"):
            findings.append({
                "point": "EMPIRICAL_LIVE_SESSION_REF_MISSING",
                "observation_ref": oid,
                "detail": "LIVE_LEARNER direct-attempt evidence must identify its learner session.",
            })
        if not row.get("question_ref"):
            findings.append({
                "point": "EMPIRICAL_LIVE_QUESTION_REF_MISSING",
                "observation_ref": oid,
                "detail": "LIVE_LEARNER direct-attempt evidence must identify the attempted question.",
            })

    if findings:
        status = INVALID
    elif live:
        status = AVAILABLE
    else:
        status = PENDING

    ignored = {
        provenance: sum(1 for row in rows if row.get("provenance") == provenance)
        for provenance in (
            "UNREVIEWED_SESSION_DRAFT",
            "HISTORICAL_IMPORT",
            "SYNTHETIC_TEST",
        )
    }

    return {
        "status": status,
        "observations": len(rows),
        "live_observations": sorted(
            row["observation_id"] for row in live if row.get("observation_id")
        ),
        "live_sessions": sorted({
            row["session_ref"] for row in live if row.get("session_ref")
        }),
        "ignored_by_provenance": ignored,
        "findings": findings,
        "passed": not findings,
        "rule": (
            "Regression may be automated; empirical learner acceptance requires reviewed "
            "LIVE_LEARNER direct-attempt evidence. Missing live evidence remains pending "
            "and never becomes a fabricated pass."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--enforce",
        action="store_true",
        help=(
            "fail only when evidence claiming LIVE_LEARNER provenance is structurally "
            "insufficient; PENDING_REAL_EVIDENCE remains a successful report"
        ),
    )
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
