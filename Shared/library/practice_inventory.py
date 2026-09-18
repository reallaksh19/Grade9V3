"""One definition of which questions belong to a bucket and which practice core exposes them."""
from __future__ import annotations


def bucket_capabilities(records: dict, bucket_id: str) -> set[str]:
    """Capabilities taught by microtopics owned by this bucket, excluding prerequisites."""
    return {
        row.get("primary_capability_ref")
        for row in records.values()
        if row.get("_collection") == "microtopics" and row.get("bucket_id") == bucket_id
        and row.get("primary_capability_ref")
    }


def bucket_questions(records: dict, bucket_id: str) -> list[dict]:
    """Questions whose primary capability is taught by this bucket itself."""
    owned = bucket_capabilities(records, bucket_id)
    return sorted(
        [row for row in records.values()
         if row.get("_collection") == "questions"
         and row.get("primary_capability_ref") in owned],
        key=lambda row: row["id"],
    )


def questions_for_core(records: dict, bucket_id: str, core: str) -> list[dict]:
    return [
        row for row in bucket_questions(records, bucket_id)
        if any(exposure.get("core") == core for exposure in row.get("exposure", []))
    ]


def coverage(records: dict, bucket_id: str) -> dict:
    questions = bucket_questions(records, bucket_id)
    return {
        "bucket_id": bucket_id,
        "owned_capabilities": sorted(bucket_capabilities(records, bucket_id)),
        "questions": [row["id"] for row in questions],
        "CORE2A": [row["id"] for row in questions_for_core(records, bucket_id, "CORE2A")],
        "CORE2B": [row["id"] for row in questions_for_core(records, bucket_id, "CORE2B")],
    }
