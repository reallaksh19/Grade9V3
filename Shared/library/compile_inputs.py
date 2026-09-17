"""Compile publication inputs for one bucket from the library.

This is what makes the library executable rather than stored: the baseline, the
source inventory and the plan skeleton are *derived* from library records, so the
numbers, questions and obligations a product publishes have a governed origin
instead of living in a build script beside the lesson.

What is derived and what is not, stated plainly:

  derived   buckets and their prerequisite edges; obligations from microtopics and
            the teaching routes that claim them; source atoms from the data
            collection; source questions with their answers and any declared
            verification; unit structure and per-core coverage; the teaching text
            the library already holds -- teaching-path steps, misconception repairs
            and exit tasks are authored prose and are carried through verbatim.

  not derived  connecting learner prose beyond what the library holds, and any
            product the library has no content for. These are reported as authoring
            requirements rather than invented. Generating teaching prose from graph
            records would produce exactly the plausible titles concealing missing
            reasoning that the library exists to prevent.

Figures sit on the line between the two. A representation record states what a figure
of its kind must show, which is a requirement, not a figure; a scene instance on that
representation states one actual figure bound to the data it draws, which compiles.
So a representation holding instances yields figure blocks, and one holding none is
reported as figure authoring still outstanding -- per representation, rather than as a
blanket warning on every run.

The compiler never fabricates to fill a gap. A bucket that cannot support a product
is reported unsupported, not padded.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from Shared.contracts import digest, join, load, require, sentence
from Shared.library.resolve import build_index, load_packages, slice_for_bucket

# Core1 and Core2 sit outside the teaching-route mechanism. A route says which product
# teaches a microtopic; these two do not teach it. Core1 is the bucket's map -- its
# objects, its governing relations and where the hard work is -- and Core2 is its
# question custody. Both are determined by what the bucket holds, not by a route.
COMPOSABLE = ("CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B")
ROUTED = ("CORE1A", "CORE1B")
PRACTICE = ("CORE2A", "CORE2B")
BADGE = {"EASY": "EASY", "MEDIUM": "MEDIUM", "HARD": "HARD"}


def _routes_by_core(records: dict) -> dict[str, set[str]]:
    """Which microtopics each core is claimed to teach, from the library's teaching routes."""
    claimed: dict[str, set[str]] = {core: set() for core in COMPOSABLE}
    for record in records.values():
        if record["_collection"] != "teaching_routes":
            continue
        for core in record.get("cores", []):
            if core in claimed:
                claimed[core].update(record.get("microtopic_refs", []))
    return claimed


def _atoms_for(records: dict, microtopic_ids: set[str]) -> list[dict]:
    """Data records reachable from this bucket's microtopics, via their relations."""
    relations = set()
    for mid in microtopic_ids:
        relations.update(records[mid].get("relation_refs", []))
    chosen = []
    for record in records.values():
        if record["_collection"] != "data":
            continue
        relation = record.get("relation_ref")
        if relation is None or relation in relations:
            chosen.append(record)
    return sorted(chosen, key=lambda r: r["id"])


def compile_bucket(records: dict, bucket_id: str, *, topic_id: str, title: str,
                   subject: str, practice_control: dict) -> dict:
    chosen = slice_for_bucket(records, bucket_id)
    microtopics = [records[m] for m in chosen["microtopic_order"]]
    require(microtopics, "LIBRARY_BUCKET_HAS_NO_MICROTOPICS", bucket_id)
    microtopic_ids = {m["id"] for m in microtopics}
    claimed = _routes_by_core(records)
    requirements: list[dict] = []

    # --- source inventory -------------------------------------------------
    atoms, equations = [], {}
    for record in _atoms_for(records, microtopic_ids):
        if record["kind"] == "EQUATION":
            equations[record["relation_ref"]] = record["id"]
            atoms.append({"id": record["id"], "value": record["value"], "kind": "EQUATION",
                          "locator": f'{record["meaning"]} -- {record["locator"]}'})
        else:
            require(record.get("unit"), "LIBRARY_DATUM_WITHOUT_UNIT", record["id"])
            atoms.append({"id": record["id"], "value": record["value"], "unit": record["unit"],
                          "kind": "DATUM", "locator": f'{record["meaning"]} -- {record["locator"]}'})

    questions, question_records = [], []
    for record in records.values():
        if record["_collection"] != "questions":
            continue
        if record.get("primary_capability_ref") not in {c["id"] for c in
                                                        chosen["records"].get("capabilities", [])}:
            continue
        row = {"id": record["id"], "original_number": record["original_identifier"],
               "stem": record["stem"], "conditions": record.get("conditions", [])}
        if record.get("verification"):
            row["verification"] = record["verification"]
            for atom_id in record["verification"]["bindings"].values():
                require(any(a["id"] == atom_id for a in atoms), "QUESTION_BINDS_UNKNOWN_DATUM",
                        f'{record["id"]} -> {atom_id}')
        questions.append(row)
        question_records.append(record)

    source = {"id": "LIBRARY", "origin": "AUTHOR_CREATED",
              "citation": f"Compiled from the {subject} library for bucket {bucket_id}. "
                          "Records are author-created candidates; no source measurement or "
                          "official question provenance is claimed.",
              "atoms": atoms, "questions": questions}

    # --- which products the library can actually support -------------------
    supported, unsupported = [], {}
    relation_ids = {r for m in microtopics for r in m.get("relation_refs", [])}
    for core in COMPOSABLE:
        covered = claimed[core] & microtopic_ids
        if core == "CORE1":
            if relation_ids:
                supported.append(core)
            else:
                unsupported[core] = ("the bucket declares no governing relation, so there is "
                                     "nothing for a map of it to orient a learner to")
        elif core == "CORE2":
            if question_records:
                supported.append(core)
            else:
                unsupported[core] = "the library holds no question for this bucket to take custody of"
        elif core in PRACTICE:
            exposed = [q for q in question_records
                       if any(e.get("core") == core for e in q.get("exposure", []))]
            if exposed:
                supported.append(core)
            else:
                unsupported[core] = "the library holds no question exposed to this product for this bucket"
        elif covered:
            supported.append(core)
        else:
            unsupported[core] = "no teaching route claims this product for this bucket's microtopics"
    require(supported, "LIBRARY_SUPPORTS_NO_PRODUCT", bucket_id)
    for core, reason in unsupported.items():
        requirements.append({"kind": "PRODUCT_UNSUPPORTED", "core": core, "detail": reason})

    # --- baseline ----------------------------------------------------------
    bucket = records[bucket_id]

    # A prerequisite bucket is carried into the baseline as a declared node even though
    # this publication holds no content for it. Dropping the edge would silently erase a
    # real dependency; keeping it says "required, and published elsewhere".
    def bucket_nodes(start: str) -> list[str]:
        ordered, pending = [], [start]
        while pending:
            current = pending.pop()
            if current in ordered:
                continue
            ordered.append(current)
            pending += [p for p in records[current].get("prerequisite_refs", [])
                        if p in records and records[p]["_collection"] == "buckets"]
        return ordered

    node_ids = bucket_nodes(bucket_id)
    bucket_prerequisites = [p for p in bucket.get("prerequisite_refs", [])
                            if p in records and records[p]["_collection"] == "buckets"]
    obligations = []
    for microtopic in microtopics:
        cores = sorted(core for core in supported
                       if microtopic["id"] in claimed[core] or core in ("CORE2A", "CORE2B"))
        relation_atoms = [a["id"] for a in atoms
                          if records[a["id"]].get("relation_ref") in microtopic.get("relation_refs", [])
                          or records[a["id"]].get("relation_ref") is None]
        if not cores or not relation_atoms:
            requirements.append({"kind": "MICROTOPIC_UNBOUND", "microtopic": microtopic["id"],
                                 "detail": "no supported product or no data bound to its relations"})
            continue
        study = [c for c in cores if c in ROUTED]
        if study:
            obligations.append({"id": f'OB-{microtopic["id"]}', "bucket_id": bucket_id,
                                "source_atom_ids": sorted(set(relation_atoms)),
                                "required_cores": study, "required_kinds": ["TEXT"]})
    orientation_obligation = f"OB-{bucket_id}-ORIENTATION"
    if "CORE1" in supported:
        obligations.append({"id": orientation_obligation, "bucket_id": bucket_id,
                            "source_atom_ids": sorted({a["id"] for a in atoms}),
                            "required_cores": ["CORE1"], "required_kinds": ["EQUATION", "TEXT"]})
    custody_obligation = f"OB-{bucket_id}-CUSTODY"
    if "CORE2" in supported:
        obligations.append({"id": custody_obligation, "bucket_id": bucket_id,
                            "source_atom_ids": sorted({a["id"] for a in atoms}),
                            "required_cores": ["CORE2"], "required_kinds": ["QUESTION"]})
    practice = [c for c in supported if c in PRACTICE]
    practice_obligation = f"OB-{bucket_id}-PRACTICE"
    if practice and questions:
        obligations.append({"id": practice_obligation, "bucket_id": bucket_id,
                            "source_atom_ids": sorted({a["id"] for a in atoms}),
                            "required_cores": practice, "required_kinds": ["QUESTION"]})
    require(obligations, "LIBRARY_PRODUCED_NO_OBLIGATIONS", bucket_id)

    accounted = {a for o in obligations for a in o["source_atom_ids"]}
    unaccounted = {a["id"] for a in atoms} - accounted
    atoms[:] = [a for a in atoms if a["id"] in accounted]
    source["atoms"] = atoms
    for atom_id in sorted(unaccounted):
        requirements.append({"kind": "DATUM_UNUSED", "datum": atom_id,
                             "detail": "no obligation binds this value; it was omitted rather than forced in"})

    baseline = {"schema_version": "1.0.0", "topic_id": topic_id,
                "baseline_id": f"BASE-{bucket_id}",
                "selected_cores": supported,
                "sources": [{"id": "LIBRARY", "path": "sources/source.json", "sha256": ""}],
                "buckets": [{"id": node, "badge": BADGE[records[node]["intrinsic_badge"]],
                             "prerequisites": [p for p in records[node].get("prerequisite_refs", [])
                                               if p in node_ids]}
                            for node in node_ids],
                "obligations": obligations,
                "required_questions": [{"core": core, "source_id": "LIBRARY", "question_id": q["id"]}
                                       for core in practice for q in questions
                                       if any(e.get("core") == core for e in
                                              next(r for r in question_records if r["id"] == q["id"])
                                              .get("exposure", []))]}

    # --- figures the library actually holds, and those it only requires -----
    representations = sorted(chosen["records"].get("representations", []), key=lambda r: r["id"])
    for representation in representations:
        instances = representation.get("scene_instances", [])
        if not instances:
            requirements.append({"kind": "FIGURE_AUTHORING", "representation": representation["id"],
                                 "detail": "the representation states what a figure of this kind must show "
                                           "but holds no scene instance; a figure must be authored"})
            continue
        for instance in instances:
            for core in sorted(set(instance["cores"]) - set(supported)):
                requirements.append({"kind": "FIGURE_PRODUCT_UNSUPPORTED", "core": core,
                                     "representation": representation["id"],
                                     "detail": f'scene instance {instance["id"]} targets a product this '
                                               "bucket does not support; it was not drawn"})

    # --- plan skeleton, carrying the prose the library actually holds -------
    plan = {"schema_version": "1.0.0", "subject": subject, "topic_id": topic_id, "title": title,
            "baseline_digest": "", "practice_control": practice_control, "products": []}
    for core in supported:
        blocks, unit_id = [], f"U-{core}-{bucket_id}"
        figures = _figure_blocks(core, representations, obligations, atoms, practice_obligation)
        if core == "CORE1":
            blocks = _orientation_blocks(records, relation_ids, atoms, microtopics,
                                         orientation_obligation, equations)
        elif core == "CORE2":
            # Custody covers every question the bucket holds, not only those a practice
            # product exposes: a question omitted here is a question with no record.
            blocks = [_question_block(core, record, custody_obligation, atoms)
                      for record in question_records]
        elif core in ROUTED:
            for microtopic in microtopics:
                obligation = f'OB-{microtopic["id"]}'
                if not any(o["id"] == obligation and core in o["required_cores"] for o in obligations):
                    continue
                bound = next(o["source_atom_ids"] for o in obligations if o["id"] == obligation)
                blocks.append({"id": f'{core}-{microtopic["id"]}-T', "kind": "TEXT",
                               "obligation_ids": [obligation], "source_atom_ids": bound,
                               "text": _teaching_text(microtopic, core)})
                # A figure belongs with the microtopic it was bound to. Appending every
                # figure after every text block put the one that explains a transition
                # after the whole argument had been read in prose.
                blocks += [b for b in figures if b["obligation_ids"] == [obligation]]
            requirements.append({"kind": "PROSE_AUTHORING", "core": core,
                                 "detail": "blocks carry library-held teaching text; connecting narrative "
                                           "and worked examples still require authoring"})
        else:
            for record in question_records:
                if not any(e.get("core") == core for e in record.get("exposure", [])):
                    continue
                blocks.append(_question_block(core, record, practice_obligation, atoms))
        # Whatever was not placed beside a microtopic -- figures carried by the practice
        # obligation -- belongs with the questions, which is where they already sat.
        blocks += [b for b in figures if b not in blocks]
        if blocks:
            plan["products"].append({"core": core, "units": [
                {"id": unit_id, "bucket_id": bucket_id, "title": bucket["title"], "blocks": blocks}]})

    plan["products"] = [p for p in plan["products"] if p["units"][0]["blocks"]]
    plan["products"].sort(key=lambda p: COMPOSABLE.index(p["core"]))
    baseline["selected_cores"] = [p["core"] for p in plan["products"]]
    return {"baseline": baseline, "source": source, "plan": plan,
            "authoring_requirements": requirements,
            "derived_from": {"bucket": bucket_id, "microtopics": [m["id"] for m in microtopics],
                             "packages": sorted({records[m]["_package"] for m in microtopic_ids})}}


def _teaching_text(microtopic: dict, core: str) -> str:
    """Carry the library's own authored prose; do not synthesise teaching."""
    lines = [sentence(microtopic["title"]), "", microtopic["inferential_jump"]]
    if core == "CORE1B":
        for item in microtopic.get("misconceptions", []):
            # The lead-in was "A common wrong idea is that", which grammatically wants a
            # clause and was handed a sentence: "is that The equals sign means...". The
            # wrong idea and its repair were also run together on one line, which is two
            # sentences pretending to be one.
            lines += ["", f'Predict first: {sentence(item["diagnostic_prompt"])}']
            lines += join("A common wrong idea", item["wrong_idea"])
            lines += join("Instead", item["repair"])
    for step in microtopic.get("teaching_path", []):
        stated = f'{sentence(step["action"])} {sentence(step["why_valid"])}'
        lines += join(f"{stated} This gives", step["output"]) if step.get("output") else [stated]
    exit_task = microtopic.get("exit_task") or {}
    if exit_task.get("prompt"):
        answer = exit_task.get("answer", {})
        lines += ["", f'Check yourself: {exit_task["prompt"]}', f'Answer: {answer.get("summary", "")}']
        lines += [f'- {step}' for step in answer.get("reasoning", [])]
        if answer.get("check"):
            lines.append(f'Verify: {answer["check"]}')
    return "\n".join(lines)


def _orientation_blocks(records: dict, relation_ids: set[str], atoms: list[dict],
                        microtopics: list[dict], obligation: str,
                        equations: dict[str, str]) -> list[dict]:
    """Core1: what the objects are, what the relations say, and where the work is.

    Every part is carried from a record that already holds it. The relation text comes
    from the relation, which is itself a bound copy of the gate that owns it, so a map
    of the bucket cannot state the mathematics differently from the engineering.
    """
    bound = sorted({a["id"] for a in atoms})
    blocks = []
    quantities = [a for a in atoms if a["kind"] == "DATUM"]
    if quantities:
        lines = ["The quantities this bucket works with."]
        lines += [f'{records[a["id"]]["symbol"]}: {records[a["id"]]["meaning"]} '
                  f'({records[a["id"]]["unit"]})' for a in quantities
                  if records[a["id"]].get("symbol")]
        blocks.append({"id": "CORE1-QUANTITIES", "kind": "TEXT", "obligation_ids": [obligation],
                       "source_atom_ids": bound, "text": "\n".join(lines)})
    for relation_id in sorted(relation_ids):
        relation = records[relation_id]
        equation_atom = equations.get(relation_id)
        if not relation.get("mathml") or equation_atom is None:
            continue
        blocks.append({"id": f"CORE1-{relation_id}", "kind": "EQUATION",
                       "obligation_ids": [obligation], "source_atom_ids": [equation_atom],
                       "mathml": relation["mathml"], "meaning": relation["meaning"],
                       "symbols": [f'{s["symbol"]}: {s["meaning"]}'
                                   for s in relation.get("symbols", [])],
                       "conditions": list(relation.get("conditions", []))})
    hard = [m for m in microtopics if m.get("intrinsic_badge") in ("MEDIUM", "HARD")]
    if hard:
        lines = ["Where the hard work is."]
        lines += [f'{sentence(m["title"])} ({m["intrinsic_badge"]}) {m["badge_reason"]}'
                  for m in hard]
        blocks.append({"id": "CORE1-DEMAND", "kind": "TEXT", "obligation_ids": [obligation],
                       "source_atom_ids": bound, "text": "\n".join(lines)})
    return blocks


def _figure_blocks(core: str, representations: list[dict], obligations: list[dict],
                   atoms: list[dict], practice_obligation: str) -> list[dict]:
    """Compile the scene instances the library holds for this product.

    A figure is bound to the obligation of the microtopic it carries, so it counts as
    coverage of that teaching rather than as decoration; in a practice product, where
    the obligation is the bucket's practice one, it is bound there instead. A scene
    instance naming a microtopic that produced no obligation, or data this bucket does
    not carry, is an error in the library and fails here rather than being dropped.
    """
    by_id = {o["id"]: o for o in obligations}
    known = {a["id"] for a in atoms}
    blocks = []
    for representation in representations:
        for instance in representation.get("scene_instances", []):
            if core not in instance["cores"]:
                continue
            wanted = f'OB-{instance["microtopic_ref"]}'
            obligation = wanted if wanted in by_id and core in by_id[wanted]["required_cores"] \
                else practice_obligation
            require(obligation in by_id, "FIGURE_OBLIGATION_MISSING",
                    f'{instance["id"]} -> {wanted}')
            missing = [d for d in instance["datum_refs"] if d not in known]
            require(not missing, "FIGURE_BINDS_UNKNOWN_DATUM",
                    f'{instance["id"]} -> {", ".join(missing)}')
            require(set(instance["datum_refs"]) & set(by_id[obligation]["source_atom_ids"]),
                    "FIGURE_DATA_OUTSIDE_OBLIGATION", f'{instance["id"]} -> {obligation}')
            blocks.append({"id": f'{core}-{instance["id"]}', "kind": "FIGURE",
                           "obligation_ids": [obligation],
                           "source_atom_ids": sorted(instance["datum_refs"]),
                           # One instance can appear in several products. Each block owns
                           # its own copy, so a caller editing one plan block cannot reach
                           # into another product or back into the library record.
                           "scene": deepcopy(instance["scene"])})
    return blocks


def _question_block(core: str, record: dict, obligation_id: str, atoms: list[dict]) -> dict:
    answer = record["answer"]
    # Core2 holds every question in its original form, so it has no exposure entry: it
    # is custody of the source, not a decision about how a question is used in teaching.
    exposure = next((e for e in record.get("exposure", []) if e.get("core") == core), None)
    role = ("SOURCE_CUSTODY" if exposure is None else
            {"PLANNED_WORKED_ANCHOR": "WORKED_EXAMPLE"}.get(exposure.get("role"), "PRACTICE"))
    block = {"id": f'{core}-{record["id"]}', "kind": "QUESTION",
             "obligation_ids": [obligation_id],
             "source_atom_ids": sorted({a["id"] for a in atoms}),
             "source_id": "LIBRARY", "source_question_id": record["id"],
             "original_number": record["original_identifier"], "stem": record["stem"],
             "subparts": [], "options": [], "conditions": record.get("conditions", []),
             "answer": {"summary": answer["summary"], "steps": answer["reasoning"],
                        "check": answer["check"],
                        **({"numeric": answer["numeric"]} if answer.get("numeric") else {})},
             "hints": [], "family": record["family_ref"],
             "learner_action": "solve", "exposure_role": role}
    return block


def write(compiled: dict, out: Path) -> dict:
    """Write inputs, sealing the source digest and baseline digest the host will check."""
    source_path = out / "sources/source.json"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(json.dumps(compiled["source"], indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    import hashlib
    compiled["baseline"]["sources"][0]["sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
    (out / "baseline.json").write_text(
        json.dumps(compiled["baseline"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    compiled["plan"]["baseline_digest"] = digest(compiled["baseline"])
    (out / "plan.json").write_text(
        json.dumps(compiled["plan"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "authoring_requirements.json").write_text(
        json.dumps(compiled["authoring_requirements"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return {"out": str(out), "selected_cores": compiled["baseline"]["selected_cores"],
            "atoms": len(compiled["source"]["atoms"]),
            "questions": len(compiled["source"]["questions"]),
            "obligations": len(compiled["baseline"]["obligations"]),
            "authoring_requirements": len(compiled["authoring_requirements"])}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Compile publication inputs for one bucket from the library")
    parser.add_argument("packages", nargs="+", type=Path)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--topic-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    records = build_index(load_packages(args.packages))
    compiled = compile_bucket(records, args.bucket, topic_id=args.topic_id, title=args.title,
                              subject=args.subject,
                              practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"})
    print(json.dumps(write(compiled, args.out), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
