# spec: specs/pr-description-generator.md

"""Core generation logic for PR descriptions."""

import json
from pathlib import Path

import yaml

from pr_description_generator.adapters.plain import PlainLinkAdapter
from pr_description_generator.models import BehaviorMapEntry, Format, GitHubInput, PRInput
from pr_description_generator.protocols import LinkAdapter


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def parse_input(yaml_path: str) -> PRInput:
    """Parse YAML input file into PRInput dataclass.

    Args:
        yaml_path: Path to the YAML input file.

    Returns:
        PRInput with parsed values.

    Raises:
        FileNotFoundError: If the YAML file doesn't exist.
        ValidationError: If YAML is invalid or format is unknown.
    """
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {yaml_path}")

    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML: {e}") from e

    if not isinstance(data, dict):
        raise ValidationError("YAML must be a mapping")

    format_str = data.get("format", "")
    try:
        fmt = Format(format_str)
    except ValueError:
        valid = ", ".join(f.value for f in Format)
        raise ValidationError(f"Unknown format '{format_str}', valid formats: {valid}") from None

    # Parse optional GitHub configuration
    github_input = None
    github_data = data.get("github")
    if github_data:
        if not isinstance(github_data, dict):
            raise ValidationError("github must be a mapping")
        missing = []
        for field in ("owner", "repo", "branch"):
            if not github_data.get(field):
                missing.append(field)
        if missing:
            raise ValidationError(f"github missing required fields: {', '.join(missing)}")
        github_input = GitHubInput(
            owner=github_data["owner"],
            repo=github_data["repo"],
            branch=github_data["branch"],
            pr_number=github_data.get("pr_number"),
        )

    return PRInput(
        format=fmt,
        summary=data.get("summary", ""),
        verify=data.get("verify", ""),
        specs=data.get("specs", []) or [],
        sessions=data.get("sessions", []) or [],
        changes=data.get("changes", ""),
        focus=data.get("focus", ""),
        breaking=data.get("breaking", ""),
        decisions=data.get("decisions", []) or [],
        behavior_map_source=data.get("behavior_map_source", ""),
        root_dir=data.get("root_dir", "."),
        github=github_input,
    )


def validate_for_format(pr_input: PRInput) -> list[str]:
    """Validate that required fields are present for the specified format.

    Args:
        pr_input: The parsed PR input.

    Returns:
        List of error messages (empty if valid).
    """
    errors = []

    # All formats require summary and verify
    if not pr_input.summary:
        errors.append("Missing required field: summary")
    if not pr_input.verify:
        errors.append("Missing required field: verify")

    if pr_input.format == Format.SIMPLE:
        if not pr_input.specs:
            errors.append("Missing required field: specs (at least one)")

    elif pr_input.format in (Format.MEDIUM, Format.LARGE):
        if not pr_input.specs:
            errors.append("Missing required field: specs (at least one)")
        if not pr_input.sessions:
            errors.append("Missing required field: sessions (at least one)")
        if not pr_input.changes:
            errors.append("Missing required field: changes")
        if not pr_input.focus:
            errors.append("Missing required field: focus")

    elif pr_input.format == Format.NON_SPEC and not pr_input.focus:
        errors.append("Missing required field: focus")

    return errors


def format_link(path: str, adapter: LinkAdapter) -> str:
    """Format a file path as a markdown link or "See in PR" reference.

    Args:
        path: Relative path to the file.
        adapter: Link adapter for platform-specific formatting.

    Returns:
        Formatted link string.
    """
    filename = Path(path).name
    exists = adapter.check_file_exists(path)
    return adapter.format_file_link(path, filename, exists)


def format_links(paths: list[str], adapter: LinkAdapter) -> str:
    """Format multiple file paths as comma-separated links.

    Args:
        paths: List of file paths.
        adapter: Link adapter for platform-specific formatting.

    Returns:
        Comma-separated formatted links.
    """
    formatted = [format_link(p, adapter) for p in paths]
    return ", ".join(formatted)


def load_behavior_map(
    source_path: str, root_dir: str, filter_specs: list[str] | None = None
) -> list[BehaviorMapEntry]:
    """Load behavior map from backlink scanner JSON output.

    Args:
        source_path: Path to the backlink scanner JSON file.
        root_dir: Root directory for resolving paths.
        filter_specs: If provided, only include sections from these spec paths.

    Returns:
        List of BehaviorMapEntry objects, empty if file doesn't exist.
    """
    full_path = Path(root_dir) / source_path
    if not full_path.exists():
        return []

    try:
        content = full_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except (json.JSONDecodeError, OSError):
        return []

    entries = []
    specs = data.get("specs", {})
    for spec_path, spec_data in specs.items():
        # Filter to only the specs in this PR if filter_specs provided
        if filter_specs is not None and spec_path not in filter_specs:
            continue
        sections = spec_data.get("sections", {})
        for section_name, files in sections.items():
            if files:
                entries.append(BehaviorMapEntry(section=section_name, files=files))

    return entries


def generate_simple(pr_input: PRInput, adapter: LinkAdapter | None = None) -> str:
    """Generate simple format PR description.

    Args:
        pr_input: The validated PR input.
        adapter: Optional link adapter. Defaults to PlainLinkAdapter.

    Returns:
        Markdown string.
    """
    if adapter is None:
        adapter = PlainLinkAdapter(pr_input.root_dir)

    lines = []

    # Summary
    lines.append(pr_input.summary.rstrip())
    lines.append("")

    # Spec: ... | Verify: ...
    spec_label = "Spec:" if len(pr_input.specs) == 1 else "Specs:"
    spec_links = format_links(pr_input.specs, adapter)
    lines.append(f"{spec_label} {spec_links} | Verify: `{pr_input.verify}`")

    return "\n".join(lines) + "\n"


def generate_medium(pr_input: PRInput, adapter: LinkAdapter | None = None) -> str:
    """Generate medium format PR description.

    Args:
        pr_input: The validated PR input.
        adapter: Optional link adapter. Defaults to PlainLinkAdapter.

    Returns:
        Markdown string.
    """
    if adapter is None:
        adapter = PlainLinkAdapter(pr_input.root_dir)

    lines = []

    # Summary
    lines.append(pr_input.summary.rstrip())
    lines.append("")

    # Spec: ... | Session: ...
    spec_label = "Spec:" if len(pr_input.specs) == 1 else "Specs:"
    spec_links = format_links(pr_input.specs, adapter)
    session_label = "Session:" if len(pr_input.sessions) == 1 else "Sessions:"
    session_links = format_links(pr_input.sessions, adapter)
    lines.append(f"{spec_label} {spec_links} | {session_label} {session_links}")

    # Verify
    lines.append(f"Verify: `{pr_input.verify}`")
    lines.append("")

    # Changes and Focus
    lines.append(f"**Changes**: {pr_input.changes}")
    lines.append(f"**Focus**: {pr_input.focus}")

    return "\n".join(lines) + "\n"


def generate_large(pr_input: PRInput, adapter: LinkAdapter | None = None) -> str:
    """Generate large format PR description.

    Args:
        pr_input: The validated PR input.
        adapter: Optional link adapter. Defaults to PlainLinkAdapter.

    Returns:
        Markdown string.
    """
    if adapter is None:
        adapter = PlainLinkAdapter(pr_input.root_dir)

    lines = []

    # Summary
    lines.append(pr_input.summary.rstrip())
    lines.append("")

    # Breaking (optional)
    if pr_input.breaking:
        lines.append(f"**Breaking**: {pr_input.breaking}")
        lines.append("")

    # Specs: ... | Sessions: ...
    spec_label = "Spec:" if len(pr_input.specs) == 1 else "Specs:"
    spec_links = format_links(pr_input.specs, adapter)
    session_label = "Session:" if len(pr_input.sessions) == 1 else "Sessions:"
    session_links = format_links(pr_input.sessions, adapter)
    lines.append(f"{spec_label} {spec_links} | {session_label} {session_links}")

    # Verify
    lines.append(f"Verify: `{pr_input.verify}`")
    lines.append("")

    # Changes and Focus
    lines.append(f"**Changes**: {pr_input.changes}")
    lines.append(f"**Focus**: {pr_input.focus}")

    # Behavior map (optional)
    if pr_input.behavior_map_source:
        entries = load_behavior_map(pr_input.behavior_map_source, pr_input.root_dir, pr_input.specs)
        if entries:
            lines.append("")
            lines.append(
                "<details><summary>Behavior map (which spec sections → which code)</summary>"
            )
            lines.append("")
            for entry in entries:
                file_links = format_links(entry.files, adapter)
                lines.append(f"§{entry.section} → {file_links}")
            lines.append("")
            lines.append("</details>")

    # Decisions (optional)
    if pr_input.decisions:
        lines.append("")
        lines.append("<details><summary>Key decisions</summary>")
        lines.append("")
        for decision in pr_input.decisions:
            lines.append(f"- {decision}")
        lines.append("")
        lines.append("</details>")

    return "\n".join(lines) + "\n"


def generate_non_spec(pr_input: PRInput, adapter: LinkAdapter | None = None) -> str:
    """Generate non-spec format PR description.

    Args:
        pr_input: The validated PR input.
        adapter: Optional link adapter. Defaults to PlainLinkAdapter.

    Returns:
        Markdown string.
    """
    # Non-spec format doesn't use file links, but accept adapter for consistency
    lines = []

    # Summary
    lines.append(pr_input.summary.rstrip())
    lines.append("")

    # Verify
    lines.append(f"Verify: `{pr_input.verify}`")
    lines.append("")

    # Focus
    lines.append(f"**Focus**: {pr_input.focus}")

    return "\n".join(lines) + "\n"


def generate(pr_input: PRInput, adapter: LinkAdapter | None = None) -> str:
    """Generate PR description for the specified format.

    Args:
        pr_input: The validated PR input.
        adapter: Optional link adapter. Defaults to PlainLinkAdapter.

    Returns:
        Markdown string.
    """
    generators = {
        Format.SIMPLE: generate_simple,
        Format.MEDIUM: generate_medium,
        Format.LARGE: generate_large,
        Format.NON_SPEC: generate_non_spec,
    }
    return generators[pr_input.format](pr_input, adapter)
