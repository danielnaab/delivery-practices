---
status: draft
---

# AI-Assisted Development Workflow Patterns

Exploration of workflow patterns that emerged from building the delivery-practices tooling with AI assistance.

## Observed Patterns

### Build → Critique → Fix Loop

The primary development rhythm observed across this project:

1. **Build**: Implement a feature or fix (spec-first when creating new tools)
2. **Critique**: Review the work just completed — look for drift, gaps, inconsistencies
3. **Fix**: Address findings from the critique
4. **Expand**: Identify what's next based on the improved state

This loop is explicitly human-directed ("critique the work you just did") but the critique itself is AI-generated. The human decides when to loop and when to move on.

**Why it works**: The AI has full context of what was just built and can apply consistent scrutiny. The human provides judgment on which findings matter.

**Risk**: Without the human gate, the loop could over-polish or introduce unnecessary changes.

### Spec-First with AI Implementation

Observed workflow for new tools (backlink-scanner, kb-linter, link-validator):

1. Human identifies the need (or AI proposes during critique)
2. Write behavioral spec following the playbook
3. AI implements against the spec
4. Run Step 9 (verify implementation against spec) — catches drift immediately
5. Dogfood on the repo itself — catches real-world edge cases

**Key insight**: The spec acts as a shared contract between human intent and AI implementation. Without it, the AI makes reasonable but potentially wrong architectural choices.

### Structural Integrity as Safety Net

Three tools enforce consistency:
- **backlink-scanner**: Are specs connected to implementations?
- **kb-linter**: Does content follow the rules?
- **link-validator**: Are internal references valid?

These catch classes of errors that are easy to introduce during rapid AI-assisted changes:
- Renaming a file but missing a reference
- Adding content without proper frontmatter
- Writing a spec but not connecting it to code

**Pattern**: Enforcement tooling compensates for the speed of AI-assisted changes. The faster you can make changes, the more you need automated consistency checks.

### Session Logging as Context Preservation

Each work session produces a dated note capturing:
- What was attempted
- What decisions were made
- What was learned
- What's next

This serves two purposes:
1. **For the human**: Record of what happened and why
2. **For future AI sessions**: Context that would otherwise be lost when conversation history ends

### Playbook Validation Through Use

Rather than reviewing playbooks abstractly, we validated them by using them:
- Used writing-specs.md to write specs/link-validator.md
- Used reviewing-against-specs.md to review link-validator against its spec
- Used ensemble-with-specs.md pattern in the AI handoff workflow

Friction during use became improvement signals: missing steps got added, unclear language got clarified.

## Open Questions

- **When to spec vs. when to just build?** Small utilities (tool_cli) don't need specs. Where's the threshold?
- **How much critique is enough?** Three loops for v0.2.0 felt right. Is there a diminishing returns signal?
- **How to preserve cross-session learning?** Session notes help but aren't queryable. Should patterns graduate to playbooks faster?
- **What about rollback?** The build-critique-fix loop assumes forward progress. What happens when a critique reveals the whole approach is wrong?

## Emerging Principles

1. **Speed demands guardrails** — AI makes changes fast; automated enforcement prevents fast mistakes from accumulating.
2. **Specs are communication protocol** — Between human intent and AI implementation, the spec is the contract.
3. **Critique is a skill** — Systematic self-review (or AI-review) catches more than ad hoc checking.
4. **Dogfooding is testing** — Running tools on their own repo is an integration test the test suite can't replicate.
5. **Log everything** — Context evaporates between sessions; explicit notes preserve decision rationale.

## Graduation Status

- **Build-Critique-Fix Loop** → Graduated to [playbooks/iterative-critique.md](../playbooks/iterative-critique.md)
- **Session logging** → Graduated to [playbooks/session-logging.md](../playbooks/session-logging.md)
- **Speed demands guardrails** → Already covered by Principles #2 and #16
- **Spec-First AI Implementation** → Partially covered by writing-specs playbook; remaining patterns still exploratory

## Sources

- Direct observation: Building delivery-practices tooling (2026-01-23 to 2026-01-24)
- Personal experience: Multiple AI-assisted development sessions (2025-2026)
- Related: [policies/living-specifications.md](../policies/living-specifications.md) principles 2, 6, 16
