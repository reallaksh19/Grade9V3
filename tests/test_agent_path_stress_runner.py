"""The saved stress runner must replay every frozen case without routing drift."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools/run_agent_path_stress.py"

spec = importlib.util.spec_from_file_location("run_agent_path_stress", TOOL)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)


class AgentPathStressRunner(unittest.TestCase):
    def test_every_frozen_case_matches_current_expected_path(self):
        suite = runner.load_suite()
        reports = [runner.run_case(case) for case in suite["cases"]]
        self.assertTrue(reports)
        self.assertEqual(
            [row["case_id"] for row in reports],
            [row["case_id"] for row in suite["cases"]],
        )
        self.assertEqual(
            [row for row in reports if row["status"] != "PASS"],
            [],
        )

    def test_runner_never_claims_learner_evidence(self):
        suite = runner.load_suite()
        for case in suite["cases"]:
            with self.subTest(case=case["case_id"]):
                report = runner.run_case(case)
                self.assertEqual(report["evidence_class"], "SYSTEM_STRESS_ONLY")
                self.assertTrue(report["actual"]["no_content_authored"])

    def test_grade9_completion_has_one_frozen_checkpoint_per_slice(self):
        cases = runner.by_id(runner.load_suite())
        expected = {
            "APSTRESS-G9-MOTION-70-DEFAULT",
            "APSTRESS-G9-MOTION2D-70-DEFAULT",
            "APSTRESS-G9-NLM-70-PRACTICE",
            "APSTRESS-G9-GRAV-60-TEACH",
            "APSTRESS-G9-WEP-95-DERIVATION",
            "APSTRESS-G9-SOUND-95-REFLECTION",
            "APSTRESS-G9-SIMPLE-MACHINES-90",
        }
        self.assertTrue(expected.issubset(cases))

    def test_grade9_motion2d_question_demand_segment_is_frozen(self):
        cases = runner.by_id(runner.load_suite())
        report = runner.run_case(cases["APSTRESS-G9-MOTION2D-70-DEFAULT"])
        self.assertEqual(report["status"], "PASS", report["differences"])
        self.assertEqual(report["actual"]["entry"], "R2")
        self.assertEqual(report["actual"]["selected_segment"], ["R2", "R3"])
        self.assertEqual(
            report["actual"]["prerequisite_checks"],
            [
                "CAP-VECTOR-VS-SCALAR",
                "CAP-SIGNED-PAIR-BRIDGE",
                "CAP-VECTOR-SIGNED-COMPONENT",
                "CAP-KIN-2D-INDEPENDENT-COMPONENTS",
                "CAP-KIN-DISTANCE-DISPLACEMENT",
                "CAP-KIN-AVERAGE-RATES",
                "CAP-KIN-MOTION-GRAPHS",
                "CAP-KIN-CONSTANT-ACCELERATION",
            ],
        )

    def test_grade9_default_segments_exclude_retained_extensions(self):
        cases = runner.by_id(runner.load_suite())
        expectations = {
            "APSTRESS-G9-MOTION-70-DEFAULT": ["R2", "R4G", "R4", "R5"],
            "APSTRESS-G9-NLM-70-PRACTICE": ["R3", "R5", "R6", "R8", "R9", "R10", "R11", "R7"],
            "APSTRESS-G9-GRAV-60-TEACH": ["R3W"],
        }
        for case_id, expected_segment in expectations.items():
            with self.subTest(case=case_id):
                report = runner.run_case(cases[case_id])
                self.assertEqual(report["status"], "PASS", report["differences"])
                self.assertEqual(report["actual"]["selected_segment"], expected_segment)

    def test_prompt_only_source_is_the_frozen_fixture(self):
        suite = runner.load_suite()
        cases = runner.by_id(suite)
        case = cases["APSTRESS-REL-60-TEACH"]
        self.assertIn(
            "Student knowledge estimate: 60%",
            case["prompt"],
        )
        self.assertEqual(
            case["request"]["learner"]["owner_estimate"]["knowledge_percentage"],
            60,
        )


if __name__ == "__main__":
    unittest.main()
