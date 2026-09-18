"""Thin study-session runner composes readiness, routing and feedback without new truth."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_session  # noqa: E402


class StudySessionRunner(unittest.TestCase):
    FIXTURE = REPO / "tests/fixtures/study_session/relative-motion.worksheet.json"

    def mapping(self):
        return json.loads(self.FIXTURE.read_text(encoding="utf-8"))

    def test_human_subtopic_estimate_resolves_to_canonical_matrix(self):
        estimates, findings = study_session.resolve_estimates(
            "Physics",
            ["relative motion=60"],
        )
        self.assertEqual(findings, [])
        self.assertEqual(len(estimates), 1)
        self.assertEqual(estimates[0]["matrix_id"], "MATRIX-PHY-RELATIVE-MOTION")
        self.assertEqual(estimates[0]["knowledge_percentage"], 60)
        self.assertEqual(estimates[0]["input_target"], "relative motion")

    def test_relative_motion_plan_is_ready_with_bridge_and_starts_from_estimate(self):
        report = study_session.plan(
            self.mapping(),
            ["Relative motion=60"],
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["valid"])
        self.assertFalse(report["ready"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertEqual(len(report["readiness"]), 1)
        self.assertEqual(
            report["readiness"][0]["matrix_id"],
            "MATRIX-PHY-RELATIVE-MOTION",
        )
        self.assertEqual(
            report["readiness"][0]["status"],
            session_readiness.READY_WITH_BRIDGE,
        )

        route = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(route["CAP-SIGNED-PAIR"]["recommended_action"], "BRIDGE")
        self.assertEqual(route["CAP-SAME-TIME"]["recommended_action"], "START_HERE")
        self.assertEqual(route["CAP-RELATIVE-V"]["recommended_action"], "STUDY")
        self.assertEqual(route["CAP-VECTOR-CHECK"]["recommended_action"], "STUDY")

        self.assertEqual(report["next_step"]["action"], "BRIDGE")
        self.assertEqual(
            report["next_step"]["external_provider"],
            "Mathematics",
        )

    def test_demonstrated_external_prerequisite_clears_execution_blocker(self):
        profile = {
            "profile_id": "PROFILE-SESSION-BRIDGE",
            "provenance": "UNKNOWN",
            "held": {"CAP-SIGNED-PAIR": "DEMONSTRATED"},
            "observation_refs": [],
        }
        report = study_session.plan(
            self.mapping(),
            ["Relative motion=60"],
            profile=profile,
        )
        self.assertTrue(report["valid"], report["findings"])
        self.assertTrue(report["ready"], report["blockers"])
        self.assertEqual(report["blockers"], [])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertEqual(report["next_step"]["action"], "START_HERE")
        self.assertEqual(
            report["next_step"]["capability_ref"],
            "CAP-SAME-TIME",
        )
        route = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(route["CAP-SIGNED-PAIR"]["recommended_action"], "SKIP")

    def test_invalid_optional_estimate_warns_and_keeps_neutral_session(self):
        report = study_session.plan(self.mapping(), ["not-a-subtopic=60"])
        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["valid"])
        self.assertEqual(
            report["execution_disposition"],
            study_session.EXECUTE_WITH_FALLBACK,
        )
        self.assertIn(
            "STUDY_SESSION_ESTIMATE_TARGET_UNKNOWN",
            [row["point"] for row in report["warnings"]],
        )
        self.assertIsNotNone(report["next_step"])

    def test_plan_keeps_academic_warnings_visible_without_blocking_family_pilot(self):
        report = study_session.plan(self.mapping(), ["Relative motion=60"])
        points = {row["point"] for row in report["academic_warnings"]}
        self.assertIn("READINESS_ACADEMIC_REVIEW_PENDING", points)
        self.assertIn("READINESS_SOURCE_QUESTION_COVERAGE_ABSENT", points)
        self.assertTrue(report["passed"])
        self.assertTrue(report["valid"])
        self.assertFalse(report["ready"])

    def test_not_ready_matrix_can_execute_usable_demanded_rungs_with_fallback(self):
        partial = {
            "subject": "Physics",
            "matrix_id": "MATRIX-PHY-RELATIVE-MOTION",
            "subtopic": "Relative motion",
            "status": session_readiness.NOT_READY,
            "external_bridges": [],
            "support_findings": [],
            "academic_warnings": [],
            "rungs": [
                {"rung": "R3", "state": "READY"},
                {"rung": "R4", "state": "READY"},
                {"rung": "R5", "state": "READY"},
                {"rung": "R99", "state": "BLOCKED"},
            ],
            "passed": False,
        }
        with patch.object(
            study_session.session_readiness,
            "audit",
            return_value=partial,
        ):
            report = study_session.plan(self.mapping(), ["Relative motion=60"])

        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["valid"])
        self.assertFalse(report["ready"])
        self.assertEqual(report["status"], session_readiness.NOT_READY)
        self.assertEqual(
            report["execution_disposition"],
            study_session.EXECUTE_WITH_FALLBACK,
        )
        self.assertIsNotNone(report["next_step"])
        self.assertTrue(report["fallback_reasons"])

    def test_blocked_demanded_rungs_require_owner_decision_not_global_failure(self):
        blocked = {
            "subject": "Physics",
            "matrix_id": "MATRIX-PHY-RELATIVE-MOTION",
            "subtopic": "Relative motion",
            "status": session_readiness.NOT_READY,
            "external_bridges": [],
            "support_findings": [],
            "academic_warnings": [],
            "rungs": [
                {"rung": "R3", "state": "BLOCKED"},
                {"rung": "R4", "state": "BLOCKED"},
                {"rung": "R5", "state": "BLOCKED"},
            ],
            "passed": False,
        }
        profile = {
            "profile_id": "PROFILE-OWNER-DECISION",
            "provenance": "UNKNOWN",
            "held": {"CAP-SIGNED-PAIR": "DEMONSTRATED"},
            "observation_refs": [],
        }
        with patch.object(
            study_session.session_readiness,
            "audit",
            return_value=blocked,
        ):
            report = study_session.plan(
                self.mapping(),
                ["Relative motion=60"],
                profile=profile,
            )

        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["valid"])
        self.assertFalse(report["ready"])
        self.assertEqual(
            report["execution_disposition"],
            study_session.OWNER_DECISION,
        )
        self.assertIsNone(report["next_step"])
        self.assertTrue(report["owner_decisions"])

    def test_owner_decision_propagates_to_dependents_but_not_unrelated_branch(self):
        synthetic_plan = {
            "worksheet_id": "SYNTHETIC-FALLBACK",
            "subject": "Physics",
            "profile_id": None,
            "findings": [],
            "warnings": [],
            "blockers": [],
            "valid": True,
            "ready": True,
            "questions": [
                {
                    "question_id": "Q-BLOCKED-BRANCH",
                    "primary_capability_ref": "CAP-B",
                    "secondary_capability_refs": [],
                },
                {
                    "question_id": "Q-INDEPENDENT",
                    "primary_capability_ref": "CAP-C",
                    "secondary_capability_refs": [],
                },
            ],
            "route": [
                {
                    "order": 1,
                    "capability_ref": "CAP-A",
                    "depends_on": [],
                    "state": "RESOLVED",
                    "delivery_state": "LOCAL",
                    "recommended_action": "STUDY",
                    "action_reason": "prerequisite",
                    "locations": [{"matrix_id": "M-A", "rung": "R1"}],
                    "lessons": [],
                },
                {
                    "order": 2,
                    "capability_ref": "CAP-B",
                    "depends_on": ["CAP-A"],
                    "state": "RESOLVED",
                    "delivery_state": "LOCAL",
                    "recommended_action": "STUDY",
                    "action_reason": "question demand",
                    "locations": [{"matrix_id": "M-B", "rung": "R1"}],
                    "lessons": [],
                },
                {
                    "order": 3,
                    "capability_ref": "CAP-C",
                    "depends_on": [],
                    "state": "RESOLVED",
                    "delivery_state": "LOCAL",
                    "recommended_action": "STUDY",
                    "action_reason": "independent question demand",
                    "locations": [{"matrix_id": "M-C", "rung": "R1"}],
                    "lessons": [],
                },
            ],
        }

        readiness = {
            "M-A": {
                "matrix_id": "M-A",
                "subtopic": "A",
                "status": session_readiness.NOT_READY,
                "rungs": [{"rung": "R1", "state": "BLOCKED"}],
                "external_bridges": [],
                "support_findings": [],
                "academic_warnings": [],
            },
            "M-B": {
                "matrix_id": "M-B",
                "subtopic": "B",
                "status": session_readiness.READY,
                "rungs": [{"rung": "R1", "state": "READY"}],
                "external_bridges": [],
                "support_findings": [],
                "academic_warnings": [],
            },
            "M-C": {
                "matrix_id": "M-C",
                "subtopic": "C",
                "status": session_readiness.READY,
                "rungs": [{"rung": "R1", "state": "READY"}],
                "external_bridges": [],
                "support_findings": [],
                "academic_warnings": [],
            },
        }

        def audit(_subject, matrix_id=None, **_kwargs):
            return readiness[matrix_id]

        with patch.object(
            study_session.worksheet_study_plan,
            "resolve",
            return_value=synthetic_plan,
        ), patch.object(
            study_session.session_readiness,
            "audit",
            side_effect=audit,
        ):
            report = study_session.plan(self.mapping())

        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(
            report["execution_disposition"],
            study_session.EXECUTE_WITH_FALLBACK,
        )
        route = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(
            route["CAP-A"]["execution_disposition"],
            study_session.OWNER_DECISION,
        )
        self.assertEqual(
            route["CAP-B"]["execution_disposition"],
            study_session.OWNER_DECISION,
        )
        self.assertIsNone(route["CAP-C"]["execution_disposition"])
        self.assertEqual(report["next_step"]["capability_ref"], "CAP-C")
        self.assertEqual(report["executable_question_ids"], ["Q-INDEPENDENT"])
        self.assertEqual(
            report["owner_decision_question_ids"],
            ["Q-BLOCKED-BRANCH"],
        )

    def test_wrong_external_question_diagnoses_without_inventing_a_hint(self):
        report = study_session.attempt(
            self.mapping(),
            "SCHOOL-REL-Q1",
            result="INCORRECT",
            when="2026-09-18",
            failed_capability_ref="CAP-RELATIVE-V",
            error_stage="CONCEPT",
            response_summary="Subtracted the speeds as scalars and ignored direction.",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["question_origin"], "WORKSHEET_MAPPING")
        self.assertEqual(report["next_action"], "DIAGNOSE")
        self.assertNotIn("hint", report)
        self.assertEqual(report["observation_draft"]["result"], "MISSING")
        self.assertEqual(report["observation_draft"]["question_ref"], "SCHOOL-REL-Q1")
        self.assertEqual(report["review"]["next_review"], "2026-09-19")
        self.assertEqual(report["persistence"], "NOT_WRITTEN")
        prompts = [
            diagnostic["diagnostic_prompt"]
            for option in report["diagnostic_options"]
            for diagnostic in option["diagnostics"]
        ]
        self.assertTrue(prompts)

    def test_local_failure_can_be_repaired_when_an_unfailed_secondary_is_external(self):
        mapping = self.mapping()
        mapping["questions"][0]["secondary_capability_refs"].append(
            "CAP-RIGHT-TRIANGLE"
        )
        report = study_session.attempt(
            mapping,
            "SCHOOL-REL-Q1",
            result="INCORRECT",
            when="2026-09-18",
            failed_capability_ref="CAP-RELATIVE-V",
            error_stage="CONCEPT",
            response_summary="Relative-velocity setup failed before the magnitude step.",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["next_action"], "DIAGNOSE")
        self.assertEqual(
            [row["capability_ref"] for row in report["external_bridges"]],
            ["CAP-RIGHT-TRIANGLE"],
        )

    def test_explicit_failure_on_external_secondary_still_blocks_local_repair(self):
        mapping = self.mapping()
        mapping["questions"][0]["secondary_capability_refs"].append(
            "CAP-RIGHT-TRIANGLE"
        )
        report = study_session.attempt(
            mapping,
            "SCHOOL-REL-Q1",
            result="INCORRECT",
            when="2026-09-18",
            failed_capability_ref="CAP-RIGHT-TRIANGLE",
            error_stage="EXECUTION",
            response_summary="Relative velocity was set up, but the right-triangle magnitude failed.",
        )
        self.assertTrue(report["passed"])
        self.assertEqual(report["next_action"], study_session.OWNER_DECISION)
        self.assertEqual(
            report["execution_disposition"],
            study_session.OWNER_DECISION,
        )
        self.assertIn(
            "STUDY_SESSION_QUESTION_EXTERNAL_ONLY",
            [row["point"] for row in report["findings"]],
        )

    def test_unattributed_wrong_attempt_with_external_secondary_requires_attribution(self):
        mapping = self.mapping()
        mapping["questions"][0]["secondary_capability_refs"].append(
            "CAP-RIGHT-TRIANGLE"
        )
        report = study_session.attempt(
            mapping,
            "SCHOOL-REL-Q1",
            result="INCORRECT",
            when="2026-09-18",
            error_stage="UNKNOWN",
            response_summary="Final answer was wrong; failure point is not yet known.",
        )
        self.assertTrue(report["passed"])
        self.assertEqual(report["next_action"], study_session.OWNER_DECISION)
        self.assertEqual(
            report["execution_disposition"],
            study_session.OWNER_DECISION,
        )
        self.assertIn(
            "STUDY_SESSION_QUESTION_EXTERNAL_ONLY",
            [row["point"] for row in report["findings"]],
        )

    def test_confirmed_misconception_repairs_then_uses_fresh_canonical_check(self):
        report = study_session.attempt(
            self.mapping(),
            "SCHOOL-REL-Q1",
            result="INCORRECT",
            when="2026-09-18",
            failed_capability_ref="CAP-RELATIVE-V",
            error_stage="CONCEPT",
            misconception_index=0,
            response_summary="Used scalar speed difference.",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["next_action"], "REPAIR")
        self.assertEqual(report["repair"]["kind"], "MISCONCEPTION_REPAIR")
        self.assertEqual(report["repair"]["microtopic_ref"], "MIC-COMMON-INTERVAL")
        self.assertEqual(report["after_repair"]["next_action"], "VERIFY")
        verification = report["after_repair"]["verification"]
        self.assertEqual(verification["kind"], "QUESTION")
        self.assertEqual(verification["question_ref"], "Q-AUTHOR-REL-01")
        self.assertNotEqual(verification["question_ref"], "SCHOOL-REL-Q1")

    def test_independent_correct_attempt_drafts_evidence_and_review_without_writing(self):
        report = study_session.attempt(
            self.mapping(),
            "SCHOOL-REL-Q1",
            result="CORRECT",
            when="2026-09-18",
            error_stage="UNKNOWN",
            help_used="NONE",
            response_summary="Set observer order, subtracted vectors, checked reversal.",
        )
        self.assertEqual(report["next_action"], "CONTINUE")
        self.assertEqual(report["observation_draft"]["result"], "DEMONSTRATED")
        self.assertEqual(report["observation_draft"]["capability_ref"], "CAP-RELATIVE-V")
        self.assertEqual(report["review"]["next_review"], "2026-09-25")
        self.assertEqual(report["persistence"], "NOT_WRITTEN")

    def test_question_not_in_supplied_worksheet_is_refused(self):
        report = study_session.attempt(
            self.mapping(),
            "NOT-IN-WORKSHEET",
            result="INCORRECT",
            when="2026-09-18",
        )
        self.assertFalse(report["passed"])
        self.assertEqual(report["next_action"], "STOP")
        self.assertEqual(
            report["findings"][0]["point"],
            "STUDY_SESSION_QUESTION_NOT_IN_WORKSHEET",
        )

    def test_readable_plan_is_parent_oriented_not_raw_json(self):
        report = study_session.plan(self.mapping(), ["Relative motion=60"])
        rendered = study_session.readable_plan(report)
        self.assertIn("Study session", rendered)
        self.assertIn("Subtopic readiness", rendered)
        self.assertIn("Start now", rendered)
        self.assertIn("Ordered study route", rendered)
        self.assertIn("Worksheet questions", rendered)
        self.assertIn("Parent warnings", rendered)
        self.assertIn("External bridge: Mathematics", rendered)


if __name__ == "__main__":
    unittest.main()
