"""Explicit-demand Grade-9 NLM momentum-transfer force extension."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, worksheet_study_plan  # noqa: E402


class Grade9NlmMomentumTransferExtension(unittest.TestCase):
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
        cls.nlm = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.nlm_matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.gates = json.loads(
            (REPO / "Physics/gates/foundational-relations.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.fixture = json.loads(
            (REPO / "tests/fixtures/real_pilots/examside-nlm-momentum-transfer.worksheet.json")
            .read_text(encoding="utf-8")
        )
        cls.scope = json.loads(
            (REPO / "docs/grade9/terminal1-pinnacle-physics.micro-scope.json")
            .read_text(encoding="utf-8")
        )
        cls.cap = cls.package["capabilities"][0]
        cls.micro = cls.package["microtopics"][0]
        cls.relations = {row["id"]: row for row in cls.package["relations"]}

    def test_existing_newton_second_law_is_not_broadened_to_hide_the_extension(self):
        second = next(
            row for row in self.nlm["capabilities"]
            if row["id"] == "CAP-NLM-SECOND-LAW"
        )
        self.assertEqual(
            second["action"],
            "Relate signed net external force to acceleration with F_net = m a.",
        )
        self.assertNotIn("momentum", second["action"].lower())
        self.assertNotIn("dp/dt", second["success_criterion"])
        self.assertEqual(self.cap["id"], "CAP-NLM-MOMENTUM-TRANSFER-RATE")
        self.assertIn("CAP-NLM-SECOND-LAW", self.cap["prerequisite_refs"])

    def test_extension_is_physically_separate_from_the_default_nlm_matrix(self):
        self.assertEqual(
            self.matrix["bucket_id"],
            "BUCKET-PHY-NLM-MOMENTUM-TRANSFER",
        )
        self.assertEqual(len(self.matrix["rungs"]), 1)
        self.assertFalse(self.matrix["rungs"][0]["default_entry_eligible"])
        default_refs = {
            row.get("microtopic_ref") for row in self.nlm_matrix["rungs"]
        }
        self.assertNotIn(
            "MIC-PHY-NLM-MOMENTUM-TRANSFER-RATE",
            default_refs,
        )
        self.assertNotIn(
            "CAP-NLM-MOMENTUM-TRANSFER-RATE",
            {
                ref
                for cap in self.nlm["capabilities"]
                for ref in cap.get("prerequisite_refs", [])
            },
        )

    def test_per_item_momentum_uses_final_minus_initial_in_one_frame(self):
        rel = self.relations["REL-NLM-LINEAR-MOMENTUM-ITEM"]
        self.assertEqual(rel["expression"], "p = m v")
        outputs = " ".join(
            step["output"] for step in self.micro["teaching_path"]
        )
        self.assertIn("Delta p_item = m(v_out - v_in)", outputs)
        self.assertIn("same inertial frame", " ".join(rel["conditions"]))

    def test_force_rate_and_discrete_stream_relations_are_explicit(self):
        self.assertEqual(
            self.relations["REL-NLM-FORCE-MOMENTUM-RATE"]["expression"],
            "F_ext = dp/dt",
        )
        self.assertEqual(
            self.relations["REL-NLM-DISCRETE-MOMENTUM-TRANSFER"]["expression"],
            "F_avg,on_ejecta = R Delta p_item",
        )
        outputs = " ".join(
            step["output"] for step in self.micro["teaching_path"]
        )
        self.assertIn(
            "F_avg,on_ejecta = Delta p_total/Delta t = (n/Delta t) Delta p_item = R Delta p_item",
            outputs,
        )

    def test_recoil_and_holding_force_directions_are_not_conflated(self):
        step = next(
            row for row in self.micro["teaching_path"]
            if row["id"] == "NLM-MTR-4"
        )
        self.assertIn(
            "F_avg,on_launcher_by_ejecta = -R Delta p_item",
            step["output"],
        )
        self.assertIn(
            "F_avg,holding_on_launcher = +R Delta p_item",
            step["output"],
        )
        self.assertIn(
            "opposite the ejection direction",
            self.micro["elicitation"]["predict"]["defensible_answer"].lower(),
        )

    def test_units_reduce_to_force_without_importing_calculus_work(self):
        step = next(
            row for row in self.micro["teaching_path"]
            if row["id"] == "NLM-MTR-5"
        )
        self.assertIn("(1/s)(kg m/s) = kg m/s^2 = N", step["output"])
        force_rel = self.relations["REL-NLM-FORCE-MOMENTUM-RATE"]
        self.assertIn(
            "no derivative calculation is required",
            " ".join(force_rel["conditions"]).lower(),
        )

    def test_library_relations_bind_exactly_to_gate_authority(self):
        gate = next(
            row for row in self.gates["gates"]
            if row["gate_id"] == "PHY-NLM-MOMENTUM-TRANSFER-RATE"
        )
        authority = {row["relation_id"]: row for row in gate["relations"]}
        self.assertEqual(set(authority), set(self.relations))
        for relation_id, row in self.relations.items():
            self.assertEqual(row["gate_relation_ref"], relation_id)
            self.assertEqual(row["expression"], authority[relation_id]["expression"])
            self.assertEqual(row["conditions"], authority[relation_id]["conditions"])

    def test_extension_matrix_is_teachable_but_nondefault(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-NLM-MOMENTUM-TRANSFER",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY)
        self.assertFalse(self.matrix["rungs"][0]["default_entry_eligible"])

    def test_owner_supplied_examside_demand_routes_cleanly(self):
        report = worksheet_study_plan.resolve(self.fixture)
        self.assertTrue(report["passed"], report["findings"])
        by_cap = {row["capability_ref"]: row for row in report["route"]}
        self.assertIn("CAP-NLM-MOMENTUM-TRANSFER-RATE", by_cap)
        for prereq in (
            "CAP-NLM-FBD-BODY-OWNERSHIP",
            "CAP-NLM-SECOND-LAW",
            "CAP-NLM-THIRD-LAW",
        ):
            self.assertIn(prereq, by_cap)
        q = self.fixture["questions"][0]
        self.assertEqual(q["mapping_basis"], "AGENT_PROPOSAL")
        self.assertNotIn("canonical_question_ref", q)

    def test_micro_scope_marks_it_as_available_extension_not_school_scope(self):
        nlm = next(
            row for row in self.scope["chapters"]
            if row["school_label"] == "NLM"
        )
        row = next(
            item for item in nlm["micro"]
            if item["micro"] ==
            "momentum-transfer / rate-of-momentum force (recoil or ejection stream)"
        )
        self.assertEqual(row["school_micro_demand"], "MICRO_TO_CONFIRM")
        self.assertEqual(row["external_question_demand"], "CONFIRMED_EXAMSIDE")
        self.assertEqual(row["local_state"], "LOCAL_EXTENSION_AVAILABLE")
        self.assertEqual(
            row["action"],
            "KEEP_NONDEFAULT_UNLESS_EXPLICITLY_DEMANDED",
        )
        self.assertIn("CAP-NLM-MOMENTUM-TRANSFER-RATE", row["local_refs"])

    def test_full_momentum_collision_and_rocket_breadth_remains_excluded(self):
        scope = self.package["buckets"][0]["scope"]
        excluded = " ".join(scope["excluded"]).lower()
        for phrase in (
            "collision",
            "impulse",
            "rocket",
            "varying-mass",
            "center-of-mass",
        ):
            self.assertIn(phrase, excluded)
        learner_text = " ".join(
            [
                self.micro["title"],
                self.micro["inferential_jump"],
                self.micro["exit_task"]["prompt"],
                self.micro["exit_task"]["answer"]["summary"],
            ]
            + [step["action"] for step in self.micro["teaching_path"]]
        ).lower()
        self.assertNotIn("coefficient of restitution", learner_text)
        self.assertNotIn("rocket equation", learner_text)
        self.assertNotIn("impulse integral", learner_text)


if __name__ == "__main__":
    unittest.main()
