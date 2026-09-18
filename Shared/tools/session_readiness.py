#!/usr/bin/env python3
"""Audit whether a subject matrix can support an actual self-study session.

This is intentionally a small readiness view over contracts that already exist. It does
not create another curriculum model, mastery score, or review lifecycle.

A matrix is SESSION_READY when every rung has:
- a canonical capability and microtopic;
- a non-empty teaching path;
- a Core1A and Core1B teaching route;
- misconception diagnosis + repair;
- a fresh verification path (microtopic exit task or same-capability question);
- prerequisite closure that is either locally/upstream taught or explicitly bridged.

Explicit external providers do not make the matrix fail. They produce
SESSION_READY_WITH_BRIDGE and remain visible to the parent/learner.

PILOT_READY means the topology/teaching/verification path is usable but some self-study
support is incomplete (for example a missing misconception diagnostic or Core1B route).
NOT_READY is reserved for blockers that make the route structurally unusable.
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

from Shared.contracts import load  # noqa: E402
from Shared.tools import capability_graph, study_map  # noqa: E402

READY = "SESSION_READY"
READY_WITH_BRIDGE = "SESSION_READY_WITH_BRIDGE"
PILOT_READY = "PILOT_READY"
NOT_READY = "NOT_READY"

BLOCKING_POINTS = {
    "READINESS_MICROTOPIC_MISSING",
    "READINESS_CAPABILITY_MISSING",
    "READINESS_TEACHING_PATH_MISSING",
    "READINESS_VERIFICATION_MISSING",
    "READINESS_PREREQUISITE_UNKNOWN",
    "READINESS_PREREQUISITE_UNTAUGHT",
}

SUPPORT_POINTS = {
    "READINESS_DIAGNOSTIC_REPAIR_INCOMPLETE",
    "READINESS_CORE1A_ROUTE_MISSING",
    "READINESS_CORE1B_ROUTE_MISSING",
}

ACADEMIC_POINTS = {
    "READINESS_ACADEMIC_REVIEW_PENDING",
    "READINESS_SOURCE_QUESTION_COVERAGE_ABSENT",
    "READINESS_PRACTICE_THIN",
}


def _subject_records(subject: str, repo: Path = REPO) -> dict:
    capabilities, microtopics = capability_graph.subject_graph(subject, repo)
    questions: list[dict] = []
    routes: list[dict] = []
    for path in sorted((repo / subject / "library").glob("*.json")):
        package = load(path)
        questions.extend(package.get("questions", []))
        routes.extend(package.get("teaching_routes", []))
    return {
        "capabilities": capabilities,
        "microtopics": microtopics,
        "questions": questions,
        "teaching_routes": routes,
        "locations": study_map.capability_locations(subject, repo),
    }


def _matrices(subject: str, repo: Path = REPO) -> list[tuple[Path, dict]]:
    root = repo / subject / "matrices"
    if not root.is_dir():
        return []
    return [(path, load(path)) for path in sorted(root.glob("*.rungs.json"))]


def _find_matrix(subject: str, matrix_id: str | None = None,
                 bucket_id: str | None = None, subtopic: str | None = None,
                 repo: Path = REPO) -> tuple[Path, dict] | None:
    matches = []
    for path, matrix in _matrices(subject, repo):
        if matrix_id and matrix.get("matrix_id") != matrix_id:
            continue
        if bucket_id and matrix.get("bucket_id") != bucket_id:
            continue
        if subtopic and matrix.get("subtopic", "").casefold() != subtopic.casefold():
            continue
        matches.append((path, matrix))
    if len(matches) == 1:
        return matches[0]
    return None


def _route_coverage(routes: list[dict]) -> dict[str, set[str]]:
    """microtopic -> cores that an existing teaching route can build."""
    result: dict[str, set[str]] = defaultdict(set)
    for route in routes:
        cores = set(route.get("cores", []))
        for mic in route.get("microtopic_refs", []):
            result[mic].update(cores)
    return result


def _question_coverage(questions: list[dict]) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    primary: dict[str, list[dict]] = defaultdict(list)
    secondary: dict[str, list[dict]] = defaultdict(list)
    for question in questions:
        cap = question.get("primary_capability_ref")
        if cap:
            primary[cap].append(question)
        for ref in question.get("secondary_capability_refs", []):
            secondary[ref].append(question)
    return primary, secondary


def _misconception_support(microtopic: dict) -> tuple[bool, int]:
    misconceptions = list(microtopic.get("misconceptions", []))
    if not misconceptions:
        return False, 0
    complete = all(
        bool(row.get("wrong_idea"))
        and bool(row.get("diagnostic_prompt"))
        and bool(row.get("repair"))
        for row in misconceptions
    )
    return complete, len(misconceptions)


def _elicitation_complete(microtopic: dict) -> bool:
    elicitation = microtopic.get("elicitation") or {}
    return all(
        elicitation.get(name)
        for name in ("predict", "attempt", "reconstruct", "boundary_test")
    )


def _source_question(question: dict) -> bool:
    """Conservative signal: only an explicit source-origin marker counts as custody."""
    return any(
        question.get(field) == "SOURCE"
        for field in ("origin", "source_basis", "provenance")
    )


def audit_matrix(subject: str, matrix: dict, repo: Path = REPO) -> dict:
    records = _subject_records(subject, repo)
    caps = records["capabilities"]
    mics = records["microtopics"]
    routes = _route_coverage(records["teaching_routes"])
    primary_q, secondary_q = _question_coverage(records["questions"])
    locations = records["locations"]

    findings: list[dict] = []
    rungs: list[dict] = []
    owned_capabilities: list[str] = []

    def finding(point: str, where: str, detail: str, **extra) -> None:
        findings.append({"point": point, "where": where, "detail": detail, **extra})

    for row in matrix.get("rungs", []):
        rung = row.get("rung")
        mic_ref = row.get("microtopic_ref")
        mic = mics.get(mic_ref) if mic_ref else None
        if mic is None:
            finding(
                "READINESS_MICROTOPIC_MISSING",
                str(rung),
                f"{mic_ref or 'no microtopic_ref'} does not resolve to a canonical microtopic",
            )
            rungs.append({
                "rung": rung,
                "ladder_position": row.get("ladder_position"),
                "microtopic_ref": mic_ref,
                "capability_ref": None,
                "teaching": False,
                "core1a": False,
                "core1b": False,
                "diagnostic_repair": False,
                "verification": False,
                "practice_questions": 0,
                "state": "BLOCKED",
            })
            continue

        capability = mic.get("primary_capability_ref")
        cap = caps.get(capability)
        if cap is None:
            finding(
                "READINESS_CAPABILITY_MISSING",
                str(rung),
                f"{capability or 'no primary capability'} does not resolve",
            )

        if capability and capability not in owned_capabilities:
            owned_capabilities.append(capability)

        teaching = bool(mic.get("teaching_path"))
        if not teaching:
            finding(
                "READINESS_TEACHING_PATH_MISSING",
                str(rung),
                f"{mic_ref} has no teaching_path",
                capability=capability,
            )

        core1a = "CORE1A" in routes.get(mic_ref, set())
        core1b = "CORE1B" in routes.get(mic_ref, set())
        if not core1a:
            finding(
                "READINESS_CORE1A_ROUTE_MISSING",
                str(rung),
                f"{mic_ref} is not covered by a Core1A teaching route",
                capability=capability,
            )
        if not core1b or not _elicitation_complete(mic):
            finding(
                "READINESS_CORE1B_ROUTE_MISSING",
                str(rung),
                f"{mic_ref} lacks full Core1B route/elicitation coverage",
                capability=capability,
            )

        diagnostic_repair, misconception_count = _misconception_support(mic)
        if not diagnostic_repair:
            finding(
                "READINESS_DIAGNOSTIC_REPAIR_INCOMPLETE",
                str(rung),
                f"{mic_ref} has no complete misconception -> diagnostic -> repair path",
                capability=capability,
            )

        practice = list(primary_q.get(capability, []))
        verification = bool(mic.get("exit_task")) or bool(practice)
        if not verification:
            finding(
                "READINESS_VERIFICATION_MISSING",
                str(rung),
                f"{mic_ref} has neither exit_task nor same-capability question",
                capability=capability,
            )

        rungs.append({
            "rung": rung,
            "ladder_position": row.get("ladder_position"),
            "microtopic_ref": mic_ref,
            "capability_ref": capability,
            "teaching": teaching,
            "core1a": core1a,
            "core1b": core1b and _elicitation_complete(mic),
            "diagnostic_repair": diagnostic_repair,
            "misconception_count": misconception_count,
            "verification": verification,
            "exit_task": bool(mic.get("exit_task")),
            "practice_questions": len(practice),
            "state": "READY" if (
                cap is not None
                and teaching
                and core1a
                and core1b
                and _elicitation_complete(mic)
                and diagnostic_repair
                and verification
            ) else "NEEDS_SUPPORT",
        })

    unknown_prereqs = capability_graph.unknown_prerequisites(owned_capabilities, caps)
    for prerequisite in unknown_prereqs:
        finding(
            "READINESS_PREREQUISITE_UNKNOWN",
            prerequisite,
            "prerequisite ref is not declared by the subject",
            capability=prerequisite,
        )

    prerequisite_refs = []
    for capability in owned_capabilities:
        for prerequisite in capability_graph.prerequisite_closure(capability, caps):
            if prerequisite not in prerequisite_refs and prerequisite not in owned_capabilities:
                prerequisite_refs.append(prerequisite)

    bridges = []
    upstream = []
    unresolved = []
    for prerequisite in prerequisite_refs:
        cap = caps.get(prerequisite)
        if cap is None:
            continue
        locs = locations.get(prerequisite, [])
        if locs:
            upstream.append({
                "capability_ref": prerequisite,
                "locations": locs,
            })
            continue
        provider = cap.get("external_provider")
        if provider:
            bridges.append({
                "capability_ref": prerequisite,
                "external_provider": provider,
                "acceptance_status": cap.get("acceptance_status"),
            })
            continue
        unresolved.append(prerequisite)
        finding(
            "READINESS_PREREQUISITE_UNTAUGHT",
            prerequisite,
            "prerequisite has no teaching location and no declared external provider",
            capability=prerequisite,
        )

    # Academic/source warnings stay visible but do not block a private family pilot.
    candidate_records = []
    for capability in owned_capabilities:
        cap = caps.get(capability)
        if cap and cap.get("status") not in {None, "CURATED", "REVIEWED"}:
            candidate_records.append(capability)
    for row in rungs:
        mic = mics.get(row.get("microtopic_ref"))
        if mic and mic.get("status") not in {None, "CURATED", "REVIEWED"}:
            candidate_records.append(mic["id"])
    if candidate_records:
        finding(
            "READINESS_ACADEMIC_REVIEW_PENDING",
            matrix.get("matrix_id", ""),
            "learner-facing records remain candidate/unpromoted",
            records=sorted(set(candidate_records)),
        )

    matrix_questions = [
        question
        for capability in owned_capabilities
        for question in primary_q.get(capability, [])
    ]
    source_questions = [q for q in matrix_questions if _source_question(q)]
    if not source_questions:
        finding(
            "READINESS_SOURCE_QUESTION_COVERAGE_ABSENT",
            matrix.get("matrix_id", ""),
            "no source-custody question is primarily owned by this matrix; authored/exit-task "
            "verification may still support a private pilot",
        )

    caps_without_primary_practice = [
        capability for capability in owned_capabilities
        if not primary_q.get(capability)
    ]
    if caps_without_primary_practice:
        finding(
            "READINESS_PRACTICE_THIN",
            matrix.get("matrix_id", ""),
            "some capabilities rely on exit tasks rather than canonical primary practice questions",
            capabilities=caps_without_primary_practice,
        )

    blocking = [row for row in findings if row["point"] in BLOCKING_POINTS]
    support = [row for row in findings if row["point"] in SUPPORT_POINTS]
    academic = [row for row in findings if row["point"] in ACADEMIC_POINTS]

    if blocking:
        status = NOT_READY
    elif support:
        status = PILOT_READY
    elif bridges:
        status = READY_WITH_BRIDGE
    else:
        status = READY

    return {
        "subject": subject,
        "matrix_id": matrix.get("matrix_id"),
        "bucket_id": matrix.get("bucket_id"),
        "topic": matrix.get("topic"),
        "subtopic": matrix.get("subtopic"),
        "status": status,
        "rungs": rungs,
        "owned_capabilities": owned_capabilities,
        "upstream_prerequisites": upstream,
        "external_bridges": bridges,
        "unresolved_prerequisites": unresolved,
        "practice": {
            "primary_question_count": len(matrix_questions),
            "source_question_count": len(source_questions),
            "capabilities_without_primary_question": caps_without_primary_practice,
            "secondary_question_uses": {
                capability: len(secondary_q.get(capability, []))
                for capability in owned_capabilities
                if secondary_q.get(capability)
            },
        },
        "findings": findings,
        "blocking_findings": blocking,
        "support_findings": support,
        "academic_warnings": academic,
        "passed": status != NOT_READY,
        "rule": (
            "Readiness is about executable self-study support. Academic review/source "
            "warnings remain visible but do not by themselves block a private pilot."
        ),
    }


def audit(subject: str, matrix_id: str | None = None, bucket_id: str | None = None,
          subtopic: str | None = None, repo: Path = REPO) -> dict:
    selected = _find_matrix(subject, matrix_id, bucket_id, subtopic, repo)
    if selected is None:
        return {
            "subject": subject,
            "status": NOT_READY,
            "findings": [{
                "point": "READINESS_MATRIX_UNRESOLVED",
                "where": matrix_id or bucket_id or subtopic or subject,
                "detail": "matrix selector did not resolve exactly one matrix",
            }],
            "passed": False,
        }
    path, matrix = selected
    report = audit_matrix(subject, matrix, repo)
    report["matrix_path"] = str(path.relative_to(repo))
    return report


def audit_all(subject: str, repo: Path = REPO) -> dict:
    rows = []
    for path, matrix in _matrices(subject, repo):
        report = audit_matrix(subject, matrix, repo)
        report["matrix_path"] = str(path.relative_to(repo))
        rows.append(report)
    return {
        "subject": subject,
        "matrices": rows,
        "counts": {
            status: sum(1 for row in rows if row["status"] == status)
            for status in (READY, READY_WITH_BRIDGE, PILOT_READY, NOT_READY)
        },
        "passed": bool(rows),
    }


def readable(report: dict) -> str:
    if "matrices" in report:
        out = [f'# Session readiness -- {report["subject"]}', ""]
        for row in report["matrices"]:
            out.append(
                f'{row["status"]:27} {row.get("subtopic") or row.get("matrix_id")}'
            )
        out += ["", json.dumps(report["counts"], indent=2)]
        return "\n".join(out)

    out = [
        f'# Session readiness -- {report.get("subtopic") or report.get("matrix_id")}',
        "",
        f'  subject   {report.get("subject")}',
        f'  matrix    {report.get("matrix_id")}',
        f'  status    {report.get("status")}',
        "",
        "## Rungs",
        "",
    ]
    for row in report.get("rungs", []):
        out.append(
            f'  {row["rung"]:4} {row.get("capability_ref") or "-":28} '
            f'{row["state"]}'
        )
    if report.get("external_bridges"):
        out += ["", "## External bridges", ""]
        for bridge in report["external_bridges"]:
            out.append(
                f'  {bridge["capability_ref"]} -> {bridge["external_provider"]} '
                f'[{bridge.get("acceptance_status") or "UNSPECIFIED"}]'
            )
    if report.get("blocking_findings"):
        out += ["", "## Blockers", ""]
        for finding in report["blocking_findings"]:
            out.append(f'  {finding["point"]}: {finding["detail"]}')
    if report.get("support_findings"):
        out += ["", "## Self-study support gaps", ""]
        for finding in report["support_findings"]:
            out.append(f'  {finding["point"]}: {finding["detail"]}')
    if report.get("academic_warnings"):
        out += ["", "## Academic/source warnings", ""]
        for finding in report["academic_warnings"]:
            out.append(f'  {finding["point"]}: {finding["detail"]}')
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--subject", required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--matrix-id")
    group.add_argument("--bucket-id")
    group.add_argument("--subtopic")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--readable", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    if args.all:
        report = audit_all(args.subject)
    else:
        if not any((args.matrix_id, args.bucket_id, args.subtopic)):
            parser.error("choose --matrix-id, --bucket-id, --subtopic, or --all")
        report = audit(
            args.subject,
            matrix_id=args.matrix_id,
            bucket_id=args.bucket_id,
            subtopic=args.subtopic,
        )

    print(readable(report) if args.readable else json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report.get("passed", False) else 0


if __name__ == "__main__":
    raise SystemExit(main())
