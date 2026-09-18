"""Publication and verification commands, driven by an injected subject adapter."""

import argparse
import json
from pathlib import Path
from xml.etree.ElementTree import ParseError

from Shared.contracts import ContractError
from .audit import verify_publication
from .host import publish


def main(argv=None, *, adapter):
    parser = argparse.ArgumentParser(
        description=f"{adapter.subject} publication and actual-artifact verification")
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('publish')
    for name in ('plan', 'baseline', 'source-root', 'out'):
        command.add_argument('--' + name, type=Path, required=True)
    command = commands.add_parser('verify-publication')
    command.add_argument('--publication', type=Path, required=True)
    command.add_argument('--expected-basis', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'publish':
            result = publish(args.plan, args.baseline, args.source_root, args.out, adapter)
        else:
            result = verify_publication(args.publication, args.expected_basis, adapter)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ContractError, ValueError, TypeError, KeyError, IndexError, OSError, ParseError) as exc:
        print(json.dumps({"status": "BLOCKED", "code": getattr(exc, 'code', 'INVALID_INPUT'), "detail": str(exc)}))
        return 2
