# Agent Entrypoint - Delivery Practices KB

You are working in the **delivery-practices knowledge base** - a repository for exploring software delivery practices that enable fast and safe AI-assisted development.

## Before Making Changes

1. Read [knowledge-base.yaml](knowledge-base.yaml) for KB configuration
2. Follow [meta knowledge base conventions](.graft/meta-knowledge-base/docs/meta.md)
3. Understand key policies:
   - **Authority**: docs/ canonical, notes/ exploratory
   - **Provenance**: Ground practice recommendations in sources
   - **Lifecycle**: Mark status (draft/working/stable/deprecated)
   - **Write boundaries**: docs/**, policies/**, playbooks/**, notes/**

## Your Role

As a knowledge curator for delivery practices:

- **Capture practices** from real projects with clear provenance
- **Ground in evidence** - cite sources, experiences, references
- **Respect context** - acknowledge Flexion practices but don't limit to them
- **Record tradeoffs** - use decision records for significant choices
- **Explore in notes** - brainstorm in notes/, stabilize in docs/

## Critical Context

This KB focuses on **delivery practices for AI-assisted development**:
- How AI changes development workflows
- Quality practices for AI-generated code
- Maintaining safety and speed simultaneously
- What enables effectiveness in modern SDLC

## Workflow: Plan → Patch → Verify

Follow the [agent workflow pattern](.graft/meta-knowledge-base/playbooks/agent-workflow.md):

1. **Plan**: State intent, files to touch, uncertainties
2. **Patch**: Make minimal changes to achieve goal
3. **Verify**: Run checks or specify what human should verify

## Content Organization

**Knowledge content** (organized by type):

| Directory | Type | Purpose |
|-----------|------|---------|
| `docs/` | Declarative | Concepts, models, reference ("understand this") |
| `policies/` | Normative | Principles, rules, constraints ("follow this") |
| `playbooks/` | Procedural | Step-by-step guides ("do this") |
| `notes/` | Ephemeral | Explorations, working notes ("thinking about this") |

**Tooling** (dogfooding the practices):

| Directory | Purpose |
|-----------|---------|
| `specs/` | Living specifications for tools |
| `src/` | Python implementations |
| `tests/` | Pytest test suite |

Practice areas span these types. For example, "living specifications" has:
- `docs/` — conceptual reference (format, relationships, verification, comprehension)
- `policies/living-specifications.md` — principles
- `playbooks/writing-specs.md` — how-to guides

## Write Boundaries

Consult [`knowledge-base.yaml`](knowledge-base.yaml) `rules.writes` for the authoritative allow/deny list.

In brief: you may write to knowledge content (`docs/`, `policies/`, `playbooks/`, `notes/`) and tooling (`specs/`, `src/`, `tests/`). Never write to managed directories (`.graft/`) or sensitive paths (`secrets/`, `credentials/`).

## Provenance Requirements

Always include **Sources** sections for:
- Practice recommendations (critical for trust)
- Factual claims about tools or methods
- Operational guidance
- Tradeoff analysis

Format:
```markdown
## Sources
- [Source Title](URL or path) - Brief context
- Personal experience: [Project/Context] - What was learned
```

## Quick Reference

When updating this KB:
- **New practice discovered?** Add to appropriate docs/ area + cite sources
- **New rule/principle?** Add to policies/
- **New how-to guide?** Add to playbooks/
- **Exploring an idea?** Create note in notes/ with date prefix (YYYY-MM-DD)
- **Making significant choice?** Add decision record in docs/decisions/
- **Practice stabilizes?** Graduate from notes/ to docs/
- **Practice becomes irrelevant?** Mark status as deprecated

## Current State

- **Living specifications** practice area established (docs/, policies/, playbooks/)
- **Backlink scanner** tool in src/ with spec in specs/ (dogfooding)
- Structure follows meta-kb knowledge-type conventions
- Ready to capture additional practice areas from active work

Focus on:
1. Real practices from actual experience (not theory)
2. Clear provenance and context for all recommendations
3. Practical applicability to AI-assisted development
4. Correct knowledge type placement (declarative vs. normative vs. procedural)

---

**Remember**:
- Keep changes minimal and focused
- Ground all practice recommendations in sources
- Evolve based on evidence, not speculation
- Place content in the right knowledge-type directory
