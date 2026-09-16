"""Canonical values, explicit failures and exact reference validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


class ContractError(ValueError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ContractError(code, detail)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load(path: str | Path) -> dict:
    def reject_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY", key)
            result[key] = value
        return result

    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=reject_pairs,
                         parse_constant=lambda x: (_ for _ in ()).throw(
                             ContractError("NONFINITE_JSON_NUMBER", x)))


def unique(rows: list[dict], key: str, code: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        value = row.get(key)
        require(isinstance(value, str) and bool(value.strip()), code, repr(value))
        require(value not in result, code, value)
        result[value] = row
    return result


def strings(values: object, code: str, *, allow_empty: bool = False) -> list[str]:
    require(isinstance(values, list), code)
    require(allow_empty or bool(values), code)
    require(all(isinstance(x, str) and x.strip() for x in values), code)
    require(len(values) == len(set(values)), code)
    return values


def text(value: object, code: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), code)
    return value


def bound_path(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and not Path(relative).is_absolute(),
            "ARTIFACT_PATH_MUST_BE_RELATIVE", str(relative))
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "ARTIFACT_PATH_ESCAPES_ROOT", relative)
    require(path.is_file(), "ARTIFACT_MISSING", relative)
    return path


def verify_file(root: Path, ref: dict) -> Path:
    path = bound_path(root, ref.get("path", ""))
    require(ref.get("sha256") == file_digest(path), "ARTIFACT_DIGEST_MISMATCH", str(path))
    return path


def validate_dag(rows: list[dict], key: str, dependency_key: str,
                 external: set[str] | None = None) -> list[str]:
    indexed = unique(rows, key, "DUPLICATE_GRAPH_NODE")
    external = external or set()
    done, active, order = set(), set(), []

    def visit(node):
        if node in done or node in external:
            return
        require(node in indexed, "UNKNOWN_DEPENDENCY", node)
        require(node not in active, "DEPENDENCY_CYCLE", node)
        active.add(node)
        dependencies = strings(indexed[node].get(dependency_key, []),
                               "INVALID_DEPENDENCIES", allow_empty=True)
        for dep in dependencies:
            visit(dep)
        active.remove(node)
        done.add(node)
        order.append(node)

    for node in indexed:
        visit(node)
    return order
