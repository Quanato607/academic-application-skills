#!/usr/bin/env python3
"""Build a simple advisor fit matrix from structured JSON inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def overlap_score(candidate_terms: list[str], advisor_terms: list[str]) -> float:
    c = {term.lower() for term in candidate_terms}
    a = {term.lower() for term in advisor_terms}
    if not c or not a:
        return 0.0
    return len(c & a) / max(1, min(len(c), len(a)))


def fit_label(score: float) -> str:
    if score >= 0.6:
        return "direct fit"
    if score >= 0.35:
        return "strong adjacent fit"
    if score >= 0.15:
        return "adjacent fit"
    if score > 0:
        return "weak fit"
    return "unknown or no clear fit"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True, help="Candidate JSON profile")
    parser.add_argument("--advisor", type=Path, required=True, help="Advisor JSON profile")
    args = parser.parse_args()

    candidate = load_json(args.candidate)
    advisor = load_json(args.advisor)
    candidate_terms = candidate.get("keywords", []) + candidate.get("topics", [])
    advisor_terms = advisor.get("topics", []) + advisor.get("methods", []) + advisor.get("domains", [])
    score = overlap_score(candidate_terms, advisor_terms)

    result = {
        "advisor": advisor.get("name", ""),
        "institution": advisor.get("institution", ""),
        "fit_score": round(score * 5, 1),
        "fit_label": fit_label(score),
        "entry_path": advisor.get("entry_path", "unknown"),
        "hook": advisor.get("hook", ""),
        "candidate_angle": candidate.get("angle", ""),
        "risks": advisor.get("risks", []),
        "sources": advisor.get("sources", []),
    }
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
