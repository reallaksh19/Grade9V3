# Question → Study Map Benchmark Gap Ledger

This file is the factual ledger produced by the benchmark agent.

The benchmark agent records **what failed or remained ambiguous**. It does not repair the system and does not convert a plausible explanation into a confirmed root cause.

## Gap record format

Use one section per gap:

```markdown
## GAP-QSM-0001 — short title

- Subject:
- Matrix/subtopic:
- Benchmark case:
- Severity: BLOCKER | HIGH | MEDIUM | LOW
- Observed status: FAIL | PARTIAL | BLOCKED_BY_SOURCE
- Expected:
- Observed:
- Reproduction:
- Evidence:
- Affected question/capability/microtopic refs:
- Likely layer: CORE | CONTENT | SOURCE | LEARNER-EVIDENCE | FEEDBACK | RENDERING | UNKNOWN
- Confidence in layer guess: HIGH | MEDIUM | LOW
- Cross-subtopic recurrence: UNKNOWN initially
- Benchmark-agent note:
- Analysis status: UNANALYSED
- Fix status: NOT_STARTED
```

## Rules

- One symptom may create one gap even if several tests expose it.
- If the same symptom appears in another subtopic, append evidence to the existing gap unless the semantics differ materially.
- Missing source information is a gap only when it materially prevents mapping/routing; do not invent the missing source.
- A `NOT_READY` matrix is not automatically a benchmark bug. Record the specific missing teaching/diagnostic/verification behavior that matters.
- Do not write proposed code patches here.
- Do not change `Analysis status` from `UNANALYSED`; that is reserved for the later reverse-engineering phase.

## Pre-benchmark known observations

These are starting observations, not final benchmark conclusions:

- Vector addition/subtraction has unresolved teaching/microtopic coverage.
- Vector representation has incomplete Core1A/Core1B support.
- Gravitation has partial matrix coverage.
- Several Physics matrices are currently `NOT_READY`.
- Figure-dependent external questions must remain unresolved when the figure is unavailable.
- External-provider dependencies can coexist with local feedback when the failed capability is clearly local.

The benchmark sweep should confirm, refine, split or merge these observations based on actual case evidence.

## Benchmark findings

_No benchmark-agent findings recorded yet._