"""Tooling: the manifest is deterministic and detects drift, the guard's exclusion
mechanism requires a reason, and generated web data tells the truth about compilation."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library import compile_inputs  # noqa: E402
from Shared.tools import (  # noqa: E402
    build_manifest, build_web_data, capability_audit, check_subjects,
    capability_collisions, spec_conformance, spec_delivery, topic_independence_guard,
)
from Shared.tools.topic_independence_guard import (  # noqa: E402
    excluded_paths, scan_python, selftest,
)


class Manifest(unittest.TestCase):
    def test_is_deterministic(self):
        self.assertEqual(build_manifest.collect()["digest"], build_manifest.collect()["digest"])

    def test_committed_manifest_matches_the_tree(self):
        committed = json.loads((REPO / "docs/architecture-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(committed["digest"], build_manifest.collect()["digest"],
                         "regenerate with python3 Shared/tools/build_manifest.py")

    def test_collect_does_not_write_to_the_tree(self):
        # It used to regenerate tools/data.js as a side effect, so merely asking what
        # the manifest should be overwrote whatever was in the working copy.
        generated = REPO / "tools/data.js"
        before = generated.read_bytes()
        build_manifest.collect()
        self.assertEqual(generated.read_bytes(), before)

    def test_check_reports_a_stale_generated_file_without_repairing_it(self):
        generated = REPO / "tools/data.js"
        before = generated.read_bytes()
        generated.write_bytes(before + b"// tampered\n")
        try:
            result = subprocess.run([sys.executable, "Shared/tools/build_manifest.py", "--check"],
                                    cwd=REPO, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("tools/data.js", result.stdout)
            self.assertEqual(generated.read_bytes(), before + b"// tampered\n",
                             "a read-only check silently rewrote the file")
        finally:
            generated.write_bytes(before)

    def test_digest_changes_when_a_component_changes(self):
        before = build_manifest.collect()["digest"]
        scratch = REPO / "Shared" / "tools" / "_drift_probe.py"
        scratch.write_text("# temporary component used to prove drift is detected\n", encoding="utf-8")
        try:
            self.assertNotEqual(before, build_manifest.collect()["digest"])
        finally:
            scratch.unlink()
        self.assertEqual(before, build_manifest.collect()["digest"])

    def test_every_component_carries_a_role(self):
        for component in build_manifest.collect()["components"]:
            self.assertTrue(component["role"])
            self.assertTrue(component["role_description"])


class Guard(unittest.TestCase):
    def test_selftest_passes(self):
        self.assertEqual(selftest(), 0)

    def test_exclusions_are_declared_with_reasons(self):
        document = json.loads(
            (REPO / "Shared/tools/topic_independence_allowlist.json").read_text(encoding="utf-8"))
        self.assertTrue(document["exclude_paths"])
        for entry in document["exclude_paths"]:
            self.assertTrue(entry["reason"].strip())
        self.assertIn("tools/data.js", excluded_paths())

    def test_an_exclusion_without_a_reason_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            broken = Path(temp) / "allowlist.json"
            broken.write_text(json.dumps({"exclude_paths": [{"path": "x", "reason": " "}]}),
                              encoding="utf-8")
            import Shared.tools.topic_independence_guard as guard
            original = guard.ALLOWLIST
            guard.ALLOWLIST = broken
            try:
                with self.assertRaises(SystemExit):
                    guard.excluded_paths()
            finally:
                guard.ALLOWLIST = original

    def test_a_planted_literal_is_still_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            planted = Path(temp) / "p.py"
            planted.write_text('def f(x):\n    return x == "PHY-REL-VELOCITY"\n', encoding="utf-8")
            self.assertEqual(len(scan_python(planted, [])), 1)


class WebData(unittest.TestCase):
    def setUp(self):
        self.payload = build_web_data.build()

    def test_every_declared_subject_appears(self):
        contracts = {p.parent.parent.name for p in REPO.glob("*/adapter/CoreContracts.json")}
        self.assertEqual(set(self.payload["subjects"]), contracts)

    def test_every_bucket_carries_an_honest_compile_preview(self):
        for entry in self.payload["subjects"].values():
            for bucket in entry["buckets"]:
                preview = bucket["compile_preview"]
                self.assertIn("compilable", preview)
                if preview["compilable"]:
                    self.assertTrue(preview["supported_products"])
                else:
                    self.assertTrue(preview["code"], "an uncompilable bucket must say why")

    def test_a_subject_without_a_library_is_marked_rather_than_hidden(self):
        without = [name for name, entry in self.payload["subjects"].items()
                   if not entry["library_available"]]
        for name in without:
            self.assertEqual(self.payload["subjects"][name]["buckets"], [])
            self.assertTrue(self.payload["subjects"][name]["contract"]["validator_catalogue"],
                            f"{name} should still declare its contract")

    def test_unsupported_products_are_reported_not_omitted_silently(self):
        physics = self.payload["subjects"].get("Physics", {})
        target = next((b for b in physics.get("buckets", []) if b["compile_preview"]["compilable"]), None)
        self.assertIsNotNone(target)
        requirements = target["compile_preview"]["authoring_requirements"]
        self.assertTrue(any(r["kind"] == "PRODUCT_UNSUPPORTED" for r in requirements))

    def test_generated_file_on_disk_matches_a_fresh_build(self):
        text = (REPO / "tools/data.js").read_text(encoding="utf-8")
        on_disk = json.loads(text[text.index("=") + 1:].rstrip().rstrip(";"))
        self.assertEqual(on_disk, json.loads(json.dumps(self.payload)),
                         "regenerate with python3 Shared/tools/build_web_data.py")


if __name__ == "__main__":
    unittest.main()


class SubjectCoverage(unittest.TestCase):
    """CI once checked one named subject. These hold the discovery honest."""

    def test_every_subject_directory_is_discovered(self):
        found = {p.name for p in check_subjects.subjects()}
        declared = {p.parent.parent.name for p in REPO.glob("*/adapter/CoreContracts.json")}
        self.assertEqual(found, declared)
        self.assertGreater(len(found), 1, "a single-subject sweep proves nothing about neutrality")

    def test_the_sweep_passes_on_the_committed_tree(self):
        report = check_subjects.run()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["subjects_checked"], len(check_subjects.subjects()))

    def test_a_subject_declaring_a_contract_but_no_adapter_is_named_not_skipped(self):
        # A subject can be planned before it is built. That state is reported rather
        # than crashing the sweep or silently counting as checked.
        states = {r["subject"]: r["state"] for r in check_subjects.run()["subjects"]}
        self.assertIn("IMPLEMENTED", states.values())
        for subject in check_subjects.subjects():
            expected = "IMPLEMENTED" if (subject / "adapter/validator.py").is_file() else "CONTRACT_ONLY"
            self.assertEqual(states[subject.name], expected)

    def test_a_hollow_library_in_any_subject_is_caught(self):
        # The falsifier the old CI could not have run: break a subject that is not the
        # one a workflow file happened to name, and the sweep must still fail.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for subject in check_subjects.subjects():
                shutil.copytree(subject, root / subject.name)
            target = sorted(root.glob("*/library/*.json"))[-1]
            package = json.loads(target.read_text(encoding="utf-8"))
            package["microtopics"][0]["inferential_jump"] = ""
            target.write_text(json.dumps(package), encoding="utf-8")
            report = check_subjects.run(root)
            self.assertFalse(report["passed"])
            self.assertTrue(any("INFERENCE" in f for r in report["subjects"] for f in r["findings"]),
                            report)


class GuardRoots(unittest.TestCase):
    """The guard scans what must be neutral, without being told where to look."""

    def test_roots_are_derived_and_exclude_subjects_and_tests(self):
        names = {p.name for p in topic_independence_guard.default_roots()}
        subjects = {p.name for p in check_subjects.subjects()}
        self.assertFalse(names & subjects, "a subject directory is allowed to name its subject")
        self.assertNotIn("tests", names)
        self.assertIn("Shared", names)

    def test_a_new_neutral_directory_is_guarded_without_a_flag(self):
        scratch = REPO / "_guard_root_probe"
        scratch.mkdir()
        try:
            (scratch / "probe.py").write_text("# temporary\n", encoding="utf-8")
            self.assertIn("_guard_root_probe",
                          {p.name for p in topic_independence_guard.default_roots()})
        finally:
            shutil.rmtree(scratch)


class CapabilityClaims(unittest.TestCase):
    """A contract may not claim a capability the repository cannot perform.

    Built before anything was fixed, and it earned that order immediately: an ad-hoc
    survey had counted the unimplemented representation kinds as unbacked claims, when
    every one of them is correctly marked PROPOSED. The gate found three real false
    claims and six that have nowhere to be stated, not eleven of everything.
    """

    def _contract(self, subject="Physics"):
        return json.loads((REPO / subject / "adapter/CoreContracts.json")
                          .read_text(encoding="utf-8"))

    def test_a_status_that_says_proposed_is_not_a_false_claim(self):
        # The honest mechanism already exists for validators and representation kinds.
        report = capability_audit.audit()
        flagged = {f["capability"] for s in report["subjects"] for f in s["findings"]}
        for subject in ("Physics", "Mathematics", "Chemistry"):
            for kind in self._contract(subject)["representation_kinds"]:
                if kind["status"] != "IMPLEMENTED":
                    self.assertNotIn(kind["id"], flagged,
                                     "a capability declared as proposed is honest")

    def test_no_contract_in_the_tree_claims_what_nothing_backs(self):
        report = capability_audit.audit()
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["claims_unbacked"], 0)

    def test_a_product_not_compiled_here_is_honest_rather_than_a_finding(self):
        # Saying so is the point of the field. What must not pass is saying nothing.
        for subject in sorted(REPO.glob("*/adapter/CoreContracts.json")):
            contract = json.loads(subject.read_text(encoding="utf-8"))
            for product, declared in contract["learner_products"].items():
                compiled = declared["production"] == "COMPILED"
                self.assertEqual(compiled, product in compile_inputs.COMPOSABLE, product)
                if not compiled:
                    self.assertTrue(declared.get("reason", "").strip(), product)

    def test_claiming_a_product_is_compiled_when_nothing_builds_it_is_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "Mathematics", root / "Mathematics")
            target = root / "Mathematics/adapter/CoreContracts.json"
            contract = json.loads(target.read_text(encoding="utf-8"))
            contract["learner_products"]["CORE_NO_SUCH_PRODUCT"] = {
                "role": "INVENTED", "production": "COMPILED"}
            target.write_text(json.dumps(contract), encoding="utf-8")
            found = capability_audit.audit_subject(root / "Mathematics")["findings"]
            self.assertIn(("CLAIMED_WITHOUT_CODE", "CORE_NO_SUCH_PRODUCT"),
                          [(f["point"], f["capability"]) for f in found])

    def test_declining_to_say_why_a_product_is_not_compiled_is_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "Mathematics", root / "Mathematics")
            target = root / "Mathematics/adapter/CoreContracts.json"
            contract = json.loads(target.read_text(encoding="utf-8"))
            contract["learner_products"]["CORE_NO_SUCH_PRODUCT"] = {
                "role": "PLANNED", "production": "NOT_COMPILED", "reason": "   "}
            target.write_text(json.dumps(contract), encoding="utf-8")
            found = capability_audit.audit_subject(root / "Mathematics")["findings"]
            self.assertIn(("PRODUCT_NOT_COMPILED_WITHOUT_REASON", "CORE_NO_SUCH_PRODUCT"),
                          [(f["point"], f["capability"]) for f in found])

    def test_planting_a_false_claim_is_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for subject in sorted(REPO.glob("*/adapter/CoreContracts.json")):
                shutil.copytree(subject.parent.parent, root / subject.parent.parent.name)
            target = root / "Mathematics/adapter/CoreContracts.json"
            contract = json.loads(target.read_text(encoding="utf-8"))
            contract["validator_catalogue"].append(
                {"id": "NO_SUCH_FAMILY", "status": "IMPLEMENTED", "inputs": [],
                 "input_units": {}, "requires": [], "proves": "x", "does_not_prove": "y",
                 "result": {"shape": "EXACT_RATIONAL", "unit": "dimensionless",
                            "comparison": "EXACT_RATIONAL_EQUALITY"}})
            target.write_text(json.dumps(contract), encoding="utf-8")
            found = capability_audit.audit_subject(root / "Mathematics")["findings"]
            self.assertIn(("CLAIMED_WITHOUT_CODE", "NO_SUCH_FAMILY"),
                          [(f["point"], f["capability"]) for f in found])

    def test_code_that_outruns_its_contract_is_reported_too(self):
        # The opposite drift: a renderer exists while the contract still calls it proposed.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "Mathematics", root / "Mathematics")
            target = root / "Mathematics/adapter/CoreContracts.json"
            contract = json.loads(target.read_text(encoding="utf-8"))
            for kind in contract["representation_kinds"]:
                if kind["id"] == "NUMBER_LINE":
                    kind["status"] = "PROPOSED"
            target.write_text(json.dumps(contract), encoding="utf-8")
            found = capability_audit.audit_subject(root / "Mathematics")["findings"]
            self.assertIn(("BUILT_BUT_NOT_CLAIMED", "NUMBER_LINE"),
                          [(f["point"], f["capability"]) for f in found])


class SpecConformance(unittest.TestCase):
    """A role spec may not require content the schema has nowhere to keep.

    The checker's own falsifiers plant each finding rather than asserting against the
    real backlog, which shrinks as R1.3 closes it. What is asserted about the real
    tree is that all six specs carry a block and that every path is at least
    well-formed -- a typo must read as a typo, not as a missing field.
    """

    def setUp(self):
        self.schema = json.loads(
            (REPO / spec_conformance.SCHEMA).read_text(encoding="utf-8"))

    def resolve(self, path):
        return spec_conformance.resolve(path, self.schema)[0]

    def test_all_six_role_specs_are_found_from_the_index(self):
        found = [p.name for p in spec_conformance.role_specs()]
        self.assertEqual(len(found), 6, found)
        self.assertNotIn("README.md", found, "the invariants document is not a seventh role")

    def test_every_spec_carries_a_block(self):
        for role in spec_conformance.audit()["roles"]:
            with self.subTest(role=role["role"]):
                self.assertNotIn("SPEC_BLOCK_MISSING",
                                 [f["point"] for f in role["findings"]])
                self.assertGreater(role["required"], 0)

    def test_a_missing_block_is_a_finding_distinct_from_an_empty_one(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = Path(temp) / "CORE1.md"
            spec.write_text("# no block here\n", encoding="utf-8")
            report = spec_conformance.audit_spec(spec, self.schema)
        self.assertEqual([f["point"] for f in report["findings"]], ["SPEC_BLOCK_MISSING"])
        self.assertEqual(report["required"], 0)

    def test_a_field_with_a_home_resolves(self):
        # Paths that must keep resolving whatever else changes: if these break, the
        # checker has stopped walking the schema rather than found a real defect.
        for path in ("microtopic.id", "relation.expression", "question.stem",
                     "microtopic.teaching_path[].why_valid",
                     "representation.scene_instances[].microtopic_ref"):
            with self.subTest(path=path):
                self.assertEqual(self.resolve(path), "", path)

    def test_a_planted_requirement_with_no_home_is_a_finding(self):
        self.assertEqual(self.resolve("microtopic.no_such_field"), "SPEC_FIELD_ABSENT")
        self.assertEqual(self.resolve("microtopic.teaching_path[].no_such_field"),
                         "SPEC_FIELD_ABSENT")

    def test_an_unknown_record_type_is_named_as_such(self):
        # Not SPEC_FIELD_ABSENT: a spec asking about a record that does not exist is a
        # different mistake from one asking for a field that does not exist.
        self.assertEqual(self.resolve("microtopics.id"), "SPEC_ROOT_UNKNOWN")
        self.assertEqual(self.resolve("answer.summary"), "SPEC_ROOT_UNKNOWN",
                         "a nested definition is not a root; a path says which record it starts from")

    def test_an_ordering_requirement_is_not_satisfied_by_a_scalar(self):
        # question.stem exists and is a string. Requiring it as an array must fail:
        # "in their original ordering" cannot be kept in something with no order.
        self.assertEqual(self.resolve("question.stem[]"), "SPEC_FIELD_NOT_ARRAY")

    def test_a_malformed_path_reads_as_malformed(self):
        for path in ("", "question..stem", "question.Stem", "question.stem[", "question[].stem"):
            with self.subTest(path=path):
                self.assertEqual(self.resolve(path), "SPEC_PATH_MALFORMED", path)

    def test_no_committed_path_is_malformed_or_names_an_unknown_record(self):
        # The backlog of absent fields is expected and shrinking. A typo is not.
        for role in spec_conformance.audit()["roles"]:
            for finding in role["findings"]:
                with self.subTest(role=role["role"], path=finding["path"]):
                    self.assertNotIn(finding["point"],
                                     ("SPEC_PATH_MALFORMED", "SPEC_ROOT_UNKNOWN"))

    def test_every_requirement_carries_the_phrase_it_came_from(self):
        # A path with no phrase cannot be checked against the prose by a reviewer,
        # which is the half of this that no gate can do.
        for spec in spec_conformance.role_specs():
            for row in spec_conformance.requirements(spec):
                with self.subTest(spec=spec.name, path=row["path"]):
                    self.assertTrue(row["phrase"], row["path"])

    def test_a_node_with_both_properties_and_a_combinator_keeps_its_properties(self):
        # Found by the gate reporting a field it had just been shown. scene_instance
        # names its fields and then uses anyOf to say that exactly one of two must be
        # present -- the ordinary way to write that -- and the first resolver dropped
        # the node's own properties in favour of the branches'.
        for path in ("representation.scene_instances[].microtopic_ref",
                     "representation.scene_instances[].question_ref",
                     "representation.scene_instances[].datum_refs[]"):
            with self.subTest(path=path):
                self.assertEqual(self.resolve(path), "", path)

    def test_the_whole_backlog_is_closed(self):
        # R1's exit condition. This is the assertion that makes --enforce meaningful:
        # once it holds, a spec requiring something with no home breaks the build.
        report = spec_conformance.audit()
        self.assertEqual(report["without_a_home"], 0,
                         [f for r in report["roles"] for f in r["findings"]])
        self.assertTrue(report["passed"])


class SweepRunsTheDifferentiationCheck(unittest.TestCase):
    """The A/B rule is enforced over every bucket, not only the one a test names.

    It is checked on the compiled plan rather than on the records, because the rule is
    about what a learner is asked to do and in what order, and only the plan says that.
    """

    def test_every_subject_passes_today(self):
        report = check_subjects.run()
        for row in report["subjects"]:
            with self.subTest(subject=row["subject"]):
                self.assertEqual([f for f in row["findings"] if "ELICITATION" in f
                                  or "OBLIGATION_WITHOUT" in f], [])

    def test_every_compilable_bucket_is_actually_checked(self):
        # The failure this prevents is a check that passes because it ran on nothing.
        # Both implemented subjects must contribute at least one bucket.
        for subject in check_subjects.subjects():
            packages = [json.loads(p.read_text(encoding="utf-8"))
                        for p in sorted((subject / "library").glob("*.json"))]
            if not packages:
                continue
            buckets = [b["id"] for package in packages for b in package.get("buckets", [])]
            with self.subTest(subject=subject.name):
                self.assertTrue(buckets)
                self.assertEqual(check_subjects._differentiation_findings(subject, packages), [])

    def test_removing_an_elicitation_makes_the_sweep_fail(self):
        # Planted against a copied tree, because the assertion is that the sweep reports
        # it -- not that some function does when called directly.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("Shared", "Physics", "Mathematics", "Chemistry"):
                shutil.copytree(REPO / name, root / name)
            target = next(root.glob("Mathematics/library/*.json"))
            package = json.loads(target.read_text(encoding="utf-8"))
            for row in package["microtopics"]:
                row.pop("elicitation", None)
            target.write_text(json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8")
            report = check_subjects.run(root)
        self.assertFalse(report["passed"])
        found = [f for row in report["subjects"] for f in row["findings"]
                 if "OBLIGATION_WITHOUT_ELICITATION" in f]
        self.assertEqual(len(found), 3, found)


class SpecDelivery(unittest.TestCase):
    """A requirement must reach the learner, not merely have somewhere to live.

    R1 proved every `requires` path has a schema home. This is the comparison neither
    R1 nor anything else made: does a compiled product carry it. Two products do not,
    and every gate was green over them.
    """

    def setUp(self):
        self.schema = json.loads(
            (REPO / spec_conformance.SCHEMA).read_text(encoding="utf-8"))
        self.roots = spec_conformance.record_types(self.schema)

    def segments(self, path):
        return [spec_conformance.SEGMENT.match(s) for s in path.split(".")]

    def test_a_path_walks_the_arrays_it_crosses(self):
        record = {"teaching_path": [{"why_valid": "first"}, {"why_valid": "second"}]}
        self.assertEqual(
            spec_delivery.values_at(record, self.segments("teaching_path[].why_valid")),
            ["first", "second"])

    def test_a_path_that_is_not_there_yields_nothing_rather_than_raising(self):
        self.assertEqual(spec_delivery.values_at({}, self.segments("a.b[].c")), [])

    def test_a_short_value_is_undecidable_rather_than_guessed(self):
        # A false DELIVERED is the one outcome this tool must never produce: an enum or
        # an id fragment can appear in compiled output by coincidence.
        rows = self.rows_for("Mathematics")
        undecidable = [r for r in rows if r.get("state") == "UNDECIDABLE"]
        self.assertTrue(undecidable)
        for row in undecidable:
            with self.subTest(path=row["path"]):
                held = spec_delivery.authored(self.records("Mathematics"), row["path"], self.roots)
                self.assertLess(max(len(v) for v in held), spec_delivery.DECIDABLE_LENGTH)

    def records(self, subject):
        from Shared.library.resolve import build_index  # noqa: PLC0415
        return build_index([json.loads(p.read_text(encoding="utf-8"))
                            for p in sorted((REPO / subject / "library").glob("*.json"))])

    def rows_for(self, subject):
        report = spec_delivery.audit_subject(REPO / subject, self.schema)
        return report["rows"]

    def test_something_is_delivered_so_the_check_is_not_vacuous(self):
        states = [r.get("state") for r in self.rows_for("Mathematics")]
        self.assertIn("DELIVERED", states)
        self.assertGreater(states.count("DELIVERED"), 10, states)

    def test_core1a_delivers_the_misconception_it_requires(self):
        """The sharpest finding R1.5 made, now closed.

        _teaching_text emitted misconceptions for CORE1B only -- and once Core1B
        compiled from elicitation instead, that branch survived solely as a fallback, so
        the wrong path reached neither product. Core1A's own spec says what that costs:
        "A misconception the learner never hears is a misconception they keep."

        Asserted for both subjects, because the defect was in shared code and fixing it
        for the subject a test happens to name would leave the other broken.
        """
        for subject in ("Mathematics", "Physics"):
            rows = {(r["role"], r["path"]): r["state"]
                    for r in self.rows_for(subject) if "path" in r}
            for field in ("wrong_idea", "diagnostic_prompt", "repair"):
                with self.subTest(subject=subject, field=field):
                    self.assertEqual(rows[("CORE1A", f"microtopic.misconceptions[].{field}")],
                                     "DELIVERED")

    def test_core1a_delivers_what_it_assumes_and_what_can_be_checked(self):
        # The other two Core1A gaps R1.5 found. entry_assumptions is named first in its
        # required content and reached nowhere: a learner who could not do it was on the
        # wrong page with no way to find out.
        for subject in ("Mathematics", "Physics"):
            rows = {(r["role"], r["path"]): r["state"]
                    for r in self.rows_for(subject) if "path" in r}
            for path in ("microtopic.entry_assumptions[]", "relation.checks[]"):
                with self.subTest(subject=subject, path=path):
                    self.assertEqual(rows[("CORE1A", path)], "DELIVERED")

    def test_the_two_products_frame_the_wrong_path_differently(self):
        # Both carry it; that is the coverage rule. They must not carry it identically,
        # which is the A/B rule -- Core1A reveals it inside a completed construction,
        # Core1B poses it as a prediction before anything is revealed.
        from Shared.library.compile_inputs import (  # noqa: PLC0415
            build_index, compile_bucket, load_packages)
        records = build_index(load_packages(sorted((REPO / "Physics/library").glob("*.json"))))
        compiled = compile_bucket(records, "BUCKET-RELATIVE-MOTION", topic_id="t", title="t",
                                  subject="Physics",
                                  practice_control={"mode": "DESIGN_PREVIEW",
                                                    "purpose": "PRACTICE"})
        texts = {p["core"]: "\n".join(b.get("text", "") for b in p["units"][0]["blocks"])
                 for p in compiled["plan"]["products"]}
        self.assertIn("Tell them apart:", texts["CORE1A"])
        self.assertNotIn("Predict first:", texts["CORE1A"])
        self.assertIn("A common wrong idea", texts["CORE1B"])

    def test_hints_are_authored_and_carried(self):
        # Both halves had to move together: authoring hints into a compiler that emits []
        # delivers nothing, and carrying [] delivers nothing. R1.5 asserted the defect
        # in both places; this asserts the fix in both.
        rows = {(r["role"], r["path"]): r["state"]
                for r in self.rows_for("Mathematics") if "path" in r}
        self.assertEqual(rows[("CORE2", "question.hints[]")], "DELIVERED")
        source = (REPO / "Shared/library/compile_inputs.py").read_text(encoding="utf-8")
        self.assertNotIn('"hints": []', source)

    def test_the_compiler_drops_nothing_the_library_holds(self):
        # The enforcement line. A compiler that drops authored content is a defect; a
        # path nobody has written yet is a backlog, counted and named on every run.
        report = spec_delivery.audit()
        self.assertEqual(report["dropped_by_the_compiler"], 0,
                         [f for s in report["subjects"] for f in s["findings"]])
        self.assertTrue(report["passed"])

    def test_the_unwritten_backlog_is_named_rather_than_only_counted(self):
        report = spec_delivery.audit()
        self.assertGreater(report["not_yet_written"], 0, "nothing is owed, so this is vacuous")
        for subject in report["subjects"]:
            for row in subject.get("unwritten", ()):
                with self.subTest(row=row):
                    self.assertGreaterEqual(len(row.split(": ")), 3, row)

    def test_a_container_path_counts_what_is_inside_it(self):
        # The first measurement read a full container as UNAUTHORED, because the walker
        # stopped at it and returned nothing. Seven paths were counted as unwritten with
        # the content sitting inside them.
        record = {"hints": [{"text": "a hint long enough to be found", "reveals": "METHOD"}]}
        self.assertIn("a hint long enough to be found",
                      spec_delivery.values_at(record, self.segments("hints[]")))

    def test_a_role_that_compiles_nothing_here_is_said_once_not_per_requirement(self):
        # Core2B compiles no product for this bucket. Repeating that for each of its
        # eleven requirements would bury the findings that are real.
        rows = self.rows_for("Mathematics")
        core2b = [r for r in rows if r["role"] == "CORE2B"]
        self.assertEqual(core2b, [{"role": "CORE2B", "state": "NOT_COMPILED_HERE"}])


class CapabilityCollisions(unittest.TestCase):
    """One skill must have one id, and a prerequisite must not carry an untaught rung.

    Both findings land on the same two capabilities -- the ones delegated to another
    subject -- which is one root cause with two symptoms.
    """

    def test_the_committed_tree_reports_exactly_the_known_two(self):
        report = capability_collisions.audit()
        self.assertEqual(report["capabilities"], 12)
        forked = {f["capability"] for f in report["findings"]
                  if f["point"] == "CAPABILITY_NAMESPACE_FORKED"}
        untaught = {f["capability"] for f in report["findings"]
                    if f["point"] == "DISCRIMINATION_TAUGHT_BY_NOTHING"}
        self.assertEqual(forked, {"CAP-SIGNED-PAIR", "CAP-RIGHT-TRIANGLE"})
        self.assertEqual(untaught, forked, "the same two, which is the point")

    def test_a_fork_quotes_both_criteria_because_that_is_the_merge_evidence(self):
        # A merge proposal without both texts is not reviewable, and this gate must not
        # merge: collapsing two ids rewrites every prerequisite graph naming either.
        for finding in capability_collisions.audit()["findings"]:
            if finding["point"] != "CAPABILITY_NAMESPACE_FORKED":
                continue
            with self.subTest(stem=finding["capability"]):
                self.assertEqual(len(finding["success_criteria"]), 2)
                for text in finding["success_criteria"].values():
                    self.assertTrue(text.strip())
                self.assertIn("criteria_agree", finding)

    def test_it_reports_rather_than_resolves(self):
        source = (REPO / "Shared/tools/capability_collisions.py").read_text(encoding="utf-8")
        self.assertNotIn("def merge", source)
        self.assertIn("never resolves them", source)

    def test_the_same_id_in_two_packages_is_caught(self):
        declared = {"CAP-X": [{"id": "CAP-X", "_package": "A", "success_criterion": "Do a thing."},
                              {"id": "CAP-X", "_package": "B", "success_criterion": "Do a thing."}]}
        points = [f["point"] for f in capability_collisions.findings(declared, taught=set())]
        self.assertIn("CAPABILITY_DECLARED_TWICE", points)

    def test_a_discrimination_a_microtopic_teaches_is_not_a_finding(self):
        # The guard against the version of this gate I threw away. Matching on "and"
        # fired on 9 of 12 capabilities, 6 wrongly -- "reverse, translate, add
        # tail-to-head, and reconcile" is one composite procedure, not a rider.
        declared = {"CAP-Y": [{"id": "CAP-Y", "_package": "A",
                               "success_criterion": "State a magnitude as nonnegative and a "
                                                    "component as signed, without confusing them."}]}
        self.assertEqual(capability_collisions.findings(declared, taught={"CAP-Y"}), [])
        self.assertEqual([f["point"] for f in
                          capability_collisions.findings(declared, taught=set())],
                         ["DISCRIMINATION_TAUGHT_BY_NOTHING"])

    def test_a_composite_procedure_is_not_mistaken_for_a_rider(self):
        declared = {"CAP-Z": [{"id": "CAP-Z", "_package": "A",
                               "success_criterion": "Reverse the vector, translate it without "
                                                    "rotating, and add tail-to-head."}]}
        self.assertEqual(capability_collisions.findings(declared, taught=set()), [])
