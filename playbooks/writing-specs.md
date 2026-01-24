---
status: working
---

# Playbook: Writing Specifications

How to write a new specification or update an existing one.

## When to Write a Spec

| Change Type | Spec Impact | Action |
|-------------|------------|--------|
| New feature | New spec needed | Write spec first, or combined with implementation |
| Behavior change | Must update | Update in same PR as code change |
| Bug fix (spec wrong) | Correction | Update spec to match intended behavior |
| Bug fix (code wrong) | None | Spec was already correct |
| Refactor | None | No behavior change, spec unchanged |

**Ceremony scales with impact.** Trivial changes need no spec update; behavior changes do.

## Steps

### 1. Create the File

```bash
# New spec
cp docs/specifications/format.md docs/specs/[feature-name].md
```

Set frontmatter:
```yaml
---
status: proposed
last-verified: [today]
owners: [your-name]
---
```

### 2. Write the Intent

Answer: why does this exist? What problem does it solve? One paragraph is usually enough.

### 3. Define Non-goals

Explicitly state what's out of scope. This prevents scope creep and clarifies boundaries for reviewers and implementers.

### 4. Specify Behavior

Use Given/When/Then structure for each scenario:

```markdown
### Login
- Given valid credentials
- When the user submits the login form
- Then they receive a session token and are redirected to dashboard
```

Add edge cases separately:
```markdown
### Edge Cases
- Empty email: returns 400 with "email required" message
- Expired account: returns 403 with reactivation link
```

### 5. Add Constraints

Non-functional requirements that might otherwise get lost:
- Performance bounds
- Security requirements
- Compatibility needs

### 6. Mark Open Questions

For anything unresolved, use checkboxes:
```markdown
## Open Questions
- [ ] Should rate limiting apply per-user or per-IP?
- [ ] What's the session token expiry? (team decision needed)
```

These explicitly invite collaboration without blocking progress.

### 7. Cite Sources

Include provenance for all behavior decisions:
```markdown
## Sources
- [OWASP Auth Guidelines](URL) - Session management patterns
- Personal experience: Project X - Rate limiting approach
```

## Updating an Existing Spec

1. Find the spec (via backlink in code, or in `docs/specs/`)
2. Update behavior statements to reflect the change
3. Update `last-verified` date in frontmatter
4. Include spec update in the same PR as code change
5. If status was `implemented`, keep it (the update is part of the implementation)

## Key Reframe

**Spec review IS design review.** It's the same discussion that would happen in Slack or meetings, but captured durably. Not extra work—better-preserved work.

## Anti-patterns

- **Spec-police**: Blocking PRs for trivial missing spec updates
- **Spec-after-the-fact**: Writing specs only to document what's already built
- **Spec-as-ticket**: Treating specs as one-time artifacts that get "done"
- **Approval-ceremony**: Requiring layers beyond normal PR review

## Related

- [Specification format](../docs/specifications/format.md) — the template reference
- [Principles](../policies/living-specifications.md) — normative rules
- [Reviewing against specs](reviewing-against-specs.md) — the reviewer's perspective
