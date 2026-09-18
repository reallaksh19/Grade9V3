"""Bounded SI mechanics checks adapted from PR350's validator families."""

from __future__ import annotations

import math


VALIDATORS = {
    "CONSTANT_ACCELERATION_VELOCITY", "CONSTANT_ACCELERATION_INITIAL_VELOCITY",
    "CONSTANT_ACCELERATION_EVENT_TIME", "SPEED_FROM_COMPONENTS", "APEX_STATE",
    "AVERAGE_RATE",
    "WAVE_SPEED",
    "AVERAGE_POWER", "INSTANTANEOUS_POWER",
    "CONSTANT_ACCELERATION_DISPLACEMENT", "CONSTANT_ACCELERATION_NO_TIME",
    "NEWTON_SECOND_LAW", "WORK_CONSTANT_FORCE", "KINETIC_ENERGY",
    "GRAVITATIONAL_POTENTIAL_ENERGY", "MECHANICAL_ADVANTAGE",
    "FREQUENCY_PERIOD", "ECHO_DISTANCE", "AVERAGE_ACCELERATION",
    "UNIFORM_CIRCULAR_SPEED",
}


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
    if kind == "AVERAGE_RATE":
        dt = _number(case, "dt", "s")
        distance = _number(case, "distance", "m")
        displacement = _number(case, "displacement", "m")
        if dt <= 0 or distance < 0:
            raise ValueError("AVERAGE_RATE_DOMAIN_INVALID")
        return {"average_speed_m_s": distance / dt,
                "average_velocity_m_s": displacement / dt}
    if kind == "WAVE_SPEED":
        frequency = _number(case, "frequency", "Hz")
        wavelength = _number(case, "wavelength", "m")
        if frequency < 0 or wavelength < 0:
            raise ValueError("WAVE_DOMAIN_INVALID")
        return frequency * wavelength
    if kind == "AVERAGE_POWER":
        dt = _number(case, "dt", "s")
        if dt <= 0:
            raise ValueError("POWER_INTERVAL_INVALID")
        return _number(case, "work", "J") / dt
    if kind == "INSTANTANEOUS_POWER":
        speed = _number(case, "speed", "m/s")
        if speed < 0:
            raise ValueError("SPEED_NEGATIVE")
        return _number(case, "force_parallel", "N") * speed
    if kind == "CONSTANT_ACCELERATION_DISPLACEMENT":
        t = _number(case, "t", "s")
        if t < 0:
            raise ValueError("TIME_NEGATIVE")
        return _number(case, "u", "m/s") * t + 0.5 * _number(case, "a", "m/s^2") * t * t
    if kind == "CONSTANT_ACCELERATION_NO_TIME":
        u = _number(case, "u", "m/s")
        a = _number(case, "a", "m/s^2")
        s = _number(case, "s", "m")
        return {"v_squared_m2_s2": u * u + 2 * a * s}
    if kind == "NEWTON_SECOND_LAW":
        mass = _number(case, "mass", "kg")
        if mass <= 0:
            raise ValueError("MASS_NONPOSITIVE")
        return mass * _number(case, "acceleration", "m/s^2")
    if kind == "WORK_CONSTANT_FORCE":
        displacement = _number(case, "displacement", "m")
        if displacement < 0:
            raise ValueError("DISPLACEMENT_NEGATIVE")
        return _number(case, "force_parallel", "N") * displacement
    if kind == "KINETIC_ENERGY":
        mass = _number(case, "mass", "kg")
        speed = _number(case, "speed", "m/s")
        if mass <= 0 or speed < 0:
            raise ValueError("KINETIC_ENERGY_DOMAIN_INVALID")
        return 0.5 * mass * speed * speed
    if kind == "GRAVITATIONAL_POTENTIAL_ENERGY":
        mass = _number(case, "mass", "kg")
        g = _number(case, "g", "m/s^2")
        if mass <= 0 or g <= 0:
            raise ValueError("GPE_DOMAIN_INVALID")
        return mass * g * _number(case, "delta_h", "m")
    if kind == "MECHANICAL_ADVANTAGE":
        load_force = _number(case, "load_force", "N")
        effort_force = _number(case, "effort_force", "N")
        if load_force < 0 or effort_force <= 0:
            raise ValueError("MECHANICAL_ADVANTAGE_DOMAIN_INVALID")
        return load_force / effort_force
    if kind == "FREQUENCY_PERIOD":
        period = _number(case, "period", "s")
        if period <= 0:
            raise ValueError("PERIOD_NONPOSITIVE")
        return 1.0 / period
    if kind == "ECHO_DISTANCE":
        speed = _number(case, "speed", "m/s")
        echo_time = _number(case, "echo_time", "s")
        if speed <= 0 or echo_time < 0:
            raise ValueError("ECHO_DOMAIN_INVALID")
        return 0.5 * speed * echo_time
    if kind == "AVERAGE_ACCELERATION":
        dt = _number(case, "dt", "s")
        if dt <= 0:
            raise ValueError("AVERAGE_ACCELERATION_INTERVAL_INVALID")
        return _number(case, "delta_v", "m/s") / dt
    if kind == "UNIFORM_CIRCULAR_SPEED":
        radius = _number(case, "radius", "m")
        period = _number(case, "period", "s")
        if radius <= 0 or period <= 0:
            raise ValueError("UNIFORM_CIRCULAR_SPEED_DOMAIN_INVALID")
        return 2.0 * math.pi * radius / period
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
