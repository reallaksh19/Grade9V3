"""Promotion lifecycle: CANDIDATE -> REVIEWED -> CURATED, with evidence.

Maturity is a claim about evidence, so it is granted by evidence, never by editing a
field. Two rules do the real work:

  * No stage may be skipped, and each promotion names the evidence that justifies it.
    Review evidence must come from someone other than the author -- an author cannot
    review their own work into a higher stage.

  * Maturity is monotone down the dependency graph. A record may not be more mature
    than anything it depends on. A CURATED microtopic resting on a CANDIDATE
    capability is exactly the kind of quiet unsoundness this library exists to make
    visible: the lesson looks accepted, its foundation was never reviewed.

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
    require(target_stage in RANK, "UNKNOWN_LIFECYCLE_STAGE", target_stage)
    current = record.get("status", "CANDIDATE")
    require(current in RANK, "UNKNOWN_LIFECYCLE_STAGE", str(current))
    if RANK[target_stage] < RANK[current]:
        return {**record, "status": target_stage}          # demotion: always allowed
    require(RANK[target_stage] == RANK[current] + 1, "PROMOTION_SKIPPED_A_STAGE",
            f"{current} -> {target_stage}")
    check_evidence(target_stage, evidence, record.get("authored_by"))
    history = list(record.get("lifecycle_history", []))
    history.append({"from": current, "to": target_stage, "evidence": evidence})
    return {**record, "status": target_stage, "lifecycle_history": history}


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
