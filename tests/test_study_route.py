"""Cross-matrix study routing follows capability prerequisites, never ladder positions."""
from __future__ import annotations

import json
import sys
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
        report = study_route.resolve(self.mapping())
        self.assertTrue(report["passed"], report["findings"])
        order = [row["capability_ref"] for row in report["route"]]
        self.assertEqual(order, [
            "CAP-KIN-DISTANCE-DISPLACEMENT",
            "CAP-KIN-ZERO-V-NONZERO-A",
            "CAP-NLM-NET-ZERO-MOTION",
            "CAP-NLM-FORCES-SUM-ZERO",
            "CAP-NLM-FBD-BODY-OWNERSHIP",
            "CAP-WEP-WORK-DIRECTION",
            "CAP-WEP-NET-WORK-SIGN",
            "CAP-WEP-POTENTIAL-ELIGIBILITY",
            "CAP-WEP-MECH-ENERGY-CONDITION",
        ])

    def test_cross_matrix_ladder_positions_do_not_order_the_route(self):
        report = study_route.resolve(self.mapping())
        rows = {row["capability_ref"]: row for row in report["route"]}
        fbd = rows["CAP-NLM-FBD-BODY-OWNERSHIP"]
        work = rows["CAP-WEP-WORK-DIRECTION"]

        self.assertEqual(fbd["locations"][0]["ladder_position"], 70)
        self.assertEqual(work["locations"][0]["ladder_position"], 20)
        self.assertLess(fbd["order"], work["order"])
        self.assertIn("CAP-NLM-FBD-BODY-OWNERSHIP", work["depends_on"])

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
