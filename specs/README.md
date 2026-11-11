# Specifications

Living specifications for this repository's tooling. Each spec is a behavioral contract that code in [`src/`](../src/) implements.

> **This directory vs. `docs/`**: Specs here describe *what the tools do*. The [`docs/`](../docs/) directory describes *how to practice* living specifications in downstream projects.

## Specs

| Spec | Status | Purpose |
|------|--------|---------|
| [pr-description-generator.md](pr-description-generator.md) | working | Generate markdown PR descriptions from YAML input |

The structural checkers (backlink scanner, KB linter, link validator) and their specs moved to
[knowledge-base-kit](https://github.com/danielnaab/knowledge-base-kit/tree/v2.0.0/specs); this repository runs the
grafted copy (see [its tools guide](../scions/knowledge-base-kit/docs/tools.md)).

## Lifecycle

Specs use the same status vocabulary as all KB content (see [`docs/README.md`](../docs/README.md#status-semantics)):

- **draft** — Design intent captured, implementation may not be complete
- **working** — Implemented and tested, expected to evolve
- **stable** — Behavior is settled, changes only via explicit decision
- **deprecated** — Superseded or no longer relevant

## Backlink Verification

Run the scanner to check spec-implementation traceability:

```bash
PYTHONPATH=scions/knowledge-base-kit/src python3 -m backlink_scanner .                # Exit 1 if dangling refs or orphan specs
PYTHONPATH=scions/knowledge-base-kit/src python3 -m backlink_scanner . --report-only  # Always exit 0 (informational)
```
