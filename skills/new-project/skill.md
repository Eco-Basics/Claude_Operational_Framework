---
name: new-project
description: Scaffold a local CLAUDE.md for a new project from confirmed intent. Called from /intent after intent block is confirmed. Not user-invocable directly.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# New Project

## Purpose
Creates a local CLAUDE.md at the project directory root. Pre-fills confirmed intent block and intelligence assignment schema.

## When to Use
Step 6 of `/intent` command — after intent is confirmed and before any work begins.
Check first: if a CLAUDE.md already exists at `--project-dir`, skip (action: skipped).

## Execution
```bash
python ~/.claude/skills/new-project/new_project.py \
  --project-dir "/abs/path/to/project" \
  --project-name "Project Name" \
  --goal "One-sentence confirmed goal" \
  --success "What done looks like" \
  --out-of-scope "What is explicitly excluded" \
  [--default-worker "claude"] \
  [--code-worker "codex"] \
  [--research-worker "claude"] \
  [--data-worker ""]
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--project-dir` | yes | Absolute path to project root |
| `--project-name` | yes | Human-readable project name |
| `--goal` | yes | Confirmed one-sentence goal |
| `--success` | yes | Success criteria |
| `--out-of-scope` | yes | Explicit exclusions |
| `--default-worker` | no | Default worker (default: claude) |
| `--code-worker` | no | Code implementation worker (default: codex) |
| `--research-worker` | no | Research worker (default: claude) |
| `--data-worker` | no | Data processing worker (default: unassigned) |

## Expected Output
```json
{
  "status": "ok",
  "claude_md_path": "/abs/path/to/project/CLAUDE.md",
  "project_name": "Project Name",
  "action": "created|skipped"
}
```

## Validation
Success: exit 0, `status: ok`, file exists at returned path.
If CLAUDE.md already exists: `action: skipped`, no overwrite.

## On Success
Read the created file back. Confirm to user: "Local CLAUDE.md created at {path}. Intelligence assignment is pre-filled — adjust workers if needed."
Then create `{project-dir}/LOG.md` with starter structure:
```markdown
# Log — {project_name}

## Active

## Archived
```
Confirm: "LOG.md created at {path}."

## On Failure
Surface the error. Do not proceed with project setup until CLAUDE.md exists.

## References
- `commands/intent.md` — step 6 calls this skill
- `templates/local-claude-md.md` — template this is based on
