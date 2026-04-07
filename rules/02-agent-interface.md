# Universal Agent Interface

## Principle
Every worker — regardless of which LLM or tool — is invoked through the same management protocol.
Claude's layer stays constant even as the worker underneath changes.

## Worker Invocation by Type

### Claude Subagents
Tool: `Agent` with `subagent_type`
Examples: `intent-auditor`, `agent-evaluator`, `gsd-planner`

### Codex (OpenAI)
Tool: `Agent`, `subagent_type: "codex:codex-rescue"`
Best for: code implementation >3 files or >30 lines
Spec must include: language, framework, explicit output structure, what NOT to do

### Local LLMs via Ollama
Tool: `Bash` — `ollama run {model} "{prompt}"`
Or HTTP: `curl http://localhost:11434/api/generate -d '{"model":"{model}","prompt":"{prompt}"}'`
Best for: research summarization, classification, data processing

### New Workers
When onboarding a new model: add a section here. Define invocation method, best-fit tasks, spec format quirks.

## Post-Run Log
After every non-Claude worker run, write to `agent-logs/YYYY-MM/YYYY-MM-DD-{worker}-{task-slug}.md`:
- Spec used
- Output summary (2-3 sentences)
- 4-dimension score
- Any anomalies or drift from spec
