"""Subtopic-wise rough estimates choose practical local start points, not mastery."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import study_start  # noqa: E402


class StudyStartOverlay(unittest.TestCase):
    PHYSICS = REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json"

    def mapping(self):
        return json.loads(self.PHYSICS.read_text(encoding="utf-8"))

    def by_capability(self, report):
        return {row["capability_ref"]: row for row in report["route"]}

    def test_estimates_apply_only_inside_their_local_matrices(self):
        report = study_start.resolve(self.mapping(), [
            {
                "matrix_id": "MATRIX-PHY-KIN-1D-MOTION",
                "knowledge_percentage": 75,
            },
            {
                "matrix_id": "MATRIX-PHY-NLM-FIRST-LAW",
                "knowledge_percentage": 75,
            },
            {
                "matrix_id": "MATRIX-PHY-WORK-ENERGY-POWER",
                "knowledge_percentage": 65,
            },
        ])
        self.assertTrue(report["passed"], report["findings"])
        rows = self.by_capability(report)

        self.assertEqual(rows["CAP-KIN-DISTANCE-DISPLACEMENT"]["learner_action"], "QUICK_CHECK")
        self.assertEqual(rows["CAP-KIN-ZERO-V-NONZERO-A"]["learner_action"], "START_HERE")

        self.assertEqual(rows["CAP-NLM-NET-ZERO-MOTION"]["learner_action"], "QUICK_CHECK")
        self.assertEqual(rows["CAP-NLM-FORCES-SUM-ZERO"]["learner_action"], "QUICK_CHECK")
        self.assertEqual(rows["CAP-NLM-FBD-BODY-OWNERSHIP"]["learner_action"], "START_HERE")

        self.assertEqual(rows["CAP-WEP-WORK-DIRECTION"]["learner_action"], "QUICK_CHECK")
        self.assertEqual(rows["CAP-WEP-NET-WORK-SIGN"]["learner_action"], "QUICK_CHECK")
        self.assertEqual(rows["CAP-WEP-POTENTIAL-ELIGIBILITY"]["learner_action"], "START_HERE")
        self.assertEqual(rows["CAP-WEP-MECH-ENERGY-CONDITION"]["learner_action"], "STUDY")

    def test_quick_check_is_never_written_as_demonstrated_mastery(self):
        report = study_start.resolve(self.mapping(), [{
            "matrix_id": "MATRIX-PHY-NLM-FIRST-LAW",
            "knowledge_percentage": 75,
        }])
        quick = [row for row in report["route"] if row["learner_action"] == "QUICK_CHECK"]
        self.assertTrue(quick)
        rendered = json.dumps(quick)
        self.assertNotIn('"DEMONSTRATED"', rendered)
        for row in quick:
            self.assertTrue(row["estimate_basis"]["not_evidence"])

    def test_no_estimate_means_study_not_guess(self):
        report = study_start.resolve(self.mapping(), [])
        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["route"])
        self.assertEqual(
            {row["learner_action"] for row in report["route"]},
            {"STUDY"},
        )

    def test_estimate_below_first_teaching_point_starts_at_first_teaching_point(self):
        report = study_start.resolve(self.mapping(), [{
            "matrix_id": "MATRIX-PHY-WORK-ENERGY-POWER",
            "knowledge_percentage": 5,
        }])
        self.assertTrue(report["passed"], report["findings"])
        decision = report["start_decisions"][0]
        self.assertEqual(decision["selected_rung"], "R1")
        self.assertEqual(decision["selected_position"], 20)
        rows = self.by_capability(report)
        self.assertEqual(rows["CAP-WEP-WORK-DIRECTION"]["learner_action"], "START_HERE")

    def test_recordless_matrix_rung_is_not_used_as_a_start_coordinate(self):
        # Architecture falsifier, not a snapshot of current Physics content. Build one
        # temporary subject where R2 exists in the matrix but has no canonical teaching
        # microtopic. A 50% estimate must not strand the learner there.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Example/library").mkdir(parents=True)
            (root / "Example/matrices").mkdir(parents=True)
            (root / "Shared/library").mkdir(parents=True)
            (root / "Shared/library/worksheet-map.schema.json").write_text(
                (REPO / "Shared/library/worksheet-map.schema.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (root / "Example/library/example.json").write_text(json.dumps({
                "capabilities": [{
                    "id": "CAP-A",
                    "action": "Do A",
                    "success_criterion": "A is done",
                    "prerequisite_refs": [],
                }],
                "microtopics": [{
                    "id": "MIC-A",
                    "primary_capability_ref": "CAP-A",
                }],
                "questions": [],
            }), encoding="utf-8")
            (root / "Example/matrices/example.rungs.json").write_text(json.dumps({
                "matrix_id": "MATRIX-EXAMPLE",
                "bucket_id": "BUCKET-EXAMPLE",
                "topic": "Example",
                "subtopic": "Example",
                "rungs": [
                    {
                        "rung": "R1",
                        "ladder_position": 20,
                        "microtopic_ref": "MIC-A"
                    },
                    {
                        "rung": "R2",
                        "ladder_position": 45,
                        "microtopic_ref": "MIC-NOT-AUTHORED"
                    }
                ]
            }), encoding="utf-8")
            mapping = {
                "worksheet_id": "EXAMPLE-WORKSHEET",
                "subject": "Example",
                "questions": [{
                    "question_id": "Q1",
                    "primary_capability_ref": "CAP-A",
                    "secondary_capability_refs": [],
                    "mapping_basis": "MANUAL",
                }],
            }
            report = study_start.resolve(mapping, [{
                "matrix_id": "MATRIX-EXAMPLE",
                "knowledge_percentage": 50,
            }], root)

        self.assertTrue(report["passed"], report["findings"])
        decision = report["start_decisions"][0]
        self.assertEqual(decision["selected_rung"], "R1")
        self.assertEqual(decision["selected_position"], 20)

    def test_bucket_id_can_be_used_when_it_identifies_one_matrix(self):
        report = study_start.resolve(self.mapping(), [{
            "bucket_id": "BUCKET-PHY-WORK-ENERGY-POWER",
            "knowledge_percentage": 65,
        }])
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(
            report["start_decisions"][0]["matrix_id"],
            "MATRIX-PHY-WORK-ENERGY-POWER",
        )

    def test_unknown_matrix_is_explicit(self):
        report = study_start.resolve(self.mapping(), [{
            "matrix_id": "MATRIX-NOT-REAL",
            "knowledge_percentage": 50,
        }])
        self.assertFalse(report["passed"])
        self.assertIn(
            "STUDY_START_MATRIX_UNKNOWN",
            [row["point"] for row in report["findings"]],
        )

    def test_out_of_range_estimate_is_refused(self):
        report = study_start.resolve(self.mapping(), [{
            "matrix_id": "MATRIX-PHY-KIN-1D-MOTION",
            "knowledge_percentage": 140,
        }])
        self.assertFalse(report["passed"])
        self.assertIn(
            "STUDY_START_ESTIMATE_OUT_OF_RANGE",
            [row["point"] for row in report["findings"]],
        )

    def test_duplicate_estimate_for_same_matrix_is_refused(self):
        report = study_start.resolve(self.mapping(), [
            {
                "matrix_id": "MATRIX-PHY-KIN-1D-MOTION",
                "knowledge_percentage": 40,
            },
            {
                "matrix_id": "MATRIX-PHY-KIN-1D-MOTION",
                "knowledge_percentage": 70,
            },
        ])
        self.assertFalse(report["passed"])
        self.assertIn(
            "STUDY_START_ESTIMATE_DUPLICATE",
            [row["point"] for row in report["findings"]],
        )


if __name__ == "__main__":
    unittest.main()
