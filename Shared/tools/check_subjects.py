#!/usr/bin/env python3
"""Run every per-subject check against every subject actually present.

Naming a subject here would let a second one arrive with an invalid gate registry or
a hollow library and still go green -- which is what CI did until Mathematics landed.
Discovery therefore lives in this module, where a test can assert it finds every
subject, rather than in a workflow file where nothing protects it.

A subject is whatever declares a contract. Gate registries and library packages are
found under it by position, not by name, so a new subject is covered the day its
directory appears.
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

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.gates.validate import curriculum_report, validate as validate_gates  # noqa: E402
from Shared.library.authority import audit as authority_audit  # noqa: E402
from Shared.library.intake import check as intake_check  # noqa: E402
from Shared.library.promote import audit as promotion_audit  # noqa: E402
from Shared.library.resolve import validate_library  # noqa: E402

LEARNER_PRODUCTS = {"CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B"}
BINDINGS = "gates/curriculum-bindings.v1.json"


def subjects(repo: Path = REPO) -> list[Path]:
    """Every subject directory, identified by the contract it declares."""
    return sorted(p.parent.parent for p in repo.glob("*/adapter/CoreContracts.json"))


def check_contract(subject: Path) -> list[str]:
    contract = load(subject / "adapter/CoreContracts.json")
    findings = []
    declared = set(contract.get("learner_products", {}))
    if declared != LEARNER_PRODUCTS:
        findings.append(f"learner_products {sorted(declared)} != {sorted(LEARNER_PRODUCTS)}")
    for entry in contract.get("validator_catalogue", []):
        if "comparison" not in entry.get("result", {}):
            findings.append(f"validator {entry.get('id')} declares no result comparison")
        if not str(entry.get("does_not_prove", "")).strip():
            findings.append(f"validator {entry.get('id')} declares no does_not_prove limit")
    return findings


def adapter_for(subject: Path):
    """This subject's adapter, or None where the subject is still contract-only.

    A declared contract with no adapter behind it is a real and reportable state --
    a subject can be planned before it is built -- so it is named in the report
    rather than crashing the sweep or being quietly skipped.
    """
    module = importlib.import_module(f"{subject.name}.adapter")
    return module.load() if hasattr(module, "load") else None


def check_gates(subject: Path) -> tuple[int, list[str]]:
    bindings_path = subject / BINDINGS
    bindings = load(bindings_path) if bindings_path.is_file() else {"bindings": []}
    adapter = adapter_for(subject)
    if adapter is None:
        return 0, []
    checked, findings = 0, []
    for registry_path in sorted((subject / "gates").glob("*.v1.json")):
        if registry_path == bindings_path:
            continue
        registry = load(registry_path)
        try:
            validate_gates(registry, adapter, bindings)
            curriculum_report(registry, bindings)
            checked += 1
        except ContractError as error:
            findings.append(f"{registry_path.name}: {error.code} {error.detail}".strip())
    return checked, findings


def check_library(subject: Path) -> tuple[int, list[str]]:
    paths = sorted((subject / "library").glob("*.json"))
    if not paths:
        return 0, []
    packages = [load(p) for p in paths]
    findings = []
    for package, path in zip(packages, paths):
        report = intake_check(package)
        findings += [f"{path.name}: {f['point']}: {f['detail']}" for f in report["findings"]]
    # Subject truth is the gate's. A library copy that disagrees with its owner is
    # two authorities for one claim, so it is checked here rather than at publish time.
    for row in authority_audit(subject)["packages"]:
        findings += [f"{row['package']}: {f['point']}: {f['record']}: {f['detail']}"
                     for f in row["findings"]]
    for stage in (validate_library, promotion_audit):
        try:
            stage(packages)
        except ContractError as error:
            findings.append(f"{stage.__name__}: {error.code} {error.detail}".strip())
    return len(packages), findings


def run(repo: Path = REPO) -> dict:
    found = subjects(repo)
    rows = []
    for subject in found:
        contract_findings = check_contract(subject)
        gate_count, gate_findings = check_gates(subject)
        package_count, library_findings = check_library(subject)
        rows.append({"subject": subject.name,
                     "state": "CONTRACT_ONLY" if adapter_for(subject) is None else "IMPLEMENTED",
                     "gate_registries": gate_count, "library_packages": package_count,
                     "findings": contract_findings + gate_findings + library_findings})
    return {"subjects_checked": len(found), "subjects": rows,
            "passed": bool(found) and not any(r["findings"] for r in rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()
    report = run()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["subjects_checked"]:
        print("no subjects found", file=sys.stderr)
        return 1
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
