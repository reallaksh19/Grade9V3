"""Representative ExamSIDE-backed Core2B transfer set for Grade-9 NLM."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import compile_inputs, practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request  # noqa: E402


class Grade9NlmExamSideCore2BTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.transfer_ids = [
            "Q-PHY-NLM-2B-FRICTION-STATE-01",
            "Q-PHY-NLM-2B-CONNECTED-SYSTEM-02",
            "Q-PHY-NLM-2B-STRING-MODEL-03",
            "Q-PHY-NLM-2B-PULLEY-REPRESENTATION-04",
            "Q-PHY-NLM-2B-FRAME-SELECTION-05",
        ]

    def test_no_earlier_pr_had_already_populated_nlm_core2b(self):
        # This is a repository-state regression, not a claim about GitHub history:
        # the transfer slice is deliberately the five-question set introduced here.
        inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-FIRST-LAW"
        )
        self.assertEqual(inventory["CORE2B"], self.transfer_ids)

    def test_transfer_set_covers_the_representative_nlm_decisions(self):
        expected = {
            "Q-PHY-NLM-2B-FRICTION-STATE-01":
                ("CAP-NLM-FRICTION-QUANT", "model_choice"),
            "Q-PHY-NLM-2B-CONNECTED-SYSTEM-02":
                ("CAP-NLM-CONNECTED-COMMON-ACCEL", "reasoning_steps"),
            "Q-PHY-NLM-2B-STRING-MODEL-03":
                ("CAP-NLM-IDEAL-STRING-TENSION", "model_choice"),
            "Q-PHY-NLM-2B-PULLEY-REPRESENTATION-04":
                ("CAP-NLM-SINGLE-STRING-CONSTRAINT", "representation_translation"),
            "Q-PHY-NLM-2B-FRAME-SELECTION-05":
                ("CAP-NLM-FRAME-CHOICE", "model_choice"),
        }
        for question_id, (capability, dimension) in expected.items():
            with self.subTest(question_id=question_id):
                q = self.questions[question_id]
                self.assertEqual(q["primary_capability_ref"], capability)
                self.assertEqual(q["transfer"]["dimension"], dimension)
                self.assertEqual(
                    q["exposure"],
                    [{"core": "CORE2B", "role": "NEW_TRANSFER", "artifact_ref": None}],
                )

    def test_every_transfer_is_a_real_adaptation_with_lineage(self):
        for question_id in self.transfer_ids:
            with self.subTest(question_id=question_id):
                q = self.questions[question_id]
                parent_ref = q["adaptation"]["parent_ref"]
                self.assertIn(parent_ref, self.questions)
                self.assertIn(parent_ref, q["transfer"]["builds_on"])
                self.assertTrue(
                    set(q["adaptation"]["changed_fields"])
                    & {"stem", "subparts", "options", "conditions", "figure_refs", "answer"}
                )
                self.assertEqual(
                    self.questions[parent_ref]["family_ref"],
                    q["family_ref"],
                )

    def test_core2b_contract_fields_are_present(self):
        for question_id in self.transfer_ids:
            with self.subTest(question_id=question_id):
                q = self.questions[question_id]
                self.assertTrue(q["hints"])
                self.assertTrue(q["answer"]["rubric"])
                for row in q["answer"]["rubric"]:
                    self.assertTrue(row["criterion"])
                    self.assertTrue(row["evidence_of"])
                self.assertTrue(q["repair_ref"])
                self.assertTrue(q["transfer"]["statement"])
                self.assertTrue(q["transfer"]["builds_on"])

    def test_model_choice_hints_do_not_hand_over_a_method(self):
        for question_id in self.transfer_ids:
            q = self.questions[question_id]
            if q["transfer"]["dimension"] != "model_choice":
                continue
            with self.subTest(question_id=question_id):
                self.assertTrue(q["hints"])
                self.assertEqual(
                    {hint["reveals"] for hint in q["hints"]},
                    {"CONCEPT"},
                )
                first = feedback.next_safe_hint(q, [])
                self.assertIsNotNone(first)
                self.assertEqual(first["reveals"], "CONCEPT")

    def test_representation_and_reasoning_transfers_do_not_change_science(self):
        connected = self.questions["Q-PHY-NLM-2B-CONNECTED-SYSTEM-02"]
        self.assertIn(
            "Q-PHY-NLM-2A-CONNECTED-02",
            connected["transfer"]["builds_on"],
        )
        pulley = self.questions["Q-PHY-NLM-2B-PULLEY-REPRESENTATION-04"]
        self.assertIn(
            "Q-PHY-NLM-2A-FIXED-PULLEY-04",
            pulley["transfer"]["builds_on"],
        )
        self.assertEqual(
            pulley["repair_ref"],
            "NLM11-2",
        )

    def test_frame_transfer_has_a_same_capability_practice_anchor(self):
        anchor = self.questions["Q-PHY-NLM-2A-FRAME-CHOICE-07"]
        transfer = self.questions["Q-PHY-NLM-2B-FRAME-SELECTION-05"]
        self.assertEqual(
            anchor["primary_capability_ref"],
            "CAP-NLM-FRAME-CHOICE",
        )
        self.assertEqual(
            anchor["exposure"],
            [{"core": "CORE2A", "role": "PRACTICE", "artifact_ref": None}],
        )
        self.assertEqual(
            transfer["adaptation"]["parent_ref"],
            anchor["id"],
        )

    def test_examside_is_demand_provenance_not_question_custody(self):
        for question_id in self.transfer_ids:
            with self.subTest(question_id=question_id):
                q = self.questions[question_id]
                self.assertEqual(q["origin"], "AUTHORED")
                self.assertEqual(q["source_refs"], ["SRC-AUTHOR-NLM"])
                self.assertEqual(
                    q["extensions"]["examside:use"],
                    "DEMAND_FAMILY_ONLY_NOT_COPIED",
                )
                self.assertTrue(
                    q["extensions"]["examside:demand_source"].startswith(
                        "https://questions.examside.com/past-years/jee/question/"
                    )
                )

    def test_core2b_inventory_is_now_representative_not_a_single_token_item(self):
        inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-FIRST-LAW"
        )
        self.assertEqual(len(inventory["CORE2B"]), 5)
        dimensions = {
            self.questions[qid]["transfer"]["dimension"]
            for qid in inventory["CORE2B"]
        }
        self.assertEqual(
            dimensions,
            {"model_choice", "reasoning_steps", "representation_translation"},
        )

    def test_compiler_carries_transfer_rubric_and_repair_payload(self):
        compiled = compile_inputs.compile_bucket(
            self.records,
            "BUCKET-PHY-NLM-FIRST-LAW",
            topic_id="g9-nlm-core2b-transfer",
            title="Grade 9 NLM transfer",
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
        self.assertEqual(set(blocks), set(self.transfer_ids))
        for question_id in self.transfer_ids:
            with self.subTest(question_id=question_id):
                original = self.questions[question_id]
                block = blocks[question_id]
                self.assertEqual(block["transfer"], original["transfer"])
                self.assertEqual(block["repair_ref"], original["repair_ref"])
                self.assertEqual(
                    block["answer"]["rubric"],
                    original["answer"]["rubric"],
                )

    def test_nondefault_frame_rung_remains_nondefault(self):
        frame = next(
            row for row in self.matrix["rungs"]
            if row["microtopic_ref"] == "MIC-PHY-NLM-FRAME-CHOICE"
        )
        self.assertFalse(frame["default_entry_eligible"])

    def test_momentum_transfer_bucket_is_not_silently_opened_for_core2b(self):
        inventory = practice_inventory.coverage(
            self.records, "BUCKET-PHY-NLM-MOMENTUM-TRANSFER"
        )
        self.assertEqual(inventory["CORE2B"], [])


if __name__ == "__main__":
    unittest.main()
