---
status: working
---

# Tooling Cleanup Session

Date: 2026-01-24

## Context

Critique of the delivery-practices KB identified 10 items of spec-implementation drift, dead code, and documentation hygiene issues. This session addresses them systematically.

## Critique Findings

1. **Dead scripts**: `scripts/setup.sh` and `scripts/test.sh` are trivial wrappers already documented in README
2. **CHANGELOG structure**: Non-standard "Conventions Established" heading under 0.1.0
3. **Write boundary duplication**: CLAUDE.md duplicates the allow/deny list from `knowledge-base.yaml`
4. **docs/verification.md**: Contains speculative `.specs/status.yaml` example not implemented
5. **Spec-implementation drift**: Spec says "Node.js (TypeScript)" but implementation is Python
6. **Missing spec-section support**: Spec describes `spec-section` behavior but scanner doesn't implement it
7. **Output format mismatch**: Spec shows nested `{implementors: [...]}` but code produces flat arrays
8. **Exit code policy**: Spec says "always exit 0" but failing on issues is more useful for CI
9. **No integration tests**: Only unit tests exist; no CLI-level tests
10. **Graduated notes convention**: Not explicit about keeping graduated notes as historical reference

## Decisions Made

- **Remove scripts/**: README already documents `uv sync` and `uv run pytest`
- **Exit codes fail by default**: Dangling refs and orphans are issues worth catching; `--report-only` restores informational mode
- **Nested output format**: Adopt spec's `{implementors: [...], sections: {...}}` structure
- **Reference knowledge-base.yaml from CLAUDE.md**: Single source of truth for write boundaries
- **Keep graduated notes**: Explicitly document that they serve as historical reference

## Changes Implemented

- Created this session note
- Removed `scripts/` directory
- Fixed CHANGELOG structure (folded "Conventions Established" into "Added")
- Updated `notes/index.md` with graduated-notes convention
- Deduplicated write boundaries in CLAUDE.md (reference to knowledge-base.yaml)
- Cleaned up `docs/verification.md` (removed speculative content)
- Updated spec: exit codes, spec-section semantics, Python language, output format
- Implemented `spec-section` support in scanner
- Implemented exit code behavior with `--report-only` flag
- Updated existing tests for new output format
- Added integration tests (`tests/test_cli.py`)
- Updated CHANGELOG with all changes
