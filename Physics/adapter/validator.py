"""Bounded SI mechanics checks adapted from PR350's validator families."""

from __future__ import annotations

import math


VALIDATORS = {"CONSTANT_ACCELERATION_VELOCITY", "CONSTANT_ACCELERATION_INITIAL_VELOCITY",
              "CONSTANT_ACCELERATION_EVENT_TIME", "SPEED_FROM_COMPONENTS", "APEX_STATE"}


def _number(case: dict, name: str, unit: str) -> float:
    value = case[name]
    if type(value) not in {int, float} or not math.isfinite(value):
        raise ValueError(f"NONFINITE_PHYSICS_VALUE:{name}")
    if case.get("units", {}).get(name) != unit:
        raise ValueError(f"PHYSICS_UNIT_MISMATCH:{name}:{unit}")
    return value


def recompute(case: dict):
    kind = case.get("validator_id")
    if kind not in VALIDATORS:
        raise ValueError(f"VALIDATOR_UNSUPPORTED:{kind}")
    if kind == "SPEED_FROM_COMPONENTS":
        return math.hypot(_number(case, "vx", "m/s"), _number(case, "vy", "m/s"))
    if kind == "APEX_STATE":
        return _apex(case)
    a = _number(case, "a", "m/s^2")
    if case.get("model") != "CONSTANT_ACCELERATION" or not case.get("axis_convention"):
        raise ValueError("PHYSICS_MODEL_AND_AXIS_REQUIRED")
    if kind == "CONSTANT_ACCELERATION_EVENT_TIME":
        if a == 0:
            raise ValueError("EVENT_TIME_NOT_UNIQUE")
        result = (_number(case, "v", "m/s") - _number(case, "u", "m/s")) / a
        if result < 0:
            raise ValueError("EVENT_BEFORE_TIME_ORIGIN")
        return result
    t = _number(case, "t", "s")
    if t < 0:
        raise ValueError("NEGATIVE_ELAPSED_TIME")
    if kind == "CONSTANT_ACCELERATION_VELOCITY":
        return _number(case, "u", "m/s") + a * t
    return _number(case, "v", "m/s") - a * t


def _apex(case: dict) -> dict:
    ux, uy = _number(case, "ux", "m/s"), _number(case, "uy", "m/s")
    g = _number(case, "g", "m/s^2")
    if g <= 0 or uy <= 0 or case.get("model") != "NO_DRAG_CONSTANT_G_UPWARD_POSITIVE":
        raise ValueError("APEX_MODEL_INVALID")
    return {"time_s": uy / g, "velocity_m_s": [ux, 0], "acceleration_m_s2": [0, -g]}
