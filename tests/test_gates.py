"""Gate layer: the registry validates, and each declared falsification case really fails.

A registry that only passes proves little. Every gate declares the mutations that should
break it; these tests apply them and assert the validator catches each one.

That claim was false for as long as this docstring has existed, and the measurement is at
EveryDeclaredFalsifierIsExecuted below. It is true now because the binding is derived from
running the mutation rather than from a table that agrees with itself.
"""
import copy
import math
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Physics.adapter import load as load_physics  # noqa: E402
from Physics.adapter.validator import recompute as physics_recompute  # noqa: E402
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


class FoundationalQuantitativeValidators(unittest.TestCase):
    def case(self, validator_id, units, **values):
        return {"validator_id": validator_id, "units": units, **values}

    def test_average_rate_keeps_distance_and_displacement_separate(self):
        result = physics_recompute(self.case(
            "AVERAGE_RATE", {"distance": "m", "displacement": "m", "dt": "s"},
            distance=120, displacement=40, dt=20))
        self.assertEqual(result, {"average_speed_m_s": 6, "average_velocity_m_s": 2})

    def test_wave_and_power_validators_compute_only_the_declared_scalar(self):
        wave = physics_recompute(self.case(
            "WAVE_SPEED", {"frequency": "Hz", "wavelength": "m"},
            frequency=5, wavelength=3))
        average = physics_recompute(self.case(
            "AVERAGE_POWER", {"work": "J", "dt": "s"}, work=120, dt=4))
        instant = physics_recompute(self.case(
            "INSTANTANEOUS_POWER", {"force_parallel": "N", "speed": "m/s"},
            force_parallel=-6, speed=2))
        self.assertEqual((wave, average, instant), (15, 30, -12))

    def test_grade9_motion_force_energy_machine_and_sound_validators(self):
        displacement = physics_recompute(self.case(
            "CONSTANT_ACCELERATION_DISPLACEMENT",
            {"u": "m/s", "a": "m/s^2", "t": "s"}, u=5, a=2, t=3))
        no_time = physics_recompute(self.case(
            "CONSTANT_ACCELERATION_NO_TIME",
            {"u": "m/s", "a": "m/s^2", "s": "m"}, u=5, a=2, s=24))
        force = physics_recompute(self.case(
            "NEWTON_SECOND_LAW",
            {"mass": "kg", "acceleration": "m/s^2"}, mass=4, acceleration=3))
        work = physics_recompute(self.case(
            "WORK_CONSTANT_FORCE",
            {"force_parallel": "N", "displacement": "m"},
            force_parallel=-5, displacement=4))
        kinetic = physics_recompute(self.case(
            "KINETIC_ENERGY", {"mass": "kg", "speed": "m/s"}, mass=2, speed=3))
        potential = physics_recompute(self.case(
            "GRAVITATIONAL_POTENTIAL_ENERGY",
            {"mass": "kg", "g": "m/s^2", "delta_h": "m"},
            mass=2, g=10, delta_h=5))
        ma = physics_recompute(self.case(
            "MECHANICAL_ADVANTAGE",
            {"load_force": "N", "effort_force": "N"},
            load_force=120, effort_force=40))
        frequency = physics_recompute(self.case(
            "FREQUENCY_PERIOD", {"period": "s"}, period=0.005))
        echo = physics_recompute(self.case(
            "ECHO_DISTANCE", {"speed": "m/s", "echo_time": "s"},
            speed=340, echo_time=0.4))
        graph_acceleration = physics_recompute(self.case(
            "AVERAGE_ACCELERATION",
            {"delta_v": "m/s", "dt": "s"}, delta_v=8, dt=4))
        circular_speed = physics_recompute(self.case(
            "UNIFORM_CIRCULAR_SPEED",
            {"radius": "m", "period": "s"}, radius=10, period=20))
        self.assertEqual(displacement, 24)
        self.assertEqual(no_time, {"v_squared_m2_s2": 121})
        self.assertEqual(force, 12)
        self.assertEqual(work, -20)
        self.assertEqual(kinetic, 9)
        self.assertEqual(potential, 100)
        self.assertEqual(ma, 3)
        self.assertEqual(frequency, 200)
        self.assertEqual(echo, 68)
        self.assertEqual(graph_acceleration, 2)
        self.assertAlmostEqual(circular_speed, math.pi)

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


# --- Declared falsifiers are bound to mutations that actually run ---------------------
#
# The module docstring above has claimed since it was written that "every gate declares
# the mutations that should break it; these tests apply them". Measured: thirteen declared
# cases across two subjects, and not one case_id appeared anywhere in this file. Seven
# matched a test by code coincidence, five were in a subject these tests never loaded, and
# one -- FAL-VEC-NO-AXES -- named a violation the validator could not raise at all, on a
# field whose content could be replaced with a single nonsense string while the registry
# still passed.
#
# The binding below is execution-derived rather than declared: a case is covered only if a
# mutation registered under its id is applied and the outcome it names is the outcome
# observed. A mutation registry that lies fails, rather than a table that agrees with
# itself.

MUTATIONS = {}


def mutates(case_id):
    def register(fn):
        assert case_id not in MUTATIONS, f"{case_id} registered twice"
        MUTATIONS[case_id] = fn
        return fn
    return register


@mutates("FAL-VEC-NO-AXES")
def _vec_no_axes(data):
    rep = gate(data, "PHY-VEC-SCALAR-VECTOR")["representations"][0]
    rep["required_labels"] = [e for e in rep["required_labels"]
                              if "axis directions" not in e["label"]]


@mutates("FAL-VEC-SYMBOL-NO-UNIT")
def _vec_symbol_no_unit(data):
    del gate(data, "PHY-VEC-SCALAR-VECTOR")["relations"][0]["symbols"][0]["unit"]


@mutates("FAL-AXIS-CYCLE")
def _axis_cycle(data):
    gate(data, "PHY-VEC-AXIS-CONVENTION")["prerequisites"] = ["PHY-VEC-AXIS-CONVENTION"]


@mutates("FAL-SUB-REP-UNDECLARED")
def _sub_rep_undeclared(data):
    gate(data, "PHY-VEC-SUBTRACTION")["representations"][0]["kind"] = "PARTICLE_DIAGRAM"


@mutates("FAL-RELPOS-NO-COUNTEREXAMPLE")
def _relpos_no_counterexample(data):
    gate(data, "PHY-REL-POSITION")["misconceptions"][0]["counterexample"] = ""


@mutates("FAL-RELV-STEP-ORDER")
def _relv_step_order(data):
    steps = gate(data, "PHY-REL-VELOCITY")["reasoning_sequence"]
    steps[0]["depends_on"] = [steps[-1]["step_id"]]


@mutates("FAL-RELV-DUPLICATE-ASSET")
def _relv_duplicate_asset(data):
    gate(data, "PHY-REL-OBSERVER-REVERSAL")["relations"][0]["relation_id"] = \
        "REL-RELATIVE-VELOCITY"


@mutates("FAL-REV-PREREQ-UNKNOWN")
def _rev_prereq_unknown(data):
    gate(data, "PHY-REL-OBSERVER-REVERSAL")["prerequisites"] = ["PHY-NO-SUCH-GATE"]


@mutates("FAL-EQ-SYMBOL-NO-DOMAIN")
def _eq_symbol_no_domain(data):
    del gate(data, "MATH-EQ-CONSTRAINT")["relations"][0]["symbols"][0]["domain"]


@mutates("FAL-EQ-REP-UNDECLARED")
def _eq_rep_undeclared(data):
    gate(data, "MATH-EQ-CONSTRAINT")["representations"][0]["kind"] = "FREE_BODY_DIAGRAM"


@mutates("FAL-EQ-BACKWARD-STEP")
def _eq_backward_step(data):
    steps = gate(data, "MATH-EQ-EQUIVALENT-OPERATIONS")["reasoning_sequence"]
    steps[0]["depends_on"] = [steps[-1]["step_id"]]


@mutates("FAL-EQ-DUPLICATE-ASSET")
def _eq_duplicate_asset(data):
    gate(data, "MATH-EQ-EXACT-SOLUTION")["relations"][0]["relation_id"] = \
        "REL-EQ-LINEAR-SOLUTION"


@mutates("FAL-EQ-PRESCRIBED-NO-BINDING")
def _eq_prescribed_no_binding(data):
    gate(data, "MATH-EQ-EXACT-SOLUTION")["curriculum"]["scope_class"] = "PRESCRIBED"


def _undeclare_first_relation_validator(data, gate_id):
    gate(data, gate_id)["relations"][0]["validator_refs"] = ["VALIDATOR_NOT_DECLARED"]


@mutates("FAL-KIN-AVG-VALIDATOR")
def _kin_avg_validator(data):
    _undeclare_first_relation_validator(data, "PHY-KIN-AVERAGE-RATES")


@mutates("FAL-WAVE-SPEED-VALIDATOR")
def _wave_speed_validator(data):
    _undeclare_first_relation_validator(data, "PHY-WAVE-SPEED")


@mutates("FAL-POWER-RATES-VALIDATOR")
def _power_rates_validator(data):
    _undeclare_first_relation_validator(data, "PHY-POWER-RATES")


@mutates("FAL-NLM2-VALIDATOR")
def _nlm2_validator(data):
    _undeclare_first_relation_validator(data, "PHY-NEWTON-SECOND-LAW")


@mutates("FAL-WEP9-VALIDATOR")
def _wep9_validator(data):
    _undeclare_first_relation_validator(data, "PHY-WORK-ENERGY-GRADE9")


@mutates("FAL-MACHINE-MA-VALIDATOR")
def _machine_ma_validator(data):
    _undeclare_first_relation_validator(data, "PHY-SIMPLE-MACHINES-GRADE9")


def registries():
    """Every subject's gate registries, with that subject's adapter and bindings."""
    import importlib
    found = []
    for path in sorted(REPO.glob("*/gates/*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "gates" not in data:
            continue
        subject = path.relative_to(REPO).parts[0]
        binding_path = REPO / subject / "gates/curriculum-bindings.v1.json"
        found.append((path, data, importlib.import_module(f"{subject}.adapter").load(),
                      json.loads(binding_path.read_text(encoding="utf-8"))))
    return found


class EveryDeclaredFalsifierIsExecuted(unittest.TestCase):
    """A declared falsifier nothing runs is a claim about checkability, never a check."""

    def cases(self):
        for path, data, adapter, binds in registries():
            for row in data["gates"]:
                for case in row["falsification_cases"]:
                    yield path, data, adapter, binds, row, case

    def test_every_declared_case_has_a_mutation_and_produces_what_it_declares(self):
        seen = 0
        for path, data, adapter, binds, row, case in self.cases():
            case_id = case["case_id"]
            with self.subTest(registry=path.name, case=case_id):
                self.assertIn(case_id, MUTATIONS,
                              "declared as a falsifier and nothing applies it")
                mutated = copy.deepcopy(data)
                MUTATIONS[case_id](mutated)
                if "expected_violation" in case:
                    with self.assertRaises(ContractError) as caught:
                        validate(mutated, adapter, binds)
                    self.assertEqual(caught.exception.code, case["expected_violation"],
                                     "the observed violation is not the declared one")
                else:
                    key = case["expected_report"]
                    before = validate(data, adapter, binds)["curriculum_scope"][key]
                    after = validate(mutated, adapter, binds)["curriculum_scope"][key]
                    self.assertNotEqual(sorted(after), sorted(before),
                                        f"{key} did not change, so the case proves nothing")
                    self.assertIn(row["gate_id"], [str(x) for x in after])
                seen += 1
        self.assertGreater(seen, 0, "no declared cases, so this asserts nothing")

    def test_no_mutation_claims_a_case_no_registry_declares(self):
        declared = {case["case_id"] for *_, case in self.cases()}
        self.assertEqual(sorted(set(MUTATIONS) - declared), [])

    def test_both_subjects_registries_are_reached(self):
        # Five of the thirteen cases were in a registry this file never loaded.
        self.assertEqual(sorted({p.relative_to(REPO).parts[0] for p, *_ in registries()}),
                         ["Mathematics", "Physics"])
