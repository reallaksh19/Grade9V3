#!/usr/bin/env python3
"""A vocabulary ceiling excludes words from ABOVE a rung, never the rung's own output.

The ceiling is the matrix's highest-value field and the only one with no home anywhere
else. A scope boundary excludes content; a ceiling excludes *words*, because a word can
import the very concept being taught. Nothing checked how it was being used.

Measured across fourteen committed matrices: 287 ceiling words, of which 55 are words a
higher rung's jump uses -- the intended kind -- and 8 were the rung's **own output**. A
rung whose ceiling forbids what it teaches cannot be written at all: you cannot repair
"distance is not displacement" without the word displacement. That is a contradiction in
the file rather than a judgement about teaching, so it is enforced.

The other two findings are not enforced, deliberately. A text that uses a word its ceiling
correctly forbids is a content defect, and the repair is somebody's teaching rewritten --
it belongs to that rung's author, the same reason capability_collisions.py reports a
namespace fork and refuses to merge one.

The one that matters most is CEILING_WORD_IN_THE_AUTHORED_EXPLANATION, because the matrix
row is advice to an author and the RECORD is what a learner reads. Nothing compared the
ceiling to the explanation it governs until the entry rung of relative motion was
authored and the question came up. Seven exist, and four of them are the exact terms the
relative-motion benchmark has named since it was written as its measured failure --
MIC-VECTOR-VS-SCALAR explaining a vector with words its entry assumptions never declare.
Named in prose for weeks; mechanical now.

Which text the ceiling binds on follows from what the fields are, not from convenience:

  author-facing   aha, misconception.wrong_idea      name the rung TO THE AUTHOR
  learner-facing  must_contain, diagnostic_prompt,   are said to, or shown to, the learner
                  repair, closure, controlled_variation.notice
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
from Shared.tools.author_brief import capability_chain, rung_state  # noqa: E402

BLOCKING = "CEILING_FORBIDS_THE_RUNGS_OWN_OUTPUT"
REPORTED = "CEILING_WORD_USED_IN_THE_RUNGS_OWN_TEXT"
AUTHORED = "CEILING_WORD_IN_THE_AUTHORED_EXPLANATION"


def says(word: str, text: str) -> bool:
    """Match the ceiling word, allowing a plural. Without this the check under-reports:
    a jump saying "a pair of signed components" hides a ceiling forbidding "component"."""
    return bool(re.search(r"\b" + re.escape(word.lower()) + r"(?:e?s)?\b",
                          (text or "").lower()))


def explanation(mic: dict) -> str:
    """The text a learner actually reads. The matrix row is advice to an author; this is
    the thing the ceiling exists to constrain, and until now nothing compared the two."""
    parts = [mic.get("inferential_jump")]
    for step in mic.get("teaching_path", []):
        parts += [step.get("action"), step.get("why_valid"), step.get("output")]
    exit_task = mic.get("exit_task") or {}
    answer = exit_task.get("answer") or {}
    parts += [exit_task.get("prompt"), answer.get("summary"), answer.get("check")]
    parts += answer.get("reasoning") or []
    return " ".join(p for p in parts if p)


def learner_text(row: dict) -> str:
    misconception = row.get("misconception") or {}
    parts = list(row.get("must_contain") or [])
    parts += [misconception.get("diagnostic_prompt"), misconception.get("repair"),
              row.get("closure")]
    parts += [phase.get("notice") for phase in row.get("controlled_variation", [])]
    return " ".join(p for p in parts if p)


def findings(board: dict, caps: dict, mics: dict) -> list[dict]:
    found = []
    for row in board.get("rungs", []):
        ceiling = row.get("ceiling") or []
        if not ceiling:
            continue
        # A SOURCE rung carries no `aha` -- the record owns it -- so the rung's own output
        # is read from the microtopic's jump. Reading only the matrix would let a ceiling
        # forbid its own output wherever a record exists, which is most of them.
        state, ref = rung_state(row, caps, mics), row.get("microtopic_ref")
        own = row.get("aha") or state.get("jump", "")
        learner = learner_text(row)
        for word in ceiling:
            if says(word, own):
                found.append({"point": BLOCKING, "where": f'{row["rung"]}.{word}',
                              "detail": "this rung teaches this word, so forbidding it "
                                        "makes the rung unwritable; a ceiling excludes "
                                        "words from above"})
            elif says(word, learner):
                found.append({"point": REPORTED, "where": f'{row["rung"]}.{word}',
                              "detail": "the matrix's learner-facing text uses a word "
                                        "this rung's ceiling forbids"})
            elif ref in mics and says(word, explanation(mics[ref])):
                found.append({"point": AUTHORED, "where": f'{row["rung"]}.{word}',
                              "detail": f"{ref}, the record a learner actually reads, "
                                        f"uses a word this rung's ceiling forbids"})
    return found


def audit(repo: Path = REPO) -> dict:
    rows, chains = [], {}
    for path in sorted(repo.glob("*/matrices/*.rungs.json")):
        board = load(path)
        subject = board["subject"]
        if subject not in chains:
            chains[subject] = capability_chain(subject)
        found = findings(board, *chains[subject])
        rows.append({"matrix": str(path.relative_to(repo)), "bucket": board["bucket_id"],
                     "ceiling_words": sum(len(r.get("ceiling") or [])
                                          for r in board.get("rungs", [])),
                     "findings": found})
    def count(point):
        return len([f for r in rows for f in r["findings"] if f["point"] == point])
    blocking = count(BLOCKING)
    return {"matrices": len(rows), "boards": rows,
            "ceiling_words": sum(r["ceiling_words"] for r in rows),
            "blocking": blocking, "reported": count(REPORTED),
            "in_the_explanation": count(AUTHORED),
            "passed": not blocking}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true",
                        help=f"exit nonzero on {BLOCKING}; {REPORTED} never fails the "
                             f"build, because the repair belongs to the rung's author")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] or not args.enforce else 1


if __name__ == "__main__":
    raise SystemExit(main())
