---
status: working
last-verified: 2026-01-25
owners: [daniel]
---

# PR Description Generator

## Intent

Generate PR descriptions from structured YAML input, following the formats defined in [pr-descriptions.md](../docs/workflow/guides/pr-descriptions.md). Unlike validator tools (which output JSON with pass/fail semantics), this is a generator that outputs markdown text.

This supports the spec-driven workflow: session notes and structured input become formatted PR descriptions with consistent structure.

## Non-goals

- Validating YAML schema beyond required fields for each format
- Generating PR titles (input provides summary, title is separate)
- Extracting content from session notes or specs (input is pre-extracted)
- Interactive editing or prompting

## Behavior

### Input format

```gherkin
Given a YAML file path as input
When the generator runs
Then it reads and parses the YAML content
```

Required fields vary by format. See Format Requirements below.

Example YAML input:
```yaml
format: medium
summary: |
  What was done and why. 2-3 sentences for medium/large.
verify: "uv run pytest && uv run kb-linter"

specs:
  - specs/kb-linter.md
sessions:
  - notes/2026-01-24-tooling-expansion.md
changes: "spec → implementation → tests → config"
focus: "Frontmatter extraction uses regex not YAML parser — intentional."

# Large format only (optional)
breaking: "Exit codes changed from 0 to 1 on failures"
decisions:
  - "Regex over YAML parser: avoids runtime dep"
behavior_map_source: .backlink-output.json

root_dir: "."

# Optional GitHub configuration for rich links
github:
  owner: anthropic
  repo: delivery-practices
  branch: main
  pr_number: 42  # optional
```

### Format requirements

| Format   | Required fields                                         | Optional fields                           |
|----------|--------------------------------------------------------|-------------------------------------------|
| simple   | summary, verify, specs (1+)                            | root_dir, github                          |
| medium   | summary, verify, specs (1+), sessions (1+), changes, focus | root_dir, github                     |
| large    | summary, verify, specs (1+), sessions (1+), changes, focus | breaking, decisions, behavior_map_source, root_dir, github |
| non-spec | summary, verify, focus                                 | root_dir, github                          |

### Validation

```gherkin
Given an input YAML file
When a required field for the specified format is missing
Then the generator exits with code 2 and an error message to stderr
```

```gherkin
Given an input YAML file
When the format field is missing or invalid
Then the generator exits with code 2 and an error message to stderr
```

```gherkin
Given an input YAML file with a github field
When github is present but missing owner, repo, or branch
Then the generator exits with code 2 and an error message listing missing fields
```

```gherkin
Given an input YAML file with a github field
When github.pr_number is not provided
Then the generator proceeds normally (pr_number is optional)
```

### Link formatting

```gherkin
Given a file path in specs or sessions
  And root_dir is specified
  And the file exists at {root_dir}/{path}
When formatting the output
Then format as markdown link: [filename](path)
```

```gherkin
Given a file path in specs or sessions
  And the file does not exist at {root_dir}/{path}
When formatting the output
Then format as: See `path` in this PR
```

```gherkin
Given a single spec or session file
When formatting the output
Then use singular label: Spec: or Session:
```

```gherkin
Given multiple spec or session files
When formatting the output
Then use plural label: Specs: or Sessions: (comma-separated)
```

### Link adapters

The generator supports pluggable link adapters for platform-specific URL formatting. This enables rich links when generating PR descriptions for specific platforms.

```gherkin
Given no link adapter is specified
When generating output
Then use PlainLinkAdapter with relative markdown links
```

```gherkin
Given a GitHubLinkAdapter with owner, repo, and branch
  And a file exists in the repository
When formatting a file link
Then generate a GitHub blob URL: https://github.com/owner/repo/blob/branch/path
```

```gherkin
Given a GitHubLinkAdapter with pr_number configured
  And a file does not exist (new in this PR)
When formatting a file link
Then generate a PR diff URL with SHA256 anchor: https://github.com/owner/repo/pull/N/files#diff-<hash>
```

```gherkin
Given a GitHubLinkAdapter without pr_number configured
  And a file does not exist
When formatting a file link
Then fall back to: See `path` in this PR
```

The LinkAdapter protocol defines the interface:
- `format_file_link(path, display_name, exists)` — format link to a file
- `format_diff_anchor(path)` — format URL anchor for PR diff view
- `format_pr_files_url()` — format URL to PR files changed view
- `supports_pr_links()` — check if PR-specific links are available
- `check_file_exists(path)` — check if file exists in repository

### Output: simple format

```markdown
[summary]

Spec: [name](link) | Verify: `[verify]`
```

### Output: medium format

```markdown
[summary]

Spec: [name](link) | Session: [note](link)
Verify: `[verify]`

**Changes**: [changes]
**Focus**: [focus]
```

### Output: large format

```markdown
[summary]

**Breaking**: [breaking]

Specs: [a](link), [b](link) | Sessions: [note](link)
Verify: `[verify]`

**Changes**: [changes]
**Focus**: [focus]

<details><summary>Behavior map (which spec sections → which code)</summary>

[behavior map entries]

</details>

<details><summary>Key decisions</summary>

[decisions as bullet list]

</details>
```

The **Breaking** line is omitted if `breaking` field is not provided.
The behavior map section is omitted if `behavior_map_source` is not provided.
The decisions section is omitted if `decisions` field is not provided or empty.

### Output: non-spec format

```markdown
[summary]

Verify: `[verify]`

**Focus**: [focus]
```

### Behavior map generation

```gherkin
Given a behavior_map_source path pointing to a backlink scanner JSON file
  And the file exists and contains spec section data
When generating the behavior map
Then extract section-to-file mappings only for specs listed in the input specs field
```

```gherkin
Given section data like {"specs": {"specs/foo.md": {"sections": {"Behavior/Login": ["src/auth.py"]}}}}
  And specs/foo.md is in the input specs list
When generating the behavior map
Then output: §Behavior/Login → src/auth.py
```

```gherkin
Given multiple files implementing a section
When generating the behavior map
Then output: §Behavior/Login → src/auth.py, src/login.py
```

```gherkin
Given the behavior_map_source file does not exist
When generating large format
Then omit the behavior map section entirely (no error)
```

```gherkin
Given specs in the backlink JSON that are not in the input specs list
When generating the behavior map
Then those specs' sections are excluded from the output
```

### Exit codes

- **Exit 0**: Success (markdown output to stdout)
- **Exit 2**: Error (missing file, invalid YAML, missing required fields)

There is no exit code 1 — this is a generator, not a validator. Either it produces output or it has a configuration error.

### Edge cases

- Empty summary: outputs empty line (valid but odd)
- Summary with multiple lines: preserved as-is
- YAML parse errors: exit 2 with error message
- Input file not found: exit 2 with error message
- root_dir not specified: defaults to "."
- Trailing newlines: output ends with exactly one newline

## Constraints

- Runs in Python
- Requires PyYAML for YAML parsing (complex nested structure)
- Outputs to stdout; errors to stderr
- No JSON output mode (this is markdown-native)

## Open Questions

None currently.

## Decisions

- Standalone CLI, not using tool_cli.run_tool(): generator outputs markdown not JSON; no pass/fail semantics that tool_cli expects
- YAML input file: complex input structure is unwieldy as CLI flags; YAML is AI-generatable
- PyYAML dependency: proper parsing warranted for nested input structure
- v1 behavior maps use `§Section → file.py` format without restatements — simpler to implement and read
- behavior_map_source accepts backlink scanner JSON directly, filtered to input specs — no transformation step needed
- Protocol-based link adapters: enables platform-specific URL generation (GitHub blob links, PR diff anchors) while maintaining testability via fakes
- GitHubLinkAdapter uses SHA256 hash of file path for diff anchors: matches GitHub's own anchor format

## Sources

- [PR Descriptions Playbook](../docs/workflow/guides/pr-descriptions.md) — format definitions and examples
- [Backlink Scanner](backlink-scanner.md) — behavior_map_source JSON format
