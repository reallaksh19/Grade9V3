"""Library layer: intake refuses hollow records, references resolve, maturity is monotone,
and a bucket compiles into inputs that actually publish."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Physics.adapter import load as load_physics  # noqa: E402
from Shared.contracts import ContractError  # noqa: E402
from Shared.library.compile_inputs import compile_bucket, write  # noqa: E402
from Shared.library import intake, substance  # noqa: E402
from Shared.library.intake import check  # noqa: E402
from Shared.library.promote import audit, promote  # noqa: E402
from Shared.library.resolve import (  # noqa: E402
    build_index, slice_for_bucket, unresolved, validate_library,
)
from Shared.publication_host.host import publish  # noqa: E402

PACKAGES = sorted((REPO / "Physics/library").glob("*.json"))


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
        self.assertEqual(result["numeric_answers_compared"], 1)
        self.assertFalse(result["release_authorized"])

    def test_a_product_the_library_cannot_support_is_reported_not_padded(self):
        compiled = self.compile()
        self.assertNotIn("CORE2B", compiled["baseline"]["selected_cores"])
        unsupported = [r for r in compiled["authoring_requirements"] if r["kind"] == "PRODUCT_UNSUPPORTED"]
        self.assertEqual([r["core"] for r in unsupported], ["CORE2B"])

    def test_remaining_authoring_is_declared_rather_than_invented(self):
        kinds = {r["kind"] for r in self.compile()["authoring_requirements"]}
        self.assertIn("FIGURE_AUTHORING", kinds)
        self.assertIn("PROSE_AUTHORING", kinds)

    def test_teaching_text_comes_from_the_library_not_from_a_template(self):
        plan = self.compile()["plan"]
        text = plan["products"][0]["units"][0]["blocks"][0]["text"]
        self.assertIn("r_A/B = r_A - r_B", text)
        self.assertIn("Vector displacements add along consecutive paths", text)

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
