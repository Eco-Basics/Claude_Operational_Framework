#!/usr/bin/env python3
"""
Skill: codex-output-validator
Purpose: Structural pre-check of Codex output before full rubric evaluation
Called by: Claude immediately after Codex returns output
"""

import sys
import json
import argparse
import pathlib
import re

LANGUAGE_MARKERS = {
    'python': [r'def ', r'import ', r'class ', r'#', r'if __name__'],
    'typescript': [r'const ', r'function ', r'interface ', r'export ', r'import '],
    'javascript': [r'const ', r'function ', r'var ', r'let ', r'=>'],
    'go': [r'func ', r'package ', r'import ', r'var '],
    'rust': [r'fn ', r'use ', r'let ', r'impl '],
    'java': [r'public ', r'class ', r'import ', r'void '],
    'bash': [r'#!/', r'echo ', r'if \[', r'function '],
}

TRUNCATION_MARKERS = [
    '...', '// TODO', '# TODO', '/* TODO', '[truncated]', '[cut off]', '// ...', '# ...'
]


def parse_args():
    parser = argparse.ArgumentParser(description='Validate Codex output structure')
    parser.add_argument('--spec', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--language', required=True)
    return parser.parse_args()


def load_output(output_str: str) -> str:
    p = pathlib.Path(output_str)
    if p.exists():
        return p.read_text(encoding='utf-8')
    return output_str


def main():
    args = parse_args()

    try:
        output_text = load_output(args.output)
        checks = {}
        issues = []

        # Check 1: non-empty
        checks['non_empty'] = bool(output_text.strip())
        if not checks['non_empty']:
            issues.append('Output is empty')

        # Check 2: has code (backtick blocks or language markers)
        has_code_blocks = '```' in output_text
        lang_markers = LANGUAGE_MARKERS.get(args.language.lower(), [])
        has_lang_markers = any(re.search(m, output_text) for m in lang_markers)
        checks['has_code'] = has_code_blocks or has_lang_markers
        if not checks['has_code']:
            issues.append(f'No recognizable {args.language} code patterns found')

        # Check 3: no obvious truncation
        checks['no_truncation'] = not any(marker in output_text for marker in TRUNCATION_MARKERS)
        if not checks['no_truncation']:
            issues.append('Output appears truncated or contains unimplemented placeholders')

        # Check 4: language matches (if we have known markers for this language)
        if lang_markers:
            checks['language_matches'] = has_lang_markers or has_code_blocks
            if not checks['language_matches']:
                issues.append(f'Output does not appear to be {args.language}')
        else:
            checks['language_matches'] = True

        # Verdict
        if not checks['non_empty'] or not checks['has_code']:
            verdict = 'FAIL'
        elif issues:
            verdict = 'FLAG'
        else:
            verdict = 'PASS'

        print(json.dumps({
            "status": "ok",
            "verdict": verdict,
            "checks": checks,
            "issues": issues
        }))
        sys.exit(0)

    except Exception as e:
        # Validator itself should not crash — degrade gracefully
        print(json.dumps({
            "status": "ok",
            "verdict": "FLAG",
            "checks": {},
            "issues": [f"Validator error: {str(e)}"]
        }))
        sys.exit(0)


if __name__ == '__main__':
    main()
