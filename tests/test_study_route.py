"""Cross-matrix study routing follows capability prerequisites, never ladder positions."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
        positions = {
            row["capability_ref"]: row["order"]
            for row in report["route"]
        }
        demanded = {
            ref
            for question in self.mapping()["questions"]
            for ref in [
                question["primary_capability_ref"],
                *question["secondary_capability_refs"],
            ]
        }
        self.assertTrue(demanded.issubset(positions))
        for row in report["route"]:
            for prerequisite in row["depends_on"]:
                if prerequisite in positions:
                    self.assertLess(
                        positions[prerequisite],
                        positions[row["capability_ref"]],
                        (prerequisite, row["capability_ref"]),
                    )

    def test_cross_matrix_ladder_positions_do_not_order_the_route(self):
        mapping = {
            "worksheet_id": "ORDER-FALSIFIER",
            "subject": "Physics",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-DEPENDANT",
                "secondary_capability_refs": [],
                "mapping_basis": "MANUAL",
            }],
        }
        index = {
            "capabilities": {
                "CAP-PREREQUISITE": {
                    "id": "CAP-PREREQUISITE",
                    "prerequisite_refs": [],
                },
                "CAP-DEPENDANT": {
                    "id": "CAP-DEPENDANT",
                    "prerequisite_refs": ["CAP-PREREQUISITE"],
                },
            },
            "locations": {
                "CAP-PREREQUISITE": [{
                    "matrix_id": "MATRIX-A",
                    "bucket_id": "BUCKET-A",
                    "rung": "R9",
                    "ladder_position": 90,
                    "microtopic_ref": "MIC-A",
                }],
                "CAP-DEPENDANT": [{
                    "matrix_id": "MATRIX-B",
                    "bucket_id": "BUCKET-B",
                    "rung": "R1",
                    "ladder_position": 10,
                    "microtopic_ref": "MIC-B",
                }],
            },
        }
        with patch.object(
            study_route.study_map,
            "resolve",
            return_value={"findings": []},
        ), patch.object(
            study_route.study_map,
            "subject_index",
            return_value=index,
        ):
            report = study_route.resolve(mapping)

        self.assertTrue(report["passed"], report["findings"])
        rows = {row["capability_ref"]: row for row in report["route"]}
        prerequisite = rows["CAP-PREREQUISITE"]
        dependant = rows["CAP-DEPENDANT"]
        self.assertGreater(
            prerequisite["locations"][0]["ladder_position"],
            dependant["locations"][0]["ladder_position"],
        )
        self.assertLess(prerequisite["order"], dependant["order"])
        self.assertEqual(dependant["depends_on"], ["CAP-PREREQUISITE"])

    def test_external_provider_is_a_valid_but_not_ready_bridge(self):
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
                        "id": "CAP-BRIDGE",
                        "action": "Use provider-owned prior knowledge",
                        "success_criterion": "Provider-owned prior knowledge is used correctly",
                        "prerequisite_refs": [],
                        "external_provider": "ProviderSubject",
                        "acceptance_status": "PROVIDER_REVIEW_REQUIRED",
                    },
                    {
                        "id": "CAP-TARGET",
                        "action": "Use the local target skill",
                        "success_criterion": "The local target skill is demonstrated",
                        "prerequisite_refs": ["CAP-BRIDGE"],
                        "external_provider": None,
                        "acceptance_status": "CANDIDATE",
                    },
                ],
                "microtopics": [{
                    "id": "MIC-TARGET",
                    "primary_capability_ref": "CAP-TARGET",
                }],
                "questions": [],
            }), encoding="utf-8")
            (root / "Example/matrices/example.rungs.json").write_text(json.dumps({
                "matrix_id": "MATRIX-EXAMPLE",
                "bucket_id": "BUCKET-EXAMPLE",
                "topic": "Synthetic",
                "subtopic": "Bridge routing",
                "rungs": [{
                    "rung": "R1",
                    "ladder_position": 20,
                    "microtopic_ref": "MIC-TARGET",
                }],
            }), encoding="utf-8")
            mapping = {
                "worksheet_id": "EXAMPLE-BRIDGE",
                "subject": "Example",
                "questions": [{
                    "question_id": "Q1",
                    "primary_capability_ref": "CAP-TARGET",
                    "secondary_capability_refs": [],
                    "mapping_basis": "MANUAL",
                }],
            }
            report = study_route.resolve(mapping, root)

        self.assertTrue(report["passed"], report["findings"])
        self.assertTrue(report["valid"])
        self.assertFalse(report["ready"])
        self.assertEqual(
            [row["point"] for row in report["blockers"]],
            [study_route.EXTERNAL_BRIDGE_REQUIRED],
        )
        rows = {row["capability_ref"]: row for row in report["route"]}
        self.assertEqual(rows["CAP-BRIDGE"]["delivery_state"], "EXTERNAL_BRIDGE")
        self.assertEqual(rows["CAP-BRIDGE"]["provider"], "ProviderSubject")
        self.assertLess(rows["CAP-BRIDGE"]["order"], rows["CAP-TARGET"]["order"])

    def test_same_missing_location_without_provider_is_invalid(self):
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
                        "id": "CAP-MISSING",
                        "action": "Use unavailable prior knowledge",
                        "success_criterion": "Unavailable prior knowledge is used correctly",
                        "prerequisite_refs": [],
                        "external_provider": None,
                        "acceptance_status": "CANDIDATE",
                    },
                    {
                        "id": "CAP-TARGET",
                        "action": "Use the local target skill",
                        "success_criterion": "The local target skill is demonstrated",
                        "prerequisite_refs": ["CAP-MISSING"],
                        "external_provider": None,
                        "acceptance_status": "CANDIDATE",
                    },
                ],
                "microtopics": [{
                    "id": "MIC-TARGET",
                    "primary_capability_ref": "CAP-TARGET",
                }],
                "questions": [],
            }), encoding="utf-8")
            (root / "Example/matrices/example.rungs.json").write_text(json.dumps({
                "matrix_id": "MATRIX-EXAMPLE",
                "bucket_id": "BUCKET-EXAMPLE",
                "topic": "Synthetic",
                "subtopic": "Missing routing",
                "rungs": [{
                    "rung": "R1",
                    "ladder_position": 20,
                    "microtopic_ref": "MIC-TARGET",
                }],
            }), encoding="utf-8")
            mapping = {
                "worksheet_id": "EXAMPLE-MISSING",
                "subject": "Example",
                "questions": [{
                    "question_id": "Q1",
                    "primary_capability_ref": "CAP-TARGET",
                    "secondary_capability_refs": [],
                    "mapping_basis": "MANUAL",
                }],
            }
            report = study_route.resolve(mapping, root)

        self.assertFalse(report["passed"])
        self.assertFalse(report["valid"])
        self.assertFalse(report["ready"])
        self.assertIn(
            study_route.NO_TEACHING_LOCATION,
            [row["point"] for row in report["findings"]],
        )

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
