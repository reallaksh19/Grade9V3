#!/usr/bin/env python3
"""Audit opt-in curriculum outcome custody.

A bucket may declare:

    extensions.curriculum_outcome_coverage_policy = "DECLARED_OUTCOMES"
    extensions.curriculum_outcomes = [
      {
        "id": "...",
        "source_ref": "...",
        "locator": "...",
        "capability_refs": ["..."],
        "microtopic_refs": ["..."],
        "question_refs": ["..."]
      }
    ]

For those buckets this audit verifies that each declared source outcome:
- points to an inspected CURRICULUM resource,
- is owned by capabilities taught in the bucket,
- is delivered by owned microtopics,
- is exercised by bucket-owned CORE2A/CORE2B practice.

It also verifies that every taught primary capability on the bucket's declared track
appears in at least one declared outcome.  The audit is subject-, board-, grade- and
topic-neutral; the finite outcome checklist lives in subject data.
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

POLICY = "DECLARED_OUTCOMES"
PRACTICE = {"CORE2A", "CORE2B"}
INSPECTED = {"SECTION_INSPECTED", "FULL_ITEM_INSPECTED"}


def _track(record: dict, fallback: str | None = None) -> str | None:
    return (record.get("extensions") or {}).get("grade9_track") or fallback


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
            and (record.get("extensions") or {}).get(
                "curriculum_outcome_coverage_policy") == POLICY
        ),
        key=lambda record: record["id"],
    )

    for bucket in buckets:
        bucket_id = bucket["id"]
        bucket_track = _track(bucket)
        outcomes = (bucket.get("extensions") or {}).get("curriculum_outcomes") or []
        if not isinstance(outcomes, list) or not outcomes:
            findings.append({
                "point": "CURRICULUM_OUTCOMES_MISSING",
                "bucket": bucket_id,
                "detail": f"bucket opts into {POLICY} but declares no outcomes",
            })
            outcomes = []

        owned_microtopics = {
            record["id"]: record
            for record in records.values()
            if record.get("_collection") == "microtopics"
            and record.get("bucket_id") == bucket_id
        }
        taught_capabilities = {
            record.get("primary_capability_ref")
            for record in owned_microtopics.values()
            if record.get("primary_capability_ref")
        }
        same_track_capabilities = {
            capability_id for capability_id in taught_capabilities
            if (
                records.get(capability_id)
                and _track(records[capability_id], bucket_track) == bucket_track
            )
        }
        owned_questions = {
            record["id"]: record
            for record in records.values()
            if record.get("_collection") == "questions"
            and record.get("primary_capability_ref") in taught_capabilities
        }

        covered_capabilities: set[str] = set()
        outcome_rows = []

        for outcome in outcomes:
            oid = outcome.get("id")
            source_ref = outcome.get("source_ref")
            locator = outcome.get("locator")
            capability_refs = outcome.get("capability_refs") or []
            microtopic_refs = outcome.get("microtopic_refs") or []
            question_refs = outcome.get("question_refs") or []

            if not isinstance(oid, str) or not oid.strip():
                findings.append({
                    "point": "CURRICULUM_OUTCOME_ID_MISSING",
                    "bucket": bucket_id,
                    "detail": "declared outcome has no non-empty id",
                })
                continue
            if oid in seen_ids:
                findings.append({
                    "point": "CURRICULUM_OUTCOME_ID_DUPLICATE",
                    "bucket": bucket_id, "outcome": oid,
                    "detail": "curriculum outcome id is duplicated within the subject",
                })
            seen_ids.add(oid)

            if not isinstance(locator, str) or not locator.strip():
                findings.append({
                    "point": "CURRICULUM_OUTCOME_LOCATOR_MISSING",
                    "bucket": bucket_id, "outcome": oid,
                    "detail": "declared outcome has no source locator",
                })

            source = records.get(source_ref)
            if not source or source.get("_collection") != "resources":
                findings.append({
                    "point": "CURRICULUM_OUTCOME_SOURCE_UNRESOLVED",
                    "bucket": bucket_id, "outcome": oid, "source_ref": source_ref,
                    "detail": "outcome source_ref does not resolve to a resource",
                })
            else:
                if "CURRICULUM" not in source.get("role", []):
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_SOURCE_WRONG_ROLE",
                        "bucket": bucket_id, "outcome": oid, "source_ref": source_ref,
                        "detail": "outcome source is not marked CURRICULUM",
                    })
                if source.get("access_status") not in INSPECTED:
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_SOURCE_NOT_INSPECTED",
                        "bucket": bucket_id, "outcome": oid, "source_ref": source_ref,
                        "detail": "outcome source has not been inspected",
                    })

            if not capability_refs:
                findings.append({
                    "point": "CURRICULUM_OUTCOME_CAPABILITY_MISSING",
                    "bucket": bucket_id, "outcome": oid,
                    "detail": "outcome names no capability owner",
                })
            for capability_ref in capability_refs:
                if capability_ref not in taught_capabilities:
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_CAPABILITY_NOT_TAUGHT",
                        "bucket": bucket_id, "outcome": oid,
                        "capability_ref": capability_ref,
                        "detail": "outcome capability is not taught by this bucket",
                    })
                else:
                    covered_capabilities.add(capability_ref)

            if not microtopic_refs:
                findings.append({
                    "point": "CURRICULUM_OUTCOME_MICROTOPIC_MISSING",
                    "bucket": bucket_id, "outcome": oid,
                    "detail": "outcome names no teaching microtopic",
                })
            for microtopic_ref in microtopic_refs:
                microtopic = owned_microtopics.get(microtopic_ref)
                if not microtopic:
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_MICROTOPIC_NOT_OWNED",
                        "bucket": bucket_id, "outcome": oid,
                        "microtopic_ref": microtopic_ref,
                        "detail": "outcome microtopic is not owned by this bucket",
                    })
                elif microtopic.get("primary_capability_ref") not in capability_refs:
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_MICROTOPIC_CAPABILITY_MISMATCH",
                        "bucket": bucket_id, "outcome": oid,
                        "microtopic_ref": microtopic_ref,
                        "detail": "outcome microtopic's primary capability is not one of the outcome owners",
                    })

            if not question_refs:
                findings.append({
                    "point": "CURRICULUM_OUTCOME_PRACTICE_MISSING",
                    "bucket": bucket_id, "outcome": oid,
                    "detail": "outcome names no practice evidence",
                })
            for question_ref in question_refs:
                question = owned_questions.get(question_ref)
                if not question:
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_QUESTION_NOT_OWNED",
                        "bucket": bucket_id, "outcome": oid,
                        "question_ref": question_ref,
                        "detail": "outcome question is not owned by this bucket",
                    })
                    continue
                if not any(entry.get("core") in PRACTICE
                           for entry in question.get("exposure", [])):
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_QUESTION_NOT_PRACTICE",
                        "bucket": bucket_id, "outcome": oid,
                        "question_ref": question_ref,
                        "detail": "outcome question has no CORE2A/CORE2B exposure",
                    })
                question_caps = {
                    question.get("primary_capability_ref"),
                    *question.get("secondary_capability_refs", []),
                }
                if not question_caps.intersection(capability_refs):
                    findings.append({
                        "point": "CURRICULUM_OUTCOME_QUESTION_CAPABILITY_MISMATCH",
                        "bucket": bucket_id, "outcome": oid,
                        "question_ref": question_ref,
                        "detail": "outcome question does not exercise any declared outcome capability",
                    })

            outcome_rows.append({
                "id": oid,
                "source_ref": source_ref,
                "locator": locator,
                "capability_refs": capability_refs,
                "microtopic_refs": microtopic_refs,
                "question_refs": question_refs,
            })

        missing_caps = sorted(same_track_capabilities - covered_capabilities)
        if missing_caps:
            findings.append({
                "point": "CURRICULUM_TRACK_CAPABILITY_WITHOUT_OUTCOME",
                "bucket": bucket_id,
                "track": bucket_track,
                "capability_refs": missing_caps,
                "detail": (
                    "taught primary capabilities on the bucket's declared track are not "
                    "owned by any declared curriculum outcome"
                ),
            })

        rows.append({
            "bucket": bucket_id,
            "track": bucket_track,
            "outcomes": outcome_rows,
            "track_capabilities": sorted(same_track_capabilities),
            "outcome_covered_capabilities": sorted(
                same_track_capabilities.intersection(covered_capabilities)),
            "missing_capabilities": missing_caps,
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
