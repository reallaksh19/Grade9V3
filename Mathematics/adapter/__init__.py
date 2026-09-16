"""This subject's adapter: contract, calculation owner, scenes and runtime files.

Naming the subject is this package's job. The shared engine receives the result of
`load()` and never imports anything from here.
"""
from __future__ import annotations

from pathlib import Path

from Shared.publication_host.adapter import Adapter, load_contract

from .scenes import SCENES
from .validator import recompute

HERE = Path(__file__).resolve().parent
SUBJECT_ROOT = HERE.parent
CONTRACT = HERE / "CoreContracts.json"


def runtime_files() -> list[Path]:
    """Subject files the publish/verify commands depend on, for portable rebuild."""
    files = [CONTRACT, SUBJECT_ROOT / "run.py"]
    files += sorted(HERE.glob("*.py"))
    return [p for p in files if p.is_file()]


def load() -> Adapter:
    return Adapter(contract=load_contract(CONTRACT), recompute=recompute,
                   scenes=SCENES, runtime_files=runtime_files)
