---
title: "Living Specifications as Source of Truth"
date: 2026-01-23
status: draft
---

# Living Specifications as Source of Truth

Exploring how to write specifications that serve as living documentation—never stale, collaborative, and integrated with agile delivery and AI-assisted development.

## Problem Statement

We need specification documentation that:
- Stays current (never out of date)
- Is the source of truth for implementation details
- Supports team consensus in plain language
- Integrates with agile cadence
- Works for async collaboration AND synchronous ensemble development

## Axes of Evaluation

### 1. Temporal Lifecycle
- **When is it written?** Before, during, or after implementation?
- **How does it evolve?** Spec-first → implementation → spec-updated-by-implementation?
- **Staleness detection**: How do you know when spec and code have diverged?
- **Retirement**: When does a spec stop being relevant?

### 2. Proximity to Code
- **Co-located** (in-repo, next to source) vs. **external** (wiki, Confluence)
- **Executable specs** (BDD/Gherkin, tests-as-docs) vs. **narrative specs** (prose)
- **Drift detection**: Can tooling alert when spec and implementation diverge?
- The closer to code, the more likely to stay current—but the less accessible to non-developers

### 3. Audience & Readability
- **Developers** implementing the work
- **Reviewers/approvers** who need to understand intent
- **AI agents** consuming specs as implementation guidance
- **Future maintainers** (including future-you)
- **Stakeholders** who care about behavior, not implementation
- **New team members** onboarding

Each audience has different needs for abstraction level, jargon tolerance, and context.

### 4. Collaboration Mode
- **Async**: Comments, PR reviews, threaded discussions—needs clear "state" (proposed/accepted/implemented)
- **Synchronous ensemble**: Real-time editing, verbal discussion captured in writing—needs low-friction capture
- **Hybrid**: Async proposal → synchronous resolution → async refinement
- **Time-zone considerations**: Can decisions progress without everyone present?

### 5. Decision Lifecycle
- **Proposal**: How are changes/additions surfaced?
- **Discussion**: Where does deliberation happen?
- **Consensus**: How do you know agreement is reached? Explicit approval vs. silence-as-consent?
- **Recording**: How is the decision captured for posterity?
- **Revisiting**: Under what conditions can decisions be reopened?

### 6. Granularity & Scope
- **System-level**: Architecture, cross-cutting concerns
- **Feature-level**: User-facing behavior, acceptance criteria
- **Component-level**: API contracts, interfaces
- **Edge-case level**: Error handling, boundary conditions
- Different granularities may need different formats

### 7. Authority & Trust
- **Who can modify specs?** Anyone? Only after consensus?
- **What constitutes approval?** Explicit sign-off? PR merge? No objection within N days?
- **Conflicting information**: When spec and code disagree, which wins?
- **Provenance**: Why was this decision made? By whom? What evidence?

### 8. Agile Integration
- **Refinement**: Specs as the output of backlog refinement?
- **Sprint boundaries**: Spec finalized before sprint? Or evolved within sprint?
- **Definition of Done**: Does DoD include spec updates?
- **Story splitting**: Can specs help identify natural split points?
- **Acceptance criteria**: Are specs and acceptance criteria the same artifact or linked?

### 9. AI-Assisted Development Implications
- **Specs as prompts**: Well-written specs become direct input to AI coding
- **AI as spec author**: AI can draft specs from conversations/requirements
- **AI as verifier**: AI can check implementation against spec
- **Spec quality requirements**: AI needs unambiguous, complete specs—which also benefits humans
- **Feedback loop**: AI implementation reveals spec ambiguities faster than human implementation

### 10. Change Management & History
- **Version control**: Git gives history, but is diff-friendly format enough?
- **Intent preservation**: Can you understand *why* something changed, not just *what*?
- **Breaking changes**: How do you signal that a spec change invalidates existing implementations?
- **Traceability**: Commit → spec change → implementation change → test change

### 11. Cognitive Load & Discovery
- **Findability**: Can someone find the relevant spec for what they're working on?
- **Navigation**: How do specs relate to each other?
- **Ceremony vs. value**: Minimum viable process that keeps specs alive
- **Context switching**: How much overhead to update a spec?

### 12. Format & Tooling
- **Markdown in repo**: Version-controlled, PR-reviewable, AI-readable
- **Structured formats**: YAML/frontmatter for machine-parseable metadata
- **Diagrams**: Mermaid, PlantUML—text-based, version-controlled
- **Tests as specs**: Executable, never stale by definition, but less readable for non-developers
- **Hybrid**: Narrative + executable components

### 13. Feedback Loops
- **How quickly do you learn a spec is wrong?** At implementation? At review? In production?
- **Who notices drift?** Developer? CI? AI?
- **Correction cost**: How expensive is it to fix a stale spec?
- **Prevention vs. detection**: Can the process prevent staleness, or only detect it?

## Key Principles (Emerging)

1. **Specs live with the code** — Co-location in the repository ensures version control, PR-reviewability, and proximity to implementation.

2. **Spec-as-source-of-truth requires enforcement** — Without mechanism (executable specs, CI checks, or cultural DoD), "source of truth" is wishful thinking.

3. **Plain language over formal notation** — For team consensus, accessibility matters more than precision.

4. **Explicit decision states** — Every spec element needs clear status: proposed → under discussion → accepted → implemented.

5. **Low ceremony, high signal** — Updating specs must be lighter than the cost of stale docs.

6. **AI-compatible is human-compatible** — Unambiguous, complete, well-structured specs serve both audiences.

7. **Separate "what" from "why" from "how"** — Specs (behavior), decision records (rationale), code (implementation) are distinct artifacts.

8. **Async-first, synchronous-to-resolve** — Default async with clear timeboxes; escalate to ensemble when not converging.

9. **Tests and specs are complementary, not identical** — Tests verify behavior; specs explain intent. Both needed, linked.

10. **Evolution over prescription** — Specs should be easy to change. The process should encourage refinement, not punish change.

## Exploration: Minimum Viable Spec Format

### Audience Needs Matrix

| Audience | Wants | Tolerates | Doesn't want |
|----------|-------|-----------|--------------|
| Developer implementing | Precise behavior, edge cases, constraints | Some prose | Vague intent without details |
| Reviewer/approver | Clear intent, scope, tradeoffs | Technical detail | Implementation-level minutiae |
| AI agent | Unambiguous requirements, clear boundaries | Structured or prose | Ambiguity, implicit assumptions |
| Future maintainer | Why decisions were made, context | Redundancy | Bare requirements without rationale |
| Stakeholder | Business value, behavior changes | Summaries | Code-level detail |
| New team member | Context, how pieces fit together | Verbose explanation | Jargon without definitions |

### Insight: Layered Structure

No single format serves everyone. A **layered document** gives each audience a section to focus on while keeping everything in one artifact:

```markdown
---
status: proposed | accepted | implemented
last-verified: YYYY-MM-DD
owners: [team-members]
---

# [Feature/Component Name]

## Intent
Why does this exist? What problem does it solve?

## Behavior
What does the system do? (Given/When/Then or plain assertions)

### [Scenario 1]
- Given [precondition]
- When [action]
- Then [expected outcome]

### Edge Cases
- [Case]: [Expected behavior]

## Constraints
- Performance: [requirements]
- Security: [requirements]
- Compatibility: [requirements]

## Open Questions
- [ ] [Unresolved question needing team input]

## Decisions
- [Date]: [Decision made and brief rationale]
```

### Key Tensions Resolved

1. **Precision vs. Accessibility** → Structured natural language with concrete examples (not formal notation, not vague prose)
2. **Completeness vs. Maintainability** → Specify boundaries and behaviors, not implementation steps
3. **Single vs. Multiple artifacts** → One primary spec per feature/component, linked to decision records and tests

### What Makes It "Minimum Viable"

- **Status**: Everyone knows if they can build against this
- **Intent**: Context for anyone encountering it
- **Behavior**: Precise enough for implementation and AI consumption
- **Constraints**: Non-functional requirements that often get lost
- **Open Questions**: Explicit uncertainty invites collaboration without blocking
- **Decisions**: Inline rationale prevents archaeology

### What's Deliberately Excluded

- Implementation details (code handles this)
- Sequence diagrams (add only when genuinely clarifying)
- Version history (git handles this)
- Approval signatures (PR reviews handle this)

### Principles from Q1

- **Spec describes "what" and "why", never "how"**
- **Examples > abstractions** — concrete scenarios beat general rules
- **Open Questions are first-class** — marking uncertainty invites collaboration
- **Status is non-negotiable** — without it, nobody knows if spec is aspirational or authoritative

---

## Exploration: Spec Updates in PR Workflow

### When Do Specs Need Updating?

| Change Type | Spec Impact | Action |
|-------------|------------|--------|
| New feature | New spec needed | Spec PR first, or combined |
| Behavior change | Spec must be updated | Update in same PR as code |
| Bug fix (spec was wrong) | Spec correction | Update spec to match intended behavior |
| Bug fix (code was wrong) | None | Spec was already correct |
| Refactor (no behavior change) | None | Spec unchanged |
| Performance optimization | Maybe constraints | Update if constraints exist |

### Integration Models

- **Spec-first**: Spec PR precedes implementation PR. Clear separation of "what" from "how". Feels heavy for small changes.
- **Combined**: Spec + code in same PR. One workflow, stays synchronized. Large PRs, reviewers may skip spec.
- **Sequential commits**: Spec commits first, then implementation, same PR. Natural narrative, one review. Requires commit discipline.
- **Iterative**: Rough spec during planning, updated during implementation, settled at PR time. Acknowledges reality. Risk of "I'll update later."

### AI Changes the Calculus

- AI can draft specs from requirements discussions (reduces "writing is tedious")
- AI can update specs as part of implementation ("update spec to reflect what we built")
- AI can flag spec-impacting changes ("this PR changes behavior in docs/specs/auth.md")
- Spec-first works better with AI (clear spec → better implementation → natural incentive)

### Ensemble Development Model

In ensemble/mob programming, spec is the *residue of the design conversation*:
1. Group discusses feature at start of session
2. Someone (or AI) captures agreement as spec
3. Implementation follows immediately
4. Lowest-ceremony model: spec is natural byproduct, not bureaucratic artifact

### Practical Integration Pattern

```
1. Planning: Draft spec (status: proposed), Open Questions for unresolved items
2. Async Review: Team comments/resolves, status → accepted
3. Implementation: Code against spec; update spec if gaps found (same PR)
4. PR Review: Does code match spec? Does spec match intent?
5. Merge: Status → implemented, last-verified updated
```

### Key Insight: Spec Review IS Design Review

Reframe: "updating specs" = "design review happens in writing." The spec PR isn't extra work—it's the same design discussion that would happen in Slack/meetings, but captured durably.

### Linking: Backlinks over Forward Links

Insight from discussion: specs should NOT maintain lists of downstream artifacts (code, tests). Instead:

- **References flow upstream**: implementation/tests annotate which spec they implement (e.g., `# spec: docs/specs/auth.md`)
- **Views are computed, not maintained**: tooling (or AI) aggregates backlinks on demand
- **Why**: Forward links are maintenance burden (another staleness vector). Backlinks live where the work happens—low friction, naturally current.
- **AI alignment**: Agents can scan for backlinks cheaply, constructing "what implements this spec?" views without curated link lists

### Anti-patterns

- **Spec-police**: Blocking PRs for missing spec updates on trivial changes
- **Spec-after-the-fact**: Writing specs only to document what was already built
- **Spec-as-ticket**: Treating spec as a ticket that gets "completed" and never revisited
- **Approval-ceremony**: Requiring N sign-offs beyond normal PR approval

### Principles from Q2

- **Spec updates are part of the work, not separate** — same PR, same review
- **Ceremony scales with impact** — trivial changes need no spec update; behavior changes do
- **AI reduces friction** — drafting and updating becomes cheap
- **Ensemble naturally produces specs** — capture design discussions as living docs
- **Spec review IS design review** — durable written form of what would happen verbally
- **References flow upstream, views are computed** — backlinks over forward links

---

## Exploration: AI Detection of Spec-Code Drift

### What Drift Looks Like

1. **Spec says X, code does Y** — behavior divergence (most dangerous)
2. **Spec describes feature that no longer exists** — stale spec (confusing)
3. **Code implements undocumented behavior** — missing spec (risky)
4. **Spec constraints violated** — performance/security drift (subtle)

### Detection Approaches

1. **PR-time analysis (CI)**: AI reads spec + code diff, flags inconsistencies. Non-blocking warning. Feasibility: high.
2. **Periodic audit**: Scheduled scan producing drift reports for team review. Feasibility: high but noisy.
3. **Test-spec linkage verification**: When tests change without spec changes, flag potential drift. Feasibility: medium.
4. **Spec-as-executable-assertion**: Structured behavior statements that can be mechanically verified. Feasibility: medium-high for APIs.

### Backlinks Enable Automation

With upstream references (`# spec: docs/specs/auth.md`), drift detection becomes:
1. Find all files referencing a spec
2. Compare spec intent with implementation
3. Flag divergence

Without backlinks, tool must guess which code relates to which spec—much harder and noisier.

### Key Insight: Git as the Drift Database

Drift findings and resolutions should be **structured data in the repo**, not ephemeral CI output:

```yaml
# .specs/status.yaml (generated by tooling)
checks:
  - spec: docs/specs/auth.md
    last-verified: 2026-01-22
    status: current
    implementors:
      - src/auth/login.ts
      - src/auth/middleware.ts
  - spec: docs/specs/rate-limiting.md
    last-verified: 2026-01-20
    status: drift-detected
    finding: "Spec states 100 req/min, implementation shows 200 req/min"
    detected-in: "PR #47"
    resolution: investigating  # or: accepted-divergence, spec-updated, code-fixed
    resolved-by: null  # or: "commit abc123"
```

Why this matters:
- **Audit trail**: Git history shows when drift detected, how resolved
- **Queryable state**: Tooling/AI can read current drift status at any time
- **Reviewable in PRs**: Drift responses are code-reviewed
- **No external dependency**: No dashboard to maintain, no separate service
- **Agent-friendly**: AI starting work checks status and knows which specs have known drift

Pattern: **Git is the database, structured files are the tables, commits are the transactions.**

### Practical Considerations

- **False positives kill trust** — start high-confidence only
- **Suggestions, not blockers** — detection over prevention
- **Cost management** — only analyze files that reference specs, only when those files change
- **Trust calibration** — AI flags, humans decide (no auto-correction initially)

### Principles from Q3

- **Detection over prevention** — flag drift, don't block progress
- **Backlinks enable automation** — without them, detection is guesswork
- **Git is the system of record for everything** — specs, code, AND their relationship health
- **Structured data enables tooling** — YAML status files are queryable, diffable, reviewable
- **Start high-confidence, expand** — false positives kill trust
- **AI flags, humans decide** — detection yes, auto-correction no
- **PR-time is the cheapest moment** — drift is cheapest to fix before merge

---

## Exploration: Specs, Acceptance Criteria, and Tests

### The Problem

Teams typically maintain three overlapping artifacts:
- **Acceptance criteria** in tickets (ephemeral, lost after sprint)
- **Specs** in docs (durable intent, often stale)
- **Tests** in code (executable, CI-enforced, always current)

They say overlapping things in different places with different lifespans.

### Different Temporal Scopes

| Artifact | Lifespan | Granularity | Lives in |
|----------|----------|-------------|----------|
| Spec | Life of the feature | Complete behavior | Repo (docs/) |
| Acceptance Criteria | Life of the story | Incremental slice | Ticket (ephemeral) |
| Tests | Life of the feature | Executable assertions | Repo (src/) |

Root insight: **teams put durable information in ephemeral containers (tickets), and it gets lost.**

### Proposed Model: Specs Subsume Acceptance Criteria

AC becomes a *view* of the spec, not a separate artifact:

```markdown
## Behavior
- Given valid credentials, user receives a session token [v0.1]
- Given invalid credentials, user sees error message [v0.1]
- Given expired password, user is prompted to reset [v0.2]
- Rate limit: 5 failed attempts per 10 minutes [v0.3]
```

Tickets reference the spec: "Implement behaviors marked `[v0.2]` in `docs/specs/auth.md`."

- **Spec** = durable source of truth (all behavior, all increments)
- **Ticket** = ephemeral reference to spec (which behaviors this sprint)
- **Tests** = executable verification (each spec behavior → test case)
- **No separate AC** that can go stale

### Three-Layer Model

```
SPEC (human-readable, durable, collaborative)
  ↓ maps to
TESTS (executable, durable, CI-enforced)
  ↓ verified by
CODE (implementation, durable, reviewed)
```

Connected by backlinks:
- Tests reference specs (`// spec: docs/specs/auth.md`)
- Code references specs where non-obvious
- Specs reference nothing downstream (views computed)

### Why Not BDD/Gherkin?

BDD merges spec and test into one artifact. In practice:
- Step definitions are their own maintenance burden
- Abstraction layer adds complexity
- Non-developers rarely read feature files
- Hard to be both precise-enough-to-execute AND clear-enough-to-read

Structured prose + separate tests can be simpler than trying to merge them.

### Principles from Q4

- **Specs are durable intent; AC is ephemeral scoping** — don't store durable info in tickets
- **Tests verify specs; they don't replace them** — readability vs. executability
- **Behavior statements map to test cases** — structured enough to verify, readable enough to discuss
- **AC references spec sections** — "implement [v0.2] behaviors" instead of restating requirements
- **Three layers: spec → test → code** — backlinks connect upward
- **BDD is one approach, not the only one** — prose + tests can be simpler

---

## Exploration: Ensemble Programming and Specs

### The Problem Ensemble Has

Design decisions happen verbally in real-time and **evaporate** when the session ends. Only code survives. Steps like "quick design discussion" and "should we handle this edge case?" produce valuable decisions with no durable record.

### Specs as Live Documents in Ensemble

- **Before session**: Draft spec (from ticket, or AI-drafted) becomes the session's "charter"
- **During session**: Navigator updates spec as decisions are made in real-time
- **After session**: Spec already reflects what was decided and built—no "go back and document" step

### Navigator-as-Scribe Pattern

One navigator focuses on spec updates while others guide implementation:
- Navigators have cognitive bandwidth (not typing code)
- Decisions are verbal and immediate—easy to capture in the moment
- Spec becomes the group's shared memory during session
- Disagreements become visible when written down
- AI can assist: "update the spec to reflect that decision"

### Spec-First Ensemble Pattern

1. **First 10 minutes**: Write/review spec together (or review AI-drafted spec)
2. **Resolve Open Questions**: Group consensus on unresolved items, right there
3. **Implement**: Shared understanding; less "what are we building?" mid-session
4. **Update as you go**: Fix spec gaps when implementation reveals them

Prevents anti-pattern: coding before alignment → verbal disagreements mid-session.

### Bridging Ensemble ↔ Async

```
Ensemble session → produces/updates spec → async developer picks up next increment
Async developer → updates spec → next ensemble reviews
```

Spec is the **continuity artifact** between collaboration modes.

### Ensemble + AI Agent Pattern

1. **Ensemble writes spec** (collaborative design, high-bandwidth)
2. **AI implements against spec** (between sessions, fast execution)
3. **Ensemble reviews** (next session, AI's PR against the spec)
4. **Spec updated** if implementation revealed gaps

Spec is the **interface between human design and AI execution**. Ensemble's advantage: design/judgment. AI's advantage: fast, thorough implementation.

### What Ensemble Doesn't Need

- Formal sign-off (consensus is immediate and verbal)
- Async review periods (whole team is present)
- Detailed spec change commit history during session (session IS the review)
- Status fields during session (everyone knows)

These exist to solve async problems. Ensemble needs the spec current *after* the session for async consumers.

### Principles from Q5

- **Specs are residue of ensemble decisions** — natural byproduct, not bureaucracy
- **Navigator-as-scribe** — real-time capture leveraging navigator's cognitive bandwidth
- **Spec-first ensemble** — 10min spec review prevents mid-session confusion
- **Specs bridge ensemble ↔ async** — continuity artifact between modes
- **Specs are the human-AI handoff protocol** — ensemble designs, AI implements
- **Ensemble eliminates async ceremony** — no sign-offs during session; spec must be current after

---

## Exploration: Existing Tools and Patterns

### What We Steal From Each

| From | We Take |
|------|---------|
| ADRs | Context → Decision → Consequences structure; status lifecycle |
| RFCs | Propose → discuss → decide workflow; Alternatives Considered; timeboxed review |
| BDD | Given/When/Then thinking structure; example-based behavior specification |
| Design Docs | Non-goals section; living document expectation; Context section |
| Executable Specs | Structured-enough-to-check behavior assertions |
| C4/arc42 | Explicit abstraction levels; consistent structure |
| Living Documentation | Specs only for what code can't express; computed views |

### Key Insights Per Pattern

- **ADRs**: Good for point-in-time decisions, but specs need to *evolve*. Use ADR-style sections within specs; standalone ADRs for cross-cutting choices only.
- **RFCs**: Good for significant/controversial proposals. Too heavy for routine specs. Keep "Alternatives Considered" and "Open Questions" patterns.
- **BDD/Gherkin**: Given/When/Then is great as a *thinking structure* in plain markdown. Don't adopt the tooling/framework.
- **Google Design Docs**: "Non-goals" section is powerful. Living document expectation is right. Use repo, not Google Docs.
- **Executable Specs**: Structure behaviors so they *could* be checked (by AI or tooling), even if not yet automated.
- **C4/arc42**: Explicit abstraction levels (system/feature/component) reduce confusion about scope.
- **Living Documentation (Martraire)**: Specs should describe what code *can't*: intent, constraints, alternatives, rationale.

### Principles from Q6

- **Steal structures, not tooling** — adopt thinking patterns without framework lock-in
- **Specs fill the gap code can't** — intent, constraints, alternatives, decisions
- **Non-goals are as valuable as goals** — explicitly scoping out prevents scope creep
- **Format for checkability** — behaviors that *could* be verified, even if not yet automated
- **Consistent structure reduces cognitive load** — same format = less time finding info
- **Weight ceremony to significance** — RFC-like for big decisions; lightweight for routine

---

## Exploration: System Comprehension as UX

### The Meta-Problem

The spec system itself is complex. How does the SDLC become legible to its participants? The "product" is the development process. The "users" are all collaborators.

### Collaborator Personas

| Persona | Context | Needs |
|---------|---------|-------|
| New team member | Day 1, unfamiliar | "How does this team work?" |
| AI agent (fresh session) | No prior context | "What are the rules? Where's the spec?" |
| Developer switching projects | Knows patterns, not this project | "What's different here?" |
| Developer mid-flow | Deep in implementation | "What did we decide about X?" |
| Ensemble participant | Synchronous, limited orient time | "What are we building?" |
| Stakeholder | Non-technical, wants status | "What's decided? What's open?" |
| Async reviewer | Reviewing PR, needs context | "What spec does this implement?" |

### UX Principles Applied to SDLC

1. **Progressive Disclosure**: Reveal complexity as needed (Level 0: "we use specs" → Level 3: "here's how drift detection works")
2. **Wayfinding**: Navigable from any starting point (code → spec via backlink; spec → tests via computed view; ticket → spec via reference)
3. **Self-Describing**: Each artifact carries enough context to be understood alone (frontmatter, clear section labels, status)
4. **Consistency**: Every spec/decision/note looks the same — one learning curve
5. **Contextual Orientation**: Entry points orient you (README, CLAUDE.md, spec frontmatter, playbooks)
6. **Multiple Representations**: Structured data enables audience-specific computed views
7. **Playbooks for Tasks**: "How do I?" guides (writing specs, running ensemble, reviewing PRs)

### Entrypoint Architecture

```
README.md (orient: what is this project?)
├── CLAUDE.md (agent: what are the rules?)
├── docs/specs/ (navigate: what does the system do?)
│   ├── index.md (discover: what specs exist, what status?)
│   └── [spec].md (understand: what does this feature do?)
├── docs/playbooks/ (learn: how do we work?)
│   ├── writing-specs.md
│   ├── ensemble-sessions.md
│   └── reviewing-prs.md
├── .specs/status.yaml (query: health of specs)
└── notes/ (explore: what's in progress?)
```

### Key Insight: What Helps AI Helps Humans

AI agents and new team members face the same problem: cold-starting into an unfamiliar system. If the SDLC is legible to an AI reading files, it's legible to a human doing the same. Design for agent comprehension and you get human comprehension for free.

### Principles from Comprehension Exploration

- **Progressive disclosure** — reveal depth as needed
- **Navigable from any starting point** — backlinks, cross-references, indexes
- **Self-describing artifacts** — each file understood alone
- **Consistency is a force multiplier** — same format everywhere
- **Contextual orientation at each entry point** — README, CLAUDE.md, frontmatter, playbooks
- **Computed views over maintained views** — structured data enables audience-specific views
- **Playbooks for tasks, specs for reference** — "how do I?" vs. "what does it do?"
- **What helps AI helps humans** — cold-start legibility benefits both
- **Fight tribal knowledge** — if it's not in the repo, it doesn't exist

---

## All Questions Explored

All open questions have been investigated. Ready for synthesis into delivery practices documentation.

## Sources

- Personal experience: Flexion delivery practices
- Personal experience: Agile team collaboration patterns
- Observation: AI-assisted development workflow needs
- ADR pattern: Michael Nygard (2011)
- BDD: Dan North, "Introducing BDD"
- Google Design Docs: internal Google engineering practices (public descriptions)
- Living Documentation: Cyrille Martraire
- C4 Model: Simon Brown
- RFC process: IETF, Rust RFC process, various company adaptations
