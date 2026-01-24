---
status: draft
---

# Navigating Spec-Driven Code Changes

Deep dive into making PRs, work logs, and spec-driven changes easy to understand for trusted reviewers.

## The Problem

Spec-driven development with AI assistance produces large, coherent changesets. A single session might touch 10-20 files across specs, implementation, tests, and documentation. Traditional PR review ("read every line of the diff") doesn't scale here.

But these aren't reckless "dump 2000 lines" PRs. They're *structured* changes where:
- A spec defines what should happen
- Code implements those behaviors
- Tests verify them
- Documentation explains why

The structure is already there. We need to surface it for reviewers.

## Progressive Disclosure for PR Review

Apply the [comprehension.md](../docs/comprehension.md) progressive disclosure principle to PR descriptions:

### Level 0: Intent (1-3 sentences)

What was accomplished and why. A reviewer reads this and knows whether the PR is relevant to them.

```
Added link-validator tool: detects broken internal markdown links across
all content directories. Spec-first implementation, 42 tests, found and
fixed 1 broken link in the repo.
```

### Level 1: Component Map

What files changed, grouped by role. A reviewer reads this and knows which files to focus on for their expertise.

```
Spec:           specs/link-validator.md
Implementation: src/link_validator/{validator,__main__}.py
Tests:          tests/{test_validator,test_link_validator_cli}.py
Config:         pyproject.toml (script entry, build, coverage)
Docs:           CHANGELOG.md, specs/README.md
Fixed:          notes/2026-01-23-initialization.md (broken link)
```

### Level 2: Behavior Map

Which spec behaviors map to which code. A reviewer reads this to understand what the code *should* do before reading what it *does*.

```
Link extraction (spec §Behavior/Link extraction)
  → validator.py:_extract_links()
  → tests: TestExtraction (8 cases)

Code block skipping (spec §Behavior/Code block handling)
  → validator.py:_extract_links() fence tracking
  → tests: TestCodeBlockSkipping (6 cases)

Path resolution (spec §Behavior/Path resolution)
  → validator.py:_resolve_path()
  → tests: TestResolvePath (10 cases)

Exit codes (spec §Behavior/Exit codes)
  → __main__.py via tool_cli.run_tool()
  → tests: test_link_validator_cli.py (6 cases)
```

### Level 3: Decisions & Rationale

Why these choices were made. A reviewer reads this when they have "but why?" questions.

```
- Skip inline code spans: `[link](target)` inside backticks are examples, not navigation
- FileNotFoundError for missing dirs: consistent with other tools' error contract
- No argparse: minimal interface doesn't justify the dependency (see tool-cli spec)
```

### Level 4: Session Context

The full exploration narrative. A reviewer reads this when they want to understand the development process.

```
Session note: notes/2026-01-24-tooling-expansion.md
- Three critique cycles refined the implementation
- Dogfooding caught inline code false positives
- Follows writing-specs playbook (validated by use)
```

## How Linking Strategy Enables This

Our existing structure already contains the metadata for every level:

| Level | Source |
|-------|--------|
| Intent | Spec's Intent section |
| Component map | Backlink scanner output (specs → implementors) |
| Behavior map | Spec behavior sections + `spec-section:` annotations |
| Decisions | Spec's Decisions section + session note |
| Context | Session note's Activities/Observations |

**Key insight**: A reviewer doesn't need to read the diff to understand the PR. They can read the spec, then spot-check the diff for correctness. The spec IS the review guide.

## The Spec as Review Guide

For spec-driven changes, the review strategy is:

1. **Read the spec first** — understand what the code should do
2. **Check behavior coverage** — does each spec section have corresponding code?
3. **Spot-check implementation** — for correctness, not comprehension
4. **Verify test coverage** — do tests exercise each behavior statement?
5. **Check consistency** — config, docs, and tooling alignment

This inverts the traditional review flow. Instead of "read code → infer intent," it's "read intent → verify code matches."

## Work Log Structure for Reviewability

Session notes already capture what a PR description needs. The mapping:

| Session note section | PR description level |
|---------------------|---------------------|
| Context | Why this PR exists |
| Activities | What was done (Level 0-1) |
| Decisions | Rationale (Level 3) |
| Observations | Review guidance (what to pay attention to) |
| Metrics | Quick confidence check (test count, coverage) |

**Convention**: When creating a PR from a work session, the session note is your source material. Extract, don't rewrite.

## Structured PR Description Template

A template that maps to our abstraction levels:

```markdown
## Summary
[Level 0: 1-3 sentences of intent]

## Spec
[Link to spec(s) this PR implements or modifies]

## Changes
[Level 1: Component map — files grouped by role]

## Behavior Map
[Level 2: Spec sections → code locations]
[Only for spec-driven changes; skip for config/docs-only PRs]

## Review Strategy
[Suggested approach — which files to read in what order]
[What to focus on vs. what's mechanical/generated]

## Decisions
[Level 3: Key choices and rationale, or link to spec Decisions section]

## Session
[Level 4: Link to session note for full context]
```

## What Could Be Tooled vs. What's Convention

### Convention (now)
- PR description template (above)
- Session notes as PR source material
- Spec-first review order
- Behavior map in PR description

### Tooling (potential)
- **PR description generator**: reads spec + backlink scanner output + session note → generates structured description
- **Behavior map generator**: reads spec behavior sections + `spec-section:` annotations → generates Level 2 map
- **Review guide generator**: reads changed files + their spec annotations → suggests review order
- **Diff grouping**: group diff hunks by spec section rather than alphabetical file order

### Tooling trade-offs
- Generator tools risk becoming stale if conventions change
- Convention-only approach relies on discipline (but our team is small and trusted)
- A lightweight generator (just Level 1 + Level 2) would have high value-to-complexity ratio
- Full diff regrouping is complex and probably not worth it for our scale

## Multi-PR Work Streams

For larger efforts spanning multiple PRs:

### Work stream index
A session note (or dedicated tracking note) that shows:
- Overall goal
- PR sequence with each PR's summary
- Current state and what's next
- Accumulated decisions

### PR ordering for reviewability
When splitting work into PRs, prefer:
1. **Spec PR first** — reviewer understands intent before seeing code
2. **Implementation PR** — reviewer has spec context, can verify
3. **Integration PR** — config, docs, CI changes

This mirrors the development order (spec → implement → integrate) and gives reviewers the same progressive disclosure.

### Alternative: single large PR with navigation
For trusted teams that prefer fewer PRs:
- Use the structured template above
- Add a "Reading Order" section
- Consider collapsible sections for Level 2+ details
- The session note link provides deep context without cluttering the PR

## Open Questions

- **How much structure is too much?** For a 3-file PR, the template is overkill. Where's the threshold?
- **Should behavior maps be generated or hand-written?** Generated is more accurate but requires tooling investment.
- **How do we handle PRs that modify specs?** The spec is both the change and the review guide — circular reference problem.
- **Can review comments reference spec sections?** "This doesn't match §Behavior/Login" is more precise than "this seems wrong."
- **Does this pattern work for non-spec changes?** Config, docs, refactors don't have specs. Do they need their own template?

## Emerging Principles

1. **Specs are review guides** — Read the spec before reading the code. The spec tells you what to verify.
2. **Progressive disclosure in PRs** — Summary for triage, component map for scoping, behavior map for verification.
3. **Extract, don't rewrite** — Session notes already contain the PR description. Surface it, don't duplicate it.
4. **Structure enables tools** — The more structured our artifacts (specs, annotations, session notes), the more we can automate.
5. **Trust enables brevity** — With trusted reviewers, a spec link + summary is often enough. The layers exist for when depth is needed.

## Potential Graduation Paths

- **PR description template** → playbook (procedural, with examples)
- **Spec-as-review-guide** → addition to reviewing-against-specs playbook
- **Behavior map convention** → enhancement to format.md
- **PR description generator** → new spec + implementation in src/
- **Work stream index** → addition to session-logging playbook

## Connections to Existing Practices

- [Comprehension](../docs/comprehension.md) — progressive disclosure principle (#1) directly applies
- [Relationships](../docs/relationships.md) — three-layer model explains why behavior maps work
- [Reviewing against specs](../playbooks/reviewing-against-specs.md) — the spec-first review flow
- [Session logging](../playbooks/session-logging.md) — session notes as PR source material
- [Verification](../docs/verification.md) — backlinks enable computed behavior maps
- [Principles](../policies/living-specifications.md) — #6 (AI-compatible = human-compatible), #13 (references flow upstream, views computed)

## Sources

- Direct observation: Creating PR descriptions for delivery-practices v0.2.0 changes
- [Comprehension UX principles](../docs/comprehension.md) — progressive disclosure, computed views
- Personal experience: Large PR review in professional teams (Flexion)
- Observation: AI-generated changesets are coherent but large; review UX matters more at scale
