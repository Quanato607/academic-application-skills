#!/usr/bin/env python3
"""Extract a lightweight academic profile from CV text or PDF.

The script is intentionally heuristic. It creates an evidence ledger that an
agent can refine, not an authoritative parser.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_PATTERNS = {
    "education": r"(?i)\bEducation\b",
    "experience": r"(?i)\b(Experience|Research Experience|Work Experience)\b",
    "publications": r"(?i)\b(Publication|Publications|Selected Publications)\b",
    "awards": r"(?i)\b(Honors|Awards|Honors & Awards)\b",
    "skills": r"(?i)\b(Technical Skills|Skills)\b",
}

STATUS_WORDS = [
    "accepted",
    "published",
    "under review",
    "submitted",
    "transferred",
    "oral",
    "spotlight",
    "findings",
]


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception as exc:  # pragma: no cover - depends on environment
            raise SystemExit(
                "PDF parsing requires pypdf. Install it or provide CV text."
            ) from exc
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def compact_lines(text: str) -> list[str]:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return [line for line in lines if line]


def find_identity(lines: list[str]) -> dict[str, str]:
    email = ""
    phone = ""
    name = lines[0] if lines else ""
    joined = "\n".join(lines[:20])
    email_match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", joined)
    phone_match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", joined)
    if email_match:
        email = email_match.group(0)
    if phone_match:
        phone = phone_match.group(1)
    return {"name": name, "email": email, "phone": phone}


def extract_publications(lines: list[str]) -> list[dict[str, object]]:
    pubs: list[dict[str, object]] = []
    venue_hint = re.compile(
        r"(?i)\b(CVPR|ICCV|ECCV|SIGGRAPH|NeurIPS|ICLR|ICML|ACL|EMNLP|NAACL|"
        r"AAAI|IJCAI|KDD|WWW|SIGIR|CHI|CSCW|UIST|VLDB|SIGMOD|ICSE|FSE|"
        r"OSDI|SOSP|NSDI|CCS|USENIX|MICCAI|ISBI|ICASSP|IEEE|ACM|AAAS|"
        r"Nature|Science|Cell|PNAS|Lancet|NEJM|JAMA|BMJ|AER|QJE|JPE|"
        r"APSR|ASR|MLA|arXiv|Findings|Journal|Transactions|Proceedings|"
        r"Conference|Workshop|Information Fusion)\b"
    )
    role_hint = re.compile(r"(?i)\b(first author|co-first|second author|corresponding author)\b")
    for line in lines:
        if venue_hint.search(line) or role_hint.search(line):
            has_year = bool(re.search(r"\b(19|20)\d{2}\b", line))
            statuses = [word for word in STATUS_WORDS if word.lower() in line.lower()]
            if not (statuses or role_hint.search(line) or has_year):
                continue
            pubs.append(
                {
                    "text": line,
                    "roles": role_hint.findall(line),
                    "statuses": statuses,
                    "needs_status_check": any(
                        word in statuses for word in ["under review", "submitted", "transferred"]
                    ),
                }
            )
    return pubs


def extract_keywords(lines: list[str]) -> list[str]:
    keywords = []
    vocab = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "data science",
        "computer vision",
        "natural language processing",
        "reinforcement learning",
        "agent",
        "tool use",
        "dialogue",
        "multimodal",
        "knowledge distillation",
        "missing-modality",
        "robotics",
        "hci",
        "systems",
        "security",
        "theory",
        "optimization",
        "statistics",
        "bioinformatics",
        "biology",
        "medical",
        "public health",
        "neuroscience",
        "neuroimaging",
        "brain",
        "economics",
        "education",
        "psychology",
        "sociology",
        "political science",
        "social science",
        "humanities",
        "history",
        "literature",
    ]
    text = "\n".join(lines).lower()
    for word in vocab:
        if word in text:
            keywords.append(word)
    return keywords


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cv", type=Path, help="CV PDF or text file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    text = read_text(args.cv)
    lines = compact_lines(text)
    profile = {
        "identity": find_identity(lines),
        "keywords": extract_keywords(lines),
        "publications": extract_publications(lines),
        "conflict_flags": [],
    }
    for pub in profile["publications"]:
        if pub.get("needs_status_check"):
            profile["conflict_flags"].append(pub["text"])

    json.dump(profile, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
