"""Smoke tests for the combined core self-study stack + Issue #19 subject content.

These are interface tests, not the C6 real-worksheet pilot. They deliberately use the
repository's synthetic worksheet-map fixtures only to prove that the independently-built
core and subject workstreams agree on ids, matrices and routing semantics.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import capability_graph, feedback, resolve_request  # noqa: E402
from Shared.tools import (  # noqa: E402
    study_map,
    study_route,
    study_scope_audit,
    study_start,
    worksheet_study_plan,
)


class CoreIssue19Integration(unittest.TestCase):
    MATH = REPO / "tests/fixtures/study_route/mathematics-cross-matrix.worksheet.json"
    PHYSICS = REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json"

    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_math_fixture_now_resolves_through_issue19_matrix(self):
        report = study_map.resolve(self.load(self.MATH))
        self.assertTrue(report["passed"], report["findings"])
        question = report["questions"][0]
        by_role = {row["role"]: row for row in question["capabilities"]}
        self.assertEqual(
            by_role["PRIMARY"]["locations"][0]["matrix_id"],
            "MATRIX-MATH-LINEAR-EQUATIONS",
        )
        self.assertEqual(by_role["PRIMARY"]["locations"][0]["rung"], "R2")
        self.assertEqual(by_role["SECONDARY"]["locations"][0]["rung"], "R1")

    def test_math_route_comes_from_capability_prerequisites_not_positions(self):
        report = study_route.resolve(self.load(self.MATH))
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(
            [row["capability_ref"] for row in report["route"]],
            ["CAP-MATH-SUBSTITUTE", "CAP-MATH-ISOLATE"],
        )

    def test_physics_fixture_still_passes_after_issue19_content_expansion(self):
        report = study_scope_audit.audit(self.load(self.PHYSICS))
        self.assertTrue(report["passed"], report["findings"])

    def test_owner_estimate_uses_new_math_matrix_as_a_real_start_coordinate(self):
        board = resolve_request.ladder("Mathematics", "BUCKET-LINEAR-EQUATION")
        self.assertIsNotNone(board)
        rows = sorted(board["rungs"], key=lambda row: row["ladder_position"])
        caps, mics = capability_graph.subject_graph("Mathematics")
        entry = resolve_request.resolve_owner_estimate(rows, 75, caps, mics)
        self.assertEqual(entry["rung"], "R2")
        self.assertEqual(entry["selected_position"], 60)
        self.assertEqual(entry["prerequisite_checks"], ["CAP-MATH-SUBSTITUTE"])

    def test_subtopic_estimate_overlay_uses_the_issue19_math_matrix(self):
        report = study_start.resolve(self.load(self.MATH), [{
            "matrix_id": "MATRIX-MATH-LINEAR-EQUATIONS",
            "knowledge_percentage": 75,
        }])
        self.assertTrue(report["passed"], report["findings"])
        rows = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(
            rows["CAP-MATH-SUBSTITUTE"]["learner_action"],
            "QUICK_CHECK",
        )
        self.assertEqual(
            rows["CAP-MATH-ISOLATE"]["learner_action"],
            "START_HERE",
        )
        decision = report["start_decisions"][0]
        self.assertEqual(decision["selected_rung"], "R2")
        self.assertEqual(decision["selected_position"], 60)

    def test_noncanonical_math_worksheet_question_can_enter_feedback_runtime(self):
        mapping = self.load(self.MATH)
        row = mapping["questions"][0]
        report = feedback.run({
            "subject": "Mathematics",
            "question_ref": row["question_id"],
            "worksheet_question": row,
            "attempt_number": 1,
            "attempted_question_refs": [row["question_id"]],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": mapping["worksheet_id"],
            "response_summary": "Solved the equation independently.",
            "evaluation": {
                "result": "CORRECT",
                "error_stage": "UNKNOWN",
            },
        })
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["question_origin"], "WORKSHEET_MAPPING")
        self.assertEqual(report["next_action"], "CONTINUE")
        self.assertEqual(
            report["observation_draft"]["capability_ref"],
            "CAP-MATH-ISOLATE",
        )
        self.assertEqual(report["review"]["next_review"], "2026-09-25")

    def test_physics_learner_facing_plan_uses_minimal_issue19_machine_route(self):
        mapping = {
            "worksheet_id": "PHYSICS-MACHINE-INTEGRATION",
            "subject": "Physics",
            "source_note": "Integration-only transient worksheet mapping.",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-MACHINE-MA",
                "secondary_capability_refs": [],
                "mapping_basis": "MANUAL",
            }],
        }
        report = worksheet_study_plan.resolve(mapping)
        self.assertTrue(report["passed"], report["findings"])

        capabilities = [row["capability_ref"] for row in report["route"]]
        self.assertEqual(
            capabilities,
            [
                "CAP-WEP-WORK-DIRECTION",
                "CAP-MACHINE-TRADEOFF",
                "CAP-MACHINE-MA",
            ],
        )
        self.assertNotIn("CAP-WEP-ENERGY-DERIVATIONS", capabilities)
        self.assertNotIn("CAP-NLM-SECOND-LAW", capabilities)
        self.assertNotIn("CAP-KIN-CONSTANT-ACCELERATION", capabilities)

        question = report["questions"][0]
        self.assertEqual(question["primary_capability_ref"], "CAP-MACHINE-MA")
        self.assertNotEqual(question["core_lesson"], "UNRESOLVED")
        self.assertEqual(question["learner_state"], "UNOBSERVED")
        self.assertIn("first attempt", question["why_extra_attention"])

        rendered = worksheet_study_plan.readable(report)
        self.assertIn("Question -> study map", rendered)
        self.assertIn("CAP-MACHINE-MA", rendered)


if __name__ == "__main__":
    unittest.main()
