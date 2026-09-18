"""Source acquisition and custody-ingestion pipeline falsifiers."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.contracts import digest  # noqa: E402
from Shared.tools import source_pipeline, source_receipts  # noqa: E402


class SourcePipeline(unittest.TestCase):
    ROOT = REPO / "tests/fixtures/source_ingest"
    ACQ = ROOT / "acquisition.json"
    MANIFEST = ROOT / "custody-manifest.json"
    PACKAGE = REPO / "Physics/library/relative-motion.v1.json"

    def acquisition(self):
        return json.loads(self.ACQ.read_text(encoding="utf-8"))

    def manifest(self):
        return json.loads(self.MANIFEST.read_text(encoding="utf-8"))

    def package(self):
        return json.loads(self.PACKAGE.read_text(encoding="utf-8"))

    def test_acquisition_snapshot_digest_and_length_are_verified(self):
        report = source_pipeline.verify_acquisition(self.acquisition())
        self.assertTrue(report["passed"], report["findings"])

    def test_acquisition_tamper_is_detected(self):
        acquisition = self.acquisition()
        acquisition["sha256"] = "0" * 64
        report = source_pipeline.verify_acquisition(acquisition)
        self.assertIn("SOURCE_ACQUISITION_DIGEST_MISMATCH",
                      [row["point"] for row in report["findings"]])

    def test_candidate_ingestion_is_valid_but_cannot_self_promote_custody(self):
        package = self.package()
        before = digest(package)
        report = source_pipeline.plan_ingestion(
            self.acquisition(), self.manifest(), package)
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(digest(package), before, "dry-run must not mutate the input package")

        merged = report["merged_package"]
        resource = next(r for r in merged["resources"]
                        if r["id"] == "SRC-TEST-FIXTURE-REL")
        question = next(q for q in merged["questions"]
                        if q["id"] == "Q-TEST-FIXTURE-REL-01")
        self.assertEqual(resource["status"], "CANDIDATE")
        self.assertEqual(question["status"], "CANDIDATE")
        self.assertEqual(question["origin"], "ORIGINAL")
        self.assertEqual(resource["snapshot_digest"], self.acquisition()["sha256"])

        receipt = report["receipt"]
        for core in ("CORE2", "CORE2A", "CORE2B"):
            self.assertEqual(receipt["coverage"][core]["status"], "INSUFFICIENT")
        self.assertRegex(receipt["inspection"]["content_sha256"], r"^[0-9a-f]{64}$")

    def test_newly_transcribed_question_is_not_structural_sufficiency(self):
        report = source_pipeline.plan_ingestion(
            self.acquisition(), self.manifest(), self.package())
        merged = report["merged_package"]
        records = {}
        for collection, rows in merged.items():
            if isinstance(rows, list):
                for row in rows:
                    if isinstance(row, dict) and row.get("id"):
                        records[row["id"]] = {**row, "_collection": collection}
        coverage = source_receipts.derive_coverage(
            records, "BUCKET-RELATIVE-MOTION", ["SRC-TEST-FIXTURE-REL"])
        self.assertEqual(coverage["CORE2"]["status"], "INSUFFICIENT")
        self.assertIn("CAP-RELATIVE-V", coverage["CORE2"]["basis"])

    def test_question_custody_requires_retained_source_bytes(self):
        acquisition = self.acquisition()
        acquisition["snapshot_ref"] = None
        manifest = self.manifest()
        manifest["resource"]["snapshot_ref"] = None
        report = source_pipeline.plan_ingestion(
            acquisition, manifest, self.package())
        self.assertIn("SOURCE_INGEST_SNAPSHOT_REQUIRED",
                      [row["point"] for row in report["findings"]])

    def test_ingestion_refuses_a_reviewed_question_from_the_same_operation(self):
        manifest = self.manifest()
        manifest["questions"][0]["status"] = "REVIEWED"
        report = source_pipeline.plan_ingestion(
            self.acquisition(), manifest, self.package())
        self.assertIn("SOURCE_INGEST_QUESTION_NOT_CANDIDATE",
                      [row["point"] for row in report["findings"]])

    def test_ingestion_refuses_authored_question_as_source_custody(self):
        manifest = self.manifest()
        manifest["questions"][0]["origin"] = "AUTHORED"
        report = source_pipeline.plan_ingestion(
            self.acquisition(), manifest, self.package())
        self.assertIn("SOURCE_INGEST_QUESTION_NOT_SOURCE_DERIVED",
                      [row["point"] for row in report["findings"]])

    def test_ingestion_refuses_unequal_question_id_collision(self):
        manifest = self.manifest()
        manifest["questions"][0]["id"] = "Q-AUTHOR-REL-01"
        report = source_pipeline.plan_ingestion(
            self.acquisition(), manifest, self.package())
        self.assertIn("SOURCE_INGEST_ID_COLLISION",
                      [row["point"] for row in report["findings"]])

    def test_resource_snapshot_must_be_the_acquired_bytes(self):
        manifest = self.manifest()
        manifest["resource"]["snapshot_digest"] = "f" * 64
        report = source_pipeline.plan_ingestion(
            self.acquisition(), manifest, self.package())
        self.assertIn("SOURCE_INGEST_RESOURCE_DIGEST_MISMATCH",
                      [row["point"] for row in report["findings"]])


if __name__ == "__main__":
    unittest.main()
