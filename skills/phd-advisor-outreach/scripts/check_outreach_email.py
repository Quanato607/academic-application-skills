#!/usr/bin/env python3
"""Check whether an academic outreach email is targeted and concise."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


GENERIC_PHRASES = [
    "your esteemed university",
    "your prestigious lab",
    "renowned professor",
    "perfect fit",
    "i have read all your papers",
    "i am very interested in your research",
]


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email", nargs="?", help="Email text file. Reads stdin if omitted.")
    args = parser.parse_args()
    text = read_input(args.email)
    lowered = text.lower()
    words = re.findall(r"\b\w+\b", text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    risks = []
    if len(words) > 280:
        risks.append("Email is longer than the default 180-260 word target.")
    if len(words) < 120:
        risks.append("Email may be too short to establish fit.")
    if any(phrase in lowered for phrase in GENERIC_PHRASES):
        risks.append("Contains generic praise or overclaiming.")
    if not re.search(r"\b(CV|resume|attached|application|PhD|RA|intern|visiting)\b", text):
        risks.append("Application goal or CV attachment is unclear.")
    if not re.search(r"\b(recent|paper|work|project|lab|study|article)\b", lowered):
        risks.append("No clear advisor-specific research hook detected.")
    if len(paragraphs) > 5:
        risks.append("Too many paragraphs for a cold outreach email.")

    result = {
        "word_count": len(words),
        "paragraph_count": len(paragraphs),
        "passes_basic_check": not risks,
        "risks": risks,
    }
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
