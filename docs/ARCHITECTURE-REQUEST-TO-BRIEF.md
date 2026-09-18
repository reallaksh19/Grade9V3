# From one request to every binding brief

The chain that answers *"create Core1A, 1B, 2A and 2B for Motion in 2D › relative
motion"* — and the three inputs it needs that nothing previously asked for.

```
Requests/<slug>.request.json          what a person asks for
        │  resolve_request.py --plan
        ▼
build plan                            entry rung · ladder segment · per-core state
        │  resolve_request.py --briefs
        ▼
author_brief.py × N                   one brief per rung, plus one per practice core
        ▼
the records an author writes          checked by every gate below
```

## The three inputs

| input | decides | why it cannot be defaulted |
|---|---|---|
| **learner** | the **entry rung** | placement is the only thing a knowledge input may change |
| **purpose of Core2A** | its support level | support is not a percentage; the purpose carries it |
| **purpose of Core2B** | support, **and whether transfer is routed at all** | `STARTER` withholds it, with its own recorded reason |

The practice cores need **no knowledge number**. A purpose already declares its support
level. Support and placement had been one number doing two jobs.

## Where the entry rung comes from — exactly one of three

The schema's `oneOf` makes this structural rather than advisory, because the failure it
prevents is silent: a percentage typed into a field and then read as evidence.

```yaml
learner:
  profile_ref: PROFILE-…              # the per-capability map decides
# or
  owner_entry:                        # an owner names the rung outright
    rung: R4
    by: …
    instruction: …
# or
  owner_estimate:                     # the percentage, recorded as the decision it is
    knowledge_percentage: 20
    by: …
    instruction: …
```

`knowledge_percentage` is stored and never computed from. From a **profile**, placement is
the lowest rung whose capability is not `DEMONSTRATED` — read from the map, never from the
profile's own summary number.

### The refusal that matters most

```
ENTRY_UNDECIDABLE_FROM_THE_PROFILE   R1 has no record, so it declares no capability
                                     to observe; nobody can be placed against it
```

Relative motion's ladder starts at `R1`, which is `ABSENT`. So **no learner can currently
be placed on it from a diagnostic** — not because the diagnostic is weak, but because the
library has nothing at the bottom to have observed. That is a fact about the library,
reported instead of defaulting to the bottom rung and looking like an answer.

## Selection, never dilution

A higher entry teaches **fewer** rungs, never shallower ones. Tested directly: the segment
at 70 is a suffix of the segment at 20, and every rung's task is identical in both plans.

| entry | segment | Core1A |
|---|---|---|
| 20 → `R1` | `R1 R3 R4 R5` | `R1` is rung work; `R3 R4 R5` are product work |
| 70 → `R4` | `R4 R5` | both product work |

A position between rungs is a hole, not a depth to interpolate:
`ENTRY_POSITION_BETWEEN_RUNGS`.

## The worked example

`Requests/relative-motion-g9.request.json` — Core1A, 1B, 2A, 2B; owner estimate 20;
`PRACTICE` for 2A, `COMPETITION` for 2B.

```
$ python3 Shared/tools/resolve_request.py --plan Requests/relative-motion-g9.request.json

  entry rung  R1   selected by LADDER_POSITION   provenance OWNER_ESTIMATE

  CORE1A -- READY          CORE2A -- READY
    R1  ABSENT   AUTHOR_THE_RUNG          purpose      PRACTICE
    R3  PRESENT  AUTHOR_THE_PRODUCT       support      medium
    R4  PRESENT  AUTHOR_THE_PRODUCT       handed over  The observer is named and
    R5  PRESENT  AUTHOR_THE_PRODUCT                    the axes are declared.
                                        CORE2B -- READY
  CORE1B -- READY                          purpose      COMPETITION
    (the same four rungs)                  support      minimum
                                           transfer     4 rows available
```

`--briefs` on the same file compiles all ten briefs — eight rung briefs plus one per
practice core — in build order.

## What each finding means

| finding | what was asked for |
|---|---|
| `REQUEST_STRUCTURE` | a bare percentage, or two sources of placement at once |
| `REQUEST_BUCKET_HAS_NO_MATRIX` | a subtopic with no ladder to place anyone on |
| `PROFILE_REF_DANGLING` · `SYNTHETIC_PROFILE_ROUTED` | a learner who is not there, or a fixture |
| `ENTRY_UNDECIDABLE_FROM_THE_PROFILE` | placement against a rung that declares no capability |
| `ENTRY_RUNG_NOT_ON_THE_LADDER` · `ENTRY_POSITION_BETWEEN_RUNGS` | an entry the ladder does not have |
| `PRACTICE_CORE_WITHOUT_A_PURPOSE` | practice with no stated purpose — there is no default that is not a guess |
| `PURPOSE_UNKNOWN` · `PURPOSE_FOR_A_CORE_NOT_REQUESTED` | a purpose outside the vocabulary, or for a product nobody asked for |
| `TRANSFER_REQUESTED_UNDER_A_PURPOSE_THAT_WITHHOLDS_IT` | Core2B under `STARTER` |

A withheld product is not a failure: it reports `WITHHELD` and carries the vocabulary's
own `reason_when_withheld`, which is distinguishable from a product that simply could not
be built.

## What this does not do

It plans and refuses. It authors nothing, and it reaches no learner. The records an author
writes from these briefs still face every gate below — which is the point: the request
layer decides *what to build*, and the gates still decide *whether it is real*.
