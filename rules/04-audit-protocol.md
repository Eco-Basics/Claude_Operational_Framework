# Audit Protocol

## What Gets Logged
After every non-Claude worker invocation, write one log file:
Path: `agent-logs/YYYY-MM/YYYY-MM-DD-{worker}-{task-slug}.md`

## Log Format
```
DATE: YYYY-MM-DD
WORKER: {model name}
TASK: {one sentence}
SPEC SUMMARY: {key constraints given}
OUTPUT SUMMARY: {2-3 sentences}
SCORES: Correctness={1-5} Scope={1-5} Quality={1-5} SideEffects={1-5}
ADAPTATIONS: {any prompting/spec changes attempted — or "none"}
FLAGS: {anomalies, drift, or notable failures — or "none"}
```

## When to Prompt User for Audit
Proactively ask user to run `/audit` when:
- Any worker scores ≤2 on a dimension in 3+ consecutive runs
- A new worker model is being considered for a task assignment

## The /audit Command
1. Read all logs in the current month's folder
2. Surface patterns: best/worst performing workers, failure modes, task-type mismatches, adaptation attempts and whether they worked
3. Propose concrete changes: updated worker profiles, reassigned task types, prompting improvements, or worker removal
4. User reviews and approves each proposal
5. Approved changes committed to git and pushed

## Evolution Rule
Every approved proposal must result in a concrete file change:
- Updated worker profile in `memory/worker-profiles/`
- Updated task assignment in project `CLAUDE.md`
- Updated spec guidance in `rules/02-agent-interface.md`

No abstract conclusions — concrete diffs only.
