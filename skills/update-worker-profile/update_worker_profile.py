#!/usr/bin/env python3
"""
Skill: update-worker-profile
Purpose: Append a performance entry to memory/worker-profiles/{model}.md
Called by: Claude post-audit or when worker degradation triggers
"""

import sys
import json
import pathlib
import argparse
from datetime import datetime

CLAUDE_HOME = pathlib.Path.home() / '.claude'
PROFILES_DIR = CLAUDE_HOME / 'memory' / 'worker-profiles'

PROFILE_TEMPLATE = """\
# Worker Profile: {model}
> Created: {date}

## Best-Fit Tasks
{task_types}

## Effective Prompting Patterns
(none recorded yet — update after first use)

## Known Failure Modes
(none recorded yet)

## Spec Format Notes
(quirks, required fields, or constraints — update as discovered)

## Performance Log
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Update worker profile')
    parser.add_argument('--model', required=True)
    parser.add_argument('--event', required=True, choices=['audit', 'degradation', 'adaptation'])
    parser.add_argument('--task-types', required=True, dest='task_types')
    parser.add_argument('--composite', type=float, required=True)
    parser.add_argument('--notes', required=True)
    parser.add_argument('--decision', required=True, choices=['keep', 'reassign', 'drop', 'adapt'])
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        profile_path = PROFILES_DIR / f"{args.model}.md"

        if not profile_path.exists():
            task_lines = '\n'.join(f'- {t.strip()}' for t in args.task_types.split(','))
            profile_path.write_text(
                PROFILE_TEMPLATE.format(
                    model=args.model,
                    date=datetime.now().strftime('%Y-%m-%d'),
                    task_types=task_lines,
                ),
                encoding='utf-8'
            )
            action = 'created'
        else:
            action = 'updated'

        entry = (
            f"\n### {datetime.now().strftime('%Y-%m-%d')} — {args.event.upper()}\n"
            f"- Composite: {args.composite}/5\n"
            f"- Task types: {args.task_types}\n"
            f"- Notes: {args.notes}\n"
            f"- Decision: {args.decision}\n"
        )

        with profile_path.open('a', encoding='utf-8') as f:
            f.write(entry)

        print(json.dumps({
            "status": "ok",
            "profile_path": str(profile_path),
            "action": action
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
