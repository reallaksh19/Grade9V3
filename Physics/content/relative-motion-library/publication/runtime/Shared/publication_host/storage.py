"""Create immutable publication directories and portable command dependencies."""

import json
import shutil
import tempfile
from pathlib import Path

from Shared.contracts import digest, file_digest, require


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding="utf-8")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


# The shared half of a publication's runtime: this engine and the contract helpers it
# imports. Deliberately not all of Shared/ -- the library compiler, the gate validator
# and the repository tooling live there too, and publish and verify import none of
# them. Sweeping the whole tree made every tooling edit invalidate every committed
# publication, so the staleness signal cried wolf and was ignored for two phases. A
# test walks the engine's imports and fails if this set ever stops covering them.
ENGINE_SOURCES = ("__init__.py", "contracts.py", "publication_host")


def runtime_files(adapter):
    """Every file the publish and verify commands depend on, for portable rebuild.

    The shared half is this engine and its contracts. The subject half is whatever
    the adapter declares -- its contract, its calculation owner, its scenes -- so no
    subject path is named here.
    """
    root = repo_root()
    files = []
    for entry in ENGINE_SOURCES:
        source = root / "Shared" / entry
        files += sorted(source.rglob('*.py')) if source.is_dir() else [source]
    files += list(adapter.runtime_files())
    return {str(p.relative_to(root)): p for p in sorted(set(files))
            if p.is_file() and '__pycache__' not in p.parts}


def runtime_manifest(adapter):
    return [{"path": 'runtime/' + name, "sha256": file_digest(path)}
            for name, path in runtime_files(adapter).items()]


def build_directory(out, action):
    require(not out.exists(), "PUBLICATION_ALREADY_EXISTS", str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.v3b-build-', dir=out.parent))
    try:
        result = action(staging)
        require(not out.exists(), "PUBLICATION_ALREADY_EXISTS", str(out))
        staging.rename(out)
        return result
    finally:
        if staging.exists():
            shutil.rmtree(staging)
