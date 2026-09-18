#!/usr/bin/env python3
"""Resolve how one canonical capability can be supplied to a study route.

Prerequisite topology answers *what must be known first*. This module answers a different
question: *how can that capability be delivered?* Keeping those concerns separate prevents
"no local matrix rung" from being mistaken for "the capability cannot be satisfied".

The resolver is deliberately subject-agnostic. It knows only about a canonical capability
record and the teaching locations already discovered for it.
"""
from __future__ import annotations

LOCAL = "LOCAL"
EXTERNAL_BRIDGE = "EXTERNAL_BRIDGE"
UNRESOLVED = "UNRESOLVED"
AMBIGUOUS = "AMBIGUOUS"


def resolve(capability: dict, locations: list[dict]) -> dict:
    """Return one deterministic delivery classification for a capability."""
    refs = list(locations or [])
    provider = capability.get("external_provider")
    acceptance = capability.get("acceptance_status")

    if len(refs) == 1:
        state = LOCAL
    elif len(refs) > 1:
        state = AMBIGUOUS
    elif provider:
        state = EXTERNAL_BRIDGE
    else:
        state = UNRESOLVED

    return {
        "state": state,
        "provider": provider,
        "acceptance_status": acceptance,
        "locations": refs,
    }


def legacy_state(delivery: dict) -> str:
    """Compatibility state used by older route/view callers."""
    return {
        LOCAL: "RESOLVED",
        EXTERNAL_BRIDGE: "EXTERNAL_BRIDGE",
        UNRESOLVED: "NO_TEACHING_LOCATION",
        AMBIGUOUS: "AMBIGUOUS_LOCATION",
    }[delivery["state"]]
