# What is pending before a production stress test

Measured, not remembered. Every number below came from a command run against the tree at
this commit.

---

## 0 · What a stress test has to be able to push on

A stress test is only worth running on axes the system can actually be pushed along. Six
products, four inputs, one review path:

| axis | exercised by | can it be pushed today |
|---|---|---|
| declarative teaching | Core1A over many buckets | **yes** — 13 of 14 |
| elicited teaching | Core1B, prompt before reveal | **yes** — 13 of 14 |
| the map | Core1, relations and the canonical figure | barely — 2 of 14 |
| source custody | Core2, question corpus | barely — 1 of 14 |
| supported practice | Core2A, support ladder, routing | barely — 1 of 14 |
| **transfer** | Core2B, changed demand, withheld information | **no — produced 0 times, ever** |
| placement | a learner profile with observations | **no** — 2 profiles, both unroutable, 0 observations |
| review | `promote.py`, `CANDIDATE → REVIEWED` | **no** — 120 of 120 records are `CANDIDATE` |
| pictures | scene instances rendered into a page | barely — 3 scenes, all in 2 buckets |

Four of the nine cannot be pushed at all. A stress run today would exercise two products
deeply and seven shallowly, and would report that as success.

---

## 1 · Measured state

```
buckets            14        microtopics        46        records      120 (all CANDIDATE)
rungs              68        with a record      42        equation-blocked   26
relations           3        questions           1        data          22
representations     3        scene instances     3        teaching routes    27
gate relations      6  — covering 2 of 14 buckets
learner profiles    2  — provenance UNKNOWN, 0 observations, neither routable
publications        2  — one LIBRARY, one AUTHORED_OUTSIDE_THE_LIBRARY
```

Per bucket, everything except teaching is empty:

| | buckets holding any |
|---|---:|
| microtopics + teaching routes | **14** |
| relations | 2 |
| questions | 1 |
| data | 6 |
| representations / figures | 2 |

**The root cause is one sentence.** Twelve of fourteen buckets carry teaching and nothing
else — no relation, no question, no datum, no figure. Every missing product downstream is
that fact restated: Core1 needs a governing relation, Core2 and Core2A need a question,
Core2B needs a question exposed to it, a figure needs a scene instance.

---

## 2 · Pending work, in dependency order

Each item names its owner, what it unlocks, and the evidence that closes it.

### P0 · Two layers disagree about whether a product can be built — **mine, small**

`resolve_request` reports `CORE2B: READY` for relative motion. `compile_inputs` refuses to
build it: *"the library holds no question exposed to this product"*. Both answer "can this
be built?" and they answer differently, so a stress run would be told a product is ready
and then find nothing.

The plan layer reads the matrix (transfer rows exist, ladder is taught); the compiler reads
the library (no exposed question). The plan must consult what the compiler consults.

**Exit:** a request's per-core state agrees with the compiler's supported set for every
bucket, and a test asserts the agreement rather than either number.

### P1 · One transfer question, so Core2B exists once — **mine, small, highest value per hour**

Core2B has never been produced. It is the only product of the six with no instance
anywhere, so every claim made about transfer — the changed demand, the withheld
information, the repair route, the rubric — is untested end to end.

Relative motion already has four authored `transfer` rows in its matrix, each with a
dimension, a changed demand, what is not handed over and a repair rung. One question
authored against one of those rows closes it.

**Exit:** a published Core2B; the exposure audit accepts the transfer claim; no hint
discloses that row's `information_not_handed_over`.

### P2 · Gate registry for the twelve subtopics — **mine, large, not offloadable**

26 rungs are equation-blocked and 12 buckets cannot produce Core1, both because Physics
declares six gate relations and all six belong to the two original buckets.

This is the layer every other gate defers to: a wrong validity condition propagates and
nothing below can catch it. It is also now falsifiable — a declared falsification case is
bound to a mutation that runs, and a representation's labels must cover what the subject
contract requires.

**Exit:** each subtopic's governing relations in the registry with symbols, conditions and
falsification cases that execute; `authority.py` accepts library copies bound to them;
Core1 compiles for those buckets.

### P3 · Data and questions per bucket — **offloadable, twelve tasks**

With P2 done, each bucket needs `data[]` with oracle-bindable values and `questions[]` with
hints, difficulty, tier and family. That is what turns Core2, Core2A and Core2B from one
bucket into twelve.

**Exit:** every bucket compiles all six products or names which it cannot and why.

### P4 · A learner who can be placed — **mine, small**

`Learners/observations/` does not exist. Both profiles are `provenance: UNKNOWN` with zero
observations, so `learner_evidence` refuses to route either, and placement from a diagnostic
has never run against real evidence.

**Exit:** one observation record per demonstrated capability on one profile; the request
layer places that learner at a rung from the map rather than from a percentage.

### P5 · Figures — **mine for the renderers, offloadable for the scenes**

Three scene instances exist, in two buckets. Eight declared representation kinds have no
renderer. The intent is "pictorial and self-explanatory"; today eleven buckets publish
prose only.

**Exit:** `FREE_BODY_DIAGRAM` built and proven by a scene compiled from a library record —
the Newton bucket is now authored, which is what it was waiting for.

### P6 · Review — **owner, not an agent**

`promote.py` is implemented and has never promoted anything. 120 records are `CANDIDATE`.
Nothing here is study material until a person says the physics is right; the gates check
structure and cannot check truth.

**Exit:** one bucket at `REVIEWED` on real review evidence from a named reviewer.

### P7 · The reported-not-enforced backlog — **mixed**

| | count | owner |
|---|---:|---|
| ceiling words in an authored explanation | 7 | the rungs' authors |
| microtopics no teaching route claims | 4 | those buckets' authors |
| capability forks with an untaught discrimination | 4 over 2 stems | owner decision |
| role-spec rows nothing has authored yet | 31 | follows P3 |

Each is reported by name and none fails the build, which is correct while they are content
decisions. They stop being acceptable once the thing they describe is published to a
learner.

---

## 3 · The minimum bar to start, versus the full bar

**Minimum to run a stress test worth believing: P0, P1, P4.** Together they make all six
products producible at least once and one learner placeable from evidence. That is enough
for the run to exercise every axis rather than two.

**Full bar, for a production-scale run: P2 and P3**, which take the exercised set from one
bucket to twelve. P5 and P6 are quality, not capability — the run would work without them
and would honestly report prose-only pages and unreviewed content.

---

## 4 · What the stress test then runs

Once P0, P1 and P4 hold, the run is:

1. Every bucket × every product, compiled and published — what refuses, and does it say why.
2. Every bucket × three purposes × three learner states through the request layer — 126
   plans, checking each per-core state against what the compiler actually produces.
3. Adversarial records: malformed at every layer, checking that each tool reports rather
   than raises. The last sweep found 7 of 18 malformed matrices produced a traceback.
4. The learner-facing pages read, not just exit-coded. Three of the six defects found so far
   were invisible to every gate and visible on the page.
5. Each reported-not-enforced count re-measured, so the backlog is a number that moves.

---

## 5 · What this plan does not claim

It does not claim the content is correct. Every record is `CANDIDATE`, no reviewer has
looked at any of it, and the gates check that a claim is backed — never that it is true.
P6 is where that changes, and nothing before it substitutes.
