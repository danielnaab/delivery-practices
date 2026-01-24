# Changelog

## [Unreleased]

### Changed
- Reorganized by knowledge type: docs/ (declarative), policies/ (normative), playbooks/ (procedural), notes/ (ephemeral)
- Flattened docs/specifications/ into docs/ (format, verification, relationships, comprehension)
- Corrected status fields: unvalidated content marked as draft
- Added context notes to playbooks (these describe project repo conventions)

### Added
- specs/backlink-scanner.md — specification for the backlink scanner tool (dogfooding)
- src/backlink-scanner.ts — backlink scanner implementation
- tests/backlink-scanner.test.ts — backlink scanner tests (11 tests)
- policies/living-specifications.md — 15 principles for spec-driven development
- playbooks/writing-specs.md — how to write a specification
- playbooks/ensemble-with-specs.md — using specs in ensemble sessions
- playbooks/reviewing-against-specs.md — reviewing PRs against specs
- docs/{format,verification,relationships,comprehension}.md — declarative reference
- READMEs for policies/ and playbooks/ directories
- package.json, tsconfig.json — project configuration for tooling

## [0.1.0] - 2026-01-23

### Added
- Initial knowledge base structure
- Graft configuration with meta-kb dependency
- Living specifications practice area (explored and synthesized)
- Notes system for exploration

### Conventions Established
- Evidence-driven evolution
- Knowledge-type directory structure (following meta-kb conventions)
- Required provenance for practice recommendations
