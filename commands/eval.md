---
name: eval
description: Toggle execution lockout for this session. In eval mode Claude is an absolute manager — delegates only, never executes. No fallback self-execution.
---

When invoked:
- Confirm: "EVAL mode active. Delegation only — no execution this session."
- Remain in this state until user runs /eval again or starts a new session.

## What Claude Can Do in EVAL
- Read, observe, assess, reason
- Invoke: agent-evaluator, intent-auditor, context-engineer
- Delegate tasks to declared workers via task spec
- Report outcomes, surface patterns, make recommendations

## What Claude Cannot Do in EVAL
- Write, Edit, Bash, or any tool that modifies state
- Self-execute as a fallback when a worker fails
- Dispatch any worker not declared in the project intelligence assignment

## When a Worker Fails in EVAL
Report the failure clearly: worker used, task, what failed, score.
Do not attempt to fix it. Do not self-execute.
State: "Worker failed. Exit EVAL mode to execute directly, or reassign to another declared worker."

## Exiting EVAL
Run /eval again to toggle off, or start a new session.
