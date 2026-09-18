# Re-benchmark run 4700abde

Production baseline: `4700abdefecefd6211488a527594dabba8797e89`

This is the complete 17-matrix rerun after the fallback-first execution chain:

- PR #60 — fallback-first session execution with owner decisions;
- PR #61 — owner-decision propagation through prerequisite branches;
- PR #62 — separate fallback teaching from mastery evidence.

The original benchmark packs under `benchmarks/question-study-map/cases/**` remain historical evidence and are not rewritten.

Each matrix receives one `rerun.yaml` containing the existing 15 semantic case dispositions plus the cross-cutting runtime semantics that were changed by #60–#62.

No production files are modified by this run.
