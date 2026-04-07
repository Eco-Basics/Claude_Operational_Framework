---
name: codex-output-validator
description: Structural pre-check of Codex output before full evaluation. Validates non-empty, has code, no truncation, language matches. Produces PASS/FLAG/FAIL verdict.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Codex Output Validator

## Purpose
Runs fast, heuristic structural checks on Codex output. Filters out clearly broken output before the full evaluation rubric runs. Not a quality judge — a gatekeeper.

## When to Use
Immediately after Codex returns output, before invoking agent-evaluator.

## Execution
```bash
python ~/.claude/skills/for-agents/codex-output-validator/codex_output_validator.py \
  --spec "{the spec that was given to Codex}" \
  --output "{Codex output string or absolute path to output file}" \
  --language "python|typescript|go|etc"
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--spec` | yes | Original spec (string) |
| `--output` | yes | Codex output (string or file path) |
| `--language` | yes | Expected language |

## Expected Output
```json
{
  "status": "ok",
  "verdict": "PASS|FLAG|FAIL",
  "checks": {
    "non_empty": true,
    "has_code": true,
    "no_truncation": true,
    "language_matches": true
  },
  "issues": []
}
```

## Verdict Meanings
- **PASS** — structurally valid, proceed to agent-evaluator
- **FLAG** — minor issues (partial response, TODO placeholders), Claude reviews before evaluating
- **FAIL** — empty, wrong language, or truncated — trigger retry with adjusted spec

## Validation
This script always exits 0 (validator itself should not crash). The `verdict` field is the signal.

## On PASS
Proceed to agent-evaluator for rubric scoring.

## On FLAG
Surface issue to Claude: accept with caveat / retry with adjusted spec.

## On FAIL
Trigger retry per failure fallback chain in `rules/01-manager-posture.md`. Log in agent-logs.

## References
- `rules/01-manager-posture.md` — failure fallback chain
- `agents/agent-evaluator.md` — next step after PASS
- `skills/for-agents/evaluator-rubric-scorer/` — scoring step after this
