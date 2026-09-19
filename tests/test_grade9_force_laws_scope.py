"""Grade-9 Force/Laws scope stays narrow while explicit extension demand remains routable."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class Grade9ForceLawsScope(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json").read_text(encoding="utf-8")
        )
        self.matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json").read_text(encoding="utf-8")
        )
        self.capabilities = {row["id"]: row for row in self.package["capabilities"]}
        self.microtopics = {row["id"]: row for row in self.package["microtopics"]}
        self.bucket = next(
            row for row in self.package["buckets"]
            if row["id"] == "BUCKET-PHY-NLM-FIRST-LAW"
        )

    def test_all_matrix_rows_reuse_current_canonical_teaching(self):
        self.assertEqual(len(self.matrix["rungs"]), 11)
        for rung in self.matrix["rungs"]:
            ref = rung.get("microtopic_ref")
            self.assertIn(ref, self.microtopics, rung["rung"])
            cap = self.microtopics[ref]["primary_capability_ref"]
            self.assertIn(cap, self.capabilities, (rung["rung"], ref))

    def test_first_law_does_not_require_the_turning_point_diagnostic(self):
        cap = self.capabilities["CAP-NLM-NET-ZERO-MOTION"]
        mic = self.microtopics["MIC-PHY-NLM-NET-ZERO-MOTION"]
        self.assertEqual(cap["prerequisite_refs"], [])
        self.assertEqual(mic["prerequisite_refs"], [])
        self.assertNotIn(
            "CAP-KIN-ZERO-V-NONZERO-A",
            {
                item
                for step in mic["teaching_path"]
                for item in step.get("inputs", [])
            },
        )

    def test_motion_bucket_sequence_is_retained_without_inventing_capability_dependency(self):
        self.assertEqual(
            self.bucket["prerequisite_refs"],
            ["BUCKET-PHY-KIN-1D-MOTION"],
        )

    def test_frame_choice_remains_canonical_for_explicit_extension_demand(self):
        rung = next(
            row for row in self.matrix["rungs"]
            if row.get("microtopic_ref") == "MIC-PHY-NLM-FRAME-CHOICE"
        )
        self.assertEqual(rung["rung"], "R4")
        self.assertIn("CAP-NLM-FRAME-CHOICE", self.capabilities)
        fixture = json.loads(
            (REPO / "tests/fixtures/real_pilots/examside-motion-in-plane.worksheet.json")
            .read_text(encoding="utf-8")
        )
        question = next(
            row for row in fixture["questions"]
            if row["question_id"] == "EXAMSIDE-MIP-2021-08-26-BOMB"
        )
        self.assertIn("CAP-NLM-FRAME-CHOICE", question["secondary_capability_refs"])

    def test_scope_audit_does_not_promote_curriculum_authority_or_add_grade_field(self):
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"], [])
        self.assertEqual(self.bucket["curriculum_mappings"], [])
        self.assertEqual(
            self.bucket["extensions"].get("issue19:scope_class"),
            "OWNER_EXTENSION",
        )
        forbidden = {"grade", "grade_level", "class", "syllabus_status"}
        self.assertFalse(forbidden & set(self.matrix))


if __name__ == "__main__":
    unittest.main()
