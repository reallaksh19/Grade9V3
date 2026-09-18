"""Study-scope audit catches both missing teaching and unjustified expansion."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import study_scope_audit  # noqa: E402


class StudyScopeAudit(unittest.TestCase):
    PHYSICS = REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json"
    MATH = REPO / "tests/fixtures/study_route/mathematics-cross-matrix.worksheet.json"

    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_real_physics_slice_is_taught_and_scope_justified(self):
        report = study_scope_audit.audit(self.load(self.PHYSICS))
        self.assertTrue(report["passed"], report["findings"])

    def test_extra_teaching_without_reason_is_rejected(self):
        mapping = self.load(self.PHYSICS)
        route = study_scope_audit.audit(mapping)
        proposed = [
            *(row["capability_ref"] for row in route["route"]),
            "CAP-MEASURED-FROM",
        ]
        report = study_scope_audit.audit(mapping, proposed)
        self.assertFalse(report["passed"])
        self.assertIn(
            study_scope_audit.UNJUSTIFIED,
            [row["point"] for row in report["findings"]],
        )

    def test_question_demand_without_a_matrix_is_named_as_not_taught(self):
        report = study_scope_audit.audit(self.load(self.MATH))
        self.assertFalse(report["passed"])
        self.assertIn(
            study_scope_audit.ASSESSMENT_NOT_TAUGHT,
            [row["point"] for row in report["findings"]],
        )

    def test_prerequisites_are_valid_scope_reasons(self):
        report = study_scope_audit.audit(self.load(self.PHYSICS))
        row = next(r for r in report["route"]
                   if r["capability_ref"] == "CAP-NLM-NET-ZERO-MOTION")
        self.assertEqual(row["scope"], "PREREQUISITE")
        self.assertEqual(row["reasons"], ["PREREQUISITE"])


if __name__ == "__main__":
    unittest.main()
