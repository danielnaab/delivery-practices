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

Content organized by knowledge type:

| Directory | Type | Purpose |
|-----------|------|---------|
| `docs/` | Declarative | Concepts, models, reference |
| `policies/` | Normative | Principles, rules, constraints |
| `playbooks/` | Procedural | Step-by-step guides |
| `notes/` | Ephemeral | Explorations, working notes |
| `specs/` | Specifications | Living specs for repo tooling (dogfooding) |
| `src/` | Source | Tool implementations |
| `tests/` | Tests | Tool tests |

## Current Practice Areas

- **[Living Specifications](docs/)** — Specs as source of truth for system behavior

## Tooling

- **[Backlink Scanner](specs/backlink-scanner.md)** — Scans for `// spec:` annotations and reports spec-to-implementation traceability

```bash
uv run backlink-scanner   # Run the scanner on the repo
uv run pytest             # Run tests
uv run ruff check .       # Lint
```

## Knowledge Base System

Follows [meta-knowledge-base](.graft/meta-knowledge-base/docs/meta.md) conventions:
- Evidence-driven evolution
- Lifecycle states: draft → working → stable → deprecated
- Provenance for all practice recommendations
- Intent-revealing structure

**Status**: Working — First practice area established, structure evolving with evidence
