#!/usr/bin/env python3
"""A published page must say which library records it came from, or say that it came from none.

Found by stress-testing one subject rather than by reading code. Every gate in this
repository governs the library -- intake, substance, authority, depiction, spec delivery,
the vocabulary ceiling. The one artifact a learner can actually open was never checked
against any of them, and the reason is simpler than drift: it was never compiled from the
library at all. Its plan carries hand-written prose in its own id space and names no
record. Adding, changing or deleting any library record cannot move it, and nothing said so.

`republish.py` verifies the frozen inputs against the published bytes. That is a real
check and it is not this one: it can only ever prove the page still matches the plan it
came from. Nothing compared the plan to the library the plan was supposed to be a
projection of.

So the state is made expressible rather than forbidden, because a hand-authored run is a
legitimate thing to have -- pretending otherwise is how a true fact stops being written
down. A run declares its basis beside its inputs, outside the digest-verified publication
basis so that declaring it cannot disturb what republish checks:

  basis: LIBRARY                       and names the records it projects
  basis: AUTHORED_OUTSIDE_THE_LIBRARY  and says why, which puts it on the board

Silence is the one answer that is not available.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402

DECLARATION = "provenance.json"
LIBRARY = "LIBRARY"
OUTSIDE = "AUTHORED_OUTSIDE_THE_LIBRARY"
# Every collection a package declares ids in. It omitted resources, so a run that
# correctly declared the sources it compiled from was told the library does not hold them.
RECORD_KEYS = ("buckets", "microtopics", "capabilities", "relations", "representations",
               "question_families", "questions", "data", "resources", "teaching_routes",
               "practice_profiles", "evidence", "known_issues")


def library_records(subject: str, repo: Path = REPO) -> dict[str, str]:
    """Every id the subject's library declares, mapped to the kind that declares it."""
    found = {}
    for path in sorted((repo / subject / "library").glob("*.json")):
        if path.name.endswith(".schema.json"):
            continue
        package = load(path)
        for key in RECORD_KEYS:
            for record in package.get(key, []):
                if isinstance(record, dict) and record.get("id"):
                    found[record["id"]] = key
    return found


def owning_bucket(subject: str, repo: Path = REPO) -> dict[str, str]:
    """Which bucket each microtopic belongs to. A run publishes one bucket, so only that
    bucket's teaching can be missing from it."""
    owner = {}
    for path in sorted((repo / subject / "library").glob("*.json")):
        if path.name.endswith(".schema.json"):
            continue
        for row in load(path).get("microtopics", []):
            if row.get("id"):
                owner[row["id"]] = row.get("bucket_id")
    return owner


def mentions(rid: str, text: str) -> bool:
    """Whether an id appears as a whole identifier rather than inside a longer one.

    A plain substring scan counted CAP-RIGHT-TRIANGLE as present wherever
    CAP-RIGHT-TRIANGLE-BRIDGE was written, which is a different capability. Identifiers
    here are upper-case and hyphenated, so a hyphen is part of the token and not a
    boundary.
    """
    return bool(re.search(rf"(?<![A-Z0-9-]){re.escape(rid)}(?![A-Z0-9-])", text))


def runs(repo: Path = REPO) -> list[Path]:
    """Every committed run, found by its publication's manifest rather than by name."""
    return sorted(p.parent.parent for p in repo.glob("*/content/*/publication/manifest.json"))


def findings(run: Path, repo: Path = REPO) -> tuple[list[dict], dict]:
    found: list[dict] = []

    def fail(point: str, detail: str):
        found.append({"point": point, "where": str(run.relative_to(repo)), "detail": detail})

    subject = run.relative_to(repo).parts[0]
    records = library_records(subject, repo)
    declaration = run / DECLARATION
    if not declaration.exists():
        fail("PUBLICATION_PROVENANCE_UNDECLARED",
             f"no {DECLARATION}: this run does not say whether a learner is reading the "
             f"library or something authored beside it")
        return found, {"basis": None, "declared": 0, "in_plan": 0}

    declared = load(declaration)
    basis = declared.get("basis")
    named = list(declared.get("records") or [])
    # What the compiler recorded it read, where it exists. Scanning the plan's text for
    # ids cannot be made correct: a loose match counted CAP-RIGHT-TRIANGLE inside
    # CAP-RIGHT-TRIANGLE-BRIDGE, and a whole-token match then missed MIC-MEASURED-FROM
    # inside the block id CORE1A-MIC-MEASURED-FROM-T. The scan survives only for runs
    # authored before the compiler existed, which have no list to read.
    compiled = run / "inputs/library_records.json"
    if compiled.exists():
        in_plan = sorted(rid for rid in load(compiled) if rid in records)
    else:
        plan = run / "inputs/plan.json"
        text = plan.read_text(encoding="utf-8") if plan.exists() else ""
        in_plan = sorted(rid for rid in records if mentions(rid, text))

    if basis == LIBRARY:
        for rid in named:
            if rid not in records:
                fail("PUBLICATION_RECORD_UNKNOWN",
                     f"declares {rid}, which {subject}'s library does not hold")
        if not in_plan:
            fail("PUBLICATION_CLAIMS_LIBRARY_BASIS_AND_NAMES_NOTHING",
                 "the plan references no record this library declares, so the claim is "
                 "not one anything can check")
        # Staleness, which is the reason this is worth running more than once: a rung
        # authored after the run was frozen is taught by the library and not by the page.
        #
        # Scoped to the buckets this run publishes. It compared against every microtopic
        # in the subject, so the first library-based run reported forty omissions for
        # teaching that belongs to eleven other subtopics -- which is not staleness, it is
        # a run being asked to publish the whole subject.
        owner = owning_bucket(subject, repo)
        published = {rid for rid in set(named) | set(in_plan)
                     if records.get(rid) == "buckets"}
        for rid in sorted(records):
            if (records[rid] == "microtopics" and owner.get(rid) in published
                    and rid not in named and rid not in in_plan):
                fail("PUBLICATION_OMITS_A_MICROTOPIC_THE_LIBRARY_TEACHES",
                     f"{rid} is taught by {owner[rid]}, which this run publishes, and "
                     f"does not appear in it")
    elif basis == OUTSIDE:
        if not str(declared.get("reason", "")).strip():
            fail("PUBLICATION_AUTHORED_OUTSIDE_WITHOUT_A_REASON",
                 "a run beside the library is allowed and an unexplained one is not")
    else:
        fail("PUBLICATION_BASIS_UNKNOWN",
             f'basis is {basis!r}; it is {LIBRARY} or {OUTSIDE}')
    return found, {"basis": basis, "declared": len(named), "in_plan": len(in_plan)}


def audit(repo: Path = REPO) -> dict:
    rows = []
    for run in runs(repo):
        found, measured = findings(run, repo)
        rows.append({"run": str(run.relative_to(repo)), **measured, "findings": found})
    blocking = [f for r in rows for f in r["findings"]
                if f["point"] != "PUBLICATION_OMITS_A_MICROTOPIC_THE_LIBRARY_TEACHES"]
    stale = [f for r in rows for f in r["findings"]
             if f["point"] == "PUBLICATION_OMITS_A_MICROTOPIC_THE_LIBRARY_TEACHES"]
    return {"runs": len(rows), "publications": rows,
            "authored_outside_the_library": sum(1 for r in rows if r["basis"] == OUTSIDE),
            "blocking": len(blocking), "stale": len(stale), "passed": not blocking}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit nonzero on an undeclared or unbacked basis; a stale "
                             "run is reported, because republishing it is owner work")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] or not args.enforce else 1


if __name__ == "__main__":
    raise SystemExit(main())
