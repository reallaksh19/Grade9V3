#!/usr/bin/env python3
"""A claim about a learner must be backed by what was seen, or say it is a waiver.

Profiles live outside every subject. They were inside packages, which meant the same
learner studying a second bucket needed a duplicate -- and capabilities cross subjects,
so a profile keyed to one package can never answer whether a prerequisite is held.

The rule this exists for: the role specs forbid inferring mastery of a prerequisite from
a high aggregate score. So an entry rung is selected from the per-capability map or from
an owner's recorded decision, and never from a percentage. `knowledge_percentage` is a
summary the system stores and never computes from.

  DIAGNOSTIC      every DEMONSTRATED capability needs an observation that says so
  OWNER_ESTIMATE  a waiver, because the number is a decision rather than a measurement
  UNKNOWN         a waiver, and nothing downstream may claim personalised fit
  SYNTHETIC_TEST  the only value an agent may write, and never routed

`measured_fit_claim` stays false unless independently established. A successfully
generated book is not evidence of fit.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import load  # noqa: E402

# Derived from the repo passed in, not from the module's own location. Baking REPO into
# these made audit(root) silently read the real tree while claiming to read the argument
# -- so a planted profile was never seen and the gate reported clean.
PROFILES = "Learners/profiles"
OBSERVATIONS = "Learners/observations"
NEEDS_WAIVER = {"OWNER_ESTIMATE", "UNKNOWN"}


def capabilities(repo: Path = REPO) -> set[str]:
    return {cap["id"] for path in sorted(repo.glob("*/library/*.json"))
            if path.name != "package.schema.json"
            for cap in load(path).get("capabilities", [])}


def referenced_profiles(repo: Path = REPO) -> dict[str, list[str]]:
    """Every practice_profile_ref in the libraries, and who made it."""
    found: dict[str, list[str]] = {}
    for path in sorted(repo.glob("*/library/*.json")):
        if path.name == "package.schema.json":
            continue
        for route in load(path).get("teaching_routes", []):
            ref = route.get("practice_profile_ref")
            if ref:
                found.setdefault(ref, []).append(f'{path.name}:{route["id"]}')
    return found


def audit(repo: Path = REPO) -> dict:
    declared = capabilities(repo)
    observed, kept = repo / OBSERVATIONS, repo / PROFILES
    observations = {load(p)["observation_id"]: load(p)
                    for p in sorted(observed.glob("*.json"))} if observed.exists() else {}
    profiles = {load(p)["profile_id"]: load(p)
                for p in sorted(kept.glob("*.json"))} if kept.exists() else {}
    findings: list[dict] = []

    def fail(point: str, who: str, detail: str):
        findings.append({"point": point, "profile": who, "detail": detail})

    for pid, profile in sorted(profiles.items()):
        provenance = profile["provenance"]
        for cap in profile.get("held", {}):
            if cap not in declared:
                fail("HELD_CAPABILITY_UNKNOWN", pid,
                     f"claims a state for {cap}, which no subject declares")
        if provenance in NEEDS_WAIVER and not profile.get("owner_waiver"):
            fail("CLAIM_WITHOUT_EVIDENCE_OR_WAIVER", pid,
                 f"{provenance} is not a measurement, so it needs the owner instruction it "
                 "is following instead")
        if provenance == "DIAGNOSTIC":
            seen = {observations[ref]["capability_ref"] for ref in profile.get("observation_refs", [])
                    if ref in observations}
            for cap, state in profile.get("held", {}).items():
                if state == "DEMONSTRATED" and cap not in seen:
                    fail("DEMONSTRATED_WITHOUT_AN_OBSERVATION", pid,
                         f"says {cap} is demonstrated and no observation records it")
        for ref in profile.get("observation_refs", []):
            if ref not in observations:
                fail("OBSERVATION_REF_DANGLING", pid, f"names {ref}, which does not exist")
        if profile.get("measured_fit_claim") and provenance != "DIAGNOSTIC":
            fail("FIT_CLAIMED_WITHOUT_DIAGNOSIS", pid,
                 f"claims measured fit on {provenance} evidence")

    for ref, users in sorted(referenced_profiles(repo).items()):
        if ref not in profiles:
            fail("PROFILE_REF_DANGLING", ref,
                 f'referenced by {", ".join(users)} and no profile holds that id')
        elif profiles[ref]["provenance"] == "SYNTHETIC_TEST":
            fail("SYNTHETIC_PROFILE_ROUTED", ref,
                 f'referenced by {", ".join(users)}; a synthetic profile is never routed')

    return {"profiles": len(profiles), "observations": len(observations),
            "findings": findings, "passed": not findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.enforce and not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
