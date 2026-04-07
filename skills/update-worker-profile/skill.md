---
name: update-worker-profile
description: Update a worker's profile in memory/worker-profiles/ after an audit or degradation event. Called by Claude post-audit or when worker degradation protocol triggers. Not user-invocable.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Update Worker Profile

## Purpose
Appends a timestamped performance entry to `memory/worker-profiles/{model}.md`. Creates the profile stub if it doesn't exist.

## When to Use
- After `/audit` — to record audit conclusions
- When worker degradation protocol triggers (2x consecutive ≤2 score on any dimension)
- After adaptation attempts succeed or fail

## Execution
```bash
python ~/.claude/skills/update-worker-profile/update_worker_profile.py \
  --model "{model-name}" \
  --event "{audit|degradation|adaptation}" \
  --task-types "{comma-separated task types}" \
  --composite {1.0-5.0} \
  --notes "{what happened, what was tried, outcome}" \
  --decision "{keep|reassign|drop|adapt}"
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--model` | yes | Model/worker name (e.g. codex, gemma-3-27b) |
| `--event` | yes | Trigger: audit, degradation, or adaptation |
| `--task-types` | yes | Comma-separated task types this worker handles |
| `--composite` | yes | Composite score from this event (1.0–5.0) |
| `--notes` | yes | What happened, what was tried, outcome |
| `--decision` | yes | keep, reassign, drop, or adapt |

## Expected Output
```json
{
  "status": "ok",
  "profile_path": "/path/to/memory/worker-profiles/{model}.md",
  "action": "updated|created"
}
```

## Validation
Success: exit 0, `status: ok`, file exists at returned path.
Failure: exit 1, error in stderr.

## On Success
If `decision` is `drop` or `reassign`: surface to user to confirm task assignment change in project's local CLAUDE.md.
Otherwise: proceed silently.

## On Failure
Log failure note. Do not block the audit workflow over a profile write error.

## References
- `rules/01-manager-posture.md` — Worker Degradation section
- `rules/04-audit-protocol.md` — when this is called
