#!/usr/bin/env python3
"""Thin practical runner for one self-study worksheet session.

This file deliberately composes existing core contracts instead of inventing another
learning model:

    worksheet map
    -> session readiness
    -> learner-facing study plan
    -> attempt feedback
    -> observation draft + review date

It does not author curriculum, grade free-form work, mutate learner profiles, or persist
observations silently. The caller still supplies the evaluated attempt outcome.
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
from Shared.tools import (  # noqa: E402
    capability_delivery,
    feedback,
    session_readiness,
    worksheet_study_plan,
)

READY = session_readiness.READY
READY_WITH_BRIDGE = session_readiness.READY_WITH_BRIDGE
PILOT_READY = session_readiness.PILOT_READY
NOT_READY = session_readiness.NOT_READY


def _matrices(subject: str, repo: Path = REPO) -> list[dict]:
    root = repo / subject / "matrices"
    if not root.is_dir():
        return []
    return [load(path) for path in sorted(root.glob("*.rungs.json"))]


def resolve_estimates(subject: str, raw_values: list[str],
                      repo: Path = REPO) -> tuple[list[dict], list[dict]]:
    """Resolve human-friendly TARGET=PERCENT estimates to canonical matrix ids.

    TARGET may be an exact matrix id, bucket id, or subtopic name. Subtopic matching is
    case-insensitive but otherwise exact; fuzzy topic guessing would be unsafe here.
    """
    boards = _matrices(subject, repo)
    estimates: list[dict] = []
    findings: list[dict] = []

    for raw in raw_values:
        if "=" not in raw:
            findings.append({
                "point": "STUDY_SESSION_ESTIMATE_FORMAT",
                "detail": f"{raw!r} must be TARGET=PERCENT",
            })
            continue

        target, percent_text = raw.rsplit("=", 1)
        target = target.strip()
        try:
            percentage = float(percent_text.strip())
        except ValueError:
            findings.append({
                "point": "STUDY_SESSION_ESTIMATE_PERCENT_INVALID",
                "target": target,
                "detail": f"{percent_text!r} is not a number",
            })
            continue

        if percentage < 0 or percentage > 100:
            findings.append({
                "point": "STUDY_SESSION_ESTIMATE_PERCENT_OUT_OF_RANGE",
                "target": target,
                "detail": "percentage must be between 0 and 100",
            })
            continue

        matches = [
            board for board in boards
            if target == board.get("matrix_id")
            or target == board.get("bucket_id")
            or target.casefold() == str(board.get("subtopic") or "").casefold()
        ]
        if not matches:
            findings.append({
                "point": "STUDY_SESSION_ESTIMATE_TARGET_UNKNOWN",
                "target": target,
                "detail": "target does not match a matrix id, bucket id, or exact subtopic",
            })
            continue
        if len(matches) > 1:
            findings.append({
                "point": "STUDY_SESSION_ESTIMATE_TARGET_AMBIGUOUS",
                "target": target,
                "matrices": sorted(board["matrix_id"] for board in matches),
                "detail": "target matches more than one matrix; use matrix_id",
            })
            continue

        board = matches[0]
        estimates.append({
            "matrix_id": board["matrix_id"],
            "knowledge_percentage": percentage,
            "input_target": target,
        })

    return estimates, findings


def _touched_matrix_ids(study_plan: dict) -> list[str]:
    found = []
    for row in study_plan.get("route", []):
        for location in row.get("locations", []):
            matrix_id = location.get("matrix_id")
            if matrix_id and matrix_id not in found:
                found.append(matrix_id)
    return found


def _session_status(readiness_rows: list[dict], study_plan: dict) -> str:
    statuses = {row.get("status") for row in readiness_rows}
    if NOT_READY in statuses or not study_plan.get("valid", study_plan.get("passed", False)):
        return NOT_READY
    if PILOT_READY in statuses:
        return PILOT_READY
    if READY_WITH_BRIDGE in statuses or not study_plan.get("ready", True):
        return READY_WITH_BRIDGE
    return READY


def _next_step(study_plan: dict) -> dict | None:
    for row in study_plan.get("route", []):
        if row.get("recommended_action") == "SKIP":
            continue
        lessons = row.get("lessons", [])
        lesson = lessons[0] if lessons else None
        return {
            "order": row.get("order"),
            "action": row.get("recommended_action"),
            "capability_ref": row.get("capability_ref"),
            "lesson": lesson,
            "reason": row.get("action_reason"),
            "external_provider": row.get("external_provider"),
            "acceptance_status": row.get("acceptance_status"),
        }
    return None


def plan(mapping: dict, estimate_specs: list[str] | None = None,
         profile: dict | None = None, repo: Path = REPO) -> dict:
    """Compile a readiness-gated, learner-facing session plan."""
    subject = mapping.get("subject")
    estimates, estimate_findings = resolve_estimates(
        subject, estimate_specs or [], repo
    )
    study_plan = worksheet_study_plan.resolve(
        mapping,
        owner_estimates=estimates,
        profile=profile,
        repo=repo,
    )

    readiness_rows = [
        session_readiness.audit(subject, matrix_id=matrix_id, repo=repo)
        for matrix_id in _touched_matrix_ids(study_plan)
    ]
    status = _session_status(readiness_rows, study_plan)
    findings = [*estimate_findings, *study_plan.get("findings", [])]

    if status == NOT_READY and not any(
        row.get("point") == "STUDY_SESSION_TOPIC_NOT_READY"
        for row in findings
    ):
        blocked = [
            row.get("matrix_id")
            for row in readiness_rows
            if row.get("status") == NOT_READY
        ]
        findings.append({
            "point": "STUDY_SESSION_TOPIC_NOT_READY",
            "matrices": blocked,
            "detail": (
                "one or more required matrices are not self-study ready; keep the "
                "content gap explicit instead of fabricating a session"
            ),
        })

    academic_warnings = [
        {
            "matrix_id": row.get("matrix_id"),
            "subtopic": row.get("subtopic"),
            **warning,
        }
        for row in readiness_rows
        for warning in row.get("academic_warnings", [])
    ]

    valid = status != NOT_READY and not estimate_findings
    ready = (
        valid
        and status != PILOT_READY
        and study_plan.get("ready", True)
    )
    return {
        "worksheet_id": mapping.get("worksheet_id"),
        "subject": subject,
        "status": status,
        "valid": valid,
        "ready": ready,
        "profile_id": study_plan.get("profile_id"),
        "owner_estimates": estimates,
        "readiness": [{
            "matrix_id": row.get("matrix_id"),
            "subtopic": row.get("subtopic"),
            "status": row.get("status"),
            "external_bridges": row.get("external_bridges", []),
            "support_findings": row.get("support_findings", []),
        } for row in readiness_rows],
        "next_step": _next_step(study_plan) if status != NOT_READY else None,
        "questions": study_plan.get("questions", []),
        "route": study_plan.get("route", []),
        "academic_warnings": academic_warnings,
        "findings": findings,
        "blockers": list(study_plan.get("blockers", [])),
        "passed": valid,
        "rules": [
            "Readiness must be established before a subtopic is treated as self-study ready.",
            "Owner percentages choose a local starting attempt; they are not mastery evidence.",
            "Worksheet questions remain transient demand unless separately promoted.",
            "Attempt evaluation is supplied by the caller; the runner does not pretend to grade free-form work.",
            "Observation drafts are returned explicitly and are never persisted silently.",
        ],
    }


def _question_readiness(mapping: dict, question: dict, repo: Path) -> tuple[list[dict], list[dict]]:
    """Return readiness rows and blockers for matrices directly teaching one question."""
    subject = mapping.get("subject")
    mapped = [
        question.get("primary_capability_ref"),
        *list(question.get("secondary_capability_refs") or []),
    ]

    from Shared.tools import study_map  # local import avoids a wider public surface

    index = study_map.subject_index(subject, repo)
    matrix_ids = []
    blockers = []

    for capability in mapped:
        locations = list(index.get("locations", {}).get(capability, []))
        cap_record = index.get("capabilities", {}).get(capability, {})
        if not cap_record:
            blockers.append({
                "point": "STUDY_SESSION_QUESTION_CAPABILITY_UNKNOWN",
                "capability_ref": capability,
                "detail": "mapped question capability is not canonical in the selected subject",
            })
            continue

        delivery = capability_delivery.resolve(cap_record, locations)
        if delivery["state"] == capability_delivery.EXTERNAL_BRIDGE:
            blockers.append({
                "point": "STUDY_SESSION_QUESTION_EXTERNAL_ONLY",
                "capability_ref": capability,
                "external_provider": delivery["provider"],
                "detail": (
                    "this mapped question capability is an external bridge; "
                    "the local feedback runtime has no canonical repair lesson for it"
                ),
            })
            continue
        if delivery["state"] == capability_delivery.UNRESOLVED:
            blockers.append({
                "point": "STUDY_SESSION_QUESTION_DELIVERY_UNRESOLVED",
                "capability_ref": capability,
                "detail": "mapped question capability has no resolvable teaching delivery",
            })
            continue
        if delivery["state"] == capability_delivery.AMBIGUOUS:
            blockers.append({
                "point": "STUDY_SESSION_QUESTION_DELIVERY_AMBIGUOUS",
                "capability_ref": capability,
                "detail": "mapped question capability has more than one teaching location",
            })
            continue

        for location in delivery["locations"]:
            matrix_id = location.get("matrix_id")
            if matrix_id and matrix_id not in matrix_ids:
                matrix_ids.append(matrix_id)

    readiness_rows = [
        session_readiness.audit(subject, matrix_id=matrix_id, repo=repo)
        for matrix_id in matrix_ids
    ]
    for row in readiness_rows:
        if row.get("status") == NOT_READY:
            blockers.append({
                "point": "STUDY_SESSION_QUESTION_TOPIC_NOT_READY",
                "matrix_id": row.get("matrix_id"),
                "detail": "question feedback is blocked because its teaching matrix is not ready",
            })

    return readiness_rows, blockers


def attempt(mapping: dict, question_id: str, *, result: str,
            when: str, failed_capability_ref: str | None = None,
            error_stage: str = "UNKNOWN", help_used: str = "NONE",
            attempt_number: int = 1, shown_hint_indices: list[int] | None = None,
            attempted_question_refs: list[str] | None = None,
            misconception_index: int | None = None,
            response_summary: str | None = None,
            session_ref: str | None = None,
            repo: Path = REPO) -> dict:
    """Run feedback for one mapped worksheet question without persisting learner state."""
    question = next(
        (row for row in mapping.get("questions", []) if row.get("question_id") == question_id),
        None,
    )
    if question is None:
        return {
            "question_ref": question_id,
            "next_action": "STOP",
            "findings": [{
                "point": "STUDY_SESSION_QUESTION_NOT_IN_WORKSHEET",
                "detail": "question id is not present in the supplied worksheet map",
            }],
            "passed": False,
        }

    readiness_rows, blockers = _question_readiness(mapping, question, repo)
    if blockers:
        return {
            "question_ref": question_id,
            "next_action": "STOP",
            "readiness": readiness_rows,
            "findings": blockers,
            "passed": False,
        }

    evaluation = {
        "result": result,
        "error_stage": error_stage,
    }
    if failed_capability_ref:
        evaluation["failed_capability_ref"] = failed_capability_ref
    if misconception_index is not None:
        evaluation["misconception_index"] = misconception_index

    request = {
        "subject": mapping.get("subject"),
        "question_ref": question_id,
        "worksheet_question": question,
        "attempt_number": attempt_number,
        "shown_hint_indices": shown_hint_indices or [],
        "attempted_question_refs": attempted_question_refs or [question_id],
        "help_used": help_used,
        "when": when,
        "session_ref": session_ref or mapping.get("worksheet_id"),
        "evaluation": evaluation,
    }
    if response_summary:
        request["response_summary"] = response_summary

    report = feedback.run(request, repo)
    return {
        **report,
        "readiness": readiness_rows,
        "persistence": "NOT_WRITTEN",
    }


def _lesson_label(step: dict | None) -> str:
    if not step:
        return ""
    lesson = step.get("lesson") or {}
    if lesson:
        return lesson.get("microtopic_title") or lesson.get("label") or ""
    if step.get("external_provider"):
        return f'External bridge: {step["external_provider"]}'
    return ""


def readable_plan(report: dict) -> str:
    out = [
        f'# Study session — {report.get("worksheet_id")}',
        "",
        f'  subject: {report.get("subject")}',
        f'  status:  {report.get("status")}',
        "",
    ]

    if report.get("owner_estimates"):
        out += ["## Rough starting estimates", ""]
        for estimate in report["owner_estimates"]:
            out.append(
                f'- {estimate.get("input_target")}: '
                f'{estimate["knowledge_percentage"]:g}% -> {estimate["matrix_id"]}'
            )
        out += [""]

    out += ["## Subtopic readiness", ""]
    if not report.get("readiness"):
        out.append("- No local teaching matrix is required.")
    for row in report.get("readiness", []):
        out.append(
            f'- {row.get("subtopic") or row.get("matrix_id")}: {row.get("status")}'
        )
        for bridge in row.get("external_bridges", []):
            out.append(
                f'  - bridge: {bridge["capability_ref"]} -> '
                f'{bridge["external_provider"]}'
            )

    if report.get("next_step"):
        step = report["next_step"]
        out += ["", "## Start now", ""]
        out.append(
            f'1. {step.get("action")} — '
            f'{_lesson_label(step) or step.get("capability_ref")}'
        )
        if step.get("reason"):
            out.append(f'   {step["reason"]}')

    out += ["", "## Ordered study route", ""]
    for row in report.get("route", []):
        lessons = ", ".join(
            lesson.get("microtopic_title") or lesson.get("label") or ""
            for lesson in row.get("lessons", [])
        )
        if not lessons and row.get("recommended_action") == "BRIDGE":
            lessons = f'External bridge: {row.get("external_provider")}'
        out.append(
            f'{row.get("order", "-")}. {row.get("recommended_action")} — '
            f'{lessons or row.get("capability_ref")}'
        )

    out += ["", "## Worksheet questions", ""]
    for row in report.get("questions", []):
        out.append(
            f'- {row.get("question_id")}: {row.get("what_is_being_learned")} '
            f'[{row.get("learner_state")}]'
        )
        out.append(f'  {row.get("why_extra_attention")}')

    if report.get("academic_warnings"):
        out += ["", "## Parent warnings", ""]
        seen = set()
        for warning in report["academic_warnings"]:
            key = (warning.get("matrix_id"), warning.get("point"))
            if key in seen:
                continue
            seen.add(key)
            out.append(
                f'- {warning.get("subtopic") or warning.get("matrix_id")}: '
                f'{warning.get("detail")}'
            )

    if report.get("findings"):
        out += ["", "## Blocking/input findings", ""]
        for finding in report["findings"]:
            out.append(
                f'- {finding.get("point")}: {finding.get("detail", "")}'
            )
    return "\n".join(out)


def readable_attempt(report: dict) -> str:
    out = [
        f'# Attempt feedback — {report.get("question_ref")}',
        "",
        f'  next: {report.get("next_action")}',
        "",
    ]
    hint = report.get("hint")
    if hint:
        out += ["## Hint", "", hint.get("text", ""), ""]

    if report.get("diagnostic_options"):
        out += ["## Diagnose", ""]
        for option in report["diagnostic_options"]:
            for diagnostic in option.get("diagnostics", []):
                out.append(f'- {diagnostic.get("diagnostic_prompt")}')

    repair = report.get("repair")
    if repair:
        out += ["", "## Repair", ""]
        if repair.get("repair"):
            out.append(repair["repair"])
        elif repair.get("action"):
            out.append(repair["action"])
        elif repair.get("title"):
            out.append(f'Review: {repair["title"]}')

    after = report.get("after_repair") or {}
    verification = after.get("verification") or report.get("verification")
    if verification:
        out += ["", "## Fresh verification", ""]
        prompt = verification.get("stem") or verification.get("prompt")
        out.append(str(prompt or verification.get("question_ref") or verification.get("verification_ref")))

    observation = report.get("observation_draft")
    if observation:
        out += ["", "## Observation draft", ""]
        out.append(
            f'{observation.get("capability_ref")}: {observation.get("result")} '
            f'({observation.get("help")})'
        )

    review = report.get("review")
    if review:
        out += ["", f'Next review: {review.get("next_review")}']

    if report.get("findings"):
        out += ["", "## Findings", ""]
        for finding in report["findings"]:
            out.append(f'- {finding.get("point")}: {finding.get("detail", "")}')

    out += ["", "Learner state was not written automatically."]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="compile the start-of-session study plan")
    p_plan.add_argument("--map", type=Path, required=True)
    p_plan.add_argument("--profile", type=Path)
    p_plan.add_argument(
        "--estimate",
        action="append",
        default=[],
        metavar="TARGET=PERCENT",
        help="TARGET is matrix id, bucket id, or exact subtopic name; may repeat",
    )
    p_plan.add_argument("--readable", action="store_true")
    p_plan.add_argument("--enforce", action="store_true")

    p_attempt = sub.add_parser("attempt", help="run feedback for one mapped question")
    p_attempt.add_argument("--map", type=Path, required=True)
    p_attempt.add_argument("--question", required=True)
    p_attempt.add_argument("--result", choices=sorted(feedback.RESULTS), required=True)
    p_attempt.add_argument("--when", required=True, help="ISO date/timestamp")
    p_attempt.add_argument("--failed-capability")
    p_attempt.add_argument(
        "--error-stage", choices=sorted(feedback.ERROR_STAGES), default="UNKNOWN"
    )
    p_attempt.add_argument(
        "--help-used", choices=sorted(feedback.HELP_LEVELS), default="NONE"
    )
    p_attempt.add_argument("--attempt-number", type=int, default=1)
    p_attempt.add_argument("--shown-hint", action="append", type=int, default=[])
    p_attempt.add_argument("--attempted-question", action="append", default=[])
    p_attempt.add_argument("--misconception-index", type=int)
    p_attempt.add_argument("--response-summary")
    p_attempt.add_argument("--session-ref")
    p_attempt.add_argument("--readable", action="store_true")
    p_attempt.add_argument("--enforce", action="store_true")

    args = parser.parse_args()
    mapping = load(args.map)

    if args.command == "plan":
        profile = load(args.profile) if args.profile else None
        report = plan(mapping, args.estimate, profile)
        print(readable_plan(report) if args.readable
              else json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if args.enforce and not report["passed"] else 0

    report = attempt(
        mapping,
        args.question,
        result=args.result,
        when=args.when,
        failed_capability_ref=args.failed_capability,
        error_stage=args.error_stage,
        help_used=args.help_used,
        attempt_number=args.attempt_number,
        shown_hint_indices=args.shown_hint,
        attempted_question_refs=args.attempted_question,
        misconception_index=args.misconception_index,
        response_summary=args.response_summary,
        session_ref=args.session_ref,
    )
    print(readable_attempt(report) if args.readable
          else json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
