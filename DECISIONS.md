# Framework Design Decisions
> Captured from founding session — April 2026
> Use this as context when continuing the build or running /reflect

---

## Purpose of This Document
This log captures every significant design decision made during the initial framework build session, including what was considered, what was rejected, and why. A future Claude session reading this file should be able to continue the build without re-litigating resolved questions.

---

## How to Use This Document
Point a fresh Claude session to this file to resume the build:
> "Read DECISIONS.md and continue building the framework from where it left off."

Claude should read this file + the current state of `~/.claude/` files and proceed without asking questions that are already answered here.

---

## What This Framework Is

A personalized Claude operational framework that is:
- **Evolvable** — improves itself through structured feedback loops
- **Migratable** — identical setup on local Windows machine and Linux VPS via git
- **Manager-first** — Claude is the employer of AI workers, not a direct executor
- **Intent-coherent** — capturing intent correctly is the most critical function

**Repository:** https://github.com/Eco-Basics/Claude_Operational_Framework (private)

---

## Foundational Philosophy

### Claude as Intent-Coherence Engine
**Decision:** Claude's primary role is not execution — it is ensuring that what the user wants and what Claude understands are the same thing before anything happens.

**Why:** The most expensive failure is building the wrong thing correctly. Intent coherence prevents this at the source.

**Implementation:** `rules/00-intent-capture.md` — highest priority rule, applies before any execution, planning, research, or delegation in any context.

---

### Claude as Manager of Intelligences
**Decision:** Claude is an employer. All AI operations — whether Claude subagents, Codex, local LLMs, or future models — are workers that Claude manages, evaluates, and reports on. The user interacts only with Claude.

**Why:** Consistent interface regardless of which AI does the work. Quality control through evaluation. Claude builds institutional knowledge about each worker over time.

**Implementation:** `SOUL.md`, `AGENTS.md`, `rules/01-manager-posture.md`, `rules/02-agent-interface.md`

---

### Give Claude Tools to Get Context — Not Context Upfront
**Decision:** The framework stays lean by design. Claude fetches what it needs when it needs it. Nothing is preloaded speculatively.

**Why:** Reduces context window bloat. Keeps CLAUDE.md under 60 lines. Rules files are always loaded but small. Memory loads on demand.

**Implementation:** CLAUDE.md as pointer file, rules as small focused files, memory loaded when relevant.

---

## File Structure Decisions

### Split CLAUDE.md Approach (from pro-workflow repo)
**Decision:** Global context is split across multiple files rather than one monolithic CLAUDE.md.

| File | Concern |
|---|---|
| `CLAUDE.md` | Lean anchor — identity, non-negotiables, pointers (<60 lines) |
| `SOUL.md` | Voice, communication style, judgment posture |
| `AGENTS.md` | Global agent roster and delegation rules |
| `LEARNED.md` | Dynamic mid-session corrections (user-approved) |
| `rules/` | Modular behavioral contracts |
| `memory/` | Semantic memory (existing system) |
| `agent-logs/` | Audit logs (never auto-loaded) |

**Why:** Each file has one concern. CLAUDE.md stays readable and cacheable. Rules can evolve independently.

**Rejected:** Single large CLAUDE.md (too bloated), lazy-loading rules (risk of being skipped).

---

### Rules Are Always-Loaded, Not Lazy
**Decision:** Rules files in `rules/` load every session. They are kept small (target <50 lines each) to make this viable.

**Why:** Lazy-loading risks rules being skipped. The solution is size discipline, not deferred loading.

---

### Git Repo for Portability
**Decision:** `~/.claude/` is its own dedicated git repo separate from the home directory repo.

**Repo:** https://github.com/Eco-Basics/Claude_Operational_Framework

**VPS sync:** `git clone https://github.com/Eco-Basics/Claude_Operational_Framework.git ~/.claude`
**Update cycle:** `git push` locally → `git pull` on VPS.
**Machine-specific:** `settings.local.json` is gitignored. Never committed.

**Why:** Single source of truth. One push syncs everything everywhere. No manual file copying.

---

## Behavioral Design Decisions

### No Explicit Modes
**Decision:** Dropped explicit mode system (RESEARCH/DEV/PROJECT/EVAL as declared states).

**Why:** The intent capture protocol + intelligence assignment in local CLAUDE.md already handle behavioral adaptation. Declaring a mode is redundant friction on top of what intent capture already does. A good manager doesn't announce mode switches — they read the demand and respond.

**What replaced it:** Dynamic posture. Claude adapts based on task type detected from intent. The intelligence assignment in local CLAUDE.md routes work to appropriate workers.

**Rejected:** Four mode rule files, MODE: declarations in CLAUDE.md.

---

### EVAL as Command, Not Mode
**Decision:** EVAL is the one exception — it remains as an explicit `/eval` command that toggles execution lockout for the session.

**Why:** EVAL is not a task type that can be inferred from intent — it's a deliberate constraint. "No execution at all" must be declared, not assumed.

**Behavior in EVAL (strict):** Claude delegates only — absolute manager posture. If an agent fails, Claude reports the failure and stays locked. Claude cannot self-execute to compensate. User must exit eval (`/eval` again or start new session) to unlock. This is stricter than normal fallback chain — the fallback chain's "Claude takes over" step is explicitly disabled in EVAL.

**Key distinction from other postures:** In normal operation, Claude can self-execute as a last resort. In EVAL, this fallback is intentionally removed. Claude is a pure observer/delegator/evaluator.

**Why this matters:** EVAL exists for auditing and strategic review. If Claude starts executing during a review session, it pollutes the review context.

---

### Worker Degradation → Adaptation Before Removal
**Decision:** When a worker performs poorly, Claude first attempts to improve output quality through different prompting strategies, revised specs, or adjusted constraints. Only after adaptation attempts fail does the monthly audit decide keep-or-remove.

**Why:** Poor output from a model is often a prompting problem, not a model problem. Removing workers too quickly wastes good tools.

**Implementation:** `rules/01-manager-posture.md` — Worker Degradation section.

---

### Failure Fallback Chain
**Decision:** Every failure state has a defined next action. Claude never stalls.

```
PASS  → proceed
FLAG  → Claude resolves autonomously (accept/retry with adjusted spec/take over)
FAIL or hard error
  → Retry once: same worker, adjusted spec
  → Still fails: Claude executes directly
  → Claude fails: surface to user with full context
```

**Hard limits:**
- Max 1 retry per worker per task
- No automatic cross-worker substitution (hides failures from audit)
- Declared fallbacks (`TASK_FALLBACK:` in local CLAUDE.md) are the only exception — added when needed, not upfront

**Why no automatic cross-worker fallback:** Silent substitution hides failure patterns from the audit log. The manager must see every failure.

---

### /intent as Project Flow Entry Point
**Decision:** `/intent` is the canonical way to start a project or a complex task. It is not just a utility — it is the entry gate to the project setup flow.

**Flow:**
1. User runs `/intent`
2. Claude walks through intent capture interactively (goal, success criteria, out of scope)
3. Intent block is confirmed
4. This naturally leads into local `CLAUDE.md` setup for the project
5. Everything downstream — worker assignment, agent selection, mode — flows from that

**Why:** Ensures no project starts without confirmed intent. The local CLAUDE.md is populated with purpose, not boilerplate.

---

### /reflect as Framework Self-Improvement Command
**Decision:** The framework needs a command to improve itself. `/reflect` reviews LEARNED.md entries + audit logs, proposes concrete changes to framework files, walks through user approval, and commits.

**Why:** The framework is designed to be evolvable. Without a structured self-improvement mechanism, evolution is ad hoc and inconsistent. `/reflect` is the scheduled maintenance interface.

**Human-gated:** Claude proposes, user approves each change individually. No autonomous rule modification.

---

### Design Log (DECISIONS.md) as Part of the Repo
**Decision:** This file (`DECISIONS.md`) is committed to the framework repo and updated at the end of each significant build session.

**Why:** Preserves the "why" behind every decision. Prevents future sessions from re-litigating resolved questions. A fresh Claude session can read this file and continue the build without losing context.

**How to use:** Point a new session to this file — "Read DECISIONS.md and continue the build." Claude reads the build status and proceeds from where it left off.

---

### Monthly Audit as Manual Command
**Decision:** `/audit` is user-triggered. Claude proactively asks when thresholds are hit (3 consecutive ≤2 scores on any dimension), but does not run autonomously.

**Why:** Evolution is human-gated. Claude proposes, user approves. No autonomous rule changes.

**What audit produces:** Concrete file changes only — updated worker profiles, reassigned task types, spec guidance updates. No abstract conclusions.

---

### LEARNED.md vs Memory System
**Decision:** Two separate mechanisms for capturing corrections.

| | LEARNED.md | memory/ |
|---|---|---|
| Speed | Fast — Claude prompts, user approves inline | Slower — structured write |
| Scope | Session corrections, quick rules | Cross-project, semantic |
| Promotion | Durable LEARNED entries → promote to memory | Stays in memory/ |

**Why:** Different latency needs. Quick corrections shouldn't require full memory protocol. Durable patterns should graduate to the semantic memory system.

---

### Worker Profiles in Memory
**Decision:** One `.md` file per LLM model in `memory/worker-profiles/`.

**Contains:** Best-fit tasks, effective prompting patterns, known failure modes, adaptation attempts, audit scores over time.

**Why:** Claude builds institutional knowledge about each worker. Changing a model doesn't lose the accumulated learning about how to work with it effectively.

---

## Intelligence Assignment Design

### Declared at Project Start in Local CLAUDE.md
**Decision:** Which intelligence handles which task type is declared explicitly in each project's local CLAUDE.md, not inferred globally.

**Format:**
```
## Intelligence Assignment
DEFAULT: claude
CODE_IMPLEMENTATION: codex
RESEARCH: claude
DATA_PROCESSING: gemma-3-27b
EVALUATION: claude
```

**Why:** Makes worker routing explicit and auditable. No ambiguity about which model did what.

**If undeclared:** All tasks default to Claude.

**If a non-Claude worker is assigned:** Claude manages, evaluates, and reports all its outputs. The user never interacts with the worker directly.

---

## Reference Research

### Repositories studied during framework design
- **shanraisshan/claude-code-best-practice** — anchor for best practices
- **rohitg00/pro-workflow** — split CLAUDE.md pattern, SOUL.md, context-engineer agent, LEARNED.md pattern
- **block/goose** — provider abstraction concept (swap LLM backends without framework changes)
- **microsoft/autogen** — multi-agent conversation patterns
- **crewAI** — hierarchical manager/worker separation, role-based agents
- **langchain-ai/langgraph** — graph-based state, checkpointing
- **AgentOps-AI/agentops** — offline audit log pattern, decorator instrumentation
- **vibrantlabsai/ragas** — LLM-graded evaluation, stochastic scoring

### Key patterns adopted
- Cache-aware static-first CLAUDE.md structure (CC-RIG)
- Hierarchical manager/worker with explicit role separation (CrewAI/MAF)
- Provider abstraction — same management protocol regardless of LLM (Goose)
- Offline audit logs, not in context (AgentOps adapted)
- Stochastic evaluation principle — LLMs are non-deterministic, single-run scoring is unreliable (AgentEval)
- Human-gated evolution — Claude proposes, user approves, committed to git

---

## Build Status

### Completed ✅
| File | Purpose |
|---|---|
| `CLAUDE.md` | Global anchor (<60 lines) |
| `SOUL.md` | Identity, voice, communication style |
| `AGENTS.md` | Global agent roster + delegation rules |
| `LEARNED.md` | Dynamic corrections (starts empty) |
| `DECISIONS.md` | This file — design log and build continuity |
| `rules/00-intent-capture.md` | Highest priority rule |
| `rules/01-manager-posture.md` | Employer posture + failure chain + fallback protocol |
| `rules/02-agent-interface.md` | Universal LLM invocation protocol |
| `rules/03-memory-protocol.md` | When/what to read and write |
| `rules/04-audit-protocol.md` | Log format + audit trigger conditions |
| `agents/intent-auditor.md` | Coherence check before execution |
| `agents/agent-evaluator.md` | Rubric scoring of worker output |
| `agents/context-engineer.md` | Context window health audit |
| `commands/audit.md` | `/audit` — review logs, propose improvements |

| `commands/eval.md` | `/eval` — execution lockout, pure delegation, no Claude self-execution |
| `commands/intent.md` | `/intent` — project flow entry point, leads to local CLAUDE.md setup |
| `commands/reflect.md` | `/reflect` — framework self-improvement, reviews LEARNED + audit logs |

### Still To Build ⏳
| Item | Notes |
|---|---|
| Local `CLAUDE.md` template | Project entry point with intelligence assignment schema |
| `setup.sh` | New machine / VPS bootstrap: clone repo, install plugins, configure env |
| Skills | Design discussion needed — what recurring workflows warrant a skill? |
| Git worktrees | Design discussion needed — parallel session patterns |

---

## Open Questions / Future Considerations
- **Skills vs commands:** Skills run inline (shared context), commands can fork. What recurring workflows are better as skills?
- **Git worktrees:** Spinning up parallel Claude sessions on separate branches — useful for research + implementation running simultaneously. Discuss pattern.
- **GSD agents:** 16 GSD agents currently installed. Which are actually used? Candidates for removal to reduce roster bloat. Context-engineer can audit this.
- **MCP audit:** Which MCPs are earning their context weight? Run context-engineer after setup to assess.
- **`rules/05-dynamic-posture.md`:** Possibly worth adding explicit guidance on how Claude shifts posture by demand type (research vs implementation vs orchestration). Currently implicit — may need to be explicit.
- **Worker onboarding flow:** When a new LLM worker is added to a project, what's the onboarding checklist? (add to `rules/02-agent-interface.md`, create worker profile stub, define task spec format quirks)
