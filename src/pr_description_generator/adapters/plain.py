# spec: specs/pr-description-generator.md

"""Plain link adapter — relative markdown links without platform-specific URLs."""

from pathlib import Path


class PlainLinkAdapter:
    """Adapter for plain markdown links.

    Formats links as relative markdown links without any platform-specific URLs.
    This is the default adapter when no GitHub configuration is provided.
    """

    def __init__(self, root_dir: str = ".") -> None:
        """Initialize the plain adapter.

        Args:
            root_dir: Root directory for checking file existence.
        """
        self._root_dir = root_dir

    def format_file_link(self, path: str, display_name: str, exists: bool) -> str:
        """Format a link to a file.

        Args:
            path: Relative path to the file.
            display_name: Text to display for the link.
            exists: Whether the file exists in the repository.

        Returns:
            Markdown link if file exists, otherwise "See in PR" reference.
        """
        if exists:
            return f"[{display_name}]({path})"
        return f"See `{path}` in this PR"

    def format_diff_anchor(self, path: str) -> str:
        """Format a URL anchor to a file in PR diff view.

        Args:
            path: Relative path to the file.

        Returns:
            Empty string (plain adapter doesn't support PR diff links).
        """
        return ""

    def format_pr_files_url(self) -> str | None:
        """Format URL to PR files changed view.

        Returns:
            None (plain adapter doesn't support PR links).
        """
        return None

    def supports_pr_links(self) -> bool:
        """Check if this adapter supports PR-specific links.

        Returns:
            False (plain adapter doesn't support PR links).
        """
        return False

    def check_file_exists(self, path: str) -> bool:
        """Check if a file exists at root_dir/path.

        Args:
            path: Relative path to the file.

        Returns:
            True if file exists, False otherwise.
        """
        full_path = Path(self._root_dir) / path
        return full_path.exists()
