#!/usr/bin/env python3
"""Audit that assessment demand is taught and proposed teaching has a scope reason.

The route generator already keeps scope small by construction. This audit exists as the
independent falsifier: callers may propose additional capabilities, and every one must be
justified by question demand, prerequisite closure, syllabus requirement or declared
extension. Conversely, question-demand capabilities must have a teaching location or an
explicit unresolved finding.
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
from Shared.tools import study_route  # noqa: E402

ASSESSMENT_NOT_TAUGHT = "ASSESSMENT_CAPABILITY_NOT_TAUGHT"
STUDY_NOT_TAUGHT = "STUDY_CAPABILITY_NOT_TAUGHT"
UNJUSTIFIED = "TEACHING_SCOPE_UNJUSTIFIED"


def audit(mapping: dict, proposed_capabilities: list[str] | None = None,
          repo: Path = REPO) -> dict:
    route = study_route.resolve(mapping, repo)
    findings = list(route["findings"])

    routed = {row["capability_ref"]: row for row in route.get("route", [])}
    for row in route.get("route", []):
        if row["state"] == "RESOLVED":
            continue
        point = (ASSESSMENT_NOT_TAUGHT if "QUESTION_DEMAND" in row["reasons"]
                 else STUDY_NOT_TAUGHT)
        findings.append({
            "point": point,
            "capability": row["capability_ref"],
            "detail": (
                f'{row["scope"]} capability is in the study slice but has state '
                f'{row["state"]}'
            ),
        })

    proposed = list(proposed_capabilities) if proposed_capabilities is not None else list(routed)
    seen = set()
    for capability in proposed:
        if capability in seen:
            continue
        seen.add(capability)
        if capability not in routed:
            findings.append({
                "point": UNJUSTIFIED,
                "capability": capability,
                "detail": (
                    "proposed teaching is not justified by question demand, prerequisite "
                    "closure, syllabus requirement or declared extension"
                ),
            })
            continue
        if not routed[capability].get("reasons"):
            findings.append({
                "point": UNJUSTIFIED,
                "capability": capability,
                "detail": "routed capability carries no scope reason",
            })

    return {
        "worksheet_id": route.get("worksheet_id"),
        "subject": route.get("subject"),
        "route": route.get("route", []),
        "proposed_capabilities": proposed,
        "findings": findings,
        "passed": not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--proposed-capability", action="append", default=None)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    report = audit(load(args.map), args.proposed_capability)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
