"""Grade-9 Sound donor adaptation stays local and preserves acoustic invariants."""
from __future__ import annotations
import json, sys, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
from Shared.tools import session_readiness  # noqa: E402

class Grade9SoundScope(unittest.TestCase):
    def setUp(self):
        self.package=json.loads((REPO/"Physics/library/phy-sound.v1.json").read_text())
        self.matrix=json.loads((REPO/"Physics/matrices/phy-sound.rungs.json").read_text())
        self.mics={m["id"]:m for m in self.package["microtopics"]}

    def test_existing_five_capability_spine_is_reused(self):
        self.assertEqual(len(self.matrix["rungs"]),5)
        for rung in self.matrix["rungs"]:
            self.assertIn(rung["microtopic_ref"],self.mics)

    def test_longitudinal_representation_is_explicit(self):
        text=json.dumps(self.mics["MIC-PHY-SOUND-LONGITUDINAL"]).lower()
        self.assertIn("compression",text)
        self.assertIn("rarefaction",text)
        self.assertIn("parallel",text)
        self.assertIn("density",text)
        self.assertIn("pressure",text)

    def test_wave_relation_keeps_same_wave_medium_condition(self):
        rel=next(r for r in self.package["relations"] if r["id"]=="REL-WAVE-SPEED")
        cond=" ".join(rel["conditions"]).lower()
        self.assertIn("same wave",cond)
        self.assertIn("same medium",cond)

    def test_echo_model_uses_round_trip_without_universal_threshold(self):
        mic=json.dumps(self.mics["MIC-PHY-SOUND-REFLECTION"]).lower()
        self.assertIn("round-trip",mic)
        self.assertIn("factor",mic)
        self.assertNotIn("17.2",mic)
        self.assertNotIn("minimum time 0.1",mic)

    def test_no_cross_repository_runtime_link(self):
        text=json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common",text)
        self.assertNotIn("github.com",text)

    def test_sound_remains_session_ready(self):
        report=session_readiness.audit("Physics",matrix_id="MATRIX-PHY-SOUND")
        self.assertEqual(report["status"],session_readiness.READY)
        self.assertTrue(report["passed"],report["findings"])

if __name__=="__main__":
    unittest.main()
