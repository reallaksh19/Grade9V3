#!/usr/bin/env python3
"""Replay a frozen agent-path stress case and report routing drift.

This is a developer/test convenience tool. It does not author content and does not create
learner evidence.

Examples:

  python3 tools/run_agent_path_stress.py --list
  python3 tools/run_agent_path_stress.py --case APSTRESS-REL-60-TEACH --prompt-only
  python3 tools/run_agent_path_stress.py --case APSTRESS-REL-60-TEACH
  python3 tools/run_agent_path_stress.py --all --enforce
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import compile_execution_packet, plan_request, resolve_request  # noqa: E402

FIXTURE = REPO / "tests/fixtures/agent_path_stress/cases.json"


def load_suite() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def by_id(suite: dict) -> dict[str, dict]:
    return {row["case_id"]: row for row in suite["cases"]}


def actual_projection(case: dict) -> dict:
    report = plan_request.plan(case["request"])
    packet = compile_execution_packet.compile_packet(case["request"])
    purposes = resolve_request.purposes()
    practice_support = {}
    for core, intent in case["request"].get("practice", {}).items():
        purpose = purposes.get(intent.get("purpose"))
        if purpose:
            practice_support[core] = purpose["support"]

    return {
        "passed": report["passed"],
        "entry": report["learner_route"].get("entry"),
        "selected_by": report["learner_route"].get("selected_by"),
        "route_state": report["learner_route"].get("state"),
        "prerequisite_checks": report["learner_route"].get("prerequisite_checks", []),
        "required_owner_inputs": [row["id"] for row in report["required_owner_inputs"]],
        "practice_support": practice_support,
        "selected_segment": [
            row["rung"] for row in packet.get("canonical", {}).get("selected_segment", [])
        ],
        "core1a_core1b_relationship": (
            report.get("core_relationships", {}).get("CORE1A_CORE1B")
        ),
        "no_content_authored": report.get("no_content_authored"),
        "findings": report.get("findings", []),
    }


def compare(case: dict, actual: dict) -> list[dict]:
    expected = case["expected"]
    differences = []
    for field in (
        "entry",
        "selected_by",
        "route_state",
        "prerequisite_checks",
        "required_owner_inputs",
        "practice_support",
    ):
        if actual.get(field) != expected.get(field):
            differences.append({
                "field": field,
                "expected": expected.get(field),
                "actual": actual.get(field),
            })

    if "selected_segment" in expected:
        if actual.get("selected_segment") != expected["selected_segment"]:
            differences.append({
                "field": "selected_segment",
                "expected": expected["selected_segment"],
                "actual": actual.get("selected_segment"),
            })

    requested = set(case["request"].get("requested_cores", []))
    if {"CORE1A", "CORE1B"}.issubset(requested):
        expected_relation = "same canonical rung segment; agency changes, target does not"
        if actual.get("core1a_core1b_relationship") != expected_relation:
            differences.append({
                "field": "core1a_core1b_relationship",
                "expected": expected_relation,
                "actual": actual.get("core1a_core1b_relationship"),
            })

    if actual.get("no_content_authored") is not True:
        differences.append({
            "field": "no_content_authored",
            "expected": True,
            "actual": actual.get("no_content_authored"),
        })

    return differences


def run_case(case: dict) -> dict:
    actual = actual_projection(case)
    differences = compare(case, actual)
    return {
        "case_id": case["case_id"],
        "prompt": case["prompt"],
        "status": "PASS" if not differences else "DRIFT",
        "actual": actual,
        "expected": case["expected"],
        "differences": differences,
        "must_not": case["expected"].get("must_not", []),
        "evidence_class": "SYSTEM_STRESS_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--case")
    group.add_argument("--all", action="store_true")
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="print only the frozen human prompt; useful for a blind agent run",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON rather than the compact text report",
    )
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="exit non-zero when any frozen expectation has drifted",
    )
    args = parser.parse_args()

    suite = load_suite()
    cases = by_id(suite)

    if args.list:
        for row in suite["cases"]:
            print(row["case_id"])
        return 0

    selected = suite["cases"] if args.all else [cases.get(args.case)]
    if selected == [None]:
        print(f"unknown case: {args.case}", file=sys.stderr)
        print("available: " + ", ".join(cases), file=sys.stderr)
        return 2

    if args.prompt_only:
        if len(selected) != 1:
            print("--prompt-only requires exactly one --case", file=sys.stderr)
            return 2
        print(selected[0]["prompt"])
        return 0

    reports = [run_case(case) for case in selected]
    failed = [row for row in reports if row["status"] != "PASS"]

    if args.json:
        print(json.dumps({
            "suite_id": suite["suite_id"],
            "reports": reports,
            "passed": not failed,
        }, indent=2, ensure_ascii=False))
    else:
        print(f'suite={suite["suite_id"]}')
        for report in reports:
            print(f'{report["case_id"]}: {report["status"]}')
            actual = report["actual"]
            print(
                "  "
                f'entry={actual["entry"]} '
                f'route={actual["route_state"]} '
                f'checks={actual["prerequisite_checks"]} '
                f'owner_inputs={actual["required_owner_inputs"]} '
                f'support={actual["practice_support"]} '
                f'segment={actual["selected_segment"]}'
            )
            for diff in report["differences"]:
                print(
                    f'  DRIFT {diff["field"]}: '
                    f'expected={diff["expected"]!r} actual={diff["actual"]!r}'
                )

    return 1 if args.enforce and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
