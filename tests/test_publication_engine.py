"""Engine tests: the port preserved behaviour, and the seam is genuinely subject-neutral.

These live outside Shared/ because they legitimately name subjects, which the topic
independence guard forbids inside the engine.
"""
import ast
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Physics.adapter import load as load_physics  # noqa: E402
from Shared.contracts import ContractError  # noqa: E402
from Shared.publication_host.adapter import (  # noqa: E402
    COMPARISONS, Adapter, compare_exact_rational, compare_tolerance,
)
from Shared.publication_host.compose import owner_board  # noqa: E402
from Shared.publication_host.host import publish  # noqa: E402
from Shared.publication_host.inputs import read_inputs  # noqa: E402
from Shared.publication_host.science import numeric_expectation  # noqa: E402
from Shared.publication_host.storage import runtime_files  # noqa: E402
from Shared.tools.republish import (  # noqa: E402
    committed_publications, regenerate, verify,
)

RUN = REPO / "Physics/content/relative-motion-g9"
EXPECTED_BASIS = "e27cbd273f502bb4af65dd448527fbfb14a06d7098ff2637928caa9fa8b7d546"


def fake_adapter(subject, catalogue, recompute=lambda case: 0):
    return Adapter(contract={"subject": subject,
                             "learner_products": {k: k for k in
                                                  ("CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B")},
                             "validator_catalogue": catalogue},
                   recompute=recompute)


class PortRegression(unittest.TestCase):
    """The refactor must not have changed what the engine produces."""

    def test_publishes_with_the_basis_digest_recorded_before_the_port(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "publication"
            result = publish(RUN / "inputs/plan.json", RUN / "inputs/baseline.json",
                             RUN / "inputs", out, load_physics())
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["basis_digest"], EXPECTED_BASIS)
            self.assertEqual(result["numeric_answers_compared"], 7)
            self.assertEqual(result["unverified_numeric_transcriptions_checked"], 0)
            self.assertFalse(result["release_authorized"])

    def test_composed_products_match_the_committed_publication_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "publication"
            publish(RUN / "inputs/plan.json", RUN / "inputs/baseline.json",
                    RUN / "inputs", out, load_physics())
            for name in ("CORE1A.html", "CORE1B.html", "CORE2A.html", "CORE2B.html", "OWNER_BOARD.html"):
                self.assertEqual((out / name).read_bytes(), (RUN / "publication" / name).read_bytes(), name)
            produced = sorted(p.name for p in (out / "figures").iterdir())
            committed = sorted(p.name for p in (RUN / "publication/figures").iterdir())
            # Figure filenames are content digests, so equal names mean equal bytes.
            self.assertEqual(produced, committed)


class CommittedPublications(unittest.TestCase):
    """Every committed run re-verifies, whichever subject owns it.

    A publication carries a snapshot of the engine that produced it. Checking only the
    composed HTML of one named run let that snapshot drift for two phases, so the runs
    are discovered here rather than listed.
    """

    def test_at_least_one_run_is_committed_so_this_sweep_is_not_vacuous(self):
        self.assertTrue(committed_publications(), "nothing committed; the sweep proves nothing")

    def test_every_committed_run_verifies_against_its_own_runtime(self):
        for publication in committed_publications():
            with self.subTest(publication=str(publication.relative_to(REPO))):
                self.assertEqual(verify(publication)["status"], "PASS")

    def _isolated_copy(self, temp):
        """A committed run copied out of the tree, so regeneration can be tested safely."""
        run = Path(temp) / "Physics/content/relative-motion-g9"
        shutil.copytree(RUN, run)
        return run / "publication", Path(temp)

    def test_regeneration_refuses_to_change_what_a_learner_reads(self):
        # A refresh moves the runtime snapshot and evidence, which is routine. Moving
        # the composed pages is a change to the product, and must be asked for.
        with tempfile.TemporaryDirectory() as temp:
            publication, root = self._isolated_copy(temp)
            page = publication / "CORE1A.html"
            page.write_bytes(page.read_bytes().replace(b"</main>", b"<p>edited</p></main>"))
            with self.assertRaises(ContractError) as caught:
                regenerate(publication, repo=root)
            self.assertEqual(caught.exception.code, "PUBLISHED_OUTPUT_WOULD_CHANGE")
            self.assertIn("CORE1A.html", caught.exception.detail)
            self.assertIn(b"edited", page.read_bytes(), "the refusal left the run untouched")

    def test_regeneration_reports_the_change_when_it_is_asked_for(self):
        with tempfile.TemporaryDirectory() as temp:
            publication, root = self._isolated_copy(temp)
            page = publication / "CORE1A.html"
            page.write_bytes(page.read_bytes().replace(b"</main>", b"<p>edited</p></main>"))
            report = regenerate(publication, accept_output_change=True, repo=root)
            self.assertEqual(report["learner_visible_changes"], ["CORE1A.html"])
            self.assertNotIn(b"edited", page.read_bytes(), "the run was rebuilt")

    def test_the_runtime_snapshot_covers_everything_the_engine_imports(self):
        # The snapshot lists the engine explicitly rather than sweeping Shared/, which
        # keeps tooling edits from invalidating published work. That is only safe while
        # the list still covers what the engine actually imports, so this checks it.
        snapshot = set(runtime_files(load_physics()))
        pending, seen = ["Shared.contracts", "Shared.publication_host"], set()
        while pending:
            module = pending.pop()
            if module in seen:
                continue
            seen.add(module)
            base = REPO / Path(module.replace(".", "/"))
            sources = sorted(base.rglob("*.py")) if base.is_dir() else [base.with_suffix(".py")]
            for source in sources:
                relative = source.relative_to(REPO).as_posix()
                self.assertIn(relative, snapshot,
                              f"{relative} is imported by the engine but absent from the snapshot")
                for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                    if isinstance(node, ast.ImportFrom) and node.module and \
                            node.module.startswith("Shared"):
                        pending.append(node.module)
                    elif isinstance(node, ast.ImportFrom) and node.level and node.module:
                        pending.append("Shared.publication_host." + node.module)


class SubjectNeutrality(unittest.TestCase):
    """The engine must carry no subject of its own."""

    def test_owner_board_renders_whatever_subject_the_adapter_declares(self):
        report = {"subject": "Chemistry", "basis_digest": "x", "products": [], "gates": {}}
        self.assertIn("Chemistry publication evidence", owner_board(report))
        self.assertNotIn("Physics", owner_board(report))

    def test_plan_subject_must_match_the_injected_adapter(self):
        plan = json.loads((RUN / "inputs/plan.json").read_text())
        baseline = json.loads((RUN / "inputs/baseline.json").read_text())
        with self.assertRaises(ContractError) as caught:
            read_inputs(plan, baseline, RUN / "inputs", fake_adapter("Mathematics", []))
        self.assertEqual(caught.exception.code, "WRONG_SUBJECT_KIT")


class DeclaredComparisons(unittest.TestCase):
    """Comparison follows the declared strategy, not a single built-in assumption."""

    def test_exact_rational_rejects_what_a_tolerance_would_accept(self):
        # 1/3 versus a 12-digit decimal: inside 1e-9 tolerance, not equal as rationals.
        approximation = "0.333333333333"
        compare_tolerance(1 / 3, approximation)  # tolerance path accepts it
        with self.assertRaises(ContractError) as caught:
            compare_exact_rational("1/3", approximation)
        self.assertEqual(caught.exception.code, "PUBLISHED_ANSWER_MISMATCH")

    def test_every_declared_comparison_in_every_subject_contract_is_implemented(self):
        for contract in sorted(REPO.glob("*/adapter/CoreContracts.json")):
            data = json.loads(contract.read_text(encoding="utf-8"))
            for entry in data["validator_catalogue"]:
                name = entry["result"]["comparison"]
                self.assertIn(name, COMPARISONS, f"{contract.parent.parent.name}:{entry['id']}")

    def test_unknown_declared_comparison_fails_closed(self):
        adapter = fake_adapter("Physics", [{"id": "X", "status": "IMPLEMENTED",
                                            "result": {"shape": "SCALAR_WITH_UNIT", "comparison": "NO_SUCH_RULE"}}])
        with self.assertRaises(ContractError) as caught:
            adapter.comparison_for(adapter.validator("X"))
        self.assertEqual(caught.exception.code, "DECLARED_COMPARISON_UNSUPPORTED")


class UnpublishableResultShapes(unittest.TestCase):
    """An implemented family whose result shape has no rendering is held, not coerced."""

    def _context(self, adapter):
        return {"adapter": adapter,
                "atoms": {"a": {"value": 1, "unit": "u", "kind": "DATUM"}},
                "questions": {("S", "q"): {"verification": {"validator_id": "X", "bindings": {"v": "a"}}}}}

    def _block(self):
        return {"id": "B", "source_id": "S", "source_question_id": "q", "source_atom_ids": ["a"],
                "answer": {"numeric": {"value": 1, "unit": "u"}}}

    def test_a_shape_with_no_rendering_is_held_for_review_rather_than_published(self):
        # Element-count maps have no published representation yet. Coercing one into
        # the scalar path would compare the wrong thing, so it is held instead.
        adapter = fake_adapter("Chemistry", [{"id": "X", "status": "IMPLEMENTED",
                                              "result": {"shape": "ELEMENT_COUNT_MAP",
                                                         "comparison": "EXACT_INTEGER_MAP_EQUALITY"}}])
        outcome = numeric_expectation(self._context(adapter), self._block())
        self.assertEqual(outcome["status"], "SCIENTIFIC_REVIEW_REQUIRED")
        self.assertEqual(outcome["code"], "NUMERIC_RESULT_SHAPE_NOT_PUBLISHABLE")
        self.assertEqual(outcome["oracle"], "NONE")

    def test_exact_rationals_became_publishable_when_a_second_subject_needed_them(self):
        adapter = fake_adapter("Mathematics", [{"id": "X", "status": "IMPLEMENTED",
                                                "result": {"shape": "EXACT_RATIONAL", "unit": "dimensionless",
                                                           "comparison": "EXACT_RATIONAL_EQUALITY"}}])
        self.assertTrue(adapter.publishable(adapter.validator("X")))

    def test_unimplemented_family_is_held_for_review(self):
        adapter = fake_adapter("Chemistry", [{"id": "X", "status": "PROPOSED",
                                              "result": {"shape": "SCALAR_WITH_UNIT",
                                                         "comparison": "RELATIVE_AND_ABSOLUTE_TOLERANCE_1E-9"}}])
        outcome = numeric_expectation(self._context(adapter), self._block())
        self.assertEqual(outcome["status"], "SCIENTIFIC_REVIEW_REQUIRED")
        self.assertEqual(outcome["code"], "NUMERIC_EVALUATOR_UNSUPPORTED")


if __name__ == "__main__":
    unittest.main()
