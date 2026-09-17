"""Library layer: intake refuses hollow records, references resolve, maturity is monotone,
and a bucket compiles into inputs that actually publish."""
import collections
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Physics.adapter import load as load_physics  # noqa: E402
from Shared.contracts import ContractError, is_prose, join  # noqa: E402
from Shared.library.compile_inputs import compile_bucket, write  # noqa: E402
from Shared.library import authority, depiction, differentiation, intake, substance  # noqa: E402
from Shared.library import resolve as resolve_module  # noqa: E402
from Shared.library.intake import check  # noqa: E402
from Shared.library.promote import audit, promote  # noqa: E402
from Shared.library.resolve import (  # noqa: E402
    build_index, slice_for_bucket, unresolved, validate_library,
)
from Shared.publication_host.host import publish  # noqa: E402

PACKAGES = sorted((REPO / "Physics/library").glob("*.json"))
BUCKET_MATH = "BUCKET-LINEAR-EQUATION"
MATH_PACKAGES = sorted((REPO / "Mathematics/library").glob("*.json"))


def math_records():
    """The Mathematics slice, which is the one with a compiled figure to place."""
    return build_index([json.loads(p.read_text(encoding="utf-8")) for p in MATH_PACKAGES])


def packages():
    return [json.loads(p.read_text(encoding="utf-8")) for p in PACKAGES]


def microtopic(package, mid):
    return next(m for m in package["microtopics"] if m["id"] == mid)


class Intake(unittest.TestCase):
    def test_both_shipped_packages_are_admitted(self):
        for package in packages():
            report = check(package)
            self.assertTrue(report["admitted"], report["findings"])

    def test_a_microtopic_without_a_closing_exit_answer_is_refused(self):
        package = packages()[0]
        microtopic(package, "MIC-SAME-TIME")["exit_task"]["answer"]["summary"] = ""
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "EXIT" for f in report["findings"]))

    def test_a_teaching_step_that_asserts_without_justifying_is_refused(self):
        package = packages()[0]
        microtopic(package, "MIC-SAME-TIME")["teaching_path"][0]["why_valid"] = "  "
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "PATH" for f in report["findings"]))

    def test_a_microtopic_with_no_plausible_wrong_path_is_refused(self):
        package = packages()[0]
        microtopic(package, "MIC-SAME-TIME")["misconceptions"] = []
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "MISCONCEPTION" for f in report["findings"]))


class Resolution(unittest.TestCase):
    def test_library_validates(self):
        report = validate_library(packages())
        self.assertEqual(report["unresolved_references"], 0)
        self.assertEqual(report["prerequisite_graph"], "ACYCLIC")

    def test_duplicate_identity_across_packages_is_rejected(self):
        first, second = packages()
        second["capabilities"].append(copy.deepcopy(first["capabilities"][0]))
        with self.assertRaises(ContractError) as caught:
            build_index([first, second])
        self.assertEqual(caught.exception.code, "LIBRARY_DUPLICATE_ID")

    def test_a_dangling_reference_is_reported(self):
        package = packages()[0]
        microtopic(package, "MIC-SAME-TIME")["relation_refs"] = ["REL-DOES-NOT-EXIST"]
        missing = unresolved(build_index([package]))
        self.assertTrue(any(m["target"] == "REL-DOES-NOT-EXIST" for m in missing))

    def test_a_prerequisite_cycle_is_rejected(self):
        package = packages()[0]
        microtopic(package, "MIC-SAME-TIME")["prerequisite_refs"] = ["MIC-GEOMETRIC-CHECK"]
        with self.assertRaises(ContractError) as caught:
            validate_library([package] + packages()[1:])
        self.assertEqual(caught.exception.code, "LIBRARY_PREREQUISITE_CYCLE")

    def test_a_bucket_slice_pulls_in_its_cross_package_prerequisites(self):
        records = build_index(packages())
        chosen = slice_for_bucket(records, "BUCKET-RELATIVE-MOTION")
        pulled = {r["id"] for rows in chosen["records"].values() for r in rows}
        # The relative-motion bucket depends on vector-representation work in the other package.
        self.assertIn("MIC-GRAPHICAL-SUBTRACTION", pulled)
        self.assertIn("BUCKET-VECTOR-REPRESENTATION", pulled)
        self.assertEqual(chosen["microtopic_order"][0], "MIC-SAME-TIME")


class Promotion(unittest.TestCase):
    EVIDENCE = {"reviewer": "second-instance", "reviewed_on": "2026-09-16",
                "scope": "relative motion derivations", "originals_inspected": True}

    def test_a_stage_cannot_be_skipped(self):
        with self.assertRaises(ContractError) as caught:
            promote({"id": "X", "status": "CANDIDATE"}, "CURATED",
                    {"accepted_by": "owner", "accepted_on": "2026-09-16", "scope": "all"})
        self.assertEqual(caught.exception.code, "PROMOTION_SKIPPED_A_STAGE")

    def test_an_author_cannot_review_their_own_record(self):
        record = {"id": "X", "status": "CANDIDATE", "authored_by": "second-instance"}
        with self.assertRaises(ContractError) as caught:
            promote(record, "REVIEWED", self.EVIDENCE)
        self.assertEqual(caught.exception.code, "SELF_REVIEW_NOT_INDEPENDENT")

    def test_a_review_that_did_not_inspect_originals_is_refused(self):
        evidence = {**self.EVIDENCE, "originals_inspected": False}
        with self.assertRaises(ContractError) as caught:
            promote({"id": "X", "status": "CANDIDATE"}, "REVIEWED", evidence)
        self.assertEqual(caught.exception.code, "REVIEW_DID_NOT_INSPECT_ORIGINALS")

    def test_a_valid_promotion_records_its_evidence(self):
        promoted = promote({"id": "X", "status": "CANDIDATE"}, "REVIEWED", self.EVIDENCE)
        self.assertEqual(promoted["status"], "REVIEWED")
        self.assertEqual(promoted["lifecycle_history"][-1]["evidence"], self.EVIDENCE)

    def test_demotion_needs_no_evidence(self):
        self.assertEqual(promote({"id": "X", "status": "CURATED"}, "CANDIDATE", {})["status"],
                         "CANDIDATE")

    def test_shipped_library_is_monotone(self):
        self.assertTrue(audit(packages())["monotone"])

    def test_a_curated_record_resting_on_a_candidate_dependency_is_caught(self):
        data = packages()
        microtopic(data[0], "MIC-COMMON-INTERVAL")["status"] = "CURATED"
        report = audit(data)
        self.assertFalse(report["monotone"])
        self.assertTrue(any(v["record"] == "MIC-COMMON-INTERVAL" and v["dependency_status"] == "CANDIDATE"
                            for v in report["maturity_violations"]))


class Compilation(unittest.TestCase):
    def compile(self):
        return compile_bucket(build_index(packages()), "BUCKET-RELATIVE-MOTION",
                              topic_id="PHY-RELV-G9", title="Relative velocity in a plane",
                              subject="Physics",
                              practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})

    def test_compiles_inputs_that_actually_publish(self):
        compiled = self.compile()
        with tempfile.TemporaryDirectory() as temp:
            inputs = Path(temp) / "inputs"
            inputs.mkdir()
            write(compiled, inputs)
            result = publish(inputs / "plan.json", inputs / "baseline.json", inputs,
                             Path(temp) / "publication", load_physics())
        self.assertEqual(result["status"], "PASS")
        # Two now, not one: Core2 holds the question in custody with its answer, so the
        # same verified result is checked again in the product that preserves it.
        self.assertEqual(result["numeric_answers_compared"], 2)
        self.assertIn("CORE1", result["products"])
        self.assertIn("CORE2", result["products"])
        self.assertFalse(result["release_authorized"])

    def test_a_product_the_library_cannot_support_is_reported_not_padded(self):
        compiled = self.compile()
        self.assertNotIn("CORE2B", compiled["baseline"]["selected_cores"])
        unsupported = [r for r in compiled["authoring_requirements"] if r["kind"] == "PRODUCT_UNSUPPORTED"]
        self.assertEqual([r["core"] for r in unsupported], ["CORE2B"])

    def test_remaining_authoring_is_declared_rather_than_invented(self):
        # This named FIGURE_AUTHORING, which R3.1 closed for this subject. Asserting a
        # particular backlog item makes closing it a test failure, which is the wrong
        # incentive. The property is that whatever is still owed is *stated*, with a
        # core or a reason, rather than quietly produced by the compiler.
        owed = self.compile()["authoring_requirements"]
        self.assertTrue(owed)
        self.assertIn("PROSE_AUTHORING", {r["kind"] for r in owed})
        for row in owed:
            with self.subTest(kind=row["kind"]):
                self.assertTrue(str(row.get("detail", "")).strip(),
                                f'{row["kind"]} is owed and says nothing about what or why')

    def test_no_figure_authoring_remains_for_this_subject(self):
        # R3.1's exit evidence, asserted where it can fail rather than only in a commit
        # message: every representation this bucket reaches holds a scene instance.
        owed = [r for r in self.compile()["authoring_requirements"]
                if r["kind"] == "FIGURE_AUTHORING"]
        self.assertEqual(owed, [])

    def test_teaching_text_comes_from_the_library_not_from_a_template(self):
        # Core1A is the product that teaches. Core1 maps the bucket and Core2 holds its
        # questions, so neither carries a teaching path and neither is what this checks.
        plan = self.compile()["plan"]
        study = next(p for p in plan["products"] if p["core"] == "CORE1A")
        text = study["units"][0]["blocks"][0]["text"]
        self.assertIn("r_A/B = r_A - r_B", text)
        self.assertIn("Vector displacements add along consecutive paths", text)

    def test_core1_maps_the_bucket_from_records_that_already_hold_it(self):
        plan = self.compile()["plan"]
        orientation = next(p for p in plan["products"] if p["core"] == "CORE1")
        blocks = orientation["units"][0]["blocks"]
        kinds = {b["kind"] for b in blocks}
        self.assertEqual(kinds, {"TEXT", "EQUATION"})
        quantities = next(b for b in blocks if b["id"] == "CORE1-QUANTITIES")["text"]
        self.assertIn("v_A/B,x", quantities, "the bucket's own symbols, with their meanings")
        demand = next(b for b in blocks if b["id"] == "CORE1-DEMAND")["text"]
        badges = {m["intrinsic_badge"] for m in packages()[0]["microtopics"]}
        self.assertTrue(badges & set(("EASY", "MEDIUM", "HARD")))
        for badge in badges:
            self.assertIn(badge, demand, "each demanding transition is named with its badge")
        self.assertIn("memorized formula", demand, "and with the reason it is demanding")
        equation = next(b for b in blocks if b["kind"] == "EQUATION")
        self.assertTrue(equation["conditions"], "a relation without its conditions is not a map")

    def test_core2_takes_custody_of_every_question_the_bucket_holds(self):
        compiled = self.compile()
        custody = next(p for p in compiled["plan"]["products"] if p["core"] == "CORE2")
        held = {b["source_question_id"] for b in custody["units"][0]["blocks"]}
        self.assertEqual(held, {q["id"] for q in compiled["source"]["questions"]})
        for block in custody["units"][0]["blocks"]:
            self.assertEqual(block["exposure_role"], "SOURCE_CUSTODY",
                             "custody is not a teaching decision about how a question is used")

    def test_a_question_binding_an_unknown_datum_is_rejected(self):
        data = packages()
        for question in data[0]["questions"]:
            if question["id"] == "Q-AUTHOR-REL-01":
                question["verification"]["bindings"]["vx"] = "DAT-NO-SUCH-VALUE"
        with self.assertRaises(ContractError) as caught:
            compile_bucket(build_index(data), "BUCKET-RELATIVE-MOTION", topic_id="T", title="T",
                           subject="Physics",
                           practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})
        self.assertEqual(caught.exception.code, "QUESTION_BINDS_UNKNOWN_DATUM")


if __name__ == "__main__":
    unittest.main()


class SubstanceGate(unittest.TestCase):
    """Records must discriminate. Fixtures are the real defects from the parallel tracks.

    The strings below are quoted verbatim from the subtopic-intelligence packets in
    reallaksh19/Common PR #402 and #403, where they appear on 31 and 52 packets
    respectively while passing that track's own six-point intake gate. They are data
    here, not instructions, and they are what this gate was built to reject.
    """

    def _corpus(self, *records):
        return {r["id"]: {"_collection": "microtopics", **r} for r in records}

    def test_the_committed_libraries_are_clean(self):
        # A gate that fires on authored content gets switched off, so this comes first.
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            with self.subTest(package=path.name):
                package = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(substance.findings(intake.corpus(package)), [])

    def test_the_same_sentence_on_two_records_is_caught(self):
        shared = "Ignoring boundary constraints or applying naive scalar intuition."
        found = substance.findings(self._corpus(
            {"id": "MIC-A", "title": "First", "misconceptions": [{"wrong_idea": shared}]},
            {"id": "MIC-B", "title": "Second", "misconceptions": [{"wrong_idea": shared}]}))
        self.assertEqual({f["point"] for f in found}, {"DUPLICATED"})
        self.assertEqual({f["record"] for f in found}, {"MIC-A", "MIC-B"})

    def test_every_site_is_reported_not_only_the_first(self):
        # An earlier version attributed a shared string to one record, so text repeated
        # across 31 packets reported 4 of 43 as defective and passed the other 27.
        shared = "Apply rigorous vector decomposition and conservation boundaries."
        records = self._corpus(*[{"id": f"MIC-{n}", "title": f"Topic {n}",
                                  "inferential_jump": shared} for n in range(8)])
        found = substance.findings(records)
        self.assertEqual({f["record"] for f in found}, set(records))

    def test_a_template_with_the_title_substituted_in_is_caught(self):
        found = substance.findings(self._corpus(
            {"id": "MIC-A", "title": "Projectile motion",
             "inferential_jump": "Standard problem scaffold for Projectile motion. "
                                 "Given system parameters, evaluate the response."},
            {"id": "MIC-B", "title": "Rotational dynamics",
             "inferential_jump": "Standard problem scaffold for Rotational dynamics. "
                                 "Given system parameters, evaluate the response."}))
        self.assertEqual({f["point"] for f in found}, {"TEMPLATED"})
        self.assertEqual({f["record"] for f in found}, {"MIC-A", "MIC-B"})

    def test_a_phrase_that_only_names_its_own_type_is_caught(self):
        found = substance.findings({
            "REL-A": {"_collection": "relations", "kind": "RELATION",
                      "statement": "Governing relation."},
            "INV-B": {"_collection": "relations", "kind": "INVARIANT",
                      "statement": "System invariant."}})
        self.assertEqual({f["point"] for f in found}, {"SELF_NAMING"})
        self.assertEqual({f["record"] for f in found}, {"REL-A", "INV-B"})

    def test_a_package_carrying_a_planted_duplicate_is_refused_by_intake(self):
        path = sorted(REPO.glob("*/library/*.v1.json"))[0]
        package = json.loads(path.read_text(encoding="utf-8"))
        first, second = package["microtopics"][0], package["microtopics"][1]
        second["inferential_jump"] = first["inferential_jump"]
        report = intake.check(package)
        self.assertFalse(report["admitted"])
        self.assertIn("DUPLICATED", {f["point"] for f in report["findings"]})


class SubstanceGateRestraint(unittest.TestCase):
    """Repetition that is correct must not be reported, or the gate gets ignored."""

    def test_classification_labels_may_repeat(self):
        records = {f"MIC-{n}": {"_collection": "microtopics", "title": f"Topic {n}",
                                "grade_level": "Grade 9-10", "exam_families": ["JEE Advanced"]}
                   for n in range(5)}
        self.assertEqual(substance.findings(records), [])

    def test_shared_validity_conditions_may_repeat(self):
        # Two relations in the same frame really do have the same hypotheses.
        condition = "Use the same observer and state the sign convention before solving."
        records = {f"REL-{n}": {"_collection": "relations", "conditions": [condition]}
                   for n in range(3)}
        self.assertEqual(substance.findings(records), [])

    def test_a_microtopic_may_restate_a_step_of_the_relation_it_teaches(self):
        step = "Subtract the same quantity from both sides, which is reversible."
        found = substance.findings({
            "MIC-A": {"_collection": "microtopics", "teaching_path": [{"action": step}]},
            "REL-A": {"_collection": "relations", "derivation": [step]}})
        self.assertEqual(found, [], "duplication is only compared between peers")


class GateAuthorityOverSubjectTruth(unittest.TestCase):
    """The gate owns the mathematics. The library carries a bound copy, not a rival one.

    Both layers had authored REL-RELATIVE-POSITION independently, under that one id,
    with different expressions and different validity conditions -- the gate requiring
    both positions at the same instant, the library a common time interval. A
    publication compiled from the library was governed by conditions no gate had
    authorised. These hold that closed.
    """

    def _subject(self, name):
        return REPO / name

    def _package(self, subject):
        return json.loads(sorted((subject / "library").glob("*.v1.json"))[0].read_text(encoding="utf-8"))

    def test_every_committed_package_agrees_with_the_gates(self):
        for subject in sorted(REPO.glob("*/adapter/CoreContracts.json")):
            root = subject.parent.parent
            if not (root / "gates").is_dir():
                continue
            with self.subTest(subject=root.name):
                self.assertTrue(authority.audit(root)["passed"], authority.audit(root))

    def test_a_relation_stating_subject_truth_with_no_gate_is_caught(self):
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0].pop("gate_relation_ref")
        package["relations"][0]["expression"] = "q = something no gate declares"
        found = authority.findings(package, authority.gate_relations(subject))
        self.assertIn("GATE_RELATION_BINDING_ABSENT", {f["point"] for f in found})

    def test_redeclaring_a_gate_expression_without_binding_is_caught(self):
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0].pop("gate_relation_ref")
        found = authority.findings(package, authority.gate_relations(subject))
        self.assertIn("SUBJECT_TRUTH_REDECLARED", {f["point"] for f in found})

    def test_a_copy_that_rewrites_the_gate_expression_is_caught(self):
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0]["expression"] = "r_A/B(t) = r_A(t) - r_B(t)"
        found = authority.findings(package, authority.gate_relations(subject))
        self.assertIn("RELATION_EXPRESSION_DIVERGED", {f["point"] for f in found})

    def test_dropping_a_validity_condition_the_gate_requires_is_caught(self):
        # The dangerous direction: a publication used outside the circumstances
        # engineering authorised it for.
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0]["conditions"] = package["relations"][0]["conditions"][1:]
        found = authority.findings(package, authority.gate_relations(subject))
        self.assertIn("VALIDITY_CONDITION_DROPPED", {f["point"] for f in found})

    def test_narrowing_further_than_the_gate_is_allowed(self):
        # Teaching a relation in fewer circumstances than it holds is a teaching
        # decision. Widening would be a claim about the subject, and is what is barred.
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0]["conditions"] = package["relations"][0]["conditions"] + [
            "Only whole-number component values appear at this level."]
        self.assertEqual(authority.findings(package, authority.gate_relations(subject)), [])

    def test_binding_to_a_gate_relation_that_does_not_exist_is_caught(self):
        subject = self._subject("Physics")
        package = self._package(subject)
        package["relations"][0]["gate_relation_ref"] = "REL-NO-SUCH-THING"
        found = authority.findings(package, authority.gate_relations(subject))
        self.assertIn("GATE_RELATION_UNKNOWN", {f["point"] for f in found})

    def test_a_gate_reference_is_not_treated_as_a_dangling_library_reference(self):
        # It deliberately points outside the library; resolving it internally would
        # report every correctly bound relation as unresolved.
        packages = [json.loads(p.read_text(encoding="utf-8")) for p in PACKAGES]
        self.assertEqual(unresolved(build_index(packages)), [])


class StepsMustDemonstrate(unittest.TestCase):
    """A step that changes the state must show the changed state, not describe it.

    The distinction needs the step's declared role to be sound. Applied to every step
    regardless of role it misfired on roughly a quarter of the authored ones, all of
    them declarations: "x ranges over the rationals." is a correct output for a step
    whose whole job is to fix the domain.
    """

    def _step(self, role, output):
        return {"MIC-A": {"_collection": "microtopics", "teaching_path": [
            {"id": "S-1", "role": role, "action": "Do something.", "why_valid": "Because.",
             "inputs": [], "output": output}]}}

    def test_the_committed_packages_have_no_named_only_transforms(self):
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            with self.subTest(package=path.name):
                package = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(substance.step_findings(intake.corpus(package)), [])

    def test_a_transform_that_describes_its_outcome_is_caught(self):
        found = substance.step_findings(self._step("TRANSFORM", "A verified solution."))
        self.assertEqual([f["point"] for f in found], ["NAMED_WITHOUT_DEMONSTRATING"])

    def test_a_transform_that_shows_the_changed_state_passes(self):
        self.assertEqual(substance.step_findings(self._step("TRANSFORM", "a*x = c - b")), [])

    def test_a_transform_demonstrated_in_words_and_numerals_passes(self):
        # "3 times 7/3, plus 2, is exactly 9." is a demonstration, written out.
        found = substance.step_findings(
            self._step("TRANSFORM", "3 times 7/3, plus 2, is exactly 9."))
        self.assertEqual(found, [])

    def test_a_declaration_producing_a_convention_is_not_a_transform(self):
        for output in ("x ranges over the rationals.",
                       "Declared frame: east positive, north positive."):
            with self.subTest(output=output):
                self.assertEqual(substance.step_findings(self._step("DECLARE", output)), [])

    def test_every_committed_step_declares_a_role(self):
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            package = json.loads(path.read_text(encoding="utf-8"))
            steps = [s for m in package["microtopics"] for s in m.get("teaching_path", [])]
            steps += [s for r in package.get("relations", []) for s in r.get("derivation", [])]
            self.assertTrue(steps)
            for step in steps:
                self.assertIn(step.get("role"), {"DECLARE", "TRANSFORM", "VERIFY"},
                              f'{path.name}:{step["id"]}')


class ExitAnswersHaveCustody(unittest.TestCase):
    """The answer a learner measures themselves against must stand behind itself.

    Every question carried a validator binding; no exit task did. Eight exit answers
    asserted computed results -- "x = 3", "P-Q = (6,-8) m/s, magnitude 10 m/s" -- with
    nothing behind them, so the self-check answer had less custody than the practice
    answer, which is the wrong way round.
    """

    def _package(self):
        return json.loads(sorted(REPO.glob("Mathematics/library/*.v1.json"))[0]
                          .read_text(encoding="utf-8"))

    def test_every_committed_exit_task_declares_its_custody(self):
        seen = collections.Counter()
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            package = json.loads(path.read_text(encoding="utf-8"))
            for row in package["microtopics"]:
                oracle = (row.get("exit_task") or {}).get("oracle")
                self.assertIsNotNone(oracle, f'{path.name}:{row["id"]}')
                self.assertEqual(len(oracle), 1, f'{path.name}:{row["id"]}')
                seen[next(iter(oracle))] += 1
        self.assertTrue(seen["verification"], "no exit answer is machine-checked at all")

    def test_an_exit_task_with_no_oracle_declared_is_refused(self):
        package = self._package()
        package["microtopics"][0]["exit_task"].pop("oracle")
        self.assertFalse(check(package)["admitted"])

    def test_holding_against_an_issue_the_package_never_declares_is_refused(self):
        package = self._package()
        package["microtopics"][0]["exit_task"]["oracle"] = {"held_by": "ISS-DOES-NOT-EXIST"}
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertIn("EXIT_ORACLE", {f["point"] for f in report["findings"]})

    def test_binding_an_oracle_to_a_datum_that_does_not_exist_is_refused(self):
        package = self._package()
        package["microtopics"][0]["exit_task"]["oracle"] = {
            "verification": {"validator_id": "LINEAR_EQUATION",
                             "bindings": {"a": "DAT-NOT-DECLARED"}}}
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertIn("EXIT_ORACLE", {f["point"] for f in report["findings"]})

    def test_the_verified_exit_answers_recompute_to_what_they_claim(self):
        # The point of the binding: the oracle actually returns the stated answer.
        from Mathematics.adapter.validator import recompute as math_recompute
        package = self._package()
        data = {d["id"]: d["value"] for d in package["data"]}
        row = next(m for m in package["microtopics"] if m["id"] == "MIC-MATH-EXACT-SOLUTION")
        spec = row["exit_task"]["oracle"]["verification"]
        case = {k: v for k, v in spec.items() if k != "bindings"}
        case.update({name: data[datum] for name, datum in spec["bindings"].items()})
        self.assertEqual(str(math_recompute(case)), "7/3")
        self.assertIn("7/3", row["exit_task"]["answer"]["summary"])


class ComposedProseReadsAsProse(unittest.TestCase):
    """A sentence embedded inside another sentence reached the learner's page.

    "This gives For x = 2: 3(2) + 2 = 8" and "A common wrong idea is that The equals
    sign means..." both shipped. Lead-ins ending in a colon never had the defect --
    a capital after a colon is correct -- so only the two word-final joins changed.
    """

    def compiled_text(self, core):
        compiled = compile_bucket(math_records(), BUCKET_MATH, topic_id="T", title="T",
                                  subject="Mathematics",
                                  practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})
        product = next(p for p in compiled["plan"]["products"] if p["core"] == core)
        return "\n".join(b.get("text", "") for b in product["units"][0]["blocks"])

    def test_a_fragment_stays_inside_its_lead_in(self):
        self.assertEqual(join("This gives", "a*x = c - b"), ["This gives a*x = c - b."])

    def test_a_sentence_takes_its_own_line_and_keeps_its_capital(self):
        self.assertEqual(join("This gives", "For x = 2: 3(2) + 2 = 8, and the right side is 9."),
                         ["This gives:", "For x = 2: 3(2) + 2 = 8, and the right side is 9."])

    def test_no_composed_line_embeds_a_sentence_mid_sentence(self):
        # This began as a list of lead-in words -- gives, that, is, means -- and that was
        # the wrong shape for the assertion. It passed a line reading "That shows
        # Treating membership of the solution set as..." written months later by code
        # using a different lead-in, which is the same defect wearing a word the list did
        # not have. The rule is restated without any word list: a capital may begin a
        # line, or follow a colon or a terminator. Anywhere else, if what follows it runs
        # to the end of the line and is long enough to be a sentence, a sentence has been
        # embedded in a sentence.
        # A list marker starts a line as much as the margin does, and a closing bracket
        # ends a parenthetical rather than a sentence, so both are stripped or allowed
        # before the rule applies. Neither is an exception to the rule: they are what
        # "begins a line" and "follows a terminator" mean in composed text.
        marker = re.compile(r"^(?:[-*\u2022]|\d+\.)\s+")
        for core in ("CORE1", "CORE1A", "CORE1B"):
            for line in self.compiled_text(core).splitlines():
                stripped = marker.sub("", line.strip())
                for found in re.finditer(r"(\S)\s+([A-Z][a-z].*)$", stripped):
                    if found.group(1) in ":.!?)":
                        continue
                    with self.subTest(core=core, line=stripped[:70]):
                        self.assertFalse(is_prose(found.group(2)), stripped)

    def test_a_colon_lead_in_keeps_its_capital_on_the_same_line(self):
        # This named "Predict first:", which R2 removed when Core1B stopped compiling
        # from the declarative text. The property is unchanged and is asserted on the
        # lead-in that carries it now: a capital after a colon is correct English and
        # must not be split onto its own line by the fix for the opposite defect.
        self.assertRegex(self.compiled_text("CORE1B"), r"Our answer: [A-Z0-9]")

    def test_the_wrong_idea_and_its_repair_are_separate_and_both_labelled(self):
        # They were run together on one line, two sentences pretending to be one.
        text = self.compiled_text("CORE1B")
        self.assertIn("A common wrong idea:", text)
        self.assertIn("Instead:", text)


class FiguresSitWithWhatTheyExplain(unittest.TestCase):
    """A figure appended after every text block explains an argument already read."""

    def compile_with_figure_on(self, microtopic_id):
        """Move the figure to another microtopic, carrying the relation its data hangs on.

        Re-pointing the figure alone is refused by the authority gate, correctly: a
        figure bound to a microtopic whose obligation does not carry its data is a
        figure attached to teaching it does not illustrate.
        """
        data = math_records()
        instance = copy.deepcopy(data["REP-MATH-NUMBER-LINE"]["scene_instances"][0])
        instance["microtopic_ref"] = microtopic_id
        data["REP-MATH-NUMBER-LINE"] = {**data["REP-MATH-NUMBER-LINE"],
                                        "scene_instances": [instance]}
        target = dict(data[microtopic_id])
        target["relation_refs"] = sorted({*target.get("relation_refs", []), "REL-MATH-EXACTNESS"})
        data[microtopic_id] = target
        return compile_bucket(data, BUCKET_MATH, topic_id="T", title="T", subject="Mathematics",
                              practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})

    def test_a_figure_follows_the_microtopic_it_is_bound_to(self):
        # Bound to the *first* microtopic, so landing last would be the old behaviour
        # rather than a coincidence of this bucket's ordering.
        compiled = self.compile_with_figure_on("MIC-MATH-CONSTRAINT")
        blocks = next(p for p in compiled["plan"]["products"]
                      if p["core"] == "CORE1A")["units"][0]["blocks"]
        kinds = [b["kind"] for b in blocks]
        self.assertEqual(kinds.index("FIGURE"), 1, kinds)
        self.assertEqual(blocks[0]["obligation_ids"], blocks[1]["obligation_ids"])

    def test_every_figure_sits_next_to_a_block_sharing_its_obligation(self):
        compiled = self.compile_with_figure_on("MIC-MATH-EQUIVALENT-OPS")
        for product in compiled["plan"]["products"]:
            blocks = product["units"][0]["blocks"]
            for index, block in enumerate(blocks):
                if block["kind"] != "FIGURE" or index == 0:
                    continue
                self.assertEqual(blocks[index - 1]["obligation_ids"], block["obligation_ids"],
                                 f'{product["core"]} block {index}')


    def test_a_figure_for_another_buckets_microtopic_is_not_reassigned_here(self):
        """Found by the A/B check two products downstream, not by reading this code.

        _figure_blocks fell back to the practice obligation whenever a scene instance's
        microtopic produced no obligation -- including when the microtopic simply belongs
        to a different bucket. A figure about one bucket's mathematics then appeared in
        another bucket's practice section, in the declarative product only, and the
        differentiation gate reported it as CORE1A covering an obligation CORE1B did not.
        The function's own docstring already said this case must not be dropped silently.
        """
        records = build_index([json.loads(p.read_text(encoding="utf-8"))
                               for p in sorted((REPO / "Physics/library").glob("*.json"))])
        compiled = compile_bucket(records, "BUCKET-RELATIVE-MOTION", topic_id="t", title="t",
                                  subject="Physics",
                                  practice_control={"mode": "DESIGN_PREVIEW",
                                                    "purpose": "PRACTICE"})
        foreign = {"SI-VECTOR-COMPONENTS", "SI-VECTOR-SUBTRACTION"}
        for product in compiled["plan"]["products"]:
            for block in product["units"][0]["blocks"]:
                if block["kind"] != "FIGURE":
                    continue
                with self.subTest(core=product["core"], block=block["id"]):
                    self.assertFalse(foreign & {block["id"].split("-", 1)[1]}, block["id"])
        self.assertTrue(differentiation.audit(compiled["plan"])["differentiated"])

    def test_a_figure_whose_core_is_not_taught_still_reaches_the_practice_slot(self):
        # The fallback is legitimate for the case it was written for, and removing it
        # entirely would have lost practice figures. Only the out-of-bucket case changed.
        records = build_index([json.loads(p.read_text(encoding="utf-8"))
                               for p in sorted((REPO / "Mathematics/library").glob("*.json"))])
        instance = copy.deepcopy(records["REP-MATH-NUMBER-LINE"]["scene_instances"][0])
        instance["cores"] = ["CORE2A"]
        records["REP-MATH-NUMBER-LINE"] = {**records["REP-MATH-NUMBER-LINE"],
                                           "scene_instances": [instance]}
        compiled = compile_bucket(records, BUCKET_MATH, topic_id="t", title="t",
                                  subject="Mathematics",
                                  practice_control={"mode": "DESIGN_PREVIEW",
                                                    "purpose": "PRACTICE"})
        practice = next(p for p in compiled["plan"]["products"] if p["core"] == "CORE2A")
        figures = [b for b in practice["units"][0]["blocks"] if b["kind"] == "FIGURE"]
        self.assertEqual(len(figures), 1)
        self.assertEqual(figures[0]["obligation_ids"], ["OB-BUCKET-LINEAR-EQUATION-PRACTICE"])

class FieldsAddedMustCarryWhatTheyPromise(unittest.TestCase):
    """R1 added fields whose whole value is a claim the schema can hold but not check.

    `reveals` says how far a hint goes, `difficult_move` says which step is the hard
    one, `closure` says which of three forms closes an attempt. Each is exactly the
    kind of field that can lie -- and a field that can lie is worse than no field,
    because a gate downstream will trust it. Every one is planted here, on a package
    that admits without it.
    """

    def package(self):
        return json.loads(MATH_PACKAGES[0].read_text(encoding="utf-8"))

    def question(self, package, index=0):
        return package["questions"][index]

    def test_the_committed_packages_still_admit_with_none_of_the_new_fields_set(self):
        # The fields are optional. Adding them must not have invalidated what exists.
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            with self.subTest(package=path.name):
                self.assertTrue(check(json.loads(path.read_text(encoding="utf-8")))["admitted"])

    def test_a_hint_revealing_the_answer_before_the_last_rung_is_refused(self):
        package = self.package()
        self.question(package)["hints"] = [
            {"text": "Which side is the unknown on?", "reveals": "ANSWER"},
            {"text": "Substitute and compare both sides.", "reveals": "METHOD"}]
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "HINT_LADDER" for f in report["findings"]),
                        report["findings"])

    def test_the_same_hint_in_the_last_position_is_allowed(self):
        # The rule is about position, not about revealing the answer at all: a ladder
        # whose final rung gives the answer is a ladder, not a defect.
        package = self.package()
        self.question(package)["hints"] = [
            {"text": "Substitute and compare both sides.", "reveals": "METHOD"},
            {"text": "x = 7/3.", "reveals": "ANSWER"}]
        self.assertTrue(check(package)["admitted"], check(package)["findings"])

    def test_a_difficult_move_index_outside_the_breakdown_is_refused(self):
        package = self.package()
        answer = self.question(package)["answer"]
        answer["difficult_move"] = len(answer["reasoning"])
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "SOLUTION_BREAKDOWN" for f in report["findings"]),
                        report["findings"])

    def test_an_index_inside_the_breakdown_is_allowed(self):
        package = self.package()
        self.question(package)["answer"]["difficult_move"] = 0
        self.assertTrue(check(package)["admitted"], check(package)["findings"])

    def test_a_transfer_claim_naming_an_undeclared_lineage_is_refused(self):
        package = self.package()
        self.question(package)["transfer"] = {
            "dimension": "model_choice",
            "statement": "The relation to apply is no longer named in the stem.",
            "builds_on": ["MIC-NOT-IN-THIS-PACKAGE"]}
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "TRANSFER" for f in report["findings"]),
                        report["findings"])

    def test_a_repair_route_pointing_nowhere_is_refused(self):
        package = self.package()
        self.question(package)["repair_ref"] = "STEP-THAT-DOES-NOT-EXIST"
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "TRANSFER" for f in report["findings"]),
                        report["findings"])

    def test_a_repair_route_pointing_at_a_real_teaching_step_is_allowed(self):
        package = self.package()
        step = package["microtopics"][0]["teaching_path"][0]["id"]
        self.question(package)["repair_ref"] = step
        self.assertTrue(check(package)["admitted"], check(package)["findings"])

    def test_a_declared_closure_with_nothing_behind_it_is_refused(self):
        package = self.package()
        package["microtopics"][0]["elicitation"] = {
            "predict": {"prompt": "Does multiplying both sides by x preserve the solution set?",
                        "defensible_answer": "No, not when x may be zero."},
            "attempt": {"produces": "A statement of when the operation is reversible.",
                        "closure": "RUBRIC"},
            "reconstruct": {"route": [
                {"ask": "What value of the multiplier would destroy information?",
                 "why_this_ask": "It is the one case where the operation is not reversible."}],
                "differs_from_teaching_path": "The learner meets the failing multiplier before "
                                              "any rule about it is stated."},
            "boundary_test": {"prompt": "Multiply both sides of x = 1 by (x - 1).",
                              "answer": "x = 1 still solves it, and x = 1 is now also a root of "
                                        "the multiplied form for a different reason.",
                              "confirms": "That a new root appears when the multiplier can vanish."}}
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "ELICITATION" for f in report["findings"]),
                        report["findings"])

    def test_a_rubric_with_no_rejected_example_is_refused(self):
        package = self.package()
        package["microtopics"][0]["elicitation"] = {
            "predict": {"prompt": "Does multiplying both sides by x preserve the solution set?",
                        "defensible_answer": "No, not when x may be zero."},
            "attempt": {"produces": "A statement of when the operation is reversible.",
                        "closure": "RUBRIC",
                        "rubric": [{"criterion": "Names the multiplier's zero as the failure case.",
                                    "evidence_of": "Reading an operation as conditional on its inputs."}],
                        "accepted": ["It fails when x = 0, because then both sides become 0."]},
            "reconstruct": {"route": [
                {"ask": "What value of the multiplier would destroy information?",
                 "why_this_ask": "It is the one case where the operation is not reversible."}],
                "differs_from_teaching_path": "The learner meets the failing multiplier before "
                                              "any rule about it is stated."},
            "boundary_test": {"prompt": "Multiply both sides of x = 1 by (x - 1).",
                              "answer": "x = 1 still solves it, and x = 1 is now also a root of "
                                        "the multiplied form for a different reason.",
                              "confirms": "That a new root appears when the multiplier can vanish."}}
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "ELICITATION" for f in report["findings"]),
                        report["findings"])


class BMustDemandWorkADoesNot(unittest.TestCase):
    """The A/B rule, made mechanical -- and proven against the product that fails it.

    The check that matters is the last one: today's Core1B, the Core1A-plus-eight-lines
    one, must be refused. A gate that would have passed the product it was built to
    catch proves nothing, so that assertion is written before the product is fixed and
    is expected to be inverted by R2 -- at which point this class keeps the old shape
    as a constructed fixture rather than as the live output.
    """

    def compiled(self):
        return compile_bucket(math_records(), BUCKET_MATH, topic_id="T", title="T",
                              subject="Mathematics",
                              practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})

    def b_unit(self, plan, core="CORE1B"):
        return next(p for p in plan["products"] if p["core"] == core)["units"][0]

    def declarative_shape(self):
        """Core1B as it was: one block per microtopic, carrying the declarative text.

        This was the live product when the check was written, and the check refused it.
        R2 replaced it, so it is kept here as a fixture -- the assertion that matters is
        that this shape is still refused, and it would quietly stop being asserted if it
        were only ever read off whatever the compiler currently emits.
        """
        plan = self.compiled()["plan"]
        unit = self.b_unit(plan)
        unit["blocks"] = [{**block, "id": block["id"] + "-FLAT", "text": "Declarative prose.",
                           "placement": "TEACHING", "reveals_block_id": None}
                          for block in self.b_unit(plan, "CORE1A")["blocks"]]
        for block in unit["blocks"]:
            block.pop("reveals_block_id")
        return plan

    def test_the_shape_core1b_used_to_have_is_refused(self):
        report = differentiation.audit(self.declarative_shape())
        self.assertFalse(report["differentiated"],
                         "the product this check exists to catch would have passed it")
        self.assertEqual({f["point"] for f in report["findings"]},
                         {"OBLIGATION_WITHOUT_ELICITATION"},
                         "every microtopic covered, no commitment asked of the learner")

    def test_core1b_as_it_now_compiles_is_differentiated(self):
        report = differentiation.audit(self.compiled()["plan"])
        self.assertTrue(report["differentiated"], report["findings"])

    def test_every_microtopic_asks_before_it_reveals(self):
        # Not "a reveal exists somewhere": one per microtopic, each naming a prompt that
        # carries the same obligation, so a single elicited concept cannot stand in for
        # the bucket.
        unit = self.b_unit(self.compiled()["plan"])
        blocks = {b["id"]: b for b in unit["blocks"]}
        reveals = [b for b in unit["blocks"] if b.get("placement") == "ELICITED_REVEAL"]
        self.assertTrue(reveals)
        elicited = set()
        for reveal in reveals:
            prompt = blocks[reveal["reveals_block_id"]]
            self.assertEqual(prompt["obligation_ids"], reveal["obligation_ids"])
            elicited |= set(prompt["obligation_ids"])
        covered = {oid for b in unit["blocks"] for oid in b["obligation_ids"]
                   if oid.startswith("OB-MIC-")}
        self.assertEqual(covered, elicited & covered)

    def test_a_reveal_naming_no_prompt_is_refused(self):
        plan = self.compiled()["plan"]
        unit = self.b_unit(plan)
        unit["blocks"].append({**unit["blocks"][0], "id": "B-REVEAL", "placement": "ELICITED_REVEAL",
                               "reveals_block_id": "B-PROMPT-THAT-DOES-NOT-EXIST"})
        self.assertIn("REVEAL_WITHOUT_PROMPT",
                      {f["point"] for f in differentiation.findings(plan)})

    def test_a_reveal_placed_before_its_prompt_is_refused(self):
        plan = self.compiled()["plan"]
        unit = self.b_unit(plan)
        prompt = unit["blocks"][-1]
        unit["blocks"].insert(0, {**prompt, "id": "B-REVEAL", "text": "Because the sides differ.",
                                  "placement": "ELICITED_REVEAL", "reveals_block_id": prompt["id"]})
        self.assertIn("REVEAL_BEFORE_PROMPT",
                      {f["point"] for f in differentiation.findings(plan)})

    def test_a_prompt_that_already_contains_its_own_answer_is_refused(self):
        # Today's defect in miniature: the prediction and the thing it predicts, in one
        # block, so a learner reads the answer while reading the question.
        plan = self.compiled()["plan"]
        unit = self.b_unit(plan)
        prompt = dict(unit["blocks"][0])
        prompt["id"], prompt["text"] = "B-PROMPT", "Does x = 2 satisfy it? No: the sides differ."
        unit["blocks"] = [prompt, {**prompt, "id": "B-REVEAL", "text": "No: the sides differ.",
                                   "placement": "ELICITED_REVEAL", "reveals_block_id": "B-PROMPT"}]
        self.assertIn("PROMPT_ANSWERED_IN_PLACE",
                      {f["point"] for f in differentiation.findings(plan)})

    def test_dropping_a_concept_from_b_is_refused(self):
        # The one resolution the spec names and forbids: solving the authoring problem
        # by eliciting less than the A product constructs.
        plan = self.compiled()["plan"]
        unit = self.b_unit(plan)
        unit["blocks"] = [b for b in unit["blocks"]
                          if "OB-MIC-MATH-EXACT-SOLUTION" not in b.get("obligation_ids", [])]
        found = [f for f in differentiation.findings(plan) if f["point"] == "COVERAGE_BELOW_A"]
        self.assertEqual([f["block"] for f in found], ["OB-MIC-MATH-EXACT-SOLUTION"])

    def test_repetition_between_a_and_b_is_not_itself_a_finding(self):
        # The invariants say a shared anchor may recur and that similarity is a review
        # trigger, not a verdict. A gate that flagged a B product for quoting its own
        # governing relation would train authors to paraphrase equations.
        plan = self.compiled()["plan"]
        a_unit = self.b_unit(plan, "CORE1A")
        unit = self.b_unit(plan)
        prompt = {**unit["blocks"][0], "id": "B-PROMPT", "text": a_unit["blocks"][0]["text"]}
        unit["blocks"] = [prompt, {**prompt, "id": "B-REVEAL", "text": "A different sentence.",
                                   "placement": "ELICITED_REVEAL", "reveals_block_id": "B-PROMPT"}]
        points = {f["point"] for f in differentiation.findings(plan)}
        self.assertNotIn("PROMPT_ANSWERED_IN_PLACE", points)
        self.assertNotIn("OBLIGATION_WITHOUT_ELICITATION", points)

    def test_a_route_of_statements_cannot_pass_as_a_route_of_asks(self):
        # R1 gave `reconstruct` a home and got its shape wrong on the one field where
        # shape is the whole point: a list of moves is what teaching_path already is,
        # so Core1B compiled from it would have been Core1A under a new key.
        schema = json.loads((REPO / "Shared/library/package.schema.json").read_text(encoding="utf-8"))
        route = (schema["$defs"]["microtopic"]["properties"]["elicitation"]
                 ["properties"]["reconstruct"]["properties"]["route"])
        self.assertEqual(sorted(route["items"]["required"]), ["ask", "why_this_ask"])
        self.assertNotIn("move", route["items"]["properties"])


    def test_core1a_is_untouched_by_the_elicited_product(self):
        # The A/B comparison is only meaningful while one side holds still. Asserted
        # structurally here; asserted byte-for-byte against the previous commit's
        # compiler when R2 landed.
        unit = self.b_unit(self.compiled()["plan"], "CORE1A")
        self.assertTrue(unit["blocks"])
        for block in unit["blocks"]:
            with self.subTest(block=block["id"]):
                self.assertNotEqual(block.get("placement"), "ELICITED_REVEAL")
                self.assertNotIn("reveals_block_id", block)
                self.assertNotIn("Our answer:", block.get("text", ""))

    def test_a_microtopic_with_no_elicitation_falls_back_and_says_so(self):
        # Silence is the failure mode here: falling back to the declarative text without
        # recording it would publish Core1A under Core1B's name and report success.
        data = math_records()
        bare = dict(data["MIC-MATH-CONSTRAINT"])
        bare.pop("elicitation", None)
        data["MIC-MATH-CONSTRAINT"] = bare
        compiled = compile_bucket(data, BUCKET_MATH, topic_id="T", title="T", subject="Mathematics",
                                  practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})
        owed = [r for r in compiled["authoring_requirements"]
                if r["kind"] == "ELICITATION_AUTHORING"]
        self.assertEqual([r["detail"].split()[0] for r in owed], ["MIC-MATH-CONSTRAINT"])
        report = differentiation.audit(compiled["plan"])
        self.assertFalse(report["differentiated"],
                         "a fallback microtopic must still fail the A/B check, not be excused by it")

class ElicitationClaimsAreChecked(unittest.TestCase):
    """The A/B claim is checked where it is made, not only where it is rendered."""

    def package(self):
        return json.loads(MATH_PACKAGES[0].read_text(encoding="utf-8"))

    def elicitation(self, differs, route=None):
        return {"predict": {"prompt": "Which side of a*x + b = c may be changed on its own?",
                            "defensible_answer": "Neither: the claim is about both together."},
                "attempt": {"produces": "A rule for what may be done to one side alone.",
                            "closure": "MODEL_RESPONSE",
                            "model_response": "Nothing, unless it is done to the other side too."},
                "reconstruct": {"route": route or [
                    {"ask": "If you add 3 to the left only, is the statement still about the same x?",
                     "why_this_ask": "It forces the learner to test the claim before naming a rule."}],
                    "differs_from_teaching_path": differs},
                "boundary_test": {"prompt": "Multiply both sides of x = 1 by (x - 1).",
                                  "answer": "x = 1 still solves it, and so now does x = 1 vacuously "
                                            "for the multiplied form.",
                                  "confirms": "That an operation which can vanish is not reversible."}}

    def test_a_difference_claim_restating_the_teaching_path_is_refused(self):
        package = self.package()
        row = package["microtopics"][0]
        restated = row["teaching_path"][0]["action"]
        row["elicitation"] = self.elicitation(restated)
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "ELICITATION" for f in report["findings"]),
                        report["findings"])

    def test_a_genuine_difference_claim_is_admitted(self):
        package = self.package()
        package["microtopics"][0]["elicitation"] = self.elicitation(
            "The expert declares the domain first; the learner reaches it only after an "
            "operation has already lost a solution.")
        self.assertTrue(check(package)["admitted"], check(package)["findings"])

    def test_an_ask_arriving_at_a_step_that_does_not_exist_is_refused(self):
        package = self.package()
        row = package["microtopics"][0]
        row["elicitation"] = self.elicitation(
            "The learner reaches the rule by testing it, not by being handed it.",
            route=[{"ask": "What would go wrong if you changed one side alone?",
                    "why_this_ask": "It is the smallest case where the claim can fail.",
                    "from_step_ref": "STEP-NOT-IN-THIS-MICROTOPIC"}])
        report = check(package)
        self.assertFalse(report["admitted"])
        self.assertTrue(any(f["point"] == "ELICITATION" for f in report["findings"]),
                        report["findings"])


class NestedIdsAreAddressableAndUnambiguous(unittest.TestCase):
    """A reference may name a teaching step, so a step id must mean exactly one thing.

    Steps had ids and nothing pointed at them, so two records could share one and it
    cost nothing. `from_step_ref` and `repair_ref` changed that: an unqualified RP-1
    could mean a relation's derivation or a microtopic's teaching path, and the resolver
    would have picked one silently.
    """

    def records(self):
        return build_index([json.loads(p.read_text(encoding="utf-8"))
                            for p in sorted(REPO.glob("*/library/*.v1.json"))])

    def test_a_reference_to_a_teaching_step_resolves(self):
        records = self.records()
        steps = {s["id"] for r in records.values() if r["_collection"] == "microtopics"
                 for s in r.get("teaching_path", [])}
        self.assertTrue(steps)
        self.assertTrue(steps <= resolve_module.addressable(records))

    def test_a_reference_to_nothing_still_does_not_resolve(self):
        # Making nested ids addressable must not make everything addressable.
        records = self.records()
        self.assertNotIn("STEP-THAT-WAS-NEVER-DECLARED", resolve_module.addressable(records))

    def test_a_step_is_not_indexed_as_a_record(self):
        # It has no collection and no provenance of its own; indexing it as a record
        # would put it into every sweep that iterates the library.
        records = self.records()
        step = next(s["id"] for r in records.values() if r["_collection"] == "microtopics"
                    for s in r.get("teaching_path", []))
        self.assertNotIn(step, records)

    def test_the_committed_library_has_no_ambiguous_id(self):
        self.assertEqual(resolve_module.id_collisions(self.records()), [])

    def test_a_planted_collision_is_refused(self):
        # Added rather than renamed: renaming a step that from_step_ref points at breaks
        # the reference first, and would have proved the wrong check fires.
        packages = [json.loads(p.read_text(encoding="utf-8"))
                    for p in sorted(REPO.glob("*/library/*.v1.json"))]
        microtopic = packages[0]["microtopics"][0]
        taken = packages[0]["relations"][0]["derivation"][0]["id"]
        microtopic["teaching_path"].append({**microtopic["teaching_path"][-1], "id": taken})
        with self.assertRaises(ContractError) as raised:
            validate_library(packages)
        self.assertEqual(raised.exception.code, "LIBRARY_NESTED_ID_COLLISION")

    def test_renaming_a_referenced_step_is_caught_as_an_unresolved_reference(self):
        # The other half of the same guarantee: a step id cannot be changed without the
        # references to it being found.
        packages = [json.loads(p.read_text(encoding="utf-8"))
                    for p in sorted(REPO.glob("*/library/*.v1.json"))]
        for row in packages[0]["microtopics"]:
            referenced = {ask.get("from_step_ref") for ask in
                          ((row.get("elicitation") or {}).get("reconstruct") or {}).get("route", [])}
            for step in row["teaching_path"]:
                if step["id"] in referenced:
                    step["id"] += "-RENAMED"
                    with self.assertRaises(ContractError) as raised:
                        validate_library(packages)
                    self.assertEqual(raised.exception.code, "LIBRARY_UNRESOLVED_REFERENCE")
                    return
        self.fail("no elicitation ask points at a teaching step, so this asserts nothing")


class DepictionIsBackedByTheContract(unittest.TestCase):
    """A library may not invent a way of depicting its subject.

    The same authority order as relations, one layer over. Three Physics
    representations declared kind VECTOR_SUBTRACTION, which that contract had never
    heard of, and nothing said so because a kind is only looked up when a scene instance
    renders -- and those three hold none.
    """

    def subject(self, name):
        return REPO / name

    def test_every_committed_representation_is_backed(self):
        for path in sorted(REPO.glob("*/adapter/CoreContracts.json")):
            report = depiction.audit(path.parent.parent)
            with self.subTest(subject=report["subject"]):
                self.assertEqual(report["findings"], [])

    def test_a_kind_the_contract_does_not_declare_is_refused(self):
        records = {"REP-X": {"_collection": "representations", "kind": "INVENTED_KIND",
                             "required_elements": [], "relation_refs": []}}
        found = depiction.findings(records, {"VECTOR": "IMPLEMENTED"})
        self.assertEqual([f["point"] for f in found], ["REPRESENTATION_KIND_UNDECLARED"])

    def test_a_drawn_figure_for_an_unbuilt_kind_is_refused(self):
        # Saying so here is cheaper than saying so at the end of a publish run, which is
        # where FIGURE_FAMILY_UNSUPPORTED catches it today -- after the figure is drawn.
        records = {"REP-X": {"_collection": "representations", "kind": "RAY_DIAGRAM",
                             "required_elements": [], "relation_refs": [],
                             "scene_instances": [{"id": "SI-1"}]}}
        found = depiction.findings(records, {"RAY_DIAGRAM": "PROPOSED"})
        self.assertEqual([f["point"] for f in found], ["SCENE_FOR_UNBUILT_KIND"])

    def test_naming_an_unbuilt_kind_without_drawing_one_is_honest(self):
        records = {"REP-X": {"_collection": "representations", "kind": "RAY_DIAGRAM",
                             "required_elements": [], "relation_refs": []}}
        self.assertEqual(depiction.findings(records, {"RAY_DIAGRAM": "PROPOSED"}), [])

    def test_a_bridge_to_a_part_that_is_not_drawn_is_refused(self):
        # Core1A: "a figure that sits beside the working without being bound to it is
        # decoration". A bridge from an element the figure never contains is that.
        records = {
            "REL-1": {"_collection": "relations", "symbols": [{"symbol": "v_A"}]},
            "REP-X": {"_collection": "representations", "kind": "VECTOR",
                      "required_elements": ["Labelled arrow"], "relation_refs": ["REL-1"],
                      "correspondence": [{"element": "A part nobody draws", "symbol": "v_A",
                                          "in_words": "the speed of A"}]}}
        found = depiction.findings(records, {"VECTOR": "IMPLEMENTED"})
        self.assertEqual([f["point"] for f in found], ["CORRESPONDENCE_ELEMENT_UNKNOWN"])

    def test_a_bridge_to_a_symbol_the_mathematics_does_not_use_is_refused(self):
        records = {
            "REL-1": {"_collection": "relations", "symbols": [{"symbol": "v_A"}]},
            "REP-X": {"_collection": "representations", "kind": "VECTOR",
                      "required_elements": ["Labelled arrow"], "relation_refs": ["REL-1"],
                      "correspondence": [{"element": "Labelled arrow", "symbol": "q",
                                          "in_words": "something else entirely"}]}}
        found = depiction.findings(records, {"VECTOR": "IMPLEMENTED"})
        self.assertEqual([f["point"] for f in found], ["CORRESPONDENCE_SYMBOL_UNKNOWN"])

    def test_a_bridge_naming_both_correctly_passes(self):
        records = {
            "REL-1": {"_collection": "relations", "symbols": [{"symbol": "v_A"}]},
            "REP-X": {"_collection": "representations", "kind": "VECTOR",
                      "required_elements": ["Labelled arrow"], "relation_refs": ["REL-1"],
                      "correspondence": [{"element": "Labelled arrow", "symbol": "v_A",
                                          "in_words": "how fast A goes and which way"}]}}
        self.assertEqual(depiction.findings(records, {"VECTOR": "IMPLEMENTED"}), [])

    def test_a_figure_bound_to_mathematics_with_no_bridge_at_all_is_refused(self):
        records = {
            "REL-1": {"_collection": "relations", "symbols": [{"symbol": "v_A"}]},
            "REP-X": {"_collection": "representations", "kind": "VECTOR",
                      "required_elements": ["Labelled arrow"], "relation_refs": ["REL-1"]}}
        found = depiction.findings(records, {"VECTOR": "IMPLEMENTED"})
        self.assertEqual([f["point"] for f in found], ["CORRESPONDENCE_ABSENT"])

    def test_a_figure_bound_to_no_relation_is_not_asked_for_a_bridge(self):
        # The rule bites where there is mathematics to bridge to. Demanding a bridge from
        # a figure with no bound relation would be demanding one be invented, which is
        # the failure mode every gate here is written to avoid.
        records = {"REP-X": {"_collection": "representations", "kind": "VECTOR",
                             "required_elements": ["Labelled arrow"], "relation_refs": []}}
        self.assertEqual(depiction.findings(records, {"VECTOR": "IMPLEMENTED"}), [])

    def test_every_committed_bridge_names_a_drawn_part_and_a_used_symbol(self):
        # The corpus-level assertion. Both halves are checkable; what stays a reviewer's
        # job is whether the words on the third leg are true, which is how I shipped a
        # row naming the second vector as a component readout before catching it.
        bridges = 0
        for path in sorted(REPO.glob("*/library/*.v1.json")):
            records = build_index([json.loads(path.read_text(encoding="utf-8"))])
            for record in records.values():
                if record.get("_collection") != "representations":
                    continue
                for bridge in record.get("correspondence", []):
                    bridges += 1
                    with self.subTest(figure=record["id"], symbol=bridge["symbol"]):
                        self.assertIn(bridge["element"], record["required_elements"])
                        self.assertIn(bridge["symbol"],
                                      depiction.relation_symbols(records, record))
                        self.assertTrue(bridge["in_words"].strip())
        self.assertGreater(bridges, 0, "nothing is bridged, so this asserts nothing")
