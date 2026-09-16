"""The seam between the subject-neutral publication engine and one subject.

Engine code never names a subject. A subject entrypoint constructs an Adapter and
injects it; everything subject-specific arrives through this object or through the
subject contract it carries:

  * how a result is computed          -- adapter.recompute
  * what shape that result has        -- contract validator_catalogue[].result.shape
  * how it is compared                -- contract validator_catalogue[].result.comparison
  * what units its inputs/results use -- contract validator_catalogue[].input_units / result.unit
  * which representation scenes exist -- adapter.scenes
  * which files are its runtime       -- adapter.runtime_files

Comparison strategies are keyed by the *declared* comparison name, not by subject, so
adding a subject adds data and a renderer, never a branch in this package.

The three subjects return genuinely different result shapes -- a scalar with a unit,
an exact rational or coefficient list, an integer element-count map. A tolerance
comparison applied to an exact-rational result would silently accept a wrong answer,
so a shape whose publication path is not implemented fails closed here rather than
being coerced into the scalar path.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from Shared.contracts import load, require

NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
TOLERANCE = 1e-9

# Result shapes whose published representation and read-back path exist today.
# A shape outside this set is a declared-but-unpublishable result: the engine holds
# it rather than guessing a rendering for it.
PUBLISHABLE_SHAPES = {"SCALAR_WITH_UNIT"}


def _finite(value: Any) -> float:
    if isinstance(value, str):
        require(bool(NUMBER.fullmatch(value.strip())), "PUBLISHED_NUMBER_INVALID")
        value = float(value)
    require(type(value) in {int, float} and math.isfinite(value), "NUMERIC_CANDIDATE_INVALID")
    return value


def _rational(value: Any) -> Fraction:
    require(type(value) in {int, str}, "EXACT_RATIONAL_REQUIRED")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise_invalid()


def raise_invalid():
    require(False, "EXACT_RATIONAL_REQUIRED")


def compare_tolerance(expected: Any, candidate: Any) -> None:
    require(math.isclose(_finite(candidate), _finite(expected), rel_tol=TOLERANCE, abs_tol=TOLERANCE),
            "PUBLISHED_ANSWER_MISMATCH")


def compare_exact_rational(expected: Any, candidate: Any) -> None:
    require(_rational(candidate) == _rational(expected), "PUBLISHED_ANSWER_MISMATCH")


def compare_exact_rational_list(expected: Any, candidate: Any) -> None:
    require(isinstance(expected, list) and isinstance(candidate, list), "PUBLISHED_ANSWER_MISMATCH")
    require(len(expected) == len(candidate), "PUBLISHED_ANSWER_MISMATCH")
    for want, got in zip(expected, candidate):
        compare_exact_rational(want, got)


def compare_exact_integer_map(expected: Any, candidate: Any) -> None:
    require(isinstance(expected, dict) and isinstance(candidate, dict), "PUBLISHED_ANSWER_MISMATCH")
    require(expected == candidate, "PUBLISHED_ANSWER_MISMATCH")


def compare_fieldwise_tolerance(expected: Any, candidate: Any) -> None:
    require(isinstance(expected, dict) and isinstance(candidate, dict), "PUBLISHED_ANSWER_MISMATCH")
    require(set(expected) == set(candidate), "PUBLISHED_ANSWER_MISMATCH")
    for key, want in expected.items():
        got = candidate[key]
        if isinstance(want, list):
            require(isinstance(got, list) and len(want) == len(got), "PUBLISHED_ANSWER_MISMATCH")
            for a, b in zip(want, got):
                compare_tolerance(a, b)
        else:
            compare_tolerance(want, got)


COMPARISONS: dict[str, Callable[[Any, Any], None]] = {
    "RELATIVE_AND_ABSOLUTE_TOLERANCE_1E-9": compare_tolerance,
    "EXACT_RATIONAL_EQUALITY": compare_exact_rational,
    "EXACT_RATIONAL_LIST_EQUALITY": compare_exact_rational_list,
    "EXACT_INTEGER_MAP_EQUALITY": compare_exact_integer_map,
    "FIELDWISE_TOLERANCE_1E-9": compare_fieldwise_tolerance,
}


def no_runtime_files() -> list[Path]:
    return []


@dataclass(frozen=True)
class Adapter:
    """One subject's contribution to the engine."""

    contract: dict
    recompute: Callable[[dict], Any]
    scenes: dict[str, Callable] = field(default_factory=dict)
    runtime_files: Callable[[], list[Path]] = no_runtime_files

    @property
    def subject(self) -> str:
        return self.contract["subject"]

    @property
    def learner_products(self) -> set[str]:
        return set(self.contract.get("learner_products", {}))

    def validator(self, validator_id: str) -> dict | None:
        for entry in self.contract.get("validator_catalogue", []):
            if entry.get("id") == validator_id:
                return entry
        return None

    def comparison_for(self, spec: dict) -> Callable[[Any, Any], None]:
        name = spec.get("result", {}).get("comparison")
        require(name in COMPARISONS, "DECLARED_COMPARISON_UNSUPPORTED", str(name))
        return COMPARISONS[name]

    def publishable(self, spec: dict) -> bool:
        return spec.get("result", {}).get("shape") in PUBLISHABLE_SHAPES


def load_contract(path: Path) -> dict:
    contract = load(path)
    for key in ("subject", "learner_products", "validator_catalogue"):
        require(key in contract, "SUBJECT_CONTRACT_INCOMPLETE", key)
    for entry in contract["validator_catalogue"]:
        require("result" in entry and "comparison" in entry["result"],
                "VALIDATOR_RESULT_COMPARISON_REQUIRED", str(entry.get("id")))
    return contract
