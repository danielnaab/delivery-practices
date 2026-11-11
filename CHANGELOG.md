# Changelog

## [Unreleased]

### Changed (2026-11-11: python-kit v2.1.0; the checker comes from knowledge-base-kit)
- Removed this repository's copy of the checker (`src/{backlink_scanner,kb_linter,link_validator,tool_cli}`, their
  tests and `specs/{backlink-scanner,kb-linter,link-validator,tool-cli}.md`). It now lives in
  [knowledge-base-kit](https://github.com/danielnaab/knowledge-base-kit) and runs from the grafted copy:
  `PYTHONPATH=scions/knowledge-base-kit/src python3 -m {backlink_scanner,kb_linter,link_validator} .` (CI does the
  same). Links to the removed specs point at knowledge-base-kit v2.0.0's. `pyproject.toml` drops the three scripts.
- python-kit updated to v2.1.0 (template stubs not taken), and the copier answer `package_name` is now
  `pr_description_generator`, this repository's real package, so future updates target it.

### Changed (2026-11-11: graft v2; living-specifications is a dependency, not a copy)
- Removed `docs/living-specifications/`, the pre-extraction copy of what is now the
  [living-specifications](https://github.com/danielnaab/living-specifications) repository. It is grafted at v1.0.2 into
  `scions/living-specifications/`, and every link now points into that copy. The repository's text was newer in every
  file that differed, so nothing was lost.
- Dependencies moved from graft v0 (`graft.yaml`, `graft.lock`, `.graft/` submodules tracking `main`) to graft v2
  (`flake.nix`, committed `scions/`, pinned tags): meta-knowledge-base v1.1.0, living-specifications v1.0.2,
  python-starter v1.3.0. graft's check and weekly upgrade workflows are in `.forgejo/workflows/`.
- `knowledge-base.yaml` imports and write rules point at `scions/`; `.copier-answers.yml` `_src_path` is python-starter's
  GitHub URL (was `.graft/python-starter`), so `copier update` works from any checkout.
- The link validator, backlink scanner and KB linter skip `scions/`, as they skip `.graft/`.

### Changed
- Reorganized docs/ into practice areas: living-specifications/ and workflow/
- Merged policies/ and playbooks/ into practice area subdirectories (principles.md, guides/)
- Updated knowledge-base.yaml to reflect simplified structure (docs/ and notes/ only)
- Updated specs with new example paths in gherkin scenarios
- Removed "Playbook:" prefix from all guide titles (now using simpler titles consistent with guides/ directory name)
- Promoted pr-descriptions.md from draft to working status
- Removed duplicated Status Semantics section from living-specifications/README.md (defined in parent docs/README.md)
- Updated guide context headers from "This playbook" to "This guide" (writing-specs, reviewing-against-specs, iterative-critique)
- Updated format.md and writing-specs.md examples to use gherkin code blocks (consistent with actual spec format)

### Added
- specs/pr-description-generator.md + src/pr_description_generator/ — generates markdown PR descriptions from structured YAML input
- pr-description: LinkAdapter protocol + PlainLinkAdapter + GitHubLinkAdapter for platform-specific link formatting
- pr-description: `github` YAML config field for GitHub blob URLs and PR diff anchors
- pr-description: FakeLinkAdapter in tests/fakes/ for protocol-based testing
- specs/tool-cli.md — behavioral spec for the shared CLI runner module
- playbooks/iterative-critique.md — build-critique-fix loop (graduated from AI-workflow note)
- playbooks/session-logging.md — session context preservation (graduated from AI-workflow note)
- playbooks/pr-descriptions.md — PR description format for spec-driven changes (graduated from PR reviewability exploration)
- notes/2026-01-24-pr-reviewability.md — PR reviewability exploration (progressive disclosure for review)
- notes/2026-01-26-repository-restructure.md — topic-first reorganization session
- Principle #16 "Dogfood the practices" in policies/living-specifications.md
- notes/2026-01-24-ai-assisted-workflow.md — exploration of AI-assisted development patterns

### Changed
- All specs now use gherkin code blocks for Given/When/Then scenarios (better visual separation, GitHub syntax highlighting)
- pr-description: behavior map files now rendered as clickable links (was plain text)

### Fixed
- pr-description generator: format_links return type annotation (was tuple, actually str)
- pr-description generator: behavior map now filters to only specs listed in input (was showing all specs from backlink JSON)
- pr-description generator: removed dead check_file_exists function (replaced by adapter methods)
- playbooks/writing-specs.md: fixed stale status vocabulary (proposed→draft, implemented→working/stable)
- README.md: updated with all tools and current commands (156 tests)
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
