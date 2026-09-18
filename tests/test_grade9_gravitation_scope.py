"""Grade-9 Gravitation fills only the current competency slice."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness  # noqa: E402


class Grade9GravitationScope(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(
            (REPO / "Physics/library/phy-grav-universal-law.v1.json").read_text(encoding="utf-8")
        )
        self.matrix = json.loads(
            (REPO / "Physics/matrices/phy-grav-universal-law.rungs.json").read_text(encoding="utf-8")
        )
        self.capabilities = {row["id"]: row for row in self.package["capabilities"]}
        self.microtopics = {row["id"]: row for row in self.package["microtopics"]}
        self.bucket = next(
            row for row in self.package["buckets"]
            if row["id"] == "BUCKET-PHY-GRAV-UNIVERSAL-LAW"
        )

    def test_grade9_core_gaps_now_have_distinct_canonical_ownership(self):
        expected = {
            "R2": ("MIC-PHY-GRAV-INVERSE-SQUARE", "CAP-PHY-GRAV-INVERSE-SQUARE"),
            "R3": ("MIC-PHY-GRAV-FREE-FALL-G", "CAP-PHY-GRAV-FREE-FALL-G"),
            "R3W": ("MIC-PHY-GRAV-MASS-WEIGHT", "CAP-PHY-GRAV-MASS-WEIGHT"),
        }
        rows = {row["rung"]: row for row in self.matrix["rungs"]}
        for rung, (mic_ref, cap_ref) in expected.items():
            self.assertEqual(rows[rung]["microtopic_ref"], mic_ref)
            self.assertIn(mic_ref, self.microtopics)
            self.assertEqual(self.microtopics[mic_ref]["primary_capability_ref"], cap_ref)
            self.assertIn(cap_ref, self.capabilities)

    def test_free_fall_uses_only_the_actual_newton_second_law_dependency(self):
        self.assertEqual(
            self.capabilities["CAP-PHY-GRAV-FREE-FALL-G"]["prerequisite_refs"],
            ["CAP-PHY-GRAV-INVERSE-SQUARE", "CAP-NLM-SECOND-LAW"],
        )
        self.assertEqual(self.bucket["prerequisite_refs"], [])

    def test_mass_weight_is_separate_from_free_fall_mass_independence(self):
        self.assertEqual(
            self.capabilities["CAP-PHY-GRAV-MASS-WEIGHT"]["prerequisite_refs"],
            ["CAP-PHY-GRAV-FREE-FALL-G"],
        )
        self.assertNotEqual(
            self.microtopics["MIC-PHY-GRAV-MASS-WEIGHT"]["primary_capability_ref"],
            self.microtopics["MIC-PHY-GRAV-FREE-FALL-G"]["primary_capability_ref"],
        )

    def test_existing_energy_and_orbit_records_are_retained_not_expanded(self):
        refs = {row["microtopic_ref"] for row in self.matrix["rungs"] if row.get("microtopic_ref")}
        self.assertIn("MIC-PHY-GRAV-R4", refs)
        self.assertIn("MIC-PHY-GRAV-R5", refs)
        self.assertEqual(self.capabilities["CAP-PHY-GRAV-R4"]["version"], "0.1.0")
        self.assertEqual(self.capabilities["CAP-PHY-GRAV-R5"]["version"], "0.1.0")

    def test_matrix_is_self_study_ready_after_grade9_core_completion(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-GRAV-UNIVERSAL-LAW",
        )
        self.assertEqual(report["status"], session_readiness.READY)
        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(all(row["core1a"] and row["core1b"] for row in report["rungs"]))

    def test_scope_pass_does_not_promote_curriculum_authority_or_add_grade_field(self):
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"], [])
        self.assertEqual(self.bucket["curriculum_mappings"], [])
        forbidden = {"grade", "grade_level", "class", "syllabus_status"}
        self.assertFalse(forbidden & set(self.matrix))

    def test_donor_adaptation_is_local_and_preserves_key_force_field_invariants(self):
        # No runtime/source dependency on the prior donor repository is retained.
        serialized = json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common", serialized)
        self.assertNotIn("github.com", serialized)

        r1 = self.microtopics["MIC-PHY-GRAV-R1"]
        r2 = self.microtopics["MIC-PHY-GRAV-INVERSE-SQUARE"]
        r3 = self.microtopics["MIC-PHY-GRAV-FREE-FALL-G"]

        r1_text = json.dumps(r1).lower()
        self.assertIn("supported", r1_text)
        self.assertIn("velocity", r1_text)
        self.assertIn("different bodies", r1_text)

        r2_text = json.dumps(r2).lower()
        self.assertIn("centre-to-centre", r2_text)
        self.assertIn("external spherical", r2_text)
        self.assertIn("inverse-square", r2_text)

        r3_text = json.dumps(r3).lower()
        self.assertIn("force per unit", r3_text)
        self.assertIn("test mass", r3_text)
        self.assertIn("9.8", r3_text)
        self.assertIn("m/r^2", r3_text)

    def test_advanced_field_superposition_was_not_pulled_into_grade9_core(self):
        learner_facing = []
        for ref in [
            "MIC-PHY-GRAV-R1",
            "MIC-PHY-GRAV-INVERSE-SQUARE",
            "MIC-PHY-GRAV-FREE-FALL-G",
            "MIC-PHY-GRAV-MASS-WEIGHT",
        ]:
            row = self.microtopics[ref]
            learner_facing.append(
                {
                    "inferential_jump": row["inferential_jump"],
                    "teaching_path": row["teaching_path"],
                    "misconceptions": row["misconceptions"],
                    "exit_task": row["exit_task"],
                    "elicitation": row["elicitation"],
                }
            )
        core = json.dumps(learner_facing).lower()
        self.assertNotIn("g_net", core)
        self.assertNotIn("vector superposition", core)


if __name__ == "__main__":
    unittest.main()
