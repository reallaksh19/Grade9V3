"""Grade-10 G10-1A closes the local spherical-mirror route without widening scope."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness  # noqa: E402


class Grade10ReflectionMirrorsScope(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(
            (REPO / "Physics/library/phy-optics-reflection-mirrors.v1.json").read_text()
        )
        self.matrix = json.loads(
            (REPO / "Physics/matrices/phy-optics-reflection-mirrors.rungs.json").read_text()
        )
        self.gates = json.loads(
            (REPO / "Physics/gates/foundational-relations.v1.json").read_text()
        )
        self.mics = {m["id"]: m for m in self.package["microtopics"]}
        self.caps = {c["id"]: c for c in self.package["capabilities"]}
        self.rels = {r["id"]: r for r in self.package["relations"]}

    def test_six_rung_spine_is_canonical_and_matrix_does_not_duplicate_teaching(self):
        self.assertEqual(len(self.matrix["rungs"]), 6)
        for row in self.matrix["rungs"]:
            ref = row["microtopic_ref"]
            self.assertIn(ref, self.mics)
            self.assertIn(self.mics[ref]["primary_capability_ref"], self.caps)
        for row in self.matrix["rungs"][3:]:
            self.assertEqual(row["provenance"], "AUTHORED")
            for duplicated in ("aha", "learner_owns", "misconception", "closure"):
                self.assertNotIn(duplicated, row)

    def test_mirror_relation_authority_matches_local_bound_copies(self):
        gate = next(g for g in self.gates["gates"] if g["gate_id"] == "PHY-OPTICS-MIRRORS-GRADE10")
        owned = {r["relation_id"]: r for r in gate["relations"]}
        for relation_id in ("REL-MIRROR-EQUATION", "REL-MIRROR-MAGNIFICATION"):
            self.assertIn(relation_id, owned)
            self.assertIn(relation_id, self.rels)
            self.assertEqual(self.rels[relation_id]["expression"], owned[relation_id]["expression"])
            self.assertEqual(self.rels[relation_id]["gate_relation_ref"], relation_id)

    def test_formula_use_keeps_sign_and_paraxial_model_boundary(self):
        mirror = self.rels["REL-MIRROR-EQUATION"]
        text = json.dumps(mirror).lower()
        self.assertEqual(mirror["expression"], "1/v + 1/u = 1/f")
        self.assertIn("paraxial", text)
        self.assertIn("cartesian sign", text)
        self.assertIn("no formula derivation is required", text)

    def test_magnification_keeps_orientation_in_the_sign(self):
        mag = self.rels["REL-MIRROR-MAGNIFICATION"]
        self.assertEqual(mag["expression"], "m = -v/u = h_i/h_o")
        text = json.dumps(self.mics["MIC-OPT-MIRROR-MAGNIFICATION"]).lower()
        self.assertIn("orientation", text)
        self.assertIn("negative", text)
        self.assertIn("|m|", text)

    def test_ray_construction_requires_consistent_independent_rays(self):
        text = json.dumps(self.mics["MIC-OPT-SPHERICAL-RAY-CONSTRUCTION"]).lower()
        self.assertIn("principal ray", text)
        self.assertIn("same image point", text)
        self.assertIn("backward", text)

    def test_refraction_and_later_optics_are_not_pulled_into_g10_1a(self):
        bucket = self.package["buckets"][0]
        excluded = " ".join(bucket["scope"]["excluded"]).lower()
        self.assertIn("refraction", excluded)
        self.assertIn("lens", excluded)
        self.assertIn("human-eye", excluded)
        self.assertIn("dispersion", excluded)
        capability_ids = set(self.caps)
        self.assertFalse(any("LENS" in cid or "REFRACT" in cid or "EYE" in cid for cid in capability_ids))

    def test_no_cross_repository_runtime_link(self):
        text = json.dumps(self.package)
        self.assertNotIn("reallaksh19/Common", text)
        self.assertNotIn("github.com", text)

    def test_curriculum_authority_is_not_fabricated(self):
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["curriculum_mappings"], [])
        self.assertEqual(self.package["buckets"][0]["curriculum_mappings"], [])
        gate = next(g for g in self.gates["gates"] if g["gate_id"] == "PHY-OPTICS-MIRRORS-GRADE10")
        self.assertEqual(gate["curriculum"]["scope_class"], "OWNER_EXTENSION")

    def test_mirror_matrix_becomes_session_ready(self):
        report = session_readiness.audit(
            "Physics", matrix_id="MATRIX-PHY-OPTICS-REFLECTION-MIRRORS"
        )
        self.assertEqual(report["status"], session_readiness.READY, report["findings"])
        self.assertTrue(report["passed"], report["findings"])


if __name__ == "__main__":
    unittest.main()
