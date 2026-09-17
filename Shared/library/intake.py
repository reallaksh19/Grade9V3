"""Library intake: admit a package, or say exactly why it cannot be admitted.

The library stores teaching substance -- what a learner can already do, the exact
inference to be learned, why each step is valid, the plausible wrong path and its
repair, and an observable exit criterion. Storing that badly is worse than not
storing it, because a plausible-looking record invites an author to trust teaching
that was never actually worked out.

Intake therefore checks structure *and* substance. The six-point checklist is
adapted from the subtopic-intelligence intake gate in reallaksh19/Common PR #395;
the checks are re-implemented here against this repository's richer package schema.

A seventh point was added after running the first six against that track's own
packets: all of them passed while saying, on record after record, exactly the same
thing. Presence checks cannot see that, because "Governing relation." is a non-empty
inferential jump. Discriminability is a property of the corpus, not of a record, and
lives in substance.py.

Nothing here grants scientific or pedagogical acceptance. Intake admits a package
as a CANDIDATE; promotion beyond that requires review evidence (see promote.py).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import load, require
from Shared.library.substance import (
    findings as substance_findings, step_findings as substance_step_findings,
)

SCHEMA = Path(__file__).resolve().parent / "package.schema.json"
LIFECYCLE = ("CANDIDATE", "REVIEWED", "CURATED")


def schema_errors(package: dict) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [f"{list(e.path)}: {e.message}"
            for e in sorted(validator.iter_errors(package), key=lambda e: list(e.path))]


def corpus(package: dict) -> dict[str, dict]:
    """Every identified record in a package, tagged with the collection it came from.

    Substance checks compare peers, so the collection has to travel with the record:
    a microtopic restating a step of the relation it teaches is not the defect being
    looked for, and two microtopics restating each other is.
    """
    records = {}
    for collection, rows in package.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                records[row["id"]] = {**row, "_collection": collection}
    return records


def check(package: dict) -> dict:
    """Run the six-point intake checklist. Returns a report; never raises on content."""
    findings: list[dict] = []

    def fail(point: str, detail: str):
        findings.append({"point": point, "detail": detail})

    structure = schema_errors(package)
    for error in structure[:10]:
        fail("STRUCTURE", error)

    microtopics = package.get("microtopics", [])
    if not microtopics:
        fail("SUBSTANCE", "package declares no microtopics")

    for row in microtopics:
        mid = row.get("id", "<unidentified>")

        # 1. An entry point: what the learner can already do before this unit.
        if not row.get("entry_assumptions"):
            fail("ENTRY", f"{mid}: no entry assumption, so the starting capability is unstated")

        # 2. A real inference, not a heading.
        if not str(row.get("inferential_jump", "")).strip():
            fail("INFERENCE", f"{mid}: no inferential jump; a title is not a teachable transition")

        # 3. A teaching path whose steps justify themselves.
        path = row.get("teaching_path", [])
        if not path:
            fail("PATH", f"{mid}: no teaching path")
        for step in path:
            if not str(step.get("why_valid", "")).strip():
                fail("PATH", f"{mid}:{step.get('id')}: step asserts an action with no justification")

        # 4. A plausible wrong path, with a diagnostic and a repair.
        misconceptions = row.get("misconceptions", [])
        if not misconceptions:
            fail("MISCONCEPTION", f"{mid}: no plausible wrong path recorded")
        for item in misconceptions:
            for field in ("wrong_idea", "diagnostic_prompt", "repair"):
                if not str(item.get(field, "")).strip():
                    fail("MISCONCEPTION", f"{mid}: misconception missing {field}")

        # 5. An observable exit task that actually closes.
        exit_task = row.get("exit_task") or {}
        if not str(exit_task.get("prompt", "")).strip():
            fail("EXIT", f"{mid}: no exit task, so mastery is unobservable")
        answer = exit_task.get("answer") or {}
        if not str(answer.get("summary", "")).strip():
            fail("EXIT", f"{mid}: exit task has no model answer; the learner cannot self-check")
        if not answer.get("reasoning"):
            fail("EXIT", f"{mid}: exit task answer states a result with no reasoning")

        # 6. Honest provenance: authored substance says so.
        if not row.get("source_refs"):
            fail("PROVENANCE", f"{mid}: no source references, not even an authored-draft marker")

    # 7. Records that discriminate: peers must not say the same thing.
    records = corpus(package)
    for finding in substance_findings(records) + substance_step_findings(records):
        fail(finding["point"], f'{finding["record"]}.{finding["field"]}: {finding["detail"]}')

    # 8. Exit answers stand behind themselves: an oracle, or a named reason there is none.
    issue_ids = {i.get("id") for i in package.get("known_issues", [])}
    datum_ids = {d.get("id") for d in package.get("data", [])}
    for row in microtopics:
        oracle = (row.get("exit_task") or {}).get("oracle") or {}
        if "held_by" in oracle and oracle["held_by"] not in issue_ids:
            fail("EXIT_ORACLE", f'{row.get("id")}: held by {oracle["held_by"]}, which this '
                                "package does not declare as a known issue")
        for variable, datum in (oracle.get("verification", {}).get("bindings") or {}).items():
            if datum not in datum_ids:
                fail("EXIT_ORACLE", f'{row.get("id")}: binds {variable} to {datum}, '
                                    "which is not a declared datum")

    status = package.get("status")
    if status not in LIFECYCLE:
        fail("LIFECYCLE", f"status {status!r} is not one of {LIFECYCLE}")

    return {"package_id": package.get("package_id"), "subject": package.get("subject"),
            "status": status, "microtopic_count": len(microtopics),
            "admitted": not findings, "findings": findings,
            "acceptance": "STRUCTURAL_AND_SUBSTANCE_CHECKS_ONLY; "
                          "no scientific or pedagogical acceptance is granted by intake"}


def admit(package: dict) -> dict:
    report = check(package)
    require(report["admitted"], "LIBRARY_INTAKE_REJECTED",
            "; ".join(f"{f['point']}: {f['detail']}" for f in report["findings"][:5]))
    return report


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run library intake on one or more packages")
    parser.add_argument("packages", nargs="+", type=Path)
    args = parser.parse_args()
    reports = [check(load(path)) for path in args.packages]
    print(json.dumps(reports, indent=2, ensure_ascii=False))
    return 0 if all(r["admitted"] for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
