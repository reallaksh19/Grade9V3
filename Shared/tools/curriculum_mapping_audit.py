#!/usr/bin/env python3
"""Audit opt-in curriculum mappings against globally declared curriculum resources.

The library schema already stores curriculum mappings, but an empty array and an
unverified mapping are both structurally valid.  A bucket can therefore opt into a
stronger contract with:

    extensions.curriculum_mapping_policy = "VERIFIED"

For those buckets this audit requires:
- the bucket itself has a VERIFIED mapping,
- every taught primary capability has a VERIFIED mapping,
- declared Grade 9 track metadata agrees with at least one verified mapping, and
- every verified mapping names a globally resolvable CURRICULUM resource that has
  actually been inspected.

The rule is subject-neutral.  It does not know CBSE, Grade 9, Physics, or any topic.
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

POLICY = "VERIFIED"
INSPECTED = {"SECTION_INSPECTED", "FULL_ITEM_INSPECTED"}


def _verified_mappings(record: dict) -> list[dict]:
    return [
        mapping for mapping in record.get("curriculum_mappings", [])
        if isinstance(mapping, dict) and mapping.get("mapping_status") == "VERIFIED"
    ]


def _record_mapping_findings(record: dict, records: dict, *, expected_track: str | None,
                             owner: str) -> list[dict]:
    findings: list[dict] = []
    mappings = _verified_mappings(record)
    if not mappings:
        findings.append({
            "point": "CURRICULUM_MAPPING_UNVERIFIED",
            "record": record.get("id"),
            "owner": owner,
            "detail": "record opts into verified curriculum mapping but has no VERIFIED mapping",
        })
        return findings

    if expected_track and not any(mapping.get("track") == expected_track for mapping in mappings):
        findings.append({
            "point": "CURRICULUM_TRACK_MISMATCH",
            "record": record.get("id"),
            "owner": owner,
            "expected_track": expected_track,
            "mapped_tracks": sorted({mapping.get("track") for mapping in mappings
                                     if mapping.get("track")}),
            "detail": "record track metadata is not represented by a VERIFIED mapping",
        })

    for mapping in mappings:
        source_ref = mapping.get("source_ref")
        if not source_ref:
            findings.append({
                "point": "CURRICULUM_MAPPING_SOURCE_MISSING",
                "record": record.get("id"),
                "owner": owner,
                "detail": "VERIFIED mapping has no curriculum source_ref",
            })
            continue
        source = records.get(source_ref)
        if not source or source.get("_collection") != "resources":
            findings.append({
                "point": "CURRICULUM_MAPPING_SOURCE_UNRESOLVED",
                "record": record.get("id"),
                "owner": owner,
                "source_ref": source_ref,
                "detail": "VERIFIED mapping source_ref does not resolve to a resource record",
            })
            continue
        if "CURRICULUM" not in source.get("role", []):
            findings.append({
                "point": "CURRICULUM_MAPPING_SOURCE_WRONG_ROLE",
                "record": record.get("id"),
                "owner": owner,
                "source_ref": source_ref,
                "detail": "VERIFIED mapping points to a resource that is not marked CURRICULUM",
            })
        if source.get("access_status") not in INSPECTED:
            findings.append({
                "point": "CURRICULUM_MAPPING_SOURCE_NOT_INSPECTED",
                "record": record.get("id"),
                "owner": owner,
                "source_ref": source_ref,
                "detail": "VERIFIED mapping source has not been inspected at section/full-item level",
            })
        if not str(source.get("last_checked", "")).strip():
            findings.append({
                "point": "CURRICULUM_MAPPING_SOURCE_UNDATED",
                "record": record.get("id"),
                "owner": owner,
                "source_ref": source_ref,
                "detail": "VERIFIED mapping source has no last_checked date",
            })
    return findings


def audit(subject: str, repo: Path = REPO) -> dict:
    library_paths = sorted((repo / subject / "library").glob("*.v1.json"))
    packages = [load(path) for path in library_paths]
    records = build_index(packages)

    findings: list[dict] = []
    rows: list[dict] = []
    buckets = sorted(
        (record for record in records.values()
         if record.get("_collection") == "buckets"
         and (record.get("extensions") or {}).get("curriculum_mapping_policy") == POLICY),
        key=lambda record: record["id"],
    )

    for bucket in buckets:
        bucket_id = bucket["id"]
        bucket_track = (bucket.get("extensions") or {}).get("grade9_track")
        findings.extend(_record_mapping_findings(
            bucket, records, expected_track=bucket_track, owner=bucket_id))

        capability_ids = sorted({
            record.get("primary_capability_ref")
            for record in records.values()
            if record.get("_collection") == "microtopics"
            and record.get("bucket_id") == bucket_id
            and record.get("primary_capability_ref")
        })
        capability_rows = []
        for capability_id in capability_ids:
            capability = records.get(capability_id)
            if not capability or capability.get("_collection") != "capabilities":
                findings.append({
                    "point": "CURRICULUM_CAPABILITY_UNRESOLVED",
                    "record": capability_id,
                    "owner": bucket_id,
                    "detail": "taught primary capability does not resolve to a capability record",
                })
                continue
            cap_track = (capability.get("extensions") or {}).get("grade9_track") or bucket_track
            cap_findings = _record_mapping_findings(
                capability, records, expected_track=cap_track, owner=bucket_id)
            findings.extend(cap_findings)
            capability_rows.append({
                "capability": capability_id,
                "track": cap_track,
                "verified_mappings": len(_verified_mappings(capability)),
            })

        rows.append({
            "bucket": bucket_id,
            "track": bucket_track,
            "verified_mappings": len(_verified_mappings(bucket)),
            "capabilities": capability_rows,
        })

    return {
        "subject": subject,
        "policy_buckets": rows,
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
