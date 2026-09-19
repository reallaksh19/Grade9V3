"""Bounded Grade-9 Vector direction/unit preparation slice from owner-approved ExamSIDE demand."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, worksheet_study_plan  # noqa: E402


class Grade9VectorDirectionUnitSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-vector-direction-unit.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-vector-direction-unit.rungs.json").read_text(
                encoding="utf-8"
            )
        )
        cls.fixture = json.loads(
            (
                REPO
                / "tests/fixtures/real_pilots/examside-vector-algebra.worksheet.json"
            ).read_text(encoding="utf-8")
        )
        cls.gates = json.loads(
            (REPO / "Physics/gates/motion-vectors.v1.json").read_text(encoding="utf-8")
        )

    def test_matrix_is_exactly_the_bounded_three_rung_slice(self):
        self.assertEqual(
            [row["rung"] for row in self.matrix["rungs"]],
            ["R1", "R2", "R3"],
        )
        self.assertEqual(
            [row["microtopic_ref"] for row in self.matrix["rungs"]],
            [
                "MIC-PHY-VEC-UNIT-NOTATION",
                "MIC-PHY-VEC-DIRECTION-FROM-COMPONENTS",
                "MIC-PHY-VEC-UNIT-DIRECTION",
            ],
        )
        self.assertEqual(
            self.matrix["bucket_id"],
            "BUCKET-PHY-VEC-DIRECTION-UNIT",
        )

    def test_inverse_trig_is_explicit_external_math_bridge(self):
        caps = {row["id"]: row for row in self.package["capabilities"]}
        bridge = caps["CAP-INVERSE-TRIG-DIRECTION-BRIDGE"]
        self.assertEqual(bridge["external_provider"], "Mathematics")
        self.assertEqual(bridge["acceptance_status"], "PROVIDER_REVIEW_REQUIRED")
        self.assertEqual(
            caps["CAP-VEC-DIRECTION-FROM-COMPONENTS"]["prerequisite_refs"],
            [
                "CAP-VECTOR-SIGNED-COMPONENT",
                "CAP-INVERSE-TRIG-DIRECTION-BRIDGE",
            ],
        )

    def test_unit_direction_does_not_require_direction_angle(self):
        caps = {row["id"]: row for row in self.package["capabilities"]}
        prereqs = caps["CAP-VEC-UNIT-DIRECTION"]["prerequisite_refs"]
        self.assertEqual(
            prereqs,
            ["CAP-VEC-UNIT-NOTATION", "CAP-RIGHT-TRIANGLE-BRIDGE"],
        )
        self.assertNotIn("CAP-VEC-DIRECTION-FROM-COMPONENTS", prereqs)
        self.assertNotIn("CAP-INVERSE-TRIG-DIRECTION-BRIDGE", prereqs)

    def test_zero_vector_normalization_boundary_is_explicit(self):
        micro = {row["id"]: row for row in self.package["microtopics"]}
        unit = micro["MIC-PHY-VEC-UNIT-DIRECTION"]
        boundary = unit["elicitation"]["boundary_test"]
        self.assertIn("zero vector", boundary["prompt"].lower())
        self.assertIn("divide by zero", boundary["answer"].lower())
        self.assertIn("|v|>0", unit["teaching_path"][0]["output"])

    def test_direction_recovery_is_quadrant_first_not_raw_inverse_tangent(self):
        micro = {row["id"]: row for row in self.package["microtopics"]}
        direction = micro["MIC-PHY-VEC-DIRECTION-FROM-COMPONENTS"]
        actions = " ".join(step["action"] for step in direction["teaching_path"])
        self.assertIn("signs", actions)
        self.assertIn("quadrant", actions)
        self.assertIn("acute reference angle", actions)
        self.assertIn("rather than reporting tan^-1(v_y/v_x) blindly",
                      {row["id"]: row for row in self.package["capabilities"]}[
                          "CAP-VEC-DIRECTION-FROM-COMPONENTS"
                      ]["success_criterion"])

    def test_library_relations_bind_to_the_new_gate_relations(self):
        library = {row["id"]: row for row in self.package["relations"]}
        gate = next(
            row for row in self.gates["gates"]
            if row["gate_id"] == "PHY-VEC-DIRECTION-UNIT"
        )
        gate_relations = {row["relation_id"]: row for row in gate["relations"]}
        self.assertEqual(set(library), set(gate_relations))
        for relation_id, row in library.items():
            self.assertEqual(row["gate_relation_ref"], relation_id)
            self.assertEqual(row["expression"], gate_relations[relation_id]["expression"])
            self.assertEqual(row["conditions"], gate_relations[relation_id]["conditions"])

    def test_matrix_is_session_ready_with_declared_bridges(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VEC-DIRECTION-UNIT",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertNotIn(
            "READINESS_PREREQUISITE_AMBIGUOUS",
            [row["point"] for row in report["blocking_findings"]],
        )

    def test_examside_demand_fixture_routes_without_becoming_canonical_questions(self):
        report = worksheet_study_plan.resolve(self.fixture)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(len(report["questions"]), 3)
        by_cap = {row["capability_ref"]: row for row in report["route"]}
        for cap in (
            "CAP-VEC-UNIT-NOTATION",
            "CAP-VEC-DIRECTION-FROM-COMPONENTS",
            "CAP-VEC-UNIT-DIRECTION",
        ):
            self.assertIn(cap, by_cap)
        bridge = by_cap["CAP-INVERSE-TRIG-DIRECTION-BRIDGE"]
        self.assertEqual(bridge["state"], "EXTERNAL_BRIDGE")
        self.assertEqual(bridge["external_provider"], "Mathematics")
        for row in self.fixture["questions"]:
            self.assertEqual(row["mapping_basis"], "AGENT_PROPOSAL")
            self.assertNotIn("canonical_question_ref", row)

    def test_learner_facing_teaching_does_not_leak_deferred_vector_breadth(self):
        banned = ("dot product", "cross product", "three-dimensional", "calculus")
        learner_text = []
        for micro in self.package["microtopics"]:
            learner_text.extend(
                [
                    micro["title"],
                    micro["inferential_jump"],
                    micro["exit_task"]["prompt"],
                    micro["exit_task"]["answer"]["summary"],
                ]
            )
            learner_text.extend(step["action"] for step in micro["teaching_path"])
            learner_text.extend(step["output"] for step in micro["teaching_path"])
        joined = " ".join(learner_text).lower()
        for phrase in banned:
            self.assertNotIn(phrase, joined)


if __name__ == "__main__":
    unittest.main()
