# Agents

Global roster. Project-specific workers are declared in local `CLAUDE.md`.

## Delegation Principle
Match task to the best available worker. Write a spec before dispatching. Evaluate output before using it or reporting it.

## Reporting
Surface agent work when the outcome is relevant or notable. A brief summary (worker, outcome, any flag) is sufficient — not required on every run. Use judgment.

## Global Agents

| Agent | Purpose | Invoke when |
|---|---|---|
| `intent-auditor` | Re-confirms intent coherence before execution | Before any high-stakes or multi-step task |
| `agent-evaluator` | Scores worker output on structured rubric | After any non-Claude worker run |
| `context-engineer` | Audits context window health | Sessions feel slow, or before adding new tools/agents |

## Task Spec Template
Before dispatching any worker:
```
WORKER: {name}
TASK: {one sentence}
INPUT: {what you're giving it}
OUTPUT: {exactly what you need back}
CONSTRAINTS: {what it must not do}
```

## Worker Profiles
Persistent performance data per model: `memory/worker-profiles/{model-name}.md`
Updated after audit runs or when a notable pattern emerges.
