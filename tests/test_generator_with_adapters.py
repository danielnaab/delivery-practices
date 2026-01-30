# spec: specs/pr-description-generator.md

"""Tests for PR description generator using adapters."""

from pr_description_generator.adapters.github import GitHubConfig, GitHubLinkAdapter
from pr_description_generator.generator import generate, generate_simple
from pr_description_generator.models import Format, PRInput
from tests.fakes.fake_link_adapter import FakeLinkAdapter


class TestGeneratorWithFakeAdapter:
    """Tests using FakeLinkAdapter to verify generator behavior."""

    def test_generate_simple_uses_adapter_for_links(self) -> None:
        adapter = FakeLinkAdapter(existing_files={"specs/test.md"})
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Test summary",
            verify="uv run pytest",
            specs=["specs/test.md"],
        )

        result = generate_simple(pr_input, adapter)

        assert "[test.md](specs/test.md)" in result
        assert len(adapter.file_link_calls) == 1
        assert adapter.file_link_calls[0] == ("specs/test.md", "test.md", True)

    def test_generate_simple_new_file_uses_see_in_pr(self) -> None:
        adapter = FakeLinkAdapter(existing_files=set())
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Test summary",
            verify="test",
            specs=["specs/new.md"],
        )

        result = generate_simple(pr_input, adapter)

        assert "See `specs/new.md` in this PR" in result

    def test_generate_dispatches_adapter(self) -> None:
        adapter = FakeLinkAdapter(existing_files={"specs/test.md"})
        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Summary",
            verify="test",
            specs=["specs/test.md"],
        )

        result = generate(pr_input, adapter)

        assert "[test.md](specs/test.md)" in result
        assert len(adapter.file_link_calls) == 1


class TestGeneratorWithGitHubAdapter:
    """Tests using GitHubLinkAdapter to verify GitHub URL generation."""

    def test_generates_github_blob_links(self) -> None:
        config = GitHubConfig(
            owner="anthropic",
            repo="delivery-practices",
            branch="main",
        )
        adapter = GitHubLinkAdapter(config)
        # Override check_file_exists for testing
        adapter.check_file_exists = lambda path: True  # type: ignore[method-assign]

        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Added new feature",
            verify="uv run pytest",
            specs=["specs/test.md"],
        )

        result = generate_simple(pr_input, adapter)

        assert "https://github.com/anthropic/delivery-practices/blob/main/specs/test.md" in result

    def test_generates_pr_diff_links_for_new_files(self) -> None:
        config = GitHubConfig(
            owner="anthropic",
            repo="delivery-practices",
            branch="feature",
            pr_number=42,
        )
        adapter = GitHubLinkAdapter(config)
        # Override check_file_exists to simulate new file
        adapter.check_file_exists = lambda path: False  # type: ignore[method-assign]

        pr_input = PRInput(
            format=Format.SIMPLE,
            summary="Added new spec",
            verify="test",
            specs=["specs/new-feature.md"],
        )

        result = generate_simple(pr_input, adapter)

        assert "https://github.com/anthropic/delivery-practices/pull/42/files#diff-" in result


class TestFakeLinkAdapterTracking:
    """Tests for FakeLinkAdapter call tracking."""

    def test_tracks_file_link_calls(self) -> None:
        adapter = FakeLinkAdapter()

        adapter.format_file_link("path1", "name1", True)
        adapter.format_file_link("path2", "name2", False)

        assert len(adapter.file_link_calls) == 2
        assert ("path1", "name1", True) in adapter.file_link_calls
        assert ("path2", "name2", False) in adapter.file_link_calls

    def test_tracks_diff_anchor_calls(self) -> None:
        adapter = FakeLinkAdapter(pr_links_supported=True)

        adapter.format_diff_anchor("path/to/file.py")

        assert adapter.diff_anchor_calls == ["path/to/file.py"]

    def test_reset_clears_tracking(self) -> None:
        adapter = FakeLinkAdapter()
        adapter.format_file_link("path", "name", True)
        adapter.format_diff_anchor("path")

        adapter.reset()

        assert adapter.file_link_calls == []
        assert adapter.diff_anchor_calls == []

    def test_check_file_exists_uses_existing_files_set(self) -> None:
        adapter = FakeLinkAdapter(existing_files={"a.py", "b.py"})

        assert adapter.check_file_exists("a.py") is True
        assert adapter.check_file_exists("b.py") is True
        assert adapter.check_file_exists("c.py") is False
