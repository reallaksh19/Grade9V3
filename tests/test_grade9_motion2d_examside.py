"""Owner-approved ExamSIDE Motion-in-a-Plane slice closes the first durable 2D gaps."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_route  # noqa: E402


class Grade9Motion2DExamSide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-kin-2d-motion.v1.json").read_text(encoding="utf-8")
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-kin-2d-motion.rungs.json").read_text(encoding="utf-8")
        )
        cls.fixture = json.loads(
            (REPO / "tests/fixtures/real_pilots/examside-motion-in-plane-core.worksheet.json")
            .read_text(encoding="utf-8")
        )

    def test_three_rung_2d_spine_is_complete(self):
        self.assertEqual(
            [r["microtopic_ref"] for r in self.matrix["rungs"]],
            [
                "MIC-PHY-KIN-2D-INDEPENDENT-COMPONENTS",
                "MIC-PHY-KIN-2D-CONSTANT-ACCELERATION",
                "MIC-PHY-KIN-PROJECTILE-MODEL",
            ],
        )
        caps = {c["id"] for c in self.package["capabilities"]}
        self.assertEqual(
            caps,
            {
                "CAP-KIN-2D-INDEPENDENT-COMPONENTS",
                "CAP-KIN-2D-CONSTANT-ACCELERATION",
                "CAP-KIN-PROJECTILE-MODEL",
            },
        )

    def test_projectile_outputs_remain_applications_of_one_model(self):
        caps = {c["id"] for c in self.package["capabilities"]}
        self.assertFalse(any(
            token in cid
            for cid in caps
            for token in ("RANGE", "MAX-HEIGHT", "TIME-OF-FLIGHT", "HORIZONTAL-PROJECTILE", "OBLIQUE-PROJECTILE")
        ))
        micro = next(m for m in self.package["microtopics"] if m["id"] == "MIC-PHY-KIN-PROJECTILE-MODEL")
        text = json.dumps(micro).lower()
        self.assertIn("range", text)
        self.assertIn("height", text)
        self.assertIn("time", text)

    def test_exam_side_fixture_is_real_demand_not_canonical_question_custody(self):
        self.assertEqual(len(self.fixture["questions"]), 4)
        self.assertIn("ExamSIDE", self.fixture["source_note"])
        for row in self.fixture["questions"]:
            self.assertEqual(row["mapping_basis"], "AGENT_PROPOSAL")
            self.assertNotIn("canonical_question_ref", row)
            self.assertIn("https://questions.examside.com/", row["note"])

    def test_selected_questions_route_through_new_capabilities(self):
        report = study_route.resolve(self.fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"]: row for row in report["route"]}
        for cap in (
            "CAP-VEC-ANGLE-DECOMPOSITION",
            "CAP-KIN-2D-INDEPENDENT-COMPONENTS",
            "CAP-KIN-2D-CONSTANT-ACCELERATION",
            "CAP-KIN-PROJECTILE-MODEL",
        ):
            self.assertIn(cap, route)
        self.assertLess(
            route["CAP-KIN-2D-INDEPENDENT-COMPONENTS"]["order"],
            route["CAP-KIN-2D-CONSTANT-ACCELERATION"]["order"],
        )
        self.assertLess(
            route["CAP-KIN-2D-CONSTANT-ACCELERATION"]["order"],
            route["CAP-KIN-PROJECTILE-MODEL"]["order"],
        )

    def test_motion2d_matrix_is_session_ready_with_declared_bridges(self):
        report = session_readiness.audit(
            "Physics", matrix_id="MATRIX-PHY-KIN-2D-MOTION"
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertIn(
            report["status"],
            {session_readiness.READY, session_readiness.READY_WITH_BRIDGE},
        )

    def test_calculus_and_trajectory_derivation_remain_outside_first_slice(self):
        excluded = " ".join(self.package["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("calculus", excluded)
        self.assertIn("trajectory-equation", excluded)
        self.assertNotIn("differentiat", " ".join(c["action"].lower() for c in self.package["capabilities"]))


if __name__ == "__main__":
    unittest.main()
