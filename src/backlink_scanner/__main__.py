# spec: specs/backlink-scanner.md

"""CLI entry point for the backlink scanner."""

import json
import sys
from dataclasses import asdict

from backlink_scanner.scanner import scan


def main() -> None:
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = scan(root_dir)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
