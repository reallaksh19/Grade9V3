#!/usr/bin/env python3
"""Issue and verify immutable learner-release receipts over the full governed chain."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError, digest, file_digest, load  # noqa: E402
from Shared.library.resolve import build_index, load_packages  # noqa: E402
from Shared.tools import (compile_execution_packet, plan_request, publication_provenance,  # noqa: E402
                          republish, review_authority)

REQUEST_SCHEMA = REPO / "Shared/library/release-request.schema.json"
RECEIPT_SCHEMA = REPO / "Shared/library/release-receipt.schema.json"


def _schema_findings(value: dict, schema: Path, point: str) -> list[dict]:
    try:
        import jsonschema
    except ModuleNotFoundError:
        return []
    validator = jsonschema.Draft202012Validator(load(schema))
    return [{
        "point": point,
        "where": "/".join(str(part) for part in error.path),
        "detail": error.message,
    } for error in validator.iter_errors(value)]


def _safe_file(path_text: str, root: Path, repo: Path) -> Path | None:
    candidate = (repo / path_text).resolve()
    try:
        candidate.relative_to((repo / root).resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def _publication_path(path_text: str, subject: str, repo: Path) -> Path | None:
    candidate = (repo / path_text).resolve()
    try:
        candidate.relative_to((repo / subject / "content").resolve())
    except ValueError:
        return None
    return candidate if candidate.is_dir() and candidate.name == "publication" else None


def _records(subject: str, repo: Path) -> tuple[dict, dict]:
    packages = []
    package_paths = {}
    for path in sorted((repo / subject / "library").glob("*.json")):
        package = load(path)
        packages.append(package)
        if package.get("package_id"):
            package_paths[package["package_id"]] = str(path.relative_to(repo))
    return build_index(packages), package_paths


def _public(record: dict) -> dict:
    return {k: v for k, v in record.items() if not k.startswith("_")}


def _receipt_ref(path_text: str, repo: Path) -> dict:
    value = load(repo / path_text)
    return {"path": path_text, "digest": digest(value)}


def _collect_review_chain(authority: dict, repo: Path) -> tuple[list[dict], list[dict]]:
    promotion, authoring = {}, {}
    path = authority.get("receipt")
    while path:
        receipt = load(repo / path)
        promotion[path] = _receipt_ref(path, repo)
        auth = receipt.get("authoring_run_receipt")
        if auth:
            authoring[auth["path"]] = {
                "path": auth["path"],
                "digest": auth["digest"],
            }
        prior = receipt.get("prior_promotion_receipt")
        path = prior.get("path") if prior else None
    return (
        [promotion[k] for k in sorted(promotion)],
        [authoring[k] for k in sorted(authoring)],
    )


def evaluate(release_request: dict, repo: Path = REPO) -> dict:
    findings = _schema_findings(
        release_request, repo / "Shared/library/release-request.schema.json",
        "RELEASE_REQUEST_STRUCTURE",
    )

    def fail(point: str, where: str, detail: str) -> None:
        findings.append({"point": point, "where": where, "detail": detail})

    subject = release_request.get("subject", "")
    request_path = _safe_file(release_request.get("request_path", ""), Path("Requests"), repo)
    if request_path is None:
        fail("RELEASE_REQUEST_INPUT_MISSING", release_request.get("request_path", ""),
             "release request must point at a committed authoring request under Requests/")
        return {"passed": False, "findings": findings, "receipt": None}

    request = load(request_path)
    if request.get("subject") != subject:
        fail("RELEASE_SUBJECT_MISMATCH", subject, "release subject differs from the authoring request")
    if digest(request) != release_request.get("request_digest"):
        fail("RELEASE_REQUEST_STALE", str(request_path.relative_to(repo)),
             "authoring request digest changed")

    publication = _publication_path(release_request.get("publication_path", ""), subject, repo)
    if publication is None:
        fail("RELEASE_PUBLICATION_INVALID", release_request.get("publication_path", ""),
             "publication must resolve inside <subject>/content/*/publication")
        return {"passed": False, "findings": findings, "receipt": None}

    fresh_plan = plan_request.plan(request, repo)
    if fresh_plan.get("lifecycle", {}).get("RELEASE", {}).get("state") != "READY_FOR_RELEASE":
        blockers = fresh_plan.get("lifecycle", {}).get("RELEASE", {}).get("blockers", [])
        fail("RELEASE_LIFECYCLE_NOT_READY", request.get("request_id", ""),
             "fresh planner release state is blocked: " + ", ".join(blockers))

    packet = compile_execution_packet.compile_packet(request, repo)
    packet_check = compile_execution_packet.verify(packet, request, repo)
    findings.extend(packet_check.get("findings", []))
    if digest(packet) != release_request.get("packet_digest"):
        fail("RELEASE_PACKET_STALE", packet.get("packet_id", ""),
             "fresh execution packet digest differs from the pinned packet digest")

    try:
        publication_check = republish.verify(publication, repo)
    except (ContractError, FileNotFoundError, KeyError, ValueError) as exc:
        code = getattr(exc, "code", "PUBLICATION_VERIFY_FAILED")
        detail = getattr(exc, "detail", str(exc))
        fail("RELEASE_PUBLICATION_VERIFY_FAILED", code, detail)
        publication_check = None

    run = publication.parent
    provenance_findings, provenance_measure = publication_provenance.findings(run, repo)
    for item in provenance_findings:
        fail("RELEASE_PUBLICATION_PROVENANCE_INVALID", item.get("point", ""),
             item.get("detail", "publication provenance finding"))
    provenance_path = run / publication_provenance.DECLARATION
    provenance = load(provenance_path) if provenance_path.is_file() else {}
    if provenance.get("basis") != publication_provenance.LIBRARY:
        fail("RELEASE_REQUIRES_LIBRARY_BASIS", str(run.relative_to(repo)),
             "learner release requires a publication compiled from canonical library records")

    manifest = load(publication / "manifest.json")
    if manifest.get("release_authorized") is not False:
        fail("PUBLICATION_MANIFEST_CANNOT_SELF_AUTHORIZE_RELEASE",
             str((publication / "manifest.json").relative_to(repo)),
             "publication manifest must remain machine-non-authoritative")

    pub_plan = load(publication / "inputs/plan.json")
    publication_cores = sorted(row["core"] for row in pub_plan.get("products", []))
    ready_cores = sorted(
        row["core"] for row in fresh_plan.get("products", [])
        if row.get("state") == "READY"
    )
    if publication_cores != ready_cores:
        fail("RELEASE_PRODUCT_SET_MISMATCH", str(publication.relative_to(repo)),
             f"publication has {publication_cores}; fresh ready product set is {ready_cores}")

    records, package_paths = _records(subject, repo)
    listed = run / "inputs/library_records.json"
    record_ids = list(load(listed)) if listed.is_file() else list(provenance.get("records") or [])
    reviewed_records, promotion_refs, authoring_refs = [], {}, {}
    for rid in sorted(set(record_ids)):
        record = records.get(rid)
        if not record or record.get("_collection") not in {"microtopics", "questions"}:
            continue
        target = package_paths.get(record.get("_package"))
        authority = (
            review_authority.authority_for_record(subject, target, _public(record), repo)
            if target else {"verified": False, "state": "NOT_REVIEWED", "findings": []}
        )
        if not authority.get("verified") or authority.get("state") not in {"REVIEWED", "CURATED"}:
            fail("RELEASE_RECORD_REVIEW_UNBACKED", rid,
                 f"learner-facing {record.get('_collection')} has no current digest-backed review authority")
            continue
        reviewed_records.append({
            "record_id": rid,
            "collection": record["_collection"],
            "status": record.get("status"),
            "record_digest": digest(_public(record)),
            "promotion_receipt": authority.get("receipt"),
        })
        promotions, authorings = _collect_review_chain(authority, repo)
        for row in promotions:
            promotion_refs[row["path"]] = row
        for row in authorings:
            authoring_refs[row["path"]] = row

    source_pin = None
    source = fresh_plan.get("source") or {}
    if source.get("receipt_ref"):
        if not source.get("receipt_digest"):
            fail("RELEASE_SOURCE_RECEIPT_UNPINNED", source.get("receipt_ref", ""),
                 "fresh plan uses a source receipt without an immutable digest")
        else:
            source_pin = {
                "receipt_id": source.get("receipt_ref"),
                "digest": source.get("receipt_digest"),
            }

    if findings:
        return {"passed": False, "findings": findings, "receipt": None}

    receipt = {
        "release_id": release_request["release_id"],
        "version": "1.0.0",
        "subject": subject,
        "request": {
            "path": str(request_path.relative_to(repo)),
            "digest": digest(request),
        },
        "plan": {
            "digest": digest(fresh_plan),
            "release_state": fresh_plan["lifecycle"]["RELEASE"]["state"],
            "products": ready_cores,
        },
        "execution_packet": {
            "packet_id": packet["packet_id"],
            "digest": digest(packet),
        },
        "publication": {
            "path": str(publication.relative_to(repo)),
            "manifest_digest": digest(manifest),
            "basis_digest": manifest.get("basis_digest"),
            "manifest_files_digest": digest(manifest.get("files", [])),
            "learner_visible_files": [
                row for row in manifest.get("files", [])
                if row.get("path", "").endswith(".html")
                or row.get("path", "").startswith("figures/")
            ],
            "provenance_digest": digest(provenance),
            "provenance_basis": provenance.get("basis"),
            "verification_scope": publication_check.get("scope") if publication_check else None,
        },
        "learner_route": {
            "digest": digest(fresh_plan.get("learner_route")),
            "value": fresh_plan.get("learner_route"),
        },
        "source_receipt": source_pin,
        "reviewed_records": reviewed_records,
        "promotion_receipts": [promotion_refs[k] for k in sorted(promotion_refs)],
        "authoring_receipts": [authoring_refs[k] for k in sorted(authoring_refs)],
        "validation": {
            "state": "RELEASED",
            "findings": [],
            "note": "Release is valid only while this receipt recomputes exactly from current governed inputs. The publication manifest itself remains release_authorized=false.",
        },
    }
    schema_findings = _schema_findings(
        receipt, repo / "Shared/library/release-receipt.schema.json",
        "RELEASE_RECEIPT_STRUCTURE",
    )
    if schema_findings:
        return {"passed": False, "findings": schema_findings, "receipt": None}
    return {"passed": True, "findings": [], "receipt": receipt}


def verify_receipt(receipt: dict, repo: Path = REPO) -> dict:
    structural = _schema_findings(
        receipt, repo / "Shared/library/release-receipt.schema.json",
        "RELEASE_RECEIPT_STRUCTURE",
    )
    if structural:
        return {"verified": False, "findings": structural}
    request = {
        "release_id": receipt["release_id"],
        "version": "1.0.0",
        "subject": receipt["subject"],
        "request_path": receipt["request"]["path"],
        "request_digest": receipt["request"]["digest"],
        "packet_digest": receipt["execution_packet"]["digest"],
        "publication_path": receipt["publication"]["path"],
    }
    fresh = evaluate(request, repo)
    if not fresh["passed"]:
        return {"verified": False, "findings": fresh["findings"]}
    if digest(fresh["receipt"]) != digest(receipt):
        return {"verified": False, "findings": [{
            "point": "RELEASE_RECEIPT_STALE",
            "where": receipt.get("release_id", ""),
            "detail": "recomputed release authority no longer matches the stored receipt",
        }]}
    return {"verified": True, "findings": [], "release_id": receipt["release_id"]}


def write_release(report: dict, repo: Path = REPO) -> dict:
    if not report.get("passed") or not report.get("receipt"):
        raise ValueError("cannot write a blocked release")
    receipt = report["receipt"]
    out = repo / "Releases/receipts" / f'{receipt["release_id"]}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise ValueError("release receipt already exists")
    out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(out.relative_to(repo)), "receipt": receipt}


def audit(repo: Path = REPO) -> dict:
    rows, findings = [], []
    root = repo / "Releases/receipts"
    if root.is_dir():
        for path in sorted(root.glob("*.json")):
            report = verify_receipt(load(path), repo)
            rows.append({"path": str(path.relative_to(repo)), **report})
            findings.extend(report.get("findings", []))

    self_authorized = []
    for manifest_path in sorted(repo.glob("*/content/*/publication/manifest.json")):
        manifest = load(manifest_path)
        if manifest.get("release_authorized") is True:
            item = {
                "point": "PUBLICATION_MANIFEST_CANNOT_SELF_AUTHORIZE_RELEASE",
                "where": str(manifest_path.relative_to(repo)),
                "detail": "release authority must exist only as a valid Releases/receipts artifact",
            }
            findings.append(item)
            self_authorized.append(str(manifest_path.relative_to(repo)))
    return {
        "receipts": rows,
        "self_authorized_manifests": self_authorized,
        "findings": findings,
        "passed": not findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--request", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    if args.audit:
        report = audit()
    elif args.receipt:
        verified = verify_receipt(load(args.receipt))
        report = {"passed": verified["verified"], **verified}
    elif args.request:
        report = evaluate(load(args.request))
        if args.write and report["passed"]:
            report["written"] = write_release(report)
    else:
        parser.error("provide --request, --receipt or --audit")

    printable = {k: v for k, v in report.items()}
    print(json.dumps(printable, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report.get("passed", report.get("verified", False)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
