# Log Protocol

## What LOG.md Is
A per-project running log that gives a future Claude session fast context after `/clear` or a new session. It captures trajectory, meaningful decisions, preferences, and ideas worth preserving.

One file per project: `{project-dir}/LOG.md`

## Structure
```
## Active
Current trajectory, open decisions, live preferences, unresolved ideas.
This section is read first — keep it tight.

## Archived
Resolved decisions and completed phases, compressed to one line each.
Never deleted — demoted here when no longer active context.
```

## When to Write
Maintain proactively during sessions. Write when:
- A meaningful decision is made (what was chosen and why)
- A preference is expressed (how the user wants things done)
- An idea is surfaced worth preserving
- A phase or direction is completed or abandoned

Do not log: routine tool calls, minor clarifications, transient state.

## When to Update on Close
When the user signals session end ("is everything logged?", "/clear", or equivalent):
1. Review the conversation for anything not yet captured
2. Demote any Active entries that are now resolved
3. Confirm to user: "LOG.md updated." or list what was added

## Pruning Rule
`## Active` stays tight by judgment — anything resolved moves to `## Archived` as a one-liner.
No hard line limit. If the file grows beyond fast-loadable, compress Archived entries further.

## On Session Start
Read LOG.md alongside local CLAUDE.md to restore context.
If LOG.md is absent in an existing project: flag it and offer to create one from available context.
