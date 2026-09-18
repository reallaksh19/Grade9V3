"""Application context is a schema layer, never a capability or prerequisite."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError  # noqa: E402
from Shared.library import intake, resolve  # noqa: E402


class ApplicationContextSchema(unittest.TestCase):
    def relative_motion(self):
        return json.loads(
            (REPO / "Physics/library/relative-motion.v1.json").read_text(
                encoding="utf-8"
            )
        )

    def context(self):
        return {
            "id": "CTX-SYNTHETIC-APPLICATION",
            "version": "0.1.0",
            "status": "CANDIDATE",
            "source_refs": [],
            "evidence_refs": [],
            "extensions": {},
            "title": "Synthetic application setting",
            "description": (
                "A reusable situation in which existing capabilities are exercised "
                "without becoming a new mastery target."
            ),
            "invariants": [
                "The underlying capability contract is unchanged by the story setting."
            ],
            "variation_dimensions": [{
                "name": "surface form",
                "description": "Change the objects, numbers or wording while preserving demand.",
            }],
            "task_objectives": [
                "Apply the existing capability to the stated situation."
            ],
            "scope_limits": [
                "A context does not add prerequisite or learner-state semantics."
            ],
        }

    def test_schema_can_classify_question_family_and_item_by_context(self):
        package = self.relative_motion()
        package["application_contexts"] = [self.context()]
        package["question_families"][0]["context_refs"] = [
            "CTX-SYNTHETIC-APPLICATION"
        ]
        package["questions"][0]["context_refs"] = [
            "CTX-SYNTHETIC-APPLICATION"
        ]
        self.assertEqual(intake.schema_errors(package), [])

    def test_context_is_indexed_and_context_refs_are_real_references(self):
        package = {
            "package_id": "PKG-SYNTHETIC",
            "application_contexts": [self.context()],
            "capabilities": [{
                "id": "CAP-SYNTHETIC",
                "prerequisite_refs": [],
            }],
            "question_families": [{
                "id": "FAM-SYNTHETIC",
                "context_refs": ["CTX-SYNTHETIC-APPLICATION"],
            }],
            "questions": [{
                "id": "Q-SYNTHETIC",
                "context_refs": ["CTX-SYNTHETIC-APPLICATION"],
            }],
        }
        records = resolve.build_index([package])
        self.assertEqual(
            records["CTX-SYNTHETIC-APPLICATION"]["_collection"],
            "application_contexts",
        )
        family_refs = dict(resolve.references(records["FAM-SYNTHETIC"]))
        question_refs = dict(resolve.references(records["Q-SYNTHETIC"]))
        self.assertIn("CTX-SYNTHETIC-APPLICATION", family_refs.values())
        self.assertIn("CTX-SYNTHETIC-APPLICATION", question_refs.values())

    def test_context_cannot_be_used_as_a_prerequisite(self):
        package = {
            "package_id": "PKG-SYNTHETIC",
            "application_contexts": [self.context()],
            "capabilities": [{
                "id": "CAP-SYNTHETIC",
                "prerequisite_refs": ["CTX-SYNTHETIC-APPLICATION"],
            }],
        }
        with self.assertRaises(ContractError) as caught:
            resolve.validate_library([package])
        self.assertEqual(
            caught.exception.code,
            "APPLICATION_CONTEXT_USED_AS_PREREQUISITE",
        )

    def test_context_does_not_enter_capability_prerequisite_closure(self):
        package = {
            "package_id": "PKG-SYNTHETIC",
            "application_contexts": [self.context()],
            "capabilities": [
                {"id": "CAP-A", "prerequisite_refs": []},
                {"id": "CAP-B", "prerequisite_refs": ["CAP-A"]},
            ],
            "question_families": [{
                "id": "FAM-B",
                "context_refs": ["CTX-SYNTHETIC-APPLICATION"],
            }],
        }
        records = resolve.build_index([package])
        closure = resolve.prerequisite_closure(records, ["CAP-B"])
        self.assertEqual(closure, ["CAP-A", "CAP-B"])
        self.assertNotIn("CTX-SYNTHETIC-APPLICATION", closure)


if __name__ == "__main__":
    unittest.main()
