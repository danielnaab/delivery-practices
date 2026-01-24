# Changelog

## [Unreleased]

### Changed
- Reorganized by knowledge type: docs/ (declarative), policies/ (normative), playbooks/ (procedural), notes/ (ephemeral)
- Flattened docs/specifications/ into docs/ (format, verification, relationships, comprehension)
- Corrected status fields: unvalidated content marked as draft
- Added context notes to playbooks (these describe project repo conventions)
- Scanner output format: nested structure with `implementors` and `sections` per spec
- Scanner exit codes: exit 1 on dangling references or orphan specs (was always exit 0)
- CLAUDE.md write boundaries now reference knowledge-base.yaml as single source of truth
- docs/verification.md: removed speculative content, tightened to reference doc

### Added
- `spec-section` annotation support in backlink scanner
- `--report-only` CLI flag (always exit 0, for informational use)
- tests/test_cli.py — integration tests for CLI output and exit codes
- specs/backlink-scanner.md — specification for the backlink scanner tool (dogfooding)
- src/backlink_scanner/ — Python implementation (no runtime dependencies)
- tests/test_scanner.py — unit tests with pytest
- policies/living-specifications.md — 15 principles for spec-driven development
- playbooks/writing-specs.md — how to write a specification
- playbooks/ensemble-with-specs.md — using specs in ensemble sessions
- playbooks/reviewing-against-specs.md — reviewing PRs against specs
- docs/{format,verification,relationships,comprehension}.md — declarative reference
- READMEs for policies/ and playbooks/ directories
- pyproject.toml — project configuration (uv, ruff, pytest)
- python-starter graft dependency for project scaffolding

### Removed
- scripts/ directory (trivial wrappers; README documents the commands directly)

### Fixed
- specs/backlink-scanner.md: corrected language from "Node.js (TypeScript)" to "Python"
- CHANGELOG 0.1.0: folded non-standard "Conventions Established" heading into "Added"

## [0.1.0] - 2026-01-23

### Added
- Initial knowledge base structure
- Graft configuration with meta-kb dependency
- Living specifications practice area (explored and synthesized)
- Notes system for exploration
- Evidence-driven evolution convention
- Knowledge-type directory structure (following meta-kb conventions)
- Required provenance for practice recommendations
