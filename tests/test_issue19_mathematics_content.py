"""Issue #19 Mathematics content integrity tests.

The Mathematics slice deliberately stays small: one existing canonical linear-equations
package plus one matrix indexing its three authored microtopics. These checks prove that
a worksheet question can be traced through capability ownership and prerequisite closure
without inventing a second source of mathematical truth.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE_PATH = REPO / "Mathematics/library/linear-equations.v1.json"
MATRIX_PATH = REPO / "Mathematics/matrices/linear-equations.rungs.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Issue19MathematicsContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load(PACKAGE_PATH)
        cls.matrix = load(MATRIX_PATH)
        cls.capabilities = {row["id"]: row for row in cls.package["capabilities"]}
        cls.microtopics = {row["id"]: row for row in cls.package["microtopics"]}
        cls.questions = {row["id"]: row for row in cls.package["questions"]}
        cls.rung_by_microtopic = {
            row["microtopic_ref"]: row for row in cls.matrix["rungs"]
        }

    def test_matrix_closes_to_existing_microtopics_and_capabilities(self):
        self.assertEqual(self.matrix["bucket_id"], "BUCKET-LINEAR-EQUATION")
        self.assertEqual(
            [row["microtopic_ref"] for row in self.matrix["rungs"]],
            [
                "MIC-MATH-CONSTRAINT",
                "MIC-MATH-EQUIVALENT-OPS",
                "MIC-MATH-EXACT-SOLUTION",
            ],
        )
        self.assertEqual(
            [row["ladder_position"] for row in self.matrix["rungs"]],
            [20, 60, 100],
        )
        for rung in self.matrix["rungs"]:
            self.assertEqual(rung["provenance"], "AUTHORED")
            self.assertNotIn("aha", rung)
            self.assertNotIn("learner_owns", rung)
            self.assertNotIn("misconception", rung)
            self.assertNotIn("closure", rung)
            self.assertTrue(rung["ceiling"])
            self.assertTrue(rung["controlled_variation"])
            mic = self.microtopics[rung["microtopic_ref"]]
            self.assertEqual(mic["bucket_id"], self.matrix["bucket_id"])
            self.assertIn(mic["primary_capability_ref"], self.capabilities)

    def test_capability_prerequisite_chain_is_explicit_and_acyclic(self):
        self.assertEqual(
            self.capabilities["CAP-MATH-SUBSTITUTE"]["prerequisite_refs"], []
        )
        self.assertEqual(
            self.capabilities["CAP-MATH-ISOLATE"]["prerequisite_refs"],
            ["CAP-MATH-SUBSTITUTE"],
        )
        self.assertEqual(
            self.capabilities["CAP-MATH-EXACTNESS"]["prerequisite_refs"],
            ["CAP-MATH-ISOLATE"],
        )

        visiting, done = set(), set()

        def visit(cap_id, stack):
            self.assertIn(cap_id, self.capabilities, (stack, cap_id))
            if cap_id in done:
                return
            self.assertNotIn(cap_id, visiting, " -> ".join(stack + [cap_id]))
            visiting.add(cap_id)
            for prereq in self.capabilities[cap_id]["prerequisite_refs"]:
                visit(prereq, stack + [cap_id])
            visiting.remove(cap_id)
            done.add(cap_id)

        for cap_id in self.capabilities:
            visit(cap_id, [])

    def test_each_capability_is_taught_by_a_real_matrix_rung(self):
        teaching = {}
        for mic in self.microtopics.values():
            teaching.setdefault(mic["primary_capability_ref"], []).append(mic["id"])

        for cap_id in (
            "CAP-MATH-SUBSTITUTE",
            "CAP-MATH-ISOLATE",
            "CAP-MATH-EXACTNESS",
        ):
            self.assertEqual(len(teaching.get(cap_id, [])), 1, cap_id)
            mic_id = teaching[cap_id][0]
            self.assertIn(mic_id, self.rung_by_microtopic, cap_id)

    def test_representative_question_maps_sparsely_and_resolves(self):
        q = self.questions["Q-MATH-LINEAR-01"]
        self.assertEqual(q["primary_capability_ref"], "CAP-MATH-ISOLATE")
        self.assertEqual(
            q["secondary_capability_refs"],
            ["CAP-MATH-EXACTNESS", "CAP-MATH-SUBSTITUTE"],
        )
        self.assertLessEqual(len(q["secondary_capability_refs"]), 2)
        for cap_id in [q["primary_capability_ref"], *q["secondary_capability_refs"]]:
            self.assertIn(cap_id, self.capabilities)

    def test_question_to_rung_trace_requires_no_guessing(self):
        q = self.questions["Q-MATH-LINEAR-01"]
        expected = {
            "CAP-MATH-ISOLATE": "MIC-MATH-EQUIVALENT-OPS",
            "CAP-MATH-EXACTNESS": "MIC-MATH-EXACT-SOLUTION",
            "CAP-MATH-SUBSTITUTE": "MIC-MATH-CONSTRAINT",
        }
        for cap_id, mic_id in expected.items():
            self.assertEqual(
                self.microtopics[mic_id]["primary_capability_ref"], cap_id
            )
            self.assertIn(mic_id, self.rung_by_microtopic)

    def test_question_ownership_follows_primary_capability(self):
        q = self.questions["Q-MATH-LINEAR-01"]
        primary = q["primary_capability_ref"]
        owner_microtopics = [
            mic for mic in self.microtopics.values()
            if mic["primary_capability_ref"] == primary
        ]
        self.assertEqual(len(owner_microtopics), 1)
        self.assertEqual(
            owner_microtopics[0]["bucket_id"], "BUCKET-LINEAR-EQUATION"
        )

    def test_owner_extension_and_authored_provenance_remain_truthful(self):
        package_mapping = self.package["curriculum_mappings"]
        bucket_mapping = self.package["buckets"][0]["curriculum_mappings"]
        for mapping in [*package_mapping, *bucket_mapping]:
            self.assertEqual(mapping["scope_class"], "OWNER_EXTENSION")
            self.assertEqual(mapping["mapping_status"], "CANDIDATE")
            self.assertEqual(mapping["source_ref"], "SRC-MATH-AUTHOR")

        resource = self.package["resources"][0]
        self.assertEqual(resource["id"], "SRC-MATH-AUTHOR")
        self.assertEqual(resource["origin"], "AUTHORED")

        q = self.questions["Q-MATH-LINEAR-01"]
        self.assertEqual(q["status"], "CANDIDATE")
        self.assertEqual(q["origin"], "AUTHORED")
        self.assertEqual(q["origin_ref"], "SRC-MATH-AUTHOR")
        self.assertIn("SRC-MATH-AUTHOR", q["source_refs"])

    def test_matrix_contains_no_learner_specific_state(self):
        payload = json.dumps(self.matrix).lower()
        for forbidden in (
            "knowledge_percent",
            "needs revision",
            "weak in",
            "learner score",
            "mastery probability",
        ):
            self.assertNotIn(forbidden, payload)


if __name__ == "__main__":
    unittest.main()
