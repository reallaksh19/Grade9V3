# Sweep method

This sweep evaluates the 17-matrix snapshot frozen at `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`.

## Evidence used

For each matrix the benchmark agent inspects:

1. its canonical matrix/rung file;
2. its canonical subject library package;
3. the current session-readiness snapshot;
4. the existing Shared routing/evidence/feedback contracts and their repository tests;
5. retained real external-question fixtures only where such evidence already exists.

The frozen commit passed the repository guardrails on GitHub Actions. The benchmark does not treat a green unit suite as proof that every matrix is useful; matrix-specific observations are recorded separately in each pack.

## No fabricated learner episode

Cases such as unknown learner, rough estimate, helped success and independent success are contract/synthetic-falsifier checks. They verify what the current routing/evidence contract permits. They do not claim that the real learner performed such an attempt.

## Status interpretation

- **PASS** — the current frozen repository supports the expected semantic behavior for the case.
- **PARTIAL** — part of the behavior is represented, but a real usability/evidence gap remains.
- **FAIL** — the observed behavior contradicts the expected semantic behavior.
- **BLOCKED_BY_SOURCE** — source information needed to evaluate the case is absent.
- **NOT_APPLICABLE** — no genuine case exists in the frozen subtopic; none is manufactured.

A matrix may correctly expose a content gap while still receiving PARTIAL overall because the learner cannot obtain a complete usable route. Honesty about the gap is good behavior; the missing teaching remains a benchmark finding.

## Repair prohibition

No production fix is made in this sweep. All material non-pass findings are recorded in `GAPS.md` with `Analysis status: UNANALYSED` and `Fix status: NOT_STARTED`.
