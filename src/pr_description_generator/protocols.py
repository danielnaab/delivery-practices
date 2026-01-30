# spec: specs/pr-description-generator.md

"""Protocols for PR description generator adapters."""

from typing import Protocol


class LinkAdapter(Protocol):
    """Protocol for platform-specific link formatting.

    Implementations must provide methods for formatting links to files
    in a way appropriate for the target platform (GitHub, GitLab, plain, etc.).

    Any class implementing these methods satisfies this protocol.
    No explicit inheritance required (structural subtyping).
    """

    def format_file_link(self, path: str, display_name: str, exists: bool) -> str:
        """Format a link to a file.

        Args:
            path: Relative path to the file.
            display_name: Text to display for the link.
            exists: Whether the file exists in the repository.

        Returns:
            Formatted link string appropriate for the platform.
        """
        ...  # pragma: no cover

    def format_diff_anchor(self, path: str) -> str:
        """Format a URL anchor to a file in PR diff view.

        Args:
            path: Relative path to the file.

        Returns:
            URL anchor string (e.g., #diff-<hash> for GitHub).
            Returns empty string if PR diff links not supported.
        """
        ...  # pragma: no cover

    def format_pr_files_url(self) -> str | None:
        """Format URL to PR files changed view.

        Returns:
            Full URL to PR files view, or None if PR number not available.
        """
        ...  # pragma: no cover

    def supports_pr_links(self) -> bool:
        """Check if this adapter supports PR-specific links.

        Returns:
            True if PR number is configured and PR links are available.
        """
        ...  # pragma: no cover
