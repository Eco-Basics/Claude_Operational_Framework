#!/usr/bin/env python3
"""
Skill: onboard-worker
Purpose: Create initial worker profile stub for a new LLM model
Called by: Claude when a new worker is declared in a project's local CLAUDE.md
"""

import sys
import json
import pathlib
import argparse
from datetime import datetime

CLAUDE_HOME = pathlib.Path.home() / '.claude'
PROFILES_DIR = CLAUDE_HOME / 'memory' / 'worker-profiles'

INVOCATION_MAP = {
    'codex': 'Agent tool, subagent_type: "codex:codex-rescue"',
    'ollama': 'Bash: ollama run {model} "{prompt}"',
    'bash': 'Bash: custom shell command',
    'agent': 'Agent tool with subagent_type',
}

PROFILE_TEMPLATE = """\
# Worker Profile: {model}
> Created: {date}

## Invocation Method
{invocation_detail}

## Best-Fit Tasks
{task_types}

## Effective Prompting Patterns
(none recorded yet — update after first use)

## Known Failure Modes
(none recorded yet)

## Spec Format Notes
(quirks, required fields, or constraints — update as discovered)

## Performance Log
(entries added by update-worker-profile skill after audits and degradation events)
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Create worker profile stub')
    parser.add_argument('--model', required=True)
    parser.add_argument('--invocation', required=True, choices=['codex', 'ollama', 'bash', 'agent'])
    parser.add_argument('--task-types', required=True, dest='task_types')
    parser.add_argument('--notes', default='none')
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        profile_path = PROFILES_DIR / f"{args.model}.md"

        if profile_path.exists():
            print(json.dumps({
                "status": "ok",
                "profile_path": str(profile_path),
                "action": "already_exists"
            }))
            sys.exit(0)

        invocation_detail = INVOCATION_MAP.get(args.invocation, args.invocation)
        task_lines = '\n'.join(f'- {t.strip()}' for t in args.task_types.split(','))

        content = PROFILE_TEMPLATE.format(
            model=args.model,
            date=datetime.now().strftime('%Y-%m-%d'),
            invocation_detail=invocation_detail,
            task_types=task_lines,
        )

        if args.notes.lower() != 'none':
            content += f"\n## Initial Notes\n{args.notes}\n"

        profile_path.write_text(content, encoding='utf-8')

        print(json.dumps({
            "status": "ok",
            "profile_path": str(profile_path),
            "action": "created"
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
