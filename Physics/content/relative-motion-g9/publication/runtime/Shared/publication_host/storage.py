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


def runtime_files(adapter):
    """Every file the publish and verify commands depend on, for portable rebuild.

    The shared half is this engine and its contracts. The subject half is whatever
    the adapter declares -- its contract, its calculation owner, its scenes -- so no
    subject path is named here.
    """
    root = repo_root()
    files = list((root / "Shared").rglob('*.py'))
    files += list((root / "Shared").rglob('*.json')) + list((root / "Shared").rglob('*.md'))
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
