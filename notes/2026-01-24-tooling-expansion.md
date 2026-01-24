---
status: working
---

# Tooling Expansion and Practices Maturation

Date: 2026-01-24 (second session)

## Context

Following the [tooling cleanup session](2026-01-24-tooling-cleanup.md), expanded the tool suite and matured the practices framework. Identified automation needs from the knowledge-base rules, built new tools spec-first, and validated all playbooks through use.

## Activities

### KB Linter (spec → implement → validate)

- Identified need: `knowledge-base.yaml` declares rules (statuses, provenance) but nothing enforces them
- Followed the writing-specs playbook step-by-step to write `specs/kb-linter.md`
- Implemented `src/kb_linter/` — reads rules from config, validates content files
- The linter found 7 real violations in the repo (missing frontmatter/Sources sections)
- Noted 5 friction points in the playbook, applied improvements

### Playbook Improvements

- Added Step 0: Orient (gather context before writing)
- Added Step 7: Record Decisions (capture rationale inline)
- Added iterative-writing note (steps are a thinking guide, not strict sequence)
- Added Step 9: Verify Against Implementation (catches drift at creation time)
- Promoted writing-specs to `status: working` with validation evidence

### Link Validator (spec → implement → validate)

- Identified from kb-linter's Non-goals: "Markdown link validation (separate concern, future tool)"
- Followed improved playbook; Step 9 caught zero drift (immediate payoff)
- Caught inline code span false positives during dogfooding → updated spec + code
- Fixed 1 real broken link in the repo

### Self-Critique Cycle

After each tool was built, critiqued the work:
- **KB linter critique**: Found 3 spec-implementation drift items (output grouping, parse error description, symlink behavior). Fixed by correcting the spec to match intended behavior.
- **Link validator critique**: Found stale example numbers, dead parameter. Fixed immediately.
- Process observation: drift was introduced at spec-creation time → led to Step 9.

### Status Vocabulary Alignment

- Discovered parallel lifecycles: specs used proposed/accepted/implemented while KB used draft/working/stable/deprecated
- Decision: unify on draft/working/stable/deprecated everywhere
- Updated: format.md template, Principle #4, both remaining playbooks, all spec frontmatter

### CI and CLI Consolidation

- Added `.github/workflows/ci.yml` — tests + ruff + format + all 3 tools
- Extracted `src/tool_cli/` shared runner from 3 identical __main__.py patterns
- Coverage improved from 82% to 90% with the consolidation

### Playbook Validation

- **reviewing-against-specs**: Validated by reviewing link-validator against its spec. Works well; added Sources.
- **ensemble-with-specs**: AI Agent Handoff pattern validated by this session's workflow. Mob-specific patterns (Navigator-as-Scribe) noted as theoretical. Added Sources.
- Both promoted to `status: working`

## Decisions Made

- KB linter reads from `knowledge-base.yaml` rather than hardcoding (adaptable, avoids drift)
- Notes excluded from KB linting (ephemeral, enforcing structure contradicts their purpose)
- Link validator scans all content dirs including notes/specs (link rot affects navigability everywhere)
- Skip links in code blocks AND inline code spans (both are illustrative, not navigational)
- Unified status vocabulary across all content types (one lifecycle, not two)
- CI runs enforcement tools (Principle #2: source-of-truth requires mechanism)
- CLI consolidation warranted at 3 tools (evolution trigger from architecture decision met)

## Metrics

- **Tests**: 101 passing (from 30 at session start)
- **Coverage**: 90% (from ~80%)
- **Tools**: 3 (backlink-scanner, kb-linter, link-validator)
- **Playbooks**: 3 validated and working (from 1 working + 2 draft)
- **Specs**: 3 at working status (from 1 at proposed)
- **Version**: v0.2.0 tagged

## Observations

1. **Spec-first development works** — writing the spec first forced clear thinking about behavior. Both tools had specs validated at Step 9 with zero or minimal drift.

2. **Self-critique is productive** — each critique cycle caught real issues (drift items, dead parameters, stale examples, vocabulary clashes). The cost is modest; the payoff is immediate.

3. **Dogfooding catches what tests miss** — running tools against their own repo exposed false positives (inline code spans) that synthetic test cases wouldn't reveal.

4. **Playbook improvement through use** — the writing-specs playbook gained 4 new steps from a single real usage. Theory → practice → refinement loop works.

5. **The tooling architecture decision's triggers are being met** — "Multiple CLI commands" triggered CLI consolidation. The flat structure is still appropriate for individual tools, but shared patterns now have a shared module.

### Post-v0.2.0 Cleanup

After cutting the release, another critique cycle identified:
- README was stale (only mentioned backlink-scanner, missing tool table)
- CHANGELOG was incomplete (missing CI, tool_cli, playbook entries)
- Coverage config missing `--cov=tool_cli`
- CI had unpinned uv version

All fixed. Then expanded practices documentation:
- Added Principle #16 to living-specifications: "Dogfood the practices"
- Created [AI-Assisted Workflow](2026-01-24-ai-assisted-workflow.md) exploration note capturing patterns from this session
