"""Shared bucket-local practice ownership.

A bucket owns a practice question only when the question's primary capability is
taught by a microtopic in that bucket. Prerequisite capabilities may be reachable
through slice_for_bucket(), but reachability is not custody.

All planner/compiler/readiness code must use this module rather than re-implementing
that distinction independently.
"""
from __future__ import annotations


PRACTICE_CORES = {"CORE2A", "CORE2B"}


def bucket_primary_capabilities(records: dict, bucket_id: str) -> set[str]:
    return {
        record.get("primary_capability_ref")
        for record in records.values()
        if record.get("_collection") == "microtopics"
        and record.get("bucket_id") == bucket_id
        and record.get("primary_capability_ref")
    }


def owned_questions(records: dict, bucket_id: str, core: str | None = None) -> list[dict]:
    """Questions genuinely owned by *bucket_id*, optionally exposed to one practice core."""
    capabilities = bucket_primary_capabilities(records, bucket_id)
    rows = []
    for record in records.values():
        if record.get("_collection") != "questions":
            continue
        if record.get("primary_capability_ref") not in capabilities:
            continue
        if core is not None and not any(
                exposure.get("core") == core for exposure in record.get("exposure", [])):
            continue
        rows.append(record)
    return sorted(rows, key=lambda record: record["id"])


def has_owned_exposure(records: dict, bucket_id: str, core: str) -> bool:
    return bool(owned_questions(records, bucket_id, core))
