"""Real-question pilot for the owner-supplied ExamSIDE Motion in a Plane bank."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import worksheet_study_plan  # noqa: E402


class ExamSideMotionInPlanePilot(unittest.TestCase):
    FIXTURE = REPO / "tests/fixtures/real_pilots/examside-motion-in-plane.worksheet.json"

    def mapping(self):
        return json.loads(self.FIXTURE.read_text(encoding="utf-8"))

    def test_real_question_slice_maps_without_promoting_questions_to_canonical_truth(self):
        mapping = self.mapping()
        report = worksheet_study_plan.resolve(mapping)
        self.assertEqual(len(report["questions"]), 3)

        for source_row, resolved in zip(mapping["questions"], report["questions"]):
            self.assertEqual(source_row["mapping_basis"], "AGENT_PROPOSAL")
            self.assertNotIn("canonical_question_ref", source_row)
            self.assertNotEqual(resolved["core_lesson"], "UNRESOLVED")
            self.assertEqual(resolved["learner_state"], "UNOBSERVED")

    def test_real_slice_exercises_more_than_one_canonical_matrix(self):
        report = worksheet_study_plan.resolve(self.mapping())
        matrices = {
            lesson["matrix_id"]
            for row in report["route"]
            for lesson in row.get("lessons", [])
        }
        self.assertIn("MATRIX-PHY-RELATIVE-MOTION", matrices)
        self.assertIn("MATRIX-PHY-NLM-FIRST-LAW", matrices)

    def test_real_slice_exposes_external_prerequisite_without_fabricating_teaching(self):
        report = worksheet_study_plan.resolve(self.mapping())
        self.assertFalse(report["passed"])
        gaps = [
            row for row in report["findings"]
            if row.get("point") == "STUDY_ROUTE_CAPABILITY_HAS_NO_TEACHING_LOCATION"
        ]
        self.assertEqual(
            [row["capability"] for row in gaps],
            ["CAP-SIGNED-PAIR"],
        )

    def test_relative_motion_demand_keeps_reference_frame_support_explicit(self):
        report = worksheet_study_plan.resolve(self.mapping())
        by_cap = {row["capability_ref"]: row for row in report["route"]}
        self.assertIn("CAP-RELATIVE-V", by_cap)
        self.assertIn("CAP-VECTOR-CHECK", by_cap)
        self.assertIn("CAP-NLM-FRAME-CHOICE", by_cap)
        self.assertIn("CAP-NLM-FBD-BODY-OWNERSHIP", by_cap)
        self.assertLess(
            by_cap["CAP-NLM-FBD-BODY-OWNERSHIP"]["order"],
            by_cap["CAP-NLM-FRAME-CHOICE"]["order"],
        )

    def test_first_use_is_diagnostic_without_inventing_weakness(self):
        report = worksheet_study_plan.resolve(self.mapping())
        self.assertEqual(
            {row["learner_state"] for row in report["questions"]},
            {"UNOBSERVED"},
        )
        self.assertTrue(all(
            "first attempt" in row["why_extra_attention"]
            for row in report["questions"]
        ))


if __name__ == "__main__":
    unittest.main()
