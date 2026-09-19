"""Machine-gun momentum-rate content is a reachable explicit-demand extension, not default NLM progression."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness, study_route  # noqa: E402


class Grade9NlmMomentumRate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pkg = json.loads((REPO / "Physics/library/phy-nlm-momentum-rate-pinnacle.v1.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((REPO / "Physics/matrices/phy-nlm-momentum-rate-pinnacle.rungs.json").read_text(encoding="utf-8"))
        cls.fixture = json.loads((REPO / "tests/fixtures/real_pilots/examside-comedk-nlm-momentum-rate.worksheet.json").read_text(encoding="utf-8"))

    def test_single_bounded_capability(self):
        self.assertEqual([row["id"] for row in self.pkg["capabilities"]], ["CAP-NLM-MOMENTUM-TRANSFER-RATE"])

    def test_extension_is_nondefault(self):
        self.assertEqual(len(self.matrix["rungs"]), 1)
        self.assertFalse(self.matrix["rungs"][0]["default_entry_eligible"])

    def test_explicit_question_mapping_reaches_extension(self):
        report = study_route.resolve(self.fixture)
        self.assertTrue(report["valid"], report["findings"])
        route = {row["capability_ref"] for row in report["route"]}
        self.assertIn("CAP-NLM-MOMENTUM-TRANSFER-RATE", route)
        self.assertIn("CAP-NLM-THIRD-LAW", route)

    def test_collision_rocket_and_integral_depth_stay_out(self):
        excluded = " ".join(self.pkg["buckets"][0]["scope"]["excluded"]).lower()
        self.assertIn("collision", excluded)
        self.assertIn("rocket", excluded)
        self.assertIn("impulse-integral", excluded)
        action = self.pkg["capabilities"][0]["action"].lower()
        self.assertNotIn("conservation", action)

    def test_matrix_is_mechanically_session_ready(self):
        report = session_readiness.audit("Physics", matrix_id="MATRIX-PHY-PINNACLE-NLM-MOMENTUM-RATE")
        self.assertTrue(report["passed"], report["findings"])


if __name__ == "__main__":
    unittest.main()
