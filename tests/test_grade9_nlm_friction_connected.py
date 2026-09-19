"""Bounded ExamSIDE NLM friction/connected slice follows the merged reconnaissance stop condition."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_route  # noqa: E402


class Grade9NlmFrictionConnected(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pkg = json.loads((REPO / "Physics/library/phy-nlm-friction-connected-pinnacle.v1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((REPO / "Physics/matrices/phy-nlm-friction-connected-pinnacle.rungs.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((REPO / "tests/fixtures/real_pilots/examside-nlm-friction-connected.worksheet.json").read_text(encoding="utf-8"))

    def test_exact_first_production_capability_spine(self):
        self.assertEqual({row["id"] for row in self.pkg["capabilities"]}, {"CAP-NLM-FRICTION-MAGNITUDE", "CAP-NLM-CONNECTED-ACCELERATION", "CAP-NLM-IDEAL-STRING"})

    def test_momentum_and_nonideal_depth_stay_out(self):
        excluded = " ".join(self.pkg["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("momentum", excluded)
        self.assertIn("massive strings", excluded)
        self.assertIn("pulley rotational inertia", excluded)
        self.assertFalse(any("momentum" in row["id"].lower() for row in self.pkg["capabilities"]))

    def test_fixture_routes_through_all_three_actions(self):
        report = study_route.resolve(self.fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"] for row in report["route"]}
        self.assertTrue({"CAP-NLM-FRICTION-MAGNITUDE", "CAP-NLM-CONNECTED-ACCELERATION", "CAP-NLM-IDEAL-STRING"} <= route)
        self.assertIn("CAP-NLM-FBD-BODY-OWNERSHIP", route)
        self.assertIn("CAP-NLM-SECOND-LAW", route)

    def test_matrix_is_session_ready(self):
        report = session_readiness.audit("Physics", matrix_id="MATRIX-PHY-PINNACLE-NLM-FRICTION-CONNECTED")
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY)

    def test_existing_frame_choice_remains_nondefault(self):
        base = json.loads((REPO / "Physics/matrices/phy-nlm-first-law.rungs.json").read_text(encoding="utf-8"))
        frame = next(row for row in base["rungs"] if row.get("microtopic_ref") == "MIC-PHY-NLM-FRAME-CHOICE")
        self.assertFalse(frame["default_entry_eligible"])


if __name__ == "__main__":
    unittest.main()
