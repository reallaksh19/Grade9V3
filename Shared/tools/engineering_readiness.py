#!/usr/bin/env python3
"""Report whether matrix rungs have the engineering assets they declare upstream.

The matrix may name a relation, validator or representation dependency; it may not
declare that dependency satisfied. Authority comes from the subject's gate registries
and contract. Missing assets on SYNTHESIS/ABSENT rows are backlog, not build failures.
A SOURCE/AUTHORED row with the same missing dependency is a contradiction and fails.
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

AUTHORED = {"SOURCE", "AUTHORED"}


def subjects(repo: Path = REPO) -> list[Path]:
    return sorted(p.parent.parent for p in repo.glob("*/adapter/CoreContracts.json"))


def _assets(subject: Path) -> dict[str, dict[str, dict]]:
    contract = load(subject / "adapter/CoreContracts.json")
    validators = {row["id"]: row for row in contract.get("validator_catalogue", [])}
    representation_kinds = {row["id"]: row for row in contract.get("representation_kinds", [])}

    relations: dict[str, dict] = {}
    representations: dict[str, dict] = {}
    bindings = subject / "gates/curriculum-bindings.v1.json"
    for path in sorted((subject / "gates").glob("*.v1.json")):
        if path == bindings:
            continue
        registry = load(path)
        for gate in registry.get("gates", []):
            gate_state = gate.get("scope_state")
            gate_id = gate.get("gate_id")
            for relation in gate.get("relations", []):
                relations[relation["relation_id"]] = {
                    **relation, "_gate_id": gate_id, "_gate_state": gate_state,
                }
            for representation in gate.get("representations", []):
                representations[representation["representation_id"]] = {
                    **representation, "_gate_id": gate_id, "_gate_state": gate_state,
                }
    return {
        "GATE_RELATION": relations,
        "VALIDATOR": validators,
        "GATE_REPRESENTATION": representations,
        "REPRESENTATION_KIND": representation_kinds,
    }


def _dependency_state(dep: dict, assets: dict[str, dict[str, dict]]) -> tuple[str, str]:
    kind, ref = dep["kind"], dep["ref"]
    record = assets.get(kind, {}).get(ref)
    if record is None:
        return "MISSING", f"{kind} {ref} is not declared by this subject"

    if kind in {"GATE_RELATION", "GATE_REPRESENTATION"}:
        if record.get("_gate_state") != "ACTIVE":
            return "HELD", (
                f"{kind} {ref} is owned by {record.get('_gate_id')} "
                f"with scope_state {record.get('_gate_state')}"
            )
        return "READY", f"{kind} {ref} is active in {record.get('_gate_id')}"

    if kind == "VALIDATOR":
        status = record.get("status")
        if dep["required_for"] == "NUMERIC_EXIT" and status != "IMPLEMENTED":
            return "PROPOSED", f"validator {ref} has status {status}"
        return "READY", f"validator {ref} has status {status}"

    if kind == "REPRESENTATION_KIND":
        status = record.get("status")
        if dep["required_for"] == "LEARNER_REPRESENTATION" and status != "IMPLEMENTED":
            return "PROPOSED", f"representation kind {ref} has status {status}"
        return "READY", f"representation kind {ref} has status {status}"

    return "MISSING", f"unknown dependency kind {kind}"


def audit_subject(subject: Path) -> dict:
    assets = _assets(subject)
    rungs, blockers, findings = [], [], []

    for path in sorted((subject / "matrices").glob("*.rungs.json")):
        matrix = load(path)
        for rung in matrix.get("rungs", []):
            deps = rung.get("engineering_dependencies") or []
            if not deps:
                continue
            resolved = []
            for dep in deps:
                state, detail = _dependency_state(dep, assets)
                row = {**dep, "state": state, "detail": detail}
                resolved.append(row)
                if state != "READY":
                    blocker = {
                        "matrix": str(path.relative_to(subject.parent)),
                        "bucket": matrix["bucket_id"],
                        "rung": rung["rung"],
                        "provenance": rung["provenance"],
                        **row,
                    }
                    blockers.append(blocker)
                    if rung["provenance"] in AUTHORED:
                        findings.append({
                            "point": "AUTHORED_RUNG_ENGINEERING_DEPENDENCY_UNREADY",
                            **blocker,
                        })
            rungs.append({
                "matrix": str(path.relative_to(subject.parent)),
                "bucket": matrix["bucket_id"],
                "rung": rung["rung"],
                "provenance": rung["provenance"],
                "dependencies": resolved,
                "engineering_ready": all(d["state"] == "READY" for d in resolved),
            })

    return {
        "subject": subject.name,
        "rungs": rungs,
        "blockers": blockers,
        "findings": findings,
        "passed": not findings,
    }


def audit_all(repo: Path = REPO) -> dict:
    reports = [audit_subject(subject) for subject in subjects(repo)]
    findings = [
        {**finding, "subject": report["subject"]}
        for report in reports
        for finding in report["findings"]
    ]
    blockers = [
        {**blocker, "subject": report["subject"]}
        for report in reports
        for blocker in report["blockers"]
    ]
    return {
        "subjects": reports,
        "blockers": blockers,
        "findings": findings,
        "passed": bool(reports) and not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--subject")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    if args.subject:
        subject = REPO / args.subject
        report = audit_subject(subject)
    else:
        report = audit_all()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
