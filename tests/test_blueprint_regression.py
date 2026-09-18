"""Regression contract derived from the committed Physics blueprint.

This suite does not simulate learner evidence. It protects architectural invariants that the
blueprint says must hold before/after every change and prevents the first Relative Motion
pilot from leaking case-specific logic into Shared/core.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BLUEPRINT = REPO / "docs/OFFLOAD-PHYSICS-BLUEPRINT.md"
GUARDRAILS = REPO / ".github/workflows/guardrails.yml"

SHARED_SESSION_SURFACE = [
    REPO / "Shared/tools/capability_delivery.py",
    REPO / "Shared/tools/session_readiness.py",
    REPO / "Shared/tools/study_session.py",
    REPO / "Shared/tools/study_map.py",
    REPO / "Shared/tools/study_route.py",
    REPO / "Shared/tools/study_start.py",
    REPO / "Shared/tools/worksheet_study_plan.py",
]


class BlueprintRegression(unittest.TestCase):
    def blueprint_text(self) -> str:
        return BLUEPRINT.read_text(encoding="utf-8")

    def test_blueprint_prescribed_regression_commands_are_ci_enforced(self):
        blueprint = self.blueprint_text()
        marker = "Run before and after every change:"
        self.assertIn(marker, blueprint)

        tail = blueprint.split(marker, 1)[1]
        match = re.search(r"```\s*\n(?P<body>.*?)\n```", tail, re.S)
        self.assertIsNotNone(match, "blueprint command block is missing")

        commands = [
            line.strip()
            for line in match.group("body").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertGreater(len(commands), 0)

        workflow = GUARDRAILS.read_text(encoding="utf-8")
        for command in commands:
            self.assertIn(
                command,
                workflow,
                f"blueprint-prescribed regression command is not enforced by CI: {command}",
            )

    def test_blueprint_keeps_engineering_gate_above_case_specific_blueprint_edits(self):
        blueprint = self.blueprint_text()
        self.assertIn(
            "A blueprint is never adjusted for a specific case.",
            blueprint,
        )
        self.assertIn(
            "engineering gate outranks the blueprint",
            blueprint,
        )

    def test_first_pilot_has_not_leaked_case_specific_logic_into_shared_runtime(self):
        forbidden = {
            "CAP-RELATIVE-V",
            "CAP-SIGNED-PAIR",
            "MATRIX-PHY-RELATIVE-MOTION",
            "EXAMSIDE-MIP",
            "river/boat",
            "river boat",
        }
        findings = []
        for path in SHARED_SESSION_SURFACE:
            text = path.read_text(encoding="utf-8")
            for token in sorted(forbidden):
                if token.casefold() in text.casefold():
                    findings.append(f"{path.relative_to(REPO)} contains {token!r}")
        self.assertEqual(
            findings,
            [],
            "Shared/core must stay generic; first-pilot identifiers belong only in content/tests",
        )

    def test_regression_and_empirical_acceptance_are_visible_as_separate_ci_steps(self):
        workflow = GUARDRAILS.read_text(encoding="utf-8")
        self.assertIn("Blueprint architecture regression", workflow)
        self.assertIn(
            "python3 -m unittest tests.test_blueprint_regression -v",
            workflow,
        )
        self.assertIn("Empirical learner acceptance status", workflow)
        self.assertIn(
            "python3 Shared/tools/empirical_acceptance.py --enforce",
            workflow,
        )

    def test_blueprint_regression_does_not_claim_to_replace_live_learner_evidence(self):
        runbook = (
            REPO / "docs/RELATIVE-MOTION-LIVE-PILOT-01.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "The next missing datum is a real learner response",
            runbook,
        )
        self.assertIn(
            "do not fabricate a successful or failed study episode",
            runbook,
        )


if __name__ == "__main__":
    unittest.main()
