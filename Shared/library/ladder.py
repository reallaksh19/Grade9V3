"""Prerequisite-safe ladder traversal.

A ladder position is a curriculum coordinate, not evidence.  This module separates:
- requested entry (profile/owner coordinate), from
- reachable entry and segment (what prerequisites permit).

A prerequisite is satisfied only when it is demonstrated/otherwise supplied by the
caller, explicitly bridged by repo-owned data supplied by the caller, or taught by an
earlier rung in the selected segment.
"""
from __future__ import annotations


def rung_capability(row: dict, microtopics: dict) -> str | None:
    mic = microtopics.get(row.get("microtopic_ref")) or {}
    return mic.get("primary_capability_ref")


def prerequisite_closure(capability_id: str, capabilities: dict) -> set[str]:
    found: set[str] = set()
    visiting: set[str] = set()

    def visit(current: str):
        if current in visiting:
            return
        visiting.add(current)
        record = capabilities.get(current) or {}
        for prerequisite in record.get("prerequisite_refs", []):
            if prerequisite in found:
                continue
            found.add(prerequisite)
            if prerequisite in capabilities:
                visit(prerequisite)
        visiting.remove(current)

    visit(capability_id)
    return found


def rung_rows_by_capability(rows: list[dict], microtopics: dict) -> dict[str, dict]:
    found = {}
    for row in rows:
        capability = rung_capability(row, microtopics)
        if capability:
            found[capability] = row
    return found


def requested_rung_from_position(rows: list[dict], position: int) -> dict:
    exact = [row for row in rows if row.get("ladder_position") == position]
    if exact:
        return {"rung": exact[0]["rung"], "why": "LADDER_POSITION"}
    below = [row["rung"] for row in rows if row.get("ladder_position", 0) < position]
    above = [row["rung"] for row in rows if row.get("ladder_position", 0) > position]
    return {
        "rung": None,
        "why": "BETWEEN_RUNGS",
        "detail": (
            f'nearest below {below[-1] if below else "none"}, nearest above '
            f'{above[0] if above else "none"}; a curriculum coordinate between rungs '
            "does not establish a new rung"
        ),
    }


def earliest_required_rung(rows: list[dict], target_rung: str, capabilities: dict,
                           microtopics: dict, demonstrated: set[str] | None = None,
                           bridged: set[str] | None = None) -> dict:
    """Rewind a requested rung to its earliest unsatisfied same-ladder prerequisite."""
    demonstrated = demonstrated or set()
    bridged = bridged or set()
    by_rung = {row["rung"]: row for row in rows}
    target = by_rung.get(target_rung)
    if target is None:
        return {"rung": None, "why": "RUNG_UNKNOWN", "target_rung": target_rung}
    target_capability = rung_capability(target, microtopics)
    if not target_capability:
        return {"rung": None, "why": "RUNG_HAS_NO_CAPABILITY", "target_rung": target_rung}

    rung_by_capability = rung_rows_by_capability(rows, microtopics)
    required = prerequisite_closure(target_capability, capabilities)
    candidates = []
    for capability in required:
        row = rung_by_capability.get(capability)
        if row is None or capability in demonstrated or capability in bridged:
            continue
        candidates.append(row)
    candidates.sort(key=lambda row: row.get("ladder_position", 0))
    if candidates:
        row = candidates[0]
        return {
            "rung": row["rung"],
            "why": "EARLIEST_MISSING_PREREQUISITE",
            "requested_rung": target_rung,
            "capability": rung_capability(row, microtopics),
        }
    return {
        "rung": target_rung,
        "why": "REQUESTED_RUNG_REACHABLE",
        "requested_rung": target_rung,
        "capability": target_capability,
    }


def segment_reachability(rows: list[dict], segment_rungs: list[str], capabilities: dict,
                         microtopics: dict, demonstrated: set[str] | None = None,
                         bridged: set[str] | None = None) -> dict:
    """Prove each rung can be entered from evidence/bridges/earlier selected rungs."""
    demonstrated = set(demonstrated or ())
    bridged = set(bridged or ())
    by_rung = {row["rung"]: row for row in rows}
    available = set(demonstrated) | set(bridged)
    steps = []
    blockers = []

    for rung in segment_rungs:
        row = by_rung.get(rung)
        if row is None:
            blockers.append({"rung": rung, "point": "SEGMENT_RUNG_UNKNOWN"})
            continue
        capability = rung_capability(row, microtopics)
        if not capability:
            blockers.append({"rung": rung, "point": "SEGMENT_RUNG_HAS_NO_CAPABILITY"})
            continue
        required = prerequisite_closure(capability, capabilities)
        missing = sorted(prerequisite for prerequisite in required
                         if prerequisite not in available)
        # A transitive prerequisite that is the current capability is a cycle elsewhere;
        # do not turn it into evidence here.
        if missing:
            blockers.append({
                "rung": rung,
                "capability": capability,
                "point": "LEARNER_PREREQUISITE_UNSATISFIED",
                "missing_capabilities": missing,
            })
        steps.append({
            "rung": rung,
            "capability": capability,
            "prerequisites": sorted(required),
            "missing_before_rung": missing,
        })
        if not missing:
            available.add(capability)

    return {
        "reachable": not blockers,
        "steps": steps,
        "blockers": blockers,
        "demonstrated": sorted(demonstrated),
        "bridged": sorted(bridged),
    }
