"""Source inspection receipt custody and sufficiency falsifiers."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import source_receipts  # noqa: E402


class SourceReceipts(unittest.TestCase):
    RECEIPT_ID = "SRCREC-NCERT-KEPH103-RELATIVE-MOTION-LEGACY"

    def legacy(self):
        return copy.deepcopy(source_receipts.store()[self.RECEIPT_ID])

    def test_migrated_ncert_receipt_is_valid_but_insufficient(self):
        report = source_receipts.verify(self.legacy())
        self.assertTrue(report["verified"])
        self.assertEqual(report["findings"], [])
        self.assertIsNone(report["inspection"]["content_sha256"])
        for core in ("CORE2", "CORE2A", "CORE2B"):
            self.assertEqual(report["coverage"][core]["status"], "INSUFFICIENT")

    def test_legacy_metadata_cannot_promote_itself_to_sufficient(self):
        receipt = self.legacy()
        receipt["coverage"]["CORE2"]["status"] = "SUFFICIENT"
        report = source_receipts.verify(receipt)
        points = [row["point"] for row in report["findings"]]
        self.assertIn("LEGACY_RECEIPT_CANNOT_ASSERT_SUFFICIENCY", points)
        self.assertIn("SOURCE_RECEIPT_SUFFICIENT_WITHOUT_CONTENT_DIGEST", points)
        self.assertIn("SOURCE_RECEIPT_SUFFICIENT_WITHOUT_QUESTIONS", points)

    def test_authored_question_cannot_establish_core2_source_custody(self):
        receipt = self.legacy()
        receipt["receipt_id"] = "TEST-AUTHORED-AS-CUSTODY"
        receipt["source_basis"] = ["V3B-Relative-Motion-Library-Seed.json"]
        receipt["resource_refs"] = ["SRC-AUTHOR"]
        receipt["inspection"] = {
            "inspector_kind": "AGENT",
            "inspector_id": "test",
            "inspected_at": "2026-09-18",
            "access_status": "FULL_ITEM_INSPECTED",
            "sections": ["Author-created derivation and micro-checks"],
            "content_sha256": "a" * 64,
            "snapshot_ref": "test-fixture",
        }
        receipt["coverage"]["CORE2"] = {
            "status": "SUFFICIENT",
            "question_refs": ["Q-AUTHOR-REL-01"],
            "basis": "Planted falsifier: an authored question is presented as custody.",
        }
        report = source_receipts.verify(receipt)
        self.assertIn("SOURCE_RECEIPT_CORE2_AUTHORED_QUESTION",
                      [row["point"] for row in report["findings"]])

    def test_sufficiency_requires_an_immutable_content_digest(self):
        receipt = self.legacy()
        receipt["receipt_id"] = "TEST-NO-DIGEST"
        receipt["source_basis"] = ["V3B-Relative-Motion-Library-Seed.json"]
        receipt["resource_refs"] = ["SRC-AUTHOR"]
        receipt["inspection"]["inspector_kind"] = "AGENT"
        receipt["inspection"]["inspector_id"] = "test"
        receipt["inspection"]["access_status"] = "FULL_ITEM_INSPECTED"
        receipt["coverage"]["CORE2A"] = {
            "status": "SUFFICIENT",
            "question_refs": ["Q-AUTHOR-REL-01"],
            "basis": "Planted falsifier: source coverage claims sufficiency without a content digest.",
        }
        report = source_receipts.verify(receipt)
        self.assertIn("SOURCE_RECEIPT_SUFFICIENT_WITHOUT_CONTENT_DIGEST",
                      [row["point"] for row in report["findings"]])

    def test_receipt_must_match_the_request_source_basis_exactly(self):
        receipt = self.legacy()
        request = {
            "subject": "Physics",
            "source_basis": ["https://example.invalid/not-the-inspected-source.pdf"],
        }
        report = source_receipts.verify(
            receipt, request=request, expected_bucket="BUCKET-RELATIVE-MOTION")
        self.assertIn("SOURCE_RECEIPT_BASIS_MISMATCH",
                      [row["point"] for row in report["findings"]])

    def test_request_cannot_self_assert_source_inspection_status(self):
        schema = json.loads(
            (REPO / "Shared/library/authoring-request.schema.json").read_text(encoding="utf-8")
        )
        try:
            import jsonschema
        except ModuleNotFoundError:
            self.skipTest("jsonschema not installed")
        request = {
            "request_id": "PLANTED-SELF-ASSERTION",
            "subject": "Physics",
            "subtopic": "Relative motion",
            "requested_cores": ["CORE2"],
            "source_basis": ["https://ncert.nic.in/textbook/pdf/keph103.pdf"],
            "source_inspection": {"status": "INGESTED_SUFFICIENT"},
        }
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(request))
        self.assertTrue(errors)
        self.assertTrue(any("source_inspection" in error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
