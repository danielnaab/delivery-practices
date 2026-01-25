# spec: specs/pr-description-generator.md

"""Data models for PR description generator."""

from dataclasses import dataclass, field
from enum import Enum


class Format(Enum):
    """PR description format types."""

    SIMPLE = "simple"
    MEDIUM = "medium"
    LARGE = "large"
    NON_SPEC = "non-spec"


@dataclass
class PRInput:
    """Parsed PR description input from YAML."""

    format: Format
    summary: str
    verify: str
    specs: list[str] = field(default_factory=list)
    sessions: list[str] = field(default_factory=list)
    changes: str = ""
    focus: str = ""
    breaking: str = ""
    decisions: list[str] = field(default_factory=list)
    behavior_map_source: str = ""
    root_dir: str = "."


@dataclass
class BehaviorMapEntry:
    """A single behavior map entry: section → files."""

    section: str
    files: list[str]
