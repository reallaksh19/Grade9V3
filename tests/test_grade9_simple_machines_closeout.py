"""Close the Grade-9 Physics authoring pass without widening scope."""
from __future__ import annotations
import json, sys, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO))
from Shared.tools import session_readiness  # noqa: E402

class Grade9SimpleMachinesAndCloseout(unittest.TestCase):
    def setUp(self):
        self.package=json.loads((REPO/"Physics/library/phy-simple-machines.v1.json").read_text())
        self.matrix=json.loads((REPO/"Physics/matrices/phy-simple-machines.rungs.json").read_text())
        self.mics={m["id"]:m for m in self.package["microtopics"]}

    def test_simple_machine_spine_remains_three_reusable_capabilities(self):
        self.assertEqual(len(self.matrix["rungs"]),3)
        self.assertEqual(
            [self.mics[r["microtopic_ref"]]["primary_capability_ref"] for r in self.matrix["rungs"]],
            ["CAP-MACHINE-TRADEOFF","CAP-MACHINE-MA","CAP-MACHINE-COMPARE"],
        )

    def test_ideal_vs_real_boundary_is_explicit_without_efficiency_formula(self):
        row=json.dumps(self.mics["MIC-PHY-MACHINE-TRADEOFF"]).lower()
        self.assertIn("ideal",row)
        self.assertIn("real",row)
        self.assertIn("loss",row)
        expressions=" ".join(r["expression"] for r in self.package["relations"]).lower()
        self.assertNotIn("efficiency",expressions)

    def test_no_cross_repository_runtime_link(self):
        text=json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common",text)
        self.assertNotIn("github.com",text)

    def test_all_six_grade9_production_matrices_are_session_ready(self):
        matrix_ids=[
            "MATRIX-PHY-KIN-1D-MOTION",
            "MATRIX-PHY-NLM-FIRST-LAW",
            "MATRIX-PHY-GRAV-UNIVERSAL-LAW",
            "MATRIX-PHY-WORK-ENERGY-POWER",
            "MATRIX-PHY-SOUND",
            "MATRIX-PHY-SIMPLE-MACHINES",
        ]
        for matrix_id in matrix_ids:
            with self.subTest(matrix_id=matrix_id):
                report=session_readiness.audit("Physics",matrix_id=matrix_id)
                self.assertEqual(report["status"],session_readiness.READY,report["findings"])
                self.assertTrue(report["passed"],report["findings"])

    def test_matrix_schema_stays_grade_neutral(self):
        forbidden={"grade","grade_level","class","syllabus_status"}
        self.assertFalse(forbidden & set(self.matrix))

if __name__=="__main__":
    unittest.main()
