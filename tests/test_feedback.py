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


if __name__ == "__main__":
    unittest.main()
