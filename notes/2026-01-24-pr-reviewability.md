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

## Conceptual Foundation

The [progressive disclosure](../docs/comprehension.md) principle applies directly to PR review. A reviewer needs different depths at different moments:

- **Triage**: "Is this relevant to me?" → the title and summary
- **Scoping**: "How big is this?" → the changes line
- **Understanding**: "What does this implement?" → spec links and behavior map
- **Verification**: "Is the approach sound?" → focus line, decisions
- **Context**: "Why this approach?" → session note link

Our structured artifacts already contain this information. Specs hold intent and behavior. Session notes hold rationale and context. Backlink annotations hold the spec-to-code mapping. The PR description is a **computed view** over these artifacts — it points to them rather than restating them.

**The spec as review guide**: For spec-driven changes, the review flow inverts. Instead of "read code → infer intent," it's "read intent → verify code matches." The spec tells the reviewer what the code should do; the diff shows whether it does.

**Session notes as source material**: When creating a PR from a work session, extract from the session note — don't rewrite. The session note's Activities become the summary, Decisions become rationale, Observations become the focus line.

## PR Description Design

### Design principles

1. **Navigation aid with glue text** — Link to specs and notes for depth. Restate key facts inline when it saves the reviewer a click. Brief restatement makes the description self-sufficient for high-trust review.
2. **One screen or less** — If a reviewer has to scroll the description, it's too long. Depth goes in collapsibles or links.
3. **The title does the heavy lifting** — Many reviewers skip the body entirely. The title is the first thing read; the body is for those who need more.
4. **Plain language over structure** — Sentences over bullet lists. Translate spec formality into casual reviewer language.
5. **Focus over completeness** — Tell the reviewer what to pay attention to, not everything that changed.
6. **Generatable** — An AI agent with access to the spec and session note should produce this consistently.

### The title

The title is the single most important line. It should tell a reviewer whether to open the PR at all.

**Principle**: Include enough behavioral detail that the title makes sense without the body. If the body disappeared, would the title alone tell a reviewer what this PR changes?

Good titles (each follows the pattern natural to its type):
- "Add kb-linter: validates frontmatter and provenance against knowledge-base.yaml" (new feature — what it does)
- "Fix link-validator false positives on inline code spans" (bug fix — which bug, specifically)
- "Unify status vocabulary to draft/working/stable/deprecated across all content" (cross-cutting — what changes and to what)
- "Extract shared tool_cli module from 3 identical __main__.py patterns" (refactor — what was extracted and why)

Weak titles (missing behavioral detail):
- "Add kb-linter tool" — what does it do?
- "Fix bug in link-validator" — which bug?
- "Update statuses" — how? why?
- "Refactor CLI code" — what was the refactoring?

### When to use which format

Choose format by **behavioral complexity**, not file count:

| Use this format | When... |
|----------------|---------|
| **Simple** | All choices are obvious from the spec. No non-trivial decisions. |
| **Medium** | A few decisions a reviewer might question. One area of focused complexity. |
| **Large** | Multiple specs, cross-cutting changes, or significant design decisions. |
| **Non-spec** | No spec exists (refactors, config, docs, dependency updates). |

A 3-file PR with a subtle algorithm needs the medium format. A 20-file mechanical rename needs the simple format.

### When to restate vs. link

| Restate inline | Link instead |
|---------------|--------------|
| One-line facts ("exit 1 on dangling refs") | Multi-paragraph explanations |
| Casual translation of formal spec language | The spec's full behavior section |
| Summary across multiple specs (1 line each) | Individual spec details |
| The delta when the spec is changing ("was X, now Y") | Background/history |
| Context for the Focus line | The session note narrative |

**The test**: Does this restatement save the reviewer a click AND fit in one sentence? If yes, restate. If it needs a paragraph, link.

### Linking in PR descriptions

**The problem**: Relative markdown links in GitHub PR descriptions resolve against the default branch, not the PR branch. If this PR adds `specs/kb-linter.md`, a link to it won't work until after merge.

**Solutions** (in order of preference):
1. **Link to the file in the PR**: Use GitHub's file-in-PR URL format — reviewers can see the file in context of the PR's changes. Format: the file will appear in the "Files changed" tab.
2. **Name the file without linking**: "See `specs/kb-linter.md` in this PR" — the reviewer finds it in the file list.
3. **Link to existing files only**: For files that already exist on the default branch (e.g., linking to an existing spec that this PR implements against), relative links work fine.

**Rule of thumb**: Link to existing files. Name new files. The reviewer already has the PR open — they can find new files in the "Files changed" tab.

### Format: simple

```markdown
[What was done and why. One sentence is fine.]

Spec: [name](link) | Verify: `command`
```

Example:

```markdown
Fix link-validator false positives on inline code spans.

Spec: [link-validator](specs/link-validator.md) | Verify: `uv run pytest && uv run link-validator`
```

### Format: medium

```markdown
[What was done and why. 2-3 sentences covering intent and approach.]

Spec: [name](link) | Session: [note](link)
Verify: `command`

**Changes**: [semantic structure — e.g., spec → implementation → tests → config]
**Focus**: [what the reviewer should actually look at]
```

Example:

```markdown
Added kb-linter: validates content files against knowledge-base.yaml rules
(status vocabulary, provenance requirements). Spec-first, 30 tests, found
7 real violations in the repo on first run.

Spec: see `specs/kb-linter.md` in this PR | Session: [tooling-expansion](notes/2026-01-24-tooling-expansion.md)
Verify: `uv run pytest && uv run kb-linter`

**Changes**: spec → implementation → tests → config (pyproject.toml entry point + build)
**Focus**: Frontmatter extraction uses regex not YAML parser — intentional (see spec §Constraints). Review the regex against real frontmatter examples in the repo.
```

### Format: large

```markdown
[What was done and why. 2-3 sentences.]

**Breaking**: [if behavior changes, one sentence on what changes for existing users]

Specs: [a](link), [b](link), [c](link) | Session: [note](link)
Verify: `command`

**Changes**: [semantic structure — e.g., spec → implementation → tests → config]
**Focus**: [where to spend review time vs. what's mechanical]

<details><summary>Behavior map (which spec sections → which code)</summary>

[Spec section — one-line restatement → code location]

</details>

<details><summary>Key decisions</summary>

[Choices that a reviewer might question, with brief rationale]

</details>
```

The `**Breaking**` line appears only when existing behavior changes. Omit it for purely additive PRs.

### Format: non-spec

For refactors, config changes, dependency updates, and docs-only PRs where no spec exists:

```markdown
[What was done and why.]

Verify: `command`

**Focus**: [why this is safe + what the reviewer should check, as a natural sentence]
```

Without a spec as review guide, the Focus line does double duty — it establishes safety AND directs attention. Examples:

- "Pure refactor — behavior identical, all tests pass unchanged. Check that run_tool() handles the same edge cases the original did."
- "Dependency update — changelog reviewed, no API changes in minor bump. Verify lockfile is clean."
- "Docs only — no code changes, just verify links resolve."

### What makes this work

| Element | Purpose | Why it's here |
|---------|---------|---------------|
| Title | Triage — "should I open this?" | The only thing some reviewers read |
| Plain summary | Scope — "is this relevant to me?" | Every reviewer who opens the PR reads this |
| Breaking line | Alert — "does this affect my code?" | Only present when behavior changes |
| Spec links | Deep intent — "what should the code do?" | The review guide for spec-driven changes |
| Session link | Full context — "what was the exploration?" | Available but not required |
| Verify line | Reproducibility — "how do I check this?" | Actionable, copy-pasteable |
| Changes line | Structure — "what's the shape?" | Semantic flow, not file counts |
| Focus line | Guidance — "where should I spend time?" | The author's review recommendation |
| Behavior map | Traceability — "which code implements which spec?" | Collapsible, for thorough reviews |
| Decisions | Rationale — "why this approach?" | Collapsible, for "but why?" questions |

### What's NOT in the description

- **Full file list** — that's what the "Files changed" tab shows
- **Diff explanations** — the code + spec should be self-explanatory
- **Test descriptions** — tests are verification, not documentation
- **Background/motivation** — the session note covers this; link, don't copy
- **Commit-by-commit breakdown** — that's what git log shows

### The "Focus" line

This is the most important non-obvious element. It tells the reviewer: "given limited time, here's what actually matters." Examples:

- "Read the spec. Implementation is straightforward against it."
- "The regex in line 47 handles a tricky edge case — verify it matches the spec's description."
- "Most changes are mechanical renames. The behavioral change is in auth.py:login()."
- "This is a pure refactor — behavior should be identical. Tests prove it."

The Focus line is the author saying "I know your time is valuable, here's where to spend it."

**Limitation**: The Focus line depends on author self-awareness. If the author doesn't realize something is non-obvious, they won't flag it. **Mitigation**: When you can't write a good Focus line, fall back to "Review the behavior map — each spec section should have corresponding correct code." The behavior map provides systematic coverage when the author's intuition about what's tricky is unavailable.

### Updating during review

If the implementation changes after review feedback:

- **Update the summary** if the approach changed (not just the details)
- **Update the Focus line** if the reviewer's feedback revealed a new area of concern
- **Update the behavior map** only if spec sections were added/removed
- **Don't update** for cosmetic fixes, test additions, or minor corrections — the description reflects the PR's intent, not its git log

## Worked Example: v0.2.0 as a Single PR

If the entire v0.2.0 release had been a single PR (8 commits, 30+ files, 3 new tools), here's what the large-format description would look like:

**Title**: "Add structural integrity tools: backlink-scanner, kb-linter, link-validator with CI enforcement"

Using the large-format template:

````markdown
Three structural integrity tools for spec-to-implementation traceability,
content rule enforcement, and broken link detection. All spec-first with
CI enforcement. Unified status vocabulary and consolidated CLI boilerplate.

Specs: see `specs/{backlink-scanner,kb-linter,link-validator,tool-cli}.md` in this PR
Session: [tooling-expansion](notes/2026-01-24-tooling-expansion.md)
Verify: `uv run pytest && uv run ruff check . && uv run backlink-scanner && uv run kb-linter && uv run link-validator`

**Changes**: specs → implementations → tests → CI workflow → playbooks → docs/policy alignment
**Focus**: Read specs first — implementation is mechanical against them. Watch for: inline code span handling in link-validator (edge case caught by dogfooding), regex YAML parsing in kb-linter (intentional, see spec §Constraints).

<details><summary>Behavior map</summary>

backlink-scanner:
- §Scanning — finds `# spec:` annotations in source files → scanner.py:scan()
- §spec-section — tracks section-level granularity → scanner.py SPEC_SECTION_PATTERN

kb-linter:
- §Frontmatter — validates status field against allowed values → linter.py:_check_frontmatter()
- §Provenance — checks for Sources section in docs/policies → linter.py:_check_provenance()

link-validator:
- §Link extraction — pulls markdown links, skips code blocks/inline code → validator.py:_extract_links()
- §Path resolution — resolves relative paths, strips fragments → validator.py:_resolve_path()

tool-cli:
- §Exit codes — 0 clean, 1 failures, 2 config error → __init__.py:run_tool()

</details>

<details><summary>Key decisions</summary>

- Regex over YAML parser for frontmatter: avoids runtime dep, only needs status/sources
- Inline code span stripping: backtick-wrapped links are examples, not navigation
- CLI consolidation at 3 tools: evolution trigger met, shared module justified
- Unified vocabulary (draft/working/stable/deprecated): eliminates parallel lifecycle confusion

</details>
````

**Notes on this example**:
- No `**Breaking**` line because this is purely additive (new tools, no existing behavior changed).
- Spec links say "see X in this PR" because all specs are new files not yet on the default branch.
- 30+ files, but the visible description is 7 lines. Everything else is collapsible.
- A high-trust reviewer reads summary + focus and goes straight to the diff.
- A thorough reviewer expands the behavior map — the one-line restatements tell them what each behavior does without opening the spec.

### Non-spec example: CLI consolidation

**Title**: "Extract shared tool_cli module from 3 identical __main__.py patterns"

```markdown
Three tools had identical CLI boilerplate (arg parsing, JSON output, exit codes).
Extracted to shared tool_cli module. No behavior change — all tools work identically.

Verify: `uv run pytest && uv run backlink-scanner && uv run kb-linter && uv run link-validator`

**Focus**: Pure refactor — all 101 tests pass unchanged, tool outputs identical. Check that run_tool() handles the edge cases each __main__.py previously handled (FileNotFoundError, --report-only flag ordering).
```

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
- **Behavior map generator**: reads spec behavior sections + `spec-section:` annotations → generates the behavior map
- **Review guide generator**: reads changed files + their spec annotations → suggests review order
- **Diff grouping**: group diff hunks by spec section rather than alphabetical file order

### Tooling trade-offs
- Generator tools risk becoming stale if conventions change
- Convention-only approach relies on discipline (but our team is small and trusted)
- A lightweight generator (just the changes line and behavior map) would have high value-to-complexity ratio
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

1. Use the large format with behavior map and key decisions
2. The Focus line should include a reading order: "Read specs first, then spot-check implementation. Tests are verification, config is mechanical."
3. Link the session note for full decision rationale
4. Use GitHub's "viewed" checkbox — mark mechanical files (config, docs) as pre-reviewed

### The trust gradient

Different review depths for different trust levels:

| Trust level | Review approach | What they read in the PR description |
|-------------|----------------|--------------------------------------|
| **High trust** (pair worked, AI-assisted with oversight) | Spec + summary sufficient. Spot-check edge cases. | Title + summary + focus |
| **Medium trust** (solo work, familiar codebase) | Behavior map review. Verify each spec section covered. | Summary + focus + behavior map |
| **Lower trust** (new contributor, unfamiliar area) | Full diff review with spec as guide. | Everything including decisions |

The format scales gracefully. All the information is there; the reviewer decides how deep to go.

## Open Questions

- **Should behavior maps be generated or hand-written?** Generated is more accurate but requires tooling. Hand-written is simpler but risks going stale. Could the backlink scanner output be reformatted into a behavior map automatically?
- **How do we handle PRs that modify specs?** The spec is both the change and the review guide — circular reference. Possible answer: the *diff* of the spec IS the intent description; the reviewer reads the spec diff first, then verifies code matches the new spec.
- **Can review comments reference spec sections?** "This doesn't match §Behavior/Login" is more precise than "this seems wrong." Would this convention be adopted naturally?
- **How do we handle PRs from people who didn't write the spec?** The Focus line depends on author knowledge. Can the spec itself provide enough guidance for any author? (Mitigation: the behavior map provides systematic review regardless of author familiarity.)
- **What's the threshold for behavior map inclusion?** The format says "large format" includes it, but is it worth maintaining for medium-complexity PRs too?

## Validation Plan

This design is currently theoretical — no actual reviewer has used it to review a PR. To validate:

1. **Use it on the next real PR** — write the description using this format, then ask: was it faster to write than ad hoc? Did it feel natural?
2. **Get reviewer feedback** — after the PR is reviewed, ask: did the Focus line help? Did you expand the behavior map? What was missing?
3. **Compare with ad hoc** — for the same work, compare time-to-understand between a structured description and an unstructured one.
4. **Test generability** — ask an AI agent to generate the description from a spec + session note without seeing the template. Does it converge on something similar?

Success criteria:
- Author can write the description in under 5 minutes (or the AI generates it)
- Reviewer can triage (approve/review/defer) from the visible portion without scrolling
- Thorough reviewer finds the behavior map useful (clicks or expands it)
- No reviewer asks "but what does this do?" after reading the description

## Emerging Principles

1. **Specs are review guides** — Read the spec before reading the code. The spec tells you what to verify.
2. **Progressive disclosure in PRs** — Summary for triage, changes line for scoping, behavior map for verification.
3. **Restate to save clicks, link for depth** — One-line facts belong inline. Multi-paragraph context belongs behind a link. The test: does it fit in one sentence AND save a context switch?
4. **Structure enables generation** — Structured artifacts (specs, annotations, session notes) enable AI-generated PR descriptions that are consistent and complete.
5. **Trust scales the template down** — High-trust review needs only summary + spec link. All levels exist for when depth is needed.
6. **The reviewer chooses their depth** — The author provides all levels; the reviewer decides how deep to go. Don't force everyone through the same path.
7. **The description should be self-sufficient for triage** — A reviewer should be able to decide "approve / review deeper / not my area" without clicking any links. Restatement makes this possible.

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
