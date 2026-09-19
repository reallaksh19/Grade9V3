"""Grade-10 G10-1B closes refraction and spherical lenses without widening later optics."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness  # noqa: E402


class Grade10RefractionLensScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(
            (REPO / "Physics/library/phy-optics-refraction-lenses.v1.json").read_text()
        )
        cls.matrix = json.loads(
            (REPO / "Physics/matrices/phy-optics-refraction-lenses.rungs.json").read_text()
        )
        cls.gates = json.loads(
            (REPO / "Physics/gates/foundational-relations.v1.json").read_text()
        )
        cls.mics = {m["id"]: m for m in cls.package["microtopics"]}
        cls.caps = {c["id"]: c for c in cls.package["capabilities"]}
        cls.rels = {r["id"]: r for r in cls.package["relations"]}

    def test_nine_rung_spine_resolves_to_canonical_microtopics(self):
        self.assertEqual(len(self.matrix["rungs"]), 9)
        self.assertEqual(
            [r["ladder_position"] for r in self.matrix["rungs"]],
            sorted(r["ladder_position"] for r in self.matrix["rungs"]),
        )
        for row in self.matrix["rungs"]:
            ref = row["microtopic_ref"]
            self.assertIn(ref, self.mics)
            self.assertIn(self.mics[ref]["primary_capability_ref"], self.caps)
            self.assertEqual(row["provenance"], "AUTHORED")

    def test_general_image_geometry_is_reused_not_duplicated(self):
        ray = self.caps["CAP-OPT-LENS-RAY-CONSTRUCTION"]
        self.assertIn("CAP-OPT-REAL-VIRTUAL-IMAGE", ray["prerequisite_refs"])
        self.assertNotIn("CAP-OPT-REAL-VIRTUAL-IMAGE", self.caps)
        self.assertTrue(
            any("real/virtual" in text.lower()
                for text in self.package["buckets"][0]["scope"]["excluded"])
        )

    def test_gate_relations_match_local_bound_copies(self):
        gate = next(
            g for g in self.gates["gates"]
            if g["gate_id"] == "PHY-OPTICS-REFRACTION-LENSES-GRADE10"
        )
        owned = {r["relation_id"]: r for r in gate["relations"]}
        for rid in (
            "REL-REFRACTIVE-INDEX",
            "REL-LENS-EQUATION",
            "REL-LENS-MAGNIFICATION",
            "REL-LENS-POWER",
        ):
            self.assertIn(rid, owned)
            self.assertIn(rid, self.rels)
            self.assertEqual(self.rels[rid]["expression"], owned[rid]["expression"])
            self.assertEqual(self.rels[rid]["gate_relation_ref"], rid)

    def test_refraction_keeps_normal_medium_order_and_speed_inverse(self):
        relation = self.rels["REL-REFRACTIVE-INDEX"]
        self.assertEqual(
            relation["expression"],
            "n_21 = n_2/n_1 = sin(i)/sin(r) = v_1/v_2",
        )
        text = json.dumps(self.mics["MIC-OPT-REFRACTIVE-INDEX"]).lower()
        self.assertIn("medium order", text)
        self.assertIn("0/0", text)
        self.assertIn("lower light speed", text)

    def test_glass_slab_practical_keeps_parallel_not_collinear_distinction(self):
        text = json.dumps(self.mics["MIC-OPT-GLASS-SLAB-TRACE"]).lower()
        self.assertIn("parallel", text)
        self.assertIn("laterally displaced", text)
        self.assertIn("angle of incidence", text)
        self.assertIn("angle of refraction", text)
        self.assertIn("angle of emergence", text)

    def test_lens_formula_is_minus_form_and_model_bounded(self):
        lens = self.rels["REL-LENS-EQUATION"]
        self.assertEqual(lens["expression"], "1/v - 1/u = 1/f")
        text = json.dumps(lens).lower()
        self.assertIn("thin", text)
        self.assertIn("paraxial", text)
        self.assertIn("no formula derivation is required", text)
        self.assertNotIn("1/v + 1/u = 1/f", text)

    def test_lens_magnification_preserves_orientation_sign(self):
        self.assertEqual(
            self.rels["REL-LENS-MAGNIFICATION"]["expression"],
            "m = v/u = h_i/h_o",
        )
        text = json.dumps(self.mics["MIC-OPT-LENS-MAGNIFICATION"]).lower()
        self.assertIn("orientation", text)
        self.assertIn("negative", text)
        self.assertIn("|m|", text)

    def test_power_requires_metres_dioptres_and_sign(self):
        relation = self.rels["REL-LENS-POWER"]
        self.assertEqual(relation["expression"], "P = 1/f")
        text = json.dumps(self.mics["MIC-OPT-LENS-POWER"]).lower()
        self.assertIn("metres", text)
        self.assertIn("dioptre", text)
        self.assertIn("positive", text)
        self.assertIn("negative", text)

    def test_convex_lens_focal_length_practical_is_safe_and_approximate(self):
        text = json.dumps(self.mics["MIC-OPT-CONVEX-LENS-FOCAL-PRACTICAL"]).lower()
        self.assertIn("distant object", text)
        self.assertIn("screen", text)
        self.assertIn("optical-centre", text)
        self.assertIn("approx", text)
        self.assertIn("sun", text)

    def test_later_optics_are_outside_g10_1b(self):
        excluded = " ".join(self.package["buckets"][0]["scope"]["excluded"]).lower()
        for phrase in ("human-eye", "prism", "dispersion", "scattering", "total internal reflection"):
            self.assertIn(phrase, excluded)
        ids = set(self.caps)
        self.assertFalse(any("EYE" in cid or "PRISM" in cid or "DISPERSION" in cid for cid in ids))

    def test_no_cross_repository_runtime_link_or_fabricated_curriculum_authority(self):
        text = json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common", text)
        self.assertNotIn("github.com", text)
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"], [])
        self.assertEqual(self.package["buckets"][0]["curriculum_mappings"], [])
        gate = next(
            g for g in self.gates["gates"]
            if g["gate_id"] == "PHY-OPTICS-REFRACTION-LENSES-GRADE10"
        )
        self.assertEqual(gate["curriculum"]["scope_class"], "OWNER_EXTENSION")
        self.assertEqual(gate["tier"], "NOT_IN_JEE")

    def test_refraction_lens_matrix_is_session_ready(self):
        report = session_readiness.audit(
            "Physics", matrix_id="MATRIX-PHY-OPTICS-REFRACTION-LENSES"
        )
        self.assertEqual(report["status"], session_readiness.READY, report["findings"])
        self.assertTrue(report["passed"], report["findings"])


if __name__ == "__main__":
    unittest.main()
