#!/usr/bin/env python3
"""Does authored teaching reach a product, or does it only sit in the library?

Found by publishing a bucket from the library for the first time. MIC-MEASURED-FROM --
the entry rung of relative motion, authored the day before with its capability, its
elicitation, its misconception and its exit oracle -- produced no block in any product.
Every gate passed: intake admitted it, the matrix bound it, the subject sweep was green,
the delivery gate was green. It was simply in no teaching route, and nothing said so.

A route is how a microtopic claims a product. The compiler asks each microtopic which
products claim it and emits nothing for one that no route names, so an unrouted rung is
authored, checked, counted -- and read by nobody.

Two states, and the difference matters:

  a bucket whose routes exist and omit it   an omission; the bucket plainly intends routing
  a bucket with no routes at all            not wired yet, which is visible at the bucket
                                            rather than hidden per microtopic

Reported rather than enforced. Four of the five found are content decisions that belong to
whoever authors those buckets -- three microtopics in a package that declares no routes,
and a non-assessment boundary note whose instructional treatment the benchmark records as
deliberately undecided. Enforcing before those are decided would force a routing claim
nobody has made.
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

UNROUTED = "MICROTOPIC_REACHES_NO_PRODUCT"
UNWIRED = "BUCKET_DECLARES_NO_TEACHING_ROUTE"


def findings(packages: list[dict]) -> list[dict]:
    claimed: dict[str, set] = {}
    routed_buckets: set = set()
    microtopics: dict[str, str] = {}
    bucket_of_route: dict[str, set] = {}
    for package in packages:
        for row in package.get("microtopics", []):
            if row.get("id"):
                microtopics[row["id"]] = row.get("bucket_id")
        for route in package.get("teaching_routes", []):
            for mid in route.get("microtopic_refs", []):
                claimed.setdefault(mid, set()).update(route.get("cores", []))
                bucket_of_route.setdefault(mid, set())
    for mid, bucket in microtopics.items():
        if mid in claimed:
            routed_buckets.add(bucket)

    found = []
    for mid in sorted(microtopics):
        if claimed.get(mid):
            continue
        bucket = microtopics[mid]
        if bucket in routed_buckets:
            found.append({"point": UNROUTED, "record": mid, "bucket": bucket,
                          "detail": f"{bucket} declares teaching routes and none names "
                                    f"{mid}, so it is authored and reaches no product"})
        else:
            found.append({"point": UNWIRED, "record": mid, "bucket": bucket,
                          "detail": f"{bucket} declares no teaching route at all, so "
                                    f"nothing it teaches reaches a teaching product"})
    return found


def audit(repo: Path = REPO) -> dict:
    rows = []
    for contract in sorted(repo.glob("*/adapter/CoreContracts.json")):
        subject = contract.parent.parent
        packages = [load(p) for p in sorted((subject / "library").glob("*.json"))
                    if not p.name.endswith(".schema.json")]
        if not packages:
            continue
        found = findings(packages)
        total = sum(len(p.get("microtopics", [])) for p in packages)
        rows.append({"subject": subject.name, "microtopics": total,
                     "reaching_no_product": len(found), "findings": found})
    return {"subjects": rows,
            "microtopics": sum(r["microtopics"] for r in rows),
            "reaching_no_product": sum(r["reaching_no_product"] for r in rows),
            "passed": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="accepted and ignored: this reports until the open routing "
                             "decisions are made, and says so rather than failing on them")
    parser.parse_args()
    print(json.dumps(audit(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
