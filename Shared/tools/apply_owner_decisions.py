#!/usr/bin/env python3
"""Apply typed owner decisions to an authoring request and immediately re-plan it."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import digest, load  # noqa: E402
from Shared.tools import plan_request  # noqa: E402

SCHEMA = REPO / "Shared/library/owner-decisions.schema.json"


def _schema_findings(value: dict, repo: Path = REPO) -> list[dict]:
    try:
        import jsonschema
    except ModuleNotFoundError:
        return []
    validator = jsonschema.Draft202012Validator(load(repo / "Shared/library/owner-decisions.schema.json"))
    return [{
        "point": "OWNER_DECISIONS_STRUCTURE",
        "where": "/".join(str(part) for part in error.path),
        "detail": error.message,
    } for error in validator.iter_errors(value)]


def plan_digest(plan: dict) -> str:
    """Digest the planner result that defines which owner decisions are currently legal."""
    return digest(plan)


def template(request: dict, repo: Path = REPO) -> dict:
    plan = plan_request.plan(request, repo)
    return {
        "decision_id": f'DEC-{request.get("request_id", "UNNAMED")}',
        "version": "1.0.0",
        "request_id": request.get("request_id"),
        "request_digest": digest(request),
        "plan_digest": plan_digest(plan),
        "required_owner_inputs": plan.get("required_owner_inputs", []),
        "decisions": {},
    }


def _learner_value(value: dict) -> dict:
    kind = value["kind"]
    if kind == "profile_ref":
        return {"profile_ref": value["profile_ref"]}
    if kind == "owner_entry":
        return {"owner_entry": {
            "rung": value["rung"],
            "by": "owner",
            **({"instruction": value["instruction"]} if value.get("instruction") else {}),
        }}
    if kind == "owner_estimate":
        return {"owner_estimate": {
            "knowledge_percentage": value["knowledge_percentage"],
            "by": "owner",
            **({"instruction": value["instruction"]} if value.get("instruction") else {}),
        }}
    return {"unknown": {
        "by": "owner",
        **({"instruction": value["instruction"]} if value.get("instruction") else {}),
    }}


def apply(request: dict, decisions: dict, repo: Path = REPO) -> dict:
    found = _schema_findings(decisions, repo)

    def fail(point: str, where: str, detail: str) -> None:
        found.append({"point": point, "where": where, "detail": detail})

    current_plan = plan_request.plan(request, repo)
    if decisions.get("request_id") != request.get("request_id"):
        fail("OWNER_DECISIONS_REQUEST_ID_MISMATCH", decisions.get("request_id", ""),
             "decision artifact does not name this request")
    if decisions.get("request_digest") != digest(request):
        fail("OWNER_DECISIONS_REQUEST_STALE", request.get("request_id", ""),
             "request changed after these decisions were prepared")
    if decisions.get("plan_digest") != plan_digest(current_plan):
        fail("OWNER_DECISIONS_PLAN_STALE", request.get("request_id", ""),
             "planner output changed after these decisions were prepared")

    required = {row["id"]: row for row in current_plan.get("required_owner_inputs", [])}
    supplied = decisions.get("decisions", {})
    for decision_id in supplied:
        if decision_id not in required:
            fail("OWNER_DECISION_UNSOLICITED", decision_id,
                 "planner did not request this owner decision in the pinned plan")

    patched = copy.deepcopy(request)
    if found:
        return {
            "passed": False,
            "findings": found,
            "request_before": request,
            "request_after": None,
            "plan_before": current_plan,
            "plan_after": None,
        }

    for decision_id, value in supplied.items():
        if decision_id == "LEARNER_ENTRY":
            patched["learner"] = _learner_value(value)

        elif decision_id == "CORE2A_PURPOSE":
            patched.setdefault("practice", {}).setdefault("CORE2A", {})["purpose"] = value

        elif decision_id == "CORE2B_PURPOSE":
            patched.setdefault("practice", {}).setdefault("CORE2B", {})["purpose"] = value

        elif decision_id == "SOURCE_BASIS":
            patched["source_basis"] = list(value)
            patched.pop("source_receipt_ref", None)
            patched.pop("source_basis_drift_acknowledgement", None)
            patched.pop("supplemental_question_policy", None)

        elif decision_id == "SOURCE_BASIS_DRIFT_DECISION":
            action = value["action"]
            if action == "KEEP_SUPPLIED_DESPITE_DRIFT":
                patched["source_basis_drift_acknowledgement"] = action
            else:
                candidates = set(
                    ((current_plan.get("source") or {}).get("basis_assessment") or {})
                    .get("replacement_candidates") or []
                )
                replacement = list(value["replacement_source_basis"])
                if not replacement or any(locator not in candidates for locator in replacement):
                    fail("OWNER_SOURCE_REPLACEMENT_NOT_OFFERED",
                         ",".join(replacement),
                         "replacement source basis must be one of the planner's receipt-backed candidates")
                    continue
                patched["source_basis"] = replacement
                patched.pop("source_receipt_ref", None)
                patched.pop("source_basis_drift_acknowledgement", None)
                # A policy chosen against the old source gap is stale after replacement.
                patched.pop("supplemental_question_policy", None)

        elif decision_id == "SUPPLEMENTAL_QUESTION_POLICY":
            patched["supplemental_question_policy"] = value

    if found:
        return {
            "passed": False,
            "findings": found,
            "request_before": request,
            "request_after": None,
            "plan_before": current_plan,
            "plan_after": None,
        }

    after = plan_request.plan(patched, repo)
    return {
        "passed": True,
        "findings": [],
        "decision_id": decisions.get("decision_id"),
        "request_id": request.get("request_id"),
        "request_digest_before": digest(request),
        "request_digest_after": digest(patched),
        "plan_digest_before": plan_digest(current_plan),
        "plan_digest_after": plan_digest(after),
        "applied_decisions": sorted(supplied),
        "request_after": patched,
        "plan_after": after,
        "remaining_owner_inputs": [row["id"] for row in after.get("required_owner_inputs", [])],
        "agent_actions": [row["id"] for row in after.get("agent_actions", [])],
    }


def audit(repo: Path = REPO) -> dict:
    # The executable behavioral contract lives in tests; audit validates decision fixtures if present.
    rows, findings = [], []
    root = repo / "Requests/decisions"
    if root.is_dir():
        for path in sorted(root.glob("*.json")):
            artifact = load(path)
            request_path = repo / artifact.get("request_path", "")
            if not request_path.is_file():
                row = {"path": str(path.relative_to(repo)), "passed": False,
                       "findings": [{"point": "OWNER_DECISION_FIXTURE_REQUEST_MISSING",
                                     "where": artifact.get("request_path", ""),
                                     "detail": "decision fixture request_path does not exist"}]}
            else:
                payload = {k: v for k, v in artifact.items() if k != "request_path"}
                report = apply(load(request_path), payload, repo)
                row = {"path": str(path.relative_to(repo)), **report}
            rows.append(row)
            findings.extend(row.get("findings", []))
    return {"fixtures": len(rows), "rows": rows, "findings": findings, "passed": not findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--request", type=Path)
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    if args.audit:
        report = audit()
    elif args.template:
        if not args.request:
            parser.error("--template requires --request")
        report = template(load(args.request))
    else:
        if not args.request or not args.decisions:
            parser.error("apply requires --request and --decisions")
        report = apply(load(args.request), load(args.decisions))

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report.get("passed", True) else 0


if __name__ == "__main__":
    raise SystemExit(main())
