#!/usr/bin/env python3
"""A library may not invent a way of depicting its subject.

The same authority order as relations, applied to figures. The subject contract says
which representation kinds this subject has, and with what status; the library teaches
through them. It does not get to add one.

Nothing compared the two layers, and they had drifted. Three Physics representations
declare kind `VECTOR_SUBTRACTION`, which that subject's contract has never heard of --
it declares VECTOR, GRAPH, FREE_BODY_DIAGRAM, RAY_DIAGRAM and CIRCUIT_SCHEMATIC. The
drift was invisible because a kind is only ever looked up when a scene instance is
rendered, and these three hold none. An author who wrote one would have got
FIGURE_FAMILY_UNSUPPORTED at publish time, after the figure was drawn -- the last
possible moment, and by then the work is done.

The second half is the bridge. Core1A requires the same idea carried across picture,
words and symbols "with the correspondence made explicit in both directions", and says
plainly that "a figure that sits beside the working without being bound to it is
decoration". R1 gave that a field. This is what makes it a claim rather than prose: a
correspondence names an element the figure must contain and a symbol a bound relation
declares, so a bridge to a part that is not drawn, or to a symbol that is not in the
mathematics, is refused.

Reports rather than decides. Which kinds a subject should gain is an owner's question,
and a gate that answered it by editing the contract would be inventing the subject.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import load
from Shared.library.resolve import build_index

BUILT = "IMPLEMENTED"


def declared_kinds(subject_root: Path) -> dict[str, str]:
    """What the subject says it can depict, and how far each one is built."""
    contract = load(subject_root / "adapter/CoreContracts.json")
    return {entry["id"]: entry.get("status") for entry in contract.get("representation_kinds", [])}


def relation_symbols(records: dict, representation: dict) -> set[str]:
    """Every symbol the relations this figure depicts actually declare.

    Drawn from the bound relations rather than from the figure, because the symbols are
    the mathematics' and a figure that labels one the relation does not use is labelling
    something else.
    """
    found = set()
    for ref in representation.get("relation_refs", []):
        relation = records.get(ref, {})
        for symbol in relation.get("symbols", []):
            if isinstance(symbol, dict) and symbol.get("symbol"):
                found.add(str(symbol["symbol"]))
    return found


def findings(records: dict, kinds: dict[str, str]) -> list[dict]:
    """Every representation claim this subject's contract does not back."""
    found: list[dict] = []

    def fail(point: str, record: str, detail: str):
        found.append({"point": point, "record": record, "detail": detail})

    for rid, record in sorted(records.items()):
        if record.get("_collection") != "representations":
            continue
        kind = record.get("kind")
        if kind not in kinds:
            fail("REPRESENTATION_KIND_UNDECLARED", rid,
                 f'depicts by {kind!r}, which this subject does not declare; it declares '
                 f'{", ".join(sorted(kinds)) or "nothing"}')
        elif record.get("scene_instances") and kinds[kind] != BUILT:
            # A scene instance is a figure someone drew. Carrying one for a kind the
            # subject has not built is work that cannot publish, and saying so here is
            # cheaper than saying so at the end of a publish run.
            fail("SCENE_FOR_UNBUILT_KIND", rid,
                 f'holds {len(record["scene_instances"])} scene instance(s) of {kind}, '
                 f"which the contract calls {kinds[kind]} rather than {BUILT}")

        elements = set(record.get("required_elements", []))
        symbols = relation_symbols(records, record)
        bridges = record.get("correspondence", [])
        if symbols and not bridges:
            # The rule only bites where there is mathematics to bridge to. A figure
            # bound to no relation has no symbols to correspond with, and demanding a
            # bridge there would be demanding one be invented.
            fail("CORRESPONDENCE_ABSENT", rid,
                 "depicts relations that declare symbols and binds none of its parts to "
                 "any of them, which is the figure beside the working that the role "
                 "specifications call decoration")
        for position, bridge in enumerate(bridges, 1):
            where = f"{rid}.correspondence[{position}]"
            if bridge.get("element") not in elements:
                fail("CORRESPONDENCE_ELEMENT_UNKNOWN", where,
                     f'bridges from {bridge.get("element")!r}, which is not one of the '
                     "elements this figure is required to contain")
            if symbols and bridge.get("symbol") not in symbols:
                fail("CORRESPONDENCE_SYMBOL_UNKNOWN", where,
                     f'bridges to {bridge.get("symbol")!r}, which none of the relations '
                     f'this figure depicts declares; they declare {", ".join(sorted(symbols))}')
    return found


def audit(subject_root: Path) -> dict:
    kinds = declared_kinds(subject_root)
    packages = [load(p) for p in sorted((subject_root / "library").glob("*.json"))]
    if not packages:
        return {"subject": subject_root.name, "declared_kinds": kinds,
                "representations": 0, "findings": [], "passed": True}
    records = build_index(packages)
    found = findings(records, kinds)
    return {"subject": subject_root.name, "declared_kinds": kinds,
            "representations": sum(1 for r in records.values()
                                   if r.get("_collection") == "representations"),
            "findings": found, "passed": not found}


def main() -> int:
    import argparse
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit non-zero on an unbacked claim (off while the backlog is open)")
    args = parser.parse_args()
    rows = [audit(p.parent.parent) for p in sorted(repo.glob("*/adapter/CoreContracts.json"))]
    report = {"subjects": rows, "unbacked": sum(len(r["findings"]) for r in rows),
              "passed": all(r["passed"] for r in rows)}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
