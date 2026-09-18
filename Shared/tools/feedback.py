#!/usr/bin/env python3
"""Progressive self-study feedback over existing question and microtopic records.

This module deliberately does not pretend to be a universal grader. The caller supplies
an evaluated outcome (CORRECT / INCORRECT / UNDECIDABLE) and, when known, the failed
capability or misconception. This module owns the safer next-step policy:

  independent attempt -> small hint -> retry -> repair -> fresh verification

It never emits an ANSWER-revealing hint, never guesses which capability failed when a
multi-capability question is ambiguous, and never writes learner state silently. Instead
it returns an observation draft that the caller may persist explicitly.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.library.resolve import build_index, load_packages  # noqa: E402

RESULTS = {"CORRECT", "INCORRECT", "UNDECIDABLE"}
ERROR_STAGES = {"CONCEPT", "SETUP", "EXECUTION", "CARELESS", "UNKNOWN"}
HELP_LEVELS = {"NONE", "HINT", "WORKED_EXAMPLE", "SOLUTION", "UNKNOWN"}
INDEPENDENT_HELP = {"NONE"}


def subject_records(subject: str, repo: Path = REPO) -> dict:
    paths = sorted((repo / subject / "library").glob("*.json"))
    return build_index(load_packages(paths))


def question_record(records: dict, question_ref: str) -> dict | None:
    record = records.get(question_ref)
    if record and record.get("_collection") == "questions":
        return record
    return None


def required_capabilities(question: dict) -> list[str]:
    return [
        question["primary_capability_ref"],
        *list(question.get("secondary_capability_refs") or []),
    ]


def microtopics_for_capability(records: dict, capability_ref: str) -> list[dict]:
    rows = [
        record for record in records.values()
        if record.get("_collection") == "microtopics"
        and record.get("primary_capability_ref") == capability_ref
    ]
    return sorted(rows, key=lambda row: row["id"])


def diagnostic_options(records: dict, capability_refs: list[str]) -> list[dict]:
    """Concrete prompts a caller may use to distinguish an ambiguous failure."""
    options = []
    for capability in capability_refs:
        for microtopic in microtopics_for_capability(records, capability):
            prompts = [
                {
                    "index": index,
                    "wrong_idea": misconception["wrong_idea"],
                    "diagnostic_prompt": misconception["diagnostic_prompt"],
                }
                for index, misconception in enumerate(microtopic.get("misconceptions", []))
            ]
            options.append({
                "capability_ref": capability,
                "microtopic_ref": microtopic["id"],
                "title": microtopic.get("title"),
                "diagnostics": prompts,
            })
    return options


def _step_repair(records: dict, repair_ref: str) -> dict | None:
    for microtopic in (
        record for record in records.values()
        if record.get("_collection") == "microtopics"
    ):
        for step in microtopic.get("teaching_path", []):
            if step.get("id") == repair_ref:
                return {
                    "kind": "TEACHING_STEP",
                    "repair_ref": repair_ref,
                    "microtopic_ref": microtopic["id"],
                    "action": step.get("action"),
                    "why_valid": step.get("why_valid"),
                    "route": "CORE1B_THEN_CORE1A",
                }
    return None


def repair_for(records: dict, question: dict, failed_capability_ref: str | None,
               misconception_index: int | None = None) -> dict | None:
    """Resolve the narrowest repair already present in canonical content."""
    repair_ref = question.get("repair_ref")
    if repair_ref:
        exact = _step_repair(records, repair_ref)
        if exact:
            return exact

    if not failed_capability_ref:
        return None

    microtopics = microtopics_for_capability(records, failed_capability_ref)
    if len(microtopics) != 1:
        return None

    microtopic = microtopics[0]
    misconceptions = list(microtopic.get("misconceptions", []))
    if misconception_index is not None:
        if 0 <= misconception_index < len(misconceptions):
            misconception = misconceptions[misconception_index]
            return {
                "kind": "MISCONCEPTION_REPAIR",
                "microtopic_ref": microtopic["id"],
                "misconception_index": misconception_index,
                "wrong_idea": misconception["wrong_idea"],
                "diagnostic_prompt": misconception["diagnostic_prompt"],
                "repair": misconception["repair"],
                "route": "CORE1B_THEN_CORE1A",
            }
        return None

    return {
        "kind": "MICROTOPIC_REPAIR",
        "microtopic_ref": microtopic["id"],
        "title": microtopic.get("title"),
        "diagnostic_prompts": [
            row["diagnostic_prompt"] for row in misconceptions
        ],
        "route": "CORE1B_THEN_CORE1A",
    }


def next_safe_hint(question: dict, shown_hint_indices: list[int]) -> dict | None:
    """Return the next non-answer hint that preserves the intended decision demand."""
    shown = set(shown_hint_indices)
    transfer = question.get("transfer") or {}
    model_choice_transfer = transfer.get("dimension") == "model_choice"

    for index, hint in enumerate(question.get("hints", [])):
        if index in shown:
            continue
        reveals = hint.get("reveals")
        if reveals == "ANSWER":
            continue
        if model_choice_transfer and reveals != "CONCEPT":
            # In a model-choice transfer task, a METHOD hint can hand over the very
            # decision the task is supposed to assess.
            continue
        return {"index": index, **hint}
    return None


def verification_candidate(records: dict, question: dict,
                           attempted_question_refs: list[str]) -> dict | None:
    """Prefer a fresh same-capability question; otherwise use the microtopic exit task."""
    attempted = set(attempted_question_refs) | {question["id"]}
    primary = question["primary_capability_ref"]
    alternatives = sorted(
        (
            record for record in records.values()
            if record.get("_collection") == "questions"
            and record.get("primary_capability_ref") == primary
            and record.get("id") not in attempted
        ),
        key=lambda row: row["id"],
    )
    if alternatives:
        chosen = alternatives[0]
        return {
            "kind": "QUESTION",
            "question_ref": chosen["id"],
            "stem": chosen.get("stem"),
            "status": chosen.get("status"),
        }

    microtopics = microtopics_for_capability(records, primary)
    for microtopic in microtopics:
        exit_task = microtopic.get("exit_task")
        if exit_task:
            return {
                "kind": "EXIT_TASK",
                "verification_ref": f'{microtopic["id"]}:exit_task',
                "microtopic_ref": microtopic["id"],
                "prompt": exit_task.get("prompt"),
                "source_ref": exit_task.get("source_ref"),
                "status": microtopic.get("status"),
            }
    return None


def _effective_help(request: dict) -> str:
    declared = request.get("help_used", "NONE")
    if declared not in HELP_LEVELS:
        return "UNKNOWN"
    if request.get("shown_hint_indices") and declared == "NONE":
        return "HINT"
    return declared


def observation_draft(request: dict, question: dict,
                      failed_capability_ref: str | None) -> dict | None:
    """Draft one capability observation when the attempt supports a clear attribution."""
    when = request.get("when")
    if not when:
        return None
    evaluation = request["evaluation"]
    result = evaluation["result"]
    error_stage = evaluation.get("error_stage", "UNKNOWN")
    help_used = _effective_help(request)

    if result == "CORRECT":
        capability = question["primary_capability_ref"]
        state = "DEMONSTRATED" if help_used in INDEPENDENT_HELP else "UNCERTAIN"
    elif result == "INCORRECT" and failed_capability_ref:
        capability = failed_capability_ref
        state = "MISSING" if error_stage in {"CONCEPT", "SETUP"} else "UNCERTAIN"
    else:
        return None

    response = request.get("response_summary") or request.get("response") or result
    return {
        "observation_id": request.get("observation_id")
        or f'OBS-{question["id"]}-ATTEMPT-{request.get("attempt_number", 1)}',
        "capability_ref": capability,
        "method": f'question attempt {question["id"]}',
        "evidence_kind": "DIRECT_ATTEMPT",
        "question_ref": question["id"],
        **({"session_ref": request["session_ref"]} if request.get("session_ref") else {}),
        "observed": str(response),
        "result": state,
        "when": when,
        "help": help_used,
        "error_stage": error_stage,
    }


def run(request: dict, repo: Path = REPO) -> dict:
    """Return the next safe learner action and an optional observation draft."""
    subject = request.get("subject")
    question_ref = request.get("question_ref")
    evaluation = request.get("evaluation") or {}
    result = evaluation.get("result")
    findings = []

    if result not in RESULTS:
        return {
            "question_ref": question_ref,
            "next_action": "STOP",
            "findings": [{
                "point": "FEEDBACK_RESULT_INVALID",
                "detail": f"evaluation.result must be one of {', '.join(sorted(RESULTS))}",
            }],
            "passed": False,
        }

    if evaluation.get("error_stage", "UNKNOWN") not in ERROR_STAGES:
        findings.append({
            "point": "FEEDBACK_ERROR_STAGE_INVALID",
            "detail": "evaluation.error_stage is outside the small feedback vocabulary",
        })

    records = subject_records(subject, repo)
    question = question_record(records, question_ref)
    if question is None:
        return {
            "question_ref": question_ref,
            "next_action": "STOP",
            "findings": [{
                "point": "FEEDBACK_QUESTION_UNKNOWN",
                "detail": f"{question_ref} is not a canonical question in {subject}",
            }],
            "passed": False,
        }

    candidates = required_capabilities(question)
    failed = evaluation.get("failed_capability_ref")
    if failed and failed not in candidates:
        findings.append({
            "point": "FEEDBACK_FAILED_CAPABILITY_NOT_REQUIRED",
            "capability_ref": failed,
            "detail": "failed_capability_ref is not primary/secondary demand of this question",
        })
        failed = None
    if result == "INCORRECT" and not failed and len(candidates) == 1:
        failed = candidates[0]

    observation = observation_draft(request, question, failed)
    base = {
        "question_ref": question["id"],
        "result": result,
        "failed_capability_ref": failed,
        "candidate_capabilities": candidates,
        "observation_draft": observation,
        "findings": findings,
    }

    if result == "UNDECIDABLE":
        return {
            **base,
            "next_action": "DIAGNOSE",
            "diagnostic_options": diagnostic_options(records, candidates),
            "passed": not findings,
        }

    if result == "CORRECT":
        help_used = _effective_help(request)
        if help_used == "NONE":
            return {
                **base,
                "next_action": "CONTINUE",
                "passed": not findings,
            }
        verification = verification_candidate(
            records, question, request.get("attempted_question_refs", [])
        )
        return {
            **base,
            "next_action": "VERIFY" if verification else "VERIFICATION_ITEM_REQUIRED",
            "verification": verification,
            "passed": not findings,
        }

    # Incorrect multi-capability work must be diagnosed before routing a repair. Guessing
    # the failed capability would turn one wrong final answer into a false learner model.
    if not failed:
        return {
            **base,
            "next_action": "DIAGNOSE",
            "diagnostic_options": diagnostic_options(records, candidates),
            "passed": not findings,
        }

    attempt_number = max(1, int(request.get("attempt_number", 1)))
    if attempt_number <= 2:
        hint = next_safe_hint(question, request.get("shown_hint_indices", []))
        if hint is not None:
            return {
                **base,
                "next_action": "RETRY",
                "hint": hint,
                "passed": not findings,
            }

    repair = repair_for(
        records,
        question,
        failed,
        evaluation.get("misconception_index"),
    )
    if repair is None:
        return {
            **base,
            "next_action": "DIAGNOSE",
            "diagnostic_options": diagnostic_options(records, [failed]),
            "passed": not findings,
        }

    verification = verification_candidate(
        records, question, request.get("attempted_question_refs", [])
    )
    return {
        **base,
        "next_action": "REPAIR",
        "repair": repair,
        "after_repair": (
            {"next_action": "VERIFY", "verification": verification}
            if verification else {"next_action": "VERIFICATION_ITEM_REQUIRED"}
        ),
        "passed": not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    request = json.loads(args.input.read_text(encoding="utf-8"))
    report = run(request)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
