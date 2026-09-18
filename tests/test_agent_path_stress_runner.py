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
