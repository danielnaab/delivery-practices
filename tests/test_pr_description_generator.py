# spec: specs/pr-description-generator.md

"""Unit tests for the PR description generator."""

import json
from pathlib import Path

import pytest

from pr_description_generator.adapters.plain import PlainLinkAdapter
from pr_description_generator.generator import (
    ValidationError,
    format_link,
    generate,
    generate_large,
    generate_medium,
    generate_non_spec,
    generate_simple,
    load_behavior_map,
    parse_input,
    validate_for_format,
)
from pr_description_generator.models import Format, PRInput


class TestParseInput:
    def test_parses_valid_yaml(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test summary
verify: "uv run pytest"
specs:
  - specs/test.md
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.format == Format.SIMPLE
        assert result.summary == "Test summary"
        assert result.verify == "uv run pytest"
        assert result.specs == ["specs/test.md"]

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            parse_input(str(tmp_path / "nonexistent.yaml"))

    def test_raises_on_invalid_yaml(self, tmp_path: Path) -> None:
        (tmp_path / "bad.yaml").write_text("{ invalid: [yaml")

        with pytest.raises(ValidationError, match="Invalid YAML"):
            parse_input(str(tmp_path / "bad.yaml"))

    def test_raises_on_unknown_format(self, tmp_path: Path) -> None:
        yaml_content = """\
format: unknown
summary: Test
verify: "test"
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        with pytest.raises(ValidationError, match="Unknown format 'unknown'"):
            parse_input(str(tmp_path / "input.yaml"))

    def test_raises_on_yaml_not_a_mapping(self, tmp_path: Path) -> None:
        (tmp_path / "input.yaml").write_text("just a string")

        with pytest.raises(ValidationError, match="YAML must be a mapping"):
            parse_input(str(tmp_path / "input.yaml"))

    def test_raises_on_yaml_list(self, tmp_path: Path) -> None:
        (tmp_path / "input.yaml").write_text("- item1\n- item2")

        with pytest.raises(ValidationError, match="YAML must be a mapping"):
            parse_input(str(tmp_path / "input.yaml"))

    def test_parses_all_optional_fields(self, tmp_path: Path) -> None:
        yaml_content = """\
format: large
summary: Full summary
verify: "uv run pytest"
specs:
  - specs/a.md
  - specs/b.md
sessions:
  - notes/session.md
changes: "spec → impl → tests"
focus: "Check the edge cases"
breaking: "API changed"
decisions:
  - "Decision 1"
  - "Decision 2"
behavior_map_source: ".backlink.json"
root_dir: "/custom/root"
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.format == Format.LARGE
        assert result.specs == ["specs/a.md", "specs/b.md"]
        assert result.sessions == ["notes/session.md"]
        assert result.changes == "spec → impl → tests"
        assert result.focus == "Check the edge cases"
        assert result.breaking == "API changed"
        assert result.decisions == ["Decision 1", "Decision 2"]
        assert result.behavior_map_source == ".backlink.json"
        assert result.root_dir == "/custom/root"

    def test_defaults_root_dir_to_dot(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.root_dir == "."

    def test_handles_empty_lists(self, tmp_path: Path) -> None:
        yaml_content = """\
format: non-spec
summary: Test
verify: "test"
focus: "Check it"
specs:
sessions:
decisions:
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.specs == []
        assert result.sessions == []
        assert result.decisions == []

    def test_parses_github_config(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
github:
  owner: anthropic
  repo: delivery-practices
  branch: main
  pr_number: 42
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.github is not None
        assert result.github.owner == "anthropic"
        assert result.github.repo == "delivery-practices"
        assert result.github.branch == "main"
        assert result.github.pr_number == 42

    def test_github_pr_number_optional(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
github:
  owner: owner
  repo: repo
  branch: feature
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.github is not None
        assert result.github.pr_number is None

    def test_github_none_when_not_provided(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        result = parse_input(str(tmp_path / "input.yaml"))

        assert result.github is None

    def test_raises_on_github_missing_required_fields(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
github:
  owner: anthropic
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        with pytest.raises(ValidationError, match="github missing required fields"):
            parse_input(str(tmp_path / "input.yaml"))

    def test_raises_on_github_not_a_mapping(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
github: "not a mapping"
"""
        (tmp_path / "input.yaml").write_text(yaml_content)

        with pytest.raises(ValidationError, match="github must be a mapping"):
            parse_input(str(tmp_path / "input.yaml"))


class TestValidateForFormat:
    def test_simple_requires_summary_verify_specs(self) -> None:
        pr_input = PRInput(format=Format.SIMPLE, summary="", verify="", specs=[])

        errors = validate_for_format(pr_input)

        assert "Missing required field: summary" in errors
        assert "Missing required field: verify" in errors
        assert "Missing required field: specs (at least one)" in errors

    def test_simple_valid_with_required_fields(self) -> None:
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Summary",
            verify="test",
            specs=["specs/test.md"],
        )

        errors = validate_for_format(pr_input)

        assert errors == []

    def test_medium_requires_all_fields(self) -> None:
        pr_input = PRInput(format=Format.MEDIUM, summary="", verify="")

        errors = validate_for_format(pr_input)

        assert "Missing required field: summary" in errors
        assert "Missing required field: verify" in errors
        assert "Missing required field: specs (at least one)" in errors
        assert "Missing required field: sessions (at least one)" in errors
        assert "Missing required field: changes" in errors
        assert "Missing required field: focus" in errors

    def test_medium_valid_with_required_fields(self) -> None:
        pr_input = PRInput(
            format=Format.MEDIUM,
            summary="Summary",
            verify="test",
            specs=["specs/test.md"],
            sessions=["notes/session.md"],
            changes="changes",
            focus="focus",
        )

        errors = validate_for_format(pr_input)

        assert errors == []

    def test_large_requires_same_as_medium(self) -> None:
        pr_input = PRInput(format=Format.LARGE, summary="", verify="")

        errors = validate_for_format(pr_input)

        assert "Missing required field: specs (at least one)" in errors
        assert "Missing required field: sessions (at least one)" in errors
        assert "Missing required field: changes" in errors
        assert "Missing required field: focus" in errors

    def test_non_spec_requires_summary_verify_focus(self) -> None:
        pr_input = PRInput(format=Format.NON_SPEC, summary="", verify="", focus="")

        errors = validate_for_format(pr_input)

        assert "Missing required field: summary" in errors
        assert "Missing required field: verify" in errors
        assert "Missing required field: focus" in errors

    def test_non_spec_does_not_require_specs(self) -> None:
        pr_input = PRInput(format=Format.NON_SPEC, summary="Summary", verify="test", focus="Focus")

        errors = validate_for_format(pr_input)

        assert errors == []


class TestFormatLink:
    def test_existing_file_becomes_link(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "specs/test.md").write_text("# Test")
        adapter = PlainLinkAdapter(str(tmp_path))

        result = format_link("specs/test.md", adapter)

        assert result == "[test.md](specs/test.md)"

    def test_new_file_becomes_see_in_pr(self, tmp_path: Path) -> None:
        adapter = PlainLinkAdapter(str(tmp_path))

        result = format_link("specs/new.md", adapter)

        assert result == "See `specs/new.md` in this PR"


class TestLoadBehaviorMap:
    def test_loads_sections_from_json(self, tmp_path: Path) -> None:
        data = {
            "specs": {
                "specs/foo.md": {
                    "implementors": ["src/foo.py"],
                    "sections": {"Behavior/Login": ["src/auth.py"]},
                }
            }
        }
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        result = load_behavior_map(".backlink.json", str(tmp_path))

        assert len(result) == 1
        assert result[0].section == "Behavior/Login"
        assert result[0].files == ["src/auth.py"]

    def test_handles_multiple_files_per_section(self, tmp_path: Path) -> None:
        data = {
            "specs": {
                "specs/foo.md": {"sections": {"Behavior/Auth": ["src/auth.py", "src/login.py"]}}
            }
        }
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        result = load_behavior_map(".backlink.json", str(tmp_path))

        assert result[0].files == ["src/auth.py", "src/login.py"]

    def test_returns_empty_for_missing_file(self, tmp_path: Path) -> None:
        result = load_behavior_map("missing.json", str(tmp_path))

        assert result == []

    def test_returns_empty_for_invalid_json(self, tmp_path: Path) -> None:
        (tmp_path / "bad.json").write_text("{ invalid json")

        result = load_behavior_map("bad.json", str(tmp_path))

        assert result == []

    def test_handles_multiple_specs(self, tmp_path: Path) -> None:
        data = {
            "specs": {
                "specs/a.md": {"sections": {"Section/A": ["src/a.py"]}},
                "specs/b.md": {"sections": {"Section/B": ["src/b.py"]}},
            }
        }
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        result = load_behavior_map(".backlink.json", str(tmp_path))

        assert len(result) == 2
        sections = {e.section for e in result}
        assert sections == {"Section/A", "Section/B"}

    def test_filters_to_specified_specs(self, tmp_path: Path) -> None:
        data = {
            "specs": {
                "specs/a.md": {"sections": {"Section/A": ["src/a.py"]}},
                "specs/b.md": {"sections": {"Section/B": ["src/b.py"]}},
                "specs/c.md": {"sections": {"Section/C": ["src/c.py"]}},
            }
        }
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        result = load_behavior_map(
            ".backlink.json", str(tmp_path), filter_specs=["specs/a.md", "specs/c.md"]
        )

        assert len(result) == 2
        sections = {e.section for e in result}
        assert sections == {"Section/A", "Section/C"}

    def test_filter_specs_none_returns_all(self, tmp_path: Path) -> None:
        data = {
            "specs": {
                "specs/a.md": {"sections": {"Section/A": ["src/a.py"]}},
                "specs/b.md": {"sections": {"Section/B": ["src/b.py"]}},
            }
        }
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        result = load_behavior_map(".backlink.json", str(tmp_path), filter_specs=None)

        assert len(result) == 2


class TestGenerateSimple:
    def test_generates_simple_format(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "specs/test.md").write_text("# Test")

        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Added a new feature.",
            verify="uv run pytest",
            specs=["specs/test.md"],
            root_dir=str(tmp_path),
        )

        result = generate_simple(pr_input)

        assert "Added a new feature." in result
        assert "Spec: [test.md](specs/test.md)" in result
        assert "Verify: `uv run pytest`" in result

    def test_uses_plural_for_multiple_specs(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "specs/a.md").write_text("# A")
        (tmp_path / "specs/b.md").write_text("# B")

        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Summary",
            verify="test",
            specs=["specs/a.md", "specs/b.md"],
            root_dir=str(tmp_path),
        )

        result = generate_simple(pr_input)

        assert "Specs:" in result
        assert "[a.md](specs/a.md)" in result
        assert "[b.md](specs/b.md)" in result


class TestGenerateMedium:
    def test_generates_medium_format(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "notes").mkdir()
        (tmp_path / "specs/test.md").write_text("# Test")
        (tmp_path / "notes/session.md").write_text("# Session")

        pr_input = PRInput(
            format=Format.MEDIUM,
            summary="Added feature with context.",
            verify="uv run pytest",
            specs=["specs/test.md"],
            sessions=["notes/session.md"],
            changes="spec → impl → tests",
            focus="Check edge cases.",
            root_dir=str(tmp_path),
        )

        result = generate_medium(pr_input)

        assert "Added feature with context." in result
        assert "Spec: [test.md](specs/test.md)" in result
        assert "Session: [session.md](notes/session.md)" in result
        assert "Verify: `uv run pytest`" in result
        assert "**Changes**: spec → impl → tests" in result
        assert "**Focus**: Check edge cases." in result


class TestGenerateLarge:
    def test_generates_large_format_minimal(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.LARGE,
            summary="Large change.",
            verify="uv run pytest",
            specs=["specs/a.md"],
            sessions=["notes/session.md"],
            changes="spec → impl",
            focus="Focus here",
            root_dir=str(tmp_path),
        )

        result = generate_large(pr_input)

        assert "Large change." in result
        assert "**Changes**:" in result
        assert "**Focus**:" in result
        assert "**Breaking**" not in result
        assert "<details>" not in result

    def test_includes_breaking_when_provided(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.LARGE,
            summary="Breaking change.",
            verify="test",
            specs=["specs/a.md"],
            sessions=["notes/session.md"],
            changes="changes",
            focus="focus",
            breaking="API v1 removed",
            root_dir=str(tmp_path),
        )

        result = generate_large(pr_input)

        assert "**Breaking**: API v1 removed" in result

    def test_includes_behavior_map_when_source_exists(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "src/auth.py").write_text("# auth")
        data = {"specs": {"specs/a.md": {"sections": {"Behavior/Auth": ["src/auth.py"]}}}}
        (tmp_path / ".backlink.json").write_text(json.dumps(data))

        pr_input = PRInput(
            format=Format.LARGE,
            summary="Summary",
            verify="test",
            specs=["specs/a.md"],
            sessions=["notes/session.md"],
            changes="changes",
            focus="focus",
            behavior_map_source=".backlink.json",
            root_dir=str(tmp_path),
        )

        result = generate_large(pr_input)

        assert "<details><summary>Behavior map" in result
        assert "§Behavior/Auth → [auth.py](src/auth.py)" in result

    def test_includes_decisions_when_provided(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.LARGE,
            summary="Summary",
            verify="test",
            specs=["specs/a.md"],
            sessions=["notes/session.md"],
            changes="changes",
            focus="focus",
            decisions=["Decision one", "Decision two"],
            root_dir=str(tmp_path),
        )

        result = generate_large(pr_input)

        assert "<details><summary>Key decisions</summary>" in result
        assert "- Decision one" in result
        assert "- Decision two" in result

    def test_omits_behavior_map_when_source_missing(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.LARGE,
            summary="Summary",
            verify="test",
            specs=["specs/a.md"],
            sessions=["notes/session.md"],
            changes="changes",
            focus="focus",
            behavior_map_source="missing.json",
            root_dir=str(tmp_path),
        )

        result = generate_large(pr_input)

        assert "Behavior map" not in result


class TestGenerateNonSpec:
    def test_generates_non_spec_format(self) -> None:
        pr_input = PRInput(
            format=Format.NON_SPEC,
            summary="Refactored the code.",
            verify="uv run pytest",
            focus="Pure refactor, tests unchanged.",
        )

        result = generate_non_spec(pr_input)

        assert "Refactored the code." in result
        assert "Verify: `uv run pytest`" in result
        assert "**Focus**: Pure refactor, tests unchanged." in result
        assert "Spec:" not in result
        assert "Session:" not in result


class TestGenerate:
    def test_dispatches_to_simple(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Summary",
            verify="test",
            specs=["specs/test.md"],
            root_dir=str(tmp_path),
        )

        result = generate(pr_input)

        assert "Spec:" in result or "Specs:" in result

    def test_dispatches_to_non_spec(self) -> None:
        pr_input = PRInput(
            format=Format.NON_SPEC,
            summary="Summary",
            verify="test",
            focus="Focus",
        )

        result = generate(pr_input)

        assert "**Focus**:" in result
        assert "Spec" not in result


class TestOutputFormat:
    def test_ends_with_single_newline(self) -> None:
        pr_input = PRInput(
            format=Format.NON_SPEC,
            summary="Summary",
            verify="test",
            focus="Focus",
        )

        result = generate(pr_input)

        assert result.endswith("\n")
        assert not result.endswith("\n\n")

    def test_multiline_summary_preserved(self, tmp_path: Path) -> None:
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Line one.\nLine two.",
            verify="test",
            specs=["specs/test.md"],
            root_dir=str(tmp_path),
        )

        result = generate_simple(pr_input)

        assert "Line one.\nLine two." in result
