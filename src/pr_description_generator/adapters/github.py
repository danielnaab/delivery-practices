# spec: specs/pr-description-generator.md

"""GitHub link adapter — rich links with blob URLs and PR diff anchors."""

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitHubConfig:
    """Configuration for GitHub link generation.

    Attributes:
        owner: Repository owner (user or organization).
        repo: Repository name.
        branch: Branch name for blob links (e.g., "main", "feature-x").
        pr_number: Pull request number for diff links (optional).
        root_dir: Root directory for checking file existence.
    """

    owner: str
    repo: str
    branch: str
    pr_number: int | None = None
    root_dir: str = "."


class GitHubLinkAdapter:
    """Adapter for GitHub-specific links.

    Generates rich links including:
    - Blob URLs for existing files: github.com/owner/repo/blob/branch/path
    - PR diff anchors for new files: github.com/owner/repo/pull/N/files#diff-<sha256>
    """

    def __init__(self, config: GitHubConfig) -> None:
        """Initialize the GitHub adapter.

        Args:
            config: GitHub configuration with owner, repo, branch, etc.
        """
        self._config = config

    @property
    def base_url(self) -> str:
        """Get the base GitHub URL for this repository."""
        return f"https://github.com/{self._config.owner}/{self._config.repo}"

    def format_file_link(self, path: str, display_name: str, exists: bool) -> str:
        """Format a link to a file.

        Args:
            path: Relative path to the file.
            display_name: Text to display for the link.
            exists: Whether the file exists in the repository.

        Returns:
            GitHub blob link if file exists, PR diff link if PR available,
            otherwise "See in PR" reference.
        """
        if exists:
            blob_url = f"{self.base_url}/blob/{self._config.branch}/{path}"
            return f"[{display_name}]({blob_url})"

        # File doesn't exist yet — link to PR diff if available
        if self._config.pr_number is not None:
            diff_anchor = self._compute_diff_anchor(path)
            pr_url = f"{self.base_url}/pull/{self._config.pr_number}/files{diff_anchor}"
            return f"[{display_name}]({pr_url})"

        return f"See `{path}` in this PR"

    def format_diff_anchor(self, path: str) -> str:
        """Format a URL anchor to a file in PR diff view.

        Args:
            path: Relative path to the file.

        Returns:
            URL anchor string (e.g., #diff-<sha256>), empty if no PR configured.
        """
        if self._config.pr_number is None:
            return ""
        return self._compute_diff_anchor(path)

    def format_pr_files_url(self) -> str | None:
        """Format URL to PR files changed view.

        Returns:
            Full URL to PR files view, or None if PR number not available.
        """
        if self._config.pr_number is None:
            return None
        return f"{self.base_url}/pull/{self._config.pr_number}/files"

    def supports_pr_links(self) -> bool:
        """Check if this adapter supports PR-specific links.

        Returns:
            True if PR number is configured.
        """
        return self._config.pr_number is not None

    def check_file_exists(self, path: str) -> bool:
        """Check if a file exists at root_dir/path.

        Args:
            path: Relative path to the file.

        Returns:
            True if file exists, False otherwise.
        """
        full_path = Path(self._config.root_dir) / path
        return full_path.exists()

    def _compute_diff_anchor(self, path: str) -> str:
        """Compute the GitHub diff anchor for a file path.

        GitHub uses SHA256 hash of the file path for diff anchors.

        Args:
            path: Relative path to the file.

        Returns:
            URL anchor string (e.g., #diff-<sha256>).
        """
        path_hash = hashlib.sha256(path.encode()).hexdigest()
        return f"#diff-{path_hash}"
