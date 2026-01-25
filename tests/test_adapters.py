# spec: specs/pr-description-generator.md

"""Unit tests for link adapters."""

from pathlib import Path

import pytest

from pr_description_generator.adapters.github import GitHubConfig, GitHubLinkAdapter
from pr_description_generator.adapters.plain import PlainLinkAdapter


class TestPlainLinkAdapter:
    """Tests for PlainLinkAdapter."""

    def test_format_file_link_existing(self) -> None:
        adapter = PlainLinkAdapter()

        result = adapter.format_file_link("src/main.py", "main.py", exists=True)

        assert result == "[main.py](src/main.py)"

    def test_format_file_link_not_existing(self) -> None:
        adapter = PlainLinkAdapter()

        result = adapter.format_file_link("src/new.py", "new.py", exists=False)

        assert result == "See `src/new.py` in this PR"

    def test_format_diff_anchor_returns_empty(self) -> None:
        adapter = PlainLinkAdapter()

        result = adapter.format_diff_anchor("src/main.py")

        assert result == ""

    def test_format_pr_files_url_returns_none(self) -> None:
        adapter = PlainLinkAdapter()

        result = adapter.format_pr_files_url()

        assert result is None

    def test_supports_pr_links_returns_false(self) -> None:
        adapter = PlainLinkAdapter()

        assert adapter.supports_pr_links() is False

    def test_check_file_exists_true(self, tmp_path: Path) -> None:
        (tmp_path / "file.py").write_text("content")
        adapter = PlainLinkAdapter(str(tmp_path))

        assert adapter.check_file_exists("file.py") is True

    def test_check_file_exists_false(self, tmp_path: Path) -> None:
        adapter = PlainLinkAdapter(str(tmp_path))

        assert adapter.check_file_exists("missing.py") is False


class TestGitHubLinkAdapter:
    """Tests for GitHubLinkAdapter."""

    def test_format_file_link_existing(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main")
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_file_link("src/main.py", "main.py", exists=True)

        assert result == "[main.py](https://github.com/owner/repo/blob/main/src/main.py)"

    def test_format_file_link_new_file_without_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main")
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_file_link("src/new.py", "new.py", exists=False)

        assert result == "See `src/new.py` in this PR"

    def test_format_file_link_new_file_with_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main", pr_number=123)
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_file_link("src/new.py", "new.py", exists=False)

        assert "[new.py](https://github.com/owner/repo/pull/123/files#diff-" in result

    def test_format_diff_anchor_without_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main")
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_diff_anchor("src/main.py")

        assert result == ""

    def test_format_diff_anchor_with_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main", pr_number=123)
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_diff_anchor("src/main.py")

        assert result.startswith("#diff-")
        # SHA256 hash should be 64 characters
        hash_part = result[6:]  # Remove "#diff-"
        assert len(hash_part) == 64

    def test_format_pr_files_url_without_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main")
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_pr_files_url()

        assert result is None

    def test_format_pr_files_url_with_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main", pr_number=42)
        adapter = GitHubLinkAdapter(config)

        result = adapter.format_pr_files_url()

        assert result == "https://github.com/owner/repo/pull/42/files"

    def test_supports_pr_links_without_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main")
        adapter = GitHubLinkAdapter(config)

        assert adapter.supports_pr_links() is False

    def test_supports_pr_links_with_pr(self) -> None:
        config = GitHubConfig(owner="owner", repo="repo", branch="main", pr_number=123)
        adapter = GitHubLinkAdapter(config)

        assert adapter.supports_pr_links() is True

    def test_base_url(self) -> None:
        config = GitHubConfig(owner="anthropic", repo="claude-code", branch="develop")
        adapter = GitHubLinkAdapter(config)

        assert adapter.base_url == "https://github.com/anthropic/claude-code"

    def test_check_file_exists(self, tmp_path: Path) -> None:
        (tmp_path / "exists.py").write_text("content")
        config = GitHubConfig(owner="o", repo="r", branch="main", root_dir=str(tmp_path))
        adapter = GitHubLinkAdapter(config)

        assert adapter.check_file_exists("exists.py") is True
        assert adapter.check_file_exists("missing.py") is False

    def test_diff_anchor_is_deterministic(self) -> None:
        config = GitHubConfig(owner="o", repo="r", branch="main", pr_number=1)
        adapter = GitHubLinkAdapter(config)

        # Same path should produce same anchor
        anchor1 = adapter.format_diff_anchor("src/file.py")
        anchor2 = adapter.format_diff_anchor("src/file.py")
        assert anchor1 == anchor2

        # Different paths should produce different anchors
        anchor3 = adapter.format_diff_anchor("src/other.py")
        assert anchor1 != anchor3


class TestGitHubConfig:
    """Tests for GitHubConfig frozen dataclass."""

    def test_config_is_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        config = GitHubConfig(owner="owner", repo="repo", branch="main")

        with pytest.raises(FrozenInstanceError):
            config.owner = "new_owner"  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = GitHubConfig(owner="o", repo="r", branch="b")

        assert config.pr_number is None
        assert config.root_dir == "."
