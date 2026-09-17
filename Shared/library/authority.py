"""Subject truth belongs to the engineering gate. The library teaches it; it does not own it.

The two layers were authored independently and drifted into declaring the same physics
twice. `REL-RELATIVE-POSITION` exists in both under that one id, with two different
expressions and two different sets of validity conditions -- the gate requiring both
positions at the same instant, the library requiring a common time interval. A
publication compiled from the library was therefore governed by conditions no
engineering gate had authorised, which is the authority order running backwards.

A library relation may hold a copy of a gate relation so the compiler can reach it
without loading the registry. What it may not do is hold a *different* copy. So the
copy is bound by exact reference and checked:

  expression   must match the gate exactly. It is the mathematical content, and two
               spellings of it are two claims.
  conditions   may add, never drop. Narrowing the circumstances in which a relation
               is used is a teaching decision; widening them is a claim about the
               subject that only the gate can make.

What the library does own is untouched here: how a transition is taught, which
misconception is repaired and in what order, which representation bridges to which.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import load

GATE_OWNED = ("expression", "conditions")


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).replace("_", "")).strip().lower()


def gate_relations(subject_root: Path) -> dict[str, dict]:
    """Every relation the subject's gate registries declare, by relation id."""
    found: dict[str, dict] = {}
    bindings = subject_root / "gates/curriculum-bindings.v1.json"
    for path in sorted((subject_root / "gates").glob("*.v1.json")):
        if path == bindings:
            continue
        for gate in load(path).get("gates", []):
            for relation in gate.get("relations", []):
                found[relation["relation_id"]] = {**relation, "_gate": gate["gate_id"]}
    return found


def findings(package: dict, gates: dict[str, dict]) -> list[dict]:
    """Where the library's copy of subject truth disagrees with the gate that owns it."""
    if not gates:
        return []
    by_expression: dict[str, list[str]] = {}
    for relation_id, relation in gates.items():
        by_expression.setdefault(_normalise(relation.get("expression", "")), []).append(relation_id)

    found: list[dict] = []

    def fail(point: str, record: str, detail: str):
        found.append({"point": point, "record": record, "detail": detail})

    for relation in package.get("relations", []):
        record = relation["id"]
        reference = relation.get("gate_relation_ref")
        expression = _normalise(relation.get("expression", ""))
        if not reference:
            twin = by_expression.get(expression)
            if twin:
                fail("SUBJECT_TRUTH_REDECLARED", record,
                     f"declares the expression the gate already owns as {twin[0]} "
                     f"({gates[twin[0]]['_gate']}) without referencing it")
            else:
                fail("GATE_RELATION_BINDING_ABSENT", record,
                     "states subject truth with no engineering gate behind it")
            continue
        if reference not in gates:
            fail("GATE_RELATION_UNKNOWN", record,
                 f"binds to {reference}, which no gate registry for this subject declares")
            continue

        owner = gates[reference]
        if expression != _normalise(owner.get("expression", "")):
            fail("RELATION_EXPRESSION_DIVERGED", record,
                 f"{reference} ({owner['_gate']}) reads {owner.get('expression')!r}; "
                 f"this copy reads {relation.get('expression')!r}")
        held = {_normalise(c) for c in relation.get("conditions", [])}
        for condition in owner.get("conditions", []):
            if _normalise(condition) not in held:
                fail("VALIDITY_CONDITION_DROPPED", record,
                     f"{reference} ({owner['_gate']}) requires {condition!r}, which this copy omits")
    return found


def audit(subject_root: Path) -> dict:
    gates = gate_relations(subject_root)
    rows = []
    for path in sorted((subject_root / "library").glob("*.json")):
        rows.append({"package": path.name, "findings": findings(load(path), gates)})
    return {"subject": subject_root.name, "gate_relations": len(gates), "packages": rows,
            "passed": not any(r["findings"] for r in rows)}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("subject_root", nargs="+", type=Path)
    args = parser.parse_args()
    reports = [audit(root) for root in args.subject_root]
    print(json.dumps(reports, indent=2, ensure_ascii=False))
    return 0 if all(r["passed"] for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
