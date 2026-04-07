# Session Discipline

## End of Every Project Session
Before closing any project session, update the relevant project documentation:
- **LOG.md** — update with decisions, preferences, ideas from this session (see `rules/06-log-protocol.md`)
- **PLAN.md / phase docs** — record what was completed, what changed, what's next
- **Local CLAUDE.md** — update if project context, stack, or intelligence assignment changed
- **LEARNED.md** — prompt user for any correction worth capturing
- **Agent logs** — ensure all worker runs from this session are logged

This applies whether the session completed its goal or was interrupted mid-task.

## What "Relevant Project Doc" Means
The project's local CLAUDE.md, PLAN.md, phase docs, or any living document that tracks ongoing state.
If the project has no documentation structure yet: flag it and prompt setup.

## Why
A fresh session has no memory of this one. The next Claude instance must be able to pick up exactly where this one left off — from docs alone, not from conversation history.

## Cross-Session Continuity Check
Before starting work in any session, read the project's local CLAUDE.md and LOG.md.
If either is absent or stale: surface this before proceeding.
If LOG.md is absent in an existing project: offer to create it from available context before starting work.
