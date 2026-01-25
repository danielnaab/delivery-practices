# spec: specs/pr-description-generator.md
# spec-section: Behavior/Exit codes

"""CLI entry point for the PR description generator."""

import sys

from pr_description_generator.generator import (
    ValidationError,
    generate,
    parse_input,
    validate_for_format,
)


def main() -> None:
    """Run the PR description generator CLI."""
    if len(sys.argv) < 2:
        print("Usage: pr-description <input.yaml>", file=sys.stderr)
        sys.exit(2)

    yaml_path = sys.argv[1]

    try:
        pr_input = parse_input(yaml_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    errors = validate_for_format(pr_input)
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)

    output = generate(pr_input)
    print(output, end="")


if __name__ == "__main__":
    main()
