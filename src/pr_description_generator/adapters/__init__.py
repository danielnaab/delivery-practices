# spec: specs/pr-description-generator.md

"""Platform-specific link adapters for PR description generation."""

from pr_description_generator.adapters.github import GitHubLinkAdapter
from pr_description_generator.adapters.plain import PlainLinkAdapter

__all__ = ["PlainLinkAdapter", "GitHubLinkAdapter"]
