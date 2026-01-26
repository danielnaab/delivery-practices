---
status: working
---

# Delivery Practices Documentation

Practice areas for fast and safe software delivery, with particular focus on AI-assisted development.

## Practice Areas

### [Living Specifications](living-specifications/)

Spec-driven development using living specifications as the source of truth for system behavior. Includes format, verification approaches, and guides for writing and reviewing against specs.

### [Workflow](workflow/)

Development workflow practices: iterative critique loops, session context preservation, and PR authoring for spec-driven changes.

## Cross-Cutting

### [Decisions](decisions/)

Architectural Decision Records (ADRs) that apply across practice areas.

## Tooling

This repository also contains tools that support these practices:

| Tool | Purpose |
|------|---------|
| [backlink-scanner](../specs/backlink-scanner.md) | Spec-to-implementation traceability |
| [kb-linter](../specs/kb-linter.md) | Content linter enforcing knowledge-base rules |
| [link-validator](../specs/link-validator.md) | Broken internal link detection |
| [pr-description](../specs/pr-description-generator.md) | PR description generator from YAML input |

See [`specs/`](../specs/) for behavioral specifications and [`src/`](../src/) for implementations.

## Status Semantics

All content carries a lifecycle status in frontmatter:

| Status | Meaning |
|--------|---------|
| `draft` | Exploratory — may change substantially or be discarded |
| `working` | In use, expected to evolve — usable now, not frozen |
| `stable` | Settled — changes only via explicit decision |
| `deprecated` | Superseded — kept for historical reference |

## Sources

- Practice exploration: [notes/2026-01-23-living-specifications.md](../notes/2026-01-23-living-specifications.md)
- Workflow patterns: [notes/2026-01-24-ai-assisted-workflow.md](../notes/2026-01-24-ai-assisted-workflow.md)
