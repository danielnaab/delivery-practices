---
status: working
---

# Notes

Working notes and explorations for delivery practices.

Notes are **ephemeral** - graduate to [docs/](../docs/) when stable.

## Active Explorations

- [AI-Assisted Development Workflow](./2026-01-24-ai-assisted-workflow.md) — Patterns from building tooling with AI (partially graduated to [iterative-critique](../docs/workflow/guides/iterative-critique.md) and [session-logging](../docs/workflow/guides/session-logging.md))
- [PR Reviewability](./2026-01-24-pr-reviewability.md) — Making spec-driven changes navigable at multiple abstraction levels (partially graduated to [pr-descriptions](../docs/workflow/guides/pr-descriptions.md))
- [Practice Lab](./2026-01-25-team-practices-meeting.md) — Team practice improvement meeting format (partially graduated to [practice-lab](../docs/workflow/guides/practice-lab.md))

## Graduated

- [Living Specifications](./2026-01-23-living-specifications.md) → Graduated to [docs/living-specifications/](../docs/living-specifications/)

## Sessions

### 2026-01-30
- [USAi Practice Lab Intro](./2026-01-30-usai-practice-lab-intro.md) - Planning for USAi team Practice Lab introduction meeting

### 2026-01-26
- [Repository Restructure](./2026-01-26-repository-restructure.md) - Topic-first organization under docs/

### 2026-01-25
- [Practice Lab](./2026-01-25-team-practices-meeting.md) - Team practice improvement exploration
- [PR Description Generator](./2026-01-25-pr-description-generator.md) - PR description generator implementation and link adapter enhancement

### 2026-01-24
- [PR Reviewability](./2026-01-24-pr-reviewability.md) - Progressive disclosure for spec-driven PRs
- [AI-Assisted Workflow](./2026-01-24-ai-assisted-workflow.md) - Workflow patterns for AI-assisted development
- [Tooling Expansion](./2026-01-24-tooling-expansion.md) - KB linter, link validator, playbook validation, CI, v0.2.0
- [Tooling Cleanup](./2026-01-24-tooling-cleanup.md) - Spec-implementation alignment, exit codes, hygiene

### 2026-01-23
- [Initialization](./2026-01-23-initialization.md) - KB setup
- [Living Specifications](./2026-01-23-living-specifications.md) - Exploring specs as living documentation (graduated)

## Guidelines

- **Time-bound** - Capture point-in-time thinking
- **Date-prefixed** - YYYY-MM-DD format
- **Ephemeral** - Archive or extract when complete
- **Exploratory** - Less rigor than docs/
- **Graduated notes remain** - Kept as historical reference; they preserve the exploratory context and reasoning that led to stable content

## Note Lifecycle

Notes can reach these end states:

| State | Meaning | Action |
|-------|---------|--------|
| **Graduated** | Insights stabilized into docs/ | Mark "Graduated to [location]", keep for reference |
| **Superseded** | A later note or doc covers the same ground better | Mark "Superseded by [link]" |
| **Abandoned** | Exploration didn't lead anywhere useful | Remove from Active, optionally delete |

### Graduation steps

1. Extract stable content to appropriate directory
2. Add provenance in the target: `Sources: [note link]`
3. Mark note "Graduated to [location]" in this index
4. Note remains as historical reference (see Guidelines)
