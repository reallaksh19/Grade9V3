"""Feedback runtime gives the smallest useful help and never guesses learner state."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import feedback  # noqa: E402


class FeedbackRuntime(unittest.TestCase):
    SUBJECT = "Mathematics"
    QUESTION = "Q-MATH-LINEAR-01"

    def request(self, **overrides):
        request = {
            "subject": self.SUBJECT,
            "question_ref": self.QUESTION,
            "attempt_number": 1,
            "shown_hint_indices": [],
            "attempted_question_refs": [self.QUESTION],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": "SESSION-1",
            "response_summary": "Could not isolate x.",
            "evaluation": {
                "result": "INCORRECT",
                "failed_capability_ref": "CAP-MATH-ISOLATE",
                "error_stage": "SETUP",
            },
        }
        for key, value in overrides.items():
            if key == "evaluation":
                request["evaluation"].update(value)
            else:
                request[key] = value
        return request

    def test_first_wrong_attempt_gets_directional_hint_not_answer(self):
        report = feedback.run(self.request())
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["next_action"], "RETRY")
        self.assertEqual(report["hint"]["index"], 0)
        self.assertEqual(report["hint"]["reveals"], "CONCEPT")
        self.assertNotIn("7/3", report["hint"]["text"])

    def test_second_wrong_attempt_escalates_to_method_hint(self):
        report = feedback.run(self.request(
            attempt_number=2,
            shown_hint_indices=[0],
            help_used="HINT",
        ))
        self.assertEqual(report["next_action"], "RETRY")
        self.assertEqual(report["hint"]["index"], 1)
        self.assertEqual(report["hint"]["reveals"], "METHOD")

    def test_answer_hint_is_never_emitted_by_retry_runtime(self):
        report = feedback.run(self.request(
            attempt_number=2,
            shown_hint_indices=[0, 1],
            help_used="HINT",
            evaluation={"misconception_index": 0},
        ))
        self.assertEqual(report["next_action"], "REPAIR")
        self.assertNotIn("hint", report)
        self.assertEqual(report["repair"]["kind"], "MISCONCEPTION_REPAIR")

    def test_repair_is_followed_by_a_fresh_verification_task(self):
        report = feedback.run(self.request(
            attempt_number=3,
            shown_hint_indices=[0, 1],
            help_used="HINT",
            evaluation={"misconception_index": 0},
        ))
        self.assertEqual(report["next_action"], "REPAIR")
        self.assertEqual(report["repair"]["microtopic_ref"], "MIC-MATH-EQUIVALENT-OPS")
        self.assertEqual(report["after_repair"]["next_action"], "VERIFY")
        verification = report["after_repair"]["verification"]
        self.assertEqual(verification["kind"], "EXIT_TASK")
        self.assertNotIn("answer", verification)

    def test_correct_after_hint_is_uncertain_until_fresh_verification(self):
        report = feedback.run(self.request(
            shown_hint_indices=[0],
            help_used="HINT",
            response_summary="Solved after one hint.",
            evaluation={
                "result": "CORRECT",
                "failed_capability_ref": None,
                "error_stage": "UNKNOWN",
            },
        ))
        self.assertEqual(report["next_action"], "VERIFY")
        self.assertEqual(report["observation_draft"]["result"], "UNCERTAIN")
        self.assertEqual(report["observation_draft"]["help"], "HINT")
        self.assertEqual(report["review"]["outcome"], "CORRECT_WITH_HINT")
        self.assertEqual(report["review"]["next_review"], "2026-09-21")
        self.assertIsNotNone(report["verification"])

    def test_independent_correct_attempt_can_continue(self):
        report = feedback.run(self.request(
            response_summary="Solved independently.",
            evaluation={
                "result": "CORRECT",
                "failed_capability_ref": None,
                "error_stage": "UNKNOWN",
            },
        ))
        self.assertEqual(report["next_action"], "CONTINUE")
        self.assertEqual(report["observation_draft"]["result"], "DEMONSTRATED")
        self.assertEqual(report["observation_draft"]["capability_ref"], "CAP-MATH-ISOLATE")
        self.assertEqual(report["review"]["outcome"], "CORRECT_INDEPENDENT")
        self.assertEqual(report["review"]["next_review"], "2026-09-25")

    def test_multi_capability_failure_without_attribution_is_diagnosed_not_guessed(self):
        report = feedback.run(self.request(
            evaluation={
                "result": "INCORRECT",
                "failed_capability_ref": None,
                "error_stage": "UNKNOWN",
            },
        ))
        self.assertEqual(report["next_action"], "DIAGNOSE")
        self.assertIsNone(report["failed_capability_ref"])
        self.assertIsNone(report["observation_draft"])
        capabilities = {row["capability_ref"] for row in report["diagnostic_options"]}
        self.assertIn("CAP-MATH-ISOLATE", capabilities)
        self.assertIn("CAP-MATH-EXACTNESS", capabilities)

    def test_invalid_failed_capability_is_not_written_into_learner_evidence(self):
        report = feedback.run(self.request(
            evaluation={"failed_capability_ref": "CAP-NOT-IN-QUESTION"},
        ))
        self.assertFalse(report["passed"])
        self.assertEqual(report["next_action"], "DIAGNOSE")
        self.assertIsNone(report["observation_draft"])
        self.assertIn(
            "FEEDBACK_FAILED_CAPABILITY_NOT_REQUIRED",
            [row["point"] for row in report["findings"]],
        )

    def test_unknown_question_stops_cleanly(self):
        request = self.request()
        request["question_ref"] = "Q-NOT-REAL"
        report = feedback.run(request)
        self.assertFalse(report["passed"])
        self.assertEqual(report["next_action"], "STOP")
        self.assertEqual(report["findings"][0]["point"], "FEEDBACK_QUESTION_UNKNOWN")

    def test_model_choice_transfer_never_receives_a_method_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            library = root / "Example/library"
            library.mkdir(parents=True)
            (library / "example.v1.json").write_text(json.dumps({
                "package_id": "PKG-EXAMPLE",
                "capabilities": [{
                    "id": "CAP-CHOICE",
                    "prerequisite_refs": [],
                }],
                "microtopics": [{
                    "id": "MIC-CHOICE",
                    "primary_capability_ref": "CAP-CHOICE",
                    "title": "Choose a model",
                    "misconceptions": [{
                        "wrong_idea": "Pick from surface words.",
                        "diagnostic_prompt": "What relation is actually constrained?",
                        "repair": "Name the invariant before selecting a model.",
                    }],
                    "teaching_path": [{
                        "id": "STEP-CHOICE",
                        "action": "Name the invariant.",
                        "why_valid": "It selects the model from structure.",
                    }],
                }],
                "questions": [{
                    "id": "Q-TRANSFER",
                    "primary_capability_ref": "CAP-CHOICE",
                    "secondary_capability_refs": [],
                    "stem": "Choose and apply the model.",
                    "hints": [
                        {"text": "What remains invariant?", "reveals": "CONCEPT"},
                        {"text": "Use model X.", "reveals": "METHOD"},
                        {"text": "The answer is Y.", "reveals": "ANSWER"},
                    ],
                    "transfer": {
                        "dimension": "model_choice",
                        "statement": "The learner must choose the model.",
                        "builds_on": ["MIC-CHOICE"],
                    },
                    "answer": {"kind": "MODEL_RESPONSE"},
                }],
            }), encoding="utf-8")

            request = {
                "subject": "Example",
                "question_ref": "Q-TRANSFER",
                "attempt_number": 2,
                "shown_hint_indices": [0],
                "attempted_question_refs": ["Q-TRANSFER"],
                "help_used": "HINT",
                "when": "2026-09-18",
                "response_summary": "Still chose the wrong model.",
                "evaluation": {
                    "result": "INCORRECT",
                    "failed_capability_ref": "CAP-CHOICE",
                    "error_stage": "CONCEPT",
                    "misconception_index": 0,
                },
            }
            report = feedback.run(request, root)
            self.assertEqual(report["next_action"], "REPAIR")
            self.assertNotIn("hint", report)
            self.assertEqual(report["repair"]["kind"], "MISCONCEPTION_REPAIR")

    def test_explicit_repair_ref_resolves_to_specific_teaching_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            library = root / "Example/library"
            library.mkdir(parents=True)
            (library / "example.v1.json").write_text(json.dumps({
                "package_id": "PKG-EXAMPLE",
                "capabilities": [{"id": "CAP-X", "prerequisite_refs": []}],
                "microtopics": [{
                    "id": "MIC-X",
                    "primary_capability_ref": "CAP-X",
                    "title": "X",
                    "misconceptions": [],
                    "teaching_path": [{
                        "id": "STEP-X",
                        "action": "Rebuild the setup.",
                        "why_valid": "The setup determines the relation.",
                    }],
                }],
                "questions": [{
                    "id": "Q-X",
                    "primary_capability_ref": "CAP-X",
                    "secondary_capability_refs": [],
                    "stem": "Solve X.",
                    "hints": [],
                    "repair_ref": "STEP-X",
                    "answer": {"kind": "MODEL_RESPONSE"},
                }],
            }), encoding="utf-8")
            request = {
                "subject": "Example",
                "question_ref": "Q-X",
                "attempt_number": 3,
                "shown_hint_indices": [],
                "attempted_question_refs": ["Q-X"],
                "help_used": "NONE",
                "when": "2026-09-18",
                "response_summary": "Setup failed.",
                "evaluation": {
                    "result": "INCORRECT",
                    "failed_capability_ref": "CAP-X",
                    "error_stage": "SETUP",
                },
            }
            report = feedback.run(request, root)
            self.assertEqual(report["next_action"], "REPAIR")
            self.assertEqual(report["repair"]["kind"], "TEACHING_STEP")
            self.assertEqual(report["repair"]["repair_ref"], "STEP-X")
            self.assertEqual(
                report["after_repair"]["next_action"],
                "VERIFICATION_ITEM_REQUIRED",
            )


    def test_arbitrary_worksheet_question_can_produce_observation_and_review(self):
        fixture = json.loads(
            (REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json")
            .read_text(encoding="utf-8")
        )
        row = fixture["questions"][0]
        report = feedback.run({
            "subject": fixture["subject"],
            "question_ref": row["question_id"],
            "worksheet_question": row,
            "attempt_number": 1,
            "attempted_question_refs": [row["question_id"]],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": fixture["worksheet_id"],
            "response_summary": "Explained the top-of-flight case correctly.",
            "evaluation": {
                "result": "CORRECT",
                "error_stage": "UNKNOWN",
            },
        })
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["question_origin"], "WORKSHEET_MAPPING")
        self.assertEqual(report["next_action"], "CONTINUE")
        self.assertEqual(
            report["observation_draft"]["capability_ref"],
            row["primary_capability_ref"],
        )
        self.assertEqual(
            report["observation_draft"]["question_ref"],
            row["question_id"],
        )
        self.assertEqual(report["review"]["next_review"], "2026-09-25")

    def test_arbitrary_worksheet_question_diagnoses_instead_of_inventing_a_hint(self):
        fixture = json.loads(
            (REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json")
            .read_text(encoding="utf-8")
        )
        row = fixture["questions"][0]
        report = feedback.run({
            "subject": fixture["subject"],
            "question_ref": row["question_id"],
            "worksheet_question": row,
            "attempt_number": 1,
            "attempted_question_refs": [row["question_id"]],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": fixture["worksheet_id"],
            "response_summary": "Said acceleration must be zero because velocity is zero.",
            "evaluation": {
                "result": "INCORRECT",
                "failed_capability_ref": row["primary_capability_ref"],
                "error_stage": "CONCEPT",
            },
        })
        self.assertTrue(report["passed"], report["findings"])
        self.assertEqual(report["question_origin"], "WORKSHEET_MAPPING")
        self.assertEqual(report["next_action"], "DIAGNOSE")
        self.assertNotIn("hint", report)
        prompts = [
            item
            for option in report["diagnostic_options"]
            for item in option["diagnostics"]
        ]
        self.assertTrue(prompts)
        self.assertIn("diagnostic_prompt", prompts[0])

    def test_diagnosed_worksheet_failure_routes_to_existing_repair_then_fresh_check(self):
        fixture = json.loads(
            (REPO / "tests/fixtures/study_route/physics-cross-matrix.worksheet.json")
            .read_text(encoding="utf-8")
        )
        row = fixture["questions"][0]
        report = feedback.run({
            "subject": fixture["subject"],
            "question_ref": row["question_id"],
            "worksheet_question": row,
            "attempt_number": 1,
            "attempted_question_refs": [row["question_id"]],
            "help_used": "NONE",
            "when": "2026-09-18",
            "session_ref": fixture["worksheet_id"],
            "response_summary": "Velocity zero, therefore acceleration zero.",
            "evaluation": {
                "result": "INCORRECT",
                "failed_capability_ref": row["primary_capability_ref"],
                "error_stage": "CONCEPT",
                "misconception_index": 0,
            },
        })
        self.assertEqual(report["next_action"], "REPAIR")
        self.assertEqual(report["repair"]["kind"], "MISCONCEPTION_REPAIR")
        self.assertEqual(
            report["repair"]["microtopic_ref"],
            "MIC-PHY-KIN-ZERO-V-NONZERO-A",
        )
        self.assertEqual(report["after_repair"]["next_action"], "VERIFY")
        verification = report["after_repair"]["verification"]
        self.assertEqual(verification["kind"], "EXIT_TASK")
        self.assertNotIn("answer", verification)

    def test_arbitrary_worksheet_mapping_with_unknown_capability_stops(self):
        report = feedback.run({
            "subject": "Physics",
            "question_ref": "SCHOOL-Q-404",
            "worksheet_question": {
                "question_id": "SCHOOL-Q-404",
                "primary_capability_ref": "CAP-NOT-REAL",
                "secondary_capability_refs": [],
                "mapping_basis": "MANUAL",
            },
            "attempt_number": 1,
            "help_used": "NONE",
            "when": "2026-09-18",
            "evaluation": {
                "result": "INCORRECT",
                "failed_capability_ref": "CAP-NOT-REAL",
                "error_stage": "CONCEPT",
            },
        })
        self.assertFalse(report["passed"])
        self.assertEqual(report["next_action"], "STOP")
        self.assertIn(
            "FEEDBACK_WORKSHEET_CAPABILITY_UNKNOWN",
            [row["point"] for row in report["findings"]],
        )

    def test_canonical_question_remains_authoritative_if_a_supplied_mapping_drifts(self):
        report = feedback.run({
            "subject": "Mathematics",
            "question_ref": self.QUESTION,
            "worksheet_question": {
                "question_id": self.QUESTION,
                "primary_capability_ref": "CAP-MATH-SUBSTITUTE",
                "secondary_capability_refs": [],
                "mapping_basis": "AGENT_PROPOSAL",
            },
            "attempt_number": 1,
            "help_used": "NONE",
            "when": "2026-09-18",
            "evaluation": {
                "result": "CORRECT",
                "error_stage": "UNKNOWN",
            },
        })
        self.assertFalse(report["passed"])
        self.assertEqual(report["question_origin"], "CANONICAL_QUESTION")
        self.assertIn(
            "FEEDBACK_CANONICAL_MAPPING_DRIFT",
            [row["point"] for row in report["findings"]],
        )
        self.assertEqual(
            report["observation_draft"]["capability_ref"],
            "CAP-MATH-ISOLATE",
        )


if __name__ == "__main__":
    unittest.main()
