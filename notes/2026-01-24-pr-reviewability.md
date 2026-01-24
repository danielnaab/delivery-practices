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

## Worked Example: v0.2.0 as a Single PR

If the entire v0.2.0 release had been a single PR (8 commits, 30+ files, 3 new tools), here's what the structured description would look like:

### Summary (Level 0)
> Three structural integrity tools (backlink-scanner, kb-linter, link-validator), all spec-first with CI enforcement. Unified status vocabulary, validated all playbooks through use, consolidated CLI boilerplate.

### Changes (Level 1)
```
New specs:       specs/{backlink-scanner,kb-linter,link-validator,tool-cli}.md
New tools:       src/{backlink_scanner,kb_linter,link_validator,tool_cli}/
New tests:       tests/test_{scanner,linter,validator,cli,kb_linter_cli,link_validator_cli}.py
New CI:          .github/workflows/ci.yml
New playbooks:   playbooks/{iterative-critique,session-logging}.md
Modified specs:  (none — all new)
Modified docs:   docs/{README,format,verification,comprehension}.md
Modified policy: policies/living-specifications.md (+Principle #16)
Config:          pyproject.toml, CHANGELOG.md, README.md
```

### Behavior Map (Level 2)
```
backlink-scanner (specs/backlink-scanner.md):
  §Behavior/Scanning     → scanner.py:_scan_file(), :scan()
  §Behavior/Exit codes   → __main__.py via tool_cli.run_tool()
  §Behavior/spec-section → scanner.py SPEC_SECTION_PATTERN

kb-linter (specs/kb-linter.md):
  §Behavior/Frontmatter  → linter.py:_check_frontmatter()
  §Behavior/Provenance   → linter.py:_check_provenance()
  §Behavior/Exit codes   → __main__.py via tool_cli.run_tool()

link-validator (specs/link-validator.md):
  §Behavior/Link extraction → validator.py:_extract_links()
  §Behavior/Path resolution → validator.py:_resolve_path()
  §Behavior/Exit codes      → __main__.py via tool_cli.run_tool()

tool-cli (specs/tool-cli.md):
  §Behavior/Argument handling → __init__.py:run_tool() argv parsing
  §Behavior/Exit codes        → __init__.py:run_tool() exit logic
```

### Review Strategy
> Read specs first (4 files, ~400 lines total). Then spot-check implementations against behavior statements. Tests are verification — skim for coverage, don't read line-by-line. Config/docs changes are mechanical.

### Session Context
> [notes/2026-01-24-tooling-expansion.md](2026-01-24-tooling-expansion.md) — full narrative including 3 critique cycles, decisions, and observations.

---

**Observation**: Even for 30+ files, the structured description fits in a screen. The reviewer can dive into any level they need. The spec links serve as authoritative documentation of intent.

## AI Agent as PR Author

In our workflow, the AI assistant has full context of:
- Which specs were implemented (it wrote them)
- Which behaviors map to which code (it implemented them)
- What decisions were made and why (it was part of the conversation)
- What the session notes contain (it wrote them)

This means the AI can *generate* structured PR descriptions from its own context. The convention becomes: **ask the AI to write the PR description using the template, referencing the spec and session note.**

The template is a prompt template as much as a documentation template. An agent that follows it produces consistent, reviewer-friendly descriptions regardless of PR size.

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

For larger efforts spanning multiple PRs (like v0.2.0's 8 commits):

### Work stream index

A tracking artifact that shows the overall shape. Can live in:
- A session note (ephemeral, for in-progress work)
- A PR description for the final merge (durable, for review)
- An issue/epic (if using an issue tracker)

Structure:
```markdown
## Work Stream: [Name]

**Goal**: [One sentence]

### PRs (in review order)
1. [Spec: backlink-scanner](#) — behavioral contract for traceability tool
2. [Implement: backlink-scanner](#) — scanner with spec-section support
3. [Spec + Implement: kb-linter](#) — content rule enforcement
4. [Spec + Implement: link-validator](#) — broken link detection
5. [Integration: CI + CLI + vocabulary](#) — enforcement, consolidation, alignment

### Accumulated Decisions
- [Decision and link to spec/session where it was made]

### Current State
[What's done, what's in review, what's next]
```

### PR ordering strategies

| Strategy | When to use | Trade-off |
|----------|-------------|-----------|
| **Spec first, then implement** | New tools/features with clear boundaries | More PRs, but each is independently reviewable |
| **Spec + implement together** | Small tools or tight feedback loops | Fewer PRs, reviewer sees intent and code together |
| **Single large PR** | Trusted team, coherent work session | Fastest for author, needs structured description |
| **Split by concern** | Cross-cutting changes (vocabulary, config) | Logical grouping, but may have ordering dependencies |

### Single large PR (trusted teams)

When the team trusts the author and prefers fewer review contexts:

1. Use the structured template with all 5 levels
2. Add a **Reading Order** section:
   ```markdown
   ## Reading Order
   1. Read specs/ first (intent and behavior contracts)
   2. Skim src/ for structural alignment with specs
   3. Check tests/ for coverage of spec edge cases
   4. Config/docs are mechanical — verify links work
   ```
3. Link the session note for full decision rationale
4. Consider GitHub's "viewed" checkbox feature — mark mechanical files as pre-reviewed

### The trust gradient

Different review depths for different trust levels:

| Trust level | Review approach | PR description needs |
|-------------|----------------|---------------------|
| **High trust** (pair worked, AI-assisted with oversight) | Spec + summary sufficient. Spot-check edge cases. | Level 0 + spec link |
| **Medium trust** (solo work, familiar codebase) | Behavior map review. Verify each spec section covered. | Levels 0-2 |
| **Lower trust** (new contributor, unfamiliar area) | Full diff review with spec as guide. | All levels + reading order |

The structured description scales down gracefully. High-trust reviews use Level 0; lower-trust reviews use all levels. The information is there either way.

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
4. **Structure enables generation** — Structured artifacts (specs, annotations, session notes) enable AI-generated PR descriptions that are consistent and complete.
5. **Trust scales the template down** — High-trust review needs only Level 0 + spec link. All levels exist for when depth is needed.
6. **The reviewer chooses their depth** — The author provides all levels; the reviewer decides how deep to go. Don't force everyone through the same path.

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
