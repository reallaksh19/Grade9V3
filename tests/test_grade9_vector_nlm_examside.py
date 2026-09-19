"""Owner-approved ExamSIDE Vector Algebra and NLM sources drive bounded Grade-9 Pinnacle extensions."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_route  # noqa: E402


class Grade9VectorNlmExamSide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vec = json.loads((REPO / "Physics/library/phy-vector-algebra-pinnacle.v1.json").read_text(encoding="utf-8"))
        cls.vec_matrix = json.loads((REPO / "Physics/matrices/phy-vector-algebra-pinnacle.rungs.json").read_text(encoding="utf-8"))
        cls.nlm = json.loads((REPO / "Physics/library/phy-nlm-applied-pinnacle.v1.json").read_text(encoding="utf-8"))
        cls.nlm_matrix = json.loads((REPO / "Physics/matrices/phy-nlm-applied-pinnacle.rungs.json").read_text(encoding="utf-8"))
        cls.vec_fixture = json.loads((REPO / "tests/fixtures/real_pilots/examside-vector-algebra-core.worksheet.json").read_text(encoding="utf-8"))
        cls.nlm_fixture = json.loads((REPO / "tests/fixtures/real_pilots/examside-nlm-pinnacle-core.worksheet.json").read_text(encoding="utf-8"))

    def test_vector_slice_has_three_durable_physics_actions(self):
        self.assertEqual([row["microtopic_ref"] for row in self.vec_matrix["rungs"]], ["MIC-PHY-VEC-DIRECTION-UNIT", "MIC-PHY-VEC-DOT-PRODUCT", "MIC-PHY-VEC-CROSS-PRODUCT"])
        caps = {row["id"] for row in self.vec["capabilities"]}
        self.assertTrue({"CAP-VEC-DIRECTION-UNIT", "CAP-VEC-DOT-PRODUCT", "CAP-VEC-CROSS-PRODUCT"} <= caps)
        bridge = next(row for row in self.vec["capabilities"] if row["id"] == "CAP-INVERSE-TRIG-BRIDGE")
        self.assertEqual(bridge["external_provider"], "Mathematics")
        self.assertEqual(bridge["acceptance_status"], "PROVIDER_REVIEW_REQUIRED")

    def test_applied_nlm_slice_has_three_durable_actions_not_story_caps(self):
        self.assertEqual([row["microtopic_ref"] for row in self.nlm_matrix["rungs"]], ["MIC-PHY-NLM-FRICTION-MAGNITUDE", "MIC-PHY-NLM-CONNECTED-SYSTEMS", "MIC-PHY-NLM-IMPULSE-MOMENTUM-RATE"])
        self.assertEqual({row["id"] for row in self.nlm["capabilities"]}, {"CAP-NLM-FRICTION-MAGNITUDE", "CAP-NLM-CONNECTED-SYSTEMS", "CAP-NLM-IMPULSE-MOMENTUM-RATE"})

    def test_external_sources_do_not_become_school_curriculum_mappings(self):
        self.assertEqual(self.vec["curriculum_mappings"], [])
        self.assertEqual(self.nlm["curriculum_mappings"], [])
        self.assertEqual(self.vec["buckets"][0]["curriculum_mappings"], [])
        self.assertEqual(self.nlm["buckets"][0]["curriculum_mappings"], [])

    def test_vector_fixture_routes_through_unit_dot_cross(self):
        report = study_route.resolve(self.vec_fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"]: row for row in report["route"]}
        for cap in ("CAP-VEC-DIRECTION-UNIT", "CAP-VEC-DOT-PRODUCT", "CAP-VEC-CROSS-PRODUCT"):
            self.assertIn(cap, route)

    def test_nlm_fixture_routes_through_friction_connections_and_momentum_rate(self):
        report = study_route.resolve(self.nlm_fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"]: row for row in report["route"]}
        for cap in ("CAP-NLM-FRICTION-MAGNITUDE", "CAP-NLM-CONNECTED-SYSTEMS", "CAP-NLM-IMPULSE-MOMENTUM-RATE"):
            self.assertIn(cap, route)
        self.assertIn("CAP-VEC-ANGLE-DECOMPOSITION", route)
        self.assertIn("CAP-NLM-THIRD-LAW", route)

    def test_vector_matrix_is_ready_with_math_bridge(self):
        report = session_readiness.audit("Physics", matrix_id="MATRIX-PHY-PINNACLE-VECTOR-ALGEBRA")
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertIn("CAP-INVERSE-TRIG-BRIDGE", {row["capability_ref"] for row in report["external_bridges"]})

    def test_nlm_matrix_is_session_ready(self):
        report = session_readiness.audit("Physics", matrix_id="MATRIX-PHY-PINNACLE-NLM-APPLIED")
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY)

    def test_momentum_slice_stops_before_collision_conservation(self):
        scope = " ".join(self.nlm["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("collision", scope)
        self.assertIn("rocket", scope)
        impulse = next(row for row in self.nlm["capabilities"] if row["id"] == "CAP-NLM-IMPULSE-MOMENTUM-RATE")
        self.assertNotIn("conservation", impulse["action"].lower())


if __name__ == "__main__":
    unittest.main()
