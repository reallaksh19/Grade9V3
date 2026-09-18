"""Maturity utilities for the library lifecycle.

Upward promotion is no longer performed here. REVIEWED/CURATED are digest-bound authority
claims and must go through Shared/tools/review_authority.py, which pins authoring/review
receipts to the exact record digest. This module retains dependency-maturity auditing and
demotion support only.

Demotion needs no evidence. Withdrawing a claim is always permitted.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import require
from Shared.library.resolve import build_index, prerequisite_edges, references

STAGES = ("CANDIDATE", "REVIEWED", "CURATED")
RANK = {stage: position for position, stage in enumerate(STAGES)}
EVIDENCE_REQUIRED = {
    "REVIEWED": ("reviewer", "reviewed_on", "scope", "originals_inspected"),
    "CURATED": ("accepted_by", "accepted_on", "scope"),
}


def check_evidence(target_stage: str, evidence: dict, author: str | None) -> None:
    required = EVIDENCE_REQUIRED[target_stage]
    missing = [field for field in required if not str(evidence.get(field, "")).strip()]
    require(not missing, "PROMOTION_EVIDENCE_INCOMPLETE", f"{target_stage} needs {missing}")
    if target_stage == "REVIEWED":
        require(evidence.get("originals_inspected") is True,
                "REVIEW_DID_NOT_INSPECT_ORIGINALS",
                "a review that did not look at the original evidence is not a review")
        if author is not None:
            require(evidence["reviewer"] != author, "SELF_REVIEW_NOT_INDEPENDENT",
                    f"{evidence['reviewer']} authored this record")


def promote(record: dict, target_stage: str, evidence: dict) -> dict:
    """Compatibility surface: direct upward promotion is intentionally disabled."""
    require(target_stage in RANK, "UNKNOWN_LIFECYCLE_STAGE", target_stage)
    current = record.get("status", "CANDIDATE")
    require(current in RANK, "UNKNOWN_LIFECYCLE_STAGE", str(current))
    if RANK[target_stage] < RANK[current]:
        return {**record, "status": target_stage}
    if target_stage == current:
        return dict(record)
    require(False, "DIGEST_BOUND_REVIEW_AUTHORITY_REQUIRED",
            "upward promotion must use Shared/tools/review_authority.py")
    return dict(record)


def maturity_violations(records: dict) -> list[dict]:
    """Records claiming more maturity than something they depend on."""
    edges = prerequisite_edges(records)
    violations = []
    for rid, record in records.items():
        stage = record.get("status", "CANDIDATE")
        if stage not in RANK:
            continue
        dependencies = set(edges.get(rid, []))
        dependencies.update(target for _, target in references(record) if target in records)
        for target in sorted(dependencies):
            if target == rid:
                continue
            below = records[target].get("status", "CANDIDATE")
            if below in RANK and RANK[below] < RANK[stage]:
                violations.append({"record": rid, "status": stage,
                                   "depends_on": target, "dependency_status": below})
    return violations


def audit(packages: list[dict]) -> dict:
    records = build_index(packages)
    violations = maturity_violations(records)
    counts: dict[str, int] = {}
    for record in records.values():
        counts[record.get("status", "CANDIDATE")] = counts.get(record.get("status", "CANDIDATE"), 0) + 1
    return {"record_count": len(records), "by_stage": dict(sorted(counts.items())),
            "maturity_violations": violations,
            "monotone": not violations,
            "note": "Stage reflects recorded evidence only. CURATED means a review and an "
                    "acceptance were recorded, not that the teaching is known to work."}


def main() -> int:
    import argparse

    from Shared.contracts import load

    parser = argparse.ArgumentParser(description="Audit library promotion state")
    parser.add_argument("packages", nargs="+", type=Path)
    args = parser.parse_args()
    report = audit([load(path) for path in args.packages])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["monotone"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
