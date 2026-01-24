---
status: working
last-validated: 2026-01-24
---

# Playbook: Iterative Build-Critique-Fix

How to develop features using structured critique loops to catch drift, gaps, and inconsistencies.

> **Context**: This playbook works with any development workflow but is especially effective with AI-assisted development, where the speed of implementation makes systematic review essential.

## When to Use

- After implementing a new feature or tool
- After making significant changes across multiple files
- When you want to verify quality before moving on
- At natural stopping points in a work session

## The Loop

```
Build → Critique → Fix → Expand (or Stop)
  ↑                          |
  └──────────────────────────┘
```

### 1. Build

Implement the feature, fix, or change. Use spec-first when creating new behavioral components.

### 2. Critique

Review the work just completed. Examine systematically:

| Category | What to check |
|----------|---------------|
| **Spec drift** | Does implementation match every behavior statement? |
| **Test gaps** | Are edge cases covered? Are assertions specific? |
| **Documentation** | Are references, examples, and descriptions current? |
| **Consistency** | Does this match patterns used elsewhere in the codebase? |
| **Dead code** | Are there unused parameters, stale imports, unreachable paths? |
| **Process** | Did we follow our own playbooks? Were steps skipped? |

**Be specific.** "The output format doesn't match the spec's example" is actionable. "Could be improved" is not.

### 3. Fix

Address findings from the critique:
- Fix spec-implementation drift (update whichever is wrong)
- Add missing tests
- Remove dead code
- Update stale documentation

**Only fix what was found.** Don't expand scope during the fix phase.

### 4. Expand or Stop

After fixing, decide:
- **Expand**: The improved state reveals what's next. Start a new Build phase.
- **Stop**: Quality is acceptable. Commit and move on.

**Signals to stop**:
- Critique findings are cosmetic, not behavioral
- Fixes are getting smaller each loop
- The work achieves its original goal

## Roles in AI-Assisted Development

| Role | Human | AI |
|------|-------|----|
| Build | Directs what to build | Implements |
| Critique | Decides which findings matter | Generates systematic critique |
| Fix | Approves approach | Executes fixes |
| Expand/Stop | Decides when to loop | Proposes next steps |

The human provides judgment; the AI provides thoroughness.

## Anti-patterns

- **Infinite polish**: Looping without a stopping signal. Each loop should have fewer, smaller findings.
- **Scope creep in fix**: Using the fix phase to add features. Fix only what the critique found.
- **Skipping critique**: Moving straight from build to the next build. Speed without review accumulates drift.
- **Ignoring diminishing returns**: Three loops caught real issues in v0.2.0. Ten loops would over-polish.

## Integration with Other Playbooks

- **Writing specs** → Build phase uses the [writing-specs playbook](writing-specs.md)
- **Reviewing against specs** → Critique phase uses the [review checklist](reviewing-against-specs.md)
- **Session logging** → Each loop's findings feed the [session note](session-logging.md)

## Related

- [Writing specs](writing-specs.md) — spec-first development (Step 9 is a mini-critique)
- [Reviewing against specs](reviewing-against-specs.md) — structured review checklist
- [Session logging](session-logging.md) — capturing what each loop found
- [Principles](../policies/living-specifications.md) — #5 (low ceremony), #16 (dogfooding)

## Sources

- Direct observation: Three critique cycles during delivery-practices v0.2.0 (2026-01-24)
- Each cycle caught real issues: spec drift (3 items), dead parameters, stale examples, vocabulary clashes
- [AI-assisted workflow exploration](../notes/2026-01-24-ai-assisted-workflow.md)
