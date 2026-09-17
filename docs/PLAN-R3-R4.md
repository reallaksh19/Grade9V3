# Execution plan: R3 and R4

Written after R0–R2 landed, and after two measurements that reorder what the roadmap said to do next. The roadmap's R3 list was drawn up before R1's schema work and before R3.0's depiction audit; both changed what is buildable.

## Two findings that reorder the batch

### The roadmap's first renderer cannot be built honestly

R3 says `FREE_BODY_DIAGRAM` first, and states the rule every renderer follows: *proven by a scene instance compiled from a library record — never by a hand-authored plan.*

Physics' library holds no force content. `force`, `newton`, `friction` and `normal` return zero hits; the 72 hits for `tension` are all the word `extensions`. A `FREE_BODY_DIAGRAM` built now could only be proven against a fixture, which that rule forbids. It is blocked on content, not on effort, and moves behind the import.

`VECTOR_SUBTRACTION` takes its place. Two library representations declare it, in a bucket that compiles, with three `FIGURE_AUTHORING` requirements pointing at it — and R3's own exit evidence is *"`FIGURE_AUTHORING` count for Physics drops from three to zero"*, which only this renderer can achieve.

### Nothing checked that a product delivers what its spec requires

R1 compared each `requires` block against the schema and closed 68 findings. That comparison proves a requirement *can* be held. It says nothing about whether anything holds it, or whether the compiler carries it to a page.

`Shared/tools/spec_delivery.py` is that third comparison. Measuring only.

## R1.5 — measured

**94 undelivered requirements**, from 186 checked across two subjects.

| State | Count | Meaning |
|---|---:|---|
| `DELIVERED` | 65 | the authored value appears in the compiled product |
| `UNAUTHORED` | 58 | the library holds nothing at this path |
| `NOT_DELIVERED` | 36 | held, and no compiled product carries it |
| `UNDECIDABLE` | 25 | held, but every value is too short to search for without matching by accident |
| `NOT_COMPILED_HERE` | 2 | Core2B, which compiles no product for either bucket |

`UNDECIDABLE` is reported as itself rather than guessed. A false `DELIVERED` is worse than an admitted gap, and an enum or an id fragment can appear in compiled output by coincidence.

### The 36, adjudicated

**Real product defects — content a role requires and a learner never sees:**

- **`CORE1A` emits no misconceptions at all.** `_teaching_text` emits them only for Core1B. Core1A's spec asks for *"the plausible wrong path, named, with a diagnostic that would expose it and the repair that fixes it"* and then says, in words, *"A misconception the learner never hears is a misconception they keep."* Three paths, both subjects. This is the sharpest finding in the batch.
- **`CORE1A` carries no `relation.checks[]`** — *"checks the learner can run alone"*.
- **`CORE1A` carries no `entry_assumptions[]`** — *"the entry capability assumed"*, named first in its required content.
- **`CORE1A` carries no `correspondence[]`** — the representation bridge authored in R3.0 reaches nobody. The figure is emitted; what binds it to the mathematics is not.
- **`CORE1A` carries no worked examples** (`question.answer.reasoning[]` via a Core1A exposure).
- **`CORE1` carries no `datum.value`.** It prints each quantity's meaning and unit and omits the number. Its spec asks for *"the worked anchor values, if the bucket has one, stated compactly"*.
- **`CORE2`/`CORE2A` substitute `"LIBRARY"` for the question's `source_refs`**, and carry no `figure_refs[]`. Core2's spec requires source identity *"preserved verbatim"* and that *"figures and their captions survive"*.
- **`question.hints[]` is `UNAUTHORED` everywhere and `_question_block` hardcodes `"hints": []`.** Both halves are broken, so fixing either alone delivers nothing.

**Author-facing by design — held for a reviewer, not for a learner:**

- `elicitation.reconstruct.route[].why_this_ask` — printing "why I asked you this" to a learner defeats the ask.
- `elicitation.reconstruct.differs_from_teaching_path` — the sentence a reviewer checks the A/B claim against.
- `resource.access_status`, `microtopic.research_contribution` — arguable, and argued in R1.6 rather than assumed here.

The `requires` block cannot currently say this. R1.6 gives it a marker, so that "not for the learner" is a claim a reviewer can dispute rather than a silence the tool has to guess at.

**Delivered in transformed form — the check cannot see it:**

- `relation.expression` reaches Core1 as MathML, which is the typeset form of the same expression.
- `question.exposure[].role` is mapped through a translation table into `exposure_role`.
- `elicitation.attempt.closure` is delivered as its content rather than its enum name.

Stated as a limit of the tool, not excused: it looks for the authored value in the compiled output rather than mapping library paths onto block fields. A mapping would need updating whenever the compiler changes shape, by whoever changed it, which is the arrangement this whole layer exists to avoid.

## The batch, in dependency order

| Step | Work | Blocked by |
|---|---|---|
| R1.5 | the delivery gate, measuring only | — |
| R3.1 | `VECTOR_SUBTRACTION` renderer; `FIGURE_AUTHORING` 3 → 0 | — |
| R1.6 | mark author-facing paths, fix the compiler defects, enforce | R1.5 |
| R3.2 | Core1's canonical-figure slot | R3.1 |
| R3.3 | renderer priority by evidence rather than list order | — |
| R4.0 | import the 12 admissible Physics packets | — |
| R3.4 | `FREE_BODY_DIAGRAM` | R4.0 |

R3.3's exit condition is that its report independently names `VECTOR_SUBTRACTION` as highest-value and `FREE_BODY_DIAGRAM` as zero-value until R4.0 lands — reproducing what had to be measured by hand to write this document.
