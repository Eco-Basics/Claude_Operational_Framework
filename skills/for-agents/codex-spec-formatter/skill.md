---
name: codex-spec-formatter
description: Format a task description into a Codex-optimal structured prompt spec. Used before any Codex invocation to convert intent into the spec format Codex performs best with.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Codex Spec Formatter

## Purpose
Converts a raw task description into the structured prompt spec that maximizes Codex output quality. Codex performs significantly better with explicit output structure, clear constraints, and explicit exclusions.

## When to Use
Before every Codex invocation. Claude calls this to convert confirmed intent into an optimized spec, then passes the `spec` field as the Codex prompt.

## Execution
```bash
python ~/.claude/skills/for-agents/codex-spec-formatter/codex_spec_formatter.py \
  --task "what needs to be done" \
  --language "python|typescript|etc" \
  --output-format "what the output should look like" \
  [--framework "fastapi|react|etc"] \
  [--constraints "comma-separated constraints"] \
  [--exclusions "comma-separated things NOT to do"]
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--task` | yes | Task in plain English |
| `--language` | yes | Target language |
| `--output-format` | yes | Expected output structure (files, functions, etc.) |
| `--framework` | no | Framework (default: none) |
| `--constraints` | no | Key constraints (default: none) |
| `--exclusions` | no | Explicit exclusions (default: none) |

## Expected Output
```json
{
  "status": "ok",
  "spec": "formatted spec string ready to pass to Codex",
  "word_count": 120
}
```

## Validation
Success: exit 0, `spec` field is a non-empty string.

## On Success
Pass the `spec` field value directly as the Codex prompt.

## References
- `rules/02-agent-interface.md` — Codex invocation section
- `skills/for-agents/codex-output-validator/` — validate Codex output after run
