# spec: specs/backlink-scanner.md

"""Core scanning logic for finding spec backlink annotations in source files."""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

SPEC_PATTERN = re.compile(r"^\s*(?://|#)\s*spec:\s*([\w./\-]+)\s*$")
FENCE_PATTERN = re.compile(r"^\s*```")

BINARY_EXTENSIONS = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".bin",
        ".exe",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".mp3",
        ".mp4",
        ".wav",
        ".avi",
    }
)

SKIP_DIRS = frozenset({".git", ".graft", ".venv", "node_modules", "__pycache__"})


@dataclass
class ScanResult:
    """Result of scanning a directory for backlink annotations."""

    specs: dict[str, list[str]] = field(default_factory=dict)
    dangling: list[str] = field(default_factory=list)
    orphans: list[str] = field(default_factory=list)


def _is_binary(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in BINARY_EXTENSIONS


def _get_files(root: Path) -> list[str]:
    """Recursively collect file paths relative to root, skipping hidden/ignored dirs."""
    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root)
            files.append(rel_path)
    return files


def _scan_file(root: Path, file: str) -> list[str]:
    """Extract spec paths referenced by annotations in a file."""
    if _is_binary(file):
        return []

    full_path = root / file
    try:
        content = full_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    is_markdown = file.endswith(".md")
    in_code_fence = False
    spec_paths: list[str] = []

    for line in content.splitlines():
        if is_markdown and FENCE_PATTERN.match(line):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        match = SPEC_PATTERN.match(line)
        if match:
            spec_paths.append(match.group(1))

    return spec_paths


def scan(root_dir: str) -> ScanResult:
    """Scan a directory for spec backlink annotations.

    Finds files containing annotations like `// spec: path/to/spec.md`
    or `# spec: path/to/spec.md` and builds a mapping of specs to implementors.

    Args:
        root_dir: The directory to scan.

    Returns:
        ScanResult with specs, dangling references, and orphan specs.
    """
    root = Path(root_dir).resolve()
    files = _get_files(root)
    spec_refs: dict[str, set[str]] = {}

    for file in files:
        for spec_path in _scan_file(root, file):
            if spec_path not in spec_refs:
                spec_refs[spec_path] = set()
            spec_refs[spec_path].add(file)

    # Find spec files in the specs/ directory
    spec_files = [f for f in files if f.startswith("specs/") and f.endswith(".md")]

    # Identify dangling references (referenced specs that don't exist)
    dangling = [sp for sp in spec_refs if not (root / sp).exists()]

    # Identify orphan specs (spec files with no references)
    orphans = [f for f in spec_files if f not in spec_refs]

    # Build output with sorted implementors
    specs = {sp: sorted(implementors) for sp, implementors in spec_refs.items()}

    return ScanResult(specs=specs, dangling=dangling, orphans=orphans)
