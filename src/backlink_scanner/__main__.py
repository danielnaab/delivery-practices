# spec: specs/backlink-scanner.md
# spec-section: Behavior/Exit codes

"""CLI entry point for the backlink scanner."""

import json
import sys

from backlink_scanner.scanner import ScanResult, scan


def _serialize(result: ScanResult) -> dict:
    """Convert ScanResult to a JSON-serializable dict."""
    specs = {}
    for spec_path, entry in result.specs.items():
        specs[spec_path] = {
            "implementors": entry.implementors,
            "sections": entry.sections,
        }
    return {
        "specs": specs,
        "dangling": result.dangling,
        "orphans": result.orphans,
    }


def main() -> None:
    report_only = "--report-only" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--report-only"]
    root_dir = args[0] if args else "."

    result = scan(root_dir)
    print(json.dumps(_serialize(result), indent=2))

    if report_only:
        sys.exit(0)

    if result.dangling or result.orphans:
        sys.exit(1)


if __name__ == "__main__":
    main()
