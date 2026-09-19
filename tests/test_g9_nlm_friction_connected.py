"""Bounded Grade-9 Pinnacle NLM friction and connected-body preparation slice."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, worksheet_study_plan  # noqa: E402


class Grade9NlmFrictionConnectedSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-nlm-first-law.v1.json").read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-nlm-first-law.rungs.json").read_text(encoding="utf-8")
        )
        cls.gates = json.loads(
            (REPO / "Physics/gates/foundational-relations.v1.json").read_text(encoding="utf-8")
        )
        cls.fixture = json.loads(
            (REPO / "tests/fixtures/real_pilots/examside-nlm-constraints.worksheet.json")
            .read_text(encoding="utf-8")
        )
        cls.scope = json.loads(
            (REPO / "docs/grade9/terminal1-pinnacle-physics.micro-scope.json")
            .read_text(encoding="utf-8")
        )
        cls.capabilities = {row["id"]: row for row in cls.package["capabilities"]}
        cls.microtopics = {row["id"]: row for row in cls.package["microtopics"]}
        cls.relations = {row["id"]: row for row in cls.package["relations"]}

    def test_existing_qualitative_friction_capability_is_not_silently_redefined(self):
        old = self.capabilities["CAP-NLM-FRICTION"]
        self.assertEqual(
            old["action"],
            "Identify friction as a contact force that opposes relative sliding or the tendency to slide.",
        )
        self.assertNotIn("mu_s", old["success_criterion"])
        quant = self.capabilities["CAP-NLM-FRICTION-QUANT"]
        self.assertEqual(
            quant["prerequisite_refs"],
            ["CAP-NLM-FRICTION", "CAP-NLM-SECOND-LAW"],
        )

    def test_static_friction_is_a_bound_not_an_unconditional_equality(self):
        rel = self.relations["REL-NLM-STATIC-FRICTION-BOUND"]
        self.assertEqual(rel["expression"], "|f_s| <= mu_s N")
        self.assertIn(
            "Equality |f_s| = mu_s N is used only at impending slip.",
            rel["conditions"],
        )
        micro = self.microtopics["MIC-PHY-NLM-FRICTION-QUANT"]
        text = " ".join(
            [micro["inferential_jump"]]
            + [step["action"] for step in micro["teaching_path"]]
            + [step["output"] for step in micro["teaching_path"]]
        )
        self.assertIn("do not assume N = mg", text)
        self.assertIn("|f_required| <= mu_s N", text)
        self.assertIn("only at impending slip", text)

    def test_kinetic_friction_requires_established_relative_sliding(self):
        rel = self.relations["REL-NLM-KINETIC-FRICTION"]
        self.assertEqual(rel["expression"], "|f_k| = mu_k N")
        self.assertIn(
            "Relative sliding between the two surfaces is established.",
            rel["conditions"],
        )

    def test_connected_body_capability_keeps_body_and_system_boundaries_distinct(self):
        cap = self.capabilities["CAP-NLM-CONNECTED-COMMON-ACCEL"]
        self.assertIn("relative separation", cap["success_criterion"])
        self.assertIn("whole-system force sum", cap["success_criterion"])
        micro = self.microtopics["MIC-PHY-NLM-CONNECTED-COMMON-ACCEL"]
        outputs = " ".join(step["output"] for step in micro["teaching_path"])
        self.assertIn("a_A = a_B = a", outputs)
        self.assertIn("Sigma F_A = m_A a", outputs)
        self.assertIn("internal pair absent only after equations are combined", outputs)

    def test_ideal_string_tension_is_model_conditional(self):
        rel = self.relations["REL-NLM-IDEAL-STRING-TENSION"]
        self.assertEqual(rel["expression"], "T_A = T_B = T")
        conditions = " ".join(rel["conditions"]).lower()
        self.assertIn("massless", conditions)
        self.assertIn("inextensible", conditions)
        self.assertIn("frictionless", conditions)
        micro = self.microtopics["MIC-PHY-NLM-IDEAL-STRING-TENSION"]
        self.assertIn(
            "equal tension is no longer guaranteed",
            micro["elicitation"]["boundary_test"]["answer"].lower(),
        )

    def test_fixed_pulley_constraint_is_derived_from_length_and_bounded(self):
        rel = self.relations["REL-NLM-FIXED-PULLEY-STRING-LENGTH"]
        self.assertEqual(
            rel["expression"],
            "y_A + y_B = L_free = constant; a_A + a_B = 0",
        )
        self.assertIn("The pulley itself does not translate.", rel["conditions"])
        micro = self.microtopics["MIC-PHY-NLM-SINGLE-STRING-CONSTRAINT"]
        self.assertIn(
            "movable pulley",
            micro["elicitation"]["boundary_test"]["answer"].lower(),
        )

    def test_library_relations_bind_exactly_to_the_contact_constraint_gate(self):
        gate = next(
            row for row in self.gates["gates"]
            if row["gate_id"] == "PHY-NLM-CONTACT-CONSTRAINTS"
        )
        gate_relations = {row["relation_id"]: row for row in gate["relations"]}
        expected = {
            "REL-NLM-STATIC-FRICTION-BOUND",
            "REL-NLM-KINETIC-FRICTION",
            "REL-NLM-COMMON-ACCEL-CONSTRAINT",
            "REL-NLM-IDEAL-STRING-TENSION",
            "REL-NLM-FIXED-PULLEY-STRING-LENGTH",
        }
        self.assertEqual(set(gate_relations), expected)
        for relation_id in expected:
            row = self.relations[relation_id]
            self.assertEqual(row["gate_relation_ref"], relation_id)
            self.assertEqual(row["expression"], gate_relations[relation_id]["expression"])
            self.assertEqual(row["conditions"], gate_relations[relation_id]["conditions"])

    def test_matrix_inserts_bounded_rungs_before_third_law_and_keeps_frame_nondefault(self):
        by_rung = {row["rung"]: row for row in self.matrix["rungs"]}
        self.assertEqual(
            [(r, by_rung[r]["ladder_position"]) for r in ("R8", "R9", "R10", "R11")],
            [("R8", 88), ("R9", 90), ("R10", 92), ("R11", 93)],
        )
        self.assertEqual(by_rung["R7"]["ladder_position"], 94)
        self.assertFalse(by_rung["R4"]["default_entry_eligible"])
        self.assertEqual(
            [by_rung[r]["microtopic_ref"] for r in ("R8", "R9", "R10", "R11")],
            [
                "MIC-PHY-NLM-FRICTION-QUANT",
                "MIC-PHY-NLM-CONNECTED-COMMON-ACCEL",
                "MIC-PHY-NLM-IDEAL-STRING-TENSION",
                "MIC-PHY-NLM-SINGLE-STRING-CONSTRAINT",
            ],
        )

    def test_matrix_remains_session_ready(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-NLM-FIRST-LAW",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY)

    def test_examside_fixture_routes_through_the_new_capabilities(self):
        report = worksheet_study_plan.resolve(self.fixture)
        self.assertTrue(report["passed"], report["findings"])
        by_cap = {row["capability_ref"]: row for row in report["route"]}
        for cap in (
            "CAP-NLM-FRICTION-QUANT",
            "CAP-NLM-CONNECTED-COMMON-ACCEL",
            "CAP-NLM-IDEAL-STRING-TENSION",
            "CAP-NLM-SINGLE-STRING-CONSTRAINT",
        ):
            self.assertIn(cap, by_cap)
        for row in self.fixture["questions"]:
            self.assertEqual(row["mapping_basis"], "AGENT_PROPOSAL")
            self.assertNotIn("canonical_question_ref", row)

    def test_micro_scope_keeps_school_demand_separate_from_examside_preparation(self):
        nlm = next(row for row in self.scope["chapters"] if row["school_label"] == "NLM")
        by_name = {row["micro"]: row for row in nlm["micro"]}
        for name in (
            "two-body contact-force systems",
            "string tension / connected bodies",
            "pulley constraints / connected acceleration",
            "coefficient-based static/kinetic friction calculations",
        ):
            self.assertEqual(by_name[name]["school_micro_demand"], "MICRO_TO_CONFIRM")
            self.assertEqual(by_name[name]["external_question_demand"], "CONFIRMED_EXAMSIDE")
        self.assertEqual(by_name["two-body contact-force systems"]["local_state"], "LOCAL_READY")
        self.assertEqual(by_name["string tension / connected bodies"]["local_state"], "LOCAL_READY")
        self.assertEqual(
            by_name["pulley constraints / connected acceleration"]["local_state"],
            "LOCAL_PARTIAL",
        )
        self.assertEqual(
            by_name["coefficient-based static/kinetic friction calculations"]["local_state"],
            "LOCAL_READY",
        )

    def test_momentum_transfer_stays_out_of_this_slice(self):
        new_ids = {
            "CAP-NLM-FRICTION-QUANT",
            "CAP-NLM-CONNECTED-COMMON-ACCEL",
            "CAP-NLM-IDEAL-STRING-TENSION",
            "CAP-NLM-SINGLE-STRING-CONSTRAINT",
        }
        for cap_id in new_ids:
            text = " ".join(
                [
                    self.capabilities[cap_id]["action"],
                    self.capabilities[cap_id]["success_criterion"],
                ]
            ).lower()
            self.assertNotIn("momentum", text)
        self.assertNotIn("CAP-NLM-MOMENTUM-TRANSFER", self.capabilities)


if __name__ == "__main__":
    unittest.main()
