# spec: specs/kb-linter.md
# spec-section: Behavior/Exit codes

"""CLI entry point for the KB linter."""

import json
import sys

from kb_linter.linter import LintResult, lint


def _serialize(result: LintResult) -> dict:
    """Convert LintResult to a JSON-serializable dict."""
    return {
        "violations": [
            {"file": v.file, "rule": v.rule, "message": v.message}
            for v in result.violations
        ],
        "summary": {
            "files_checked": result.files_checked,
            "files_passing": result.files_checked - len({
                v.file for v in result.violations
            }),
            "violations": len(result.violations),
        },
    }


def main() -> None:
    report_only = "--report-only" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--report-only"]
    root_dir = args[0] if args else "."

    try:
        result = lint(root_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(_serialize(result), indent=2))

    if report_only:
        sys.exit(0)

    if result.violations:
        sys.exit(1)


if __name__ == "__main__":
    main()
