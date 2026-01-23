# Agent Entrypoint - Delivery Practices KB

You are working in the **delivery-practices knowledge base** - a repository for exploring software delivery practices that enable fast and safe AI-assisted development.

## Before Making Changes

1. Read [knowledge-base.yaml](knowledge-base.yaml) for KB configuration
2. Follow [meta knowledge base conventions](../meta-knowledge-base/docs/meta.md)
3. Understand key policies:
   - **Authority**: docs/ canonical, notes/ exploratory
   - **Provenance**: Ground practice recommendations in sources
   - **Lifecycle**: Mark status (draft/working/stable/deprecated)
   - **Write boundaries**: docs/**, notes/** only

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

Follow the [agent workflow pattern](../meta-knowledge-base/playbooks/agent-workflow.md):

1. **Plan**: State intent, files to touch, uncertainties
2. **Patch**: Make minimal changes to achieve goal
3. **Verify**: Run checks or specify what human should verify

## Content Organization

Content will be organized in `docs/` as it emerges from real project work:
- Create directories for practice areas as needed (e.g., `docs/development/`, `docs/quality/`)
- Use `docs/decisions/` for Architecture Decision Records when significant choices arise
- Use `notes/` for time-bounded explorations and brainstorming

**Current state**: No practice areas yet. Add directories when you have content to put in them.

## Write Boundaries

You may write to:
- `docs/**` - Stable practices and decisions
- `notes/**` - Explorations and brainstorming

Never write to:
- `secrets/**`
- `credentials/**`

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

## Decision Records

For significant practice choices, create decision record in `docs/decisions/`:

**File**: `docs/decisions/YYYYMMDD-descriptive-title.md`

**Format**:
```markdown
# Decision Title

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Context**: Professional (Flexion) | Personal | General

## Context
What problem or situation prompted this decision?

## Decision
What practice or approach are we adopting?

## Consequences
What are the positive and negative implications?

## Alternatives Considered
What else was evaluated? Why not those?

## Sources
Where did this insight come from?
```

## Quick Reference

When updating this KB:
- **New practice discovered?** Add to appropriate docs/ area + cite sources
- **Exploring an idea?** Create note in notes/ with date prefix (YYYY-MM-DD)
- **Making significant choice?** Add decision record
- **Practice stabilizes?** Graduate from notes/ to docs/
- **Practice becomes irrelevant?** Mark status as deprecated

## Current Priorities

This KB is in **early initialization phase**:
- Minimal structure established
- Ready to capture practices from active projects
- Will evolve directories and organization based on evidence

**Critical**: Only create directories/structure when you have content. Don't pre-create practice areas.

Focus on:
1. Real practices from actual experience (not theory)
2. Clear provenance and context for all recommendations
3. Practical applicability to AI-assisted development
4. Evolutionary approach - structure emerges from content, not vice versa

## Examples

**Good practice documentation**:
```markdown
# Code Review with AI-Generated Code

**Status**: working

Our team reviews AI-generated code using a two-pass approach...

## Effectiveness

This approach catches 95% of issues in our experience across 50+ PRs.

## Sources
- Personal experience: [Project X, 3 months, 50+ PRs]
- [GitHub Copilot Best Practices](https://example.com)
```

**Good exploration note**:
```markdown
# 2026-01-25 - Exploring TDD with AI Pair Programming

Trying test-first development with Claude Code...

Quick observations:
- AI good at generating test cases
- Struggles with edge cases initially
- Iterative refinement works well

**Status**: Exploring - will document if effective
```

---

**Remember**:
- Keep changes minimal and focused
- Ground all practice recommendations in sources
- Evolve based on evidence, not speculation
- Use notes/ for exploration, docs/ for stable content
