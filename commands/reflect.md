---
name: reflect
description: Review framework health and evolve it. Reads LEARNED.md and recent audit logs, identifies patterns, and proposes concrete improvements to framework files. Human-gated — Claude proposes, user approves each change.
---

## Step 1 — Read Current State
Read in sequence:
- `LEARNED.md` — all entries since last reflect
- `agent-logs/YYYY-MM/` — current month's logs
- `DECISIONS.md` — open questions and future considerations sections

## Step 2 — Identify Patterns
Surface:
- Recurring corrections in LEARNED.md worth promoting to a rule or memory entry
- Worker performance trends from audit logs
- Any open question from DECISIONS.md that now has enough evidence to resolve
- Framework friction — anything that's being worked around repeatedly

## Step 3 — Propose Changes
For each pattern found, propose a concrete change:

```
PROPOSAL {N}
Pattern: {what you observed}
Proposed change: {specific file + what to add/modify/remove}
Rationale: {why this improves the framework}
```

Present proposals one at a time. Wait for explicit approval or rejection before moving to the next.

## Step 4 — Execute Approved Changes
Write only approved changes. Commit all approved changes in a single commit.
Update `DECISIONS.md` with any newly resolved open questions.
Push to remote.

## Step 5 — Clear Applied Entries
Remove LEARNED.md entries that have been promoted to rules or memory.
For entries reviewed but not promoted: if they've appeared in 2+ reflect cycles without action, remove them — they're stale noise.
Log the reflect session date in DECISIONS.md under `## Reflect Log`.
