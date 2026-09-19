"""Guard the Grade-9 Terminal-1 Pinnacle boundary against chapter-title overreach."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCOPE = REPO / "docs/grade9/terminal1-pinnacle-physics.micro-scope.json"
SOURCE = REPO / "docs/grade9/sources/TERMINAL1-PORTION-SHEET-2026-27.md"


class Terminal1PinnacleChapterOnlyGuard(unittest.TestCase):
    @classmethod
    def scope(cls):
        return json.loads(SCOPE.read_text(encoding="utf-8"))

    def test_school_authority_is_chapter_level_only(self):
        scope = self.scope()
        self.assertEqual(scope["source_scope"], "CHAPTER_LEVEL_ONLY")
        self.assertEqual(
            [row["school_label"] for row in scope["chapters"]],
            ["Vectors", "Motion 1 D", "Motion in 2 D", "NLM"],
        )
        self.assertTrue(
            all(row["school_demand"] == "CHAPTER_CONFIRMED" for row in scope["chapters"])
        )

    def test_no_microtopic_is_silently_promoted_from_chapter_title(self):
        scope = self.scope()
        rows = [micro for chapter in scope["chapters"] for micro in chapter["micro"]]
        self.assertGreater(len(rows), 20)
        self.assertTrue(
            all(micro["school_micro_demand"] == "MICRO_TO_CONFIRM" for micro in rows)
        )

    def test_known_local_gaps_remain_demand_gated(self):
        scope = self.scope()
        lookup = {
            (chapter["school_label"], micro["micro"]): micro
            for chapter in scope["chapters"]
            for micro in chapter["micro"]
        }
        guarded = {
            ("NLM", "momentum-transfer / rate-of-momentum force (recoil or ejection stream)"):
                "AUTHOR_EXPLICIT_DEMAND_EXTENSION",
            ("NLM", "momentum / impulse / conservation under an NLM chapter"):
                "DEFER_UNLESS_EXPLICITLY_DEMANDED",
        }
        for key, action in guarded.items():
            with self.subTest(chapter=key[0], micro=key[1]):
                row = lookup[key]
                self.assertEqual(row["local_state"], "LOCAL_GAP")
                self.assertEqual(row["school_micro_demand"], "MICRO_TO_CONFIRM")
                self.assertEqual(row["action"], action)


    def test_examside_can_confirm_external_question_demand_without_promoting_school_scope(self):
        scope = self.scope()
        lookup = {
            (chapter["school_label"], micro["micro"]): micro
            for chapter in scope["chapters"]
            for micro in chapter["micro"]
        }
        expected = {
            ("Vectors", "arbitrary-angle decomposition into x/y components"):
                "CAP-VEC-ANGLE-DECOMPOSITION",
            ("Motion in 2 D", "independence of orthogonal x/y motion coupled by common time"):
                "CAP-KIN-2D-INDEPENDENT-COMPONENTS",
            ("Motion in 2 D", "two-dimensional constant-acceleration component solving"):
                "CAP-KIN-2D-CONSTANT-ACCELERATION",
            ("Motion in 2 D", "horizontal projectile model"):
                "CAP-KIN-PROJECTILE-MODEL",
            ("Motion in 2 D", "oblique projectile model"):
                "CAP-KIN-PROJECTILE-MODEL",
        }
        for key, cap in expected.items():
            with self.subTest(chapter=key[0], micro=key[1]):
                row = lookup[key]
                self.assertEqual(row["school_micro_demand"], "MICRO_TO_CONFIRM")
                self.assertEqual(row["external_question_demand"], "CONFIRMED_EXAMSIDE")
                self.assertIn(cap, row["local_refs"])
                self.assertEqual(row["action"], "REUSE_IF_DEMANDED")

    def test_existing_extensions_stay_nondefault_until_explicit_demand(self):
        scope = self.scope()
        rows = {
            micro["micro"]: micro
            for chapter in scope["chapters"]
            for micro in chapter["micro"]
        }
        for name in (
            "zero velocity with nonzero acceleration at a turning point",
            "accelerating observer / pseudo-force convention",
        ):
            with self.subTest(micro=name):
                row = rows[name]
                self.assertEqual(row["local_state"], "LOCAL_EXTENSION_AVAILABLE")
                self.assertEqual(
                    row["action"],
                    "KEEP_NONDEFAULT_UNLESS_EXPLICITLY_DEMANDED",
                )

    def test_source_transcription_explicitly_denies_micro_scope_inference(self):
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("confirms only the chapter-level Terminal-1 boundary", text)
        self.assertIn("chapter title", text)
        self.assertIn("proof of every plausible subtopic", text)


if __name__ == "__main__":
    unittest.main()
