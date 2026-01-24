# spec: specs/backlink-scanner.md

"""Tests for the backlink scanner."""

from pathlib import Path

from backlink_scanner.scanner import scan


class TestScanningForBacklinks:
    def test_finds_double_slash_annotations(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "src.py").write_text("# spec: specs/auth.md\nx = 1")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["src.py"]

    def test_finds_hash_annotations(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "script.py").write_text("# spec: specs/auth.md\nx = 1")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["script.py"]

    def test_finds_slash_slash_annotations(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "src.ts").write_text("// spec: specs/auth.md\nconst x = 1;")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["src.ts"]

    def test_records_multiple_implementors(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "a.py").write_text("# spec: specs/auth.md")
        (tmp_project / "b.py").write_text("# spec: specs/auth.md")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["a.py", "b.py"]

    def test_records_multiple_specs_from_one_file(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "specs/rate.md").write_text("# Rate")
        (tmp_project / "src.py").write_text("# spec: specs/auth.md\n# spec: specs/rate.md")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["src.py"]
        assert result.specs["specs/rate.md"] == ["src.py"]


class TestDanglingReferences:
    def test_reports_nonexistent_specs(self, tmp_project: Path) -> None:
        (tmp_project / "src.py").write_text("# spec: specs/nonexistent.md")

        result = scan(str(tmp_project))

        assert "specs/nonexistent.md" in result.dangling


class TestOrphanSpecs:
    def test_reports_unreferenced_specs(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/orphan.md").write_text("# Orphan")
        (tmp_project / "src.py").write_text("x = 1")

        result = scan(str(tmp_project))

        assert "specs/orphan.md" in result.orphans

    def test_does_not_report_referenced_specs(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/used.md").write_text("# Used")
        (tmp_project / "src.py").write_text("# spec: specs/used.md")

        result = scan(str(tmp_project))

        assert result.orphans == []


class TestEdgeCases:
    def test_skips_binary_files(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "image.png").write_text("# spec: specs/auth.md")

        result = scan(str(tmp_project))

        assert result.specs == {}

    def test_skips_hidden_dirs(self, tmp_project: Path) -> None:
        (tmp_project / ".git").mkdir()
        (tmp_project / ".git/config").write_text("# spec: specs/auth.md")

        result = scan(str(tmp_project))

        assert result.specs == {}

    def test_skips_ignored_dirs(self, tmp_project: Path) -> None:
        (tmp_project / "node_modules/dep").mkdir(parents=True)
        (tmp_project / "node_modules/dep/index.js").write_text("// spec: specs/auth.md")
        (tmp_project / "__pycache__").mkdir()
        (tmp_project / "__pycache__/mod.pyc").write_text("# spec: specs/auth.md")

        result = scan(str(tmp_project))

        assert result.specs == {}

    def test_handles_empty_directories(self, tmp_project: Path) -> None:
        (tmp_project / "empty").mkdir()

        result = scan(str(tmp_project))

        assert result.specs == {}
        assert result.dangling == []
        assert result.orphans == []

    def test_skips_annotations_inside_code_fences(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "example.md").write_text(
            "# Example\n```python\n# spec: specs/auth.md\ndef login():\n    pass\n```\n"
        )

        result = scan(str(tmp_project))

        assert result.specs == {}

    def test_matches_annotations_outside_code_fences(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "example.md").write_text(
            "# spec: specs/auth.md\n\n```python\n# not matched\n```\n"
        )

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["example.md"]

    def test_ignores_embedded_annotations(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "src.py").write_text('write_file("x", "# spec: specs/auth.md")')

        result = scan(str(tmp_project))

        assert result.specs == {}

    def test_returns_sorted_implementors(self, tmp_project: Path) -> None:
        (tmp_project / "specs").mkdir()
        (tmp_project / "specs/auth.md").write_text("# Auth")
        (tmp_project / "z.py").write_text("# spec: specs/auth.md")
        (tmp_project / "a.py").write_text("# spec: specs/auth.md")
        (tmp_project / "m.py").write_text("# spec: specs/auth.md")

        result = scan(str(tmp_project))

        assert result.specs["specs/auth.md"] == ["a.py", "m.py", "z.py"]
