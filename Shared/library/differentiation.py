#!/usr/bin/env python3
"""An A product and its B product must demand different learner work.

The shared role invariants state the rule and also state its failure mode: "Turning B
into A with the nouns changed, or into A with random blanks punched into it, fails this
rule." Today's Core1B is neither of those and fails anyway -- it is Core1A with eight
lines appended, each prediction answered on the line below it. A learner reads straight
through and never commits to anything.

The rule is made mechanical **structurally, not by similarity**, and that is deliberate.
The same invariants say that a legitimate shared anchor may recur, that necessary
repetition is legitimate, and that similarity scores are review triggers rather than
verdicts. A gate that flagged a B product for quoting its own governing relation would
be measuring the wrong thing and would train authors to paraphrase equations, which is
worse than the defect.

What is checked instead is the shape of the demand:

  a B product elicits before it reveals      every obligation it covers carries a prompt
                                             and a reveal that names it
  a reveal answers a prompt that came first   the prompt block exists and precedes it
  a prompt is not its own answer              the prompt block does not already contain
                                             what its reveal says, which is exactly the
                                             defect the current product has
  B covers what A covers                      the coverage obligation, which the spec says
                                             is not negotiable because elicitation is
                                             harder to author than exposition

None of these can be satisfied by changing nouns, and none of them fires on repetition.
Product role names are learner-product vocabulary, not subject vocabulary; no subject
appears in this file.
"""
from __future__ import annotations

from Shared.contracts import normalise
from Shared.library.compile_inputs import CONCEPT

# From the shared role invariants' A/B table: the A product reveals a completed
# construction, the B product elicits the decision first.
PAIRS = (("CORE1A", "CORE1B"), ("CORE2A", "CORE2B"))
REVEAL = "ELICITED_REVEAL"


def _blocks(plan: dict, core: str) -> list[dict]:
    return [block for product in plan.get("products", []) if product.get("core") == core
            for unit in product.get("units", []) for block in unit.get("blocks", [])]


def _obligations(blocks: list[dict], concepts: set[str] | None = None) -> set[str]:
    """The obligations these blocks cover, optionally only the ones that are concepts.

    A bucket-level obligation -- orientation, custody, practice -- is a slot in the
    product rather than something taught, and counting one as coverage made a worked
    example in the declarative product read as a concept the eliciting product had
    silently dropped. Which is which comes from the compiler that built them, not from
    the shape of an id: matching a prefix here would put a governed identifier into
    shared code, which is the thing the topic-independence guard exists to refuse.
    """
    found = {oid for block in blocks for oid in block.get("obligation_ids", [])}
    return found if concepts is None else found & concepts


def _revealed_text(block: dict) -> str:
    """What a learner gets after opening a reveal, regardless of block kind."""
    if block.get("kind") == "QUESTION":
        answer = block.get("answer") or {}
        return " ".join([
            str(answer.get("summary", "")),
            *[str(step) for step in answer.get("steps", [])],
            str(answer.get("check", "")),
        ])
    return str(block.get("text", ""))


def findings(plan: dict, obligations: list[dict] | None = None) -> list[dict]:
    """Every way a compiled plan's B product fails to demand work its A product does not."""
    found: list[dict] = []
    concepts = None if obligations is None else {
        o["id"] for o in obligations if o.get("scope") == CONCEPT}

    def fail(point: str, core: str, subject_id: str, detail: str):
        found.append({"point": point, "core": core, "block": subject_id, "detail": detail})

    for a_core, b_core in PAIRS:
        a_blocks, b_blocks = _blocks(plan, a_core), _blocks(plan, b_core)
        if not b_blocks:
            continue

        # The coverage obligation. A B product that quietly teaches less than its A
        # product has solved the authoring problem by dropping the hard concepts, which
        # is the one resolution the spec names and refuses.
        missing = _obligations(a_blocks, concepts) - _obligations(b_blocks, concepts)
        for oid in sorted(missing):
            fail("COVERAGE_BELOW_A", b_core, oid,
                 f"{a_core} constructs this and {b_core} does not elicit it, which is the "
                 "silent coverage reduction the role forbids")

        indexed = {block["id"]: position for position, block in enumerate(b_blocks)}
        elicited: set[str] = set()
        for position, block in enumerate(b_blocks):
            if block.get("placement") != REVEAL:
                continue
            prompt_id = block.get("reveals_block_id")
            if not prompt_id or prompt_id not in indexed:
                fail("REVEAL_WITHOUT_PROMPT", b_core, block["id"],
                     f"reveals {prompt_id or '<nothing>'}, which this product does not contain")
                continue
            if indexed[prompt_id] >= position:
                fail("REVEAL_BEFORE_PROMPT", b_core, block["id"],
                     f"is placed before {prompt_id}, so the answer arrives before the question")
                continue
            prompt = b_blocks[indexed[prompt_id]]
            revealed = normalise(_revealed_text(block))
            if revealed and revealed in normalise(prompt.get("text", "")):
                fail("PROMPT_ANSWERED_IN_PLACE", b_core, prompt["id"],
                     "already contains what its reveal says, so nothing is being asked")
            elicited |= set(prompt.get("obligation_ids", []))

        for oid in sorted(_obligations(b_blocks, concepts) - elicited):
            fail("OBLIGATION_WITHOUT_ELICITATION", b_core, oid,
                 f"is covered by {b_core} with no prompt a learner must answer before a "
                 "reveal, so this product asks for no commitment here")

    return found


def audit(plan: dict, obligations: list[dict] | None = None) -> dict:
    found = findings(plan, obligations)
    return {"findings": found, "differentiated": not found}
