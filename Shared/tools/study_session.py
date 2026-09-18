#!/usr/bin/env python3
"""Run one thin self-study session against one readiness-audited matrix.

This is deliberately not an all-subject scheduler. It accepts one explicit matrix,
requires that matrix to be SESSION_READY or SESSION_READY_WITH_BRIDGE, and then exposes
only the next safe learner action from content that already exists.

The runner does not own curriculum truth, mastery state, answer evaluation or persistence.
It composes:
- session_readiness for the go/no-go gate;
- learner_evidence for current capability state;
- canonical microtopic teaching / reconstruction / exit tasks;
- feedback.py for attempt diagnosis, repair, verification and review scheduling.

A caller may therefore run one subtopic now without creating another learning architecture.
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
from Shared.tools import feedback, learner_evidence, session_readiness, study_map  # noqa: E402

STARTABLE = {
    session_readiness.READY,
    session_readiness.READY_WITH_BRIDGE,
}

SESSION_READY = "READY_TO_START"
SESSION_AWAITING_BRIDGE = "AWAITING_BRIDGE"
SESSION_IN_PROGRESS = "IN_PROGRESS"
SESSION_COMPLETE = "COMPLETE"
SESSION_STOPPED = "STOPPED"

LOCAL_ACTIONS = {
    "MISSING": "TEACH",
    "UNCERTAIN": "RECONSTRUCT",
    "UNOBSERVED": "ATTEMPT",
    "DEMONSTRATED": "QUICK_CHECK",
}


def _state(profile: dict | None, capability_ref: str, repo: Path) -> dict:
    if profile is None:
        return {
            "state": "UNOBSERVED",
            "source": "NO_PROFILE",
            "observation_ref": None,
            "when": None,
            "help": None,
        }
    return learner_evidence.effective_state(profile, capability_ref, repo)


def _readiness(subject: str, matrix_id: str, repo: Path) -> dict:
    return session_readiness.audit(subject, matrix_id=matrix_id, repo=repo)


def _index(subject: str, repo: Path) -> dict:
    return study_map.subject_index(subject, repo)


def _rung_rows(readiness: dict) -> list[dict]:
    return sorted(
        list(readiness.get("rungs", [])),
        key=lambda row: (
            int(row.get("ladder_position") or 0),
            str(row.get("rung") or ""),
        ),
    )


def _verification(microtopic: dict) -> dict | None:
    exit_task = microtopic.get("exit_task")
    if not exit_task:
        return None
    return {
        "kind": "EXIT_TASK",
        "question_ref": f'{microtopic["id"]}:exit_task',
        "microtopic_ref": microtopic["id"],
        "prompt": exit_task.get("prompt"),
        "source_ref": exit_task.get("source_ref"),
        "answer": exit_task.get("answer"),
        "status": microtopic.get("status"),
    }


def _local_action(
    rung: dict,
    microtopic: dict,
    learner_state: dict,
) -> dict:
    state = learner_state["state"]
    action = LOCAL_ACTIONS.get(state, "ATTEMPT")
    base = {
        "type": action,
        "rung": rung.get("rung"),
        "ladder_position": rung.get("ladder_position"),
        "capability_ref": rung.get("capability_ref"),
        "microtopic_ref": rung.get("microtopic_ref"),
        "title": microtopic.get("title"),
        "learner_state": learner_state,
        "verification": _verification(microtopic),
    }

    if action == "TEACH":
        return {
            **base,
            "teaching_path": list(microtopic.get("teaching_path", [])),
            "after": "ATTEMPT_EXIT_TASK",
            "reason": "Current learner evidence says MISSING.",
        }

    elicitation = microtopic.get("elicitation") or {}
    if action == "RECONSTRUCT":
        return {
            **base,
            "predict": elicitation.get("predict"),
            "attempt": elicitation.get("attempt"),
            "reconstruct": elicitation.get("reconstruct"),
            "boundary_test": elicitation.get("boundary_test"),
            "after": "ATTEMPT_EXIT_TASK",
            "reason": "Current learner evidence says UNCERTAIN.",
        }

    if action == "QUICK_CHECK":
        return {
            **base,
            "reason": (
                "Capability is already demonstrated; use the exit task as a brief "
                "independent confirmation before spending study time here."
            ),
        }

    return {
        **base,
        "reason": (
            "No learner evidence exists yet; attempt the exit task without help first "
            "and let the existing feedback loop decide whether teaching is needed."
        ),
    }


def _bridge_action(bridge: dict, profile: dict | None, repo: Path) -> dict:
    capability = bridge["capability_ref"]
    state = _state(profile, capability, repo)
    demonstrated = state["state"] == "DEMONSTRATED"
    return {
        "type": "SKIP" if demonstrated else "BRIDGE",
        "capability_ref": capability,
        "external_provider": bridge.get("external_provider"),
        "acceptance_status": bridge.get("acceptance_status"),
        "learner_state": state,
        "satisfied": demonstrated,
        "reason": (
            "Learner evidence already demonstrates this prerequisite; no provider detour "
            "is needed."
            if demonstrated
            else "Verify or repair this prerequisite through the declared provider before "
            "starting local study."
        ),
    }


def _session_rows(
    readiness: dict,
    index: dict,
    profile: dict | None,
    repo: Path,
) -> list[dict]:
    rows = []
    for rung in _rung_rows(readiness):
        microtopic_ref = rung.get("microtopic_ref")
        microtopic = index["microtopics"].get(microtopic_ref, {})
        capability = rung.get("capability_ref")
        rows.append({
            **rung,
            "learner_state": _state(profile, capability, repo),
            "entry_action": _local_action(
                rung,
                microtopic,
                _state(profile, capability, repo),
            ),
        })
    return rows


def start(
    subject: str,
    matrix_id: str,
    profile: dict | None = None,
    repo: Path = REPO,
) -> dict:
    """Return the first executable action for one explicitly selected matrix."""
    readiness = _readiness(subject, matrix_id, repo)
    status = readiness.get("status")
    if status not in STARTABLE:
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "readiness_status": status,
            "session_state": SESSION_STOPPED,
            "next_action": {
                "type": "STOP",
                "reason": "Selected matrix is not session-ready.",
            },
            "findings": [{
                "point": "STUDY_SESSION_MATRIX_NOT_READY",
                "detail": (
                    "study_session only starts matrices audited as SESSION_READY or "
                    "SESSION_READY_WITH_BRIDGE"
                ),
                "readiness_status": status,
            }],
            "readiness": readiness,
            "passed": False,
        }

    if profile is not None and profile.get("provenance") == "SYNTHETIC_TEST":
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "readiness_status": status,
            "session_state": SESSION_STOPPED,
            "next_action": {
                "type": "STOP",
                "reason": "Synthetic test profiles may not drive a real learner session.",
            },
            "findings": [{
                "point": "STUDY_SESSION_SYNTHETIC_PROFILE_REFUSED",
                "detail": "synthetic learner evidence is test-only",
            }],
            "readiness": readiness,
            "passed": False,
        }

    index = _index(subject, repo)
    bridges = [
        _bridge_action(row, profile, repo)
        for row in readiness.get("external_bridges", [])
    ]
    pending_bridges = [row for row in bridges if not row["satisfied"]]
    rungs = _session_rows(readiness, index, profile, repo)

    if pending_bridges:
        session_state = SESSION_AWAITING_BRIDGE
        next_action = pending_bridges[0]
    elif rungs:
        session_state = SESSION_IN_PROGRESS
        next_action = rungs[0]["entry_action"]
    else:
        session_state = SESSION_COMPLETE
        next_action = {
            "type": "COMPLETE",
            "reason": "No local rungs remain in the selected matrix.",
        }

    return {
        "subject": subject,
        "matrix_id": matrix_id,
        "bucket_id": readiness.get("bucket_id"),
        "subtopic": readiness.get("subtopic"),
        "readiness_status": status,
        "session_state": session_state,
        "profile_id": profile.get("profile_id") if profile else None,
        "bridges": bridges,
        "rungs": rungs,
        "next_action": next_action,
        "academic_warnings": list(readiness.get("academic_warnings", [])),
        "findings": [],
        "passed": True,
        "rule": (
            "One explicit readiness-audited matrix only. The runner exposes existing "
            "teaching/reconstruction/verification content and delegates attempt diagnosis "
            "to feedback.py; it does not create curriculum or learner truth."
        ),
    }


def _rung_for_microtopic(readiness: dict, microtopic_ref: str) -> tuple[int, dict] | None:
    rows = _rung_rows(readiness)
    for index, row in enumerate(rows):
        if row.get("microtopic_ref") == microtopic_ref:
            return index, row
    return None


def _next_local_action(
    readiness: dict,
    index: dict,
    current_microtopic_ref: str,
    profile: dict | None,
    repo: Path,
) -> dict:
    found = _rung_for_microtopic(readiness, current_microtopic_ref)
    if found is None:
        return {
            "type": "STOP",
            "reason": "Current microtopic is not a rung of the selected matrix.",
        }
    position, _ = found
    rows = _rung_rows(readiness)
    if position + 1 >= len(rows):
        return {
            "type": "COMPLETE",
            "reason": "The final rung was independently verified.",
        }

    next_rung = rows[position + 1]
    microtopic = index["microtopics"].get(next_rung.get("microtopic_ref"), {})
    state = _state(profile, next_rung.get("capability_ref"), repo)
    return _local_action(next_rung, microtopic, state)


def attempt(
    request: dict,
    profile: dict | None = None,
    repo: Path = REPO,
) -> dict:
    """Run one matrix exit-task attempt through the existing feedback runtime."""
    subject = request.get("subject")
    matrix_id = request.get("matrix_id")
    microtopic_ref = request.get("microtopic_ref")
    readiness = _readiness(subject, matrix_id, repo)

    if readiness.get("status") not in STARTABLE:
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "session_state": SESSION_STOPPED,
            "next_action": "STOP",
            "findings": [{
                "point": "STUDY_SESSION_MATRIX_NOT_READY",
                "detail": "attempt refused because the selected matrix is not session-ready",
            }],
            "passed": False,
        }

    found = _rung_for_microtopic(readiness, microtopic_ref)
    if found is None:
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "session_state": SESSION_STOPPED,
            "next_action": "STOP",
            "findings": [{
                "point": "STUDY_SESSION_MICROTOPIC_OUTSIDE_MATRIX",
                "microtopic_ref": microtopic_ref,
                "detail": "attempt target is not a rung of the selected matrix",
            }],
            "passed": False,
        }

    _, rung = found
    index = _index(subject, repo)
    microtopic = index["microtopics"].get(microtopic_ref)
    if not microtopic or not microtopic.get("exit_task"):
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "session_state": SESSION_STOPPED,
            "next_action": "STOP",
            "findings": [{
                "point": "STUDY_SESSION_EXIT_TASK_MISSING",
                "microtopic_ref": microtopic_ref,
                "detail": "selected rung has no exit task to run",
            }],
            "passed": False,
        }

    question_ref = f"{microtopic_ref}:exit_task"
    evaluation = dict(request.get("evaluation") or {})
    feedback_request = {
        "subject": subject,
        "question_ref": question_ref,
        "worksheet_question": {
            "question_id": question_ref,
            "primary_capability_ref": rung["capability_ref"],
            "secondary_capability_refs": [],
            "mapping_basis": "SESSION_EXIT_TASK",
        },
        "attempt_number": request.get("attempt_number", 1),
        "attempted_question_refs": list(request.get("attempted_question_refs", [])),
        "shown_hint_indices": list(request.get("shown_hint_indices", [])),
        "help_used": request.get("help_used", "NONE"),
        "when": request.get("when"),
        "session_ref": request.get("session_ref"),
        "response_summary": request.get("response_summary"),
        "evaluation": evaluation,
    }
    result = feedback.run(feedback_request, repo)

    if not result.get("passed"):
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "microtopic_ref": microtopic_ref,
            "session_state": SESSION_IN_PROGRESS,
            "feedback": result,
            "next_action": result.get("next_action", "STOP"),
            "findings": list(result.get("findings", [])),
            "passed": False,
        }

    if result.get("next_action") == "CONTINUE":
        next_action = _next_local_action(
            readiness,
            index,
            microtopic_ref,
            profile,
            repo,
        )
        session_state = (
            SESSION_COMPLETE
            if next_action.get("type") == "COMPLETE"
            else SESSION_IN_PROGRESS
        )
        return {
            "subject": subject,
            "matrix_id": matrix_id,
            "microtopic_ref": microtopic_ref,
            "session_state": session_state,
            "feedback": result,
            "next_action": next_action,
            "findings": [],
            "passed": True,
        }

    return {
        "subject": subject,
        "matrix_id": matrix_id,
        "microtopic_ref": microtopic_ref,
        "session_state": SESSION_IN_PROGRESS,
        "feedback": result,
        "next_action": {
            "type": result.get("next_action"),
            **({
                "diagnostic_options": result.get("diagnostic_options"),
            } if result.get("diagnostic_options") is not None else {}),
            **({
                "repair": result.get("repair"),
                "after_repair": result.get("after_repair"),
            } if result.get("repair") is not None else {}),
            **({
                "verification": result.get("verification"),
            } if result.get("verification") is not None else {}),
            **({
                "hint": result.get("hint"),
            } if result.get("hint") is not None else {}),
        },
        "findings": [],
        "passed": True,
    }


def run(
    request: dict,
    profile: dict | None = None,
    repo: Path = REPO,
) -> dict:
    command = request.get("command", "START")
    if command == "START":
        return start(
            request.get("subject"),
            request.get("matrix_id"),
            profile=profile,
            repo=repo,
        )
    if command == "ATTEMPT":
        return attempt(request, profile=profile, repo=repo)
    return {
        "subject": request.get("subject"),
        "matrix_id": request.get("matrix_id"),
        "session_state": SESSION_STOPPED,
        "next_action": "STOP",
        "findings": [{
            "point": "STUDY_SESSION_COMMAND_UNKNOWN",
            "detail": "command must be START or ATTEMPT",
        }],
        "passed": False,
    }


def readable(report: dict) -> str:
    out = [
        f'# Study session -- {report.get("subtopic") or report.get("matrix_id")}',
        "",
        f'  readiness: {report.get("readiness_status", "-")}',
        f'  state:     {report.get("session_state", "-")}',
        "",
    ]
    action = report.get("next_action")
    if isinstance(action, dict):
        out += [
            "## Next action",
            "",
            f'  {action.get("type")}',
        ]
        if action.get("capability_ref"):
            out.append(f'  capability: {action["capability_ref"]}')
        if action.get("microtopic_ref"):
            out.append(f'  microtopic: {action["microtopic_ref"]}')
        if action.get("external_provider"):
            out.append(f'  provider: {action["external_provider"]}')
        if action.get("reason"):
            out.append(f'  reason: {action["reason"]}')
        verification = action.get("verification")
        if verification and verification.get("prompt"):
            out += ["", f'  prompt: {verification["prompt"]}']
    elif action:
        out += ["## Next action", "", f'  {action}']

    if report.get("academic_warnings"):
        out += ["", "## Academic/source warnings", ""]
        for warning in report["academic_warnings"]:
            out.append(f'  {warning["point"]}: {warning["detail"]}')
    if report.get("findings"):
        out += ["", "## Findings", ""]
        for finding in report["findings"]:
            out.append(f'  {finding["point"]}: {finding["detail"]}')
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--readable", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    request = json.loads(args.input.read_text(encoding="utf-8"))
    profile = load(args.profile) if args.profile else None
    report = run(request, profile=profile)
    print(readable(report) if args.readable
          else json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report.get("passed", False) else 0


if __name__ == "__main__":
    raise SystemExit(main())
