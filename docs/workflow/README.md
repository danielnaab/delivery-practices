---
status: working
---

# Workflow Practices

Development workflow practices that enable fast and safe delivery, with focus on AI-assisted development.

## What This Is

These practices address how to work effectively in modern development environments where AI accelerates implementation speed. The challenge shifts from "how do I write code" to "how do I maintain quality at speed."

## Guides

- [Iterative Critique](guides/iterative-critique.md) — Build-critique-fix loops for quality
- [Session Logging](guides/session-logging.md) — Preserving context across work sessions
- [PR Descriptions](guides/pr-descriptions.md) — Writing PR descriptions for spec-driven changes
- [Practice Lab](guides/practice-lab.md) — Running team practice improvement meetings

## Core Ideas

### Speed Requires Structure

AI-assisted development produces changes faster than traditional development. Without explicit quality loops, drift accumulates:

- Implementation deviates from spec
- Documentation becomes stale
- Context evaporates between sessions

### Explicit Critique Loops

The [iterative critique](guides/iterative-critique.md) pattern:

```
Build → Critique → Fix → Expand (or Stop)
```

Human provides judgment; AI provides thoroughness.

### Context Preservation

AI conversations are ephemeral. [Session logging](guides/session-logging.md) captures:

- Decisions and their rationale
- Discoveries and observations
- Deferred work and next steps

### Progressive Disclosure for Review

[PR descriptions](guides/pr-descriptions.md) use format tiers (simple/medium/large) to give reviewers exactly the context they need — no more, no less.

## Integration with Living Specifications

These workflow practices work alongside [living specifications](../living-specifications/):

| Practice | Integration Point |
|----------|-------------------|
| Iterative critique | Critique phase checks spec-implementation alignment |
| Session logging | Sessions often produce spec updates |
| PR descriptions | Link to specs as authoritative behavior definition |

## Sources

- [AI-assisted workflow exploration](../../notes/2026-01-24-ai-assisted-workflow.md)
- Direct observation: delivery-practices v0.2.0 development (2026-01-24)
