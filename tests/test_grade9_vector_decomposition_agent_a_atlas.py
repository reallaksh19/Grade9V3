"""Agent A semantic Atlas packet for vector decomposition / initial-state representation."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import feedback, session_readiness  # noqa: E402


class Grade9VectorDecompositionAgentAAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-vec-add-sub.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-vec-add-sub.rungs.json").read_text(
                encoding="utf-8"
            )
        )
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.microtopics = {row["id"]: row for row in cls.package["microtopics"]}
        cls.capabilities = {row["id"]: row for row in cls.package["capabilities"]}

    def test_existing_four_capability_spine_is_preserved(self):
        self.assertEqual(
            [row["microtopic_ref"] for row in self.matrix["rungs"]],
            [
                "MIC-PHY-VEC-COMPONENT-SUM",
                "MIC-PHY-VEC-RESULTANT-CONSTRAINT",
                "MIC-PHY-VEC-SUB-ORDER",
                "MIC-PHY-VEC-ANGLE-DECOMPOSITION",
            ],
        )
        self.assertEqual(
            {row["id"] for row in self.package["capabilities"]},
            {
                "CAP-VEC-RESULTANT-CONSTRAINT",
                "CAP-VEC-COMPONENT-SUM",
                "CAP-VEC-SUB-ORDER",
                "CAP-VEC-ANGLE-DECOMPOSITION",
            },
        )

    def test_angle_decomposition_has_stable_decision_changing_leaves(self):
        micro = self.microtopics["MIC-PHY-VEC-ANGLE-DECOMPOSITION"]
        self.assertEqual(
            [row["id"] for row in micro["teaching_path"]],
            ["VAD-1", "VAD-2", "VAD-3", "VAD-4", "VAD-5"],
        )
        by_id = {row["id"]: row for row in micro["teaching_path"]}
        self.assertIn("already supplied", by_id["VAD-1"]["action"])
        self.assertIn("adjacent", by_id["VAD-2"]["action"])
        self.assertIn("component magnitudes", by_id["VAD-3"]["action"])
        self.assertIn("initial velocity", by_id["VAD-4"]["action"])
        self.assertIn("Reconstruct", by_id["VAD-5"]["action"])

    def test_vector_motion_boundary_is_explicit_not_a_new_capability(self):
        cap = self.capabilities["CAP-VEC-ANGLE-DECOMPOSITION"]
        boundary = cap["extensions"]["agent_a:semantic_boundary"]
        self.assertIn("representation", boundary.lower())
        self.assertIn("CAP-KIN-2D-INDEPENDENT-COMPONENTS", boundary)

        package_text = json.dumps(self.package)
        self.assertNotIn("CAP-VEC-INITIAL-VELOCITY", package_text)
        self.assertNotIn("CAP-VEC-PROJECTILE-DECOMPOSITION", package_text)

        excluded = " ".join(self.package["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("later-time evolution", excluded)

        initial = self.questions["Q-PHY-VEC-DECOMP-2A-INITIAL-STATE-05"]
        self.assertEqual(initial["primary_capability_ref"], "CAP-VEC-ANGLE-DECOMPOSITION")
        self.assertEqual(initial["secondary_capability_refs"], [])

    def test_misconceptions_cover_reference_sign_need_and_boundary(self):
        micro = self.microtopics["MIC-PHY-VEC-ANGLE-DECOMPOSITION"]
        text = " ".join(row["wrong_idea"] for row in micro["misconceptions"]).lower()
        self.assertIn("regardless of which axis", text)
        self.assertIn("automatically provide", text)
        self.assertIn("trigonometric decomposition", text)
        self.assertIn("later", text)

    def test_new_family_has_five_practice_and_five_transfer_items(self):
        family = next(
            row for row in self.package["question_families"]
            if row["id"] == "FAM-PHY-VEC-ANGLE-DECOMP-PRACTICE"
        )
        self.assertEqual(len(family["item_refs"]), 10)
        rows = [self.questions[qid] for qid in family["item_refs"]]
        core2a = [
            row for row in rows
            if any(e["core"] == "CORE2A" for e in row["exposure"])
        ]
        core2b = [
            row for row in rows
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(len(core2a), 5)
        self.assertEqual(len(core2b), 5)

    def test_transfer_spans_representation_model_choice_and_reasoning(self):
        family = next(
            row for row in self.package["question_families"]
            if row["id"] == "FAM-PHY-VEC-ANGLE-DECOMP-PRACTICE"
        )
        rows = [
            self.questions[qid]
            for qid in family["item_refs"]
            if any(
                e["core"] == "CORE2B"
                for e in self.questions[qid]["exposure"]
            )
        ]
        self.assertEqual(
            {row["transfer"]["dimension"] for row in rows},
            {"representation_translation", "model_choice", "reasoning_steps"},
        )
        step_ids = {"VAD-1", "VAD-2", "VAD-3", "VAD-4", "VAD-5"}
        for row in rows:
            with self.subTest(question=row["id"]):
                self.assertIn(row["repair_ref"], step_ids)
                self.assertIsNotNone(row["adaptation"])
                self.assertIn(row["adaptation"]["parent_ref"], self.questions)
                self.assertIn(
                    row["adaptation"]["parent_ref"],
                    row["transfer"]["builds_on"],
                )
                self.assertTrue(row["answer"].get("rubric"))

    def test_model_choice_hint_does_not_hand_over_the_decision(self):
        row = self.questions["Q-PHY-VEC-DECOMP-2B-ALREADY-COMPONENTS-02"]
        self.assertEqual(row["transfer"]["dimension"], "model_choice")
        self.assertEqual({hint["reveals"] for hint in row["hints"]}, {"CONCEPT"})
        safe = feedback.next_safe_hint(row, [])
        self.assertIsNotNone(safe)
        self.assertEqual(safe["reveals"], "CONCEPT")

    def test_all_new_questions_are_authored_not_external_copies(self):
        family = next(
            row for row in self.package["question_families"]
            if row["id"] == "FAM-PHY-VEC-ANGLE-DECOMP-PRACTICE"
        )
        for qid in family["item_refs"]:
            row = self.questions[qid]
            with self.subTest(question=qid):
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(
                    row["source_refs"],
                    ["SRC-AUTHOR-VEC-ANGLE-DECOMP-PRACTICE"],
                )
                self.assertEqual(
                    row["extensions"]["examside:use"],
                    "DEMAND_FAMILY_ONLY_NOT_COPIED",
                )

    def test_matrix_r4_makes_boundary_and_variation_visible(self):
        r4 = next(row for row in self.matrix["rungs"] if row["rung"] == "R4")
        self.assertGreaterEqual(len(r4["controlled_variation"]), 6)
        text = " ".join(
            row["notice"] for row in r4["controlled_variation"]
        ).lower()
        self.assertIn("decomposition is skipped", text)
        self.assertIn("initial instant", text)
        self.assertIn("motion-in-2d", text)

        dims = {
            row["dimension"]
            for row in self.matrix["transfer"]
            if row["repair_to"] == "R4"
        }
        self.assertEqual(
            dims,
            {"representation_translation", "model_choice", "reasoning_steps"},
        )

    def test_vector_matrix_remains_ready_with_only_declared_math_bridge(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VEC-ADD-SUB",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)


if __name__ == "__main__":
    unittest.main()
