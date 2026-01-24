# spec: specs/link-validator.md
# spec-section: Behavior/Exit codes

"""CLI entry point for the link validator."""

import json
import sys

from link_validator.validator import ValidateResult, validate


def _serialize(result: ValidateResult) -> dict:
    """Convert ValidateResult to a JSON-serializable dict."""
    return {
        "violations": [
            {
                "file": v.file,
                "target": v.target,
                "resolved": v.resolved,
                "rule": v.rule,
                "message": v.message,
            }
            for v in result.violations
        ],
        "summary": {
            "files_checked": result.files_checked,
            "links_checked": result.links_checked,
            "broken": len(result.violations),
        },
    }


def main() -> None:
    report_only = "--report-only" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--report-only"]
    root_dir = args[0] if args else "."

    result = validate(root_dir)
    print(json.dumps(_serialize(result), indent=2))

    if report_only:
        sys.exit(0)

    if result.violations:
        sys.exit(1)


if __name__ == "__main__":
    main()
