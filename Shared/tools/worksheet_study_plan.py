#!/usr/bin/env python3
"""Compile one learner-facing worksheet -> study plan from existing core layers.

This is an orchestration/view layer, not a new learning architecture. It composes:

    worksheet map
    -> canonical question/capability locations
    -> prerequisite-ordered study route
    -> optional local owner-estimate start hints
    -> optional learner evidence overlay

The output deliberately keeps question demand, canonical teaching truth, owner estimates
and learner evidence separate. Owner estimates never become mastery evidence, and learner
state never enters matrices or capabilities.
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
from Shared.tools import learner_evidence, study_map, study_start  # noqa: E402

STATE_PRIORITY = {
    "MISSING": 40,
    "UNCERTAIN": 30,
    "UNOBSERVED": 20,
    "DEMONSTRATED": 10,
}


def _lesson(location: dict, index: dict) -> dict:
    microtopic_ref = location.get("microtopic_ref")
    microtopic = index["microtopics"].get(microtopic_ref, {})
    title = microtopic.get("title")
    label_base = (
        location.get("subtopic")
        or location.get("topic")
        or location.get("matrix_id")
        or "unknown matrix"
    )
    rung = location.get("rung")
    label = f"{label_base} / {rung}" if rung else str(label_base)
    return {
        "matrix_id": location.get("matrix_id"),
        "bucket_id": location.get("bucket_id"),
        "rung": rung,
        "ladder_position": location.get("ladder_position"),
        "microtopic_ref": microtopic_ref,
        "microtopic_title": title,
        "label": label,
    }


def _profile_state(profile: dict | None, capability_ref: str,
                   repo: Path) -> dict:
    if profile is None:
        return {
            "state": "UNOBSERVED",
            "source": "NO_PROFILE",
            "observation_ref": None,
            "when": None,
            "help": None,
        }
    return learner_evidence.effective_state(profile, capability_ref, repo)


def _observation_lookup(profile: dict | None, repo: Path) -> dict[str, dict]:
    if profile is None:
        return {}
    all_observations = learner_evidence.load_observations(repo)
    return {
        ref: all_observations[ref]
        for ref in profile.get("observation_refs", [])
        if ref in all_observations
    }


def _attention_for(capabilities: list[dict], observations: dict[str, dict]) -> tuple[str, str]:
    """Return question-level learner state and an evidence-grounded attention note."""
    if not capabilities:
        return "UNOBSERVED", "No mapped capability is available to diagnose."

    worst = max(
        capabilities,
        key=lambda row: STATE_PRIORITY.get(row["learner_state"]["state"], 0),
    )
    state = worst["learner_state"]["state"]
    evidence = worst["learner_state"]
    observation_ref = evidence.get("observation_ref")
    observation = observations.get(observation_ref or "")

    if observation:
        observed = observation.get("observed", "").strip()
        stage = observation.get("error_stage")
        prefix = f"{stage.title()} — " if stage and stage != "UNKNOWN" else ""
        if observed:
            return state, f"{prefix}{observed}"
    capability = worst.get("capability_ref")
    if state == "MISSING":
        return state, f"{capability} is currently marked missing; teach before retry."
    if state == "UNCERTAIN":
        return state, f"{capability} is currently uncertain; repair then retry independently."
    if state == "DEMONSTRATED":
        return state, "Mapped capability is already demonstrated; use this mainly as consolidation."
    return state, "No learner evidence yet; use the first attempt as the diagnostic."


def _route_action(row: dict, learner_state: dict) -> tuple[str, str]:
    """Let real evidence override an estimate; otherwise preserve study_start's action."""
    if row.get("state") == "EXTERNAL_BRIDGE":
        provider = row.get("external_provider") or "external provider"
        status = row.get("acceptance_status")
        suffix = f" ({status})" if status else ""
        return "BRIDGE", f"Use/check the declared provider: {provider}{suffix}."
    if row.get("state") != "RESOLVED":
        return "UNRESOLVED", "Canonical teaching location is unresolved."

    state = learner_state["state"]
    scope = row.get("scope")
    if state == "MISSING":
        return "TEACH", "Current learner evidence says MISSING."
    if state == "UNCERTAIN":
        return "REPAIR", "Current learner evidence says UNCERTAIN."
    if state == "DEMONSTRATED":
        if scope in {"QUESTION_ONLY", "QUESTION_AND_SYLLABUS"}:
            return "QUICK_CHECK", "Already demonstrated; confirm briefly on the worksheet demand."
        return "SKIP", "Prerequisite is already demonstrated; no study detour is needed."

    estimate = row.get("estimate_basis")
    if estimate:
        action = row.get("learner_action") or "STUDY"
        return (
            action,
            f'Owner estimate {estimate["knowledge_percentage"]}% selected '
            f'{estimate["selected_rung"]}; this is a routing hint, not evidence.',
        )
    return row.get("learner_action") or "STUDY", (
        "No learner evidence or owner estimate is available; follow the canonical route."
    )


def resolve(mapping: dict, owner_estimates: list[dict] | None = None,
            profile: dict | None = None, repo: Path = REPO) -> dict:
    """Compile a learner-facing question map plus an ordered study route."""
    started = study_start.resolve(mapping, owner_estimates or [], repo)
    subject = mapping.get("subject")
    index = study_map.subject_index(subject, repo)
    resolved_map = study_map.resolve(mapping, repo)
    observations = _observation_lookup(profile, repo)

    if profile is not None and profile.get("provenance") == "SYNTHETIC_TEST":
        findings = list(started.get("findings", []))
        findings.append({
            "point": "WORKSHEET_STUDY_PLAN_SYNTHETIC_PROFILE_REFUSED",
            "profile_id": profile.get("profile_id"),
            "detail": "a synthetic test profile may not be used for learner routing",
        })
        return {
            "worksheet_id": mapping.get("worksheet_id"),
            "subject": subject,
            "profile_id": profile.get("profile_id"),
            "questions": [],
            "route": [],
            "start_decisions": started.get("start_decisions", []),
            "findings": findings,
            "passed": False,
        }

    resolved_questions = {
        row["question_id"]: row
        for row in resolved_map.get("questions", [])
    }
    question_rows = []
    for declared in mapping.get("questions", []):
        qid = declared["question_id"]
        mapped = resolved_questions.get(qid, {})
        capability_rows = []
        for cap in mapped.get("capabilities", []):
            capability_ref = cap["capability_ref"]
            state = _profile_state(profile, capability_ref, repo)
            lessons = [_lesson(loc, index) for loc in cap.get("locations", [])]
            capability_rows.append({
                "role": cap.get("role"),
                "capability_ref": capability_ref,
                "state": cap.get("state"),
                "action": cap.get("action"),
                "success_criterion": cap.get("success_criterion"),
                "external_provider": cap.get("external_provider"),
                "acceptance_status": cap.get("acceptance_status"),
                "learner_state": state,
                "lessons": lessons,
            })

        primary = next(
            (row for row in capability_rows if row.get("role") == "PRIMARY"),
            capability_rows[0] if capability_rows else None,
        )
        primary_lesson = (
            primary["lessons"][0]["microtopic_title"]
            if primary and primary.get("lessons")
            and primary["lessons"][0].get("microtopic_title")
            else (primary.get("action") if primary else "Unmapped capability")
        )
        lesson_labels = [
            lesson["label"]
            for cap in capability_rows
            for lesson in cap.get("lessons", [])
        ]
        lesson_labels += [
            f'External bridge: {cap.get("external_provider")}'
            for cap in capability_rows
            if cap.get("state") == "EXTERNAL_BRIDGE"
        ]
        question_state, attention = _attention_for(capability_rows, observations)
        question_rows.append({
            "question_id": qid,
            "mapping_state": mapped.get("state"),
            "primary_capability_ref": declared.get("primary_capability_ref"),
            "secondary_capability_refs": list(declared.get("secondary_capability_refs") or []),
            "core_lesson": " + ".join(lesson_labels) if lesson_labels else "UNRESOLVED",
            "what_is_being_learned": primary_lesson,
            "learner_state": question_state,
            "why_extra_attention": attention,
            "capabilities": capability_rows,
        })

    route_rows = []
    for row in started.get("route", []):
        capability_ref = row["capability_ref"]
        state = _profile_state(profile, capability_ref, repo)
        action, reason = _route_action(row, state)
        locations = [_lesson(loc, index) for loc in row.get("locations", [])]
        route_rows.append({
            **row,
            "learner_state": state,
            "recommended_action": action,
            "action_reason": reason,
            "lessons": locations,
        })

    findings = list(started.get("findings", []))
    return {
        "worksheet_id": mapping.get("worksheet_id"),
        "subject": subject,
        "profile_id": profile.get("profile_id") if profile else None,
        "questions": question_rows,
        "route": route_rows,
        "start_decisions": started.get("start_decisions", []),
        "findings": findings,
        "passed": not findings,
        "rules": [
            "Worksheet mappings describe demand; canonical subject records remain academic truth.",
            "Cross-matrix study order comes only from capability prerequisites.",
            "Owner estimates choose a local starting attempt and never create mastery evidence.",
            "Observed learner state overrides owner estimates but never mutates subject content.",
        ],
    }


def _md(value) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def readable(report: dict) -> str:
    out = [
        f'# Worksheet study plan — {report.get("worksheet_id")}',
        "",
        f'  subject: {report.get("subject")}',
        f'  profile: {report.get("profile_id") or "none"}',
        "",
        "## Question -> study map",
        "",
        "| Question | Core (1) lesson | What is being learned | Learner state | Why extra attention? |",
        "|---|---|---|---|---|",
    ]
    for row in report.get("questions", []):
        out.append(
            "| " + " | ".join([
                _md(row["question_id"]),
                _md(row["core_lesson"]),
                _md(row["what_is_being_learned"]),
                _md(row["learner_state"]),
                _md(row["why_extra_attention"]),
            ]) + " |"
        )

    out += [
        "",
        "## Ordered study route",
        "",
        "| # | Action | Capability | Lesson | State | Why |",
        "|---:|---|---|---|---|---|",
    ]
    for row in report.get("route", []):
        lesson = " + ".join(item["label"] for item in row.get("lessons", []))
        if not lesson and row.get("state") == "EXTERNAL_BRIDGE":
            lesson = f'External bridge: {row.get("external_provider")}'
        out.append(
            "| " + " | ".join([
                _md(row.get("order")),
                _md(row.get("recommended_action")),
                _md(row.get("capability_ref")),
                _md(lesson or "UNRESOLVED"),
                _md(row.get("learner_state", {}).get("state")),
                _md(row.get("action_reason")),
            ]) + " |"
        )

    if report.get("findings"):
        out += ["", "## Findings", ""]
        for finding in report["findings"]:
            out.append(
                f'- {_md(finding.get("point"))}: {_md(finding.get("detail", ""))}'
            )
    return "\n".join(out)


def _estimates(raw_values: list[str], parser: argparse.ArgumentParser) -> list[dict]:
    rows = []
    for raw in raw_values:
        if "=" not in raw:
            parser.error("--estimate must be MATRIX_ID=PERCENT")
        matrix_id, percentage = raw.split("=", 1)
        try:
            number = float(percentage)
        except ValueError:
            parser.error(f"invalid percentage in --estimate {raw}")
        rows.append({
            "matrix_id": matrix_id,
            "knowledge_percentage": number,
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--map", type=Path, required=True, help="worksheet capability map JSON")
    parser.add_argument("--profile", type=Path, help="optional learner profile JSON")
    parser.add_argument(
        "--estimate",
        action="append",
        default=[],
        metavar="MATRIX_ID=PERCENT",
        help="optional rough owner estimate for one local matrix; may be repeated",
    )
    parser.add_argument("--readable", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    mapping = load(args.map)
    profile = load(args.profile) if args.profile else None
    report = resolve(mapping, _estimates(args.estimate, parser), profile)
    print(readable(report) if args.readable
          else json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
