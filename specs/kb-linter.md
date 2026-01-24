---
status: proposed
last-verified: 2026-01-24
owners: [daniel]
---

# KB Linter

## Intent

Enforce the content rules declared in [`knowledge-base.yaml`](../knowledge-base.yaml) — validating that content files have proper frontmatter status fields and provenance (Sources sections) where required.

This gives [Principle #2](../policies/living-specifications.md) ("source-of-truth requires enforcement") its mechanical backing: rules declared in configuration are checked by tooling, not just convention.

## Non-goals

- Prose quality or completeness checking
- Write boundary enforcement (agent entrypoint handles this)
- Markdown link validation (separate concern, future tool)
- Spec-to-implementation traceability (handled by [backlink scanner](backlink-scanner.md))
- Semantic analysis of whether content qualifies as "practice-recommendations" vs. other types

## Behavior

### Configuration

- Given a `knowledge-base.yaml` file in the root directory
- When the linter starts
- Then it reads `rules.lifecycle.statuses` for valid status values
- And it reads `sources.canonical` paths for provenance-required directories

### Frontmatter validation

- Given a markdown file in a content directory (docs/, policies/, playbooks/)
- When the file has no YAML frontmatter
- Then it reports a "missing frontmatter" violation

- Given a markdown file with frontmatter
- When the frontmatter has no `status` field
- Then it reports a "missing status" violation

- Given a frontmatter `status` field
- When the value is not in `rules.lifecycle.statuses`
- Then it reports an "invalid status" violation with the invalid value and allowed values

- Given a frontmatter with a valid `status` field
- When the status value is in the allowed set
- Then no violation is reported for that file's frontmatter

### Provenance validation

- Given a file in a path matching `sources.canonical` entries (docs/**, policies/**)
- When the file does not contain a `## Sources` heading
- Then it reports a "missing provenance" violation

- Given a file in a canonical path with a `## Sources` heading
- When the section exists (regardless of content)
- Then no provenance violation is reported

- Given a file in a non-canonical path (playbooks/, notes/)
- When the file lacks a Sources section
- Then no provenance violation is reported (provenance is optional for these paths)

### Scanned paths

- Content directories: docs/, policies/, playbooks/
- Only `.md` files are checked
- README.md files are included (they carry status and may need provenance)
- Files in subdirectories are included recursively
- Skips: .git/, .graft/, .venv/, node_modules/, __pycache__/
- Does not scan: specs/, src/, tests/, notes/ (specs have their own lifecycle; code and tests don't need frontmatter; notes are ephemeral)

### Output structure

- Given completed linting
- When results are reported
- Then output is a JSON object with violations grouped by file

Example output:
```json
{
  "violations": [
    {
      "file": "docs/example.md",
      "rule": "missing-status",
      "message": "No status field in frontmatter"
    },
    {
      "file": "policies/example.md",
      "rule": "missing-provenance",
      "message": "No Sources section found (required for canonical content)"
    }
  ],
  "summary": {
    "files_checked": 12,
    "files_passing": 10,
    "violations": 2
  }
}
```

### Exit codes

- **Exit 0**: no violations found
- **Exit 1**: one or more violations found
- **`--report-only` flag**: always exit 0

### Edge cases

- Files with empty frontmatter (`---\n---`): reports "missing status"
- Files with frontmatter but non-YAML content: reports parse error
- Binary files: skipped
- Symlinks: not followed
- knowledge-base.yaml missing: exit with error message (not a violation, a misconfiguration)

## Constraints

- Runs in Python (no runtime dependencies beyond standard library)
- Reads configuration from `knowledge-base.yaml` (not hardcoded)
- Completes in under 1 second for knowledge bases up to 1,000 content files

## Open Questions

- [ ] Should notes/ files be checked for frontmatter status? (Currently excluded as ephemeral, but they do use status fields)
- [ ] Should the linter support a `# kb-lint: ignore` annotation for intentional exceptions?

## Decisions

- 2026-01-24: Read rules from knowledge-base.yaml rather than hardcoding. Keeps the tool adaptable to different KBs and avoids drift between declared rules and enforcement.
- 2026-01-24: Provenance checking uses `sources.canonical` paths to determine which files need Sources sections. This is more precise than checking all files (notes are ephemeral, playbooks link to sources in docs/).
- 2026-01-24: Notes excluded from linting. They're ephemeral explorations — enforcing structure on them contradicts their purpose.

## Sources

- [`knowledge-base.yaml`](../knowledge-base.yaml) — the rules being enforced
- [Living Specifications Principles](../policies/living-specifications.md) — #2 (enforcement), #14 (fight tribal knowledge)
- [Specification Format](../docs/format.md) — "Status is non-negotiable"
- [Backlink Scanner](backlink-scanner.md) — sibling tool, structural patterns to follow
