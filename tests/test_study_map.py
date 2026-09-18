"""Worksheet-to-capability mapping: transient demand resolves to canonical teaching."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import study_map  # noqa: E402


class WorksheetStudyMap(unittest.TestCase):
    PHYSICS = REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json"
    MATH = REPO / "tests/fixtures/study_route/mathematics-cross-matrix.worksheet.json"

    def physics(self):
        return json.loads(self.PHYSICS.read_text(encoding="utf-8"))

    def test_realistic_physics_fixture_maps_across_existing_matrices(self):
        report = study_map.resolve(self.physics())
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(len(report["questions"]), 3)

        first = report["questions"][0]
        primary = next(row for row in first["capabilities"] if row["role"] == "PRIMARY")
        secondary = next(row for row in first["capabilities"] if row["role"] == "SECONDARY")
        self.assertEqual(primary["capability_ref"], "CAP-KIN-ZERO-V-NONZERO-A")
        self.assertEqual(primary["locations"][0]["matrix_id"], "MATRIX-PHY-KIN-1D-MOTION")
        self.assertEqual(primary["locations"][0]["rung"], "R3")
        self.assertEqual(secondary["capability_ref"], "CAP-KIN-DISTANCE-DISPLACEMENT")
        self.assertEqual(secondary["locations"][0]["rung"], "R1")

        matrices = {
            row["locations"][0]["matrix_id"]
            for question in report["questions"]
            for row in question["capabilities"]
        }
        self.assertGreaterEqual(len(matrices), 3)

    def test_an_arbitrary_worksheet_question_need_not_be_a_canonical_question(self):
        mapping = self.physics()
        mapping["questions"] = [{
            "question_id": "SCHOOL-WORKSHEET-Q999",
            "primary_capability_ref": "CAP-KIN-ZERO-V-NONZERO-A",
            "secondary_capability_refs": [],
            "mapping_basis": "MANUAL",
        }]
        report = study_map.resolve(mapping)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["questions"][0]["question_id"], "SCHOOL-WORKSHEET-Q999")

    def test_unknown_capability_is_reported_not_invented(self):
        mapping = self.physics()
        mapping["questions"][0]["primary_capability_ref"] = "CAP-DOES-NOT-EXIST"
        report = study_map.resolve(mapping)
        self.assertFalse(report["passed"])
        points = [row["point"] for row in report["findings"]]
        self.assertIn(study_map.UNKNOWN_CAPABILITY, points)
        primary = report["questions"][0]["capabilities"][0]
        self.assertEqual(primary["state"], "UNKNOWN")
        self.assertEqual(primary["locations"], [])

    def test_existing_capability_without_a_matrix_is_an_explicit_gap(self):
        mapping = json.loads(self.MATH.read_text(encoding="utf-8"))
        report = study_map.resolve(mapping)
        self.assertFalse(report["passed"])
        points = [row["point"] for row in report["findings"]]
        self.assertIn(study_map.NO_TEACHING_LOCATION, points)
        self.assertNotIn(study_map.UNKNOWN_CAPABILITY, points)

    def test_secondary_capability_is_not_expanded_into_prerequisites_here(self):
        report = study_map.resolve(self.physics())
        first = report["questions"][0]
        self.assertEqual(
            first["secondary_capability_refs"],
            ["CAP-KIN-DISTANCE-DISPLACEMENT"],
        )
        self.assertNotIn("prerequisites", first)
        self.assertNotIn("prerequisite_closure", first)

    def test_primary_may_not_be_repeated_as_secondary(self):
        mapping = self.physics()
        first = mapping["questions"][0]
        first["secondary_capability_refs"] = [first["primary_capability_ref"]]
        report = study_map.resolve(mapping)
        self.assertFalse(report["passed"])
        self.assertIn(
            "WORKSHEET_PRIMARY_REPEATED_AS_SECONDARY",
            [row["point"] for row in report["findings"]],
        )

    def test_canonical_mapping_detects_drift_from_the_canonical_question(self):
        mapping = self.physics()
        mapping["questions"] = [{
            "question_id": "COPY-OF-CANONICAL-Q",
            "primary_capability_ref": "CAP-MEASURED-FROM",
            "secondary_capability_refs": [],
            "mapping_basis": "CANONICAL_QUESTION",
            "canonical_question_ref": "Q-AUTHOR-REL-01",
        }]
        report = study_map.resolve(mapping)
        self.assertFalse(report["passed"])
        self.assertIn(
            "WORKSHEET_CANONICAL_MAPPING_DRIFT",
            [row["point"] for row in report["findings"]],
        )

    def test_duplicate_question_ids_are_refused(self):
        mapping = self.physics()
        mapping["questions"].append(copy.deepcopy(mapping["questions"][0]))
        report = study_map.resolve(mapping)
        self.assertFalse(report["passed"])
        self.assertIn(
            "WORKSHEET_QUESTION_ID_DUPLICATE",
            [row["point"] for row in report["findings"]],
        )

    def test_schema_refuses_learner_state_in_a_worksheet_map(self):
        mapping = self.physics()
        mapping["questions"][0]["learner_state"] = "MISSING"
        findings = study_map.validate_mapping(mapping)
        self.assertIn("WORKSHEET_MAP_STRUCTURE", [row["point"] for row in findings])


if __name__ == "__main__":
    unittest.main()
