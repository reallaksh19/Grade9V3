#!/usr/bin/env python3
"""Validate governed Graphical Cognitive Deconstruction Route activity contracts.

This guard validates structure, referential integrity and honest conformance claims.
It does not grant scientific or pedagogical approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parents[2]
SCHEMA = REPO / "Shared" / "library" / "explorer_design_contract.schema.json"
KIND = "GRAPHICAL_COGNITIVE_DECONSTRUCTION"
MANDATORY_SEQUENCE = [
    "CONTEXT",
    "PREDICT",
    "MANIPULATE",
    "OBSERVE",
    "CONTRADICT",
    "GRAPHICAL_DECONSTRUCTION",
    "MATHEMATICAL_RECONSTRUCTION",
    "INVARIANT_DISCOVERY",
    "BOUNDARY_STRESS",
    "SCAFFOLD_FADE",
    "FRESH_TRANSFER",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def packages(repo: Path = REPO):
    for path in sorted(repo.glob("*/library/*.json")):
        try:
            obj = load(path)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "resources" in obj and "capabilities" in obj:
            yield path, obj


def findings(repo: Path = REPO) -> list[dict]:
    schema = load(repo / "Shared" / "library" / "explorer_design_contract.schema.json")
    loaded = list(packages(repo))

    capability_ids = {
        cap["id"]
        for _, package in loaded
        for cap in package.get("capabilities", [])
        if isinstance(cap, dict) and cap.get("id")
    }
    step_ids = {
        step["id"]
        for _, package in loaded
        for micro in package.get("microtopics", [])
        for step in micro.get("teaching_path", [])
        if isinstance(step, dict) and step.get("id")
    }

    result: list[dict] = []
    seen_activity_ids: set[str] = set()

    def add(path: Path, resource_id: str, point: str, detail: str):
        result.append({
            "file": str(path.relative_to(repo)),
            "resource": resource_id,
            "point": point,
            "detail": detail,
        })

    for path, package in loaded:
        for resource in package.get("resources", []):
            if not isinstance(resource, dict):
                continue
            ext = resource.get("extensions", {}).get("topic_atlas", {})
            if ext.get("activity_kind") != KIND:
                continue

            rid = resource.get("id", "<missing-id>")
            if rid in seen_activity_ids:
                add(path, rid, "DUPLICATE_ACTIVITY_ID", "GCDR activity id is not unique")
            seen_activity_ids.add(rid)

            contract = ext.get("gcdr_contract")
            if contract is None:
                add(path, rid, "MISSING_CONTRACT",
                    "GRAPHICAL_COGNITIVE_DECONSTRUCTION activity requires gcdr_contract")
                continue

            try:
                jsonschema.validate(instance=contract, schema=schema)
            except jsonschema.ValidationError as exc:
                location = ".".join(str(p) for p in exc.absolute_path) or "<root>"
                add(path, rid, "SCHEMA_INVALID", f"{location}: {exc.message}")
                continue

            if (resource.get("role") or []).count("ACTIVITY") != 1:
                add(path, rid, "NOT_ACTIVITY", "GCDR resource must carry ACTIVITY exactly once")

            claims = resource.get("supports_claims", [])
            if not claims:
                add(path, rid, "NO_CAPABILITY_BINDING", "supports_claims must not be empty")
            for cap in claims:
                if cap not in capability_ids:
                    add(path, rid, "UNKNOWN_CAPABILITY", cap)

            refs = ext.get("teaching_step_refs", [])
            if not refs:
                add(path, rid, "NO_SEMANTIC_LEAF_BINDING",
                    "topic_atlas.teaching_step_refs must not be empty")
            for ref in refs:
                if ref not in step_ids:
                    add(path, rid, "UNKNOWN_TEACHING_STEP", ref)

            rejoin = contract["exit_evidence"]["rejoin_step_ref"]
            if rejoin not in refs:
                add(path, rid, "REJOIN_OUTSIDE_BINDING",
                    f"rejoin_step_ref {rejoin!r} must be one of teaching_step_refs")

            if contract["interaction_sequence"] != MANDATORY_SEQUENCE:
                add(path, rid, "SEQUENCE_DRIFT",
                    "interaction_sequence must use the canonical GCDR sequence in order")

            locator = resource.get("locator", "")
            if locator.startswith("public/") and not (repo / locator).is_file():
                add(path, rid, "MISSING_IMPLEMENTATION", locator)

            evidence = contract["implementation_evidence"]
            if contract["conformance_status"] == "CERTIFIED":
                missing = [name for name, present in evidence.items() if not present]
                if missing:
                    add(path, rid, "FALSE_CERTIFICATION",
                        "CERTIFIED requires every implementation_evidence flag true: "
                        + ", ".join(missing))

    return result


def audit(repo: Path = REPO) -> dict:
    rows = findings(repo)
    return {
        "schema": str(SCHEMA.relative_to(REPO)),
        "activity_kind": KIND,
        "findings": rows,
        "passed": not rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
