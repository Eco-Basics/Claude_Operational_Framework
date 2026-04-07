#!/usr/bin/env python3
"""
Skill: evaluator-rubric-scorer
Purpose: Aggregate 4-dimension rubric scores and produce structured verdict
Called by: agent-evaluator agent after reviewing worker output
"""

import sys
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Aggregate rubric scores and produce verdict')
    parser.add_argument('--worker', required=True)
    parser.add_argument('--task', required=True)
    parser.add_argument('--correctness', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--correctness-rationale', required=True, dest='correctness_rationale')
    parser.add_argument('--scope', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--scope-rationale', required=True, dest='scope_rationale')
    parser.add_argument('--quality', type=int, required=True, choices=range(1, 6), metavar='1-5')
    parser.add_argument('--quality-rationale', required=True, dest='quality_rationale')
    parser.add_argument('--side-effects', type=int, required=True, choices=range(1, 6), metavar='1-5', dest='side_effects')
    parser.add_argument('--side-effects-rationale', required=True, dest='side_effects_rationale')
    return parser.parse_args()


def compute_verdict(composite: float, scores: dict) -> str:
    min_score = min(scores.values())
    if min_score == 1 or composite < 2.5:
        return 'FAIL'
    if min_score == 2 or composite < 3.5:
        return 'FLAG'
    return 'PASS'


def main():
    args = parse_args()

    try:
        scores = {
            'correctness': args.correctness,
            'scope': args.scope,
            'quality': args.quality,
            'side_effects': args.side_effects,
        }
        rationales = {
            'correctness': args.correctness_rationale,
            'scope': args.scope_rationale,
            'quality': args.quality_rationale,
            'side_effects': args.side_effects_rationale,
        }

        composite = round(sum(scores.values()) / 4, 2)
        verdict = compute_verdict(composite, scores)

        print(json.dumps({
            "status": "ok",
            "worker": args.worker,
            "task": args.task,
            "scores": scores,
            "rationales": rationales,
            "composite": composite,
            "verdict": verdict,
        }))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
