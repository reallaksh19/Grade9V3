"""Gate layer: the registry validates, and each declared falsification case really fails.

A registry that only passes proves little. Every gate declares the mutations that
should break it; these tests apply them and assert the validator catches each one.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Physics.adapter import load as load_physics  # noqa: E402
from Shared.contracts import ContractError  # noqa: E402
from Shared.gates.validate import validate  # noqa: E402

REGISTRY = REPO / "Physics/gates/motion-vectors.v1.json"
BINDINGS = REPO / "Physics/gates/curriculum-bindings.v1.json"


def registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def bindings():
    return json.loads(BINDINGS.read_text(encoding="utf-8"))


def gate(data, gate_id):
    return next(g for g in data["gates"] if g["gate_id"] == gate_id)


class RegistryValidates(unittest.TestCase):
    def test_physics_registry_passes(self):
        report = validate(registry(), load_physics(), bindings())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["gate_count"], 6)
        self.assertEqual(report["held"], [])
        self.assertEqual(report["release_authority"], "NOT_GRANTED_BY_GATE_VALIDATION")

    def test_every_gate_declares_at_least_one_falsification_case(self):
        for row in registry()["gates"]:
            self.assertTrue(row["falsification_cases"], row["gate_id"])


class CurriculumAuthorityFailsClosed(unittest.TestCase):
    """A board claim needs an exact binding; it is never assumed."""

    def test_all_shipped_gates_are_owner_extension_not_prescribed(self):
        report = validate(registry(), load_physics(), bindings())
        self.assertEqual(report["curriculum_scope"]["authorised_prescribed"], [])
        self.assertEqual(len(report["curriculum_scope"]["owner_extension"]), 6)

    def test_prescribed_claim_without_a_binding_is_held(self):
        data = registry()
        gate(data, "PHY-REL-VELOCITY")["curriculum"]["scope_class"] = "PRESCRIBED"
        report = validate(data, load_physics(), bindings())
        self.assertIn("PHY-REL-VELOCITY", report["curriculum_scope"]["held_insufficient_authority"])
        self.assertEqual(report["curriculum_scope"]["authorised_prescribed"], [])

    def test_prescribed_claim_with_an_exact_binding_is_authorised(self):
        data = registry()
        for row in data["gates"]:
            row["curriculum"]["scope_class"] = "PRESCRIBED"
        exact = {"bindings": [{"board": "CBSE", "grade": 9, "chapter": "Motion",
                               "gate_ids": sorted(g["gate_id"] for g in data["gates"])}]}
        report = validate(data, load_physics(), exact)
        self.assertEqual(len(report["curriculum_scope"]["authorised_prescribed"]), 6)
        self.assertEqual(report["curriculum_scope"]["held_insufficient_authority"], [])

    def test_a_partial_binding_does_not_authorise_the_chapter(self):
        data = registry()
        for row in data["gates"]:
            row["curriculum"]["scope_class"] = "PRESCRIBED"
        partial = {"bindings": [{"board": "CBSE", "grade": 9, "chapter": "Motion",
                                 "gate_ids": ["PHY-REL-VELOCITY"]}]}
        report = validate(data, load_physics(), partial)
        self.assertEqual(report["curriculum_scope"]["authorised_prescribed"], [])
        self.assertEqual(len(report["curriculum_scope"]["held_insufficient_authority"]), 6)


class DeclaredFalsifiersReallyFail(unittest.TestCase):
    """Each mutation named in the registry's falsification_cases is applied for real."""

    def assert_blocked(self, data, code, bindings_=None):
        with self.assertRaises(ContractError) as caught:
            validate(data, load_physics(), bindings_ or bindings())
        self.assertEqual(caught.exception.code, code)

    def test_duplicate_asset_id_across_gates(self):
        data = registry()
        gate(data, "PHY-REL-OBSERVER-REVERSAL")["relations"][0]["relation_id"] = "REL-RELATIVE-VELOCITY"
        self.assert_blocked(data, "GATE_DUPLICATE_ASSET_ID")

    def test_unknown_prerequisite(self):
        data = registry()
        gate(data, "PHY-REL-OBSERVER-REVERSAL")["prerequisites"] = ["PHY-NO-SUCH-GATE"]
        self.assert_blocked(data, "GATE_PREREQUISITE_UNKNOWN")

    def test_prerequisite_cycle(self):
        data = registry()
        gate(data, "PHY-VEC-SCALAR-VECTOR")["prerequisites"] = ["PHY-REL-VELOCITY"]
        self.assert_blocked(data, "DEPENDENCY_CYCLE")

    def test_reasoning_step_depending_on_a_later_step(self):
        data = registry()
        steps = gate(data, "PHY-REL-VELOCITY")["reasoning_sequence"]
        steps[0]["depends_on"] = [steps[-1]["step_id"]]
        self.assert_blocked(data, "REASONING_DEPENDENCY_NOT_EARLIER")

    def test_representation_kind_the_subject_never_declared(self):
        data = registry()
        gate(data, "PHY-VEC-SUBTRACTION")["representations"][0]["kind"] = "PARTICLE_DIAGRAM"
        self.assert_blocked(data, "REPRESENTATION_KIND_UNDECLARED")

    def test_symbol_missing_a_field_the_subject_requires(self):
        data = registry()
        del gate(data, "PHY-VEC-SCALAR-VECTOR")["relations"][0]["symbols"][0]["unit"]
        self.assert_blocked(data, "SYMBOL_FIELD_MISSING")

    def test_subject_cannot_accept_another_subjects_capability_itself(self):
        data = registry()
        gate(data, "PHY-VEC-SCALAR-VECTOR")["external_prerequisites"][0]["acceptance_status"] = "PROVIDER_ACCEPTED"
        self.assert_blocked(data, "PROVIDER_ACCEPTANCE_NOT_SELF_GRANTABLE")

    def test_grade_outside_the_subjects_declared_band(self):
        data = registry()
        gate(data, "PHY-REL-VELOCITY")["curriculum"]["grade"] = 11
        data_ok = validate(data, load_physics(), bindings())   # 11 is in band, so this passes
        self.assertEqual(data_ok["status"], "PASS")
        gate(data, "PHY-REL-VELOCITY")["curriculum"]["grade"] = 12
        self.assert_blocked(data, "GATE_SCHEMA_VIOLATION")

    def test_registry_for_the_wrong_subject_is_rejected(self):
        data = registry()
        data["subject"] = "Chemistry"
        self.assert_blocked(data, "GATE_REGISTRY_WRONG_SUBJECT")

    def test_a_gate_may_not_claim_validated_maturity(self):
        data = registry()
        data["maturity"] = "VALIDATED"
        self.assert_blocked(data, "GATE_SCHEMA_VIOLATION")


class GatesBindToAuthoredContent(unittest.TestCase):
    """The gate set must actually cover the buckets this repository has authored."""

    def test_relative_velocity_gate_exists_for_the_authored_bucket(self):
        ids = {g["gate_id"] for g in registry()["gates"]}
        self.assertIn("PHY-REL-VELOCITY", ids)
        self.assertIn("PHY-VEC-SUBTRACTION", ids)

    def test_mathematics_prerequisites_stay_provider_review_required(self):
        external = [e for g in registry()["gates"] for e in g.get("external_prerequisites", [])]
        self.assertTrue(external)
        for entry in external:
            self.assertEqual(entry["provider_subject"], "Mathematics")
            self.assertEqual(entry["acceptance_status"], "PROVIDER_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
