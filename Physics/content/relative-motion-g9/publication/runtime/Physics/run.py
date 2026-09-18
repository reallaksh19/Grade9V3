#!/usr/bin/env python3
"""Subject entrypoint: construct this subject's adapter and hand it to the engine.

    python3 Physics/run.py publish --plan P --baseline B --source-root S --out O
    python3 Physics/run.py verify-publication --publication O --expected-basis DIGEST
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Physics.adapter import load  # noqa: E402
from Shared.publication_host.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(adapter=load()))
