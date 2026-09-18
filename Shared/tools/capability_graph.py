#!/usr/bin/env python3
"""Capability topology is the reachability authority; ladder positions may not contradict it."""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

from Shared.contracts import ContractError, load

VIOLATION = "LADDER_PREREQUISITE_ORDER_VIOLATION"


def subject_graph(subject: str, repo: Path = REPO) -> tuple[dict, dict]:
    """Return capabilities and microtopics for a subject, indexed by id."""
    caps, mics = {}, {}
    for path in sorted((repo / subject / "library").glob("*.json")):
        package = load(path)
        for cap in package.get("capabilities", []):
            caps[cap["id"]] = cap
        for mic in package.get("microtopics", []):
            mics[mic["id"]] = mic
    return caps, mics


def prerequisite_closure(capability: str, caps: dict) -> list[str]:
    """Known transitive capability prerequisites, prerequisites before dependants."""
    seen, active, ordered = set(), set(), []

    def visit(node: str) -> None:
        if node in seen or node not in caps:
            return
        if node in active:
            return
        active.add(node)
        for parent in caps[node].get("prerequisite_refs", []):
            if parent in caps:
                visit(parent)
        active.remove(node)
        seen.add(node)
        if node != capability:
            ordered.append(node)

    visit(capability)
    return ordered


def _stable_unique(values) -> list[str]:
    seen, out = set(), []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def topological_subset(capabilities, caps: dict) -> list[str]:
    """Known prerequisite closure plus targets, dependencies before dependants.

    The input order is preserved for otherwise-unrelated target capabilities. A cycle in
    the requested slice is an explicit error here: study routing may not silently flatten
    a cyclic prerequisite claim.
    """
    roots = _stable_unique(capabilities)
    seen, active, ordered = set(), set(), []

    def visit(node: str) -> None:
        if node not in caps or node in seen:
            return
        if node in active:
            raise ContractError("CAPABILITY_PREREQUISITE_CYCLE", node)
        active.add(node)
        for parent in caps[node].get("prerequisite_refs", []):
            if parent in caps:
                visit(parent)
        active.remove(node)
        seen.add(node)
        ordered.append(node)

    for root in roots:
        visit(root)
    return ordered


def prerequisite_closure_many(capabilities, caps: dict) -> list[str]:
    """Known transitive prerequisites for several targets, once each."""
    roots = set(_stable_unique(capabilities))
    return [cap for cap in topological_subset(capabilities, caps) if cap not in roots]


def unknown_prerequisites(capabilities, caps: dict) -> list[str]:
    """Unknown prerequisite refs reachable from known requested capabilities."""
    roots = _stable_unique(capabilities)
    seen, missing = set(), []

    def visit(node: str) -> None:
        if node in seen or node not in caps:
            return
        seen.add(node)
        for parent in caps[node].get("prerequisite_refs", []):
            if parent not in caps:
                if parent not in missing:
                    missing.append(parent)
                continue
            visit(parent)

    for root in roots:
        visit(root)
    return missing


def ladder_capabilities(board: dict, mics: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    """Return rung->capability metadata and capability->rung for recorded rows."""
    by_rung, by_cap = {}, {}
    for row in board.get("rungs", []):
        mic = mics.get(row.get("microtopic_ref"))
        cap = mic.get("primary_capability_ref") if mic else None
        if not cap:
            continue
        item = {"rung": row["rung"], "position": row.get("ladder_position", 0),
                "capability": cap, "microtopic": mic["id"]}
        by_rung[row["rung"]] = item
        by_cap[cap] = item
    return by_rung, by_cap


def topology_findings(board: dict, caps: dict, mics: dict) -> list[dict]:
    """A same-ladder prerequisite must appear strictly before its dependant."""
    _, by_cap = ladder_capabilities(board, mics)
    found = []
    for capability, row in sorted(by_cap.items(), key=lambda item: item[1]["position"]):
        for prerequisite in prerequisite_closure(capability, caps):
            prior = by_cap.get(prerequisite)
            if prior is None or prior["position"] < row["position"]:
                continue
            found.append({
                "point": VIOLATION,
                "where": row["rung"],
                "detail": (
                    f'{capability} at {row["position"]} depends on {prerequisite} at '
                    f'{prior["position"]}; a dependant rung may not precede or tie a '
                    "prerequisite rung"
                ),
                "capability": capability,
                "prerequisite": prerequisite,
                "dependent_position": row["position"],
                "prerequisite_position": prior["position"],
            })
    return found


def resolve_entry(rows: list[dict], requested_rung: str, held: dict[str, str],
                  caps: dict, mics: dict) -> dict:
    """Resolve entry without treating a coordinate as evidence of prerequisites.

    Missing same-ladder prerequisites move entry backward to the earliest unmet rung.
    Known prerequisites taught elsewhere are returned as bridge capabilities; callers
    schedule those bridges before the selected subtopic instead of silently assuming them.
    """
    board = {"rungs": rows}
    by_rung, by_cap = ladder_capabilities(board, mics)
    target = by_rung.get(requested_rung)
    if target is None:
        return {"rung": requested_rung, "reason": "NO_RECORDED_CAPABILITY",
                "bridges": [], "unresolved": []}

    closure = prerequisite_closure(target["capability"], caps)
    unmet = [p for p in closure if held.get(p) != "DEMONSTRATED"]
    same = [by_cap[p] for p in unmet if p in by_cap]
    selected = min(same, key=lambda row: row["position"]) if same else target

    # Re-evaluate from the selected rung. If we backtracked from R4 to R3, R3's own
    # external prerequisite is still required; backtracking must not erase it.
    selected_closure = prerequisite_closure(selected["capability"], caps)
    selected_unmet = [p for p in selected_closure if held.get(p) != "DEMONSTRATED"]
    cap_to_mic = {}
    for mic in mics.values():
        cap = mic.get("primary_capability_ref")
        if cap:
            cap_to_mic.setdefault(cap, mic["id"])
    external = [p for p in selected_unmet if p not in by_cap]
    bridges = [
        p for p in external
        if p in cap_to_mic or bool(caps.get(p, {}).get("external_provider"))
    ]
    unresolved = [p for p in external if p not in bridges]
    reason = "PREREQUISITE_BACKTRACK" if same else "REQUESTED_RUNG_REACHABLE"
    return {"rung": selected["rung"], "reason": reason,
            "requested_rung": requested_rung,
            "requested_capability": target["capability"],
            "capability": selected["capability"], "bridges": bridges,
            "unresolved": unresolved}
