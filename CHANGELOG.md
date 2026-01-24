# Changelog

## [Unreleased]

### Added
- Principle #16 "Dogfood the practices" in policies/living-specifications.md
- notes/2026-01-24-ai-assisted-workflow.md — exploration of AI-assisted development patterns

### Fixed
- README.md: updated with all tools and current commands
- CHANGELOG.md: completed v0.2.0 entries (CI, tool_cli, playbook validation)
- pyproject.toml: added --cov=tool_cli to pytest coverage config
- CI: pinned uv version to >=0.5

## [0.2.0] - 2026-01-24

### Changed
- Unified status vocabulary across all content: draft/working/stable/deprecated (replaces proposed/accepted/implemented in specs)
- Reorganized by knowledge type: docs/ (declarative), policies/ (normative), playbooks/ (procedural), notes/ (ephemeral)
- Flattened docs/specifications/ into docs/ (format, verification, relationships, comprehension)
- Scanner output format: nested structure with `implementors` and `sections` per spec
- Scanner exit codes: exit 1 on dangling references or orphan specs (was always exit 0)
- CLAUDE.md write boundaries now reference knowledge-base.yaml as single source of truth
- docs/verification.md: removed speculative content, tightened to reference doc
- playbooks/writing-specs.md: promoted to working, added Steps 0, 7, 9; iterative-writing note
- playbooks/ensemble-with-specs.md + reviewing-against-specs.md: validated and promoted to working
- pyproject.toml: renamed project to delivery-practices-tools, multi-package build config

### Added
- specs/kb-linter.md + src/kb_linter/ — content linter enforcing knowledge-base.yaml rules
- specs/link-validator.md + src/link_validator/ — broken internal link detection
- specs/backlink-scanner.md + src/backlink_scanner/ — spec-to-implementation traceability
- src/tool_cli/ — shared CLI runner extracted from three identical __main__.py patterns
- .github/workflows/ci.yml — tests + ruff lint/format + all three tools
- `spec-section` annotation support and `--report-only` CLI flag across all tools
- Full test suites: unit + integration tests for all three tools (101 tests)
- policies/living-specifications.md — 15 principles for spec-driven development
- playbooks/ — writing-specs, ensemble-with-specs, reviewing-against-specs
- docs/{format,verification,relationships,comprehension}.md — declarative reference

### Removed
- scripts/ directory (trivial wrappers; README documents the commands directly)

### Fixed
- specs/kb-linter.md: corrected 3 behavior statements (output grouping, parse error, symlinks)
- notes/2026-01-23-initialization.md: fixed broken link to graft-knowledge directory
- specs/backlink-scanner.md: corrected language from "Node.js (TypeScript)" to "Python"

## [0.1.0] - 2026-01-23

### Added
- Initial knowledge base structure
- Graft configuration with meta-kb dependency
- Living specifications practice area (explored and synthesized)
- Notes system for exploration
- Evidence-driven evolution convention
- Knowledge-type directory structure (following meta-kb conventions)
- Required provenance for practice recommendations
