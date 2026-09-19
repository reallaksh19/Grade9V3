"""Grade-9 Work/Energy donor adaptation stays local and preserves model conditions."""
from __future__ import annotations
import json, sys, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
from Shared.tools import session_readiness  # noqa: E402

class Grade9WorkEnergyScope(unittest.TestCase):
    def setUp(self):
        self.package=json.loads((REPO/"Physics/library/phy-work-energy-power.v1.json").read_text())
        self.matrix=json.loads((REPO/"Physics/matrices/phy-work-energy-power.rungs.json").read_text())
        self.mics={m["id"]:m for m in self.package["microtopics"]}
        self.caps={c["id"]:c for c in self.package["capabilities"]}

    def test_existing_capability_spine_is_reused(self):
        self.assertEqual(len(self.matrix["rungs"]),7)
        for rung in self.matrix["rungs"]:
            ref=rung["microtopic_ref"]
            self.assertIn(ref,self.mics)
            self.assertIn(self.mics[ref]["primary_capability_ref"],self.caps)

    def test_mechanical_conservation_is_explicitly_conditional(self):
        row=self.mics["MIC-PHY-WEP-MECH-ENERGY-CONDITION"]
        text=json.dumps(row).lower()
        self.assertIn("system boundary",text)
        self.assertIn("total energy",text)
        self.assertIn("non-conservative",text)
        self.assertIn("not",text)
        self.assertIn("destroy",text)

    def test_constant_force_and_reference_conditions_remain_owned_relations(self):
        rels={r["id"]:r for r in self.package["relations"]}
        self.assertIn("constant over the displacement"," ".join(rels["REL-WORK-CONSTANT-FORCE"]["conditions"]).lower())
        self.assertIn("same body and reference frame"," ".join(rels["REL-WORK-ENERGY-THEOREM"]["conditions"]).lower())
        self.assertIn("same potential-energy reference"," ".join(rels["REL-MECHANICAL-ENERGY-CONSERVATION"]["conditions"]).lower())

    def test_no_cross_repository_runtime_link(self):
        text=json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common",text)
        self.assertNotIn("github.com",text)

    def test_grade9_wep_remains_session_ready(self):
        report=session_readiness.audit("Physics",matrix_id="MATRIX-PHY-WORK-ENERGY-POWER")
        self.assertEqual(report["status"],session_readiness.READY)
        self.assertTrue(report["passed"],report["findings"])

if __name__=="__main__":
    unittest.main()
