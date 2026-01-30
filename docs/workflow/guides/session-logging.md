---
status: working
last-validated: 2026-01-24
---

# Session Logging

How to capture work session context so it persists across sessions and is useful to teammates and future AI assistants.

> **Context**: AI-assisted development sessions produce rapid changes. Without explicit logging, decision rationale and exploration paths are lost when the conversation ends.

## When to Log

- At the start of every non-trivial work session
- When the session produces changes worth explaining
- When decisions are made that might be questioned later

**Skip logging for**: single-line fixes, typo corrections, routine dependency updates.

## Session Note Structure

Create a dated note: `notes/YYYY-MM-DD-[topic].md`

```markdown
---
status: working
---

# [Topic]

Date: YYYY-MM-DD

## Context

Why this work is happening. What triggered it.

## Activities

What was done, organized by logical unit (not chronologically).
Include decisions made and their rationale.

## Observations

What was learned. Patterns noticed. Surprises.

## What's Next

What this session sets up for future work.
```

## What to Capture

| Category | Examples |
|----------|----------|
| **Decisions** | "Unified status vocabulary because two parallel lifecycles caused confusion" |
| **Discoveries** | "Running the linter on its own repo revealed 7 violations" |
| **Friction** | "Playbook Step 3 was unclear — had to re-read format.md to understand intent" |
| **Metrics** | "Tests: 30 → 101. Coverage: 80% → 90%" |
| **Deferred work** | "tool_cli needs a spec but not urgent enough for this session" |

## What NOT to Capture

- Blow-by-blow command history (that's what git log is for)
- Routine operations ("ran the linter, it passed")
- Content that belongs in docs/ (graduate it instead)

## Updating the Index

After creating a session note, update `notes/index.md`:

1. Add to the appropriate date section under **Sessions**
2. If the note starts an exploration, add to **Active Explorations**
3. Use format: `- [Title](./filename.md) - Brief description`

## Graduation

When patterns from session notes stabilize:

1. Extract the stable content to the appropriate practice area in docs/
2. Add provenance in the target: `Sources: [note link]`
3. Move from Active Explorations to **Graduated** in the index
4. Keep the note as historical reference (preserves exploratory context)

## For PR Descriptions

Session notes support PR authoring:
- **Activities** section provides the summary bullets
- **Decisions** section provides rationale for reviewers
- **Observations** section highlights what reviewers should pay attention to

## Related

- [Iterative critique](iterative-critique.md) — critique loops feed session notes
- [Notes index](../../../notes/index.md) — where sessions are tracked
- [Notes lifecycle](../../../notes/index.md#note-lifecycle) — graduation paths

## Sources

- Direct observation: 4 session notes produced during delivery-practices development (2026-01-23 to 2026-01-24)
- [AI-assisted workflow exploration](../../../notes/2026-01-24-ai-assisted-workflow.md)
- Pattern: context evaporation between AI sessions is a real problem; explicit notes solve it
