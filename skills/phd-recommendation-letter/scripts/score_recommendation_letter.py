#!/usr/bin/env python3
"""Heuristically score an academic recommendation letter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


GENERIC_PRAISE = [
    "hard-working",
    "hardworking",
    "smart",
    "excellent",
    "outstanding",
    "passionate",
    "diligent",
]


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    return sys.stdin.read()


def count_any(text: str, patterns: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(p.lower()) for p in patterns)


def score_letter(text: str) -> dict[str, object]:
    lowered = text.lower()
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    word_count = len(re.findall(r"\b\w+\b", text))

    has_relationship = any(
        phrase in lowered
        for phrase in ["supervised", "worked closely", "served as", "collaborated", "course"]
    )
    has_specific_episode = any(
        phrase in lowered
        for phrase in ["i remember", "for example", "one discussion", "when ", "during "]
    )
    has_comparison = any(
        phrase in lowered
        for phrase in ["one of the strongest", "top", "among the strongest", "comparable to"]
    )
    has_research = any(
        phrase in lowered
        for phrase in ["research question", "problem formulation", "failure", "evaluation", "method"]
    )
    direct_scope = any(
        phrase in lowered
        for phrase in ["according to his cv", "broader trajectory", "my evaluation is based"]
    )
    generic_count = count_any(text, GENERIC_PRAISE)
    repeated_judgment = lowered.count("research judgment")

    scores = {
        "recommender_credibility": min(10, 5 + 2 * has_relationship + 1 * direct_scope),
        "specificity": min(10, 4 + 3 * has_specific_episode + min(2, word_count // 300)),
        "research_potential": min(10, 5 + 3 * has_research + 1 * has_comparison),
        "authenticity": max(1, min(10, 8 - max(0, repeated_judgment - 2) - (1 if generic_count > 5 else 0))),
        "evidence_discipline": min(10, 6 + 2 * direct_scope + 1 * has_specific_episode),
    }
    overall = round(sum(scores.values()) / len(scores), 1)

    risks = []
    if not has_relationship:
        risks.append("Missing clear recommender-candidate relationship.")
    if not has_specific_episode:
        risks.append("Missing a concrete observed episode.")
    if generic_count > 5:
        risks.append("Too much generic praise without evidence.")
    if repeated_judgment > 3:
        risks.append("Overuses 'research judgment'.")
    if word_count < 350:
        risks.append("Likely too short for a strong PhD recommendation.")
    if word_count > 950:
        risks.append("Likely too long; consider tightening.")

    return {
        "overall": overall,
        "scores": scores,
        "word_count": word_count,
        "sentence_count": len([s for s in sentences if s.strip()]),
        "risks": risks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("letter", nargs="?", help="Letter text file. Reads stdin if omitted.")
    args = parser.parse_args()
    result = score_letter(read_input(args.letter))
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
