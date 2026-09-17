#!/usr/bin/env python3
"""A role specification may not require content the schema has nowhere to keep.

The six role specifications were written to the intent. The package schema was written
to what already existed. Nothing compared them, and three separate findings turned out
to be that one gap: Core2's ladder hints, Core2A's first difficult move, four of
Core2B's five required fields -- all stated in prose, none with a field to live in. A
requirement with no home is not a requirement; it is a sentence.

Each spec now ends with a fenced ``requires`` block: one field path per line, then the
prose phrase it was translated from. This resolves every path against the schema and
reports the ones with no home.

What it cannot do, stated here because a gate that is trusted for more than it checks
is worse than no gate. It checks *block against schema*. It cannot check *prose against
block*, because the prose is prose: a requirement nobody writes into a block is
invisible here and stays a reviewer's duty. Nor does it report the reverse direction --
a schema field no spec requires -- because identifiers, references and provenance
plumbing legitimately exist without any role asking for them, and a finding this tool
cannot adjudicate is noise.

What it does buy: once a requirement is written down, it can never quietly lose its
home. Deleting the field breaks the build, and so does renaming it.

The record types are read out of the schema rather than listed here, so a collection
added later is resolvable the day it lands, and no subject vocabulary enters this file.
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

from Shared.contracts import load  # noqa: E402

SPECS = "Shared/roles"
SCHEMA = "Shared/library/package.schema.json"
BLOCK = re.compile(r"^```requires$(.*?)^```$", re.MULTILINE | re.DOTALL)
LINKED = re.compile(r"\]\((CORE[0-9A-Z]*\.md)\)")
SEGMENT = re.compile(r"^([a-z][a-z0-9_]*)(\[\])?$")
PACKAGE_ROOT = "package"


def requirements(spec: Path) -> list[dict] | None:
    """The paths a spec requires, with the phrase each was translated from.

    None -- distinct from an empty list -- means the spec carries no block at all,
    which is a different failure from a block that asks for nothing.
    """
    found = BLOCK.search(spec.read_text(encoding="utf-8"))
    if not found:
        return None
    rows = []
    for offset, line in enumerate(found.group(1).splitlines()):
        if not line.strip():
            continue
        path, _, phrase = line.strip().partition(" ")
        rows.append({"path": path, "phrase": phrase.strip(),
                     "line": found.group(1)[:0].count("\n") + offset + 1})
    return rows


def record_types(schema: dict) -> dict[str, str]:
    """Each schema definition that a package collection holds, by the name a path uses.

    Derived from the collections rather than listed, so the vocabulary here is whatever
    the schema says it is. A definition reachable only by nesting -- an answer, a step --
    is deliberately not a root: a path says which record it starts from.
    """
    roots = {}
    for collection, spec in schema.get("properties", {}).items():
        ref = (spec.get("items") or {}).get("$ref", "")
        if spec.get("type") == "array" and ref.startswith("#/$defs/"):
            roots[ref.rsplit("/", 1)[1]] = collection
    return roots


def _deref(node: dict, schema: dict) -> dict:
    seen = set()
    while "$ref" in node:
        ref = node["$ref"]
        if ref in seen:
            return {}
        seen.add(ref)
        node = schema.get("$defs", {}).get(ref.rsplit("/", 1)[1], {})
    return node


def _branches(node: dict, schema: dict):
    """Every object shape a node may take, flattening the combinators the schema uses.

    A node may carry its own `properties` *and* a combinator -- an object that names its
    fields and then uses `anyOf` to say which of them are required is the ordinary way to
    write "exactly one of these two". So each branch is merged with the node's own
    properties rather than replacing them, which is the bug this comment exists for: the
    first version dropped them, and the gate reported a field it had itself just been
    shown.
    """
    node = _deref(node, schema)
    own = node.get("properties", {})
    for key in ("anyOf", "oneOf"):
        if key in node:
            for option in node[key]:
                for shape in _branches(option, schema):
                    yield {**shape, "properties": {**own, **shape.get("properties", {})},
                           "type": shape.get("type") or node.get("type"),
                           "additionalProperties": shape.get("additionalProperties",
                                                             node.get("additionalProperties"))}
            return
    if "allOf" in node:
        merged = {"type": node.get("type"), "properties": {},
                  "additionalProperties": node.get("additionalProperties")}
        for option in node["allOf"]:
            for shape in _branches(option, schema):
                merged["properties"].update(shape.get("properties", {}))
                merged["type"] = merged["type"] or shape.get("type")
                if shape.get("additionalProperties") is False:
                    merged["additionalProperties"] = False
        merged["properties"].update(node.get("properties", {}))
        yield merged
        return
    yield node


def resolve(path: str, schema: dict) -> tuple[str, str]:
    """Where a required path lands in the schema: ("", "") when it has a home.

    Returns a finding code and a detail otherwise. An array marker is checked rather
    than ignored -- `question.hints[]` satisfied by a string field would be a home in
    name only, and the requirement it came from says "in their original ordering".
    """
    segments = path.split(".")
    parsed = [SEGMENT.match(s) for s in segments]
    if not path or not all(parsed):
        bad = next((s for s, m in zip(segments, parsed) if not m), path)
        return "SPEC_PATH_MALFORMED", f"{bad!r} is not a field name, optionally followed by []"

    roots, head = record_types(schema), parsed[0]
    if head.group(2):
        return "SPEC_PATH_MALFORMED", "the first segment names a record type and takes no []"
    if head.group(1) == PACKAGE_ROOT:
        node = schema
    elif head.group(1) in roots:
        node = schema["$defs"][head.group(1)]
    else:
        return "SPEC_ROOT_UNKNOWN", (f'{head.group(1)!r} is no record type; the schema holds '
                                     f'{", ".join(sorted(roots)) or "none"}')

    walked = head.group(1)
    for segment in parsed[1:]:
        name, is_array = segment.group(1), bool(segment.group(2))
        shapes = list(_branches(node, schema))
        match = next((s["properties"][name] for s in shapes
                      if name in s.get("properties", {})), None)
        if match is None:
            if any(s.get("additionalProperties") not in (False, None) for s in shapes):
                return "SPEC_FIELD_UNCHECKED", (f"{walked} would accept {name!r} as an extra "
                                                f"property, but names and constrains nothing")
            return "SPEC_FIELD_ABSENT", f"{walked} has no {name!r}"
        walked = f"{walked}.{name}"
        match = _deref(match, schema)
        if is_array:
            if match.get("type") != "array":
                return "SPEC_FIELD_NOT_ARRAY", (f'{walked} is held as '
                                                f'{match.get("type") or "an unstated type"}, '
                                                f"so an ordering cannot be preserved in it")
            match = _deref(match.get("items", {}), schema)
        node = match
    return "", ""


def audit_spec(spec: Path, schema: dict) -> dict:
    role = spec.stem
    rows = requirements(spec)
    if rows is None:
        return {"role": role, "required": 0, "passed": False,
                "findings": [{"point": "SPEC_BLOCK_MISSING", "path": "",
                              "detail": "states no requirements a schema can be checked against"}]}
    findings = []
    for row in rows:
        code, detail = resolve(row["path"], schema)
        if code:
            findings.append({"point": code, "path": row["path"],
                             "phrase": row["phrase"], "detail": detail})
    return {"role": role, "required": len(rows), "findings": findings, "passed": not findings}


def role_specs(repo: Path = REPO) -> list[Path]:
    """The six role specifications, found by their link from the index that lists them.

    README.md is the shared invariants document, not a seventh role, and carries no
    block of its own: its closure and source-honesty invariants are requirements of the
    roles that pose the work, and appear in their blocks. Reading the index rather than
    globbing means a role added there without a spec is a broken link rather than a
    silently unchecked file.
    """
    index = (repo / SPECS / "README.md").read_text(encoding="utf-8")
    return [repo / SPECS / name for name in dict.fromkeys(LINKED.findall(index))]


def audit(repo: Path = REPO) -> dict:
    schema = load(repo / SCHEMA)
    rows = [audit_spec(spec, schema) for spec in role_specs(repo)]
    return {"roles_checked": len(rows), "roles": rows,
            "requirements": sum(r["required"] for r in rows),
            "without_a_home": sum(len(r["findings"]) for r in rows),
            "passed": bool(rows) and all(r["passed"] for r in rows)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help="exit non-zero on a requirement with no home "
                             "(off while the backlog it measures is open)")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
