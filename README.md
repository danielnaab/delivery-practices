# Delivery Practices Knowledge Base

Knowledge base for exploring **software delivery practices that enable fast and safe AI-assisted development**.

## Entrypoints

- **Humans**: [docs/README.md](docs/README.md)
- **Agents**: [CLAUDE.md](CLAUDE.md)

## Purpose

Personal exploration of delivery practices for:
- Fast, safe development with AI assistance
- SDLC practices that work in professional contexts (including Flexion)
- Evidence-based evolution of effective methods

## Structure

**Knowledge content** (organized by type):

| Directory | Type | Purpose |
|-----------|------|---------|
| `docs/` | Declarative | Concepts, models, reference |
| `policies/` | Normative | Principles, rules, constraints |
| `playbooks/` | Procedural | Step-by-step guides |
| `notes/` | Ephemeral | Explorations, working notes |

**Tooling** (dogfooding the practices):

| Directory | Purpose |
|-----------|---------|
| `specs/` | Living specifications for tools |
| `src/` | Python implementations |
| `tests/` | Pytest test suite |

## Current Practice Areas

- **[Living Specifications](docs/)** — Specs as source of truth for system behavior

## Tooling

Three structural integrity tools, all spec-first with no runtime dependencies:

| Tool | Spec | Purpose |
|------|------|---------|
| `backlink-scanner` | [spec](specs/backlink-scanner.md) | Spec-to-implementation traceability via `# spec:` annotations |
| `kb-linter` | [spec](specs/kb-linter.md) | Validates frontmatter status and provenance against `knowledge-base.yaml` |
| `link-validator` | [spec](specs/link-validator.md) | Detects broken internal markdown links |

```bash
uv run backlink-scanner        # Traceability check (exit 1 on issues)
uv run kb-linter               # Content rule enforcement
uv run link-validator           # Broken link detection
uv run pytest                  # Run tests (101 tests)
uv run ruff check .            # Lint
uv run ruff format --check .   # Format check
```

All tools support `--report-only` for informational output (always exit 0).

## Knowledge Base System

Follows [meta-knowledge-base](.graft/meta-knowledge-base/docs/meta.md) conventions:
- Evidence-driven evolution
- Lifecycle states: draft → working → stable → deprecated
- Provenance for all practice recommendations
- Intent-revealing structure

**Status**: Working — First practice area established, structure evolving with evidence
