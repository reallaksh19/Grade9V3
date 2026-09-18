# Owner decision application

The planner may ask the owner for a small number of decisions that the repository cannot
derive. Those answers must not be applied by ad-hoc request editing.

This layer turns owner answers into a typed, stale-detectable artifact and immediately
re-plans the request after applying them.

## Closed loop

```text
short request
   ↓
plan_request.py
   ↓
required_owner_inputs
   ↓
owner-decisions.json
   ↓
apply_owner_decisions.py
   ↓
patched request
   ↓
re-plan immediately
   ↓
next owner inputs / agent actions / execution packet
```

The owner-decision artifact pins both:

- the request digest; and
- the full planner-result digest.

If either the request or the architecture changes after the artifact was prepared, the
decision is rejected as stale.

## Supported decisions

The current typed contract covers every owner input the planner can emit:

- `LEARNER_ENTRY`
- `CORE2A_PURPOSE`
- `CORE2B_PURPOSE`
- `SOURCE_BASIS`
- `SOURCE_BASIS_DRIFT_DECISION`
- `SUPPLEMENTAL_QUESTION_POLICY`

CI scans every committed plan fixture and fails if the planner introduces a new
`required_owner_input` with no typed decision field.

## Incremental answers are legal

The owner does not need to answer every question at once.

A decision artifact may answer only a subset of the currently requested owner inputs. The
applier then re-plans and returns the remaining owner questions.

This matters because source decisions are sequential:

```text
SOURCE_BASIS_DRIFT_DECISION
        ↓
keep supplied source
        ↓
SUPPLEMENTAL_QUESTION_POLICY may become relevant
```

The second question must not be asked before the first one is resolved.

## Source-basis drift

When a verified receipt reports `DRIFT`, the planner offers:

```text
KEEP_SUPPLIED_DESPITE_DRIFT
or
CHANGE_SOURCE_BASIS:<receipt-backed replacement candidate>
```

### Keep supplied

The applier records the drift acknowledgement and leaves the original receipt pinned.
Re-planning then evaluates that source exactly as it currently exists. If practice coverage
is insufficient, the supplemental-question policy may become the next owner decision.

### Change source basis

The replacement must be one of the verified receipt's `replacement_candidates`. An
arbitrary locator is rejected.

Changing the basis automatically clears:

- the old `source_receipt_ref`;
- the drift acknowledgement;
- any `supplemental_question_policy` derived from the old source's gap.

The re-planned request therefore returns to:

```text
INSPECT_AND_INGEST_SOURCE_BASIS
```

No evidence or policy from the old source silently survives the replacement.

## Learner entry

The owner may provide a learner profile ref, an explicit rung, an owner knowledge estimate,
or explicit `unknown`.

`unknown` is a real resolved owner answer. It stops the system from repeatedly asking the
same question, but learner-routed products remain blocked because no reachability evidence
exists.

```text
owner answered
!=
learner route is reachable
```

## Unsolicited decisions

The applier accepts only decisions that the pinned planner result actually requested.

For example, while source drift is unresolved the owner cannot pre-apply
`SUPPLEMENTAL_QUESTION_POLICY`. That policy belongs to a later planning state and may
become irrelevant if the source basis changes.

## Commands

Generate a fillable decision template:

```text
python3 Shared/tools/apply_owner_decisions.py --request Requests/example.plan-request.json --template
```

Apply decisions and re-plan:

```text
python3 Shared/tools/apply_owner_decisions.py --request Requests/example.plan-request.json --decisions /path/to/owner-decisions.json
```

Audit the planner/applier contract:

```text
python3 Shared/tools/apply_owner_decisions.py --audit --enforce
```

Behavioral falsifiers live in `tests/test_owner_decisions.py`.
