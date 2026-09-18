"""Cross-matrix study routing follows capability prerequisites, never ladder positions."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError  # noqa: E402
from Shared.tools import capability_graph, study_route  # noqa: E402


class CrossMatrixStudyRoute(unittest.TestCase):
    FIXTURE = REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json"

    def mapping(self):
        return json.loads(self.FIXTURE.read_text(encoding="utf-8"))

    def test_prerequisites_order_the_real_cross_matrix_fixture(self):
        # The subject content may legitimately refine prerequisite edges over time.
        # Assert the architecture invariant rather than freezing one historical topology:
        # every known dependency in the resolved slice must appear before its dependant.
        report = study_route.resolve(self.mapping())
        self.assertTrue(report["passed"], report["findings"])
        positions = {
            row["capability_ref"]: row["order"]
            for row in report["route"]
        }
        self.assertTrue(positions)
        for row in report["route"]:
            for dependency in row["depends_on"]:
                with self.subTest(capability=row["capability_ref"], dependency=dependency):
                    self.assertIn(dependency, positions)
                    self.assertLess(positions[dependency], row["order"])

    def test_cross_matrix_ladder_positions_do_not_order_the_route(self):
        # Architecture falsifier independent of current Physics pedagogy. Put prerequisite
        # A at local position 90 in one matrix and dependant B at local position 10 in a
        # different matrix. Global study order must still be A -> B.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Example/library").mkdir(parents=True)
            (root / "Example/matrices").mkdir(parents=True)
            (root / "Shared/library").mkdir(parents=True)
            (root / "Shared/library/worksheet-map.schema.json").write_text(
                (REPO / "Shared/library/worksheet-map.schema.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (root / "Example/library/example.json").write_text(json.dumps({
                "capabilities": [
                    {
                        "id": "CAP-A",
                        "action": "Do A",
                        "success_criterion": "A is done",
                        "prerequisite_refs": [],
                    },
                    {
                        "id": "CAP-B",
                        "action": "Do B",
                        "success_criterion": "B is done",
                        "prerequisite_refs": ["CAP-A"],
                    },
                ],
                "microtopics": [
                    {"id": "MIC-A", "primary_capability_ref": "CAP-A"},
                    {"id": "MIC-B", "primary_capability_ref": "CAP-B"},
                ],
                "questions": [],
            }), encoding="utf-8")
            (root / "Example/matrices/a.rungs.json").write_text(json.dumps({
                "matrix_id": "MATRIX-A",
                "bucket_id": "BUCKET-A",
                "topic": "Example",
                "subtopic": "A",
                "rungs": [{
                    "rung": "R-A",
                    "ladder_position": 90,
                    "microtopic_ref": "MIC-A",
                }],
            }), encoding="utf-8")
            (root / "Example/matrices/b.rungs.json").write_text(json.dumps({
                "matrix_id": "MATRIX-B",
                "bucket_id": "BUCKET-B",
                "topic": "Example",
                "subtopic": "B",
                "rungs": [{
                    "rung": "R-B",
                    "ladder_position": 10,
                    "microtopic_ref": "MIC-B",
                }],
            }), encoding="utf-8")
            mapping = {
                "worksheet_id": "CROSS-MATRIX-ORDER",
                "subject": "Example",
                "questions": [{
                    "question_id": "Q1",
                    "primary_capability_ref": "CAP-B",
                    "secondary_capability_refs": [],
                    "mapping_basis": "MANUAL",
                }],
            }
            report = study_route.resolve(mapping, root)

        self.assertTrue(report["passed"], report["findings"])
        rows = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(rows["CAP-A"]["locations"][0]["ladder_position"], 90)
        self.assertEqual(rows["CAP-B"]["locations"][0]["ladder_position"], 10)
        self.assertLess(rows["CAP-A"]["order"], rows["CAP-B"]["order"])
        self.assertEqual(rows["CAP-B"]["depends_on"], ["CAP-A"])

    def test_question_secondary_is_demand_but_not_magic_prerequisite(self):
        report = study_route.resolve(self.mapping())
        rows = {row["capability_ref"]: row for row in report["route"]}
        distance = rows["CAP-KIN-DISTANCE-DISPLACEMENT"]
        self.assertIn("QUESTION_DEMAND", distance["reasons"])
        self.assertIn("PREREQUISITE", distance["reasons"])

    def test_syllabus_overlay_stays_distinct_from_question_demand(self):
        mapping = self.mapping()
        mapping["syllabus_capabilities"] = [{
            "capability_ref": "CAP-NLM-FRAME-CHOICE",
            "source_ref": "SRC-SYLLABUS-DEMO",
        }]
        report = study_route.resolve(mapping)
        self.assertTrue(report["passed"], report["findings"])
        row = next(r for r in report["route"]
                   if r["capability_ref"] == "CAP-NLM-FRAME-CHOICE")
        self.assertEqual(row["scope"], "SYLLABUS_ONLY")
        self.assertEqual(row["syllabus_source_refs"], ["SRC-SYLLABUS-DEMO"])
        self.assertNotIn("QUESTION_DEMAND", row["reasons"])
        self.assertIn("SYLLABUS_REQUIREMENT", row["reasons"])

    def test_declared_extension_stays_labelled_extension(self):
        mapping = self.mapping()
        mapping["declared_extension_capabilities"] = ["CAP-MEASURED-FROM"]
        report = study_route.resolve(mapping)
        self.assertTrue(report["passed"], report["findings"])
        row = next(r for r in report["route"]
                   if r["capability_ref"] == "CAP-MEASURED-FROM")
        self.assertEqual(row["scope"], "DECLARED_EXTENSION")
        self.assertEqual(row["reasons"], ["DECLARED_EXTENSION"])

    def test_diamond_prerequisite_appears_once(self):
        caps = {
            "A": {"id": "A", "prerequisite_refs": []},
            "B": {"id": "B", "prerequisite_refs": ["A"]},
            "C": {"id": "C", "prerequisite_refs": ["A"]},
            "D": {"id": "D", "prerequisite_refs": ["B", "C"]},
        }
        self.assertEqual(
            capability_graph.topological_subset(["D"], caps),
            ["A", "B", "C", "D"],
        )

    def test_unknown_prerequisite_is_explicit(self):
        caps = {
            "A": {"id": "A", "prerequisite_refs": ["MISSING"]},
        }
        self.assertEqual(
            capability_graph.unknown_prerequisites(["A"], caps),
            ["MISSING"],
        )

    def test_requested_slice_cycle_is_refused(self):
        caps = {
            "A": {"id": "A", "prerequisite_refs": ["B"]},
            "B": {"id": "B", "prerequisite_refs": ["A"]},
        }
        with self.assertRaises(ContractError) as caught:
            capability_graph.topological_subset(["A"], caps)
        self.assertEqual(caught.exception.code, "CAPABILITY_PREREQUISITE_CYCLE")


if __name__ == "__main__":
    unittest.main()
