#!/usr/bin/env python3
"""Audit opt-in teaching-route coverage for authored bucket microtopics.

A bucket may set:

    extensions.teaching_route_coverage_policy = "ALL_MICROTOPICS_CORE1A_CORE1B"

For such buckets, every microtopic owned by the bucket must be reachable through at
least one CORE1A route and at least one CORE1B route.  The audit is subject-neutral:
it discovers bucket ownership from microtopic.bucket_id and teaching reachability
from route.microtopic_refs.
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

POLICY = "ALL_MICROTOPICS_CORE1A_CORE1B"
REQUIRED_CORES = ("CORE1A", "CORE1B")


def audit(subject: str, repo: Path = REPO) -> dict:
    paths = sorted((repo / subject / "library").glob("*.v1.json"))
    packages = [load(path) for path in paths]
    records = build_index(packages)

    findings: list[dict] = []
    rows: list[dict] = []

    buckets = sorted(
        (
            record for record in records.values()
            if record.get("_collection") == "buckets"
            and (record.get("extensions") or {}).get("teaching_route_coverage_policy") == POLICY
        ),
        key=lambda record: record["id"],
    )
    routes = [
        record for record in records.values()
        if record.get("_collection") == "teaching_routes"
    ]

    for bucket in buckets:
        bucket_id = bucket["id"]
        microtopics = sorted(
            record["id"]
            for record in records.values()
            if record.get("_collection") == "microtopics"
            and record.get("bucket_id") == bucket_id
        )
        owned = set(microtopics)
        by_core: dict[str, dict] = {}

        for core in REQUIRED_CORES:
            matching_routes = [
                route for route in routes
                if core in route.get("cores", [])
                and owned.intersection(route.get("microtopic_refs", []))
            ]
            covered = sorted({
                ref
                for route in matching_routes
                for ref in route.get("microtopic_refs", [])
                if ref in owned
            })
            missing = sorted(owned - set(covered))
            by_core[core] = {
                "routes": sorted(route["id"] for route in matching_routes),
                "covered": covered,
                "missing": missing,
            }
            if missing:
                findings.append({
                    "point": "TEACHING_ROUTE_COVERAGE_INCOMPLETE",
                    "bucket": bucket_id,
                    "core": core,
                    "missing_microtopics": missing,
                    "detail": (
                        f"bucket opts into {POLICY} but {core} routes do not cover "
                        "every owned microtopic"
                    ),
                })

        rows.append({
            "bucket": bucket_id,
            "microtopics": microtopics,
            "cores": by_core,
        })

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
