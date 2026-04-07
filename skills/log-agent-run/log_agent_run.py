#!/usr/bin/env python3
"""
Skill: log-agent-run
Purpose: Write a standardized agent run log after any worker invocation.
Called by: Claude (post-worker, per rules/01-manager-posture.md)
"""

import sys
import json
import pathlib
import argparse
import re
from datetime import datetime

CLAUDE_HOME = pathlib.Path.home() / '.claude'


def parse_args():
    parser = argparse.ArgumentParser(description='Log an agent run to agent-logs/')
    parser.add_argument('--worker', required=True, help='Worker/model name')
    parser.add_argument('--task', required=True, help='Task in one sentence')
    parser.add_argument('--spec', required=True, help='Key constraints given to worker')
    parser.add_argument('--output', required=True, help='Output summary (2-3 sentences)')
    parser.add_argument('--correctness', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--scope', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--quality', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--side-effects', type=int, required=True, choices=range(1, 6), metavar='1-5', dest='side_effects')
    parser.add_argument('--adaptations', default='none', help='Prompting/spec changes attempted')
    parser.add_argument('--flags', default='none', help='Anomalies or notable failures')
    return parser.parse_args()


def slugify(text: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower())
    return slug.strip('-')[:40]


def main():
    args = parse_args()

    try:
        now = datetime.now()
        month_dir = CLAUDE_HOME / 'agent-logs' / now.strftime('%Y-%m')
        month_dir.mkdir(parents=True, exist_ok=True)

        task_slug = slugify(args.task)
        filename = f"{now.strftime('%Y-%m-%d')}-{args.worker}-{task_slug}.md"
        log_path = month_dir / filename

        composite = round(
            (args.correctness + args.scope + args.quality + args.side_effects) / 4, 1
        )

        content = (
            f"DATE: {now.strftime('%Y-%m-%d')}\n"
            f"WORKER: {args.worker}\n"
            f"TASK: {args.task}\n"
            f"SPEC SUMMARY: {args.spec}\n"
            f"OUTPUT SUMMARY: {args.output}\n"
            f"SCORES: Correctness={args.correctness} Scope={args.scope} "
            f"Quality={args.quality} SideEffects={args.side_effects}\n"
            f"COMPOSITE: {composite}/5\n"
            f"ADAPTATIONS: {args.adaptations}\n"
            f"FLAGS: {args.flags}\n"
        )

        log_path.write_text(content, encoding='utf-8')

        needs_attention = composite <= 2.0 or args.flags.lower() != 'none'

        print(json.dumps({
            "status": "ok",
            "log_path": str(log_path),
            "composite_score": composite,
            "needs_attention": needs_attention
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
