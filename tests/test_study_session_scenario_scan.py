"""Semantic scenario scanner for study-session routing and execution.

This file complements the exhaustive feedback-policy scanner in test_feedback.py.
It deliberately scans the finite study-session orchestration partitions that are not
covered there: owner estimates, owner choices, route fallback/owner-decision states,
dependency propagation, question projection, and readiness-aware attempt boundaries.

All scenarios are synthetic regression evidence.  Nothing here is LIVE_LEARNER evidence.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_session  # noqa: E402


class StudySessionScenarioScan(unittest.TestCase):
    SESSION_FIXTURE = REPO / "tests/fixtures/study_session/relative-motion.worksheet.json"
    NEETPREP_FIXTURE = REPO / "tests/fixtures/real_pilots/neetprep-relative-motion.worksheet.json"

    def mapping(self):
        return json.loads(self.SESSION_FIXTURE.read_text(encoding="utf-8"))

    def neetprep(self):
        return json.loads(self.NEETPREP_FIXTURE.read_text(encoding="utf-8"))

    @staticmethod
    def route_row(
        capability="CAP-A",
        *,
        state="RESOLVED",
        delivery_state="LOCAL",
        action="STUDY",
        depends_on=None,
        locations=None,
        lessons=None,
    ):
        if locations is None:
            locations = [{"matrix_id": "M-A", "rung": "R1"}]
        if lessons is None:
            lessons = [
                {
                    "matrix_id": row["matrix_id"],
                    "rung": row["rung"],
                    "label": f'{row["matrix_id"]} / {row["rung"]}',
                }
                for row in locations
            ]
        return {
            "order": 1,
            "capability_ref": capability,
            "depends_on": list(depends_on or []),
            "state": state,
            "delivery_state": delivery_state,
            "recommended_action": action,
            "action_reason": "scenario scan",
            "locations": locations,
            "lessons": lessons,
        }

    @staticmethod
    def readiness(
        matrix_id="M-A",
        *,
        status=session_readiness.READY,
        rung_state="READY",
        blocking_findings=None,
    ):
        return {
            "matrix_id": matrix_id,
            "subtopic": matrix_id,
            "status": status,
            "rungs": [
                {
                    "rung": "R1",
                    "state": rung_state,
                    "teaching": rung_state != "BLOCKED",
                    "verification": rung_state != "BLOCKED",
                }
            ],
            "blocking_findings": list(blocking_findings or []),
            "external_bridges": [],
            "support_findings": [],
            "academic_warnings": [],
        }

    def test_estimate_parser_semantic_partitions(self):
        cases = [
            ("matrix-id", ["MATRIX-PHY-RELATIVE-MOTION=60"], 1, set()),
            ("bucket-id", ["BUCKET-RELATIVE-MOTION=60"], 1, set()),
            ("subtopic", ["relative motion=60"], 1, set()),
            ("zero-boundary", ["relative motion=0"], 1, set()),
            ("hundred-boundary", ["relative motion=100"], 1, set()),
            ("missing-equals", ["relative motion"], 0, {"STUDY_SESSION_ESTIMATE_FORMAT"}),
            ("not-a-number", ["relative motion=abc"], 0, {"STUDY_SESSION_ESTIMATE_PERCENT_INVALID"}),
            ("below-zero", ["relative motion=-1"], 0, {"STUDY_SESSION_ESTIMATE_PERCENT_OUT_OF_RANGE"}),
            ("above-hundred", ["relative motion=101"], 0, {"STUDY_SESSION_ESTIMATE_PERCENT_OUT_OF_RANGE"}),
            ("unknown-target", ["definitely-not-a-matrix=60"], 0, {"STUDY_SESSION_ESTIMATE_TARGET_UNKNOWN"}),
        ]
        for name, raw, expected_count, expected_points in cases:
            with self.subTest(name=name):
                estimates, findings = study_session.resolve_estimates("Physics", raw)
                self.assertEqual(len(estimates), expected_count)
                self.assertEqual({row["point"] for row in findings}, expected_points)

        duplicate_subtopics = [
            {"matrix_id": "M-1", "bucket_id": "B-1", "subtopic": "Same topic"},
            {"matrix_id": "M-2", "bucket_id": "B-2", "subtopic": "Same topic"},
        ]
        with patch.object(study_session, "_matrices", return_value=duplicate_subtopics):
            estimates, findings = study_session.resolve_estimates(
                "Physics", ["same topic=50"]
            )
        self.assertEqual(estimates, [])
        self.assertEqual(
            [row["point"] for row in findings],
            ["STUDY_SESSION_ESTIMATE_TARGET_AMBIGUOUS"],
        )

    def test_owner_choice_parser_semantic_partitions(self):
        cases = [
            (
                "external-valid",
                ["CAP-A=EXTERNAL:Owner tutor"],
                {"CAP-A": {"kind": "EXTERNAL", "provider": "Owner tutor", "scope": "SESSION_ONLY"}},
                set(),
            ),
            (
                "location-valid",
                ["CAP-A=LOCATION:M-A:R1"],
                {"CAP-A": {"kind": "LOCATION", "matrix_id": "M-A", "rung": "R1", "scope": "SESSION_ONLY"}},
                set(),
            ),
            ("missing-equals", ["CAP-A"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("missing-capability", ["=EXTERNAL:Tutor"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("missing-kind-separator", ["CAP-A=EXTERNAL"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("external-provider-empty", ["CAP-A=EXTERNAL:"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("location-matrix-only", ["CAP-A=LOCATION:M-A"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("location-rung-empty", ["CAP-A=LOCATION:M-A:"], {}, {"STUDY_SESSION_OWNER_CHOICE_FORMAT"}),
            ("unknown-kind", ["CAP-A=LOCAL:M-A:R1"], {}, {"STUDY_SESSION_OWNER_CHOICE_KIND_UNKNOWN"}),
        ]
        for name, raw, expected_choices, expected_points in cases:
            with self.subTest(name=name):
                choices, warnings = study_session.resolve_owner_choices(raw)
                self.assertEqual(choices, expected_choices)
                self.assertEqual({row["point"] for row in warnings}, expected_points)

        choices, warnings = study_session.resolve_owner_choices(
            ["CAP-A=EXTERNAL:First", "CAP-A=EXTERNAL:Second"]
        )
        self.assertEqual(choices["CAP-A"]["provider"], "First")
        self.assertEqual(
            [row["point"] for row in warnings],
            ["STUDY_SESSION_OWNER_CHOICE_DUPLICATE"],
        )

    def test_route_execution_semantic_partitions(self):
        ready = self.readiness()
        needs_support = self.readiness(rung_state="NEEDS_SUPPORT")
        not_ready = self.readiness(status=session_readiness.NOT_READY)
        pilot = self.readiness(status=session_readiness.PILOT_READY)
        blocked = self.readiness(rung_state="BLOCKED")
        missing_teaching = self.readiness(
            status=session_readiness.NOT_READY,
            rung_state="NEEDS_SUPPORT",
            blocking_findings=[
                {
                    "point": "READINESS_TEACHING_PATH_MISSING",
                    "where": "R1",
                    "detail": "scenario",
                }
            ],
        )

        def run(row, readiness_rows=None, warnings=None, choices=None):
            return study_session._route_execution(
                {"route": [row]},
                list(readiness_rows or []),
                list(warnings or []),
                dict(choices or {}),
            )

        cases = [
            {
                "name": "ready-local",
                "row": self.route_row(),
                "readiness": [ready],
                "row_disposition": None,
                "overall": None,
                "executable": 1,
                "owners": 0,
                "fallbacks": 0,
            },
            {
                "name": "ready-local-with-warning",
                "row": self.route_row(),
                "readiness": [ready],
                "warnings": [{"point": "OPTIONAL_WARNING"}],
                "row_disposition": None,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 0,
            },
            {
                "name": "needs-support",
                "row": self.route_row(),
                "readiness": [needs_support],
                "row_disposition": study_session.EXECUTE_WITH_FALLBACK,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 1,
            },
            {
                "name": "pilot-matrix",
                "row": self.route_row(),
                "readiness": [pilot],
                "row_disposition": study_session.EXECUTE_WITH_FALLBACK,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 1,
            },
            {
                "name": "not-ready-matrix-usable-rung",
                "row": self.route_row(),
                "readiness": [not_ready],
                "row_disposition": study_session.EXECUTE_WITH_FALLBACK,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 1,
            },
            {
                "name": "blocked-rung",
                "row": self.route_row(),
                "readiness": [blocked],
                "row_disposition": study_session.OWNER_DECISION,
                "overall": study_session.OWNER_DECISION,
                "executable": 0,
                "owners": 1,
                "fallbacks": 0,
            },
            {
                "name": "missing-teaching",
                "row": self.route_row(),
                "readiness": [missing_teaching],
                "row_disposition": study_session.OWNER_DECISION,
                "overall": study_session.OWNER_DECISION,
                "executable": 0,
                "owners": 1,
                "fallbacks": 0,
            },
            {
                "name": "unresolved-no-choice",
                "row": self.route_row(
                    state="UNRESOLVED",
                    delivery_state="UNRESOLVED",
                    action="UNRESOLVED",
                    locations=[],
                    lessons=[],
                ),
                "readiness": [],
                "row_disposition": study_session.OWNER_DECISION,
                "overall": study_session.OWNER_DECISION,
                "executable": 0,
                "owners": 1,
                "fallbacks": 0,
            },
            {
                "name": "ambiguous-no-choice",
                "row": self.route_row(
                    state="AMBIGUOUS",
                    delivery_state="AMBIGUOUS",
                    action="UNRESOLVED",
                    locations=[
                        {"matrix_id": "M-A", "rung": "R1"},
                        {"matrix_id": "M-X", "rung": "R1"},
                    ],
                ),
                "readiness": [ready, self.readiness("M-X")],
                "row_disposition": study_session.OWNER_DECISION,
                "overall": study_session.OWNER_DECISION,
                "executable": 0,
                "owners": 1,
                "fallbacks": 0,
            },
            {
                "name": "unresolved-owner-external",
                "row": self.route_row(
                    state="UNRESOLVED",
                    delivery_state="UNRESOLVED",
                    action="UNRESOLVED",
                    locations=[],
                    lessons=[],
                ),
                "readiness": [],
                "choices": {
                    "CAP-A": {"kind": "EXTERNAL", "provider": "Tutor", "scope": "SESSION_ONLY"}
                },
                "row_disposition": study_session.EXECUTE_WITH_FALLBACK,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 1,
                "applied": 1,
                "recommended_action": "BRIDGE",
            },
            {
                "name": "ambiguous-owner-offered-location",
                "row": self.route_row(
                    state="AMBIGUOUS",
                    delivery_state="AMBIGUOUS",
                    action="UNRESOLVED",
                    locations=[
                        {"matrix_id": "M-A", "rung": "R1"},
                        {"matrix_id": "M-X", "rung": "R1"},
                    ],
                ),
                "readiness": [ready, self.readiness("M-X")],
                "choices": {
                    "CAP-A": {
                        "kind": "LOCATION",
                        "matrix_id": "M-X",
                        "rung": "R1",
                        "scope": "SESSION_ONLY",
                    }
                },
                "row_disposition": study_session.EXECUTE_WITH_FALLBACK,
                "overall": study_session.EXECUTE_WITH_FALLBACK,
                "executable": 1,
                "owners": 0,
                "fallbacks": 1,
                "applied": 1,
            },
            {
                "name": "ambiguous-owner-unoffered-location",
                "row": self.route_row(
                    state="AMBIGUOUS",
                    delivery_state="AMBIGUOUS",
                    action="UNRESOLVED",
                    locations=[
                        {"matrix_id": "M-A", "rung": "R1"},
                        {"matrix_id": "M-X", "rung": "R1"},
                    ],
                ),
                "readiness": [ready, self.readiness("M-X")],
                "choices": {
                    "CAP-A": {
                        "kind": "LOCATION",
                        "matrix_id": "M-NOT-OFFERED",
                        "rung": "R9",
                        "scope": "SESSION_ONLY",
                    }
                },
                "row_disposition": study_session.OWNER_DECISION,
                "overall": study_session.OWNER_DECISION,
                "executable": 0,
                "owners": 1,
                "fallbacks": 0,
            },
            {
                "name": "canonical-external-bridge",
                "row": self.route_row(
                    state="RESOLVED",
                    delivery_state="EXTERNAL_BRIDGE",
                    action="BRIDGE",
                    locations=[],
                    lessons=[],
                ),
                "readiness": [],
                "row_disposition": None,
                "overall": None,
                "executable": 1,
                "owners": 0,
                "fallbacks": 0,
            },
            {
                "name": "skip",
                "row": self.route_row(action="SKIP"),
                "readiness": [ready],
                "row_disposition": None,
                "overall": None,
                "executable": 0,
                "owners": 0,
                "fallbacks": 0,
            },
        ]

        for case in cases:
            with self.subTest(name=case["name"]):
                (
                    route,
                    owners,
                    fallbacks,
                    executable,
                    overall,
                    applied,
                    choice_warnings,
                ) = run(
                    case["row"],
                    case.get("readiness"),
                    case.get("warnings"),
                    case.get("choices"),
                )
                self.assertEqual(route[0]["execution_disposition"], case["row_disposition"])
                self.assertEqual(overall, case["overall"])
                self.assertEqual(executable, case["executable"])
                self.assertEqual(len(owners), case["owners"])
                self.assertEqual(len(fallbacks), case["fallbacks"])
                self.assertEqual(len(applied), case.get("applied", 0))
                self.assertEqual(choice_warnings, [])
                if "recommended_action" in case:
                    self.assertEqual(route[0]["recommended_action"], case["recommended_action"])

        # Session-only choices cannot override an already-safe canonical route, and a
        # choice for a capability outside the current route remains a warning.
        (
            route,
            _owners,
            _fallbacks,
            executable,
            _overall,
            applied,
            choice_warnings,
        ) = run(
            self.route_row(),
            [ready],
            choices={
                "CAP-A": {"kind": "EXTERNAL", "provider": "Tutor", "scope": "SESSION_ONLY"},
                "CAP-NOT-IN-ROUTE": {
                    "kind": "EXTERNAL",
                    "provider": "Tutor",
                    "scope": "SESSION_ONLY",
                },
            },
        )
        self.assertEqual(route[0]["execution_disposition"], None)
        self.assertEqual(executable, 1)
        self.assertEqual(applied, [])
        self.assertEqual(
            {row["point"] for row in choice_warnings},
            {
                "STUDY_SESSION_OWNER_CHOICE_NOT_REQUIRED",
                "STUDY_SESSION_OWNER_CHOICE_TARGET_UNKNOWN",
            },
        )

    def test_dependency_and_question_projection_matrix(self):
        synthetic_plan = {
            "route": [
                self.route_row("CAP-A", locations=[{"matrix_id": "M-A", "rung": "R1"}]),
                self.route_row(
                    "CAP-B",
                    depends_on=["CAP-A"],
                    locations=[{"matrix_id": "M-B", "rung": "R1"}],
                ),
                self.route_row("CAP-C", locations=[{"matrix_id": "M-C", "rung": "R1"}]),
            ]
        }
        readiness = [
            self.readiness("M-A", rung_state="BLOCKED"),
            self.readiness("M-B"),
            self.readiness("M-C"),
        ]
        route, owners, _, executable, overall, _, _ = study_session._route_execution(
            synthetic_plan, readiness, [], {}
        )
        by_cap = {row["capability_ref"]: row for row in route}
        self.assertEqual(by_cap["CAP-A"]["execution_disposition"], study_session.OWNER_DECISION)
        self.assertEqual(by_cap["CAP-B"]["execution_disposition"], study_session.OWNER_DECISION)
        self.assertIsNone(by_cap["CAP-C"]["execution_disposition"])
        self.assertEqual(executable, 1)
        self.assertEqual(overall, study_session.EXECUTE_WITH_FALLBACK)
        self.assertEqual(len(owners), 2)

        question_cases = [
            (
                "primary-normal",
                [{"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": None}],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": []},
                None,
            ),
            (
                "primary-fallback",
                [{"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": study_session.EXECUTE_WITH_FALLBACK}],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": []},
                study_session.EXECUTE_WITH_FALLBACK,
            ),
            (
                "secondary-fallback",
                [
                    {"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": None},
                    {"capability_ref": "CAP-B", "depends_on": [], "execution_disposition": study_session.EXECUTE_WITH_FALLBACK},
                ],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": ["CAP-B"]},
                study_session.EXECUTE_WITH_FALLBACK,
            ),
            (
                "prerequisite-fallback",
                [
                    {"capability_ref": "CAP-A", "depends_on": ["CAP-P"], "execution_disposition": None},
                    {"capability_ref": "CAP-P", "depends_on": [], "execution_disposition": study_session.EXECUTE_WITH_FALLBACK},
                ],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": []},
                study_session.EXECUTE_WITH_FALLBACK,
            ),
            (
                "primary-owner",
                [{"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": study_session.OWNER_DECISION}],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": []},
                study_session.OWNER_DECISION,
            ),
            (
                "secondary-owner",
                [
                    {"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": None},
                    {"capability_ref": "CAP-B", "depends_on": [], "execution_disposition": study_session.OWNER_DECISION},
                ],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": ["CAP-B"]},
                study_session.OWNER_DECISION,
            ),
            (
                "prerequisite-owner",
                [
                    {"capability_ref": "CAP-A", "depends_on": ["CAP-P"], "execution_disposition": None},
                    {"capability_ref": "CAP-P", "depends_on": [], "execution_disposition": study_session.OWNER_DECISION},
                ],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": []},
                study_session.OWNER_DECISION,
            ),
            (
                "owner-dominates-fallback",
                [
                    {"capability_ref": "CAP-A", "depends_on": [], "execution_disposition": study_session.EXECUTE_WITH_FALLBACK},
                    {"capability_ref": "CAP-B", "depends_on": [], "execution_disposition": study_session.OWNER_DECISION},
                ],
                {"question_id": "Q", "primary_capability_ref": "CAP-A", "secondary_capability_refs": ["CAP-B"]},
                study_session.OWNER_DECISION,
            ),
        ]

        for name, qroute, question, expected in question_cases:
            with self.subTest(name=name):
                annotated, executable_ids, owner_ids = study_session._question_execution(
                    [question], qroute
                )
                self.assertEqual(annotated[0]["execution_disposition"], expected)
                if expected == study_session.OWNER_DECISION:
                    self.assertEqual(owner_ids, ["Q"])
                    self.assertEqual(executable_ids, [])
                else:
                    self.assertEqual(executable_ids, ["Q"])
                    self.assertEqual(owner_ids, [])

    def test_attempt_wrapper_readiness_and_evidence_boundaries(self):
        mapping = self.mapping()

        normal = study_session.attempt(
            mapping,
            "SCHOOL-REL-Q2",
            result="CORRECT",
            when="2026-09-18",
            help_used="NONE",
            session_ref="SCENARIO-SCAN",
        )
        self.assertEqual(normal["observation_draft"]["result"], "DEMONSTRATED")
        self.assertEqual(normal["persistence"], "NOT_WRITTEN")

        with patch.object(
            study_session,
            "_primary_verification_supported",
            return_value=False,
        ):
            limited = study_session.attempt(
                mapping,
                "SCHOOL-REL-Q2",
                result="CORRECT",
                when="2026-09-18",
                help_used="NONE",
                session_ref="SCENARIO-SCAN",
            )
        self.assertEqual(limited["observation_draft"]["result"], "UNCERTAIN")
        self.assertEqual(
            limited["evidence_limited"]["point"],
            "STUDY_SESSION_VERIFICATION_UNAVAILABLE",
        )
        self.assertEqual(limited["persistence"], "NOT_WRITTEN")

        neetprep = self.neetprep()

        unattributed = study_session.attempt(
            neetprep,
            "NEETPREP-MQB-REL-Q3",
            result="INCORRECT",
            when="2026-09-18",
            session_ref="SCENARIO-SCAN",
        )
        self.assertEqual(unattributed["next_action"], study_session.OWNER_DECISION)
        self.assertIn(
            "STUDY_SESSION_QUESTION_EXTERNAL_ONLY",
            [row["point"] for row in unattributed["findings"]],
        )

        local_failure = study_session.attempt(
            neetprep,
            "NEETPREP-MQB-REL-Q3",
            result="INCORRECT",
            failed_capability_ref="CAP-RELATIVE-V",
            when="2026-09-18",
            session_ref="SCENARIO-SCAN",
        )
        self.assertNotEqual(local_failure["next_action"], study_session.OWNER_DECISION)

        external_failure = study_session.attempt(
            neetprep,
            "NEETPREP-MQB-REL-Q3",
            result="INCORRECT",
            failed_capability_ref="CAP-RIGHT-TRIANGLE",
            when="2026-09-18",
            session_ref="SCENARIO-SCAN",
        )
        self.assertEqual(external_failure["next_action"], study_session.OWNER_DECISION)

        correct_with_external_secondary = study_session.attempt(
            neetprep,
            "NEETPREP-MQB-REL-Q3",
            result="CORRECT",
            when="2026-09-18",
            help_used="NONE",
            session_ref="SCENARIO-SCAN",
        )
        self.assertNotEqual(
            correct_with_external_secondary["next_action"],
            study_session.OWNER_DECISION,
        )


if __name__ == "__main__":
    unittest.main()
