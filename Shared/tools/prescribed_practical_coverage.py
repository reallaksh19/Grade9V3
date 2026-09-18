#!/usr/bin/env python3
"""Audit prescribed practical custody declared by library buckets.

A bucket may declare official practical obligations in:

    extensions.practical_coverage_policy = "PRESCRIBED_PRACTICALS"
    extensions.prescribed_practicals = [
      {
        "id": "...",
        "source_ref": "...",
        "locator": "...",
        "capability_ref": "..."
      }
    ]

Each obligation must resolve to an inspected CURRICULUM source, target a primary
capability taught by that bucket, and be exercised by at least one bucket-owned
CORE2A/CORE2B question whose extensions.prescribed_practical_refs names the
obligation.  The audit is subject-, board-, grade- and topic-neutral.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402
from Shared.library.resolve import build_index  # noqa: E402

POLICY = "PRESCRIBED_PRACTICALS"
PRACTICE_CORES = {"CORE2A", "CORE2B"}
INSPECTED = {"SECTION_INSPECTED", "FULL_ITEM_INSPECTED"}


def audit(subject: str, repo: Path = REPO) -> dict:
    paths = sorted((repo / subject / "library").glob("*.v1.json"))
    packages = [load(path) for path in paths]
    records = build_index(packages)

    findings: list[dict] = []
    rows: list[dict] = []
    seen_ids: set[str] = set()

    buckets = sorted(
        (
            record for record in records.values()
            if record.get("_collection") == "buckets"
            and (record.get("extensions") or {}).get("practical_coverage_policy") == POLICY
        ),
        key=lambda record: record["id"],
    )

    for bucket in buckets:
        bucket_id = bucket["id"]
        extensions = bucket.get("extensions") or {}
        obligations = extensions.get("prescribed_practicals") or []
        if not isinstance(obligations, list) or not obligations:
            findings.append({
                "point": "PRACTICAL_OBLIGATIONS_MISSING",
                "bucket": bucket_id,
                "detail": f"bucket opts into {POLICY} but declares no prescribed practicals",
            })
            obligations = []

        taught_caps = {
            record.get("primary_capability_ref")
            for record in records.values()
            if record.get("_collection") == "microtopics"
            and record.get("bucket_id") == bucket_id
            and record.get("primary_capability_ref")
        }
        questions = [
            record for record in records.values()
            if record.get("_collection") == "questions"
            and record.get("primary_capability_ref") in taught_caps
            and any(entry.get("core") in PRACTICE_CORES
                    for entry in record.get("exposure", []))
        ]

        obligation_rows = []
        for obligation in obligations:
            oid = obligation.get("id")
            source_ref = obligation.get("source_ref")
            capability_ref = obligation.get("capability_ref")
            locator = obligation.get("locator")

            if not isinstance(oid, str) or not oid.strip():
                findings.append({
                    "point": "PRACTICAL_ID_MISSING", "bucket": bucket_id,
                    "detail": "prescribed practical has no non-empty id",
                })
                continue
            if oid in seen_ids:
                findings.append({
                    "point": "PRACTICAL_ID_DUPLICATE", "bucket": bucket_id,
                    "practical": oid,
                    "detail": "prescribed practical id is duplicated within the subject",
                })
            seen_ids.add(oid)

            if not isinstance(locator, str) or not locator.strip():
                findings.append({
                    "point": "PRACTICAL_LOCATOR_MISSING", "bucket": bucket_id,
                    "practical": oid,
                    "detail": "prescribed practical has no source locator",
                })

            source = records.get(source_ref)
            if not source or source.get("_collection") != "resources":
                findings.append({
                    "point": "PRACTICAL_SOURCE_UNRESOLVED", "bucket": bucket_id,
                    "practical": oid, "source_ref": source_ref,
                    "detail": "prescribed practical source_ref does not resolve to a resource",
                })
            else:
                if "CURRICULUM" not in source.get("role", []):
                    findings.append({
                        "point": "PRACTICAL_SOURCE_WRONG_ROLE", "bucket": bucket_id,
                        "practical": oid, "source_ref": source_ref,
                        "detail": "prescribed practical source is not marked CURRICULUM",
                    })
                if source.get("access_status") not in INSPECTED:
                    findings.append({
                        "point": "PRACTICAL_SOURCE_NOT_INSPECTED", "bucket": bucket_id,
                        "practical": oid, "source_ref": source_ref,
                        "detail": "prescribed practical source has not been inspected",
                    })

            if capability_ref not in taught_caps:
                findings.append({
                    "point": "PRACTICAL_CAPABILITY_NOT_TAUGHT", "bucket": bucket_id,
                    "practical": oid, "capability_ref": capability_ref,
                    "detail": "prescribed practical targets a capability not taught by this bucket",
                })

            matching = []
            for question in questions:
                practical_refs = (question.get("extensions") or {}).get(
                    "prescribed_practical_refs", [])
                question_caps = {
                    question.get("primary_capability_ref"),
                    *question.get("secondary_capability_refs", []),
                }
                if oid in practical_refs and capability_ref in question_caps:
                    matching.append(question["id"])

            if not matching:
                findings.append({
                    "point": "PRACTICAL_PRACTICE_MISSING", "bucket": bucket_id,
                    "practical": oid, "capability_ref": capability_ref,
                    "detail": (
                        "no bucket-owned CORE2A/CORE2B question both names this practical "
                        "and exercises its declared capability"
                    ),
                })

            obligation_rows.append({
                "id": oid,
                "source_ref": source_ref,
                "locator": locator,
                "capability_ref": capability_ref,
                "question_refs": sorted(matching),
            })

        rows.append({"bucket": bucket_id, "practicals": obligation_rows})

    return {
        "subject": subject,
        "policy": POLICY,
        "buckets": rows,
        "findings": findings,
        "passed": not findings,
    }


def audit_all(repo: Path = REPO) -> dict:
    subjects = sorted({
        path.parent.parent.name
        for path in repo.glob("*/library/*.v1.json")
        if path.parent.is_dir()
    })
    reports = [audit(subject, repo) for subject in subjects]
    findings = [
        {**finding, "subject": report["subject"]}
        for report in reports
        for finding in report["findings"]
    ]
    return {"subjects": reports, "findings": findings, "passed": not findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--subject")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    report = audit(args.subject) if args.subject else audit_all()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
