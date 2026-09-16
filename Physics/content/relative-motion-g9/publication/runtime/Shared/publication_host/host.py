"""The Physics publication transaction: validate, compose, bind, then read back."""

import shutil
from pathlib import Path

from Shared.contracts import digest, file_digest, load, verify_file
from .audit import publication_basis, verify_publication
from .compose import compose, owner_board, report_for
from .inputs import read_inputs
from .storage import build_directory, runtime_files, runtime_manifest, write_json



def publish(plan_path: Path, baseline_path: Path, source_root: Path, out: Path, adapter):
    plan, baseline = load(plan_path), load(baseline_path)
    ctx = read_inputs(plan, baseline, source_root, adapter)
    rendered, evidence = compose(ctx)
    basis = publication_basis(plan, baseline)
    report = report_for(ctx, evidence, basis)

    def write(staging):
        write_json(staging / 'inputs/plan.json', plan)
        write_json(staging / 'inputs/baseline.json', baseline)
        for ref in baseline["sources"]:
            source = verify_file(source_root, ref)
            target = staging / 'inputs/sources' / ref["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for name, source in runtime_files(adapter).items():
            target = staging / 'runtime' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for name, contents in rendered.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(contents, encoding="utf-8")
        write_json(staging / 'evidence.json', report)
        (staging / 'OWNER_BOARD.html').write_text(owner_board(report), encoding="utf-8")
        files = [{"path": str(p.relative_to(staging)), "sha256": file_digest(p)}
                 for p in sorted(staging.rglob('*')) if p.is_file()]
        manifest = {"basis_digest": basis, "runtime_digest": digest(runtime_manifest(adapter)),
                    "files": files, "release_authorized": False,
                    "portable_scope": "EXACT_INPUTS_AND_PUBLISH_VERIFY_COMMANDS; NOT_QUALIFIED_AUTHORING_RESTART"}
        write_json(staging / 'manifest.json', manifest)
        return verify_publication(staging, basis, adapter)

    verified = build_directory(out, write)
    return {**verified, "publication": str(out.resolve()), "owner_board": str(out.resolve() / 'OWNER_BOARD.html')}
