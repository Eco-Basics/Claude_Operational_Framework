---
name: evaluator-rubric-scorer
description: Aggregate and validate 4-dimension rubric scores for agent-evaluator. Ensures consistent scoring format with required rationales. Produces composite score and PASS/FLAG/FAIL verdict.
allowed-tools: [Bash]
model: haiku
user-invocable: false
---

# Evaluator Rubric Scorer

## Purpose
Takes 4 dimension scores + rationales from agent-evaluator, computes composite, and returns a structured verdict. Ensures scoring is consistent and that every dimension has a one-sentence rationale from actual output evidence.

## When to Use
Called by agent-evaluator when it has finished reviewing worker output. Provides the final structured score before logging.

## Execution
```bash
python ~/.claude/skills/for-agents/evaluator-rubric-scorer/evaluator_rubric_scorer.py \
  --worker "{worker name}" \
  --task "{task slug}" \
  --correctness {1-5} \
  --correctness-rationale "one sentence from actual output" \
  --scope {1-5} \
  --scope-rationale "one sentence from actual output" \
  --quality {1-5} \
  --quality-rationale "one sentence from actual output" \
  --side-effects {1-5} \
  --side-effects-rationale "one sentence from actual output"
```

## Arguments
| Argument | Required | Description |
|---|---|---|
| `--worker` | yes | Worker name |
| `--task` | yes | Task slug |
| `--correctness` | yes | Score 1-5 |
| `--correctness-rationale` | yes | Evidence-based one sentence |
| `--scope` | yes | Score 1-5 |
| `--scope-rationale` | yes | Evidence-based one sentence |
| `--quality` | yes | Score 1-5 |
| `--quality-rationale` | yes | Evidence-based one sentence |
| `--side-effects` | yes | Score 1-5 |
| `--side-effects-rationale` | yes | Evidence-based one sentence |

## Expected Output
```json
{
  "status": "ok",
  "worker": "codex",
  "task": "implement-auth-middleware",
  "scores": {"correctness": 4, "scope": 5, "quality": 3, "side_effects": 5},
  "rationales": {"correctness": "...", "scope": "...", "quality": "...", "side_effects": "..."},
  "composite": 4.25,
  "verdict": "PASS"
}
```

## Verdict Thresholds
- **PASS** — composite ≥ 3.5 and no dimension ≤ 2
- **FLAG** — composite ≥ 2.5 or any dimension = 2
- **FAIL** — composite < 2.5 or any dimension = 1

## On Return
Pass the full JSON to `log-agent-run` skill for audit logging.
Surface verdict to Claude per manager-posture rules (FLAG/FAIL require action).

## References
- `agents/agent-evaluator.md` — calls this skill
- `rules/01-manager-posture.md` — evaluation framework and fallback chain
- `skills/log-agent-run/` — called after this with the scores
