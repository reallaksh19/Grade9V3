"""Keep architectural regression and real learner acceptance as separate evidence layers."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import empirical_acceptance, feedback, import_study_observations  # noqa: E402


class EmpiricalAcceptanceBoundary(unittest.TestCase):
    def write_observation(self, root: Path, observation: dict) -> None:
        target = root / "Learners/observations"
        target.mkdir(parents=True, exist_ok=True)
        (target / f'{observation["observation_id"]}.json').write_text(
            json.dumps(observation), encoding="utf-8"
        )

    def test_no_real_observations_is_pending_not_a_regression_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = empirical_acceptance.audit(Path(tmp))
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], "PENDING_REAL_EVIDENCE")
        self.assertEqual(report["live_sessions"], [])

    def test_feedback_draft_is_explicitly_unreviewed_not_live_acceptance(self):
        question = {
            "id": "Q-1",
            "primary_capability_ref": "CAP-A",
            "secondary_capability_refs": [],
        }
        draft = feedback.observation_draft({
            "when": "2026-09-18",
            "attempt_number": 1,
            "help_used": "NONE",
            "session_ref": "SESSION-1",
            "response_summary": "Solved independently.",
            "evaluation": {"result": "CORRECT", "error_stage": "UNKNOWN"},
        }, question, None)
        self.assertEqual(draft["provenance"], "UNREVIEWED_SESSION_DRAFT")

    def test_historical_import_is_never_live_acceptance(self):
        rows = import_study_observations.convert({
            "study_map_id": "OLD-MAP",
            "rows": [{
                "capability_ref": "CAP-A",
                "observed": "Prior note.",
                "suggested_state": "UNCERTAIN",
            }],
        }, "2026-09-01")
        self.assertEqual(rows[0]["provenance"], "HISTORICAL_IMPORT")

    def test_committed_direct_attempt_without_provenance_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_observation(root, {
                "observation_id": "OBS-UNCLASSIFIED",
                "capability_ref": "CAP-A",
                "method": "question attempt",
                "evidence_kind": "DIRECT_ATTEMPT",
                "question_ref": "Q-1",
                "session_ref": "SESSION-1",
                "observed": "Attempt exists but its evidence layer is unknown.",
                "result": "UNCERTAIN",
                "when": "2026-09-18",
                "help": "NONE",
                "error_stage": "UNKNOWN",
            })
            report = empirical_acceptance.audit(root)
        self.assertFalse(report["passed"])
        self.assertEqual(report["status"], "INVALID_EMPIRICAL_EVIDENCE")
        self.assertIn(
            "EMPIRICAL_DIRECT_ATTEMPT_PROVENANCE_MISSING",
            [row["point"] for row in report["findings"]],
        )

    def test_synthetic_and_unreviewed_attempts_do_not_satisfy_empirical_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for oid, provenance in [
                ("OBS-SYN", "SYNTHETIC_TEST"),
                ("OBS-DRAFT", "UNREVIEWED_SESSION_DRAFT"),
            ]:
                self.write_observation(root, {
                    "observation_id": oid,
                    "capability_ref": "CAP-A",
                    "method": "question attempt",
                    "evidence_kind": "DIRECT_ATTEMPT",
                    "question_ref": "Q-1",
                    "session_ref": "SESSION-1",
                    "observed": "Synthetic or unreviewed work.",
                    "result": "DEMONSTRATED",
                    "when": "2026-09-18",
                    "help": "NONE",
                    "error_stage": "UNKNOWN",
                    "provenance": provenance,
                })
            report = empirical_acceptance.audit(root)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], "PENDING_REAL_EVIDENCE")
        self.assertEqual(report["live_sessions"], [])

    def test_reviewed_live_attempt_makes_empirical_evidence_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_observation(root, {
                "observation_id": "OBS-LIVE",
                "capability_ref": "CAP-A",
                "method": "question attempt",
                "evidence_kind": "DIRECT_ATTEMPT",
                "question_ref": "Q-1",
                "session_ref": "SESSION-REAL-1",
                "observed": "Learner attempted the question independently.",
                "result": "UNCERTAIN",
                "when": "2026-09-18",
                "help": "NONE",
                "error_stage": "SETUP",
                "provenance": "LIVE_LEARNER",
            })
            report = empirical_acceptance.audit(root)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], "EMPIRICAL_EVIDENCE_AVAILABLE")
        self.assertEqual(report["live_sessions"], ["SESSION-REAL-1"])
        self.assertEqual(report["live_observations"], ["OBS-LIVE"])

    def test_live_attempt_without_session_or_question_is_structurally_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_observation(root, {
                "observation_id": "OBS-BAD-LIVE",
                "capability_ref": "CAP-A",
                "method": "question attempt",
                "evidence_kind": "DIRECT_ATTEMPT",
                "observed": "Real learner work with missing linkage.",
                "result": "UNCERTAIN",
                "when": "2026-09-18",
                "help": "NONE",
                "error_stage": "UNKNOWN",
                "provenance": "LIVE_LEARNER",
            })
            report = empirical_acceptance.audit(root)
        self.assertFalse(report["passed"])
        points = {row["point"] for row in report["findings"]}
        self.assertIn("EMPIRICAL_LIVE_SESSION_REF_MISSING", points)
        self.assertIn("EMPIRICAL_LIVE_QUESTION_REF_MISSING", points)


if __name__ == "__main__":
    unittest.main()
