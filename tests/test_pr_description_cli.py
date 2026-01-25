# spec: specs/pr-description-generator.md
# spec-section: Behavior/Exit codes

"""Integration tests for the PR description generator CLI."""

import subprocess
import sys
from pathlib import Path


def _run_generator(yaml_path: str) -> subprocess.CompletedProcess:
    """Run the PR description generator CLI on a YAML file."""
    return subprocess.run(
        [sys.executable, "-m", "pr_description_generator", yaml_path],
        capture_output=True,
        text=True,
    )


class TestCLIExitCodes:
    def test_exit_0_on_success(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test summary
verify: "uv run pytest"
specs:
  - specs/test.md
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0

    def test_exit_2_on_missing_file(self, tmp_path: Path) -> None:
        proc = _run_generator(str(tmp_path / "nonexistent.yaml"))

        assert proc.returncode == 2
        assert "not found" in proc.stderr.lower()

    def test_exit_2_on_invalid_yaml(self, tmp_path: Path) -> None:
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("{ invalid: [yaml")

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 2
        assert "yaml" in proc.stderr.lower()

    def test_exit_2_on_unknown_format(self, tmp_path: Path) -> None:
        yaml_content = """\
format: unknown
summary: Test
verify: "test"
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 2
        assert "unknown format" in proc.stderr.lower()

    def test_exit_2_on_missing_required_fields(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 2
        assert "missing required field" in proc.stderr.lower()

    def test_exit_2_with_no_arguments(self) -> None:
        proc = subprocess.run(
            [sys.executable, "-m", "pr_description_generator"],
            capture_output=True,
            text=True,
        )

        assert proc.returncode == 2
        assert "usage" in proc.stderr.lower()


class TestCLIOutput:
    def test_outputs_markdown_to_stdout(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Added new feature.
verify: "uv run pytest"
specs:
  - specs/test.md
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "Added new feature." in proc.stdout
        assert "Verify: `uv run pytest`" in proc.stdout

    def test_errors_go_to_stderr(self, tmp_path: Path) -> None:
        proc = _run_generator(str(tmp_path / "missing.yaml"))

        assert proc.returncode == 2
        assert proc.stdout == ""
        assert "Error:" in proc.stderr

    def test_simple_format_output(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Simple change.
verify: "make test"
specs:
  - specs/feature.md
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert "Simple change." in proc.stdout
        assert "Spec:" in proc.stdout or "See `specs/feature.md`" in proc.stdout
        assert "Verify: `make test`" in proc.stdout

    def test_medium_format_output(self, tmp_path: Path) -> None:
        yaml_content = """\
format: medium
summary: Medium complexity change.
verify: "uv run pytest"
specs:
  - specs/feature.md
sessions:
  - notes/session.md
changes: "spec → impl → tests"
focus: "Check the validation logic."
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "Medium complexity change." in proc.stdout
        assert "**Changes**:" in proc.stdout
        assert "**Focus**:" in proc.stdout

    def test_non_spec_format_output(self, tmp_path: Path) -> None:
        yaml_content = """\
format: non-spec
summary: Refactored code.
verify: "uv run pytest"
focus: "Pure refactor, all tests pass unchanged."
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "Refactored code." in proc.stdout
        assert "**Focus**:" in proc.stdout
        assert "Spec:" not in proc.stdout

    def test_large_format_with_all_options(self, tmp_path: Path) -> None:
        yaml_content = """\
format: large
summary: Large comprehensive change.
verify: "uv run pytest && uv run ruff check"
specs:
  - specs/a.md
  - specs/b.md
sessions:
  - notes/session.md
changes: "spec → implementation → tests → config"
focus: "Review the behavior map sections."
breaking: "Exit codes changed from 0 to 1"
decisions:
  - "Used regex for performance"
  - "Skipped edge case X"
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "Large comprehensive change." in proc.stdout
        assert "**Breaking**: Exit codes changed" in proc.stdout
        assert "Key decisions" in proc.stdout
        assert "- Used regex for performance" in proc.stdout

    def test_output_ends_with_newline(self, tmp_path: Path) -> None:
        yaml_content = """\
format: non-spec
summary: Test.
verify: "test"
focus: "Focus."
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.stdout.endswith("\n")


class TestLinkFormatting:
    def test_existing_files_become_links(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "specs/test.md").write_text("# Test")

        yaml_content = f"""\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
root_dir: "{tmp_path}"
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert "[test.md](specs/test.md)" in proc.stdout

    def test_new_files_get_see_in_pr(self, tmp_path: Path) -> None:
        yaml_content = f"""\
format: simple
summary: Test
verify: "test"
specs:
  - specs/new-spec.md
root_dir: "{tmp_path}"
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert "See `specs/new-spec.md` in this PR" in proc.stdout


class TestGitHubLinkFormatting:
    def test_github_blob_links_for_existing_files(self, tmp_path: Path) -> None:
        (tmp_path / "specs").mkdir()
        (tmp_path / "specs/test.md").write_text("# Test")

        yaml_content = f"""\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
root_dir: "{tmp_path}"
github:
  owner: anthropic
  repo: delivery-practices
  branch: main
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert (
            "https://github.com/anthropic/delivery-practices/blob/main/specs/test.md" in proc.stdout
        )

    def test_github_pr_diff_links_for_new_files(self, tmp_path: Path) -> None:
        yaml_content = f"""\
format: simple
summary: Test
verify: "test"
specs:
  - specs/new-spec.md
root_dir: "{tmp_path}"
github:
  owner: anthropic
  repo: delivery-practices
  branch: feature
  pr_number: 42
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "https://github.com/anthropic/delivery-practices/pull/42/files#diff-" in proc.stdout

    def test_github_without_pr_number_falls_back(self, tmp_path: Path) -> None:
        yaml_content = f"""\
format: simple
summary: Test
verify: "test"
specs:
  - specs/new-spec.md
root_dir: "{tmp_path}"
github:
  owner: anthropic
  repo: repo
  branch: main
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 0
        assert "See `specs/new-spec.md` in this PR" in proc.stdout

    def test_github_missing_required_fields(self, tmp_path: Path) -> None:
        yaml_content = """\
format: simple
summary: Test
verify: "test"
specs:
  - specs/test.md
github:
  owner: anthropic
"""
        yaml_file = tmp_path / "input.yaml"
        yaml_file.write_text(yaml_content)

        proc = _run_generator(str(yaml_file))

        assert proc.returncode == 2
        assert "github missing required fields" in proc.stderr
