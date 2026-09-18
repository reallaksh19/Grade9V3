"""Practical learner evidence stays small, deterministic and conservative."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import import_study_observations, learner_evidence, plan_request  # noqa: E402
from Shared.tools import capability_graph, resolve_request  # noqa: E402


class PracticalLearnerEvidence(unittest.TestCase):
    def temp_root(self):
        return tempfile.TemporaryDirectory()

    def write_observation(self, root: Path, observation: dict):
        path = root / "Learners/observations"
        path.mkdir(parents=True, exist_ok=True)
        (path / f'{observation["observation_id"]}.json').write_text(
            json.dumps(observation), encoding="utf-8"
        )

    def test_direct_attempt_beats_prior_imported_evidence(self):
        with self.temp_root() as tmp:
            root = Path(tmp)
            prior = {
                "observation_id": "OBS-PRIOR",
                "capability_ref": "CAP-X",
                "method": "old diagnostic",
                "evidence_kind": "PRIOR_DIAGNOSTIC",
                "observed": "Solved correctly.",
                "result": "DEMONSTRATED",
                "when": "2026-09-18",
                "help": "NONE",
            }
            direct = {
                "observation_id": "OBS-DIRECT",
                "capability_ref": "CAP-X",
                "method": "current attempt",
                "evidence_kind": "DIRECT_ATTEMPT",
                "observed": "Could not set up the relation.",
                "result": "MISSING",
                "when": "2026-09-17",
                "help": "NONE",
            }
            self.write_observation(root, prior)
            self.write_observation(root, direct)
            profile = {
                "observation_refs": ["OBS-PRIOR", "OBS-DIRECT"],
                "held": {"CAP-X": "DEMONSTRATED"},
                "provenance": "DIAGNOSTIC",
            }
            state = learner_evidence.effective_state(profile, "CAP-X", root)
            self.assertEqual(state["state"], "MISSING")
            self.assertEqual(state["source"], "DIRECT_ATTEMPT")
            self.assertEqual(state["observation_ref"], "OBS-DIRECT")

    def test_newer_observation_wins_within_the_same_evidence_kind(self):
        with self.temp_root() as tmp:
            root = Path(tmp)
            for oid, when, result in [
                ("OBS-OLD", "2026-09-10", "MISSING"),
                ("OBS-NEW", "2026-09-18", "DEMONSTRATED"),
            ]:
                self.write_observation(root, {
                    "observation_id": oid,
                    "capability_ref": "CAP-X",
                    "method": "direct attempt",
                    "evidence_kind": "DIRECT_ATTEMPT",
                    "observed": result,
                    "result": result,
                    "when": when,
                    "help": "NONE",
                })
            profile = {
                "observation_refs": ["OBS-OLD", "OBS-NEW"],
                "held": {},
                "provenance": "DIAGNOSTIC",
            }
            self.assertEqual(
                learner_evidence.effective_state(profile, "CAP-X", root)["state"],
                "DEMONSTRATED",
            )

    def test_helped_success_is_not_independent_demonstration(self):
        with self.temp_root() as tmp:
            root = Path(tmp)
            self.write_observation(root, {
                "observation_id": "OBS-HINTED",
                "capability_ref": "CAP-X",
                "method": "retry after hint",
                "evidence_kind": "DIRECT_ATTEMPT",
                "observed": "Solved after a structural hint.",
                "result": "DEMONSTRATED",
                "when": "2026-09-18",
                "help": "HINT",
            })
            profile = {
                "observation_refs": ["OBS-HINTED"],
                "held": {},
                "provenance": "DIAGNOSTIC",
            }
            self.assertEqual(
                learner_evidence.effective_state(profile, "CAP-X", root)["state"],
                "UNCERTAIN",
            )

    def test_observation_overrides_profile_snapshot_for_routing(self):
        with self.temp_root() as tmp:
            root = Path(tmp)
            self.write_observation(root, {
                "observation_id": "OBS-NOW",
                "capability_ref": "CAP-X",
                "method": "current attempt",
                "evidence_kind": "DIRECT_ATTEMPT",
                "observed": "Solved independently.",
                "result": "DEMONSTRATED",
                "when": "2026-09-18",
                "help": "NONE",
            })
            profile = {
                "observation_refs": ["OBS-NOW"],
                "held": {"CAP-X": "MISSING"},
                "provenance": "DIAGNOSTIC",
            }
            self.assertEqual(
                learner_evidence.effective_held(profile, root),
                {"CAP-X": "DEMONSTRATED"},
            )

    def test_prior_study_map_converts_to_normal_observations(self):
        payload = {
            "study_map_id": "PT-2",
            "rows": [{
                "question_ref": "Q13",
                "capability_ref": "CAP-X",
                "observed": "Delta-y / delta-x roles unstable.",
                "suggested_state": "UNCERTAIN",
            }],
        }
        rows = import_study_observations.convert(payload, "2026-09-18")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["evidence_kind"], "PRIOR_STUDY_MAP")
        self.assertEqual(rows[0]["question_ref"], "Q13")
        self.assertEqual(rows[0]["session_ref"], "PT-2")
        self.assertEqual(rows[0]["result"], "UNCERTAIN")
        self.assertEqual(rows[0]["help"], "UNKNOWN")

    def test_prior_study_map_can_derive_a_single_mapped_capability(self):
        payload = {
            "study_map_id": "PT-3",
            "rows": [{
                "question_ref": "Q1",
                "observed": "Could not state what changes.",
                "suggested_state": "MISSING",
            }],
        }
        worksheet_map = {
            "worksheet_id": "WS-1",
            "subject": "Physics",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-ONLY",
                "secondary_capability_refs": [],
                "mapping_basis": "MANUAL",
            }],
        }
        rows = import_study_observations.convert(
            payload, "2026-09-18", worksheet_map
        )
        self.assertEqual(rows[0]["capability_ref"], "CAP-ONLY")
        self.assertEqual(rows[0]["question_ref"], "Q1")

    def test_prior_study_map_refuses_to_guess_between_multiple_question_capabilities(self):
        payload = {
            "study_map_id": "PT-4",
            "rows": [{
                "question_ref": "Q1",
                "observed": "The solution broke somewhere.",
                "suggested_state": "UNCERTAIN",
            }],
        }
        worksheet_map = {
            "worksheet_id": "WS-2",
            "subject": "Mathematics",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-A",
                "secondary_capability_refs": ["CAP-B"],
                "mapping_basis": "MANUAL",
            }],
        }
        with self.assertRaisesRegex(ValueError, "multiple capabilities"):
            import_study_observations.convert(
                payload, "2026-09-18", worksheet_map
            )

    def test_prior_study_map_explicit_capability_must_agree_with_question_mapping(self):
        payload = {
            "study_map_id": "PT-5",
            "rows": [{
                "question_ref": "Q1",
                "capability_ref": "CAP-C",
                "observed": "A specific misconception was noted.",
                "suggested_state": "MISSING",
            }],
        }
        worksheet_map = {
            "worksheet_id": "WS-3",
            "subject": "Mathematics",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-A",
                "secondary_capability_refs": ["CAP-B"],
                "mapping_basis": "MANUAL",
            }],
        }
        with self.assertRaisesRegex(ValueError, "not among the mapped capabilities"):
            import_study_observations.convert(
                payload, "2026-09-18", worksheet_map
            )

    def test_prior_study_map_can_disambiguate_a_multi_capability_question_explicitly(self):
        payload = {
            "study_map_id": "PT-6",
            "rows": [{
                "question_ref": "Q1",
                "capability_ref": "CAP-B",
                "observed": "Secondary skill was the observed weakness.",
                "suggested_state": "MISSING",
            }],
        }
        worksheet_map = {
            "worksheet_id": "WS-4",
            "subject": "Mathematics",
            "questions": [{
                "question_id": "Q1",
                "primary_capability_ref": "CAP-A",
                "secondary_capability_refs": ["CAP-B"],
                "mapping_basis": "MANUAL",
            }],
        }
        rows = import_study_observations.convert(
            payload, "2026-09-18", worksheet_map
        )
        self.assertEqual(rows[0]["capability_ref"], "CAP-B")

    def test_diagnostic_profile_cannot_claim_demonstrated_from_solution_help(self):
        with self.temp_root() as tmp:
            root = Path(tmp)
            schema_dir = root / "Shared/library"
            schema_dir.mkdir(parents=True)
            shutil.copy(
                REPO / "Shared/library/observation.schema.json",
                schema_dir / "observation.schema.json",
            )
            library = root / "Example/library"
            library.mkdir(parents=True)
            (library / "example.v1.json").write_text(json.dumps({
                "capabilities": [{"id": "CAP-X"}]
            }), encoding="utf-8")
            self.write_observation(root, {
                "observation_id": "OBS-SOLUTION",
                "capability_ref": "CAP-X",
                "method": "after reading solution",
                "evidence_kind": "DIRECT_ATTEMPT",
                "observed": "Repeated the shown method.",
                "result": "DEMONSTRATED",
                "when": "2026-09-18",
                "help": "SOLUTION",
            })
            profiles = root / "Learners/profiles"
            profiles.mkdir(parents=True)
            (profiles / "p.json").write_text(json.dumps({
                "profile_id": "P",
                "provenance": "DIAGNOSTIC",
                "held": {"CAP-X": "DEMONSTRATED"},
                "observation_refs": ["OBS-SOLUTION"],
                "measured_fit_claim": False,
            }), encoding="utf-8")
            report = learner_evidence.audit(root)
            self.assertIn(
                "DEMONSTRATED_WITHOUT_AN_OBSERVATION",
                [row["point"] for row in report["findings"]],
            )

    def test_owner_estimate_floor_is_shared_by_plan_request(self):
        board = resolve_request.ladder("Physics", "BUCKET-RELATIVE-MOTION")
        caps, mics = capability_graph.subject_graph("Physics")
        request = {
            "learner": {
                "owner_estimate": {
                    "knowledge_percentage": 45,
                    "by": "owner",
                    "instruction": "rough starting estimate",
                }
            }
        }
        route = plan_request._learner_route(request, board, caps, mics, REPO)
        self.assertEqual(route["requested_entry"], "R1")
        self.assertEqual(route["selected_by"], "OWNER_ESTIMATE_CONSERVATIVE_FLOOR")
        self.assertEqual(route["entry"], "R1")
        self.assertEqual(route["prerequisite_checks"], [])

    def test_higher_owner_estimate_starts_higher_and_keeps_prerequisites_unverified(self):
        board = resolve_request.ladder("Physics", "BUCKET-RELATIVE-MOTION")
        caps, mics = capability_graph.subject_graph("Physics")
        request = {
            "learner": {
                "owner_estimate": {
                    "knowledge_percentage": 70,
                    "by": "owner",
                    "instruction": "rough starting estimate",
                }
            }
        }
        route = plan_request._learner_route(request, board, caps, mics, REPO)
        self.assertEqual(route["state"], "READY_WITH_CHECKS")
        self.assertEqual(route["entry"], "R4")
        self.assertEqual(route["selected_by"], "OWNER_ESTIMATE_CONSERVATIVE_FLOOR")
        self.assertEqual(
            route["prerequisite_checks"],
            ["CAP-SIGNED-PAIR", "CAP-SAME-TIME"],
        )
        self.assertEqual(route["bridges"], [])


if __name__ == "__main__":
    unittest.main()
