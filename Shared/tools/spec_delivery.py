#!/usr/bin/env python3
"""A role spec's requirement must reach the learner, not merely have somewhere to live.

R1 compared each role's `requires` block against the package schema and closed 68
findings. That comparison proves a requirement *can* be held. It says nothing about
whether anything holds it, and nothing about whether the compiler carries it into the
product -- so every gate in this repository went green over two products that do not
deliver what their own specs require:

  question.hints[]              never authored, and `_question_block` hardcodes `[]`,
                                so authoring it would not have helped
  question.answer.difficult_move never authored, and not carried either

Both are named in Core2's, Core2A's and Core2B's blocks. Both got schema homes in R1.
Neither reaches a page.

Three outcomes per requirement, because three different things go wrong and collapsing
them would hide which:

  UNAUTHORED      the library holds nothing at this path. Content work.
  NOT_DELIVERED   the library holds it and no compiled product carries it. Compiler work,
                  and the more dangerous of the two: the content exists, so every
                  authored-ness check would pass.
  UNDECIDABLE     held, but every value is too short to look for in the compiled output
                  without matching by accident. Reported as itself rather than guessed,
                  because a false DELIVERED is worse than an admitted gap.

Delivery is checked by looking for the authored value in the compiled product rather
than by mapping library paths onto block fields. A mapping would have to be updated
whenever the compiler changes shape, and would be updated by whoever changed it --
which is the arrangement this whole layer exists to avoid.

A role that compiles no product for a subject is reported once and its paths skipped.
The compiler already records why, as PRODUCT_UNSUPPORTED with a reason, and repeating
that per requirement would bury the findings that are real.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.library.compile_inputs import compile_bucket  # noqa: E402
from Shared.library.resolve import build_index  # noqa: E402
from Shared.tools.spec_conformance import (  # noqa: E402
    SCHEMA, SEGMENT, record_types, requirements, role_specs)

# Below this, a value can appear in compiled output by coincidence -- an id fragment, an
# enum, a single symbol. Searching for it would report DELIVERED for content nobody
# carried, which is the one outcome this tool must never produce.
DECIDABLE_LENGTH = 12


def values_at(record: object, segments: list) -> list[str]:
    """Every leaf value a path reaches in one record, flattening the arrays it crosses."""
    if not segments:
        return [str(record)] if isinstance(record, (str, int, float)) else []
    name, is_array = segments[0].group(1), bool(segments[0].group(2))
    if not isinstance(record, dict) or name not in record:
        return []
    value = record[name]
    if is_array:
        if not isinstance(value, list):
            return []
        return [found for item in value for found in values_at(item, segments[1:])]
    return values_at(value, segments[1:])


def authored(records: dict, path: str, roots: dict) -> list[str]:
    """Every value this subject's library holds at a required path."""
    segments = [SEGMENT.match(s) for s in path.split(".")]
    if not all(segments):
        return []
    collection = roots.get(segments[0].group(1))
    if collection is None:
        return []
    return [value for record in records.values()
            if record.get("_collection") == collection
            for value in values_at(record, segments[1:]) if str(value).strip()]


def compiled_products(subject: Path, records: dict) -> tuple[dict[str, str], list[str]]:
    """Each role's compiled output as one searchable blob, plus buckets that would not compile."""
    blobs: dict[str, list] = {}
    refused = []
    for bucket_id in sorted(rid for rid, r in records.items() if r["_collection"] == "buckets"):
        try:
            compiled = compile_bucket(records, bucket_id, topic_id=bucket_id.lower(),
                                      title=records[bucket_id]["title"], subject=subject.name,
                                      practice_control={"mode": "DESIGN_PREVIEW",
                                                        "purpose": "PRACTICE"})
        except ContractError as error:
            refused.append(f"{bucket_id}: {error.code} {error.detail}".strip())
            continue
        for product in compiled["plan"]["products"]:
            blobs.setdefault(product["core"], []).append(product)
    return ({core: json.dumps(rows, ensure_ascii=False) for core, rows in blobs.items()},
            refused)


def audit_subject(subject: Path, schema: dict) -> dict:
    packages = [load(p) for p in sorted((subject / "library").glob("*.json"))]
    if not packages:
        return {"subject": subject.name, "state": "NO_LIBRARY", "rows": [], "findings": []}
    records = build_index(packages)
    roots = record_types(schema)
    blobs, refused = compiled_products(subject, records)

    rows, findings = [], list(refused)
    for spec in role_specs():
        role = spec.stem
        if role not in blobs:
            rows.append({"role": role, "state": "NOT_COMPILED_HERE"})
            continue
        for row in requirements(spec) or []:
            held = authored(records, row["path"], roots)
            longest = max(held, key=len, default="")
            if not held:
                state = "UNAUTHORED"
            elif len(longest) < DECIDABLE_LENGTH:
                state = "UNDECIDABLE"
            elif any(value in blobs[role] for value in held):
                state = "DELIVERED"
            else:
                state = "NOT_DELIVERED"
            rows.append({"role": role, "path": row["path"], "state": state,
                         "phrase": row["phrase"], "held": len(held)})
            if state in ("UNAUTHORED", "NOT_DELIVERED"):
                findings.append(f'{role}: {row["path"]}: {state}: {row["phrase"]}')
    return {"subject": subject.name, "state": "CHECKED", "rows": rows, "findings": findings}


def audit(repo: Path = REPO) -> dict:
    schema = load(repo / SCHEMA)
    rows = [audit_subject(p.parent.parent, schema)
            for p in sorted(repo.glob("*/adapter/CoreContracts.json"))]
    counted: dict[str, int] = {}
    for subject in rows:
        for row in subject["rows"]:
            counted[row["state"]] = counted.get(row["state"], 0) + 1
    return {"subjects": rows, "by_state": counted,
            "undelivered": sum(len(s["findings"]) for s in rows),
            "passed": not any(s["findings"] for s in rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit non-zero on an undelivered requirement "
                             "(off while the backlog it measures is open)")
    parser.add_argument("--summary", action="store_true", help="counts only")
    args = parser.parse_args()
    report = audit()
    print(json.dumps({k: v for k, v in report.items() if k != "subjects"} if args.summary
                     else report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
