"""ExamSIDE-backed Laws-of-Motion practice acceptance without copying external questions."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import practice_inventory  # noqa: E402
from Shared.tools import resolve_request, worksheet_study_plan  # noqa: E402


class Grade9NlmExamSidePracticeAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlm = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.momentum = json.loads(
            (REPO / "Physics/library/phy-nlm-momentum-transfer.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.nlm_matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.momentum_matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-momentum-transfer.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.fixture = json.loads(
            (
                REPO
                / "tests/fixtures/real_pilots/examside-laws-of-motion.acceptance.json"
            ).read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.nlm_questions = {row["id"]: row for row in cls.nlm["questions"]}
        cls.momentum_questions = {
            row["id"]: row for row in cls.momentum["questions"]
        }

    def test_each_new_bounded_nlm_capability_has_core2a_practice(self):
        expected = {
            "CAP-NLM-FRICTION-QUANT": "Q-PHY-NLM-2A-FRICTION-THRESHOLD-01",
            "CAP-NLM-CONNECTED-COMMON-ACCEL": "Q-PHY-NLM-2A-CONNECTED-02",
            "CAP-NLM-IDEAL-STRING-TENSION": "Q-PHY-NLM-2A-IDEAL-STRING-03",
            "CAP-NLM-SINGLE-STRING-CONSTRAINT": "Q-PHY-NLM-2A-FIXED-PULLEY-04",
        }
        for capability, question_id in expected.items():
            with self.subTest(capability=capability):
                q = self.nlm_questions[question_id]
                self.assertEqual(q["primary_capability_ref"], capability)
                self.assertEqual(
                    q["exposure"],
                    [{"core": "CORE2A", "role": "PRACTICE", "artifact_ref": None}],
                )

    def test_momentum_transfer_explicit_extension_has_core2a_practice(self):
        q = self.momentum_questions["Q-PHY-NLM-MTR-2A-01"]
        self.assertEqual(
            q["primary_capability_ref"],
            "CAP-NLM-MOMENTUM-TRANSFER-RATE",
        )
        self.assertEqual(
            q["exposure"],
            [{"core": "CORE2A", "role": "PRACTICE", "artifact_ref": None}],
        )

    def test_practice_questions_are_authored_not_exam_identity_copies(self):
        question_ids = (
            "Q-PHY-NLM-2A-FRICTION-THRESHOLD-01",
            "Q-PHY-NLM-2A-CONNECTED-02",
            "Q-PHY-NLM-2A-IDEAL-STRING-03",
            "Q-PHY-NLM-2A-FIXED-PULLEY-04",
        )
        for question_id in question_ids:
            with self.subTest(question_id=question_id):
                q = self.nlm_questions[question_id]
                self.assertEqual(q["origin"], "AUTHORED")
                self.assertEqual(q["source_refs"], ["SRC-AUTHOR-NLM"])
                self.assertTrue(q["original_identifier"].startswith("AUTHOR-NLM-"))
                self.assertEqual(
                    q["extensions"]["examside:use"],
                    "DEMAND_FAMILY_ONLY_NOT_COPIED",
                )
                self.assertTrue(
                    q["extensions"]["examside:demand_source"].startswith(
                        "https://questions.examside.com/past-years/jee/question/"
                    )
                )

        q = self.momentum_questions["Q-PHY-NLM-MTR-2A-01"]
        self.assertEqual(q["origin"], "AUTHORED")
        self.assertEqual(
            q["source_refs"],
            ["SRC-AUTHOR-NLM-MOMENTUM-TRANSFER"],
        )
        self.assertEqual(
            q["extensions"]["examside:use"],
            "DEMAND_FAMILY_ONLY_NOT_COPIED",
        )

    def test_practice_inventory_closes_core2a_but_does_not_prematurely_open_core2b(self):
        nlm = practice_inventory.coverage(
            self.records,
            "BUCKET-PHY-NLM-FIRST-LAW",
        )
        for question_id in (
            "Q-PHY-NLM-2A-FRICTION-THRESHOLD-01",
            "Q-PHY-NLM-2A-CONNECTED-02",
            "Q-PHY-NLM-2A-IDEAL-STRING-03",
            "Q-PHY-NLM-2A-FIXED-PULLEY-04",
        ):
            self.assertIn(question_id, nlm["CORE2A"])
        self.assertEqual(nlm["CORE2B"], [])

        momentum = practice_inventory.coverage(
            self.records,
            "BUCKET-PHY-NLM-MOMENTUM-TRANSFER",
        )
        self.assertIn("Q-PHY-NLM-MTR-2A-01", momentum["CORE2A"])
        self.assertEqual(momentum["CORE2B"], [])

    def test_real_examside_acceptance_fixture_routes_through_current_capability_graph(self):
        report = worksheet_study_plan.resolve(self.fixture)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(len(report["questions"]), 7)

        mapped = {
            row["question_id"]: row
            for row in self.fixture["questions"]
        }
        self.assertEqual(
            mapped["EXAMSIDE-NLM-2021-03-18-BULLET-WOOD"][
                "primary_capability_ref"
            ],
            "CAP-KIN-CONSTANT-ACCELERATION",
        )
        self.assertEqual(
            mapped["EXAMSIDE-NLM-2021-03-18-BULLET-WOOD"][
                "secondary_capability_refs"
            ],
            ["CAP-NLM-SECOND-LAW"],
        )
        self.assertEqual(
            mapped["EXAMSIDE-NLM-2021-08-31-ACCELERATING-CAR-BOB"][
                "primary_capability_ref"
            ],
            "CAP-NLM-FRAME-CHOICE",
        )
        self.assertEqual(
            mapped["EXAMSIDE-NLM-MOMENTUM-TRANSFER-MACHINE-GUN"][
                "primary_capability_ref"
            ],
            "CAP-NLM-MOMENTUM-TRANSFER-RATE",
        )
        for row in self.fixture["questions"]:
            self.assertEqual(row["mapping_basis"], "AGENT_PROPOSAL")
            self.assertNotIn("canonical_question_ref", row)
            self.assertIn(
                "https://questions.examside.com/past-years/jee/question/",
                row["note"],
            )

    def test_nondefault_extensions_stay_nondefault(self):
        frame = next(
            row for row in self.nlm_matrix["rungs"]
            if row["microtopic_ref"] == "MIC-PHY-NLM-FRAME-CHOICE"
        )
        self.assertFalse(frame["default_entry_eligible"])
        self.assertEqual(len(self.momentum_matrix["rungs"]), 1)
        self.assertFalse(
            self.momentum_matrix["rungs"][0]["default_entry_eligible"]
        )

    def test_no_core2b_question_was_added_as_a_side_effect(self):
        for package in (self.nlm, self.momentum):
            for q in package["questions"]:
                cores = {row["core"] for row in q.get("exposure", [])}
                self.assertNotIn("CORE2B", cores)


if __name__ == "__main__":
    unittest.main()
