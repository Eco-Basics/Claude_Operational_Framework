#!/usr/bin/env python3
"""
Skill: codex-spec-formatter
Purpose: Convert raw task description into Codex-optimal structured prompt spec
Called by: Claude before any Codex invocation
"""

import sys
import json
import argparse

SPEC_TEMPLATE = """\
## Task
{task}

## Language / Framework
- Language: {language}
- Framework: {framework}

## Output Requirements
{output_format}

## Constraints
{constraints}

## Explicitly Out of Scope
{exclusions}

## Instructions
- Implement only what is described above
- Do not add features, refactor surrounding code, or improve things not mentioned
- Return only code and inline comments — no prose explanations
- If something is ambiguous, implement the simpler interpretation
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Format Codex task spec')
    parser.add_argument('--task', required=True)
    parser.add_argument('--language', required=True)
    parser.add_argument('--output-format', required=True, dest='output_format')
    parser.add_argument('--framework', default='none')
    parser.add_argument('--constraints', default='none')
    parser.add_argument('--exclusions', default='none')
    return parser.parse_args()


def format_list(value: str) -> str:
    if value.lower() == 'none':
        return '- none'
    return '\n'.join(f'- {item.strip()}' for item in value.split(','))


def main():
    args = parse_args()

    try:
        spec = SPEC_TEMPLATE.format(
            task=args.task,
            language=args.language,
            framework=args.framework,
            output_format=args.output_format,
            constraints=format_list(args.constraints),
            exclusions=format_list(args.exclusions),
        ).strip()

        print(json.dumps({
            "status": "ok",
            "spec": spec,
            "word_count": len(spec.split())
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
