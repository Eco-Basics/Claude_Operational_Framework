---
name: onboard-worker
description: Create a new worker profile stub in memory/worker-profiles/. Called when a new LLM worker is added to a project. Not user-invocable.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Onboard Worker

## Purpose
Creates `memory/worker-profiles/{model}.md` with an initial profile stub for a new worker. First step when adding a new LLM to the roster.

## When to Use
When a new LLM worker is declared in a project's local CLAUDE.md and no profile exists yet.
Check first: if `memory/worker-profiles/{model}.md` already exists, `action: already_exists` — do not overwrite.

## Execution
```bash
python ~/.claude/skills/onboard-worker/onboard_worker.py \
  --model "{model-name}" \
  --invocation "{codex|ollama|bash|agent}" \
  --task-types "{comma-separated best-fit task types}" \
  [--notes "{any known quirks, prompting tips, or context}"]
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--model` | yes | Model/worker name (e.g. gemma-3-27b) |
| `--invocation` | yes | How to call this worker: codex, ollama, bash, agent |
| `--task-types` | yes | Comma-separated task types this worker handles |
| `--notes` | no | Initial notes on known quirks or prompting guidance |

## Expected Output
```json
{
  "status": "ok",
  "profile_path": "/path/to/memory/worker-profiles/{model}.md",
  "action": "created|already_exists"
}
```

## Validation
Success: exit 0, `status: ok`.
If profile already exists: `action: already_exists`, no overwrite — not an error.

## On Success
Confirm to user: "Worker profile created at {path}. Add task assignment to local CLAUDE.md."
If `action: already_exists`: "Profile already exists at {path} — no changes made."

## On Failure
Surface the error. Worker should not be used in managed operations without a profile.

## References
- `rules/02-agent-interface.md` — invocation patterns by type
- `rules/03-memory-protocol.md` — worker profiles section
- `skills/update-worker-profile/` — used after the first run to record performance
