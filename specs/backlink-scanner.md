---
status: proposed
last-verified: 2026-01-24
owners: [daniel]
---

# Backlink Scanner

## Intent

Enable spec-to-implementation traceability by scanning source files for backlink annotations (`// spec:` or `# spec:`) and producing a structured report of which files reference which specs.

This supports the living specifications practice: references flow upstream (code points to specs), and views are computed from those references.

## Non-goals

- Semantic analysis of whether implementations match spec intent
- Modifying source files or specs
- Blocking CI pipelines (output is informational)
- Watching for file changes (runs on demand)

## Behavior

### Scanning for backlinks

- Given a directory path
- When the scanner runs
- Then it finds all files containing backlink annotations matching `// spec:` or `# spec:` followed by a path

### Annotation format

Annotations must be standalone lines (the annotation is the entire line content, ignoring leading/trailing whitespace).

- Given a line `// spec: specs/backlink-scanner.md`
- When the scanner parses it
- Then it records that file as an implementor of `specs/backlink-scanner.md`

- Given a line `# spec: specs/backlink-scanner.md`
- When the scanner parses it
- Then it records that file as an implementor of `specs/backlink-scanner.md`

- Given a line containing an annotation embedded in other content (e.g. inside a string literal)
- When the scanner parses it
- Then it does not match

- Given a line `// spec-section: Behavior/Scanning for backlinks`
- When the scanner parses it
- Then it records the section reference alongside the spec reference

### Output structure

- Given completed scanning
- When results are reported
- Then output is a JSON object mapping spec paths to arrays of implementor file paths

Example output:
```json
{
  "specs": {
    "specs/backlink-scanner.md": {
      "implementors": [
        "src/backlink-scanner.ts",
        "tests/backlink-scanner.test.ts"
      ]
    }
  }
}
```

### Dangling references

- Given a backlink annotation referencing `specs/nonexistent.md`
- When the referenced spec file does not exist
- Then the scanner includes it in a `dangling` array in the output

### Orphan specs

- Given spec files exist in the specs directory
- When no source files reference a given spec
- Then the scanner includes that spec path in an `orphans` array in the output

### Edge cases

- Binary files: skipped
- Markdown code fences: annotations inside ``` blocks are skipped
- Standalone lines only: annotations embedded in other content (string literals, inline code) are ignored
- Multiple annotations in one file: all recorded
- Self-referencing specs: allowed (a spec can reference another spec)

## Constraints

- Runs in Node.js (TypeScript)
- No external dependencies beyond Node standard library
- Completes in under 1 second for repositories up to 10,000 files
- Exit code 0 on success regardless of findings (dangling/orphans are informational)

## Open Questions

- [ ] Should the scanner support configurable annotation patterns beyond `// spec:` and `# spec:`?
- [ ] Should output include line numbers for each annotation?

## Decisions

- 2026-01-24: Use JSON output for machine readability. Human-readable summaries can be built on top.
- 2026-01-24: No external dependencies. Keeps the tool simple and the repo self-contained.
- 2026-01-24: Informational only (exit 0). Blocking behavior belongs in CI configuration, not the tool.

## Sources

- [Verification and Drift Detection](../docs/verification.md) - backlink annotation patterns
- [Artifact Relationships](../docs/relationships.md) - three-layer model, upstream references
- Personal experience: backlink-based navigation in knowledge bases
