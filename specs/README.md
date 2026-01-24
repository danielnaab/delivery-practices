# Specifications

Living specifications for this repository's tooling. Each spec is a behavioral contract that code in [`src/`](../src/) implements.

> **This directory vs. `docs/`**: Specs here describe *what the tools do*. The [`docs/`](../docs/) directory describes *how to practice* living specifications in downstream projects.

## Specs

| Spec | Status | Purpose |
|------|--------|---------|
| [backlink-scanner.md](backlink-scanner.md) | proposed | Scan for `spec:` annotations, report traceability |

## Lifecycle

Specs use these statuses (defined in [`docs/format.md`](../docs/format.md)):

- **proposed** — Design intent captured, implementation may not be complete
- **accepted** — Team agrees on the contract
- **implemented** — Code satisfies all behavior statements
- **deprecated** — Superseded or no longer relevant

## Backlink Verification

Run the scanner to check spec-implementation traceability:

```bash
uv run backlink-scanner        # Exit 1 if dangling refs or orphan specs
uv run backlink-scanner --report-only  # Always exit 0 (informational)
```
