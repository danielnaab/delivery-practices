---
status: draft
---

# Playbook: Practice Lab

How to run a weekly team meeting focused on discovering and capturing effective delivery practices.

> **Context**: Teams often know retrospectives but struggle to systematically improve practices. Practice Lab is discovery-focused — finding what works, not validating existing assumptions.

## Meeting Format

Weekly 30 minutes, team only.

| Segment | Time | Purpose |
|---------|------|---------|
| **This Week's Observations** | 10 min | What did we notice? What worked unexpectedly? What friction did we hit? |
| **Pattern Recognition** | 10 min | Recurring themes? What might be worth trying systematically? |
| **Experiment for Next Week** | 5 min | Pick ONE thing to consciously try. Not formal — just intentional attention. |
| **Capture** | 5 min | What should we write down? KB note? Updated playbook? |

## Bootstrapping (First 2-3 Meetings)

First meetings have no prior data. Use this adapted format:

| Segment | Week 1 Approach |
|---------|-----------------|
| **Observations** | "Think about this past week. What surprised you? What was harder than expected? Easier?" |
| **Pattern Recognition** | Skip — not enough data yet |
| **Experiment** | "What ONE thing do we want to pay attention to this week?" |
| **Capture** | "What question should we add to observation prompts?" |

## Observation Prompts

Help people notice during the week:

- What took longer than expected?
- What was a surprisingly smooth handoff?
- Where did I feel uncertain about the right approach?
- What did I learn from someone else this week?
- What would I do differently if I could redo something?

## Recording Meetings

Use the [meeting record template](../meetings/_template.yaml).

```yaml
date: 2026-01-25
observations:
  - "PR description format helped Bob understand my change quickly"
  - "Lost 30 min trying to recover context from last session"
patterns:
  - "Context loss keeps coming up — third week in a row"
experiment:
  what: "Try session logging for one feature"
  who: ["Alice"]
captured:
  - note: "Added observation to notes/context-loss.md"
```

Store records in `meetings/YYYY-MM-DD.yaml`.

## Anti-Patterns and Antidotes

| Anti-Pattern | Symptom | Antidote |
|--------------|---------|----------|
| **Complaint session** | All friction, no insights | Require pattern recognition: "What does this tell us?" |
| **Vague observations** | "Things were hard" | Ask: "Can you give a specific example?" |
| **Capture paralysis** | Never writing anything down | Lightweight default: at least log observations |
| **Phantom experiments** | Experiments declared but never run | Start each meeting: "Did we try what we said?" |
| **Staleness** | Same topics, no progress | Track topics over time, escalate if recurring |

## Empty Weeks

"Nothing to observe" is a signal, not a skip. Use it for forced reflection:

- Are we not paying attention?
- Has everything genuinely been smooth? (That's worth noting too)
- What questions should we be asking ourselves?

## Knowledge Flow

```
observations → patterns → experiments → (if successful) → playbooks/docs
```

The meeting feeds the knowledge base. Practice Lab isn't the artifact — the KB is.

## Success Criteria

Evaluate after 6 weeks.

**Success requires all of:**
1. At least one practice documented in the KB
2. Team finds it useful (people want to continue)
3. At least one recurring friction addressed

**Week 6 questions:**
- Did any patterns turn into documented practices?
- What friction did we address?
- Should we continue, adjust, or stop?

## Facilitation Notes

- **Pre-work**: Encourage async observation collection, but don't require it
- **Owner**: Dedicated facilitator initially; expand once established
- **Time discipline**: 30 minutes is short — keep segments moving

## Related

- [Exploration note](../notes/2026-01-25-team-practices-meeting.md) — rationale and alternative models considered
- [Meeting record template](../meetings/_template.yaml) — structured capture format
- [Session logging](session-logging.md) — individual session capture (complements team-level Practice Lab)

## Sources

- Exploration: [Team practices meeting note](../notes/2026-01-25-team-practices-meeting.md) — analysis of alternative approaches
- Personal experience: retrospective formats that work vs. become stale
