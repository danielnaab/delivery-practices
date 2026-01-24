---
status: working
---

# Living Specifications

Practices for writing specifications that serve as **living documentation**—always current, collaborative, and integrated with agile delivery and AI-assisted development.

## Contents

1. [Principles](#principles) - Core beliefs driving the approach
2. [Format](#specification-format) - The minimum viable spec structure
3. [Workflow](#workflow-integration) - How specs integrate with development
4. [Collaboration](#collaboration-modes) - Async, ensemble, and AI patterns
5. [Verification](#verification-and-drift-detection) - Keeping specs honest
6. [Artifact Relationships](#artifact-relationships) - Specs, tests, acceptance criteria
7. [Comprehension](#system-comprehension) - Making the system legible
8. [Patterns Borrowed](#patterns-borrowed) - What we took from existing approaches

---

## Principles

These principles drive all specification practices:

1. **Specs live with the code** — Co-located in the repository. Version-controlled, PR-reviewable, AI-readable.

2. **Source-of-truth requires enforcement** — Without mechanism (executable checks, CI, or cultural Definition of Done), "source of truth" is wishful thinking.

3. **Plain language over formal notation** — For team consensus, accessibility matters more than precision. Structured natural language with examples.

4. **Explicit decision states** — Every spec has clear status: proposed → accepted → implemented. Async collaboration requires knowing "can I build against this?"

5. **Low ceremony, high signal** — Updating specs must be lighter than the cost of stale docs. If updating is harder than coding, people won't do it.

6. **AI-compatible is human-compatible** — Unambiguous, complete, well-structured specs serve both audiences. Design for agent comprehension and humans benefit too.

7. **Separate what from why from how** — Specs describe behavior (what), decision records capture rationale (why), code implements (how). Distinct concerns, distinct artifacts.

8. **Async-first, synchronous-to-resolve** — Default to async proposals with clear timeboxes. Escalate to ensemble when not converging. Record outcomes either way.

9. **Tests and specs are complementary** — Tests verify behavior (executable proof); specs explain intent (readable context). Both needed, linked by backlinks.

10. **Evolution over prescription** — Specs should be easy to change. The process encourages refinement, not punishes change.

11. **Open Questions are first-class** — Explicitly marking uncertainty invites collaboration without blocking progress.

12. **Non-goals are as valuable as goals** — Explicitly scoping out prevents scope creep and clarifies boundaries.

13. **References flow upstream, views are computed** — Implementation references specs (backlinks). Tooling aggregates views. Forward links are a maintenance burden.

14. **Fight tribal knowledge** — If it's not in the repo, it doesn't exist. Make implicit conventions explicit.

15. **Specs fill the gap code can't** — Intent, constraints, alternatives, rationale. Don't re-describe what readable code already shows.

---

## Specification Format

### Minimum Viable Structure

```markdown
---
status: proposed | accepted | implemented | deprecated
last-verified: YYYY-MM-DD
owners: [team-members]
---

# [Feature/Component Name]

## Intent

Why does this exist? What problem does it solve?

## Non-goals

What is explicitly out of scope?

## Behavior

What does the system do?

### [Scenario Name]
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

- [Date]: [Decision and brief rationale]

## Sources

- [Reference](URL) - Context
- Personal experience: [Project] - Learning
```

### Section Purposes

| Section | Audience | Purpose |
|---------|----------|---------|
| Intent | Everyone | Why this matters; context for newcomers |
| Non-goals | Reviewers, implementers | Prevent scope creep; clarify boundaries |
| Behavior | Developers, AI, testers | Precise enough to implement and verify |
| Constraints | Developers, ops | Non-functional requirements that often get lost |
| Open Questions | Team | Explicit "not decided yet"—invites collaboration |
| Decisions | Future maintainers | Inline rationale prevents "why is this like this?" archaeology |
| Sources | Everyone | Provenance for trust |

### Design Choices

- **Status is non-negotiable** — without it, nobody knows if the spec is aspirational or authoritative
- **Examples over abstractions** — concrete Given/When/Then scenarios beat general rules
- **No implementation details** — that's what code is for
- **No version history** — git handles this
- **No approval signatures** — PR reviews handle this
- **Structured enough for tools** — behavior statements could be mechanically verified

### Increment Tagging

Behavior statements can indicate which increment introduced them:

```markdown
## Behavior
- Given valid credentials, user receives a session token [v0.1]
- Given expired password, user is prompted to reset [v0.2]
- Rate limit: 5 failed attempts per 10 minutes [v0.3]
```

This allows tickets to reference specific increments: "Implement behaviors marked `[v0.2]`."

---

## Workflow Integration

### When Do Specs Need Updating?

| Change Type | Spec Impact | Action |
|-------------|------------|--------|
| New feature | New spec needed | Spec first, or combined with implementation |
| Behavior change | Must update | Same PR as code change |
| Bug fix (spec wrong) | Correction | Update spec to match intended behavior |
| Bug fix (code wrong) | None | Spec was already correct |
| Refactor | None | No behavior change, spec unchanged |

**Ceremony scales with impact.** Trivial changes need no spec update; behavior changes do.

### The Practical Pattern

```
1. Planning/Refinement
   - Draft spec (status: proposed)
   - Open Questions for unresolved items
   - AI can draft from requirements discussions

2. Async Review (if needed)
   - Team comments, resolves Open Questions
   - Status → accepted when approved

3. Implementation
   - Code against spec
   - If spec gaps found → update spec in same PR
   - PR references spec: "Implements docs/specs/feature-x.md"

4. PR Review
   - Does code match spec?
   - Does spec match intent?
   - If spec updated, validate changes

5. Merge
   - Status → implemented
   - last-verified date updated
```

### Key Reframe

**Spec review IS design review.** It's the same discussion that would happen in Slack or meetings, but captured durably. Not extra work—better-preserved work.

### Anti-patterns

- **Spec-police**: Blocking PRs for trivial missing spec updates
- **Spec-after-the-fact**: Writing specs only to document what's already built
- **Spec-as-ticket**: Treating specs as one-time artifacts that get "done"
- **Approval-ceremony**: Requiring layers beyond normal PR review

---

## Collaboration Modes

### Async (Default)

- Spec proposed via PR with status: proposed
- Team comments inline, resolves Open Questions
- Timeboxed review (e.g., 2 days—silence is consent to proceed)
- Status → accepted when approved
- Works across time zones

### Ensemble (Synchronous)

In ensemble/mob programming, specs are the **residue of design decisions**:

**Spec-First Ensemble Pattern**:
1. First 10 minutes: Write/review spec together (or review AI draft)
2. Resolve Open Questions: Group consensus, right there
3. Implement: Shared understanding from step 1
4. Update as you go: Fix gaps when discovered

**Navigator-as-Scribe**: One navigator updates the spec in real-time while others guide implementation. Navigators have cognitive bandwidth (not typing code), and decisions are verbal and immediate.

**What Ensemble Doesn't Need**:
- Formal sign-off (consensus is immediate)
- Async review periods (whole team present)
- Status fields during session (everyone knows)

The spec must be current *after* the session for async consumers.

### Bridging Modes

Specs are the **continuity artifact** between collaboration modes:

```
Ensemble session → updates spec → async developer picks up next increment
Async developer → updates spec → next ensemble reviews
```

### AI Agent Collaboration

**Specs as the human-AI handoff protocol**:

1. Ensemble (or async team) writes spec — collaborative design, high-bandwidth
2. AI implements against spec — between sessions, fast execution
3. Team reviews — AI's PR checked against spec
4. Spec updated if implementation revealed gaps

The ensemble's advantage is design/judgment. AI's advantage is fast, thorough implementation. The spec is the interface.

**AI also assists spec creation**:
- Draft specs from requirements discussions
- Update specs during implementation
- Flag spec-impacting changes in PRs
- Reduce "writing specs is tedious" friction

---

## Verification and Drift Detection

### Detection Approaches

1. **PR-time analysis**: AI reads spec + code diff, flags inconsistencies. Non-blocking warning. Cheapest moment to fix.
2. **Periodic audit**: Scheduled scan producing drift reports. Noisier but catches gradual drift.
3. **Test-spec linkage**: When tests change without spec changes, flag potential drift.
4. **Structured assertion checking**: Behavior statements precise enough for mechanical verification.

### Backlinks Enable Automation

Implementation annotates which spec it implements:

```python
# spec: docs/specs/auth.md
# spec-section: Behavior/Login
def login(credentials):
    ...
```

Tools can then:
1. Find all files referencing a spec
2. Compare spec intent with implementation
3. Flag divergence

Without backlinks, detection requires guessing which code relates to which spec.

### Git as the Drift Database

Drift findings and resolutions are **structured data in the repo**:

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
    resolution: investigating
```

**Why this matters**:
- Audit trail in git history
- Queryable by tooling and AI agents
- Reviewable in PRs (drift responses are code-reviewed)
- No external dashboard dependency

**Pattern**: Git is the database, structured files are the tables, commits are the transactions.

### Trust Calibration

- **Start high-confidence only** — false positives kill trust in tooling
- **Suggestions, not blockers** — detection over prevention
- **AI flags, humans decide** — no auto-correction (initially)
- **Cost management** — only analyze files referencing specs, only when changed

---

## Artifact Relationships

### The Three-Layer Model

```
SPEC (human-readable, durable, collaborative)
  ↓ maps to
TESTS (executable, durable, CI-enforced)
  ↓ verified by
CODE (implementation, durable, reviewed)
```

Connected by backlinks flowing upstream:
- Tests reference specs: `// spec: docs/specs/auth.md`
- Code references specs where non-obvious
- Specs reference nothing downstream (views computed from backlinks)

### Specs vs. Acceptance Criteria

| Aspect | Spec | Acceptance Criteria |
|--------|------|-------------------|
| Lifespan | Life of the feature | Life of the story |
| Granularity | Complete behavior | Incremental slice |
| Location | Repo (durable) | Ticket (ephemeral) |
| Purpose | Source of truth | Planning/scoping tool |

**Specs subsume acceptance criteria.** AC becomes a reference to spec sections:
- "Implement behaviors marked `[v0.2]` in `docs/specs/auth.md`"
- Ticket doesn't restate requirements—it points to the spec
- No durable information stored in ephemeral containers

### Specs vs. Tests

- **Specs** are readable by non-developers, capture intent and context
- **Tests** are executable, catch regressions, enforced by CI
- Together they form a complete verification chain
- Neither replaces the other

### Why Not BDD/Gherkin?

Given/When/Then is valuable as a **thinking structure** in plain markdown. But the Gherkin tooling ecosystem (step definitions, Cucumber/SpecFlow) adds complexity without proportional benefit for most teams:
- Step definitions are their own maintenance burden
- Hard to be both precise-enough-to-execute AND clear-enough-to-read
- Non-developers rarely read feature files in practice

**Our approach**: Structured prose that maps to tests, without trying to *be* tests.

---

## System Comprehension

### The Meta-Problem

The spec system itself must be legible. Different collaborators need different entry points, different depths, and different representations.

### UX Principles for SDLC

1. **Progressive disclosure** — Don't front-load. Level 0: "we use specs." Level 3: "here's drift detection."
2. **Wayfinding** — Navigable from any starting point (code → spec → tests, all via backlinks and indexes)
3. **Self-describing artifacts** — Each file carries enough context to be understood alone
4. **Consistency** — Every spec looks the same. One learning curve for all.
5. **Contextual orientation** — Entry points orient you (README, CLAUDE.md, frontmatter)
6. **Computed views** — Structured data enables audience-specific representations
7. **Playbooks for tasks** — "How do I write a spec?" vs. "What does the system do?"

### Entrypoint Architecture

```
README.md                      → "What is this project?"
├── CLAUDE.md                  → "What are the rules?" (agents)
├── docs/specs/                → "What does the system do?"
│   └── index.md              → "What specs exist? What status?"
├── docs/playbooks/            → "How do we work?"
│   ├── writing-specs.md
│   ├── ensemble-sessions.md
│   └── reviewing-prs.md
├── .specs/status.yaml         → "What's the health of our specs?"
└── notes/                     → "What's in progress?"
```

### Persona → Entry Point

| Persona | Starts at | Then navigates to |
|---------|-----------|-------------------|
| New team member | README | Playbooks |
| AI agent | CLAUDE.md | Relevant spec |
| Developer mid-flow | Backlink in code | Spec behavior section |
| Ensemble participant | Playbook | Spec being implemented |
| Stakeholder | Specs index | Status + Open Questions |
| Async reviewer | PR description | Referenced spec |

### Playbooks

Task-oriented guides answering "how do I X?":
- How do I write a new spec?
- How do I start an ensemble session with a spec?
- How do I review a PR against its spec?
- How do I update a spec when I discover it's wrong?

Short, action-oriented, linking to relevant artifacts rather than re-explaining.

### Key Insight

**What helps AI agents helps humans.** Both cold-start into unfamiliar systems. Both need orientation, rules, and navigation. Design for agent comprehension and human comprehension follows.

---

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

---

## Sources

- Personal experience: Flexion delivery practices, agile team collaboration
- ADR pattern: Michael Nygard, "Documenting Architecture Decisions" (2011)
- BDD: Dan North, "Introducing BDD" (2006)
- Google Design Docs: public descriptions of internal engineering practices
- Living Documentation: Cyrille Martraire, "Living Documentation" (2019)
- C4 Model: Simon Brown, c4model.com
- RFC process: IETF, Rust RFC process, various company adaptations
- Observation: AI-assisted development workflow patterns (2025-2026)
