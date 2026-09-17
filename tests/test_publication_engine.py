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


class ElicitedRevealIsClosedAndOrdered(unittest.TestCase):
    """A learner must not be able to read the answer on the way past the question.

    Asserted against the rendered HTML rather than the plan. The plan can say a block is
    a reveal and the renderer can still print it inline, which is the failure this exists
    to catch -- and the one the composed blocks alone cannot show.
    """

    @classmethod
    def setUpClass(cls):
        from Shared.library.compile_inputs import (  # noqa: PLC0415
            build_index, compile_bucket, load_packages, write)
        import importlib  # noqa: PLC0415
        records = build_index(load_packages(sorted((REPO / "Mathematics/library").glob("*.json"))))
        cls.compiled = compile_bucket(records, "BUCKET-LINEAR-EQUATION",
                                      topic_id="linear-equation-g9", title="Linear equations",
                                      subject="Mathematics",
                                      practice_control={"mode": "DESIGN_PREVIEW",
                                                        "purpose": "PRACTICE"})
        cls._temp = tempfile.TemporaryDirectory()
        root = Path(cls._temp.name)
        write(cls.compiled, root / "inputs")
        publish(root / "inputs/plan.json", root / "inputs/baseline.json", root / "inputs",
                root / "publication", importlib.import_module("Mathematics.adapter").load())
        cls.html = (root / "publication/CORE1B.html").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls._temp.cleanup()

    def outside_the_reveals(self):
        import re  # noqa: PLC0415
        return re.sub(r'<details class="reveal">.*?</details>', "", self.html, flags=re.S)

    def test_every_reveal_is_rendered_closed(self):
        self.assertEqual(self.html.count('<details class="reveal">'), 6)
        self.assertNotIn("<details open", self.html)

    def test_the_answer_is_not_readable_without_opening_it(self):
        outside = self.outside_the_reveals()
        for hidden in ("Our answer:", "Getting there:", "A common wrong idea",
                       "It claims something"):
            with self.subTest(hidden=hidden):
                self.assertNotIn(hidden, outside)

    def test_the_question_is_readable_without_opening_anything(self):
        # The other half, and the one a too-eager fix would break: a product that hid the
        # prompt as well would pass the test above and teach nobody.
        self.assertIn("does this line ask you to do something", self.outside_the_reveals())

    def test_the_reveal_is_open_able_rather_than_locked(self):
        # The role wants attempt-first ordering and also says the answer stays accessible
        # rather than locked. <details> is both; a server-side omission would be neither.
        self.assertIn("<summary>Check your answer</summary>", self.html)
        self.assertIn("Our answer:", self.html)


class RevealPlacementIsValidated(unittest.TestCase):
    """The engine refuses a reveal that could not have been read after its prompt."""

    def plan_with(self, mutate):
        import importlib  # noqa: PLC0415
        from Shared.library.compile_inputs import (  # noqa: PLC0415
            build_index, compile_bucket, load_packages, write)
        records = build_index(load_packages(sorted((REPO / "Mathematics/library").glob("*.json"))))
        compiled = compile_bucket(records, "BUCKET-LINEAR-EQUATION", topic_id="t", title="t",
                                  subject="Mathematics",
                                  practice_control={"mode": "DESIGN_PREVIEW",
                                                    "purpose": "PRACTICE"})
        unit = next(p for p in compiled["plan"]["products"]
                    if p["core"] == "CORE1B")["units"][0]
        mutate(unit)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(compiled, root / "inputs")
            with self.assertRaises(ContractError) as raised:
                read_inputs(json.loads((root / "inputs/plan.json").read_text(encoding="utf-8")),
                            json.loads((root / "inputs/baseline.json").read_text(encoding="utf-8")),
                            root / "inputs",
                            importlib.import_module("Mathematics.adapter").load())
        return raised.exception.code

    def test_a_reveal_before_its_prompt_is_refused(self):
        def move_first(unit):
            reveal = next(b for b in unit["blocks"] if b.get("placement") == "ELICITED_REVEAL")
            unit["blocks"].remove(reveal)
            unit["blocks"].insert(0, reveal)
        self.assertEqual(self.plan_with(move_first), "REVEAL_PRECEDES_PROMPT")

    def test_a_reveal_naming_a_block_that_is_not_there_is_refused(self):
        def repoint(unit):
            reveal = next(b for b in unit["blocks"] if b.get("placement") == "ELICITED_REVEAL")
            reveal["reveals_block_id"] = "NO-SUCH-BLOCK"
        self.assertEqual(self.plan_with(repoint), "REVEAL_PROMPT_UNKNOWN")

    def test_a_reveal_whose_prompt_is_itself_hidden_is_refused(self):
        # A prompt inside another reveal has not been read either, so the ordering
        # guarantee would be satisfied on paper and broken on the page.
        def hide_prompt(unit):
            # The *second* prompt is hidden behind the first one, so it still follows
            # what it names and only the readability rule is broken. Pointing it at its
            # own reveal instead would make a cycle and prove the ordering check fires,
            # which is a different assertion.
            reveals = [b for b in unit["blocks"] if b.get("placement") == "ELICITED_REVEAL"]
            first, second = reveals[0], reveals[1]
            prompt = next(b for b in unit["blocks"] if b["id"] == second["reveals_block_id"])
            prompt["placement"] = "ELICITED_REVEAL"
            prompt["reveals_block_id"] = first["reveals_block_id"]
        self.assertEqual(self.plan_with(hide_prompt), "REVEAL_PROMPT_NOT_READABLE")

    def test_an_unknown_placement_is_refused_rather_than_treated_as_teaching(self):
        # The defect this prevents is silent: a typo that fell through to the default
        # would publish a reveal open and report success.
        def typo(unit):
            unit["blocks"][0]["placement"] = "ELICITED_REVEL"
        self.assertEqual(self.plan_with(typo), "CONTENT_PLACEMENT_UNSUPPORTED")


class VectorSubtractionIsAConstruction(unittest.TestCase):
    """P minus Q drawn as a construction, not as a component readout.

    VECTOR draws one vector against axes and would hide the reversal, which is the only
    thing this figure exists to show. The contract records that distinction under this
    kind's `limits`; these assert it is real.
    """

    def scene(self, **overrides):
        spec = {"kind": "VECTOR_SUBTRACTION", "unit": "m/s",
                "x_label": "east (m/s)", "y_label": "north (m/s)",
                "frame": "One common east/north frame.", "caption": "A caption.",
                "minuend": {"symbol": "P", "x_atom": "P-X", "y_atom": "P-Y"},
                "subtrahend": {"symbol": "Q", "x_atom": "Q-X", "y_atom": "Q-Y"},
                "resultant": {"symbol": "P-Q", "x_atom": "R-X", "y_atom": "R-Y"}}
        spec.update(overrides)
        return spec

    def draw(self, values, **overrides):
        from Physics.adapter.scenes import vector_subtraction  # noqa: PLC0415
        atoms = {k: {"id": k, "value": v, "unit": "m/s", "kind": "DATUM"}
                 for k, v in values.items()}
        ctx = {"atoms": atoms}
        block = {"id": "FIG", "source_atom_ids": list(values), "scene": self.scene(**overrides)}
        return vector_subtraction(ctx, block)

    SOUND = {"P-X": 6, "P-Y": 0, "Q-X": 0, "Q-Y": 8, "R-X": 6, "R-Y": -8}

    def test_it_draws_all_four_vectors_of_the_construction(self):
        markup, _ = self.draw(self.SOUND)
        for role in ("minuend", "subtrahend", "reversed_subtrahend", "resultant"):
            with self.subTest(role=role):
                self.assertIn(f'data-vector="{role}"', markup)

    def test_the_reversed_vector_starts_where_the_first_one_ends(self):
        # Tail-to-head, translated without rotation. If it started at the origin the
        # picture would be three arrows from a point, which is the misleading
        # alternative the representation record names.
        _, evidence = self.draw(self.SOUND)
        self.assertIn("reversed_from", evidence)
        self.assertEqual(evidence["minuend"], [6, 0])
        self.assertEqual(evidence["resultant"], [6, -8])

    def test_a_resultant_that_disagrees_with_its_own_operands_is_refused(self):
        # The figure reads the answer from declared data and then checks it. One that
        # computed the answer could never disagree with itself, and so could never catch
        # a library whose stated answer and stated operands are different claims.
        with self.assertRaises(ContractError) as raised:
            self.draw({**self.SOUND, "R-Y": 8})
        self.assertEqual(raised.exception.code, "VECTOR_SUBTRACTION_RESULTANT_DISAGREES")

    def test_a_zero_subtrahend_is_refused(self):
        # Nothing to reverse, so the construction demonstrates nothing -- and drawing it
        # would show a resultant equal to P, teaching that subtraction leaves a vector
        # alone.
        with self.assertRaises(ContractError) as raised:
            self.draw({**self.SOUND, "Q-X": 0, "Q-Y": 0, "R-X": 6, "R-Y": 0})
        self.assertEqual(raised.exception.code, "VECTOR_SUBTRACTION_NOTHING_TO_REVERSE")

    def test_an_operand_missing_its_symbol_or_atoms_is_refused(self):
        for overrides in ({"minuend": {"x_atom": "P-X", "y_atom": "P-Y"}},
                          {"subtrahend": {"symbol": "Q", "y_atom": "Q-Y"}},
                          {"resultant": "P-Q"}):
            with self.subTest(overrides=list(overrides)):
                with self.assertRaises(ContractError) as raised:
                    self.draw(self.SOUND, **overrides)
                self.assertEqual(raised.exception.code, "VECTOR_SUBTRACTION_OPERAND_REQUIRED")

    def test_an_undeclared_frame_or_axis_or_unit_is_refused(self):
        for overrides, code in (({"x_label": ""}, "FIGURE_CONTEXT_REQUIRED"),
                                ({"y_label": ""}, "FIGURE_CONTEXT_REQUIRED"),
                                ({"unit": ""}, "VECTOR_SUBTRACTION_UNIT_REQUIRED")):
            with self.subTest(overrides=list(overrides)):
                with self.assertRaises(ContractError) as raised:
                    self.draw(self.SOUND, **overrides)
                self.assertEqual(raised.exception.code, code)

    def test_it_may_only_draw_values_it_declared_as_its_own_source_atoms(self):
        from Physics.adapter.scenes import vector_subtraction  # noqa: PLC0415
        atoms = {k: {"id": k, "value": v, "unit": "m/s", "kind": "DATUM"}
                 for k, v in self.SOUND.items()}
        block = {"id": "FIG", "source_atom_ids": ["P-X"], "scene": self.scene()}
        with self.assertRaises(ContractError) as raised:
            vector_subtraction({"atoms": atoms}, block)
        self.assertEqual(raised.exception.code, "FIGURE_SOURCE_BINDING_MISSING")

    def test_the_committed_scene_instance_renders_in_a_publication(self):
        # Proven by a scene instance compiled from a library record, never by a
        # hand-authored plan -- which is the rule every renderer here follows.
        import importlib  # noqa: PLC0415
        from Shared.library.compile_inputs import (  # noqa: PLC0415
            build_index, compile_bucket, load_packages, write)
        records = build_index(load_packages(sorted((REPO / "Physics/library").glob("*.json"))))
        compiled = compile_bucket(records, "BUCKET-RELATIVE-MOTION",
                                  topic_id="relative-motion-g9", title="Relative motion",
                                  subject="Physics",
                                  practice_control={"mode": "DESIGN_PREVIEW",
                                                    "purpose": "PRACTICE"})
        self.assertEqual([r for r in compiled["authoring_requirements"]
                          if r["kind"] == "FIGURE_AUTHORING"], [])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(compiled, root / "inputs")
            publish(root / "inputs/plan.json", root / "inputs/baseline.json", root / "inputs",
                    root / "publication", importlib.import_module("Physics.adapter").load())
            svgs = sorted((root / "publication/figures").glob("*.svg"))
            self.assertTrue(svgs)
            body = "".join(s.read_text(encoding="utf-8") for s in svgs)
        self.assertIn('data-vector="reversed_subtrahend"', body)
        self.assertIn(">-v_B<", body)
