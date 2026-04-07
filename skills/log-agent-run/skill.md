---
name: log-agent-run
description: Write a standardized agent run log after any worker invocation. Called automatically by Claude after every non-Claude worker completes. Not user-invocable.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Log Agent Run

## Purpose
Creates a structured, timestamped log file in `agent-logs/YYYY-MM/` after every non-Claude worker run. Ensures the audit trail is consistent regardless of which worker was used.

## When to Use
After every non-Claude worker invocation, once agent-evaluator has scored the output.

## Execution
```bash
python ~/.claude/skills/log-agent-run/log_agent_run.py \
  --worker "{worker-name}" \
  --task "{one sentence task}" \
  --spec "{key constraints given}" \
  --output "{2-3 sentence output summary}" \
  --correctness {1-5} \
  --scope {1-5} \
  --quality {1-5} \
  --side-effects {1-5} \
  --adaptations "{any spec/prompting changes tried, or 'none'}" \
  --flags "{anomalies or failures, or 'none'}"
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--worker` | yes | Model/worker name (e.g. codex, gemma-3-27b) |
| `--task` | yes | Task in one sentence |
| `--spec` | yes | Key constraints given to worker |
| `--output` | yes | 2-3 sentence output summary |
| `--correctness` | yes | Score 1-5 |
| `--scope` | yes | Score 1-5 |
| `--quality` | yes | Score 1-5 |
| `--side-effects` | yes | Score 1-5 |
| `--adaptations` | no | Prompting/spec changes tried (default: none) |
| `--flags` | no | Anomalies or failures (default: none) |

## Expected Output
```json
{
  "status": "ok",
  "log_path": "/path/to/agent-logs/YYYY-MM/YYYY-MM-DD-{worker}-{task-slug}.md",
  "composite_score": 3.5,
  "needs_attention": false
}
```

## Validation
Success: exit code 0, `status: ok`, log file exists at returned path.
Failure: exit code 1, error in stderr.

## On Success
If `needs_attention: true` (composite ≤2.0 or flags present): surface to user per manager-posture rules.
Otherwise: proceed silently.

## On Failure
Log the failure itself with a note. Do not block the main workflow over a logging error.

## References
- `rules/01-manager-posture.md` — when to call this skill
- `rules/04-audit-protocol.md` — log format specification
