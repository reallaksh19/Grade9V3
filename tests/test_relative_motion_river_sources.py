"""Relative Motion river/boat sources keep explanation, authority and demand distinct."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "Physics/library/relative-motion.v1.json"


class RelativeMotionRiverBoatSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads(PACKAGE.read_text(encoding="utf-8"))
        cls.resources = {
            row["id"]: row
            for row in cls.package["resources"]
        }

    def test_owner_supplied_scribd_bank_is_question_demand_only(self):
        row = self.resources["SRC-SCRIBD-DPP8-RIVER-BOAT"]
        self.assertEqual(row["role"], ["QUESTION_BANK"])
        self.assertEqual(row["supports_claims"], [])
        self.assertIn("do not copy", row["rights_status"].lower())
        self.assertIn("not scientific authority", row["selection_reason"])

    def test_owner_supplied_anand_page_is_explanation_not_curriculum_authority(self):
        row = self.resources["SRC-ANAND-RIVER-BOAT"]
        self.assertEqual(row["role"], ["EXPLANATION"])
        self.assertNotIn("CURRICULUM", row["role"])
        self.assertNotIn("SCIENTIFIC_CHECK", row["role"])
        self.assertIn("not used as curriculum authority", row["selection_reason"])

    def test_stronger_sources_back_the_river_application(self):
        ncert = self.resources["SRC-NCERT-EXEMPLAR-RIVER"]
        openstax = self.resources["SRC-OPENSTAX-RELATIVE-RIVER"]
        self.assertIn("SCIENTIFIC_CHECK", ncert["role"])
        self.assertIn("QUESTION_BANK", ncert["role"])
        self.assertIn("SCIENTIFIC_CHECK", openstax["role"])
        self.assertIn("EXPLANATION", openstax["role"])
        self.assertIn("CAP-RELATIVE-V", ncert["entry_capabilities"])
        self.assertIn("CAP-VECTOR-CHECK", openstax["entry_capabilities"])

    def test_existing_geometric_check_is_cross_checked_without_new_capability(self):
        microtopic = next(
            row for row in self.package["microtopics"]
            if row["id"] == "MIC-GEOMETRIC-CHECK"
        )
        self.assertIn("SRC-NCERT-EXEMPLAR-RIVER", microtopic["source_refs"])
        self.assertIn("SRC-OPENSTAX-RELATIVE-RIVER", microtopic["source_refs"])

        capability_ids = {
            row["id"]
            for row in self.package["capabilities"]
        }
        self.assertNotIn("CAP-RIVER-BOAT", capability_ids)
        self.assertNotIn("CAP-MOVING-MEDIUM-CROSSING", capability_ids)


if __name__ == "__main__":
    unittest.main()
