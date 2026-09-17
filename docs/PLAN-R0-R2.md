# Execution plan: R0, R1, R2

The roadmap in [ROADMAP-LEARNER-READY.md](ROADMAP-LEARNER-READY.md) says what and why. This says how, at the level an agent executes from: exact files, exact rules, exact falsifiers, exact commit boundaries.

R0–R2 are planned in full because they are tightly coupled — R1's conformance gate names the fields R2 needs, and R0's composition fixes are inherited by both. R3 onward is planned at start-ready detail only, because what R1 measures will change it.

## The working pattern

Every step in this session that held up followed the same order, and every step below does too:

```
measure  →  gate (non-enforcing)  →  fix the data  →  enforce  →  commit
```

Three rules that come from this session's mistakes, not from theory:

- **A gate that fires on good content gets switched off.** A5's first rule flagged 17 of 32 authored steps. Measure against real content and count the false positives before shipping any check.
- **Assert nothing from a screenshot.** The R0 label-collision claim was retracted after measuring the SVG. If a defect can be measured, measure it.
- **One commit per step, every commit green.** Full suite, guard, capability audit, subject sweep and publication sweep pass before each commit. A red intermediate state is how a half-built thing starts reading as finished.

---

## R0 — Two composition defects

Cheap, global, inherited by every phase after. Two items, not the three the roadmap first claimed.

### R0.1 — A sentence embedded inside another sentence

**Sites**, all in `Shared/library/compile_inputs.py::_teaching_text`:

| Line | Join | Produces |
|---|---|---|
| 304 | `f' This gives {sentence(step["output"])}'` | `This gives For x = 2: 3(2) + 2 = 8, and the right side is 9, so 8 = 9 is false.` |
| 301 | `f'A common wrong idea is that {wrong_idea} {repair}'` | `A common wrong idea is that The equals sign means work out the left side…` — and it runs two sentences together on one line |
| 308 | `f'Answer: {answer.get("summary")}'` | ~~benign today; same shape, so same treatment~~ **Not a site.** It ends in a colon, and a capital after a colon is correct English. Left alone, along with `Predict first:`, `Check yourself:` and `Verify:`. Two sites, not three. |

**The rule.** Not lowercasing — that needs proper-noun knowledge nothing has. A field is either a *fragment* that belongs inside the lead-in, or a *sentence* that belongs on its own line. `substance.is_prose` already draws exactly that line (≥6 words, or ends with a terminator) and is already trusted by the substance gate.

```python
def join(lead: str, fragment: str) -> list[str]:
    """One line, or two, depending on whether the fragment is a sentence.

    "a*x = c - b" is a fragment and belongs inside its lead-in.
    "For x = 2: 3(2) + 2 = 8, and the right side is 9" is a sentence and does not.
    Lowercasing the fragment instead would need to know a proper noun from a symbol,
    which nothing here does.
    """
```

- `join("This gives", "a*x = c - b")` → `["This gives a*x = c - b."]`
- `join("This gives", "For x = 2: 3(2) + 2 = 8, …")` → `["This gives:", "For x = 2: 3(2) + 2 = 8, …"]`

Lives in `Shared/contracts.py` beside `sentence()`. `wrong_idea` and `repair` stop being concatenated: the misconception becomes two lines, which is also what it is.

**Falsifiers** (`tests/test_library.py`):
- a fragment output stays inline and gains one terminator
- a sentence output moves to its own line and keeps its capital
- no compiled block in any committed package contains a capital letter directly after `that ` or `gives ` (the general assertion, not the two known strings)

### R0.2 — Figures appended after all prose

**Site**: `compile_inputs.py:281`, `blocks += _figure_blocks(...)` after the microtopic loop closes. Every figure lands after every text block, so the number line that explains exact-versus-truncation appears after the whole argument has been read.

**The fix.** `_figure_blocks` already knows each figure's obligation, and the obligation names the microtopic. Interleave: after appending a microtopic's TEXT block, append the figures bound to that microtopic's obligation. Figures bound to the practice obligation keep their current position, because they belong to the question set rather than to a microtopic.

**Falsifiers**:
- in a compiled CORE1A/CORE1B product, each figure block's index is exactly one greater than the index of the text block carrying the same obligation
- a figure on the practice obligation still sits with the questions
- the committed Physics publication's learner-visible bytes are unchanged (its plan is hand-authored; nothing here touches it)

### R0 exit evidence

- Full suite green (153 tests); guard, capability audit, subject sweep, publication sweep and manifest green at each of the two commits
- The compiled Mathematics products contain no capitalised word directly after a lead-in word, asserted generally across Core1/Core1A/Core1B rather than against the two strings that were found
- Every microtopic figure is the block immediately after the microtopic sharing its obligation; practice-obligation figures still sit with the questions
- `republish.py --write` reports `learner_visible_changes: []` for the Physics run

**~~`--accept-output-change` is passed deliberately and named in the commit message.~~ Retracted: there was nothing to accept.** The plan assumed a committed Mathematics publication whose pages would move. There is none — `Mathematics/` holds a library and gates, and its bucket is compiled to inputs on demand rather than published into the tree. `committed_publications()` finds exactly one run, the Physics one, and its learner-visible bytes are unchanged because its plan is hand-authored and contains no composed joins. So R0.3 has no work in it: the republish that R0.1 already needed, for the runtime snapshot, is the whole of it.

That the flag was never needed is worth more than the flag being used. It means these two composition fixes changed no published page — the only pages they change are the ones the Mathematics compiler will produce the first time that bucket is published.

---

## R1 — Close the specs against the schema

The root cause: role specs were written to the intent, the schema to what existed, and nothing compared them. Three separate findings this session were that one gap.

### R1.1 — The `requires:` block

Each `Shared/roles/<CORE>.md` gains one fenced block at the end. The prose above stays the authority for *meaning*; the block is the authority for *presence*.

````
```requires
question.hints[]                  ladder hints, in the source's original ordering
question.original_identifier      exact source identity, preserved verbatim
question.answer.summary           an answer, for every question held
```
````

Format: one field path per line, path then whitespace then the prose phrase it comes from. A path may end `[]` for an array. Paths resolve against `Shared/library/package.schema.json`, plus (from R5) the run-input schema.

**The honest limit, stated in the module docstring.** This checks block↔schema. It cannot check prose↔block — the prose is prose. A required item that nobody writes into the block is invisible to the gate, and that stays a reviewer's duty. What the gate does buy: once a requirement is in the block, it can never quietly lose its schema home.

### R1.2 — The checker

`Shared/tools/spec_conformance.py`, measuring only at first:

| Finding | Meaning |
|---|---|
| `SPEC_FIELD_ABSENT` | a role spec requires a field the schema has no home for |
| `SPEC_BLOCK_MISSING` | a role spec has no `requires:` block at all |
| `SPEC_PATH_MALFORMED` | a path that does not resolve syntactically |

Run it. The expected first result, from §2 of the roadmap: Core2 `hints[]`; Core2A `hints[]` and `answer.difficult_move`; Core2B `transfer`, `repair_ref`, `rubric[]`; Core1B the elicitation fields R2 defines. Whatever it actually reports is what gets built — the list above is a prediction, and the measurement replaces it.

### R1.3 — Add the fields

```
question
  + hints[]           [{text, reveals: CONCEPT | METHOD | ANSWER}]
  + transfer          {dimension, statement, builds_on[]}          (Core2B)
  + repair_ref        a microtopic teaching-path step id            (Core2B)
  + rubric[]          [{criterion, evidence_of}]                    (Core2B)
  answer
    + difficult_move  index into answer.reasoning[]                (Core2A)
```

Three design decisions, each following the rule the repo already enforces — a field carries the thing or says why not:

- `hints[].reveals` exists so that a hint handing over the answer is detectable. A `reveals: ANSWER` hint before the last position is a finding.
- `answer.difficult_move` is an index, not a copy of the text, so it cannot drift from the step it points at. Out of range is a finding.
- `transfer.dimension` uses the Core2B spec's own four values: `MODEL_CHOICE`, `REPRESENTATION`, `CONTEXT`, `REASONING_LOAD`. The spec says *"a cover story is not a dimension"*; the enum is what makes that enforceable.

All optional at the schema level. A Core2A question has no `transfer`; a question with no hints has an empty array. Absent is legal; **absent and needed** is what the compiler reports.

### R1.4 — Enforce

`spec_conformance.py --enforce` joins `check_subjects.py` and CI, once R1.3 closes what R1.2 found.

### R1 exit evidence

- Every field named in every `requires:` block resolves in the schema
- A planted requirement with no schema home fails the check
- A planted `reveals: ANSWER` hint in a non-final position is a finding
- A `difficult_move` index out of range is a finding
- The committed packages still admit — the new fields are optional and nothing existing is disturbed

---

## R2 — Core1B becomes a self-tutor

The product the intent leans on hardest and currently the thinnest: Core1A plus eight lines, with each prediction answered on the next line.

### R2.1 — What the spec actually requires

`Shared/roles/CORE1B.md` §*Required shape* names a six-step cycle per microtopic. Mapping it against what the library holds today:

| Step | Spec demands | Held today |
|---|---|---|
| 1 Predict | the decision posed before anything is revealed, with a defensible answer | partially — `misconceptions[].diagnostic_prompt` |
| 2 Attempt | what the learner should produce | **nothing** |
| 3 Reconstruct | the correct construction *reached the way a learner would reach it* | no — `teaching_path` is Core1A's expert construction |
| 4 Diagnose | the plausible wrong answer, named, with a question separating it from the right one | yes — `misconceptions[].wrong_idea` + `diagnostic_prompt` |
| 5 Repair | what to do having got it wrong | yes — `misconceptions[].repair` |
| 6 Boundary test | a limiting case or reversal confirming understanding rather than recall | **nothing** |

Two steps have no home, one is borrowed from a product that constructs rather than elicits. That is why Core1B reads as Core1A: three of its six steps are Core1A's.

### R2.2 — Schema

```
microtopic
  + elicitation
      predict        {prompt, defensible_answer}
      attempt        {produces, closure: MODEL_RESPONSE | RUBRIC | CRITERIA}
      reconstruct    {route: [{ask, why_this_ask}], differs_from_teaching_path}
      boundary_test  {prompt, answer}
```

`diagnose` and `repair` are not duplicated — they come from the existing `misconceptions[]`, which already carries exactly those two.

`reconstruct.route` is the load-bearing field and the one that makes the A/B rule enforceable. It is a sequence of *asks*, not of statements: each entry is a question that moves the learner one decision forward, with why that ask rather than a different one. `differs_from_teaching_path` is the author's statement of how the learner's route differs from the expert's — the thing a reviewer checks.

`attempt.closure` implements the spec's *Closure without a tutor*: every prompt closes with a model response, a rubric, or explicit criteria. Three legal answers, no fourth, and no silence.

### R2.3 — Compiler

`compile_inputs.py` gains `_elicitation_blocks(microtopic, obligation)`, and CORE1B stops reusing `_teaching_text`. Emission order is the spec's order:

```
predict prompt        TEXT,  placement TEACHING
attempt instruction   TEXT,  placement TEACHING
reveal                TEXT,  placement ELICITED_REVEAL   ← reconstruct route
diagnose + repair     TEXT,  placement ELICITED_REVEAL   ← from misconceptions[]
boundary test         TEXT,  placement TEACHING
boundary answer       TEXT,  placement ELICITED_REVEAL
```

CORE1A is untouched. Its `_teaching_text` stays exactly as it is, which is also what keeps the A/B comparison meaningful.

### R2.4 — Engine

`placement: ELICITED_REVEAL` is new. Today `inputs.py` knows `TEACHING` and `ANSWER`, and `ANSWER` requires a `question_id` pointing at a QUESTION block — which a microtopic reveal has not got. So:

- `inputs.py`: accept the third value; require it to carry `reveals_block_id` naming the prompt block it answers, and require that block to exist and precede it
- `compose.py`: render it as `<details><summary>` so a self-study reader cannot read straight through

This is a change to subject-neutral engine code and must stay subject-neutral: the guard scans it, and nothing here names a subject.

### R2.5 — The A/B falsifier

The README's rule is *"turning B into A with the nouns changed … fails this rule"*. Made mechanical:

- every Core1B microtopic has ≥1 `ELICITED_REVEAL` block, and each is preceded by the prompt block it names
- no Core1B prompt block's text appears anywhere in the Core1A product — a prompt that is a Core1A sentence is a reveal wearing a question mark
- `reconstruct.differs_from_teaching_path` is non-empty and is not a substring of the teaching path it claims to differ from
- the substance gate already covers the rest: `elicitation` prose is compared against peers like every other field, so a template across microtopics is caught without new code

**The falsifier that matters most:** take the current Core1B, the Core1A-plus-eight-lines one, and require the check to reject it. A gate that would have passed today's product proves nothing.

### R2 exit evidence

- Core1B compiles from `elicitation`, not from `_teaching_text`
- Today's Core1B shape is refused by the A/B check
- A self-study reader cannot see a reveal without opening it — asserted against the rendered HTML, not the plan
- Core1A's composed bytes are unchanged

---

## R3 onward — start-ready only

Deliberately not planned in detail: R1's measurement will change the field list, and R2's reveal mechanism is what R4's hints will reuse.

| Phase | First move | Depends on |
|---|---|---|
| R3 renderers | `FREE_BODY_DIAGRAM` first — 8 of 12 admissible Physics packets need it. Follow the `NUMBER_LINE` pattern exactly: declare required elements, refuse an undeclared frame, digest marks exactly, prove with a library scene instance | R0.2 (placement) |
| R4 banks | `question.difficulty` and `tier` before volume; a bank of one difficulty is not a bank | R1.3 (hints ship with items) |
| R5 routing | `learner_state` as a run input; the schema is in the roadmap §6 | R4 (nothing to route without a bank) |
| R6 JEE | Tier existing gates first; only then author `TRAP` items from the nano-research matrices | R3, R4, R5 |
| R7 authoring contract | `author_bucket.py --scaffold`; the sequence in roadmap §7 is already dependency-ordered | R1–R6 (the contract must describe the finished schema) |
| R8 review | One bucket `CANDIDATE → REVIEWED` on real evidence | R7 (review what an agent produced) |
| R9 Chemistry | Validator module, then `ELEMENT_COUNT_MAP` through `PUBLISHABLE_SHAPES` with its own read-back | R3 (particle + equation renderers) |

---

## Commit sequence

Each line is one commit, green before it lands.

```
R0.1  join() and the two join sites, with falsifiers (three claimed; one was not a site)
R0.2  figure placement interleaved with microtopics
R0.3  (empty -- no committed Mathematics publication exists to republish; folded into R0.1)
R1.1  requires: blocks in all six role specs
R1.2  spec_conformance.py, measuring only; report committed
R1.3  the fields the measurement found
R1.4  enforce in check_subjects and CI
R2.1  elicitation schema
R2.2  ELICITED_REVEAL placement in engine and compose
R2.3  Core1B compiles from elicitation
R2.4  A/B falsifier, including the rejection of today's Core1B
R2.5  author elicitation for the three Mathematics microtopics; republish
```

Twelve commits. R0 is a day's work, R1 two, R2 the largest because it needs authored elicitation content for three microtopics — and that content is the first real test of whether the six-step cycle is writable at grade-9 level, which is a finding either way.

## Risks

| Risk | Handling |
|---|---|
| The `requires:` blocks are written to match the schema that exists, making R1 vacuous | Write each block from the prose alone, before looking at the schema. The predicted findings in R1.2 are recorded here in advance precisely so a suspiciously clean result is visible |
| `elicitation` proves unwritable for some microtopics | That is the spec's own case: *"If a concept is too hard to elicit, that is a design problem to solve, not a licence to drop it."* Record it as a known issue against the microtopic and keep the gate closed |
| R2's engine change breaks the frozen Physics oracle | The Physics plan is hand-authored and declares no `ELICITED_REVEAL`. `republish.py` will report `learner_visible_changes: []` or the step is wrong |
| Twelve commits drift from the roadmap | The roadmap is the strategic document and does not change; this plan is revised when measurement contradicts it, and the contradiction is recorded rather than silently corrected |

## Decisions already taken, not reopened

- Core1 and Core2 are compiled here — settled by the role specs and the library already holding their inputs
- The parallel tracks' packets are candidate input only, per PR #351's own C5 contract
- Chemistry is last
- The #403 survey is not posted; #402's is
