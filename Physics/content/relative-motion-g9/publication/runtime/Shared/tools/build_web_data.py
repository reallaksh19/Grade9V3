#!/usr/bin/env python3
"""Generate the data file the browsable surfaces read.

The surfaces are static and must work from `file://`, where `fetch()` of a sibling
JSON file is blocked. The data is therefore emitted as a JavaScript file assigning a
global, not as JSON to be fetched. That is the whole reason this generator exists.

It also precomputes, per bucket, what the library compiler would produce: which
products are supported, which are not and why, and what authoring remains. The run
builder can then tell the truth about a bucket without a server behind it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
OUT = REPO / "tools" / "data.js"

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.library.compile_inputs import compile_bucket  # noqa: E402
from Shared.library.intake import check  # noqa: E402
from Shared.library.resolve import build_index, slice_for_bucket  # noqa: E402


def subjects() -> list[str]:
    return sorted(p.parent.parent.name for p in REPO.glob("*/adapter/CoreContracts.json"))


def gate_summary(subject: str) -> list[dict]:
    rows = []
    for path in sorted((REPO / subject / "gates").glob("*.json")):
        registry = load(path)
        if "gates" not in registry:
            continue
        for gate in registry["gates"]:
            rows.append({"gate_id": gate["gate_id"], "title": gate["title"],
                         "grade": gate["curriculum"]["grade"], "chapter": gate["curriculum"]["chapter"],
                         "scope_class": gate["curriculum"]["scope_class"], "tier": gate["tier"],
                         "scope_state": gate["scope_state"],
                         "prerequisites": gate["prerequisites"],
                         "external_prerequisites": [e["capability_id"]
                                                    for e in gate.get("external_prerequisites", [])],
                         "concepts": [c["statement"] for c in gate["canonical_concepts"]],
                         "misconceptions": [m["wrong_idea"] for m in gate["misconceptions"]]})
    return rows


def bucket_view(records: dict, bucket_id: str) -> dict:
    chosen = slice_for_bucket(records, bucket_id)
    bucket = records[bucket_id]
    microtopics = []
    for mid in chosen["microtopic_order"]:
        row = records[mid]
        microtopics.append({
            "id": mid, "title": row["title"], "badge": row["intrinsic_badge"],
            "status": row.get("status"), "badge_reason": row.get("badge_reason"),
            "entry_assumptions": row.get("entry_assumptions", []),
            "inferential_jump": row.get("inferential_jump"),
            "teaching_path": [{"action": s["action"], "why_valid": s["why_valid"],
                               "output": s.get("output")} for s in row.get("teaching_path", [])],
            "misconceptions": row.get("misconceptions", []),
            "exit_task": row.get("exit_task"),
            "prerequisites": row.get("prerequisite_refs", []),
        })
    return {"id": bucket_id, "title": bucket["title"], "topic": bucket.get("topic"),
            "badge": bucket["intrinsic_badge"], "status": bucket.get("status"),
            "prerequisites": bucket.get("prerequisite_refs", []),
            "curriculum": bucket.get("curriculum_mappings", []),
            "microtopics": microtopics,
            "relations": [{"id": r["id"], "expression": r["expression"], "meaning": r["meaning"],
                           "conditions": r.get("conditions", [])}
                          for r in chosen["records"].get("relations", [])],
            "questions": [{"id": q["id"], "stem": q["stem"], "origin": q.get("origin"),
                           "answer": q["answer"].get("summary")}
                          for q in chosen["records"].get("questions", [])],
            "capabilities": [{"id": c["id"], "action": c["action"],
                              "provider": c.get("external_provider"),
                              "acceptance": c.get("acceptance_status")}
                             for c in chosen["records"].get("capabilities", [])],
            "record_count": chosen["record_count"]}


def compile_preview(records: dict, bucket_id: str, subject: str) -> dict:
    try:
        compiled = compile_bucket(records, bucket_id, topic_id=f"PREVIEW-{bucket_id}",
                                  title=records[bucket_id]["title"], subject=subject,
                                  practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})
    except ContractError as exc:
        return {"compilable": False, "code": exc.code, "detail": exc.detail}
    return {"compilable": True,
            "supported_products": compiled["baseline"]["selected_cores"],
            "atoms": len(compiled["source"]["atoms"]),
            "questions": len(compiled["source"]["questions"]),
            "obligations": len(compiled["baseline"]["obligations"]),
            "authoring_requirements": compiled["authoring_requirements"]}


def build() -> dict:
    payload = {"generated_by": "Shared/tools/build_web_data.py", "subjects": {}}
    for subject in subjects():
        packages = [load(p) for p in sorted((REPO / subject / "library").glob("*.json"))]
        entry = {"contract": {}, "gates": gate_summary(subject), "buckets": [],
                 "packages": [], "library_available": bool(packages)}
        contract = load(REPO / subject / "adapter" / "CoreContracts.json")
        entry["contract"] = {
            "learner_products": contract["learner_products"],
            "validator_catalogue": [{"id": v["id"], "status": v["status"],
                                     "shape": v["result"]["shape"],
                                     "comparison": v["result"]["comparison"],
                                     "does_not_prove": v["does_not_prove"]}
                                    for v in contract["validator_catalogue"]],
            "representation_kinds": contract.get("representation_kinds", []),
            "curriculum": contract.get("curriculum", {}),
        }
        if packages:
            entry["packages"] = [{"package_id": p["package_id"], "status": p["status"],
                                  "admitted": check(p)["admitted"]} for p in packages]
            records = build_index(packages)
            for bucket_id in sorted(r for r, v in records.items() if v["_collection"] == "buckets"):
                view = bucket_view(records, bucket_id)
                view["compile_preview"] = compile_preview(records, bucket_id, subject)
                entry["buckets"].append(view)
        payload["subjects"][subject] = entry
    return payload


def write() -> dict:
    """Regenerate the page data file. Silent, so other tools can depend on it."""
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("// Generated by Shared/tools/build_web_data.py -- do not edit by hand.\n"
                   "window.GRADE9V3 = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n",
                   encoding="utf-8")
    return payload


def main() -> int:
    payload = write()
    buckets = sum(len(s["buckets"]) for s in payload["subjects"].values())
    print(f"wrote {OUT.relative_to(REPO)}: {len(payload['subjects'])} subject(s), {buckets} bucket(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
