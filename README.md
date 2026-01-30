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

**Practice documentation** (organized by topic):

| Directory | Practice Area |
|-----------|---------------|
| [`docs/living-specifications/`](docs/living-specifications/) | Spec-driven development |
| [`docs/workflow/`](docs/workflow/) | Development workflow practices |
| [`docs/decisions/`](docs/decisions/) | Cross-cutting architectural decisions |
| `notes/` | Explorations, working notes |

**Tooling** (dogfooding the practices):

| Directory | Purpose |
|-----------|---------|
| `specs/` | Living specifications for tools |
| `src/` | Python implementations |
| `tests/` | Pytest test suite |

## Practice Areas

- **[Living Specifications](docs/living-specifications/)** — Specs as source of truth for system behavior
- **[Workflow](docs/workflow/)** — Development workflow practices (iterative critique, session logging, PR descriptions)

## Tooling

Spec-first tools for structural integrity and workflow support:

| Tool | Spec | Purpose |
|------|------|---------|
| `backlink-scanner` | [spec](specs/backlink-scanner.md) | Spec-to-implementation traceability via `# spec:` annotations |
| `kb-linter` | [spec](specs/kb-linter.md) | Validates frontmatter status and provenance against `knowledge-base.yaml` |
| `link-validator` | [spec](specs/link-validator.md) | Detects broken internal markdown links |
| `pr-description` | [spec](specs/pr-description-generator.md) | Generates markdown PR descriptions from YAML input |

```bash
uv run backlink-scanner        # Traceability check (exit 1 on issues)
uv run kb-linter               # Content rule enforcement
uv run link-validator          # Broken link detection
uv run pr-description input.yaml  # Generate PR description
uv run pytest                  # Run tests (193 tests)
uv run ruff check .            # Lint
uv run ruff format --check .   # Format check
```

Validator tools support `--report-only` for informational output (always exit 0).

## Knowledge Base System

Follows [meta-knowledge-base](.graft/meta-knowledge-base/docs/meta.md) conventions:
- Evidence-driven evolution
- Lifecycle states: draft → working → stable → deprecated
- Provenance for all practice recommendations
- Intent-revealing structure

**Status**: Working — First practice area established, structure evolving with evidence
