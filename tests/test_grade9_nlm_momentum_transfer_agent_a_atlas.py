"""Agent A semantic Atlas packet for the explicit-demand NLM momentum-transfer extension."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import compile_inputs, practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request, session_readiness  # noqa: E402


class Grade9NlmMomentumTransferAgentAAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-nlm-momentum-transfer.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-momentum-transfer.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.capability = cls.package["capabilities"][0]
        cls.micro = cls.package["microtopics"][0]
        cls.family = cls.package["question_families"][0]
        cls.questions = {row["id"]: row for row in cls.package["questions"]}

    def test_one_durable_capability_remains_the_owner(self):
        self.assertEqual(len(self.package["capabilities"]), 1)
        self.assertEqual(
            self.capability["id"],
            "CAP-NLM-MOMENTUM-TRANSFER-RATE",
        )
        boundary = self.capability["extensions"]["agent_a:semantic_boundary"]
        self.assertIn("average external force", boundary)
        self.assertIn("does not own the instantaneous force-time pulse", boundary)

    def test_semantic_actions_are_stable_and_diagnostic_addressable(self):
        self.assertEqual(
            [row["id"] for row in self.micro["teaching_path"]],
            [
                "NLM-MTR-1",
                "NLM-MTR-2",
                "NLM-MTR-3",
                "NLM-MTR-4",
                "NLM-MTR-5",
                "NLM-MTR-6",
            ],
        )
        for row in self.micro["teaching_path"]:
            with self.subTest(step=row["id"]):
                self.assertTrue(row["action"])
                self.assertTrue(row["why_valid"])
                self.assertTrue(row["output"])

    def test_question_family_is_bound_to_the_microtopic(self):
        self.assertEqual(
            self.micro["question_family_refs"],
            ["FAM-PHY-NLM-MOMENTUM-TRANSFER-PRACTICE"],
        )
        self.assertEqual(
            self.family["capability_refs"],
            ["CAP-NLM-MOMENTUM-TRANSFER-RATE"],
        )
        self.assertEqual(set(self.family["item_refs"]), set(self.questions))

    def test_misconceptions_cover_distinct_failure_boundaries(self):
        wrong = " ".join(
            row["wrong_idea"] for row in self.micro["misconceptions"]
        ).lower()
        self.assertIn("final momentum", wrong)
        self.assertIn("same direction", wrong)
        self.assertIn("rocket", wrong)
        self.assertIn("instantaneous force", wrong)

    def test_packet_has_five_core2a_and_five_core2b_items(self):
        rows = list(self.questions.values())
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

        inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-MOMENTUM-TRANSFER"
        )
        self.assertEqual(set(inventory["CORE2A"]), {row["id"] for row in core2a})
        self.assertEqual(set(inventory["CORE2B"]), {row["id"] for row in core2b})

    def test_all_packet_questions_are_authored_and_have_repair_routes(self):
        self.assertEqual(len(self.questions), 10)
        for row in self.questions.values():
            with self.subTest(question=row["id"]):
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(
                    row["source_refs"],
                    ["SRC-AUTHOR-NLM-MOMENTUM-TRANSFER"],
                )
                self.assertEqual(
                    row["extensions"].get("agent_a:packet"),
                    "NLM_MOMENTUM_TRANSFER",
                )
                self.assertTrue(row["original_identifier"].startswith("AUTHOR-NLM-MTR-"))
                self.assertTrue(row.get("repair_ref"))

    def test_transfer_set_spans_existing_changed_demand_dimensions(self):
        transfers = [
            row for row in self.questions.values()
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        ]
        self.assertEqual(
            {row["transfer"]["dimension"] for row in transfers},
            {"model_choice", "representation_translation", "reasoning_steps"},
        )
        step_ids = {row["id"] for row in self.micro["teaching_path"]}
        parents = set()
        for row in transfers:
            with self.subTest(question=row["id"]):
                parent = row["adaptation"]["parent_ref"]
                self.assertIn(parent, self.questions)
                self.assertIn(parent, row["transfer"]["builds_on"])
                self.assertNotIn(parent, parents)
                parents.add(parent)
                self.assertIn(row["repair_ref"], step_ids)
                self.assertTrue(row["answer"].get("rubric"))

    def test_model_choice_hints_remain_conceptual(self):
        for row in self.questions.values():
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

    def test_zero_change_case_refuses_final_momentum_shortcut(self):
        q = self.questions["Q-PHY-NLM-MTR-2B-ZERO-04"]
        self.assertIn("Delta p=m(120-120)=0", q["answer"]["summary"])
        self.assertIn("zero average transfer force", q["answer"]["summary"])
        self.assertEqual(q["repair_ref"], "NLM-MTR-2")

    def test_average_force_is_not_promoted_to_instantaneous_force(self):
        practice = self.questions["Q-PHY-NLM-MTR-2A-05"]
        transfer = self.questions["Q-PHY-NLM-MTR-2B-AVERAGE-05"]
        self.assertIn("average stream force is +30 N", practice["answer"]["summary"])
        self.assertIn(
            "time-average momentum-transfer force",
            transfer["answer"]["summary"],
        )
        self.assertIn("pulse-duration", transfer["answer"]["summary"])
        self.assertEqual(transfer["repair_ref"], "NLM-MTR-6")

    def test_compiler_carries_extension_transfer_payload(self):
        compiled = compile_inputs.compile_bucket(
            self.records,
            "BUCKET-PHY-NLM-MOMENTUM-TRANSFER",
            topic_id="g9-nlm-momentum-transfer-agent-a",
            title="Grade 9 NLM momentum transfer",
            subject="Physics",
            practice_control={"mode": "DESIGN_PREVIEW", "purpose": "COMPETITION"},
        )
        product = next(
            row for row in compiled["plan"]["products"]
            if row["core"] == "CORE2B"
        )
        blocks = {
            row["source_question_id"]: row
            for row in product["units"][0]["blocks"]
            if row["kind"] == "QUESTION"
        }
        expected = {
            qid for qid, row in self.questions.items()
            if any(e["core"] == "CORE2B" for e in row["exposure"])
        }
        self.assertEqual(set(blocks), expected)
        for qid in expected:
            with self.subTest(question=qid):
                self.assertEqual(blocks[qid]["transfer"], self.questions[qid]["transfer"])
                self.assertEqual(blocks[qid]["repair_ref"], self.questions[qid]["repair_ref"])
                self.assertEqual(
                    blocks[qid]["answer"]["rubric"],
                    self.questions[qid]["answer"]["rubric"],
                )

    def test_extension_remains_nondefault_and_bounded(self):
        self.assertEqual(len(self.matrix["rungs"]), 1)
        rung = self.matrix["rungs"][0]
        self.assertFalse(rung["default_entry_eligible"])
        self.assertGreaterEqual(len(rung["controlled_variation"]), 4)
        must = " ".join(rung["must_contain"]).lower()
        self.assertIn("zero-momentum-change", must)
        self.assertIn("average repeated-event force", must)

        text = json.dumps(self.package).lower()
        for forbidden_capability in (
            "cap-nlm-impulse",
            "cap-nlm-collision",
            "cap-nlm-rocket",
            "cap-nlm-variable-mass",
            "cap-nlm-peak-force",
        ):
            self.assertNotIn(forbidden_capability, text)

    def test_default_nlm_bucket_does_not_absorb_extension_practice(self):
        default_inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-FIRST-LAW"
        )
        for core in ("CORE2A", "CORE2B"):
            self.assertTrue(
                all(
                    not qid.startswith("Q-PHY-NLM-MTR-")
                    for qid in default_inventory[core]
                )
            )

    def test_matrix_remains_session_ready_but_nondefault(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-NLM-MOMENTUM-TRANSFER",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY)
        self.assertFalse(self.matrix["rungs"][0]["default_entry_eligible"])


if __name__ == "__main__":
    unittest.main()
