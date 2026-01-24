---
status: working
---

# Living Specifications

Practices for writing specifications that serve as **living documentation**—always current, collaborative, and integrated with agile delivery and AI-assisted development.

## Overview

Living specifications are the source of truth for system behavior. They sit between intent and implementation, serving as the durable record of what the system does and why.

```
SPEC (human-readable, durable, collaborative)
  ↓ maps to
TESTS (executable, durable, CI-enforced)
  ↓ verified by
CODE (implementation, durable, reviewed)
```

## Reference

- [Format](format.md) — the minimum viable spec template
- [Artifact relationships](relationships.md) — how specs relate to tests, AC, and code
- [Verification](verification.md) — drift detection and keeping specs honest
- [Comprehension](comprehension.md) — making the system legible (UX of the SDLC)

## Rules

- [Principles](../../policies/living-specifications.md) — normative rules governing specification practices

## How-To

- [Writing specs](../../playbooks/writing-specs.md) — how to write or update a specification
- [Ensemble with specs](../../playbooks/ensemble-with-specs.md) — using specs in mob programming
- [Reviewing against specs](../../playbooks/reviewing-against-specs.md) — PR review with specs as source of truth

## Patterns Borrowed

| Pattern | What We Took | What We Left |
|---------|-------------|--------------|
| ADRs | Context → Decision → Consequences; status lifecycle | Point-in-time immutability (specs evolve) |
| RFCs | Propose → discuss → decide; Alternatives Considered; timeboxed review | Heavyweight process; formal numbering |
| BDD/Gherkin | Given/When/Then thinking; example-based specification | Step definitions; Cucumber tooling |
| Google Design Docs | Non-goals; living document expectation; Context section | Google Docs (not version-controlled) |
| Executable Specs | Structured-enough-to-check assertions | Specific framework lock-in |
| C4/arc42 | Explicit abstraction levels | Heavy diagramming upfront |
| Living Documentation | Specs for what code can't express; computed views | Assumption that code is always readable |

**Meta-principle**: Steal structures, not tooling. Adopt thinking patterns without framework lock-in.

## Sources

- Personal experience: Flexion delivery practices, agile team collaboration
- ADR pattern: Michael Nygard, "Documenting Architecture Decisions" (2011)
- BDD: Dan North, "Introducing BDD" (2006)
- Google Design Docs: public descriptions of internal engineering practices
- Living Documentation: Cyrille Martraire, "Living Documentation" (2019)
- C4 Model: Simon Brown, c4model.com
- RFC process: IETF, Rust RFC process, various company adaptations
- Exploration: [notes/2026-01-23-living-specifications.md](../../notes/2026-01-23-living-specifications.md)
