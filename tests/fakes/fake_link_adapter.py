# spec: specs/pr-description-generator.md

"""Fake link adapter for testing."""

from dataclasses import dataclass, field


@dataclass
class FakeLinkAdapter:
    """Configurable fake for testing code that uses LinkAdapter protocol.

    All behavior is controlled via constructor arguments, making tests
    explicit about what the adapter should return.
    """

    # Files that "exist" — format_file_link will use exists=True behavior for these
    existing_files: set[str] = field(default_factory=set)

    # Whether to support PR links
    pr_links_supported: bool = False

    # Optional PR files URL to return
    pr_files_url: str | None = None

    # Track all calls for verification
    file_link_calls: list[tuple[str, str, bool]] = field(default_factory=list)
    diff_anchor_calls: list[str] = field(default_factory=list)

    def format_file_link(self, path: str, display_name: str, exists: bool) -> str:
        """Format a link to a file.

        Records the call and returns a predictable format for testing.

        Args:
            path: Relative path to the file.
            display_name: Text to display for the link.
            exists: Whether the file exists in the repository.

        Returns:
            A predictable link format: [display_name](path) if exists,
            otherwise "See `path` in this PR".
        """
        self.file_link_calls.append((path, display_name, exists))
        if exists:
            return f"[{display_name}]({path})"
        return f"See `{path}` in this PR"

    def format_diff_anchor(self, path: str) -> str:
        """Format a URL anchor to a file in PR diff view.

        Records the call and returns a predictable anchor.

        Args:
            path: Relative path to the file.

        Returns:
            A predictable anchor format if PR links supported, empty otherwise.
        """
        self.diff_anchor_calls.append(path)
        if self.pr_links_supported:
            return f"#diff-{path.replace('/', '-')}"
        return ""

    def format_pr_files_url(self) -> str | None:
        """Format URL to PR files changed view.

        Returns:
            The configured pr_files_url.
        """
        return self.pr_files_url

    def supports_pr_links(self) -> bool:
        """Check if this adapter supports PR-specific links.

        Returns:
            The configured pr_links_supported value.
        """
        return self.pr_links_supported

    def check_file_exists(self, path: str) -> bool:
        """Check if a file exists.

        Args:
            path: Relative path to the file.

        Returns:
            True if path is in existing_files set.
        """
        return path in self.existing_files

    def reset(self) -> None:
        """Reset call tracking for a new test."""
        self.file_link_calls.clear()
        self.diff_anchor_calls.clear()
