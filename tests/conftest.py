"""Pytest fixtures for backlink scanner tests."""

from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Provide a temporary directory for test fixtures."""
    return tmp_path
