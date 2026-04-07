---
name: intent
description: Start a project or complex task by formally capturing intent. This is the entry point for all new project flows — run this before any planning, setup, or execution begins.
---

Walk through intent capture interactively. Do not rush — stay in this conversation until intent is unambiguous.

## Step 1 — Understand the Goal
Ask: "What are you trying to achieve?"
Listen for the actual outcome, not just the surface request.

## Step 2 — Define Success
Ask: "What does a successful outcome look like? How will you know it worked?"

## Step 3 — Define Scope Boundaries
Ask: "What is explicitly out of scope? What should I not touch or change?"

## Step 4 — Surface Assumptions
State any assumptions you're making. Ask the user to confirm or correct them.

## Step 5 — Confirm Intent Block
Output a structured intent summary and ask for confirmation:

```
INTENT CONFIRMED

Goal: {one sentence}
Success: {measurable outcome}
Out of scope: {explicit exclusions}
Assumptions: {list or "none"}
```

Do not proceed until the user confirms this block.

## Step 6 — Invoke Intent Auditor
Pass the user's original words + the confirmed intent block to intent-auditor.
If verdict is HOLD: surface the specific question and return to conversation.
If verdict is GO: proceed.

## Step 7 — Route to Project Setup
If this is a new project: run `skills/new-project/` with the confirmed intent block fields.
Pass --goal, --success, --out-of-scope from the confirmed intent. Ask user for --project-dir if not known.
Read the created CLAUDE.md back and confirm: "Local CLAUDE.md created at {path}. Adjust intelligence assignment if needed."

## Step 8 — Create Starter LOG.md
Create `{project-dir}/LOG.md` with empty structure:

```markdown
# Log — {Project Name}

## Active

## Archived
```

Confirm: "LOG.md created at {path}."
