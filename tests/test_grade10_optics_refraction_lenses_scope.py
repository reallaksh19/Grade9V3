"""Grade-10 G10-1B closes refraction/lens self-study without widening later optics."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness  # noqa: E402


class Grade10RefractionLensesScope(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(
            (REPO / "Physics/library/phy-optics-refraction-lenses.v1.json").read_text()
        )
        self.matrix = json.loads(
            (REPO / "Physics/matrices/phy-optics-refraction-lenses.rungs.json").read_text()
        )
        self.gates = json.loads(
            (REPO / "Physics/gates/foundational-relations.v1.json").read_text()
        )
        self.mics = {m["id"]: m for m in self.package["microtopics"]}
        self.caps = {c["id"]: c for c in self.package["capabilities"]}
        self.rels = {r["id"]: r for r in self.package["relations"]}

    def test_six_rung_spine_is_canonical(self):
        self.assertEqual(len(self.matrix["rungs"]), 6)
        for row in self.matrix["rungs"]:
            ref = row["microtopic_ref"]
            self.assertIn(ref, self.mics)
            self.assertIn(self.mics[ref]["primary_capability_ref"], self.caps)
            self.assertEqual(row["provenance"], "AUTHORED")

    def test_relation_authority_matches_local_bound_copies(self):
        gate = next(g for g in self.gates["gates"] if g["gate_id"] == "PHY-OPTICS-LENSES-GRADE10")
        owned = {r["relation_id"]: r for r in gate["relations"]}
        for relation_id in (
            "REL-SNELLS-LAW",
            "REL-REFRACTIVE-INDEX-SPEED",
            "REL-LENS-EQUATION",
            "REL-LENS-MAGNIFICATION",
            "REL-LENS-POWER",
        ):
            self.assertIn(relation_id, owned)
            self.assertIn(relation_id, self.rels)
            self.assertEqual(self.rels[relation_id]["expression"], owned[relation_id]["expression"])
            self.assertEqual(self.rels[relation_id]["gate_relation_ref"], relation_id)

    def test_refraction_keeps_normal_and_medium_ownership(self):
        text = json.dumps(self.mics["MIC-OPT-REFRACTION-NORMAL"]).lower()
        self.assertIn("normal", text)
        self.assertIn("parallel-sided glass slab", text)
        self.assertIn("toward", text)
        self.assertIn("away", text)

        snell = self.rels["REL-SNELLS-LAW"]
        self.assertEqual(snell["expression"], "n_1 sin(i) = n_2 sin(r)")
        self.assertTrue(any("normal" in row.lower() for row in snell["conditions"]))

    def test_index_keeps_speed_meaning(self):
        relation = self.rels["REL-REFRACTIVE-INDEX-SPEED"]
        self.assertEqual(relation["expression"], "n = c/v")
        text = json.dumps(self.mics["MIC-OPT-REFRACTIVE-INDEX-SNELL"]).lower()
        self.assertIn("higher n", text)
        self.assertIn("lower", text)
        self.assertIn("speed", text)

    def test_lens_formula_keeps_sign_and_model_boundary(self):
        lens = self.rels["REL-LENS-EQUATION"]
        self.assertEqual(lens["expression"], "1/v - 1/u = 1/f")
        text = json.dumps(self.mics["MIC-OPT-LENS-EQUATION"]).lower()
        self.assertIn("paraxial", text)
        self.assertIn("thin", text)
        self.assertIn("formula derivation a learner requirement", text)

    def test_lens_magnification_keeps_orientation(self):
        mag = self.rels["REL-LENS-MAGNIFICATION"]
        self.assertEqual(mag["expression"], "m = v/u = h_i/h_o")
        text = json.dumps(self.mics["MIC-OPT-LENS-MAGNIFICATION"]).lower()
        self.assertIn("orientation", text)
        self.assertIn("negative", text)
        self.assertIn("|m|", text)

    def test_lens_power_keeps_metres_and_sign(self):
        power = self.rels["REL-LENS-POWER"]
        self.assertEqual(power["expression"], "P = 1/f")
        text = json.dumps(self.mics["MIC-OPT-LENS-POWER"]).lower()
        self.assertIn("metres", text)
        self.assertIn("dioptre", text)
        self.assertIn("sign", text)

    def test_principal_rays_are_independent_and_practical_is_bounded(self):
        text = json.dumps(self.mics["MIC-OPT-LENS-RAY-CONSTRUCTION"]).lower()
        self.assertIn("principal ray", text)
        self.assertIn("independent", text)
        self.assertIn("distant object", text)
        self.assertNotIn("sun is required", text)

    def test_later_optics_are_not_pulled_into_g10_1b(self):
        bucket = self.package["buckets"][0]
        excluded = " ".join(bucket["scope"]["excluded"]).lower()
        self.assertIn("human-eye", excluded)
        self.assertIn("dispersion", excluded)
        self.assertIn("wave-optics", excluded)
        capability_ids = set(self.caps)
        self.assertFalse(any("EYE" in cid or "DISPERSION" in cid for cid in capability_ids))

    def test_no_cross_repository_runtime_link(self):
        text = json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common", text)
        self.assertNotIn("github.com", text)

    def test_curriculum_authority_is_not_fabricated(self):
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"], [])
        self.assertEqual(self.package["buckets"][0]["curriculum_mappings"], [])
        gate = next(g for g in self.gates["gates"] if g["gate_id"] == "PHY-OPTICS-LENSES-GRADE10")
        self.assertEqual(gate["curriculum"]["scope_class"], "OWNER_EXTENSION")

    def test_refraction_lens_matrix_becomes_session_ready(self):
        report = session_readiness.audit(
            "Physics", matrix_id="MATRIX-PHY-OPTICS-REFRACTION-LENSES"
        )
        self.assertEqual(report["status"], session_readiness.READY, report["findings"])
        self.assertTrue(report["passed"], report["findings"])


if __name__ == "__main__":
    unittest.main()