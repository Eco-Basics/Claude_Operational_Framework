# Memory Protocol

## Design Principle
Memory is fetched when relevant — not preloaded speculatively.
The index (MEMORY.md) loads automatically. Individual files load on demand.

## When to Read
- Task involves a project you've worked on before → load project memory
- User references a preference or past correction → load feedback memory
- Task requires knowing about a specific tool or resource → load reference memory
- Working with a specific LLM worker → load its worker profile

## When to Write
| Trigger | Memory type | Location |
|---|---|---|
| User corrects behavior or gives preference | `feedback` | `memory/` |
| Project state changes (milestone, decision) | `project` | `memory/` |
| New resource or tool location learned | `reference` | `memory/` |
| Worker performance pattern observed | worker profile | `memory/worker-profiles/` |
| User explicitly asks to remember something | whichever fits | `memory/` |

## LEARNED.md vs Memory
- `LEARNED.md` — quick session corrections, Claude prompts user to add
- `memory/` — structured, semantic, persists across all projects
- When a LEARNED.md entry proves durable and cross-project: promote it to memory

## Worker Profiles
One file per LLM model: `memory/worker-profiles/{model-name}.md`
Contains: best-fit tasks, effective prompting patterns, known failure modes, audit scores over time.
Updated after: monthly audit, or when a notable pattern emerges mid-project.
