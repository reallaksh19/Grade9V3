# Imported candidates — source, not subject truth

Twelve packets from the parallel Physics track, imported by `Shared/library/import_sil.py`
under the C5 contract: `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY`, `packet_authority: NONE`.

They are **not** a library. Nothing here is compiled, published, or trusted as a claim
about physics. Each `*.v1.json` pins the digest of the packet it came from, so a later
divergence upstream is visible rather than silent, and each `*.gaps.json` names what the
source had no field for.

## What they carry, measured

| | |
|---|---:|
| microtopics | 12 |
| relations | 0 |
| representations | 0 |
| data | 0 |
| questions | 0 |
| capabilities | 0 |

One microtopic per packet and nothing else. 204 named gaps across the twelve:
144 `SIL_FIELD_ABSENT`, 36 `IMPORTER_INFERRED`, 24 `TTU_CANDIDATE_NOT_PROMOTED`.

## What that means for the work downstream

An author opens one of these and closes its gaps, writing the relations, data and
representations the packet has no field for. The importer will not write them: a packet's
TTU scaffolds are candidate input under the C5 mapping rather than exit tasks, and its
misconception cues are repairs with no diagnostic prompt behind them. Filling those in
mechanically would manufacture exactly the plausible-looking teaching this library exists
to keep out.

**These do not unblock a renderer.** A free-body diagram needs forces as data atoms bound
to a relation, and no packet carries either in an importable form. What unblocks
`FREE_BODY_DIAGRAM` is authoring a force bucket with this as candidate input — content
work, not an import.

Moving a file from here into `Physics/library/` is refused by the subject sweep:
`CANDIDATE_IN_LIBRARY`.
