#!/usr/bin/env python3
"""Re-verify, and on request regenerate, every publication committed to this repository.

A publication carries a snapshot of the engine that produced it, so any change under
the shared engine or a subject adapter makes every committed run stale. That went
unnoticed for two phases because the only check named one subject and one run. This
discovers the runs instead, so a second committed run is covered the day it lands.

Regeneration separates two things that look alike in a diff but are not alike at all:
the runtime snapshot and the evidence move whenever engine code moves, which is
routine, while the composed pages and figures are what a learner reads. A change to
those is a change to the product, so it has to be asked for explicitly rather than
carried along by a refresh.
"""
from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if __package__ in (None, ""):
    sys.path.insert(0, str(REPO))

from Shared.contracts import ContractError, load  # noqa: E402
from Shared.publication_host.audit import verify_publication  # noqa: E402
from Shared.publication_host.host import publish  # noqa: E402


def committed_publications(repo: Path = REPO) -> list[Path]:
    """Every committed publication directory, found by its manifest rather than by name."""
    return sorted(p.parent for p in repo.glob("*/content/*/publication/manifest.json"))


def adapter_for(publication: Path, repo: Path = REPO):
    """The adapter of whichever subject owns this run, resolved from its path."""
    subject = publication.relative_to(repo).parts[0]
    return importlib.import_module(f"{subject}.adapter").load()


def learner_visible(root: Path) -> dict[str, bytes]:
    """The bytes a learner actually reads: composed pages and the figures they embed.

    The runtime snapshot, manifest and evidence are deliberately excluded. They record
    how the publication was produced, not what it says.
    """
    pages = {p.name: p.read_bytes() for p in root.glob("*.html")}
    figures = {f"figures/{p.name}": p.read_bytes() for p in (root / "figures").glob("*")}
    return {**pages, **figures}


def verify(publication: Path, repo: Path = REPO) -> dict:
    basis = load(publication / "manifest.json").get("basis_digest")
    result = verify_publication(publication, basis, adapter_for(publication, repo))
    return {"publication": str(publication.relative_to(repo)), **result}


def regenerate(publication: Path, *, accept_output_change: bool = False,
               repo: Path = REPO) -> dict:
    run = publication.parent
    inputs = run / "inputs"
    with tempfile.TemporaryDirectory() as temp:
        fresh = Path(temp) / "publication"
        result = publish(inputs / "plan.json", inputs / "baseline.json", inputs, fresh,
                         adapter_for(publication, repo))
        before, after = learner_visible(publication), learner_visible(fresh)
        changed = sorted({name for name in before.keys() | after.keys()
                          if before.get(name) != after.get(name)})
        if changed and not accept_output_change:
            raise ContractError("PUBLISHED_OUTPUT_WOULD_CHANGE",
                                f'{publication.relative_to(repo)}: {", ".join(changed)}')
        shutil.rmtree(publication)
        shutil.copytree(fresh, publication)
    return {"publication": str(publication.relative_to(repo)),
            "basis_digest": result["basis_digest"], "learner_visible_changes": changed}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true",
                        help="regenerate each publication instead of only verifying it")
    parser.add_argument("--accept-output-change", action="store_true",
                        help="permit a regeneration that changes what a learner reads")
    args = parser.parse_args()

    found = committed_publications()
    if not found:
        print("no committed publications found")
        return 1
    reports, failed = [], False
    for publication in found:
        try:
            reports.append(regenerate(publication, accept_output_change=args.accept_output_change)
                           if args.write else verify(publication))
        except ContractError as error:
            failed = True
            reports.append({"publication": str(publication.relative_to(REPO)),
                            "status": "BLOCKED", "code": error.code, "detail": error.detail})
    print(json.dumps(reports, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
