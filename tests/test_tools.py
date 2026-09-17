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

from Shared.tools import (  # noqa: E402
    build_manifest, build_web_data, check_subjects, topic_independence_guard,
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
