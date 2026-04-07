---
name: audit
description: Review agent logs for the current period, surface worker performance patterns, and propose concrete changes to rules, worker profiles, or intelligence assignments.
---

Read all files in `agent-logs/YYYY-MM/` for the current month.
Invoke agent-evaluator to synthesize patterns across runs.

Report in sequence:
1. **Worker performance summary** — scores by worker and task type
2. **Failure patterns** — recurring FAILs or FLAGs and their root causes
3. **Adaptation attempts** — which prompting/spec changes worked, which didn't
4. **Concrete proposals** — specific file changes to rules, worker profiles, or intelligence assignments

Present each proposal individually. Wait for explicit approval before writing any change.
Commit all approved changes together and push.
