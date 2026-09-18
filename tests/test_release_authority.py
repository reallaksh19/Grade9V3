"""Final learner-release authority, drift invalidation, and bypass falsifiers."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.contracts import digest  # noqa: E402
from Shared.tools import compile_execution_packet, release_authority  # noqa: E402


class ReleaseAuthority(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        for name in ("release-request.schema.json", "release-receipt.schema.json"):
            target = self.repo / "Shared/library" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / "Shared/library" / name, target)

        self.request = {
            "request_id": "REQ-RELEASE-TEST",
            "subject": "Physics",
            "subtopic": "Synthetic",
            "requested_cores": ["CORE1"],
        }
        self.request_path = self.repo / "Requests/release-test.author-request.json"
        self.request_path.parent.mkdir(parents=True, exist_ok=True)
        self.request_path.write_text(json.dumps(self.request, indent=2) + "\n", encoding="utf-8")

        self.publication = self.repo / "Physics/content/release-test/publication"
        (self.publication / "inputs").mkdir(parents=True, exist_ok=True)
        (self.publication / "CORE1.html").write_text("<main>released fixture</main>", encoding="utf-8")
        (self.publication / "inputs/plan.json").write_text(
            json.dumps({"products": [{"core": "CORE1"}]}, indent=2) + "\n", encoding="utf-8")
        self.manifest = {
            "basis_digest": "b" * 64,
            "runtime_digest": "r" * 64,
            "files": [{"path": "CORE1.html", "sha256": "a" * 64}],
            "release_authorized": False,
            "portable_scope": "TEST",
        }
        (self.publication / "manifest.json").write_text(
            json.dumps(self.manifest, indent=2) + "\n", encoding="utf-8")

        run = self.publication.parent
        (run / "inputs").mkdir(exist_ok=True)
        (run / "inputs/library_records.json").write_text(
            json.dumps(["MIC-X"], indent=2) + "\n", encoding="utf-8")
        self.provenance = {
            "run_id": "release-test",
            "basis": "LIBRARY",
            "reason": "Synthetic release-authority fixture.",
            "records": ["MIC-X"],
        }
        (run / "provenance.json").write_text(
            json.dumps(self.provenance, indent=2) + "\n", encoding="utf-8")

        promo = {
            "promotion_id": "PROMO-X",
            "authoring_run_receipt": {
                "path": "publication/authoring-runs/RUN-X.receipt.json",
                "digest": "d" * 64,
            },
            "prior_promotion_receipt": None,
        }
        promo_path = self.repo / "Reviews/receipts/PROMO-X.json"
        promo_path.parent.mkdir(parents=True, exist_ok=True)
        promo_path.write_text(json.dumps(promo, indent=2) + "\n", encoding="utf-8")

        self.plan = {
            "lifecycle": {"RELEASE": {"state": "READY_FOR_RELEASE", "blockers": []}},
            "products": [{"core": "CORE1", "state": "READY"}],
            "learner_route": {
                "state": "READY", "entry": "R1", "bridges": [], "unresolved": []
            },
            "source": {"receipt_ref": None, "receipt_digest": None},
        }
        self.packet = {"packet_id": "PACKET-X", "mode": "AUTHORING_EXECUTION_PACKET"}

    def tearDown(self):
        self.temp.cleanup()

    def release_request(self):
        return {
            "release_id": "REL-TEST-01",
            "version": "1.0.0",
            "subject": "Physics",
            "request_path": "Requests/release-test.author-request.json",
            "request_digest": digest(self.request),
            "packet_digest": digest(self.packet),
            "publication_path": "Physics/content/release-test/publication",
        }

    def patches(self, plan=None):
        plan = plan or self.plan
        return (
            mock.patch.object(release_authority.plan_request, "plan", return_value=plan),
            mock.patch.object(
                release_authority.compile_execution_packet, "compile_packet",
                return_value=self.packet),
            mock.patch.object(
                release_authority.compile_execution_packet, "verify",
                return_value={"verified": True, "findings": []}),
            mock.patch.object(
                release_authority.republish, "verify",
                return_value={"status": "PASS", "scope": "EXACT_BYTES"}),
            mock.patch.object(
                release_authority.publication_provenance, "findings",
                return_value=([], {"basis": "LIBRARY"})),
            mock.patch.object(
                release_authority, "_records",
                return_value=(
                    {
                        "MIC-X": {
                            "id": "MIC-X",
                            "status": "REVIEWED",
                            "_collection": "microtopics",
                            "_package": "PKG-X",
                        }
                    },
                    {"PKG-X": "Physics/library/x.json"},
                )),
            mock.patch.object(
                release_authority.review_authority, "authority_for_record",
                return_value={
                    "verified": True,
                    "state": "REVIEWED",
                    "receipt": "Reviews/receipts/PROMO-X.json",
                    "findings": [],
                }),
        )

    def evaluate_with(self, request=None, plan=None):
        patches = self.patches(plan)
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
            return release_authority.evaluate(request or self.release_request(), self.repo)

    def verify_with(self, receipt, plan=None):
        patches = self.patches(plan)
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
            return release_authority.verify_receipt(receipt, self.repo)

    def test_valid_release_binds_full_governed_chain(self):
        report = self.evaluate_with()
        self.assertTrue(report["passed"], report["findings"])
        receipt = report["receipt"]
        self.assertEqual(receipt["validation"]["state"], "RELEASED")
        self.assertEqual(receipt["request"]["digest"], digest(self.request))
        self.assertEqual(receipt["execution_packet"]["digest"], digest(self.packet))
        self.assertEqual(receipt["publication"]["provenance_basis"], "LIBRARY")
        self.assertEqual(receipt["learner_route"]["digest"], digest(self.plan["learner_route"]))
        self.assertEqual(
            [row["record_id"] for row in receipt["reviewed_records"]], ["MIC-X"])
        self.assertEqual(
            [row["path"] for row in receipt["promotion_receipts"]],
            ["Reviews/receipts/PROMO-X.json"])
        self.assertEqual(
            [row["path"] for row in receipt["authoring_receipts"]],
            ["publication/authoring-runs/RUN-X.receipt.json"])
        self.assertFalse(self.manifest["release_authorized"])

    def test_publication_manifest_cannot_self_authorize(self):
        manifest = dict(self.manifest)
        manifest["release_authorized"] = True
        (self.publication / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        report = self.evaluate_with()
        self.assertIn("PUBLICATION_MANIFEST_CANNOT_SELF_AUTHORIZE_RELEASE",
                      [row["point"] for row in report["findings"]])

    def test_non_library_publication_cannot_receive_learner_release(self):
        provenance = dict(self.provenance)
        provenance["basis"] = "AUTHORED_OUTSIDE_THE_LIBRARY"
        (self.publication.parent / "provenance.json").write_text(
            json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
        report = self.evaluate_with()
        self.assertIn("RELEASE_REQUIRES_LIBRARY_BASIS",
                      [row["point"] for row in report["findings"]])

    def test_manifest_change_stales_existing_release_receipt(self):
        issued = self.evaluate_with()["receipt"]
        manifest = dict(self.manifest)
        manifest["portable_scope"] = "CHANGED_AFTER_RELEASE"
        (self.publication / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        report = self.verify_with(issued)
        self.assertFalse(report["verified"])
        self.assertIn("RELEASE_RECEIPT_STALE",
                      [row["point"] for row in report["findings"]])

    def test_learner_route_change_stales_existing_release_receipt(self):
        issued = self.evaluate_with()["receipt"]
        changed = json.loads(json.dumps(self.plan))
        changed["learner_route"]["entry"] = "R2"
        report = self.verify_with(issued, changed)
        self.assertFalse(report["verified"])
        self.assertIn("RELEASE_RECEIPT_STALE",
                      [row["point"] for row in report["findings"]])

    def test_request_change_blocks_old_release_receipt(self):
        issued = self.evaluate_with()["receipt"]
        changed = dict(self.request)
        changed["requested_cores"] = ["CORE1", "CORE1A"]
        self.request_path.write_text(json.dumps(changed, indent=2) + "\n", encoding="utf-8")
        report = self.verify_with(issued)
        self.assertFalse(report["verified"])
        self.assertIn("RELEASE_REQUEST_STALE",
                      [row["point"] for row in report["findings"]])

    def test_unbacked_learner_facing_record_blocks_release(self):
        patches = self.patches()
        bad = mock.patch.object(
            release_authority.review_authority, "authority_for_record",
            return_value={"verified": False, "state": "UNBACKED_REVIEWED",
                          "receipt": None, "findings": []})
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], bad:
            report = release_authority.evaluate(self.release_request(), self.repo)
        self.assertIn("RELEASE_RECORD_REVIEW_UNBACKED",
                      [row["point"] for row in report["findings"]])

    def test_audit_detects_manifest_release_flag_bypass(self):
        manifest = dict(self.manifest)
        manifest["release_authorized"] = True
        (self.publication / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        report = release_authority.audit(self.repo)
        self.assertFalse(report["passed"])
        self.assertEqual(
            [row["point"] for row in report["findings"]],
            ["PUBLICATION_MANIFEST_CANNOT_SELF_AUTHORIZE_RELEASE"],
        )


class CurrentRepositoryReleaseBoundary(unittest.TestCase):
    def test_current_relative_motion_publication_is_not_accidentally_releasable(self):
        path = REPO / "Requests/relative-motion-teaching.author-request.json"
        request = json.loads(path.read_text(encoding="utf-8"))
        packet = compile_execution_packet.compile_packet(request)
        attempt = {
            "release_id": "REL-CURRENT-BOUNDARY-TEST",
            "version": "1.0.0",
            "subject": "Physics",
            "request_path": "Requests/relative-motion-teaching.author-request.json",
            "request_digest": digest(request),
            "packet_digest": digest(packet),
            "publication_path": "Physics/content/relative-motion-library/publication",
        }
        report = release_authority.evaluate(attempt)
        self.assertFalse(report["passed"])
        self.assertIn("RELEASE_LIFECYCLE_NOT_READY",
                      [row["point"] for row in report["findings"]])


if __name__ == "__main__":
    unittest.main()
