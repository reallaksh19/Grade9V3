"""Exact rational checks; no arbitrary expression evaluation or domain inference."""

from __future__ import annotations

from fractions import Fraction


VALIDATORS = {"POLYNOMIAL_FROM_ROOTS", "POLYNOMIAL_VALUE", "LINEAR_EQUATION"}


def _rational(value) -> Fraction:
    if type(value) not in {int, str}:
        raise ValueError("EXACT_RATIONAL_REQUIRED")
    return Fraction(value)


def _serialize(value: Fraction):
    return int(value) if value.denominator == 1 else str(value)


def recompute(case: dict):
    kind = case.get("validator_id")
    if kind not in VALIDATORS:
        raise ValueError(f"VALIDATOR_UNSUPPORTED:{kind}")
    if case.get("domain") != "RATIONAL":
        raise ValueError("MATHEMATICAL_DOMAIN_UNSUPPORTED")
    if kind == "POLYNOMIAL_FROM_ROOTS":
        roots = case.get("roots", [])
        if not roots:
            raise ValueError("ROOTS_REQUIRED")
        leading = _rational(case["leading_coefficient"])
        if leading == 0:
            raise ValueError("LEADING_COEFFICIENT_ZERO")
        coefficients = [leading]
        for raw in roots:
            root = _rational(raw)
            next_coeffs = [Fraction(0)] * (len(coefficients) + 1)
            for index, coefficient in enumerate(coefficients):
                next_coeffs[index] += coefficient
                next_coeffs[index + 1] -= coefficient * root
            coefficients = next_coeffs
        return [_serialize(x) for x in coefficients]
    if kind == "POLYNOMIAL_VALUE":
        coefficients = case.get("coefficients_descending", [])
        if not coefficients:
            raise ValueError("COEFFICIENTS_REQUIRED")
        x, result = _rational(case["x"]), Fraction(0)
        for coefficient in coefficients:
            result = result * x + _rational(coefficient)
        return _serialize(result)
    a, b, c = (_rational(case[x]) for x in ("a", "b", "c"))
    if a == 0:
        raise ValueError("LINEAR_SOLUTION_NOT_UNIQUE")
    return _serialize((c - b) / a)
