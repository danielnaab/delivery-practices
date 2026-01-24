---
status: working
---

# Verification and Drift Detection

How to keep specifications honest—detecting and resolving divergence between specs and implementation.

## Detection Approaches

1. **PR-time analysis**: AI reads spec + code diff, flags inconsistencies. Non-blocking warning. Cheapest moment to fix.
2. **Periodic audit**: Scheduled scan producing drift reports. Noisier but catches gradual drift.
3. **Test-spec linkage**: When tests change without spec changes, flag potential drift.
4. **Structured assertion checking**: Behavior statements precise enough for mechanical verification.

## Backlinks Enable Automation

Implementation annotates which spec it implements:

```python
# spec: docs/specs/auth.md
# spec-section: Behavior/Login
def login(credentials):
    ...
```

Tools can then:
1. Find all files referencing a spec
2. Compare spec intent with implementation
3. Flag divergence

Without backlinks, detection requires guessing which code relates to which spec.

## Design Principles

- **High confidence first** — false positives kill trust in tooling
- **Detection over prevention** — suggestions, not blockers
- **Human decision authority** — AI flags, humans decide; no auto-correction
- **Targeted analysis** — only analyze files referencing specs, only when changed

## Implementation in This Repo

The [backlink scanner](../specs/backlink-scanner.md) implements structural verification for this repository: detecting dangling references and orphan specs via backlink annotations.

## Related

- [Principles](../policies/living-specifications.md) — #13 (references flow upstream)
- [Artifact relationships](relationships.md) — backlink patterns
