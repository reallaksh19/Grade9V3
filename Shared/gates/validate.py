"""Validate a technical gate registry against the schema and its subject contract.

Structure comes from gate.schema.json. Meaning comes from the subject contract, so
the rules enforced here stay subject-neutral while the values they check are the
subject's own: which representation kinds exist, which fields a symbol must carry,
which grades and tiers the subject covers.

Curriculum authority fails closed. A gate may *claim* a board prescribes its content
only when an exact binding exists in the subject's binding registry, matching board,
grade, chapter and the exact gate set. Absent that, the claim is reported as
HELD_INSUFFICIENT_AUTHORITY rather than accepted -- the posture adapted from the
curriculum-scope binding registry in reallaksh19/Common PR #350.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):  # invoked directly as a script
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import load, require, validate_dag

SCHEMA = Path(__file__).resolve().parent / "gate.schema.json"


def _schema_validate(registry: dict) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:  # structural checks below still run
        return
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        require(False, "GATE_SCHEMA_VIOLATION", f"{list(first.path)}: {first.message}")


def validate(registry: dict, adapter, bindings: dict | None = None) -> dict:
    """Return a report; raise ContractError on the first violation."""
    _schema_validate(registry)
    require(registry["subject"] == adapter.subject, "GATE_REGISTRY_WRONG_SUBJECT")
    require(registry["maturity"] == "ENGINEERING", "GATE_MATURITY_CLAIM_FORBIDDEN")

    gates = registry["gates"]
    index = {g["gate_id"]: g for g in gates}
    require(len(index) == len(gates), "GATE_DUPLICATE_ID")

    contract = adapter.contract
    declared_kinds = {k["id"] for k in contract.get("representation_kinds", [])}
    required_symbol_fields = set(contract.get("required_symbol_fields", []))
    allowed_grades = set(contract.get("curriculum", {}).get("grades", []))
    allowed_tiers = set(contract.get("curriculum", {}).get("tiers", []))

    asset_owner: dict[str, str] = {}
    for gate in gates:
        gid = gate["gate_id"]
        _unique_assets(gate, gid, asset_owner)

        grade = gate["curriculum"]["grade"]
        require(grade in allowed_grades, "GATE_GRADE_OUTSIDE_SUBJECT_SCOPE", f"{gid}: grade {grade}")
        require(gate["tier"] in allowed_tiers, "GATE_TIER_UNDECLARED", f"{gid}: {gate['tier']}")

        for rep in gate["representations"]:
            require(rep["kind"] in declared_kinds, "REPRESENTATION_KIND_UNDECLARED",
                    f"{gid}:{rep['representation_id']} uses {rep['kind']}")

        concept_ids = {c["concept_id"] for c in gate["canonical_concepts"]}
        relation_ids = {r["relation_id"] for r in gate["relations"]}
        for relation in gate["relations"]:
            seen = set()
            for symbol in relation["symbols"]:
                missing = required_symbol_fields - set(symbol)
                require(not missing, "SYMBOL_FIELD_MISSING",
                        f"{gid}:{relation['relation_id']}:{symbol.get('symbol')} missing {sorted(missing)}")
                require(symbol["symbol"] not in seen, "SYMBOL_DUPLICATE",
                        f"{gid}:{relation['relation_id']}:{symbol['symbol']}")
                seen.add(symbol["symbol"])

        for rep in gate["representations"]:
            unknown = set(rep.get("relation_bindings", [])) - relation_ids
            require(not unknown, "REPRESENTATION_RELATION_UNKNOWN", f"{gid}: {sorted(unknown)}")
            unknown = set(rep.get("concept_bindings", [])) - concept_ids
            require(not unknown, "REPRESENTATION_CONCEPT_UNKNOWN", f"{gid}: {sorted(unknown)}")

        representation_ids = {r["representation_id"] for r in gate["representations"]}
        for family in gate["problem_families"]:
            wanted = family.get("required_representation")
            require(wanted is None or wanted in representation_ids,
                    "PROBLEM_FAMILY_REPRESENTATION_UNKNOWN", f"{gid}:{family['family_id']}")

        _reasoning_sequence(gate, gid)

        require(gate["difficulty"]["maturity"] == "ENGINEERING", "GATE_DIFFICULTY_CLAIM_FORBIDDEN", gid)
        if gate["scope_state"] == "HELD":
            require(str(gate.get("held_reason", "")).strip(), "HELD_GATE_NEEDS_REASON", gid)

        for external in gate.get("external_prerequisites", []):
            require(external["provider_subject"] != adapter.subject,
                    "EXTERNAL_PREREQUISITE_IS_OWN_SUBJECT", f"{gid}:{external['capability_id']}")
            require(external["acceptance_status"] == "PROVIDER_REVIEW_REQUIRED",
                    "PROVIDER_ACCEPTANCE_NOT_SELF_GRANTABLE",
                    f"{gid}:{external['capability_id']} -- only the providing subject may accept it")

    for gate in gates:
        unknown = set(gate["prerequisites"]) - set(index)
        require(not unknown, "GATE_PREREQUISITE_UNKNOWN", f"{gate['gate_id']}: {sorted(unknown)}")
    validate_dag(gates, "gate_id", "prerequisites")

    scope = curriculum_report(registry, bindings or {"bindings": []})
    return {"status": "PASS", "registry_id": registry["registry_id"], "subject": registry["subject"],
            "gate_count": len(gates), "active": sorted(g["gate_id"] for g in gates if g["scope_state"] == "ACTIVE"),
            "held": sorted(g["gate_id"] for g in gates if g["scope_state"] == "HELD"),
            "curriculum_scope": scope,
            "release_authority": "NOT_GRANTED_BY_GATE_VALIDATION"}


def _unique_assets(gate: dict, gid: str, owner: dict[str, str]) -> None:
    """Canonical asset identifiers are globally unique across the registry."""
    assets = [c["concept_id"] for c in gate["canonical_concepts"]]
    assets += [r["relation_id"] for r in gate["relations"]]
    assets += [r["representation_id"] for r in gate["representations"]]
    assets += [m["misconception_id"] for m in gate["misconceptions"]]
    for asset in assets:
        require(asset not in owner, "GATE_DUPLICATE_ASSET_ID",
                f"{asset} appears in {owner.get(asset)} and {gid}")
        owner[asset] = gid


def _reasoning_sequence(gate: dict, gid: str) -> None:
    steps = sorted(gate["reasoning_sequence"], key=lambda s: s["sequence"])
    require([s["sequence"] for s in steps] == list(range(1, len(steps) + 1)),
            "REASONING_SEQUENCE_NOT_CONTIGUOUS", gid)
    position = {s["step_id"]: s["sequence"] for s in steps}
    require(len(position) == len(steps), "REASONING_STEP_DUPLICATE", gid)
    for step in steps:
        for dependency in step.get("depends_on", []):
            require(dependency in position, "REASONING_DEPENDENCY_UNKNOWN", f"{gid}:{step['step_id']}")
            require(position[dependency] < step["sequence"], "REASONING_DEPENDENCY_NOT_EARLIER",
                    f"{gid}:{step['step_id']} depends on {dependency}")


def curriculum_report(registry: dict, bindings: dict) -> dict:
    """Which prescribed-scope claims are actually authorised by an exact binding."""
    exact = {(b["board"], b["grade"], b["chapter"], tuple(sorted(b["gate_ids"])))
             for b in bindings.get("bindings", [])}
    authorised, held, extensions = [], [], []
    by_chapter: dict[tuple, list[str]] = {}
    for gate in registry["gates"]:
        curriculum = gate["curriculum"]
        key = (curriculum["board"], curriculum["grade"], curriculum["chapter"])
        by_chapter.setdefault(key, []).append(gate["gate_id"])
    for gate in registry["gates"]:
        curriculum = gate["curriculum"]
        gid = gate["gate_id"]
        if curriculum["scope_class"] == "OWNER_EXTENSION":
            extensions.append(gid)
            continue
        key = (curriculum["board"], curriculum["grade"], curriculum["chapter"])
        if (*key, tuple(sorted(by_chapter[key]))) in exact:
            authorised.append(gid)
        else:
            held.append(gid)
    return {"authorised_prescribed": sorted(authorised),
            "held_insufficient_authority": sorted(held),
            "owner_extension": sorted(extensions),
            "rule": "A PRESCRIBED claim needs an exact board/grade/chapter/gate-set binding; "
                    "otherwise it is HELD_INSUFFICIENT_AUTHORITY, never assumed."}


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Validate a technical gate registry")
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--bindings", type=Path)
    parser.add_argument("--subject-root", type=Path, required=True,
                        help="directory of the subject whose adapter should validate this registry")
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    module = __import__(f"{args.subject_root.name}.adapter", fromlist=["load"])
    report = validate(load(args.registry), module.load(),
                      load(args.bindings) if args.bindings else None)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
