"""Grade-9 Simple Machines closes the active Grade-9 authoring pass."""
from __future__ import annotations
import json, sys, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
from Shared.tools import session_readiness  # noqa: E402

class Grade9SimpleMachinesScope(unittest.TestCase):
    def setUp(self):
        self.package=json.loads((REPO/"Physics/library/phy-simple-machines.v1.json").read_text())
        self.matrix=json.loads((REPO/"Physics/matrices/phy-simple-machines.rungs.json").read_text())
        self.mics={m["id"]:m for m in self.package["microtopics"]}
        self.caps={c["id"]:c for c in self.package["capabilities"]}
        self.bucket=self.package["buckets"][0]

    def test_three_rung_spine_reuses_current_canonical_content(self):
        self.assertEqual(len(self.matrix["rungs"]),3)
        for rung in self.matrix["rungs"]:
            ref=rung["microtopic_ref"]
            self.assertIn(ref,self.mics)
            self.assertIn(self.mics[ref]["primary_capability_ref"],self.caps)

    def test_ma_owns_same_state_measurement_and_practical_reasoning(self):
        cap=self.caps["CAP-MACHINE-MA"]
        mic=self.mics["MIC-PHY-MACHINE-MA"]
        text=json.dumps([cap,mic]).lower()
        self.assertIn("same machine state",text)
        self.assertIn("same steady",text)
        self.assertIn("load",text)
        self.assertIn("effort",text)
        self.assertIn("dimensionless",text)
        practical=next(q for q in self.package["questions"] if q["id"]=="Q-PHY-MACHINE-PRACTICAL-11")
        self.assertEqual(practical["primary_capability_ref"],"CAP-MACHINE-MA")

    def test_higher_depth_machine_formulae_are_not_pulled_down(self):
        scope=" ".join(self.bucket["scope"]["excluded"]).lower()
        self.assertIn("pulley-system",scope)
        self.assertIn("torque",scope)
        self.assertIn("efficiency",scope)

    def test_authority_and_matrix_contract_boundaries_hold(self):
        self.assertEqual(self.package["status"],"CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"],[])
        self.assertEqual(self.bucket["curriculum_mappings"],[])
        forbidden={"grade","grade_level","class","syllabus_status"}
        self.assertFalse(forbidden & set(self.matrix))

    def test_simple_machines_remains_session_ready(self):
        report=session_readiness.audit("Physics",matrix_id="MATRIX-PHY-SIMPLE-MACHINES")
        self.assertEqual(report["status"],session_readiness.READY)
        self.assertTrue(report["passed"],report["findings"])

if __name__=="__main__":
    unittest.main()
