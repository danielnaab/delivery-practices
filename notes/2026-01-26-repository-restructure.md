---
status: working
---

# Repository Restructure

Date: 2026-01-26

## Context

Reorganized repository from knowledge-type organization (docs/policies/playbooks/) to topic-first organization with practice areas under docs/. The previous structure separated content by type (declarative/normative/procedural), but practice areas span these types. The new structure groups all material for a practice area together.

## Activities

### Structure Changes

Old:
```
docs/         → declarative reference
policies/     → normative principles
playbooks/    → procedural guides
```

New:
```
docs/
├── living-specifications/    → all spec-driven content
│   ├── format.md, relationships.md, verification.md, comprehension.md
│   ├── principles.md
│   └── guides/writing-specs.md, ensemble-with-specs.md, reviewing-against-specs.md
├── workflow/                 → all workflow content
│   └── guides/iterative-critique.md, session-logging.md, pr-descriptions.md
└── decisions/                → cross-cutting ADRs
```

### File Moves

| From | To |
|------|-----|
| docs/*.md | docs/living-specifications/*.md |
| policies/living-specifications.md | docs/living-specifications/principles.md |
| playbooks/writing-specs.md | docs/living-specifications/guides/writing-specs.md |
| playbooks/ensemble-with-specs.md | docs/living-specifications/guides/ensemble-with-specs.md |
| playbooks/reviewing-against-specs.md | docs/living-specifications/guides/reviewing-against-specs.md |
| playbooks/iterative-critique.md | docs/workflow/guides/iterative-critique.md |
| playbooks/session-logging.md | docs/workflow/guides/session-logging.md |
| playbooks/pr-descriptions.md | docs/workflow/guides/pr-descriptions.md |

### Configuration Updates

- `knowledge-base.yaml`: Removed policies and playbooks paths; simplified to docs and notes
- `CLAUDE.md`: Updated content organization section, write boundaries, current state
- Root `README.md`: Updated structure section

### Link Updates

Updated ~100+ internal links across 29 files. Key patterns:
- `../policies/living-specifications.md` → `../principles.md` (within living-specifications/)
- `../playbooks/*.md` → `guides/*.md` or `../workflow/guides/*.md` (depending on context)
- `../notes/` → `../../notes/` (files moved one level deeper)

### Spec Updates

Updated specs with new examples:
- `kb-linter.md`: Content directories, canonical paths, example output
- `link-validator.md`: Example paths in gherkin scenarios

## Decisions Made

1. **Topic-first over type-first**: Practice areas are the primary axis; knowledge types are secondary. This matches how people think about the content ("I want to learn about specs" not "I want some procedural docs").

2. **guides/ not playbooks/**: Within a practice area, procedural content lives in `guides/` (shorter, less formal).

3. **CHANGELOG historical**: Did not update historical CHANGELOG entries — they accurately describe what was added at that time.

4. **Graduated notes unchanged**: Historical ASCII diagrams in exploration notes are historical artifacts, not navigation.

## Observations

1. **Link depth increases complexity**: Moving files deeper requires updating all relative paths. The link-validator was essential for catching these.

2. **Spec examples drift**: Gherkin examples in specs referenced non-existent paths after the move. Spec examples are assertions about behavior — they need updating when structure changes.

3. **Display text vs. target**: Some markdown links had old paths in display text but correct targets. Confusing for readers.

## What's Next

- Monitor for workflow principles that might warrant `docs/workflow/principles.md`
- Consider whether decisions/ should be per-practice-area or remain cross-cutting
