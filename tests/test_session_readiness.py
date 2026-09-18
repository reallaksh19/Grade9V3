"""Session readiness distinguishes usable self-study matrices from structural closure alone."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import session_readiness  # noqa: E402


class SessionReadiness(unittest.TestCase):
    def test_relative_motion_is_session_ready_with_explicit_math_bridge(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-RELATIVE-MOTION",
        )
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertEqual(len(report["rungs"]), 4)
        self.assertTrue(all(row["state"] == "READY" for row in report["rungs"]))
        self.assertEqual(
            [row["capability_ref"] for row in report["external_bridges"]],
            ["CAP-SIGNED-PAIR"],
        )
        self.assertEqual(
            report["external_bridges"][0]["external_provider"],
            "Mathematics",
        )
        self.assertEqual(
            report["external_bridges"][0]["acceptance_status"],
            "PROVIDER_REVIEW_REQUIRED",
        )
        self.assertIn(
            "READINESS_ACADEMIC_REVIEW_PENDING",
            [row["point"] for row in report["academic_warnings"]],
        )
        self.assertIn(
            "READINESS_SOURCE_QUESTION_COVERAGE_ABSENT",
            [row["point"] for row in report["academic_warnings"]],
        )

    def fixture(self, *, diagnostic=True, teaching=True, verification=True,
                core1b=True, external=False):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "Example/library").mkdir(parents=True)
        (root / "Example/matrices").mkdir(parents=True)

        capabilities = [{
            "id": "CAP-MAIN",
            "status": "REVIEWED",
            "action": "Do the main thing.",
            "success_criterion": "The main thing is done.",
            "prerequisite_refs": ["CAP-EXT"] if external else [],
        }]
        if external:
            capabilities.append({
                "id": "CAP-EXT",
                "status": "REVIEWED",
                "action": "Use the bridge.",
                "success_criterion": "Bridge is usable.",
                "prerequisite_refs": [],
                "external_provider": "Mathematics",
                "acceptance_status": "PROVIDER_REVIEW_REQUIRED",
            })

        microtopic = {
            "id": "MIC-MAIN",
            "status": "REVIEWED",
            "title": "Main lesson",
            "primary_capability_ref": "CAP-MAIN",
            "teaching_path": ([{
                "id": "STEP-1",
                "action": "Do it.",
                "why_valid": "Because the relation holds.",
            }] if teaching else []),
            "misconceptions": ([{
                "wrong_idea": "Wrong idea.",
                "diagnostic_prompt": "What did you assume?",
                "repair": "Rebuild the relation.",
            }] if diagnostic else []),
            "elicitation": ({
                "predict": {"prompt": "Predict."},
                "attempt": {"produces": "Attempt."},
                "reconstruct": {"route": [{"ask": "Why?"}]},
                "boundary_test": {"prompt": "Boundary."},
            } if core1b else {}),
        }
        if verification:
            microtopic["exit_task"] = {
                "prompt": "Fresh check.",
                "answer": {"kind": "MODEL_RESPONSE"},
            }

        routes = [{
            "id": "ROUTE-A",
            "status": "REVIEWED",
            "cores": ["CORE1A"],
            "microtopic_refs": ["MIC-MAIN"],
        }]
        if core1b:
            routes.append({
                "id": "ROUTE-B",
                "status": "REVIEWED",
                "cores": ["CORE1B"],
                "microtopic_refs": ["MIC-MAIN"],
            })

        (root / "Example/library/example.json").write_text(json.dumps({
            "capabilities": capabilities,
            "microtopics": [microtopic],
            "questions": [],
            "teaching_routes": routes,
        }), encoding="utf-8")
        (root / "Example/matrices/example.rungs.json").write_text(json.dumps({
            "matrix_id": "MATRIX-EXAMPLE",
            "bucket_id": "BUCKET-EXAMPLE",
            "topic": "Example",
            "subtopic": "Example",
            "rungs": [{
                "rung": "R1",
                "ladder_position": 20,
                "microtopic_ref": "MIC-MAIN",
            }],
        }), encoding="utf-8")
        return tmp, root

    def test_complete_matrix_without_bridge_is_session_ready(self):
        tmp, root = self.fixture()
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.READY)
        self.assertTrue(report["passed"])

    def test_external_prerequisite_yields_ready_with_bridge(self):
        tmp, root = self.fixture(external=True)
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertEqual(
            report["external_bridges"][0]["capability_ref"],
            "CAP-EXT",
        )

    def test_readiness_uses_shared_delivery_resolver_for_prerequisites(self):
        tmp, root = self.fixture(external=True)
        calls = []
        real_resolve = session_readiness.capability_delivery.resolve

        def recording_resolve(capability, locations):
            calls.append((capability["id"], list(locations)))
            return real_resolve(capability, locations)

        try:
            with patch.object(
                session_readiness.capability_delivery,
                "resolve",
                side_effect=recording_resolve,
            ):
                report = session_readiness.audit(
                    "Example", matrix_id="MATRIX-EXAMPLE", repo=root
                )
        finally:
            tmp.cleanup()

        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertEqual(calls, [("CAP-EXT", [])])

    def test_shared_unresolved_delivery_remains_a_readiness_blocker(self):
        tmp, root = self.fixture(external=True)
        try:
            package = json.loads(
                (root / "Example/library/example.json").read_text(encoding="utf-8")
            )
            external = next(
                row for row in package["capabilities"]
                if row["id"] == "CAP-EXT"
            )
            external["external_provider"] = None
            (root / "Example/library/example.json").write_text(
                json.dumps(package),
                encoding="utf-8",
            )
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()

        self.assertEqual(report["status"], session_readiness.NOT_READY)
        self.assertFalse(report["passed"])
        self.assertIn(
            "READINESS_PREREQUISITE_UNTAUGHT",
            [row["point"] for row in report["blocking_findings"]],
        )

    def test_missing_diagnostic_is_pilot_ready_not_falsely_session_ready(self):
        tmp, root = self.fixture(diagnostic=False)
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.PILOT_READY)
        self.assertTrue(report["passed"])
        self.assertIn(
            "READINESS_DIAGNOSTIC_REPAIR_INCOMPLETE",
            [row["point"] for row in report["support_findings"]],
        )

    def test_missing_teaching_path_is_not_ready(self):
        tmp, root = self.fixture(teaching=False)
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.NOT_READY)
        self.assertFalse(report["passed"])
        self.assertIn(
            "READINESS_TEACHING_PATH_MISSING",
            [row["point"] for row in report["blocking_findings"]],
        )

    def test_missing_verification_is_not_ready(self):
        tmp, root = self.fixture(verification=False)
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.NOT_READY)
        self.assertIn(
            "READINESS_VERIFICATION_MISSING",
            [row["point"] for row in report["blocking_findings"]],
        )

    def test_missing_core1b_route_is_only_pilot_ready(self):
        tmp, root = self.fixture(core1b=False)
        try:
            report = session_readiness.audit(
                "Example", matrix_id="MATRIX-EXAMPLE", repo=root
            )
        finally:
            tmp.cleanup()
        self.assertEqual(report["status"], session_readiness.PILOT_READY)
        self.assertIn(
            "READINESS_CORE1B_ROUTE_MISSING",
            [row["point"] for row in report["support_findings"]],
        )


    def test_vector_representation_modernization_has_distinct_capabilities(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VECTOR-REPRESENTATION",
        )
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertTrue(report["passed"])
        self.assertEqual(
            [row["capability_ref"] for row in report["rungs"]],
            [
                "CAP-VECTOR-VS-SCALAR",
                "CAP-VECTOR-SIGNED-COMPONENT",
                "CAP-GRAPHICAL-SUBTRACT",
            ],
        )
        self.assertNotIn(
            "READINESS_PREREQUISITE_AMBIGUOUS",
            [row["point"] for row in report["findings"]],
        )
        self.assertTrue(all(row["core1a"] and row["core1b"] for row in report["rungs"]))
        self.assertEqual(
            {row["capability_ref"] for row in report["external_bridges"]},
            {"CAP-SIGNED-PAIR-BRIDGE", "CAP-RIGHT-TRIANGLE-BRIDGE"},
        )

    def test_vector_add_sub_completion_is_session_ready_with_math_bridge(self):
        report = session_readiness.audit(
            "Physics",
            matrix_id="MATRIX-PHY-VEC-ADD-SUB",
        )
        self.assertEqual(report["status"], session_readiness.READY_WITH_BRIDGE)
        self.assertTrue(report["passed"], report["findings"])
        points = [row["point"] for row in report["findings"]]
        self.assertNotIn("READINESS_MICROTOPIC_MISSING", points)
        self.assertNotIn("READINESS_PREREQUISITE_AMBIGUOUS", points)
        self.assertTrue(all(row["core1a"] and row["core1b"] for row in report["rungs"]))
        self.assertIn(
            "CAP-RIGHT-TRIANGLE-BRIDGE",
            {row["capability_ref"] for row in report["external_bridges"]},
        )


if __name__ == "__main__":
    unittest.main()
