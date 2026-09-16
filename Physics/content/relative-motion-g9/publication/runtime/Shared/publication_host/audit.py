"""Read actual exported answers/assets and enforce an externally pinned basis."""

from html.parser import HTMLParser
from pathlib import Path

from Shared.contracts import digest, file_digest, load, require, verify_file
from .compose import compose, owner_board, report_for
from .inputs import read_inputs
from .science import compare_candidate
from .storage import runtime_manifest


class PublishedNumbers(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.numbers, self.objects, self.answers = {}, [], []
        self.current = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "data-object-id" in data:
            self.objects.append(data["data-object-id"])
        if "data-answer-id" in data:
            self.answers.append(data["data-answer-id"])
        if "data-answer-value" in data:
            require(tag == "span" and self.current is None, "PUBLISHED_NUMBER_MARKUP_INVALID")
            key = data["data-answer-value"]
            require(key not in self.numbers, "PUBLISHED_NUMBER_DUPLICATE")
            self.numbers[key] = {"value": "", "unit": data.get("data-unit")}
            self.current = key

    def handle_data(self, data):
        if self.current is not None:
            self.numbers[self.current]["value"] += data

    def handle_endtag(self, tag):
        if tag == "span":
            self.current = None


def publication_basis(plan, baseline):
    return digest({"plan": plan, "baseline": baseline})


def verify_publication(root: Path, expected_basis: str, adapter):
    manifest = load(root / "manifest.json")
    plan, baseline = load(root / "inputs/plan.json"), load(root / "inputs/baseline.json")
    require(publication_basis(plan, baseline) == expected_basis == manifest.get("basis_digest"),
            "PUBLICATION_BASIS_MISMATCH")
    runtime = runtime_manifest(adapter)
    require(manifest.get("runtime_digest") == digest(runtime), "PUBLICATION_RUNTIME_STALE")
    require(manifest.get("release_authorized") is False, "MACHINE_CANNOT_AUTHORIZE_RELEASE")
    ctx = read_inputs(plan, baseline, root / "inputs/sources", adapter)
    rendered, evidence = compose(ctx)
    required_files = set(rendered) | {"inputs/plan.json", "inputs/baseline.json", "evidence.json", "OWNER_BOARD.html"}
    required_files |= {"inputs/sources/" + r["path"] for r in baseline["sources"]}
    required_files |= {r["path"] for r in runtime}
    indexed = {row["path"]: row for row in manifest["files"]}
    require(len(indexed) == len(manifest["files"]), "MANIFEST_PATH_COLLISION")
    require(required_files <= set(indexed), "MANIFEST_ARTIFACT_MISSING")
    all_objects, all_answers, all_numbers = [], [], {}
    for product in plan["products"]:
        parser = PublishedNumbers()
        parser.feed((root / (product["core"] + '.html')).read_text(encoding="utf-8"))
        all_objects.extend(parser.objects)
        all_answers.extend(parser.answers)
        require(not (all_numbers.keys() & parser.numbers.keys()), "PUBLISHED_NUMBER_DUPLICATE")
        all_numbers.update(parser.numbers)
    require(len(all_objects) == len(set(all_objects)) and set(all_objects) == set(ctx["objects"]),
            "PUBLISHED_OBJECT_COVERAGE")
    question_ids = {k for k, v in ctx["objects"].items() if v["content"]["kind"] == "QUESTION"}
    require(len(all_answers) == len(set(all_answers)) and set(all_answers) == question_ids,
            "PUBLISHED_ANSWER_CLOSURE")
    require(set(all_numbers) == set(evidence["numeric_answers"]), "PUBLISHED_NUMBER_CLOSURE")
    for key, expected in evidence["numeric_answers"].items():
        actual = all_numbers[key]
        compare_candidate(actual["value"], actual["unit"], expected["value"], expected["unit"])
    for row in manifest["files"]:
        verify_file(root, row)
    for row in runtime:
        verify_file(root, row)
    for name, expected in rendered.items():
        require((root / name).read_text(encoding="utf-8") == expected, "PUBLICATION_COMPOSITION_CHANGED", name)
    report = load(root / "evidence.json")
    expected_report = report_for(ctx, evidence, expected_basis)
    require(report == _json_form(expected_report), "PUBLICATION_EVIDENCE_CHANGED")
    require((root / 'OWNER_BOARD.html').read_text(encoding='utf-8') == owner_board(expected_report),
            "OWNER_BOARD_CHANGED")
    return {"status": "PASS", "scope": "SOURCE_BYTES_OBJECT_CLOSURE_NUMERIC_OUTPUT_COMPOSITION_AND_DIGESTS",
            "basis_digest": expected_basis, "products": [p["core"] for p in plan["products"]],
            "numeric_answers_compared": sum(r['status'] == 'VERIFIED_BY_SUPPORTED_EVALUATOR'
                                             for r in evidence['numeric_answers'].values()),
            "unverified_numeric_transcriptions_checked": sum(r['status'] == 'SCIENTIFIC_REVIEW_REQUIRED'
                                                              for r in evidence['numeric_answers'].values()),
            "scientific_reviews_pending": len(evidence['scientific_review_requirements']),
            "release_authorized": False,
            "academic_review": "NOT_RUN", "visual_review": "NOT_RUN"}


def _json_form(value):
    import json
    return json.loads(json.dumps(value))
