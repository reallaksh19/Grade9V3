#!/usr/bin/env python3
"""A contract may not claim a capability this repository cannot perform.

Subject contracts are the top of the authority chain: everything downstream trusts
them to say what the subject can do. Three kinds of claim live there, and all three
had drifted from what the code can actually do:

  learner products      all three contracts declare six; the compiler builds four,
                        and CORE1 and CORE2 have never been produced by anything here
  validators            one subject marks three families IMPLEMENTED with no
                        validator module behind them at all
  representation kinds  eleven declared across the subjects, three with a renderer

Two of the three already carry a `status` field, so the mechanism for saying "declared
but not built" exists and was simply wrong and unchecked. Learner products have no
such field, which is why that claim had nowhere to be honest.

This is the same rule the library layer enforces on teaching records, applied one
level up: a claim must be backed, or must say that it is not. It reports rather than
decides -- which capabilities should be built is an owner's question, and a gate that
answered it by deleting the claim would be destroying the record of the intent.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402
from Shared.library.compile_inputs import COMPOSABLE  # noqa: E402

BUILT = "IMPLEMENTED"


def _module_names(subject: str, module: str, attribute: str) -> set[str] | None:
    """What a subject's adapter actually registers, or None when it has no such module."""
    try:
        found = getattr(importlib.import_module(f"{subject}.adapter.{module}"), attribute, None)
    except ModuleNotFoundError:
        return None
    return set(found) if found is not None else set()


def audit_subject(subject_root: Path) -> dict:
    subject = subject_root.name
    contract = load(subject_root / "adapter/CoreContracts.json")
    findings: list[dict] = []

    def fail(point: str, capability: str, detail: str):
        findings.append({"point": point, "capability": capability, "detail": detail})

    # A product says whether this repository compiles it. Claiming COMPILED with no
    # compiler path is the same defect as a validator marked IMPLEMENTED with no code;
    # saying NOT_COMPILED is honest, and must carry the reason rather than a bare word.
    for product, declared in sorted(contract.get("learner_products", {}).items()):
        if not isinstance(declared, dict):
            fail("PRODUCT_STATUS_ABSENT", product,
                 "declares no production status, so whether anything builds it cannot be said")
            continue
        compiled, buildable = declared.get("production") == "COMPILED", product in COMPOSABLE
        if compiled and not buildable:
            fail("CLAIMED_WITHOUT_CODE", product,
                 "claims to be compiled here, but no compiler path can build it")
        elif not compiled and buildable:
            fail("BUILT_BUT_NOT_CLAIMED", product,
                 f'the compiler builds it while the contract calls it '
                 f'{declared.get("production")}')
        elif not compiled and not str(declared.get("reason", "")).strip():
            fail("PRODUCT_NOT_COMPILED_WITHOUT_REASON", product,
                 "is not compiled here and says nothing about why, which is the silence "
                 "this field exists to prevent")

    for kind, registered, label in (
            ("validator_catalogue", _module_names(subject, "validator", "VALIDATORS"), "validator"),
            ("representation_kinds", _module_names(subject, "scenes", "SCENES"), "representation")):
        for entry in contract.get(kind, []):
            name, status = entry.get("id"), entry.get("status")
            if status != BUILT:
                continue
            if registered is None:
                fail("CLAIMED_WITHOUT_CODE", name,
                     f"marked {BUILT}, but this subject has no {label} module at all")
            elif name not in registered:
                fail("CLAIMED_WITHOUT_CODE", name,
                     f"marked {BUILT}, but the {label} module registers "
                     f"{sorted(registered) or 'nothing'}")
        for name in sorted(registered or ()):
            declared = {e.get("id"): e.get("status") for e in contract.get(kind, [])}
            if declared.get(name) not in (None, BUILT):
                fail("BUILT_BUT_NOT_CLAIMED", name,
                     f"the {label} module registers it while the contract calls it "
                     f"{declared[name]}")

    return {"subject": subject, "findings": findings, "passed": not findings}


def audit(repo: Path = REPO) -> dict:
    rows = [audit_subject(p.parent.parent)
            for p in sorted(repo.glob("*/adapter/CoreContracts.json"))]
    return {"subjects": rows, "claims_unbacked": sum(len(r["findings"]) for r in rows),
            "passed": bool(rows) and all(r["passed"] for r in rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit non-zero on an unbacked claim (off while the backlog is open)")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
