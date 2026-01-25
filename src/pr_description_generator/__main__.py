# spec: specs/pr-description-generator.md
# spec-section: Behavior/Exit codes

"""CLI entry point for the PR description generator."""

import sys

from pr_description_generator.adapters.github import GitHubConfig, GitHubLinkAdapter
from pr_description_generator.adapters.plain import PlainLinkAdapter
from pr_description_generator.generator import (
    ValidationError,
    generate,
    parse_input,
    validate_for_format,
)
from pr_description_generator.protocols import LinkAdapter


def create_adapter(pr_input) -> LinkAdapter:
    """Create the appropriate link adapter based on PR input configuration.

    Args:
        pr_input: Parsed PR input with optional github configuration.

    Returns:
        GitHubLinkAdapter if github config present, otherwise PlainLinkAdapter.
    """
    if pr_input.github:
        config = GitHubConfig(
            owner=pr_input.github.owner,
            repo=pr_input.github.repo,
            branch=pr_input.github.branch,
            pr_number=pr_input.github.pr_number,
            root_dir=pr_input.root_dir,
        )
        return GitHubLinkAdapter(config)
    return PlainLinkAdapter(pr_input.root_dir)


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

    adapter = create_adapter(pr_input)
    output = generate(pr_input, adapter)
    print(output, end="")


if __name__ == "__main__":
    main()
