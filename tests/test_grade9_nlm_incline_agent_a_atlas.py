"""Agent A semantic Atlas packet for bounded NLM inclined-plane integration."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request, session_readiness  # noqa: E402


class Grade9NlmInclineIntegrationAgentAAtlas(unittest.TestCase):
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
        cls.contexts = {row["id"]: row for row in cls.package.get("application_contexts", [])}
        cls.family = next(
            row for row in cls.package["question_families"]
            if row["id"] == "FAM-PHY-NLM-INCLINE-MODELLING"
        )
        cls.packet_rows = [
            row for row in cls.package["questions"]
            if row["extensions"].get("agent_a:packet") == "NLM_INCLINE_INTEGRATION"
        ]

    def test_incline_is_context_and_family_not_new_capability(self):
        self.assertIn("CTX-PHY-NLM-INCLINED-PLANE", self.contexts)
        self.assertEqual(
            self.family["context_refs"],
            ["CTX-PHY-NLM-INCLINED-PLANE"],
        )
        capability_ids = set(self.capabilities)
        for forbidden in (
            "CAP-NLM-INCLINE",
            "CAP-NLM-INCLINED-PLANE",
            "CAP-NLM-NORMAL-ON-INCLINE",
            "CAP-NLM-WEIGHT-COMPONENTS",
        ):
            self.assertNotIn(forbidden, capability_ids)

        context_id = "CTX-PHY-NLM-INCLINED-PLANE"
        for cap in self.package["capabilities"]:
            self.assertNotIn(context_id, cap.get("prerequisite_refs", []))
        for micro in self.package["microtopics"]:
            self.assertNotIn(context_id, micro.get("prerequisite_refs", []))

    def test_existing_durable_owners_are_reused(self):
        self.assertEqual(
            set(self.family["capability_refs"]),
            {
                "CAP-NLM-FBD-BODY-OWNERSHIP",
                "CAP-NLM-SECOND-LAW",
                "CAP-NLM-FRICTION",
                "CAP-NLM-FRICTION-QUANT",
                "CAP-VEC-ANGLE-DECOMPOSITION",
            },
        )
        for cap_id in (
            "CAP-NLM-FBD-BODY-OWNERSHIP",
            "CAP-NLM-SECOND-LAW",
            "CAP-NLM-FRICTION",
            "CAP-NLM-FRICTION-QUANT",
        ):
            self.assertEqual(
                self.capabilities[cap_id]["extensions"]["agent_a:incline_integration"],
                "USES_EXISTING_OWNER",
            )

    def test_new_semantic_actions_target_setup_not_a_new_skill_tree(self):
        fbd_steps = {
            row["id"]: row
            for row in self.microtopics["MIC-PHY-NLM-FBD-BODY-OWNERSHIP"]["teaching_path"]
        }
        second_steps = {
            row["id"]: row
            for row in self.microtopics["MIC-PHY-NLM-SECOND-LAW"]["teaching_path"]
        }
        self.assertIn("NLM3-4", fbd_steps)
        self.assertIn("NLM6-4", second_steps)
        self.assertIn("never both", fbd_steps["NLM3-4"]["output"])
        self.assertIn("a_perp = 0", second_steps["NLM6-4"]["output"])

    def test_setup_misconceptions_are_explicit(self):
        fbd_wrong = " ".join(
            row["wrong_idea"]
            for row in self.microtopics["MIC-PHY-NLM-FBD-BODY-OWNERSHIP"]["misconceptions"]
        ).lower()
        second_wrong = " ".join(
            row["wrong_idea"]
            for row in self.microtopics["MIC-PHY-NLM-SECOND-LAW"]["misconceptions"]
        ).lower()
        self.assertIn("three separate forces", fbd_wrong)
        self.assertIn("total acceleration must be zero", second_wrong)

    def test_packet_has_five_core2a_and_five_core2b_items(self):
        core2a = [
            row for row in self.packet_rows
            if any(e["core"] == "CORE2A" for e in row["exposure"])
        ]
        core2b = [
            row for row in self.packet_rows
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(len(core2a), 5)
        self.assertEqual(len(core2b), 5)

        inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-FIRST-LAW"
        )
        for row in core2a:
            self.assertIn(row["id"], inventory["CORE2A"])
        for row in core2b:
            self.assertIn(row["id"], inventory["CORE2B"])

    def test_every_packet_question_uses_the_incline_context(self):
        self.assertEqual(len(self.packet_rows), 10)
        for row in self.packet_rows:
            with self.subTest(question=row["id"]):
                self.assertEqual(
                    row["context_refs"],
                    ["CTX-PHY-NLM-INCLINED-PLANE"],
                )
                self.assertEqual(row["family_ref"], self.family["id"])
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(row["source_refs"], ["SRC-AUTHOR-NLM"])
                self.assertTrue(row.get("repair_ref"))

    def test_transfer_set_spans_model_representation_and_reasoning(self):
        transfers = [
            row for row in self.packet_rows
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(
            {row["transfer"]["dimension"] for row in transfers},
            {"model_choice", "representation_translation", "reasoning_steps"},
        )
        parents = set()
        for row in transfers:
            with self.subTest(question=row["id"]):
                parent = row["adaptation"]["parent_ref"]
                self.assertIn(parent, self.questions)
                self.assertIn(parent, row["transfer"]["builds_on"])
                self.assertNotIn(parent, parents)
                parents.add(parent)
                self.assertTrue(row["answer"].get("rubric"))

    def test_model_choice_hints_remain_conceptual(self):
        for row in self.packet_rows:
            if (
                not row.get("transfer")
                or row["transfer"]["dimension"] != "model_choice"
            ):
                continue
            with self.subTest(question=row["id"]):
                self.assertEqual(
                    {hint["reveals"] for hint in row["hints"]},
                    {"CONCEPT"},
                )
                first = feedback.next_safe_hint(row, [])
                self.assertIsNotNone(first)
                self.assertEqual(first["reveals"], "CONCEPT")

    def test_smooth_incline_witness_has_correct_boundary_values(self):
        q = self.questions["Q-PHY-NLM-INCLINE-2A-SMOOTH-01"]
        summary = q["answer"]["summary"]
        self.assertIn("N=mg cos(theta)", summary)
        self.assertIn("g sin(theta)", summary)
        check = q["answer"]["check"]
        self.assertIn("theta=0", check)
        self.assertIn("90 degrees", check)

    def test_horizontal_push_changes_normal_reaction(self):
        q = self.questions["Q-PHY-NLM-INCLINE-2A-HORIZONTAL-PUSH-04"]
        self.assertIn(
            "N=mg cos(theta)+P sin(theta)",
            q["answer"]["summary"],
        )
        transfer = self.questions["Q-PHY-NLM-INCLINE-2B-HORIZONTAL-THRESHOLD-03"]
        self.assertIn(
            "|mg sin(theta)-P cos(theta)| <= mu_s[mg cos(theta)+P sin(theta)]",
            transfer["answer"]["summary"],
        )

    def test_static_friction_can_reverse_or_be_zero(self):
        q = self.questions["Q-PHY-NLM-INCLINE-2B-FRICTION-DIRECTION-02"]
        summary = q["answer"]["summary"]
        self.assertIn("P<mg sin(theta)", summary)
        self.assertIn("P>mg sin(theta)", summary)
        self.assertIn("required static friction is zero", summary)

    def test_timing_transfer_reaches_exam_demand_without_new_capability(self):
        q = self.questions["Q-PHY-NLM-INCLINE-2B-TIMING-05"]
        self.assertIn(
            "mu_k=tan(theta)[1-t_0^2/t^2]",
            q["answer"]["summary"],
        )
        self.assertIn(
            "CAP-KIN-CONSTANT-ACCELERATION",
            q["secondary_capability_refs"],
        )
        self.assertNotIn(
            "CAP-NLM-INCLINE",
            json.dumps(q),
        )

    def test_matrix_exposes_representation_and_contact_boundaries(self):
        by_rung = {row["rung"]: row for row in self.matrix["rungs"]}
        self.assertGreaterEqual(len(by_rung["R3"]["controlled_variation"]), 3)
        self.assertGreaterEqual(len(by_rung["R6"]["controlled_variation"]), 3)
        self.assertGreaterEqual(len(by_rung["R8"]["controlled_variation"]), 4)
        self.assertIn(
            "components",
            " ".join(by_rung["R3"]["must_contain"]).lower(),
        )
        self.assertIn(
            "zero perpendicular acceleration",
            " ".join(by_rung["R6"]["must_contain"]).lower(),
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
