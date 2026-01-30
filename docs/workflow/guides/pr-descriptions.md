---
status: working
last-validated: 2026-01-26
---

# Writing PR Descriptions

How to write PR descriptions that help trusted reviewers navigate spec-driven changes efficiently.

> **Context**: Spec-driven development produces large, coherent changesets. The structure is already in specs, session notes, and backlink annotations — the PR description surfaces it for reviewers rather than restating it.

## Core Idea

The spec is the review guide. Instead of "read code → infer intent," the reviewer's flow is "read intent → verify code matches." The PR description connects these layers with minimal ceremony.

## When to Write

Write the description after the code is done. If you kept a session note, extract from it rather than rewriting:

- **Activities** section → the summary
- **Decisions** section → key decisions or Focus line rationale
- **Observations** section → Focus line ("here's what's tricky")

See [session logging](session-logging.md#for-pr-descriptions) for details.

## Choose a Format

Choose by **behavioral complexity**, not file count:

| Use this format | When... |
|----------------|---------|
| **Simple** | All choices are obvious from the spec. No non-trivial decisions. |
| **Medium** | A few decisions a reviewer might question. One area of focused complexity. |
| **Large** | Multiple specs, cross-cutting changes, or significant design decisions. |
| **Non-spec** | No spec exists (refactors, config, docs, dependency updates). |

A 3-file PR with a subtle algorithm needs the medium format. A 20-file mechanical rename needs the simple format.

## The Title

The title is the single most important line. It should tell a reviewer whether to open the PR at all.

**Principle**: Include enough behavioral detail that the title makes sense without the body.

Good titles:
- "Add kb-linter: validates frontmatter and provenance against knowledge-base.yaml" (new feature — what it does)
- "Fix link-validator false positives on inline code spans" (bug fix — which bug)
- "Unify status vocabulary to draft/working/stable/deprecated across all content" (cross-cutting — what changes)
- "Extract shared tool_cli module from 3 identical __main__.py patterns" (refactor — what and why)

Weak titles:
- "Add kb-linter tool" — what does it do?
- "Fix bug in link-validator" — which bug?
- "Update statuses" — how? why?

## Format: Simple

```markdown
[What was done and why. One sentence is fine.]

Spec: [name](link) | Verify: `command`
```

## Format: Medium

```markdown
[What was done and why. 2-3 sentences covering intent and approach.]

Spec: [name](link) | Session: [note](link)
Verify: `command`

**Changes**: [semantic structure — e.g., spec → implementation → tests → config]
**Focus**: [what the reviewer should actually look at]
```

## Format: Large

```markdown
[What was done and why. 2-3 sentences.]

**Breaking**: [if behavior changes, one sentence on what changes for existing users]

Specs: [a](link), [b](link) | Session: [note](link)
Verify: `command`

**Changes**: [semantic structure]
**Focus**: [where to spend review time vs. what's mechanical]

<details><summary>Behavior map (which spec sections → which code)</summary>

§Scanning — finds spec: annotations in source → scanner.py:scan()
§Exit codes — 0 clean, 1 failures, 2 config error → __init__.py:run_tool()

</details>

<details><summary>Key decisions</summary>

- Regex over YAML parser for frontmatter: avoids runtime dep, only needs status/sources
- Inline code span stripping: backtick-wrapped links are examples, not navigation

</details>
```

The `**Breaking**` line appears only when existing behavior changes. Omit for additive PRs.

## Format: Non-spec

For refactors, config changes, dependency updates, and docs-only PRs:

```markdown
[What was done and why.]

Verify: `command`

**Focus**: [why this is safe + what the reviewer should check, as a natural sentence]
```

Without a spec as review guide, the Focus line does double duty — it establishes safety AND directs attention:

- "Pure refactor — behavior identical, all tests pass unchanged. Check that run_tool() handles the same edge cases."
- "Dependency update — changelog reviewed, no API changes in minor bump. Verify lockfile is clean."
- "Docs only — no code changes, just verify links resolve."

## Element Reference

| Element | Purpose |
|---------|---------|
| Title | Triage — "should I open this?" |
| Summary | Scope — "is this relevant to me?" |
| Breaking line | Alert — "does this affect my code?" |
| Spec links | Intent — "what should the code do?" |
| Session link | Context — "what was the exploration?" |
| Verify line | Reproducibility — "how do I check this?" |
| Changes line | Structure — semantic flow, not file counts |
| Focus line | Guidance — the author's review recommendation |
| Behavior map | Traceability — which code implements which spec |
| Decisions | Rationale — "why this approach?" |

## Writing the Focus Line

The Focus line tells the reviewer: "given limited time, here's what actually matters."

- "Read the spec. Implementation is straightforward against it."
- "The regex in line 47 handles a tricky edge case — verify it matches the spec's description."
- "Most changes are mechanical renames. The behavioral change is in auth.py:login()."
- "New tool, spec-first — spec defines all behaviors, implementation follows it directly."

**When you can't identify what's tricky**: Fall back to "Review the behavior map — each spec section should have corresponding correct code." The behavior map provides systematic coverage when author intuition is unavailable.

## When to Restate vs. Link

| Restate inline | Link instead |
|---------------|--------------|
| One-line facts ("exit 1 on dangling refs") | Multi-paragraph explanations |
| Casual translation of formal spec language | The spec's full behavior section |
| Summary across multiple specs (1 line each) | Individual spec details |
| The delta ("was X, now Y") | Background/history |
| Context for the Focus line | The session note narrative |

**The test**: Does this restatement save the reviewer a click AND fit in one sentence? If yes, restate.

## Linking

**The problem**: Relative markdown links in GitHub PR descriptions resolve against the default branch, not the PR branch.

**Rule of thumb**: Link to existing files. Name new files. The reviewer can find new files in the "Files changed" tab.

- Existing files: link normally (relative links work)
- New files in this PR: "See `specs/kb-linter.md` in this PR"

## Updating During Review

If the implementation changes after feedback:

- **Update the summary** if the approach changed (not just details)
- **Update the Focus line** if feedback revealed a new area of concern
- **Update the behavior map** only if spec sections were added/removed
- **Don't update** for cosmetic fixes, test additions, or minor corrections — the description reflects intent, not git log

## Worked Example

**Title**: "Extract shared tool_cli module from 3 identical __main__.py patterns"

```markdown
Three tools had identical CLI boilerplate (arg parsing, JSON output, exit codes).
Extracted to shared tool_cli module. No behavior change — all tools work identically.

Verify: `uv run pytest && uv run backlink-scanner && uv run kb-linter && uv run link-validator`

**Focus**: Pure refactor — all 101 tests pass unchanged, tool outputs identical. Check that
run_tool() handles the edge cases each __main__.py previously handled (FileNotFoundError,
--report-only flag ordering).
```

This uses the non-spec format: no spec existed for the refactoring itself. The Focus line establishes safety ("pure refactor, tests pass") and directs attention ("check edge case handling").

## Multi-PR Work Streams

For larger efforts spanning multiple PRs, see the [PR Reviewability exploration](../../../notes/2026-01-24-pr-reviewability.md#multi-pr-work-streams) for work stream index patterns, ordering strategies, and trust gradient guidance. This content hasn't been validated on real work streams yet.

## What's NOT in the Description

- **Full file list** — that's what "Files changed" shows
- **Diff explanations** — code + spec should be self-explanatory
- **Test descriptions** — tests are verification, not documentation
- **Background/motivation** — session note covers this; link, don't copy
- **Commit-by-commit breakdown** — that's what git log shows

## Related

- [Session logging](session-logging.md) — session notes as PR source material
- [Reviewing against specs](../../living-specifications/guides/reviewing-against-specs.md) — the reviewer's perspective
- [Iterative critique](iterative-critique.md) — build-critique-fix produces session material

## Sources

- [PR Reviewability exploration](../../../notes/2026-01-24-pr-reviewability.md) — full design rationale and worked examples
- Direct observation: Authoring descriptions for delivery-practices v0.2.0 changes
- [Comprehension UX principles](../../living-specifications/comprehension.md) — progressive disclosure applied to review
