"""Planning guard for the Pinnacle Terminal-1 Grade-9 Physics micro-scope."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLAN = REPO / "docs/grade9/terminal1-pinnacle-physics.micro-scope.json"


class Terminal1PinnacleMicroScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(PLAN.read_text(encoding="utf-8"))
        cls.chapters = {
            row["school_label"]: row
            for row in cls.plan["chapters"]
        }

    def test_only_chapter_level_school_scope_is_currently_confirmed(self):
        self.assertEqual(self.plan["status"], "PLANNING_ONLY")
        self.assertEqual(self.plan["source_scope"], "CHAPTER_LEVEL_ONLY")
        self.assertEqual(
            set(self.chapters),
            {"Vectors", "Motion 1 D", "Motion in 2 D", "NLM"},
        )
        self.assertTrue(all(
            row["school_demand"] == "CHAPTER_CONFIRMED"
            for row in self.chapters.values()
        ))

    def test_no_microtopic_is_silently_promoted_without_school_evidence(self):
        rows = [
            micro
            for chapter in self.chapters.values()
            for micro in chapter["micro"]
        ]
        self.assertTrue(rows)
        self.assertEqual(
            {row["school_micro_demand"] for row in rows},
            {"MICRO_TO_CONFIRM"},
        )

    def test_motion2d_ready_foundations_remain_reusable_not_reauthored(self):
        rows = {
            row["micro"]: row
            for row in self.chapters["Motion in 2 D"]["micro"]
        }
        for name in (
            "vector representation and signed components in a plane",
            "vector addition/subtraction in common axes",
            "relative position at the same time",
            "relative velocity in a plane",
            "resultant-direction/component constraints such as river crossing",
        ):
            with self.subTest(micro=name):
                self.assertEqual(rows[name]["school_micro_demand"], "MICRO_TO_CONFIRM")
                self.assertEqual(rows[name]["local_state"], "LOCAL_READY_WITH_BRIDGE")
                self.assertEqual(rows[name]["action"], "REUSE_IF_DEMANDED")
                self.assertTrue(rows[name]["local_refs"])

    def test_motion2d_projectile_spine_is_a_local_gap_but_not_school_confirmed(self):
        rows = {
            row["micro"]: row
            for row in self.chapters["Motion in 2 D"]["micro"]
        }
        for name in (
            "arbitrary-angle initial-vector decomposition",
            "independence of orthogonal x/y motion coupled by common time",
            "two-dimensional constant-acceleration component solving",
            "horizontal projectile model",
            "oblique projectile model",
        ):
            with self.subTest(micro=name):
                self.assertEqual(rows[name]["local_state"], "LOCAL_GAP")
                self.assertEqual(rows[name]["school_micro_demand"], "MICRO_TO_CONFIRM")
                self.assertEqual(rows[name]["action"], "AUTHOR_ONLY_IF_CONFIRMED")
                self.assertEqual(rows[name].get("priority_if_confirmed"), "HIGH")
                self.assertEqual(rows[name]["local_refs"], [])

    def test_projectile_formula_outputs_are_not_predeclared_as_separate_capabilities(self):
        rows = {
            row["micro"]: row
            for row in self.chapters["Motion in 2 D"]["micro"]
        }
        row = rows["projectile time of flight / maximum height / range"]
        self.assertEqual(row["school_micro_demand"], "MICRO_TO_CONFIRM")
        self.assertEqual(row["local_state"], "LOCAL_GAP")
        self.assertEqual(
            row["action"],
            "TREAT_AS_APPLICATIONS_UNLESS_FAILURE_PROVES_SEPARATE_CAPABILITY",
        )

    def test_advanced_nlm_families_stay_demand_gated(self):
        rows = {
            row["micro"]: row
            for row in self.chapters["NLM"]["micro"]
        }
        for name in (
            "inclined-plane dynamics",
            "two-body contact-force systems",
            "string tension / connected bodies",
            "pulley constraints / connected acceleration",
            "coefficient-based static/kinetic friction calculations",
        ):
            with self.subTest(micro=name):
                self.assertEqual(rows[name]["school_micro_demand"], "MICRO_TO_CONFIRM")
                self.assertIn(rows[name]["local_state"], {"LOCAL_PARTIAL", "LOCAL_GAP"})
                self.assertNotEqual(rows[name]["action"], "REUSE_IF_DEMANDED")

    def test_nondefault_extensions_are_not_promoted_by_school_chapter_names(self):
        vector_turning = next(
            row for row in self.chapters["Motion 1 D"]["micro"]
            if row["micro"] == "zero velocity with nonzero acceleration at a turning point"
        )
        frame_choice = next(
            row for row in self.chapters["NLM"]["micro"]
            if row["micro"] == "accelerating observer / pseudo-force convention"
        )
        for row in (vector_turning, frame_choice):
            self.assertEqual(row["local_state"], "LOCAL_EXTENSION_AVAILABLE")
            self.assertEqual(row["school_micro_demand"], "MICRO_TO_CONFIRM")
            self.assertEqual(
                row["action"],
                "KEEP_NONDEFAULT_UNLESS_EXPLICITLY_DEMANDED",
            )


if __name__ == "__main__":
    unittest.main()
