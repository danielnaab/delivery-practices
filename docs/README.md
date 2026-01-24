---
status: working
---

# Living Specifications

Reference material for the living specifications practice — concepts, templates, and relationship models for teams adopting spec-driven development.

> **This directory vs. `specs/`**: The `docs/` directory describes *how to practice* living specifications (for downstream projects). The [`specs/`](../specs/) directory contains *actual behavioral specifications* for this repository's tooling — contracts that code in `src/` implements.

## What This Is

Living specifications are the source of truth for system behavior. They describe what a system does and why, sitting between intent and implementation.

```
SPEC (readable, durable, collaborative)
  ↓ maps to
TESTS (executable, durable, CI-enforced)
  ↓ verified by
CODE (implementation, durable, reviewed)
```

## Reference

- [Format](format.md) — the specification template
- [Relationships](relationships.md) — how specs relate to tests, acceptance criteria, and code
- [Verification](verification.md) — drift detection approaches
- [Comprehension](comprehension.md) — making the system legible to all collaborators

## Rules

- [Principles](../policies/living-specifications.md) — rules governing specification practices

## How-To

- [Writing specs](../playbooks/writing-specs.md) — how to write or update a specification
- [Ensemble with specs](../playbooks/ensemble-with-specs.md) — using specs in mob programming
- [Reviewing against specs](../playbooks/reviewing-against-specs.md) — reviewing PRs with specs as source of truth

## Patterns Borrowed

| Pattern | What We Took | What We Left |
|---------|-------------|--------------|
| ADRs | Context → Decision → Consequences; status lifecycle | Immutability (specs evolve) |
| RFCs | Propose → discuss → decide; Alternatives Considered | Heavyweight process |
| BDD/Gherkin | Given/When/Then as thinking structure | Step definitions; Cucumber |
| Google Design Docs | Non-goals; living document expectation | Google Docs (not version-controlled) |
| Executable Specs | Structured-enough-to-check assertions | Framework lock-in |
| Living Documentation | Specs for what code can't express; computed views | Assumption code is always readable |

Guiding principle: steal structures, not tooling.

## Status Semantics

All content carries a lifecycle status in frontmatter:

| Status | Meaning |
|--------|---------|
| `draft` | Exploratory — may change substantially or be discarded |
| `working` | In use, expected to evolve — usable now, not frozen |
| `stable` | Settled — changes only via explicit decision |
| `deprecated` | Superseded — kept for historical reference |

## Sources

- Exploration: [notes/2026-01-23-living-specifications.md](../notes/2026-01-23-living-specifications.md)
- ADR pattern: Michael Nygard, "Documenting Architecture Decisions" (2011)
- BDD: Dan North, "Introducing BDD" (2006)
- Living Documentation: Cyrille Martraire (2019)
- C4 Model: Simon Brown
