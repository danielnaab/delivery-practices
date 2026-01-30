# Agent Entrypoint - Delivery Practices KB

You are working in the **delivery-practices knowledge base** - a repository for exploring software delivery practices that enable fast and safe AI-assisted development.

## Before Making Changes

1. Read [knowledge-base.yaml](knowledge-base.yaml) for KB configuration
2. Follow [meta knowledge base conventions](.graft/meta-knowledge-base/docs/meta.md)
3. Understand key policies:
   - **Authority**: docs/ canonical, notes/ exploratory
   - **Provenance**: Ground practice recommendations in sources
   - **Lifecycle**: Mark status (draft/working/stable/deprecated) — see [status semantics](docs/README.md#status-semantics)
   - **Write boundaries**: see [`knowledge-base.yaml`](knowledge-base.yaml) `rules.writes`

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

**Practice documentation** (organized by topic):

| Directory | Practice Area |
|-----------|---------------|
| [`docs/living-specifications/`](docs/living-specifications/) | Spec-driven development |
| [`docs/workflow/`](docs/workflow/) | Development workflow practices |
| [`docs/decisions/`](docs/decisions/) | Cross-cutting architectural decisions |
| `notes/` | Explorations, working notes ("thinking about this") |

Each practice area contains:
- Reference docs (concepts, models)
- Principles (rules, constraints)
- Guides (how-to procedures)

**Tooling** (dogfooding the practices):

| Directory | Purpose |
|-----------|---------|
| [`specs/`](specs/) | Behavioral specifications for *this repo's* tools |
| `src/` | Python implementations of those specs |
| `tests/` | Pytest test suite verifying spec compliance |

**Key distinction**: `docs/` describes *how to practice* delivery practices (for downstream projects). `specs/` contains *behavioral contracts* for this repo's tooling — what the code in `src/` must do.

## Write Boundaries

Consult [`knowledge-base.yaml`](knowledge-base.yaml) `rules.writes` for the authoritative allow/deny list.

In brief: you may write to practice documentation (`docs/`), explorations (`notes/`), and tooling (`specs/`, `src/`, `tests/`). Never write to managed directories (`.graft/`) or sensitive paths (`secrets/`, `credentials/`).

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
- **New practice discovered?** Add to appropriate practice area in docs/ + cite sources
- **New principle?** Add to the practice area's principles file
- **New how-to guide?** Add to the practice area's guides/ directory
- **Exploring an idea?** Create note in notes/ with date prefix (YYYY-MM-DD)
- **Making significant choice?** Add decision record in docs/decisions/
- **Practice stabilizes?** Graduate from notes/ to docs/
- **Practice becomes irrelevant?** Mark status as deprecated

## Current State

Practice areas established:
- **[Living specifications](docs/living-specifications/)** — spec-driven development
- **[Workflow](docs/workflow/)** — development workflow practices (iterative critique, session logging, PR descriptions)

Tooling (dogfooding):
- **[Backlink scanner](specs/backlink-scanner.md)**, **[kb-linter](specs/kb-linter.md)**, **[link-validator](specs/link-validator.md)**, **[pr-description](specs/pr-description-generator.md)** — tools in [src/](src/) with specs in [specs/](specs/)

Focus on:
1. Real practices from actual experience (not theory)
2. Clear provenance and context for all recommendations
3. Practical applicability to AI-assisted development
4. Place content in the appropriate practice area

---

**Remember**:
- Keep changes minimal and focused
- Ground all practice recommendations in sources
- Evolve based on evidence, not speculation
- Place content in the appropriate practice area under docs/
