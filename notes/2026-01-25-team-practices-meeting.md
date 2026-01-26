---
status: draft
---

# Practice Lab: Team Practice Improvement Exploration

Date: 2026-01-25

Exploration of establishing a regular team meeting for delivery practice improvement. Evolved from initial "Win/Pain Point/Practice Review" format through analysis of alternative models to a discovery-focused "Practice Lab" approach.

## Context

Starting point was a weekly meeting concept with structured segments (Win Report, Pain Point Triage, Practice Review). But before committing to a mechanism, we needed to understand the actual problems being solved.

## Part 1: What Problem Are We Actually Solving?

| Problem | Is it real? | Evidence |
|---------|-------------|----------|
| Practices don't get adopted | Probably | Teams know about good practices but don't use them |
| Knowledge gets lost | Yes | Same mistakes repeat, onboarding is slow |
| Pain points linger | Depends | Some teams address friction, others don't |
| No systematic improvement | Common | Retros produce action items that die |

**Fundamental tension**: Discovery vs. Adoption

- If **discovery**: Need experimentation, diverse inputs, failure tolerance
- If **adoption**: Need demonstration, practice, accountability

The original proposal conflated these. Win Report assumes adoption validation. Pain Point Triage is about discovery. Practice Review could be either.

## Part 2: Alternative Models Considered

### Model A: Experiment-Driven (No Standing Meeting)

Run explicit practice experiments with hypothesis → measurement → conclusion cycles.

```yaml
experiment:
  name: "PR description template"
  hypothesis: "Structured PR descriptions reduce review time by 30%"
  duration: "2 weeks"
  measurement: "Self-reported review effort (1-5 scale)"
  outcome: "succeeded" | "failed" | "inconclusive"
```

**Strengths**: Forces specificity, built-in measurement, lower time commitment
**Weaknesses**: Experiments take design energy, momentum can die over 2 weeks

### Model B: Embedded Practice Reflection (No New Meeting)

Inject practice reflection into existing workflows:

| Activity | Hook |
|----------|------|
| PR description | "What practice did this PR apply?" |
| Code review | "What made this PR easy/hard to review?" |
| PR merge | CI bot asks about friction |
| Weekly standup | 2-minute "Practice of the week" |

**Strengths**: Zero additional meetings, captures in context
**Weaknesses**: Easy to ignore, no dedicated attention

### Model C: Practice Guild (Cross-Team, Lower Frequency)

Monthly cross-team meeting. Each meeting: one team presents a practice they've been working on.

**Strengths**: Broader perspective, learn from diverse experience
**Weaknesses**: Cross-team coordination is hard, practices may not transfer

### Model D: Personal Practice Journals + Periodic Share

Individual reflection with optional sharing. Daily prompt, weekly synthesis, biweekly share.

**Strengths**: Individual reflection is more honest, written artifacts persist
**Weaknesses**: Many won't maintain journals, no collective decision mechanism

### Model E: Friction-Triggered Sessions (No Standing Meeting)

Meet only when someone calls a practice session for specific friction.

**Strengths**: Directly addresses real problems, demand-driven
**Weaknesses**: Bias toward visible friction, doesn't capture wins

## Part 3: Priorities Clarified

Through discussion, priorities emerged:

| Priority | Implication |
|----------|-------------|
| **Discovery** over adoption | Open observations, not structured reports |
| **Knowledge persistence** | Explicit capture step, git-tracked artifacts |
| **Systematic improvement** | Regular cadence, recurring format |
| **Room for emergence** | Not over-structured, patterns emerge from data |

Weekly meeting acceptable. Lightweight structure preferred.

## Part 4: Chosen Approach — Practice Lab

A discovery-focused meeting format optimized for finding what works, not validating what we think should work.

### Format

Weekly 30 min, team only.

| Segment | Time | Purpose |
|---------|------|---------|
| **This Week's Observations** | 10 min | What did we notice? What worked unexpectedly? What friction did we hit? |
| **Pattern Recognition** | 10 min | Recurring themes across observations? What might be worth trying? |
| **Experiment for Next Week** | 5 min | ONE thing to consciously try. Intentional attention, not formal hypothesis. |
| **Capture** | 5 min | What should we write down? KB note? Updated playbook? |

### Key Differences from Original Proposal

1. **No "Win Report"** — assumes you know what practices are. Instead: open observations.
2. **No "Practice Review"** — assumes existing practices to review. Instead: pattern recognition.
3. **Explicit "Capture" step** — knowledge persistence is first-class, not byproduct.
4. **Lighter experiments** — intentional attention, not formal hypothesis/measurement rigor.

### Knowledge Flow

```
observations → patterns → experiments → (if successful) → playbooks/docs
```

The meeting isn't the artifact — it feeds the KB.

### Anti-Patterns to Avoid

| Anti-Pattern | Symptom | Antidote |
|--------------|---------|----------|
| **Complaint session** | All friction, no insights | Require pattern recognition |
| **Vague observations** | "Things were hard" | Ask for specific examples |
| **Capture paralysis** | Never writing anything | Lightweight default: log observations |
| **Phantom experiments** | Declared but never run | Start each meeting: "Did we try it?" |
| **Staleness** | Same topics, no progress | Track topics, escalate if recurring |

## Part 5: Success Criteria

**Evaluation point:** 6 weeks

**Success requires all of:**
1. At least one practice documented — concrete artifact emerged
2. Team finds it useful — qualitative: people want to continue
3. Recurring friction addressed — something that kept coming up got resolved

**Week 6 retrospective questions:**
- Did any patterns turn into documented practices?
- What friction point(s) did we address?
- Should we continue, adjust, or stop?

## Deliverables

From this exploration:

1. **This note** — exploration journey and rationale
2. **[Playbook](../playbooks/practice-lab.md)** — operational guide for running meetings
3. **[Meeting template](../meetings/_template.yaml)** — structured record format

## What's Next

1. Share with team for feedback
2. Schedule first Practice Lab meeting
3. Run for 6 weeks
4. Evaluate against success criteria

## Sources

- Personal experience: delivery-practices KB development — patterns from building this repo
- Personal experience: team retrospectives — what works vs. what becomes stale
- Exploration discussion: 2026-01-25 session analyzing alternative approaches
