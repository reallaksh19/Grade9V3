"""Agent A semantic Atlas packet for Grade-9 Motion in 2D / Motion in a Plane."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request, session_readiness  # noqa: E402


class Grade9Motion2DAgentAAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-kin-2d-motion.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-kin-2d-motion.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.microtopics = {
            row["id"]: row for row in cls.package["microtopics"]
        }

    def test_durable_three_capability_spine_is_preserved(self):
        self.assertEqual(
            [row["ladder_position"] for row in self.matrix["rungs"]],
            [30, 60, 90],
        )
        self.assertEqual(
            [row["microtopic_ref"] for row in self.matrix["rungs"]],
            [
                "MIC-PHY-KIN-2D-INDEPENDENT-COMPONENTS",
                "MIC-PHY-KIN-2D-CONSTANT-ACCELERATION",
                "MIC-PHY-KIN-PROJECTILE-MODEL",
            ],
        )
        self.assertEqual(
            {row["id"] for row in self.package["capabilities"]},
            {
                "CAP-KIN-2D-INDEPENDENT-COMPONENTS",
                "CAP-KIN-2D-CONSTANT-ACCELERATION",
                "CAP-KIN-PROJECTILE-MODEL",
            },
        )

    def test_semantic_leaf_ids_are_stable_and_diagnostic_addressable(self):
        expected = {
            "MIC-PHY-KIN-2D-INDEPENDENT-COMPONENTS": [
                "K2D1-1", "K2D1-2", "K2D1-3", "K2D1-4"
            ],
            "MIC-PHY-KIN-2D-CONSTANT-ACCELERATION": [
                "K2D2-1", "K2D2-2", "K2D2-3"
            ],
            "MIC-PHY-KIN-PROJECTILE-MODEL": [
                "K2D3-1", "K2D3-2", "K2D3-3", "K2D3-4",
                "K2D3-5", "K2D3-6", "K2D3-7",
            ],
        }
        for micro_id, step_ids in expected.items():
            with self.subTest(micro_id=micro_id):
                micro = self.microtopics[micro_id]
                self.assertEqual(
                    [row["id"] for row in micro["teaching_path"]],
                    step_ids,
                )
                for row in micro["teaching_path"]:
                    self.assertTrue(row["action"])
                    self.assertTrue(row["why_valid"])

    def test_projectile_leaf_decomposition_covers_real_failure_boundaries(self):
        micro = self.microtopics["MIC-PHY-KIN-PROJECTILE-MODEL"]
        by_id = {row["id"]: row for row in micro["teaching_path"]}
        self.assertIn("v_y=0", by_id["K2D3-4"]["action"])
        self.assertIn("Delta y=0", by_id["K2D3-5"]["action"])
        self.assertIn("actual Delta y=y_f-y_i", by_id["K2D3-6"]["action"])
        self.assertIn("actual u_y", by_id["K2D3-6"]["action"])
        self.assertIn("horizontal launch specifically", by_id["K2D3-6"]["action"])

        misconception_text = " ".join(
            row["wrong_idea"] for row in micro["misconceptions"]
        ).lower()
        self.assertIn("highest point", misconception_text)
        self.assertIn("same-height", misconception_text)
        self.assertIn("horizontal launch", misconception_text)
        self.assertIn("horizontal speed", misconception_text)

    def test_unequal_height_transfer_repairs_to_actual_landing_geometry_leaf(self):
        q = next(
            row for row in self.package["questions"]
            if row["id"] == "Q-PHY-KIN-2D-2B-UNEQUAL-HEIGHT-03"
        )
        self.assertEqual(q["repair_ref"], "K2D3-6")
        self.assertIn("u_y=10", q["stem"])
        self.assertIn("15 m above level ground", q["stem"])

    def test_outputs_remain_semantic_leaves_not_new_capabilities(self):
        caps = {row["id"] for row in self.package["capabilities"]}
        for token in (
            "RANGE",
            "MAX-HEIGHT",
            "TIME-OF-FLIGHT",
            "HORIZONTAL-PROJECTILE",
            "OBLIQUE-PROJECTILE",
            "APEX",
            "SAME-HEIGHT",
        ):
            self.assertFalse(
                any(token in cap_id for cap_id in caps),
                f"{token} should not become a separate capability in this packet",
            )

    def test_practice_family_has_balanced_core2a_and_core2b_inventory(self):
        self.assertEqual(len(self.package["question_families"]), 1)
        family = self.package["question_families"][0]
        self.assertEqual(family["id"], "FAM-PHY-KIN-2D-PRACTICE")
        self.assertEqual(len(family["item_refs"]), 10)

        inventory = practice_inventory.coverage(
            self.records,
            "BUCKET-PHY-KIN-2D-MOTION",
        )
        self.assertEqual(len(inventory["CORE2A"]), 5)
        self.assertEqual(len(inventory["CORE2B"]), 5)
        self.assertEqual(
            set(inventory["CORE2A"]) | set(inventory["CORE2B"]),
            set(family["item_refs"]),
        )

    def test_transfer_set_spans_three_real_dimensions(self):
        transfer_questions = [
            row for row in self.package["questions"]
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(len(transfer_questions), 5)
        self.assertEqual(
            {row["transfer"]["dimension"] for row in transfer_questions},
            {"representation_translation", "model_choice", "reasoning_steps"},
        )

        all_step_ids = {
            step["id"]
            for micro in self.package["microtopics"]
            for step in micro["teaching_path"]
        }
        for row in transfer_questions:
            with self.subTest(question=row["id"]):
                self.assertIsNotNone(row["adaptation"])
                self.assertIn(row["adaptation"]["parent_ref"], self.questions)
                self.assertIn(row["repair_ref"], all_step_ids)
                self.assertIn(
                    row["adaptation"]["parent_ref"],
                    row["transfer"]["builds_on"],
                )
                self.assertTrue(row["answer"].get("rubric"))

    def test_model_choice_transfer_hints_do_not_reveal_the_method(self):
        for row in self.package["questions"]:
            if not row.get("transfer"):
                continue
            if row["transfer"]["dimension"] != "model_choice":
                continue
            with self.subTest(question=row["id"]):
                self.assertEqual(
                    {hint["reveals"] for hint in row["hints"]},
                    {"CONCEPT"},
                )
                safe = feedback.next_safe_hint(row, [])
                self.assertIsNotNone(safe)
                self.assertEqual(safe["reveals"], "CONCEPT")

    def test_questions_are_authored_and_external_material_is_demand_only(self):
        for row in self.package["questions"]:
            with self.subTest(question=row["id"]):
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(
                    row["source_refs"],
                    ["SRC-AUTHOR-KIN-2D-EXAMSIDE-ADAPTATION"],
                )
                self.assertEqual(
                    row["extensions"]["examside:use"],
                    "DEMAND_FAMILY_ONLY_NOT_COPIED",
                )
                self.assertTrue(row["original_identifier"].startswith("AUTHOR-"))

    def test_relative_motion_and_trajectory_derivation_are_not_duplicated(self):
        package_text = json.dumps(self.package)
        self.assertNotIn("CAP-KIN-RELATIVE", package_text)
        excluded = " ".join(
            self.package["buckets"][0]["scope"]["excluded"]
        ).lower()
        self.assertIn("trajectory-equation", excluded)
        self.assertIn(
            "trajectory-equation derivation",
            [x.lower() for x in next(
                row for row in self.matrix["rungs"] if row["rung"] == "R3"
            )["ceiling"]],
        )

    def test_matrix_variations_make_event_and_model_boundaries_visible(self):
        by_rung = {row["rung"]: row for row in self.matrix["rungs"]}
        self.assertGreaterEqual(len(by_rung["R1"]["controlled_variation"]), 2)
        self.assertGreaterEqual(len(by_rung["R2"]["controlled_variation"]), 3)
        self.assertGreaterEqual(len(by_rung["R3"]["controlled_variation"]), 4)

        notices = " ".join(
            row["notice"] for row in by_rung["R3"]["controlled_variation"]
        ).lower()
        self.assertIn("same-height", notices)
        self.assertIn("event", notices)
        self.assertIn("one component model", notices)

    def test_matrix_remains_session_ready(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-KIN-2D-MOTION",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertIn(
            report["status"],
            {session_readiness.READY, session_readiness.READY_WITH_BRIDGE},
        )


if __name__ == "__main__":
    unittest.main()
