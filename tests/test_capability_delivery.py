"""Capability delivery is independent from prerequisite topology and learner state."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import capability_delivery  # noqa: E402


class CapabilityDelivery(unittest.TestCase):
    def test_one_local_location_is_local(self):
        report = capability_delivery.resolve(
            {"id": "CAP-A", "external_provider": None, "acceptance_status": "CANDIDATE"},
            [{"matrix_id": "MATRIX-A", "rung": "R1"}],
        )
        self.assertEqual(report["state"], capability_delivery.LOCAL)
        self.assertEqual(capability_delivery.legacy_state(report), "RESOLVED")

    def test_no_local_location_with_provider_is_an_external_bridge(self):
        report = capability_delivery.resolve(
            {
                "id": "CAP-A",
                "external_provider": "Subject-B",
                "acceptance_status": "PROVIDER_REVIEW_REQUIRED",
            },
            [],
        )
        self.assertEqual(report["state"], capability_delivery.EXTERNAL_BRIDGE)
        self.assertEqual(report["provider"], "Subject-B")
        self.assertEqual(
            report["acceptance_status"],
            "PROVIDER_REVIEW_REQUIRED",
        )
        self.assertEqual(capability_delivery.legacy_state(report), "EXTERNAL_BRIDGE")

    def test_no_location_and_no_provider_is_unresolved(self):
        report = capability_delivery.resolve(
            {"id": "CAP-A", "external_provider": None, "acceptance_status": "CANDIDATE"},
            [],
        )
        self.assertEqual(report["state"], capability_delivery.UNRESOLVED)
        self.assertEqual(
            capability_delivery.legacy_state(report),
            "NO_TEACHING_LOCATION",
        )

    def test_multiple_locations_are_ambiguous_even_if_a_provider_is_declared(self):
        report = capability_delivery.resolve(
            {
                "id": "CAP-A",
                "external_provider": "Subject-B",
                "acceptance_status": "REVIEWED",
            },
            [
                {"matrix_id": "MATRIX-A", "rung": "R1"},
                {"matrix_id": "MATRIX-A", "rung": "R2"},
            ],
        )
        self.assertEqual(report["state"], capability_delivery.AMBIGUOUS)
        self.assertEqual(
            capability_delivery.legacy_state(report),
            "AMBIGUOUS_LOCATION",
        )


if __name__ == "__main__":
    unittest.main()
