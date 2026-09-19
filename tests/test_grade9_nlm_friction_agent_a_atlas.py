"""Agent A semantic Atlas packet for Grade-9 NLM friction."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request, session_readiness  # noqa: E402


class Grade9NlmFrictionAgentAAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json").read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json").read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.microtopics = {row["id"]: row for row in cls.package["microtopics"]}
        cls.capabilities = {row["id"]: row for row in cls.package["capabilities"]}
        cls.friction_caps = {"CAP-NLM-FRICTION", "CAP-NLM-FRICTION-QUANT"}

    def test_friction_keeps_two_durable_capabilities(self):
        friction_ids = {
            cap_id for cap_id in self.capabilities
            if "FRICTION" in cap_id
        }
        self.assertEqual(
            friction_ids,
            {"CAP-NLM-FRICTION", "CAP-NLM-FRICTION-QUANT"},
        )
        self.assertIn(
            "qualitative contact-level",
            self.capabilities["CAP-NLM-FRICTION"]["extensions"][
                "agent_a:semantic_boundary"
            ],
        )
        self.assertIn(
            "static-feasibility",
            self.capabilities["CAP-NLM-FRICTION-QUANT"]["extensions"][
                "agent_a:semantic_boundary"
            ],
        )

    def test_semantic_leaf_ids_are_stable_and_diagnostic_addressable(self):
        expected = {
            "MIC-PHY-NLM-FRICTION": ["NLM5-1", "NLM5-2", "NLM5-3", "NLM5-4"],
            "MIC-PHY-NLM-FRICTION-QUANT": ["NLM8-1", "NLM8-2", "NLM8-3", "NLM8-4"],
        }
        for micro_id, step_ids in expected.items():
            with self.subTest(micro_id=micro_id):
                micro = self.microtopics[micro_id]
                self.assertEqual([row["id"] for row in micro["teaching_path"]], step_ids)
                for row in micro["teaching_path"]:
                    self.assertTrue(row["action"])
                    self.assertTrue(row["why_valid"])

    def test_misconceptions_cover_distinct_friction_failure_boundaries(self):
        qualitative = " ".join(
            row["wrong_idea"]
            for row in self.microtopics["MIC-PHY-NLM-FRICTION"]["misconceptions"]
        ).lower()
        quantitative = " ".join(
            row["wrong_idea"]
            for row in self.microtopics["MIC-PHY-NLM-FRICTION-QUANT"]["misconceptions"]
        ).lower()

        self.assertIn("opposite the object's velocity", qualitative)
        self.assertIn("nonzero friction", qualitative)
        self.assertIn("friction always equals mu n", quantitative)
        self.assertIn("normal force is always mg", quantitative)
        self.assertIn("which friction model", quantitative)

    def test_friction_packet_has_five_core2a_and_five_core2b_items(self):
        friction_questions = [
            row for row in self.package["questions"]
            if row["extensions"].get("agent_a:packet") == "NLM_FRICTION"
        ]
        core2a = [
            row for row in friction_questions
            if any(e["core"] == "CORE2A" for e in row["exposure"])
        ]
        core2b = [
            row for row in friction_questions
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(len(core2a), 5)
        self.assertEqual(len(core2b), 5)

        inventory = practice_inventory.coverage(
            self.records,
            "BUCKET-PHY-NLM-FIRST-LAW",
        )
        for row in core2a:
            self.assertIn(row["id"], inventory["CORE2A"])
        for row in core2b:
            self.assertIn(row["id"], inventory["CORE2B"])

    def test_transfer_set_spans_materially_different_demands(self):
        transfers = [
            row for row in self.package["questions"]
            if row["extensions"].get("agent_a:packet") == "NLM_FRICTION"
            and any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(
            {row["transfer"]["dimension"] for row in transfers},
            {"representation_translation", "model_choice", "reasoning_steps"},
        )

        friction_step_ids = {
            step["id"]
            for micro_id in ("MIC-PHY-NLM-FRICTION", "MIC-PHY-NLM-FRICTION-QUANT")
            for step in self.microtopics[micro_id]["teaching_path"]
        }
        for row in transfers:
            with self.subTest(question=row["id"]):
                self.assertIsNotNone(row["adaptation"])
                self.assertIn(row["adaptation"]["parent_ref"], self.questions)
                self.assertIn(row["repair_ref"], friction_step_ids)
                self.assertIn(
                    row["adaptation"]["parent_ref"],
                    row["transfer"]["builds_on"],
                )
                self.assertTrue(row["answer"].get("rubric"))

    def test_model_choice_hints_do_not_hand_over_the_method(self):
        for row in self.package["questions"]:
            if (
                row["extensions"].get("agent_a:packet") != "NLM_FRICTION"
                or not row.get("transfer")
                or row["transfer"]["dimension"] != "model_choice"
            ):
                continue
            with self.subTest(question=row["id"]):
                self.assertEqual(
                    {hint["reveals"] for hint in row["hints"]},
                    {"CONCEPT"},
                )
                safe = feedback.next_safe_hint(row, [])
                self.assertIsNotNone(safe)
                self.assertEqual(safe["reveals"], "CONCEPT")

    def test_all_friction_packet_questions_are_authored(self):
        rows = [
            row for row in self.package["questions"]
            if row["extensions"].get("agent_a:packet") == "NLM_FRICTION"
        ]
        self.assertEqual(len(rows), 10)
        for row in rows:
            with self.subTest(question=row["id"]):
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(row["source_refs"], ["SRC-AUTHOR-NLM"])
                self.assertEqual(
                    row["extensions"].get("agent_a:packet"),
                    "NLM_FRICTION",
                )
                self.assertTrue(row["original_identifier"].startswith("AUTHOR-NLM-"))
                self.assertTrue(row.get("repair_ref"))

    def test_zero_friction_and_state_selection_remain_actions_not_new_skills(self):
        package_text = json.dumps(self.package)
        for token in (
            "CAP-NLM-FRICTION-ZERO",
            "CAP-NLM-STATIC-FRICTION-LIMIT",
            "CAP-NLM-KINETIC-FRICTION",
            "CAP-NLM-NORMAL-REACTION",
        ):
            self.assertNotIn(token, package_text)

        r5 = next(row for row in self.matrix["rungs"] if row["rung"] == "R5")
        r8 = next(row for row in self.matrix["rungs"] if row["rung"] == "R8")
        self.assertGreaterEqual(len(r5["controlled_variation"]), 3)
        self.assertGreaterEqual(len(r8["controlled_variation"]), 3)
        self.assertIn(
            "zero",
            " ".join(r5["must_contain"]).lower(),
        )
        self.assertIn(
            "contact-state",
            " ".join(r8["must_contain"]).lower(),
        )

    def test_connected_systems_remain_secondary_context_not_reauthored_here(self):
        packet_rows = [
            row for row in self.package["questions"]
            if row["extensions"].get("agent_a:packet") == "NLM_FRICTION"
        ]
        self.assertTrue(
            any(
                "CAP-NLM-CONNECTED-COMMON-ACCEL" in row["secondary_capability_refs"]
                for row in packet_rows
            )
        )
        self.assertFalse(
            any(
                row["primary_capability_ref"] == "CAP-NLM-CONNECTED-COMMON-ACCEL"
                for row in packet_rows
            )
        )

    def test_matrix_remains_session_ready(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-NLM-FIRST-LAW",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertIn(
            report["status"],
            {session_readiness.READY, session_readiness.READY_WITH_BRIDGE},
        )


if __name__ == "__main__":
    unittest.main()
