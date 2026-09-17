#!/usr/bin/env python3
"""Import a subtopic-intelligence packet as a candidate, and say what it cannot supply.

The parallel tracks author packets in a four-layer shape that is close to this
library's but not the same, and their own contract is explicit that the packets carry
no authority: PR #351's C5 stage records them as DIGEST_PINNED_CANDIDATE_SOURCE_ONLY,
packet_authority NONE, with direct runtime and normative import both disallowed. This
importer is built to that, not around it.

So it does three things and refuses a fourth:

  guards      a packet the substance gate rejects is never imported. Thirty-one of the
              forty-three Physics packets and all fifty-two Chemistry ones say the same
              things as each other; importing those would put the library's stated
              purpose into reverse.
  pins        every imported record records the packet digest it came from, so a later
              divergence upstream is visible rather than silent.
  reports     everything the source has no field for -- why each teaching step is
              valid, what makes a misconception diagnosable, which gate owns the
              mathematics -- is emitted as a named gap.

  never       fills a gap by writing the missing text. A packet's TTU scaffolds are
  invents     candidate input under the C5 mapping, not exit tasks; its misconception
              cues are repairs with no diagnostic prompt behind them. Generating the
              missing halves would manufacture exactly the plausible-looking teaching
              the library exists to keep out.

An imported package is therefore incomplete by construction and will not pass intake
until an author closes the gaps. That is the design, not a shortfall in it.
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

from Shared.contracts import digest, require  # noqa: E402
from Shared.library.substance import findings as substance_findings  # noqa: E402

# What the source layer can supply, and what this library requires that it cannot.
# Named here rather than discovered per packet, so the list is reviewable.
ABSENT_FIELDS = {
    "microtopic.badge_reason": "the source records no reason for a subtopic's difficulty",
    "microtopic.teaching_path[].why_valid": "the source states procedures without justifying them",
    "microtopic.misconceptions[].diagnostic_prompt": "the source pairs a flawed action with a "
                                                     "repair, but asks the learner nothing",
    "microtopic.exit_task": "the source's TTU scaffolds are candidate input under the C5 layer "
                            "mapping, not exit tasks, and carry no oracle; the field is left "
                            "absent rather than filled with a scaffold that cannot be checked",
    "capabilities": "the source declares no assessment capabilities, which are owned by the "
                    "assessment layer and cannot be inferred from a teaching packet",
    "resources": "the source cites no materials of its own",
    "microtopic.research_contribution": "the source records no provenance for its own claims",
    "relation.gate_relation_ref": "subject truth is owned by an engineering gate, and the "
                                  "source names none",
    "data": "the source states no quantitative values, so nothing can be machine-checked",
}
ROLE_BY_ATOM = {"PROCEDURE": "TRANSFORM", "STRATEGY": "DECLARE", "INVARIANT": "VERIFY"}


def slug(gate_id: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", gate_id.upper()).strip("-")


def load_catalog(path: Path) -> list[dict]:
    """A SIL catalogue, whether emitted as JSON or as the explorer's JavaScript."""
    text = path.read_text(encoding="utf-8")
    start, end = text.index("["), text.rindex("]") + 1
    packets = json.loads(text[start:end])
    require(isinstance(packets, list) and packets, "SIL_CATALOG_EMPTY", str(path))
    return packets


def admissible(packets: list[dict]) -> tuple[set[str], list[dict]]:
    """Which packets the substance gate lets through, judged against their own peers."""
    records = {p["gate_id"]: {**p, "_collection": "sil_packet"} for p in packets}
    found = substance_findings(records)
    return set(records) - {f["record"] for f in found}, found


def convert(packet: dict, *, subject: str, source: dict) -> tuple[dict, list[dict]]:
    """One packet as a candidate package, plus the gaps that stop it being admitted."""
    bucket_id = f"BUCKET-{slug(packet['gate_id'])}"
    pin = {"source_pr": source["pr"], "source_head": source["head"],
           "packet_id": packet["gate_id"], "packet_digest": digest(packet),
           "import_mode": "DIGEST_PINNED_CANDIDATE_SOURCE_ONLY", "packet_authority": "NONE"}
    gaps = [{"kind": "SIL_FIELD_ABSENT", "field": field, "detail": why}
            for field, why in sorted(ABSENT_FIELDS.items())]

    atoms = packet.get("atoms", [])
    concept = next((a for a in atoms if a["atom_type"] == "CONCEPT"), None)
    steps = [{"id": a["atom_id"], "role": ROLE_BY_ATOM.get(a["atom_type"], "DECLARE"),
              "action": a["description"], "why_valid": "", "inputs": [], "output": ""}
             for a in atoms if a["atom_type"] in ROLE_BY_ATOM]
    microtopic = {
        "id": f"MIC-{slug(packet['gate_id'])}", "version": "0.1.0", "status": "CANDIDATE",
        "source_refs": [], "evidence_refs": [], "extensions": {"sil_import": pin},
        "title": packet["title"], "bucket_id": bucket_id, "primary_capability_ref": "",
        "intrinsic_badge": "MEDIUM", "badge_reason": "",
        "entry_assumptions": list(packet.get("preconditions", [])),
        "inferential_jump": concept["description"] if concept else "",
        "teaching_path": steps, "relation_refs": [], "representation_refs": [],
        "question_family_refs": [f["family_id"] for f in packet.get("families", [])],
        "misconceptions": [{"wrong_idea": m["flawed_action"], "diagnostic_prompt": "",
                            "repair": m["diagnostic_cue"]} for m in packet.get("misconceptions", [])],
        "research_contribution": "", "prerequisite_refs": [], "lineage": [],
    }
    package = {
        "schema_version": "0.1.0", "package_id": f"LIB-{slug(packet['gate_id'])}-IMPORTED",
        "version": "0.1.0", "status": "CANDIDATE", "subject": subject,
        "scope_summary": f"Imported candidate for {packet['title']}. No authority is carried; "
                         "every gap below must be authored before this can be admitted.",
        "curriculum_mappings": [], "resources": [], "buckets": [
            {"id": bucket_id, "version": "0.1.0", "status": "CANDIDATE", "source_refs": [],
             "evidence_refs": [], "extensions": {"sil_import": pin},
             "title": packet["title"], "topic": packet.get("domain", ""),
             "intrinsic_badge": "MEDIUM", "badge_reason": "",
             "depth_overlay": "FOUNDATION", "curriculum_mappings": [],
             "prerequisite_refs": []}],
        "capabilities": [], "microtopics": [microtopic], "relations": [], "representations": [],
        "question_families": [{"id": f["family_id"], "version": "0.1.0", "status": "CANDIDATE",
                               "source_refs": [], "evidence_refs": [],
                               "extensions": {"sil_import": pin, "source_tier": f.get("tier", "")},
                               "title": f["description"], "capability_refs": [],
                               "solution_structure": [], "demand_dimensions": [],
                               "safe_variations": [], "transfer_boundaries": [],
                               "common_wrong_routes": [], "item_refs": []}
                              for f in packet.get("families", [])],
        "questions": [], "teaching_routes": [], "practice_profiles": [], "evidence": [],
        "known_issues": [], "extensions": {"sil_import": pin}, "data": [],
    }
    for step, atom in zip(steps, [a for a in atoms if a["atom_type"] in ROLE_BY_ATOM]):
        gaps.append({"kind": "SIL_FIELD_ABSENT", "field": f'teaching_path.{step["id"]}',
                     "detail": "carries an action with no justification and no output state"})
        gaps.append({"kind": "IMPORTER_INFERRED", "field": f'teaching_path.{step["id"]}.role',
                     "detail": f'read as {step["role"]} from the source atom type '
                               f'{atom["atom_type"]}; the source declares no role, so this is '
                               "the importer's reading and an author should confirm it"})
    for ttu in packet.get("ttus", []):
        gaps.append({"kind": "TTU_CANDIDATE_NOT_PROMOTED", "field": ttu["ttu_id"],
                     "detail": "held as candidate input; promoting a scaffold to an exit task "
                               "needs an oracle the source does not carry"})
    return package, gaps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--packet", required=True, help="the source packet's gate id")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--source-pr", required=True)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    packets = load_catalog(args.catalog)
    admitted, found = admissible(packets)
    chosen = next((p for p in packets if p["gate_id"] == args.packet), None)
    require(chosen is not None, "SIL_PACKET_UNKNOWN", args.packet)
    if args.packet not in admitted:
        reasons = sorted({f["point"] for f in found if f["record"] == args.packet})
        print(json.dumps({"status": "REFUSED", "packet": args.packet, "points": reasons,
                          "detail": "the substance gate rejects this packet; importing it would "
                                    "carry the defect into the library",
                          "catalogue": {"packets": len(packets), "admissible": len(admitted)}},
                         indent=2))
        return 1

    package, gaps = convert(chosen, subject=args.subject,
                            source={"pr": args.source_pr, "head": args.source_head})
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        (args.out.parent / f"{args.out.stem}.gaps.json").write_text(
            json.dumps(gaps, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "IMPORTED_AS_CANDIDATE", "packet": args.packet,
                      "package_id": package["package_id"], "gaps": len(gaps),
                      "catalogue": {"packets": len(packets), "admissible": len(admitted)},
                      "admitted_by_intake": False,
                      "note": "gaps must be authored before intake will admit this"},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
