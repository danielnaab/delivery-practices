---
status: working
---

# PR Description Generator Implementation

Date: 2026-01-25

## Context

Implemented the PR description generator tool based on a detailed plan. The tool generates markdown PR descriptions from structured YAML input, following the formats defined in `docs/workflow/guides/pr-descriptions.md`. Unlike the validator tools (which output JSON with pass/fail), this is a generator that outputs markdown text.

## Activities

### Initial Implementation

- Created spec: `specs/pr-description-generator.md`
- Added PyYAML dependency to pyproject.toml
- Implemented `src/pr_description_generator/`:
  - `models.py`: Format enum, PRInput dataclass, BehaviorMapEntry
  - `generator.py`: parse_input, validate_for_format, format_link, load_behavior_map, generate_*
  - `__main__.py`: standalone CLI (not using tool_cli — outputs markdown, not JSON)
- Wrote 51 unit tests and 15 CLI integration tests
- Updated pyproject.toml with entry point, package, coverage config
- Updated README with new tool documentation

### First Critique Cycle

Reviewed implementation and found several issues:

1. **Bug**: `format_links` return type annotation was `tuple[str, str]` but actually returned `str`
2. **Bug**: `load_behavior_map` extracted ALL sections from backlink JSON, not just specs in input
3. **Missing test**: No coverage for YAML that parses to non-dict (string or list)
4. **Documentation**: Spec status was `draft`, should be `working` with `last-verified`
5. **Documentation**: README not updated with new tool

All fixed. Added `filter_specs` parameter to `load_behavior_map`, added 4 new tests.

### Gherkin Formatting

User observed that Given/When/Then bullet lists rendered as one continuous list in markdown (blank lines don't create visual separation between bullet lists).

Research:
- Checked Martin Fowler's article on Given-When-Then
- Confirmed GitHub supports `gherkin` syntax highlighting via Linguist

Applied gherkin code blocks to all specs:
- `pr-description-generator.md`
- `kb-linter.md`
- `backlink-scanner.md`
- `link-validator.md`

Each scenario now in its own fenced code block with syntax highlighting.

### Final Critique

Reviewed all work and identified remaining items:
- Missing example YAML files (deferred — spec examples sufficient for v1)
- Missing `spec-section` annotations (deferred — doesn't affect functionality)
- Open question about `behavior_map_source` format (closed — implemented direct backlink JSON)

## Decisions Made

- **Standalone CLI**: Not using `tool_cli.run_tool()` because generator outputs markdown not JSON, has no pass/fail semantics
- **YAML input**: Complex nested structure unwieldy as CLI flags; YAML is AI-generatable
- **PyYAML dependency**: Proper parsing warranted (unlike kb-linter's regex approach for simple frontmatter)
- **v1 behavior maps**: `§Section → file.py` format without restatements — simpler to implement
- **behavior_map_source accepts backlink JSON directly**: No transformation step needed, filtered to input specs
- **Gherkin code blocks for specs**: Better visual separation and syntax highlighting on GitHub

## Metrics

- **Tests**: 156 total (55 new for pr-description generator)
- **Coverage**: 100% on generator.py, 88% overall for new tool
- **Tools**: 4 (backlink-scanner, kb-linter, link-validator, pr-description)

## Observations

1. **Plan-driven implementation works well** — The detailed plan provided clear direction. Implementation was straightforward with spec as guide.

2. **Critique cycles catch real bugs** — First critique found 2 actual bugs (return type, filter logic) and 3 documentation gaps. Worth the time investment.

3. **Formatting details matter for specs** — The Given/When/Then rendering issue wasn't visible until someone read the rendered output. Gherkin blocks solve this elegantly.

4. **Generator tools need different patterns** — The tool_cli module assumes JSON output and pass/fail exit codes. Generators that output other formats (markdown) need standalone CLIs.

### Link Adapter Enhancement

User tested the generator on a separate project and identified that plain relative links don't work well in PR descriptions — GitHub needs absolute URLs for navigability.

#### Critique Findings

1. **CLI doesn't support GitHub adapter** — GitHubLinkAdapter existed but was unusable from CLI
2. **Dead code** — `check_file_exists()` function orphaned after adapter refactor
3. **No YAML input for GitHub config** — Users couldn't configure adapter from input file
4. **Behavior map files not linked** — Files displayed as plain text, not clickable

#### Implementation

Following patterns from `.graft/python-starter`:
- **Protocol-based DI**: `LinkAdapter` protocol in `protocols.py`
- **Fakes over mocks**: `FakeLinkAdapter` in `tests/fakes/` for testing
- **Frozen dataclass**: `GitHubConfig` as immutable context object

New adapter hierarchy:
- `PlainLinkAdapter` — relative markdown links (default, backward compatible)
- `GitHubLinkAdapter` — GitHub blob URLs + PR diff anchors

Added YAML configuration:
```yaml
github:
  owner: anthropic
  repo: delivery-practices
  branch: main
  pr_number: 42  # optional
```

GitHub adapter generates:
- Blob URLs for existing files: `https://github.com/owner/repo/blob/branch/path`
- PR diff anchors for new files: `#diff-<sha256(path)>`

#### Changes Made

| File | Change |
|------|--------|
| `protocols.py` | New — `LinkAdapter` protocol |
| `adapters/plain.py` | New — `PlainLinkAdapter` |
| `adapters/github.py` | New — `GitHubLinkAdapter` + `GitHubConfig` |
| `models.py` | Added `GitHubInput`, `github` field to `PRInput` |
| `generator.py` | Removed dead code, behavior map uses adapter |
| `__main__.py` | Added `create_adapter()`, uses config |
| `tests/fakes/` | New — `FakeLinkAdapter` |

## Updated Metrics

- **Tests**: 193 total (37 new for adapters)
- **Coverage**: 90% overall, 100% on generator and adapters
- **Tools**: 4 (backlink-scanner, kb-linter, link-validator, pr-description)

## Additional Observations

5. **Critique cycles continue to find real issues** — Second critique found 4 issues including dead code and unusable feature (GitHub adapter with no CLI support).

6. **Protocol-based DI enables clean testing** — FakeLinkAdapter with call tracking makes tests explicit about adapter interactions without mocking.
