#!/usr/bin/env python3
"""Build a cross-matrix study route from worksheet capability demand.

This layer answers "what must be studied first?" It consumes the worksheet mapping from
study_map.py, closes canonical capability prerequisites, and orders the resulting slice by
prerequisite topology. It never compares ladder_position values across matrices.

Question-derived scope, syllabus scope and declared extension remain distinct so a
worksheet can never silently become a claim about the complete syllabus.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.tools import capability_graph, study_map  # noqa: E402

UNKNOWN_SYLLABUS_CAPABILITY = "STUDY_ROUTE_SYLLABUS_CAPABILITY_UNKNOWN"
UNKNOWN_EXTENSION_CAPABILITY = "STUDY_ROUTE_EXTENSION_CAPABILITY_UNKNOWN"
UNKNOWN_PREREQUISITE = "STUDY_ROUTE_PREREQUISITE_UNKNOWN"
PREREQUISITE_CYCLE = "STUDY_ROUTE_PREREQUISITE_CYCLE"
NO_TEACHING_LOCATION = "STUDY_ROUTE_CAPABILITY_HAS_NO_TEACHING_LOCATION"
AMBIGUOUS_LOCATION = "STUDY_ROUTE_CAPABILITY_AMBIGUOUS_LOCATION"


def _stable_unique(values) -> list[str]:
    seen, out = set(), []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def question_demands(mapping: dict) -> tuple[list[str], dict[str, list[str]]]:
    """Capability demand in worksheet order, plus the questions requiring each one."""
    ordered = []
    required_by: dict[str, list[str]] = defaultdict(list)
    for question in mapping.get("questions", []):
        refs = [question.get("primary_capability_ref"), *question.get("secondary_capability_refs", [])]
        for ref in refs:
            if not ref:
                continue
            if ref not in required_by:
                ordered.append(ref)
            if question["question_id"] not in required_by[ref]:
                required_by[ref].append(question["question_id"])
    return ordered, dict(required_by)


def syllabus_demands(mapping: dict) -> tuple[list[str], dict[str, list[str]]]:
    """Optional syllabus overlay, preserving source refs without creating curriculum truth."""
    ordered, sources = [], defaultdict(list)
    for row in mapping.get("syllabus_capabilities", []):
        ref = row["capability_ref"]
        if ref not in sources:
            ordered.append(ref)
        source = row.get("source_ref")
        if source and source not in sources[ref]:
            sources[ref].append(source)
    return ordered, dict(sources)


def _scope(capability: str, question_refs: set[str], syllabus_refs: set[str],
           extension_refs: set[str], prerequisite_refs: set[str]) -> tuple[str, list[str]]:
    reasons = []
    if capability in question_refs:
        reasons.append("QUESTION_DEMAND")
    if capability in syllabus_refs:
        reasons.append("SYLLABUS_REQUIREMENT")
    if capability in extension_refs:
        reasons.append("DECLARED_EXTENSION")
    if capability in prerequisite_refs:
        reasons.append("PREREQUISITE")

    if capability in question_refs and capability in syllabus_refs:
        scope = "QUESTION_AND_SYLLABUS"
    elif capability in question_refs:
        scope = "QUESTION_ONLY"
    elif capability in syllabus_refs:
        scope = "SYLLABUS_ONLY"
    elif capability in extension_refs:
        scope = "DECLARED_EXTENSION"
    else:
        scope = "PREREQUISITE"
    return scope, reasons


def resolve(mapping: dict, repo: Path = REPO) -> dict:
    """Resolve worksheet/syllabus demand to an ordered canonical capability slice."""
    mapped = study_map.resolve(mapping, repo)
    structural = [f for f in mapped["findings"] if f["point"] == "WORKSHEET_MAP_STRUCTURE"]
    if structural:
        return {
            "worksheet_id": mapping.get("worksheet_id"),
            "subject": mapping.get("subject"),
            "route": [],
            "findings": structural,
            "passed": False,
        }

    subject = mapping["subject"]
    index = study_map.subject_index(subject, repo)
    caps = index["capabilities"]
    q_order, required_by = question_demands(mapping)
    s_order, syllabus_sources = syllabus_demands(mapping)
    e_order = _stable_unique(mapping.get("declared_extension_capabilities", []))

    findings = list(mapped["findings"])
    for ref in s_order:
        if ref not in caps:
            findings.append({
                "point": UNKNOWN_SYLLABUS_CAPABILITY,
                "capability": ref,
                "detail": "syllabus overlay names no canonical capability in this subject",
            })
    for ref in e_order:
        if ref not in caps:
            findings.append({
                "point": UNKNOWN_EXTENSION_CAPABILITY,
                "capability": ref,
                "detail": "declared extension names no canonical capability in this subject",
            })

    roots = _stable_unique([*q_order, *s_order, *e_order])
    known_roots = [ref for ref in roots if ref in caps]

    for ref in capability_graph.unknown_prerequisites(known_roots, caps):
        findings.append({
            "point": UNKNOWN_PREREQUISITE,
            "capability": ref,
            "detail": "a requested capability depends on a prerequisite not declared by the subject",
        })

    try:
        ordered = capability_graph.topological_subset(known_roots, caps)
        prerequisites = {
            prerequisite
            for root in known_roots
            for prerequisite in capability_graph.prerequisite_closure(root, caps)
        }
    except ContractError as exc:
        if exc.code != "CAPABILITY_PREREQUISITE_CYCLE":
            raise
        findings.append({
            "point": PREREQUISITE_CYCLE,
            "capability": exc.detail,
            "detail": "the requested capability slice contains a prerequisite cycle",
        })
        ordered, prerequisites = [], set()

    q_set, s_set, e_set = set(q_order), set(s_order), set(e_order)
    route = []
    for capability in ordered:
        locations = list(index["locations"].get(capability, []))
        if not locations:
            state = "NO_TEACHING_LOCATION"
            findings.append({
                "point": NO_TEACHING_LOCATION,
                "capability": capability,
                "detail": "canonical capability exists but no matrix/rung currently teaches it",
            })
        elif len({row["matrix_id"] for row in locations}) > 1:
            state = "AMBIGUOUS_LOCATION"
            findings.append({
                "point": AMBIGUOUS_LOCATION,
                "capability": capability,
                "detail": "canonical capability resolves to more than one matrix",
                "locations": locations,
            })
        else:
            state = "RESOLVED"

        scope, reasons = _scope(capability, q_set, s_set, e_set, prerequisites)
        route.append({
            "order": len(route) + 1,
            "capability_ref": capability,
            "scope": scope,
            "reasons": reasons,
            "required_by_questions": required_by.get(capability, []),
            "syllabus_source_refs": syllabus_sources.get(capability, []),
            "depends_on": [
                ref for ref in caps[capability].get("prerequisite_refs", [])
                if ref in caps
            ],
            "locations": locations,
            "state": state,
        })

    return {
        "worksheet_id": mapping["worksheet_id"],
        "subject": subject,
        "question_capabilities": q_order,
        "syllabus_capabilities": s_order,
        "declared_extension_capabilities": e_order,
        "route": route,
        "findings": findings,
        "passed": not findings,
        "ordering_rule": (
            "Cross-matrix order is derived only from capability.prerequisite_refs; "
            "ladder_position is never compared across matrices."
        ),
        "scope_rule": (
            "Question demand, syllabus requirement, prerequisite closure and declared "
            "extension remain separately labelled."
        ),
    }


def readable(report: dict) -> str:
    out = [
        f'# Study route -- {report.get("worksheet_id")}',
        "",
        f'  subject  {report.get("subject")}',
        "",
    ]
    for row in report.get("route", []):
        why = ", ".join(row["reasons"])
        out += [
            f'{row["order"]:>2}. {row["capability_ref"]} [{row["scope"]}] -- {row["state"]}',
            f'    why: {why}',
        ]
        if row["required_by_questions"]:
            out += [f'    questions: {", ".join(row["required_by_questions"])}']
        for loc in row["locations"]:
            out += [
                f'    teaches: {loc["matrix_id"]} / {loc["rung"]} '
                f'({loc["microtopic_ref"]})'
            ]
        out += [""]
    if report.get("findings"):
        out += ["## Findings", ""]
        for finding in report["findings"]:
            out += [
                f'  {finding["point"]:48} {finding.get("capability", "")}'
            ]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--readable", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    report = resolve(load(args.map))
    print(readable(report) if args.readable
          else json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
