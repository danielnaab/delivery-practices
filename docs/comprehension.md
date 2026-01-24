---
status: working
---

# System Comprehension

How to make the specification system legible to all collaborators—the UX of the SDLC.

## The Meta-Problem

The spec system itself must be legible. Different collaborators need different entry points, different depths, and different representations.

## UX Principles for SDLC

1. **Progressive disclosure** — Don't front-load. Level 0: "we use specs." Level 3: "here's drift detection."
2. **Wayfinding** — Navigable from any starting point (code → spec → tests, all via backlinks and indexes)
3. **Self-describing artifacts** — Each file carries enough context to be understood alone
4. **Consistency** — Every spec looks the same. One learning curve for all.
5. **Contextual orientation** — Entry points orient you (README, CLAUDE.md, frontmatter)
6. **Computed views** — Structured data enables audience-specific representations
7. **Playbooks for tasks** — "How do I write a spec?" vs. "What does the system do?"

## Entrypoint Architecture

```
README.md                      → "What is this project?"
├── CLAUDE.md                  → "What are the rules?" (agents)
├── docs/                      → "What are the concepts?"
│   ├── format.md              → "What goes in a spec?"
│   ├── relationships.md       → "How do artifacts connect?"
│   ├── verification.md        → "How is drift detected?"
│   └── comprehension.md       → "How do people navigate?"
├── policies/                  → "What rules do we follow?"
├── playbooks/                 → "How do I do X?"
├── specs/                     → "What does the tooling do?"
├── src/                       → "Tool implementations"
└── notes/                     → "What's in progress?"
```

## Persona → Entry Point

| Persona | Starts at | Then navigates to |
|---------|-----------|-------------------|
| New team member | README | Playbooks |
| AI agent | CLAUDE.md | Relevant spec |
| Developer mid-flow | Backlink in code | Spec behavior section |
| Ensemble participant | Playbook | Spec being implemented |
| Stakeholder | Specs index | Status + Open Questions |
| Async reviewer | PR description | Referenced spec |

## Knowledge Types as Directories

The directory structure signals what kind of knowledge each file contains:

| Directory | Knowledge Type | Question it answers |
|-----------|---------------|-------------------|
| `docs/` | Declarative | "Understand this" — concepts, models, reference |
| `policies/` | Normative | "Follow this rule" — constraints, principles |
| `playbooks/` | Procedural | "Do this" — step-by-step guidance |
| `notes/` | Ephemeral | "Thinking about this" — explorations |

## Key Insight

**What helps AI agents helps humans.** Both cold-start into unfamiliar systems. Both need orientation, rules, and navigation. Design for agent comprehension and human comprehension follows.

## Related

- [Principles](../policies/living-specifications.md) — #6 (AI-compatible is human-compatible), #14 (fight tribal knowledge)
