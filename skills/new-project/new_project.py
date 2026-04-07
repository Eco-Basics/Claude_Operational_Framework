#!/usr/bin/env python3
"""
Skill: new-project
Purpose: Scaffold local CLAUDE.md for a new project from confirmed intent
Called by: /intent command after intent confirmation (step 6)
"""

import sys
import json
import pathlib
import argparse
from datetime import datetime

TEMPLATE = """\
# {project_name}
> Created: {date}

## Intent
**Goal:** {goal}
**Success:** {success}
**Out of scope:** {out_of_scope}

## Intelligence Assignment
DEFAULT: {default_worker}
CODE_IMPLEMENTATION: {code_worker}
RESEARCH: {research_worker}
DATA_PROCESSING: {data_worker}
EVALUATION: claude

## Stack
(fill in as established)

## State
Phase: setup
Last updated: {date}

## Notes
(running notes — updated each session per rules/05-session-discipline.md)
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Scaffold local CLAUDE.md')
    parser.add_argument('--project-dir', required=True, dest='project_dir')
    parser.add_argument('--project-name', required=True, dest='project_name')
    parser.add_argument('--goal', required=True)
    parser.add_argument('--success', required=True)
    parser.add_argument('--out-of-scope', required=True, dest='out_of_scope')
    parser.add_argument('--default-worker', default='claude', dest='default_worker')
    parser.add_argument('--code-worker', default='codex', dest='code_worker')
    parser.add_argument('--research-worker', default='claude', dest='research_worker')
    parser.add_argument('--data-worker', default='', dest='data_worker')
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        project_dir = pathlib.Path(args.project_dir)
        claude_md = project_dir / 'CLAUDE.md'

        if claude_md.exists():
            print(json.dumps({
                "status": "ok",
                "claude_md_path": str(claude_md),
                "project_name": args.project_name,
                "action": "skipped"
            }))
            sys.exit(0)

        project_dir.mkdir(parents=True, exist_ok=True)

        content = TEMPLATE.format(
            project_name=args.project_name,
            date=datetime.now().strftime('%Y-%m-%d'),
            goal=args.goal,
            success=args.success,
            out_of_scope=args.out_of_scope,
            default_worker=args.default_worker,
            code_worker=args.code_worker,
            research_worker=args.research_worker,
            data_worker=args.data_worker if args.data_worker else '(unassigned)',
        )

        claude_md.write_text(content, encoding='utf-8')

        print(json.dumps({
            "status": "ok",
            "claude_md_path": str(claude_md),
            "project_name": args.project_name,
            "action": "created"
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
