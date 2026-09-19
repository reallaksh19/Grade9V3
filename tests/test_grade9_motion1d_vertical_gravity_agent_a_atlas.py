"""Agent A semantic Atlas packet for vertical 1-D constant-g integration."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import practice_inventory  # noqa: E402
from Shared.tools import feedback, resolve_request, session_readiness  # noqa: E402


class Grade9Motion1DVerticalGravityAgentAAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-kin-1d-motion.v1.json")
            .read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-kin-1d-motion.rungs.json")
            .read_text(encoding="utf-8")
        )
        cls.scope = json.loads(
            (REPO / "docs/grade9/terminal1-pinnacle-physics.micro-scope.json")
            .read_text(encoding="utf-8")
        )
        cls.records = resolve_request.library_records("Physics")
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.microtopics = {row["id"]: row for row in cls.package["microtopics"]}
        cls.capabilities = {row["id"]: row for row in cls.package["capabilities"]}
        cls.contexts = {
            row["id"]: row for row in cls.package.get("application_contexts", [])
        }
        cls.family = next(
            row for row in cls.package["question_families"]
            if row["id"] == "FAM-PHY-KIN-VERTICAL-GRAVITY"
        )
        cls.packet_rows = [
            row for row in cls.package["questions"]
            if row["extensions"].get("agent_a:packet")
            == "MOTION1D_VERTICAL_GRAVITY"
        ]

    def test_vertical_gravity_is_integration_not_new_capability(self):
        self.assertIn("CTX-PHY-KIN-VERTICAL-GRAVITY", self.contexts)
        capability_ids = set(self.capabilities)
        for forbidden in (
            "CAP-KIN-VERTICAL-MOTION",
            "CAP-KIN-FREE-FALL-SIGNS",
            "CAP-KIN-THROW-UP",
            "CAP-KIN-APEX-EVENT",
        ):
            self.assertNotIn(forbidden, capability_ids)

        self.assertEqual(
            set(self.family["capability_refs"]),
            {
                "CAP-KIN-CONSTANT-ACCELERATION",
                "CAP-KIN-ZERO-V-NONZERO-A",
                "CAP-KIN-DISTANCE-DISPLACEMENT",
                "CAP-KIN-MOTION-GRAPHS",
                "CAP-PHY-GRAV-FREE-FALL-G",
            },
        )

    def test_context_never_enters_prerequisite_topology(self):
        context_id = "CTX-PHY-KIN-VERTICAL-GRAVITY"
        for cap in self.package["capabilities"]:
            self.assertNotIn(context_id, cap.get("prerequisite_refs", []))
        for micro in self.package["microtopics"]:
            self.assertNotIn(context_id, micro.get("prerequisite_refs", []))

    def test_semantic_actions_make_sign_and_apex_boundaries_explicit(self):
        const_steps = {
            row["id"]: row
            for row in self.microtopics["MIC-PHY-KIN-CONSTANT-ACCELERATION"][
                "teaching_path"
            ]
        }
        apex_steps = {
            row["id"]: row
            for row in self.microtopics["MIC-PHY-KIN-ZERO-V-NONZERO-A"][
                "teaching_path"
            ]
        }
        self.assertIn("KIN4-6", const_steps)
        self.assertIn("+up -> a=-g", const_steps["KIN4-6"]["output"])
        self.assertIn("+down -> a=+g", const_steps["KIN4-6"]["output"])
        self.assertIn("KIN3-4", apex_steps)
        self.assertIn("v=0", apex_steps["KIN3-4"]["output"])
        self.assertIn("acceleration remains downward", apex_steps["KIN3-4"]["output"])

    def test_acceleration_does_not_flip_with_velocity(self):
        wrong = " ".join(
            row["wrong_idea"]
            for row in self.microtopics["MIC-PHY-KIN-CONSTANT-ACCELERATION"][
                "misconceptions"
            ]
        ).lower()
        self.assertIn(
            "gravitational acceleration is -g while the object rises and +g",
            wrong,
        )

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
            self.records, "BUCKET-PHY-KIN-1D-MOTION"
        )
        for row in core2a:
            self.assertIn(row["id"], inventory["CORE2A"])
        for row in core2b:
            self.assertIn(row["id"], inventory["CORE2B"])

    def test_every_packet_question_is_authored_and_context_bound(self):
        self.assertEqual(len(self.packet_rows), 10)
        for row in self.packet_rows:
            with self.subTest(question=row["id"]):
                self.assertEqual(row["origin"], "AUTHORED")
                self.assertEqual(row["source_refs"], ["SRC-AUTHOR-KIN-1D"])
                self.assertEqual(
                    row["context_refs"],
                    ["CTX-PHY-KIN-VERTICAL-GRAVITY"],
                )
                self.assertEqual(
                    row["family_ref"],
                    "FAM-PHY-KIN-VERTICAL-GRAVITY",
                )
                self.assertTrue(row.get("repair_ref"))
                self.assertLessEqual(len(row["secondary_capability_refs"]), 2)

    def test_transfer_set_spans_existing_dimensions(self):
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

    def test_model_choice_hint_does_not_reveal_acceleration_sign(self):
        q = self.questions["Q-PHY-KIN-VERT-2B-DIRECTION-SWITCH-04"]
        self.assertEqual(q["transfer"]["dimension"], "model_choice")
        self.assertEqual(
            {hint["reveals"] for hint in q["hints"]},
            {"CONCEPT"},
        )
        first = feedback.next_safe_hint(q, [])
        self.assertIsNotNone(first)
        self.assertEqual(first["reveals"], "CONCEPT")

    def test_upward_throw_witness_keeps_apex_acceleration_nonzero(self):
        q = self.questions["Q-PHY-KIN-VERT-2A-UPWARD-01"]
        self.assertIn("a=-g", q["answer"]["summary"])
        self.assertIn("t_top=u/g", q["answer"]["summary"])
        self.assertIn("H=u^2/(2g)", q["answer"]["summary"])

        apex = self.questions["Q-PHY-KIN-VERT-2A-APEX-05"]
        self.assertIn("v=0 but a=-g", apex["answer"]["summary"])

    def test_coordinate_reversal_changes_signs_not_physical_event(self):
        q = self.questions["Q-PHY-KIN-VERT-2B-REVERSED-AXIS-01"]
        self.assertIn("initial velocity is -u", q["answer"]["summary"])
        self.assertIn("acceleration is +g", q["answer"]["summary"])
        self.assertIn("u^2/(2g)", q["answer"]["summary"])
        self.assertIn("t_top=u/g", q["answer"]["summary"])

    def test_return_trip_keeps_displacement_and_distance_distinct(self):
        q = self.questions["Q-PHY-KIN-VERT-2A-RETURN-03"]
        self.assertIn("displacement is 0", q["answer"]["summary"])
        self.assertIn("distance is 2H=u^2/g", q["answer"]["summary"])
        self.assertIn("v=-u", q["answer"]["summary"])

    def test_velocity_time_transfer_preserves_slope_through_apex(self):
        q = self.questions["Q-PHY-KIN-VERT-2B-VT-GRAPH-05"]
        self.assertEqual(q["primary_capability_ref"], "CAP-KIN-MOTION-GRAPHS")
        self.assertIn("constant slope -g", q["answer"]["summary"])
        self.assertIn("t=u/g", q["answer"]["summary"])
        self.assertIn("t=2u/g", q["answer"]["summary"])

    def test_matrix_exposes_vertical_sign_and_turning_point_boundaries(self):
        by_rung = {row["rung"]: row for row in self.matrix["rungs"]}
        self.assertGreaterEqual(len(by_rung["R3"]["controlled_variation"]), 3)
        self.assertGreaterEqual(len(by_rung["R4"]["controlled_variation"]), 4)
        self.assertIn(
            "signed gravitational acceleration",
            " ".join(by_rung["R3"]["must_contain"]).lower(),
        )
        self.assertIn(
            "velocity changes sign",
            " ".join(
                row["notice"] for row in by_rung["R4"]["controlled_variation"]
            ).lower(),
        )

    def test_micro_scope_marks_local_readiness_without_school_promotion(self):
        motion = next(
            row for row in self.scope["chapters"]
            if row["school_label"] == "Motion 1 D"
        )
        vertical = next(
            row for row in motion["micro"]
            if row["micro"]
            == "vertical one-dimensional motion under gravity / sign handling"
        )
        self.assertEqual(vertical["local_state"], "LOCAL_READY_WITH_BRIDGE")
        self.assertEqual(vertical["school_micro_demand"], "MICRO_TO_CONFIRM")
        self.assertEqual(vertical["external_question_demand"], "CONFIRMED_EXAMSIDE")
        self.assertEqual(vertical["action"], "REUSE_IF_DEMANDED")
        self.assertIn("CAP-PHY-GRAV-FREE-FALL-G", vertical["local_refs"])

    def test_matrix_remains_session_ready(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-KIN-1D-MOTION",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertIn(
            report["status"],
            {session_readiness.READY, session_readiness.READY_WITH_BRIDGE},
        )


if __name__ == "__main__":
    unittest.main()
