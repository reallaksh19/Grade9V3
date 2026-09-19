"""Bounded ExamSIDE Vector direction/unit slice stays within the merged reconnaissance boundary."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_route  # noqa: E402


class Grade9VectorDirectionUnit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pkg = json.loads((REPO / "Physics/library/phy-vector-direction-unit-pinnacle.v1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((REPO / "Physics/matrices/phy-vector-direction-unit-pinnacle.rungs.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((REPO / "tests/fixtures/real_pilots/examside-vector-direction-unit.worksheet.json").read_text(encoding="utf-8"))

    def test_exact_bounded_capability_spine(self):
        caps = {row["id"] for row in self.pkg["capabilities"] if row.get("external_provider") is None}
        self.assertEqual(caps, {"CAP-VEC-DIRECTION-FROM-COMPONENTS", "CAP-VEC-UNIT-NOTATION", "CAP-VEC-UNIT-DIRECTION"})

    def test_inverse_trig_stays_a_math_bridge(self):
        bridge = next(row for row in self.pkg["capabilities"] if row["id"] == "CAP-INVERSE-TRIG-BRIDGE")
        self.assertEqual(bridge["external_provider"], "Mathematics")
        self.assertEqual(bridge["acceptance_status"], "PROVIDER_REVIEW_REQUIRED")

    def test_dot_cross_3d_calculus_are_not_authored(self):
        blob = json.dumps(self.pkg).lower()
        excluded = " ".join(self.pkg["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("dot", excluded)
        self.assertIn("cross", excluded)
        self.assertIn("three-dimensional", excluded)
        self.assertIn("calculus", excluded)
        cap_ids = {row["id"].lower() for row in self.pkg["capabilities"]}
        self.assertFalse(any("dot" in x or "cross" in x for x in cap_ids))

    def test_fixture_routes_through_all_three_actions(self):
        report = study_route.resolve(self.fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"] for row in report["route"]}
        self.assertTrue({"CAP-VEC-DIRECTION-FROM-COMPONENTS", "CAP-VEC-UNIT-NOTATION", "CAP-VEC-UNIT-DIRECTION"} <= route)

    def test_matrix_is_ready_with_explicit_math_bridge(self):
        report = session_readiness.audit("Physics", matrix_id="MATRIX-PHY-PINNACLE-VECTOR-DIRECTION-UNIT")
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertIn("CAP-INVERSE-TRIG-BRIDGE", {row["capability_ref"] for row in report["external_bridges"]})


if __name__ == "__main__":
    unittest.main()
