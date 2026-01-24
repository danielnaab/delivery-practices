# Tooling Architecture: Flat Now, Evolve When Warranted

**Status**: Working
**Date**: 2026-01-24

## Context

We adopted [python-starter](/.graft/python-starter/) for scaffolding: `pyproject.toml`, ruff, pytest, uv. The template also provides architecture layers (domain models, protocols, services, adapters, context objects) designed for larger applications.

The backlink scanner is a single-purpose CLI tool: walk files, match annotations, report results. Its complexity doesn't warrant protocol hierarchies, adapter layers, or context objects today.

## Decision

Start with a flat module structure. Evolve toward python-starter patterns individually, each triggered by a concrete complexity need.

## Evolution Triggers

| Trigger | Pattern to adopt |
|---------|-----------------|
| Multiple scan strategies or output formats | Protocols (strategy pattern) |
| Configuration beyond a single directory path | Context objects |
| External integrations (git, CI APIs) | Adapters |
| Multiple CLI commands | Typer with command groups |

## What to Adopt from python-starter

When triggers are met, adopt these patterns specifically:

- **Protocol-based interfaces** — define behavior contracts without inheritance
- **Functional services with context** — pure functions that receive a context object
- **Fakes over mocks in tests** — test doubles that implement protocols, not mock patches

## What We Already Use

- `pyproject.toml` with project metadata and tool configuration
- ruff for linting and formatting
- pytest for testing
- uv for dependency management
- Script entrypoints via `[project.scripts]`

## Sources

- `.graft/python-starter/` — template providing the architecture patterns
- Backlink scanner spec: `specs/backlink-scanner.md`
