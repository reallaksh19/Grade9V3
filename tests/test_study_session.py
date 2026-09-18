"""Thin study-session runner uses only readiness-audited existing content."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_session  # noqa: E402


class StudySession(unittest.TestCase):
    SUBJECT = "Physics"
    MATRIX = "MATRIX-PHY-RELATIVE-MOTION"

    def bridge_profile(self, **held):
        return {
            "profile_id": "PROFILE-SESSION-PILOT",
            "provenance": "UNKNOWN",
            "held": {
                "CAP-SIGNED-PAIR": "DEMONSTRATED",
                **held,
            },
            "observation_refs": [],
        }

    def test_relative_motion_starts_at_explicit_bridge_without_evidence(self):
        report = study_session.start(self.SUBJECT, self.MATRIX)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(
            report["readiness_status"],
            session_readiness.READY_WITH_BRIDGE,
        )
        self.assertEqual(
            report["session_state"],
            study_session.SESSION_AWAITING_BRIDGE,
        )
        action = report["next_action"]
        self.assertEqual(action["type"], "BRIDGE")
        self.assertEqual(action["capability_ref"], "CAP-SIGNED-PAIR")
        self.assertEqual(action["external_provider"], "Mathematics")
        self.assertEqual(
            action["acceptance_status"],
            "PROVIDER_REVIEW_REQUIRED",
        )
        self.assertFalse(action["satisfied"])

    def test_demonstrated_bridge_starts_r1_with_no_help_attempt(self):
        report = study_session.start(
            self.SUBJECT,
            self.MATRIX,
            profile=self.bridge_profile(),
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["session_state"], study_session.SESSION_IN_PROGRESS)
        self.assertEqual(report["bridges"][0]["type"], "SKIP")

        action = report["next_action"]
        self.assertEqual(action["type"], "ATTEMPT")
        self.assertEqual(action["rung"], "R1")
        self.assertEqual(action["microtopic_ref"], "MIC-MEASURED-FROM")
        self.assertEqual(action["learner_state"]["state"], "UNOBSERVED")
        self.assertTrue(action["verification"]["prompt"])
        self.assertNotIn("answer", action["verification"])
        self.assertNotIn("oracle", action["verification"])
        self.assertIn("without help first", action["reason"])

    def test_missing_capability_teaches_before_exit_attempt(self):
        report = study_session.start(
            self.SUBJECT,
            self.MATRIX,
            profile=self.bridge_profile(**{"CAP-MEASURED-FROM": "MISSING"}),
        )
        action = report["next_action"]
        self.assertEqual(action["type"], "TEACH")
        self.assertEqual(action["rung"], "R1")
        self.assertTrue(action["teaching_path"])
        self.assertEqual(action["after"], "ATTEMPT_EXIT_TASK")
        self.assertTrue(action["verification"]["prompt"])

    def test_uncertain_capability_reconstructs_before_exit_attempt(self):
        report = study_session.start(
            self.SUBJECT,
            self.MATRIX,
            profile=self.bridge_profile(**{"CAP-MEASURED-FROM": "UNCERTAIN"}),
        )
        action = report["next_action"]
        self.assertEqual(action["type"], "RECONSTRUCT")
        self.assertTrue(action["predict"])
        self.assertTrue(action["attempt"])
        self.assertTrue(action["reconstruct"])
        self.assertTrue(action["boundary_test"])
        self.assertNotIn("defensible_answer", action["predict"])
        self.assertNotIn("accepted", action["attempt"])
        self.assertNotIn("rejected", action["attempt"])
        self.assertNotIn("answer", action["boundary_test"])
        self.assertNotIn("confirms", action["boundary_test"])
        self.assertTrue(all(
            set(row) == {"ask"}
            for row in action["reconstruct"]["route"]
        ))
        self.assertNotIn("answer", action["verification"])
        self.assertEqual(action["after"], "ATTEMPT_EXIT_TASK")

    def test_demonstrated_local_capability_gets_quick_check_not_reteach(self):
        report = study_session.start(
            self.SUBJECT,
            self.MATRIX,
            profile=self.bridge_profile(**{"CAP-MEASURED-FROM": "DEMONSTRATED"}),
        )
        action = report["next_action"]
        self.assertEqual(action["type"], "QUICK_CHECK")
        self.assertTrue(action["verification"]["prompt"])
        self.assertNotIn("teaching_path", action)

    def test_correct_independent_exit_attempt_advances_to_next_rung(self):
        report = study_session.run({
            "command": "ATTEMPT",
            "subject": self.SUBJECT,
            "matrix_id": self.MATRIX,
            "microtopic_ref": "MIC-MEASURED-FROM",
            "attempt_number": 1,
            "attempted_question_refs": [],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": "SESSION-REL-1",
            "response_summary": "The number is incomplete unless the reference is named.",
            "evaluation": {
                "result": "CORRECT",
                "error_stage": "UNKNOWN",
            },
        }, profile=self.bridge_profile())

        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["feedback"]["next_action"], "CONTINUE")
        self.assertEqual(
            report["feedback"]["observation_draft"]["capability_ref"],
            "CAP-MEASURED-FROM",
        )
        self.assertEqual(
            report["feedback"]["review"]["next_review"],
            "2026-09-25",
        )
        action = report["next_action"]
        self.assertEqual(action["type"], "ATTEMPT")
        self.assertEqual(action["rung"], "R3")
        self.assertEqual(action["microtopic_ref"], "MIC-SAME-TIME")

    def test_incorrect_exit_attempt_uses_existing_diagnostic_repair_runtime(self):
        report = study_session.run({
            "command": "ATTEMPT",
            "subject": self.SUBJECT,
            "matrix_id": self.MATRIX,
            "microtopic_ref": "MIC-COMMON-INTERVAL",
            "attempt_number": 1,
            "attempted_question_refs": [],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": "SESSION-REL-2",
            "response_summary": "I subtracted the two speeds and ignored direction.",
            "evaluation": {
                "result": "INCORRECT",
                "failed_capability_ref": "CAP-RELATIVE-V",
                "error_stage": "CONCEPT",
            },
        }, profile=self.bridge_profile())

        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["feedback"]["next_action"], "DIAGNOSE")
        self.assertEqual(report["next_action"]["type"], "DIAGNOSE")
        prompts = [
            diagnostic["diagnostic_prompt"]
            for option in report["next_action"]["diagnostic_options"]
            for diagnostic in option["diagnostics"]
        ]
        self.assertTrue(any("directions" in prompt for prompt in prompts))
        self.assertEqual(
            report["feedback"]["observation_draft"]["result"],
            "MISSING",
        )

    def test_pilot_ready_matrix_is_refused_by_the_thin_runner(self):
        with patch.object(
            study_session.session_readiness,
            "audit",
            return_value={
                "subject": "Example",
                "matrix_id": "MATRIX-EXAMPLE",
                "status": session_readiness.PILOT_READY,
                "findings": [],
                "passed": True,
            },
        ):
            report = study_session.start("Example", "MATRIX-EXAMPLE")

        self.assertFalse(report["passed"])
        self.assertEqual(report["session_state"], study_session.SESSION_STOPPED)
        self.assertEqual(
            report["findings"][0]["point"],
            "STUDY_SESSION_MATRIX_NOT_READY",
        )

    def test_runner_has_no_all_subject_mode_and_requires_one_matrix_per_start(self):
        with patch.object(
            study_session.session_readiness,
            "audit",
            return_value={
                "subject": "Example",
                "matrix_id": None,
                "status": session_readiness.NOT_READY,
                "findings": [],
                "passed": False,
            },
        ):
            report = study_session.start("Example", None)

        self.assertFalse(report["passed"])
        self.assertEqual(report["next_action"]["type"], "STOP")


if __name__ == "__main__":
    unittest.main()
