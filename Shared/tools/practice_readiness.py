#!/usr/bin/env python3
"""Report practice-product readiness from the planner and compiler, bucket by bucket.

A matrix can carry taught rungs and transfer rows without holding a question that the
compiler can actually place in CORE2A or CORE2B. This audit makes that distinction
visible across a subject and enforces the one safe implication:

    planner says READY  =>  compiler selects that practice core

BLOCKED is not a failure. It is the truthful state when the bucket has no exposed
question yet. WITHHELD is likewise intentional when the selected purpose does not
route transfer.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.library.compile_inputs import compile_bucket  # noqa: E402
from Shared.library.resolve import build_index, slice_for_bucket  # noqa: E402
from Shared.library.practice import owned_questions  # noqa: E402
from Shared.tools import resolve_request  # noqa: E402

PRACTICE = ("CORE2A", "CORE2B")


def _practice_coverage(records: dict, bucket_id: str, questions: list[dict]) -> dict:
    """Coverage of this bucket's taught primary capabilities by local practice items."""
    bucket = records.get(bucket_id, {})
    policy = (bucket.get("extensions") or {}).get("practice_coverage_policy")
    taught = sorted({
        record.get("primary_capability_ref")
        for record in records.values()
        if record.get("_collection") == "microtopics"
        and record.get("bucket_id") == bucket_id
        and record.get("primary_capability_ref")
    })
    practiced: set[str] = set()
    for question in questions:
        if not any(entry.get("core") in PRACTICE for entry in question.get("exposure", [])):
            continue
        primary = question.get("primary_capability_ref")
        if primary:
            practiced.add(primary)
        practiced.update(question.get("secondary_capability_refs", []))
    covered = sorted(capability for capability in taught if capability in practiced)
    missing = sorted(capability for capability in taught if capability not in practiced)
    return {
        "policy": policy,
        "taught_primary_capabilities": taught,
        "practice_covered_capabilities": covered,
        "missing_capabilities": missing,
    }


def _request(subject: str, board: dict) -> dict:
    position = min(row["ladder_position"] for row in board.get("rungs", []))
    return {
        "request_id": f'readiness:{board["bucket_id"]}',
        "subject": subject,
        "bucket_id": board["bucket_id"],
        "cores": list(PRACTICE),
        "learner": {
            "owner_estimate": {
                "knowledge_percentage": position,
                "by": "PRACTICE_READINESS_AUDIT",
                "instruction": "Use the ladder entry only to expose practice readiness.",
            }
        },
        "practice": {
            "CORE2A": {"purpose": "PRACTICE"},
            "CORE2B": {"purpose": "PRACTICE"},
        },
    }


def audit(subject: str, repo: Path = REPO) -> dict:
    library_paths = sorted((repo / subject / "library").glob("*.v1.json"))
    matrix_paths = sorted((repo / subject / "matrices").glob("*.rungs.json"))
    packages = [load(path) for path in library_paths]
    records = build_index(packages)

    rows, findings = [], []
    for path in matrix_paths:
        board = load(path)
        bucket_id = board["bucket_id"]
        plan = resolve_request.plan(_request(subject, board), repo)
        planned = {row["core"]: row for row in plan.get("cores", [])}

        compiler_error = None
        selected: set[str] = set()
        try:
            compiled = compile_bucket(
                records, bucket_id,
                topic_id="readiness-audit", title=board.get("subtopic", bucket_id),
                subject=subject,
                practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"},
            )
            selected = set(compiled["baseline"]["selected_cores"])
        except ContractError as error:
            compiler_error = {"code": error.code, "detail": error.detail}

        questions = owned_questions(records, bucket_id)
        coverage = _practice_coverage(records, bucket_id, questions)
        if (coverage["policy"] == "ALL_PRIMARY_CAPABILITIES"
                and coverage["missing_capabilities"]):
            findings.append({
                "point": "BUCKET_PRACTICE_COVERAGE_INCOMPLETE",
                "bucket": bucket_id,
                "missing_capabilities": coverage["missing_capabilities"],
                "detail": "bucket opts into ALL_PRIMARY_CAPABILITIES but local practice does not cover every taught primary capability",
            })
        exposed = {
            core: [
                q["id"] for q in questions
                if any(entry.get("core") == core for entry in q.get("exposure", []))
            ]
            for core in PRACTICE
        }

        for core in PRACTICE:
            state = planned.get(core, {}).get("state")
            if state == "READY" and not exposed[core]:
                findings.append({
                    "point": "PLAN_READY_WITHOUT_BUCKET_OWNED_QUESTION",
                    "bucket": bucket_id,
                    "core": core,
                    "detail": "practice is READY but only prerequisite/reachable questions, not a question owned by this bucket, could support it",
                })
            if state == "READY" and core not in selected:
                findings.append({
                    "point": "PLAN_READY_COMPILER_UNSUPPORTED",
                    "bucket": bucket_id,
                    "core": core,
                    "detail": "resolve_request says READY but compile_bucket does not select the core",
                })
            if (state == "BLOCKED"
                    and "no question exposed" in planned.get(core, {}).get("reason", "")
                    and core in selected):
                findings.append({
                    "point": "PLAN_FALSE_EXPOSURE_BLOCK",
                    "bucket": bucket_id,
                    "core": core,
                    "detail": "resolve_request says no question is exposed but compile_bucket selects the core",
                })

        rows.append({
            "bucket": bucket_id,
            "matrix": str(path.relative_to(repo)),
            "questions": len(questions),
            "coverage": coverage,
            "exposed": exposed,
            "planner": {
                core: {
                    "state": planned.get(core, {}).get("state"),
                    "reason": planned.get(core, {}).get("reason"),
                }
                for core in PRACTICE
            },
            "compiler_selected": sorted(core for core in selected if core in PRACTICE),
            **({"compiler_error": compiler_error} if compiler_error else {}),
        })

    return {
        "subject": subject,
        "buckets": rows,
        "findings": findings,
        "passed": not findings,
    }


def audit_all(repo: Path = REPO) -> dict:
    subjects = sorted({
        path.parent.parent.name
        for path in repo.glob("*/matrices/*.rungs.json")
        if (path.parent.parent / "library").is_dir()
    })
    reports = [audit(subject, repo) for subject in subjects]
    findings = [
        {**finding, "subject": report["subject"]}
        for report in reports
        for finding in report["findings"]
    ]
    return {
        "subjects": reports,
        "findings": findings,
        "passed": not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--subject")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    report = audit(args.subject) if args.subject else audit_all()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
