"""Importing a subtopic-intelligence packet: guarded, pinned, and honest about gaps.

The parallel tracks' own contract (PR #351, stage C5) records their packets as
DIGEST_PINNED_CANDIDATE_SOURCE_ONLY with packet_authority NONE and direct normative
import disallowed. These tests hold the importer to that: it refuses what the
substance gate rejects, it never fills a field the source has no answer for, and its
claim that intake will not admit the result is checked against intake rather than
asserted.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import import_sil  # noqa: E402
from Shared.library.intake import check  # noqa: E402

SOURCE = {"pr": "395", "head": "242878b04787905087060318c14b89b14238f195"}


def packet(gate_id, title, atoms, misconception, precondition, family):
    """One packet in the source layer's shape."""
    return {
        "gate_id": gate_id, "title": title, "domain": "Algebra", "grade_level": "Grade 9",
        "exam_families": ["CBSE", "JEE Main"], "preconditions": [precondition],
        "atoms": [{"atom_id": f"ATOM-{gate_id}-{n:02d}", "atom_type": kind, "description": text}
                  for n, (kind, text) in enumerate(atoms, 1)],
        "misconceptions": [{"name": "M", "flawed_action": misconception[0],
                            "diagnostic_cue": misconception[1]}],
        "ttus": [{"ttu_id": f"TTU-{gate_id}", "title": "Scaffold", "role": "Core1A",
                  "kind": "RECONSTRUCTABLE_SCAFFOLD", "viewport": "x in [-5, 5]",
                  "scaffold": "Step 1: [ ___ ]", "completion_key": "Step 1: done"}],
        "families": [{"family_id": f"FAM-{gate_id}", "tier": "CBSE", "description": family}],
    }


# Two packets that genuinely say different things. Written out rather than generated
# from a template, because a first attempt at this fixture interpolated the title into
# one fixed sentence -- and the gate correctly refused the lot of it.
CLEAN = [
    packet("A", "Linear systems",
           [("CONCEPT", "A pair of linear equations describes two lines, and a solution is a "
                        "point lying on both of them at once."),
            ("PROCEDURE", "Eliminate one unknown by scaling one equation until its coefficients "
                          "match, then subtracting."),
            ("INVARIANT", "Scaling an equation by a non-zero number leaves its line, and "
                          "therefore the solution set, exactly where it was.")],
           ("Reading parallel lines as having one solution because two equations were given.",
            "Compare the ratios of the coefficients before solving: equal ratios on the left "
            "with a different ratio on the right means no intersection exists."),
           "Both equations are written with the unknowns on the same side before the "
           "coefficients are compared.",
           "Two-equation systems solved by elimination and checked by substitution."),
    packet("B", "Quadratic forms",
           [("CONCEPT", "A quadratic expression traces a parabola whose turning point sits "
                        "halfway between its two roots."),
            ("PROCEDURE", "Complete the square by halving the coefficient of the linear term "
                          "and squaring it, then correcting the constant."),
            ("INVARIANT", "Completing the square rewrites the expression without changing its "
                          "value for any input.")],
           ("Taking the square root of both sides and keeping only the positive root.",
            "Ask what happens to a negative candidate: squaring destroys the sign, so both "
            "roots must be carried forward until one is ruled out on other grounds."),
           "The coefficient of the squared term is non-zero, or the expression is not "
           "quadratic at all.",
           "Roots found by completing the square and verified against the discriminant."),
]
# Two packets saying the same things as each other, which is the defect the gate exists
# to catch and the importer exists to refuse.
SHARED = "Apply the standard method to the system and check the boundary conditions."
TEMPLATED = [
    packet("C", "Circles", [("CONCEPT", SHARED), ("PROCEDURE", SHARED), ("INVARIANT", SHARED)],
           (SHARED, SHARED), SHARED, SHARED),
    packet("D", "Parabolas", [("CONCEPT", SHARED), ("PROCEDURE", SHARED), ("INVARIANT", SHARED)],
           (SHARED, SHARED), SHARED, SHARED),
]


class TheGateGuardsTheImport(unittest.TestCase):
    def test_a_packet_its_peers_duplicate_is_not_admissible(self):
        admissible, found = import_sil.admissible(TEMPLATED)
        self.assertEqual(admissible, set())
        self.assertTrue(found)

    def test_an_authored_packet_is_admissible(self):
        admissible, _ = import_sil.admissible(CLEAN)
        self.assertEqual(admissible, {"A", "B"})

    def test_the_command_refuses_a_rejected_packet_and_exits_non_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            catalog = Path(temp) / "catalog.js"
            catalog.write_text("window.SIL_CATALOG = " + json.dumps(TEMPLATED) + ";")
            result = subprocess.run(
                [sys.executable, "Shared/library/import_sil.py", str(catalog), "--packet", "C",
                 "--subject", "Mathematics", "--source-pr", "395", "--source-head", "abc"],
                cwd=REPO, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["status"], "REFUSED")


class TheImportIsPinnedAndHonest(unittest.TestCase):
    def setUp(self):
        self.package, self.gaps = import_sil.convert(CLEAN[0], subject="Mathematics", source=SOURCE)

    def test_every_imported_record_carries_the_packet_digest_it_came_from(self):
        pin = self.package["extensions"]["sil_import"]
        self.assertEqual(pin["import_mode"], "DIGEST_PINNED_CANDIDATE_SOURCE_ONLY")
        self.assertEqual(pin["packet_authority"], "NONE")
        self.assertEqual(pin["source_head"], SOURCE["head"])
        self.assertEqual(len(pin["packet_digest"]), 64)
        for collection in ("buckets", "microtopics"):
            for row in self.package[collection]:
                self.assertEqual(row["extensions"]["sil_import"]["packet_digest"],
                                 pin["packet_digest"])

    def test_the_import_is_a_candidate_and_claims_no_authority(self):
        self.assertEqual(self.package["status"], "CANDIDATE")
        self.assertEqual(self.package["microtopics"][0]["status"], "CANDIDATE")

    def test_nothing_the_source_lacks_is_invented(self):
        microtopic = self.package["microtopics"][0]
        self.assertNotIn("exit_task", microtopic, "a TTU scaffold is not an exit task")
        self.assertEqual(microtopic["badge_reason"], "")
        self.assertEqual(microtopic["research_contribution"], "")
        for item in microtopic["misconceptions"]:
            self.assertEqual(item["diagnostic_prompt"], "",
                             "the source pairs an action with a repair but asks nothing")
        for step in microtopic["teaching_path"]:
            self.assertEqual(step["why_valid"], "")

    def test_every_field_left_empty_is_named_in_the_gap_report(self):
        named = {gap["field"] for gap in self.gaps}
        for field in ("microtopic.badge_reason", "microtopic.exit_task",
                      "microtopic.research_contribution", "data",
                      "microtopic.teaching_path[].why_valid",
                      "microtopic.misconceptions[].diagnostic_prompt"):
            self.assertIn(field, named)

    def test_a_reading_the_importer_made_is_declared_as_its_own(self):
        # The source declares no step role; the importer reads one from the atom type.
        inferred = [g for g in self.gaps if g["kind"] == "IMPORTER_INFERRED"]
        self.assertTrue(inferred)
        for gap in inferred:
            self.assertIn("the importer's reading", gap["detail"])

    def test_a_ttu_is_held_as_candidate_input_rather_than_promoted(self):
        held = [g for g in self.gaps if g["kind"] == "TTU_CANDIDATE_NOT_PROMOTED"]
        self.assertEqual(len(held), len(CLEAN[0]["ttus"]))

    def test_intake_agrees_the_import_is_not_admissible(self):
        # The importer says so; this checks it against intake rather than taking its word.
        report = check(self.package)
        self.assertFalse(report["admitted"])
        points = {f["point"] for f in report["findings"]}
        self.assertTrue({"PATH", "MISCONCEPTION", "EXIT"} <= points, points)

    def test_the_gaps_are_the_reason_intake_refuses_it(self):
        # No finding should come from the importer emitting a malformed shape: every
        # structural complaint must be about something genuinely absent.
        report = check(self.package)
        for finding in report["findings"]:
            if finding["point"] == "STRUCTURE":
                self.assertTrue(
                    "should be non-empty" in finding["detail"]
                    or "is a required property" in finding["detail"],
                    f'importer emitted a bad shape rather than an absence: {finding["detail"]}')


if __name__ == "__main__":
    unittest.main()
