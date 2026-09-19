"""Vector foundation modernization keeps capability granularity and real demand aligned."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_map, study_route  # noqa: E402


class VectorFoundationsModernization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = json.loads(
            (REPO / "Physics/library/vector-representation.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.ops = json.loads(
            (REPO / "Physics/library/phy-vec-add-sub.v1.json").read_text(
                encoding="utf-8"
            )
        )
        cls.ops_matrix = json.loads(
            (REPO / "Physics/matrices/phy-vec-add-sub.rungs.json").read_text(
                encoding="utf-8"
            )
        )

    def test_vector_representation_r1_and_r2_are_distinct_capabilities(self):
        micro = {row["id"]: row for row in self.rep["microtopics"]}
        self.assertEqual(
            micro["MIC-VECTOR-VS-SCALAR"]["primary_capability_ref"],
            "CAP-VECTOR-VS-SCALAR",
        )
        self.assertEqual(
            micro["MIC-SIGNED-COMPONENT"]["primary_capability_ref"],
            "CAP-VECTOR-SIGNED-COMPONENT",
        )
        self.assertNotEqual(
            micro["MIC-VECTOR-VS-SCALAR"]["primary_capability_ref"],
            micro["MIC-SIGNED-COMPONENT"]["primary_capability_ref"],
        )

    def test_each_vector_representation_capability_has_one_teaching_location(self):
        locations = study_map.capability_locations("Physics")
        for cap in (
            "CAP-VECTOR-VS-SCALAR",
            "CAP-VECTOR-SIGNED-COMPONENT",
            "CAP-GRAPHICAL-SUBTRACT",
        ):
            self.assertEqual(len(locations[cap]), 1, (cap, locations[cap]))

    def test_graphical_subtraction_depends_on_signed_components_not_broad_alias(self):
        caps = {row["id"]: row for row in self.rep["capabilities"]}
        self.assertEqual(
            caps["CAP-GRAPHICAL-SUBTRACT"]["prerequisite_refs"],
            ["CAP-VECTOR-SIGNED-COMPONENT"],
        )
        self.assertEqual(
            caps["CAP-VECTOR-SIGNED-COMPONENT"]["prerequisite_refs"],
            ["CAP-VECTOR-VS-SCALAR", "CAP-SIGNED-PAIR-BRIDGE"],
        )
        self.assertEqual(
            caps["CAP-VECTOR-VS-SCALAR"]["prerequisite_refs"],
            [],
        )

    def test_vector_representation_has_core1a_core1b_for_every_matrix_rung(self):
        matrix = json.loads(
            (REPO / "Physics/matrices/vector-representation.rungs.json").read_text(
                encoding="utf-8"
            )
        )
        matrix_microtopics = {
            row["microtopic_ref"]
            for row in matrix["rungs"]
        }
        route_coverage = {"CORE1A": set(), "CORE1B": set()}
        for route in self.rep["teaching_routes"]:
            for core in route["cores"]:
                if core in route_coverage:
                    route_coverage[core].update(route["microtopic_refs"])
        self.assertTrue(matrix_microtopics <= route_coverage["CORE1A"])
        self.assertTrue(matrix_microtopics <= route_coverage["CORE1B"])
        micro = {row["id"]: row for row in self.rep["microtopics"]}
        for ref in matrix_microtopics:
            self.assertTrue(micro[ref].get("elicitation"), ref)

    def test_vector_representation_is_ready_with_only_explicit_math_bridge(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VECTOR-REPRESENTATION",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertNotIn(
            "READINESS_PREREQUISITE_AMBIGUOUS",
            [row["point"] for row in report["blocking_findings"]],
        )
        self.assertNotIn(
            "READINESS_CORE1A_ROUTE_MISSING",
            [row["point"] for row in report["support_findings"]],
        )
        self.assertNotIn(
            "READINESS_CORE1B_ROUTE_MISSING",
            [row["point"] for row in report["support_findings"]],
        )

    def test_active_vector_add_sub_matrix_contains_demanded_four_rungs(self):
        self.assertEqual(
            [row["rung"] for row in self.ops_matrix["rungs"]],
            ["R1", "R2", "R3", "R4"],
        )
        self.assertEqual(
            [row["microtopic_ref"] for row in self.ops_matrix["rungs"]],
            [
                "MIC-PHY-VEC-COMPONENT-SUM",
                "MIC-PHY-VEC-RESULTANT-CONSTRAINT",
                "MIC-PHY-VEC-SUB-ORDER",
                "MIC-PHY-VEC-ANGLE-DECOMPOSITION",
            ],
        )
        self.assertTrue(
            any(
                row["id"] == "ISS-VEC-CROSS-PRODUCT-DEFERRED"
                for row in self.ops["known_issues"]
            )
        )

    def test_vector_add_sub_matrix_is_ready_without_ambiguity(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VEC-ADD-SUB",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        points = [row["point"] for row in report["blocking_findings"]]
        self.assertNotIn("READINESS_PREREQUISITE_AMBIGUOUS", points)
        self.assertNotIn("READINESS_RUNG_MICROTOPIC_MISSING", points)

    def test_neetprep_q4_q5_now_route_to_reusable_vector_capability(self):
        mapping = json.loads(
            (
                REPO
                / "tests/fixtures/real_pilots/neetprep-relative-motion.worksheet.json"
            ).read_text(encoding="utf-8")
        )
        by_id = {row["question_id"]: row for row in mapping["questions"]}
        for qid in ("NEETPREP-MQB-REL-Q4", "NEETPREP-MQB-REL-Q5"):
            self.assertEqual(
                by_id[qid]["primary_capability_ref"],
                "CAP-VEC-RESULTANT-CONSTRAINT",
            )

        report = study_route.resolve(mapping)
        self.assertTrue(report["valid"], report["findings"])
        self.assertNotIn(
            "STUDY_ROUTE_CAPABILITY_AMBIGUOUS",
            [row["point"] for row in report["findings"]],
        )
        route = {row["capability_ref"]: row for row in report["route"]}
        self.assertIn("CAP-VEC-COMPONENT-SUM", route)
        self.assertIn("CAP-VEC-RESULTANT-CONSTRAINT", route)
        self.assertLess(
            route["CAP-VEC-COMPONENT-SUM"]["order"],
            route["CAP-VEC-RESULTANT-CONSTRAINT"]["order"],
        )

    def test_angle_decomposition_is_now_real_demand_backed_with_math_bridge(self):
        caps = {row["id"]: row for row in self.ops["capabilities"]}
        cap = caps["CAP-VEC-ANGLE-DECOMPOSITION"]
        self.assertEqual(
            cap["prerequisite_refs"],
            ["CAP-VECTOR-SIGNED-COMPONENT", "CAP-TRIG-RATIO-BRIDGE"],
        )
        self.assertIn(
            "REL-VEC-ANGLE-COMPONENTS",
            {row["id"] for row in self.ops["relations"]},
        )
        self.assertFalse(any(
            row["id"] == "ISS-VEC-ANGLE-DECOMPOSITION-MATH"
            for row in self.ops["known_issues"]
        ))
        report = session_readiness.audit(
            "Physics", matrix_id="MATRIX-PHY-VEC-ADD-SUB"
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)


if __name__ == "__main__":
    unittest.main()
