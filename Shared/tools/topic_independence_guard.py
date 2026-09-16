#!/usr/bin/env python3
"""Fail if subject-neutral engine code carries hardcoded subject or topic identity.

The rule this enforces: subject and topic variation is governed data, never a branch
in engine code. Code under Shared/ must work for Physics, Mathematics and Chemistry
without knowing which one it is running for.

What counts as a violation, inside a scanned root:

  1. A governed-identifier literal  -- hyphenated uppercase tokens such as
     PHY-M2D, BUCKET-RELATIVE-MOTION, CAP-SIGNED-PAIR, MIC-SAME-TIME. These name
     specific buckets, gates, capabilities or microtopics and belong in JSON data
     or in a subject adapter, not in shared logic.
  2. A subject-name literal -- "Physics", "Mathematics", "Chemistry" appearing as a
     string constant. Shared code may accept a subject as a parameter; it may not
     name one.

Python files are parsed with `ast`, so only real string constants are inspected:
comments and docstrings explaining the architecture are not violations. JavaScript
files are scanned with a quoted-string regex, which is approximate -- it can miss
template literals and can flag strings inside comments.

Exceptions live in topic_independence_allowlist.json and each require a written
reason; an entry without a reason is itself a violation.

Usage:
    python3 Shared/tools/topic_independence_guard.py
    python3 Shared/tools/topic_independence_guard.py --root Shared --root docs
    python3 Shared/tools/topic_independence_guard.py --selftest
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = Path(__file__).resolve().parent / "topic_independence_allowlist.json"
# This detector necessarily contains the patterns it detects -- its own regexes and its
# planted selftest fixture. It is the single structurally exempt file, and its correct
# behaviour is proven independently by --selftest rather than by scanning itself.
SELF = Path(__file__).resolve()

GOVERNED_ID = re.compile(r"\b[A-Z]{2,}(?:-[A-Z0-9]+)+\b")
SUBJECT_NAME = re.compile(r"\b(?:Physics|Mathematics|Chemistry)\b")
JS_STRING = re.compile(r"""(['"])((?:\\.|(?!\1)[^\\\n])*)\1""")
PY_SUFFIXES = {".py"}
JS_SUFFIXES = {".js", ".mjs", ".cjs"}


class Violation:
    def __init__(self, path: Path, line: int, literal: str, reason: str):
        self.path, self.line, self.literal, self.reason = path, line, literal, reason

    def __str__(self) -> str:
        shown = self.literal if len(self.literal) <= 60 else self.literal[:57] + "..."
        rel = self.path.relative_to(REPO_ROOT) if self.path.is_relative_to(REPO_ROOT) else self.path
        return f"{rel}:{self.line}: {self.reason}: {shown!r}"


def load_allowlist() -> list[dict]:
    if not ALLOWLIST.is_file():
        return []
    entries = json.loads(ALLOWLIST.read_text(encoding="utf-8")).get("allow", [])
    for entry in entries:
        if not str(entry.get("reason", "")).strip():
            raise SystemExit(f"allowlist entry without a reason: {entry}")
    return entries


def allowed(entries: list[dict], path: Path, literal: str) -> bool:
    rel = str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path)
    return any(entry["path"] == rel and entry["literal"] == literal for entry in entries)


def check_literal(literal: str) -> str | None:
    if GOVERNED_ID.search(literal):
        return "governed identifier in engine code"
    if SUBJECT_NAME.search(literal):
        return "subject name in engine code"
    return None


def docstring_nodes(tree: ast.AST) -> set[int]:
    marked = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                marked.add(id(body[0].value))
    return marked


def scan_python(path: Path, entries: list[dict]) -> list[Violation]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [Violation(path, exc.lineno or 0, str(exc.msg), "file does not parse")]
    skip, found = docstring_nodes(tree), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
            reason = check_literal(node.value)
            if reason and not allowed(entries, path, node.value):
                found.append(Violation(path, node.lineno, node.value, reason))
    return found


def scan_javascript(path: Path, entries: list[dict]) -> list[Violation]:
    found = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for match in JS_STRING.finditer(line):
            literal = match.group(2)
            reason = check_literal(literal)
            if reason and not allowed(entries, path, literal):
                found.append(Violation(path, number, literal, reason))
    return found


def scan(roots: list[Path]) -> tuple[list[Violation], int]:
    entries, found, scanned = load_allowlist(), [], 0
    for root in roots:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.resolve() == SELF:
                continue
            if path.suffix in PY_SUFFIXES:
                found += scan_python(path, entries)
            elif path.suffix in JS_SUFFIXES:
                found += scan_javascript(path, entries)
            else:
                continue
            scanned += 1
    return found, scanned


def selftest() -> int:
    """Prove the guard detects a planted violation; a guard that scans nothing passes vacuously."""
    with tempfile.TemporaryDirectory() as temp:
        planted = Path(temp) / "planted.py"
        planted.write_text(
            '"""Docstring mentioning Physics and PHY-M2D must not be flagged."""\n'
            "# A comment mentioning Chemistry and BUCKET-RELATIVE-MOTION must not be flagged.\n"
            "def route(bucket_id):\n"
            '    if bucket_id == "PHY-M2D":\n'
            "        return 1\n"
            '    if bucket_id == "Mathematics":\n'
            "        return 2\n"
            '    return "generic_value"\n',
            encoding="utf-8")
        found = scan_python(planted, [])
        literals = sorted(v.literal for v in found)
        if literals != ["Mathematics", "PHY-M2D"]:
            print(f"SELFTEST FAIL: expected ['Mathematics', 'PHY-M2D'], detected {literals}")
            return 1
    print("SELFTEST PASS: planted identifier and subject literals detected; "
          "docstring and comment mentions correctly ignored.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Topic independence guard for subject-neutral engine code")
    parser.add_argument("--root", action="append", default=None,
                        help="directory to scan, relative to the repository root (default: Shared)")
    parser.add_argument("--selftest", action="store_true", help="verify the guard detects a planted violation")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    roots = [REPO_ROOT / r for r in (args.root or ["Shared"])]
    missing = [r for r in roots if not r.is_dir()]
    if missing:
        print("no such root: " + ", ".join(str(r) for r in missing))
        return 2
    found, scanned = scan(roots)
    if found:
        print(f"Topic independence guard: {len(found)} violation(s) in {scanned} scanned file(s)\n")
        for violation in found:
            print("  " + str(violation))
        print("\nMove the identifier into governed data or a subject adapter, or add an "
              "allowlist entry with a reason in Shared/tools/topic_independence_allowlist.json.")
        return 1
    print(f"Topic independence guard: 0 violations in {scanned} scanned file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
