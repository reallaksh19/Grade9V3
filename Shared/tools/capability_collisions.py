#!/usr/bin/env python3
"""One skill must have one id. Reports collisions; never resolves them.

The capability namespace has already forked per package. `relative-motion.v1.json`
declares `CAP-SIGNED-PAIR` and `CAP-RIGHT-TRIANGLE`; `vector-representation.v1.json`
declares `CAP-SIGNED-PAIR-BRIDGE` and `CAP-RIGHT-TRIANGLE-BRIDGE`. If those are one
skill each, then a learner's demonstrated capability cannot be matched across packages
-- which makes selecting an entry rung impossible even with perfect evidence, because the
evidence and the requirement are keyed differently.

Why this reports rather than merges: collapsing two ids rewrites every prerequisite
graph that names either, and the two `success_criterion` texts are the evidence for
whether they are the same skill at all. That is an owner decision. A gate that merged
them would be inventing the skill graph.

It also reports a second shape, found while building the authoring brief: a
`success_criterion` that asserts two things. `CAP-SIGNED-PAIR` reads "preserve east/north
signs *and* distinguish a point from a displacement" -- an arithmetic skill with a
conceptual claim riding inside it. The rider is taught by no microtopic, repaired by no
misconception and assessed by no check, and because the words are present it looks
covered. That is worse than absent, and the shape is mechanical.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load, normalise  # noqa: E402

# Suffixes a package adds when it redeclares a skill it did not want to depend on.
# Listed because they are naming habits rather than anything structural, and a habit
# this gate has not seen yet must be added here deliberately.
LOCALISING = ("-BRIDGE", "-LOCAL", "-PREREQ", "-EXT")
# A discrimination -- telling two things apart -- is a conceptual claim, and one riding
# inside a procedural criterion is the shape being hunted. Matching on "and" instead was
# the first attempt and it fired on 9 of 12 capabilities, 6 of them wrongly: "reverse,
# translate, add tail-to-head, and reconcile" is one composite procedure, not a rider.
# The same mistake shape as a word list, and caught the same way -- by measuring.
DISCRIMINATION = re.compile(r"\b(distinguish|confus\w+|tell \w+ apart|not (?:the same|its))\b",
                            re.IGNORECASE)


def capabilities(repo: Path = REPO) -> dict[str, list[dict]]:
    """Every capability declared anywhere, grouped by id, with where it came from."""
    found: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(repo.glob("*/library/*.json")):
        if path.name == "package.schema.json":
            continue
        package = load(path)
        for cap in package.get("capabilities", []):
            found[cap["id"]].append({**cap, "_package": str(path.relative_to(repo))})
    return dict(found)


def stem(capability_id: str) -> str:
    """The id with a localising suffix removed, for grouping candidates only."""
    for suffix in LOCALISING:
        if capability_id.endswith(suffix):
            return capability_id[: -len(suffix)]
    return capability_id


def claimed_by_microtopics(repo: Path = REPO) -> set[str]:
    """Capabilities some microtopic claims as the thing it teaches."""
    return {mic.get("primary_capability_ref")
            for path in sorted(repo.glob("*/library/*.json")) if path.name != "package.schema.json"
            for mic in load(path).get("microtopics", [])} - {None}


def findings(declared: dict[str, list[dict]], taught: set[str] | None = None) -> list[dict]:
    taught = claimed_by_microtopics() if taught is None else taught
    found: list[dict] = []

    def fail(point: str, subject: str, detail: str, **extra):
        found.append({"point": point, "capability": subject, "detail": detail, **extra})

    for cid, rows in sorted(declared.items()):
        if len(rows) > 1:
            fail("CAPABILITY_DECLARED_TWICE", cid,
                 f'declared in {", ".join(r["_package"] for r in rows)}; one skill, one record')

    by_stem: dict[str, list[str]] = defaultdict(list)
    for cid in declared:
        by_stem[stem(cid)].append(cid)
    for root, ids in sorted(by_stem.items()):
        if len(ids) < 2:
            continue
        # Both criteria are quoted, because they are the evidence for whether these are
        # the same skill, and a merge proposed without them is not reviewable.
        fail("CAPABILITY_NAMESPACE_FORKED", root,
             "two ids share a stem, so demonstrated evidence for one does not satisfy a "
             "requirement naming the other",
             ids=sorted(ids),
             success_criteria={cid: declared[cid][0].get("success_criterion", "")
                               for cid in sorted(ids)},
             criteria_agree=len({normalise(declared[cid][0].get("success_criterion", ""))
                                 for cid in ids}) == 1)

    for cid, rows in sorted(declared.items()):
        criterion = rows[0].get("success_criterion", "")
        if not DISCRIMINATION.search(criterion):
            continue
        # Legitimate where a microtopic exists to teach that discrimination: then it is
        # the skill, not a rider. A discrimination nothing claims is taught by no
        # microtopic, repaired by no misconception and assessed by no check -- and looks
        # covered because the words are present, which is worse than absent.
        if cid in taught:
            continue
        fail("DISCRIMINATION_TAUGHT_BY_NOTHING", cid,
             "the criterion asks the learner to tell two things apart, and no microtopic "
             "claims this capability, so the discrimination is a conceptual rung riding "
             "inside a prerequisite that was delegated",
             success_criterion=criterion, package=rows[0]["_package"])
    return found


def audit(repo: Path = REPO) -> dict:
    declared = capabilities(repo)
    found = findings(declared)
    return {"capabilities": len(declared), "packages_scanned": len(
        {r["_package"] for rows in declared.values() for r in rows}),
        "findings": found, "passed": not found}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit non-zero on a collision (off until the owner has "
                             "decided each one; this gate never decides)")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
