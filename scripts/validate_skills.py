#!/usr/bin/env python3
"""Validate harness skill metadata and reference links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "harness" / "SKILL.md"
REFS = ROOT / "skills" / "harness" / "references"


def validate_frontmatter(text: str) -> list[str]:
    errors: list[str] = []
    if not text.startswith("---"):
        return ["SKILL.md missing YAML frontmatter"]
    match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return ["SKILL.md has invalid frontmatter block"]
    frontmatter = match.group(1)
    if "name:" not in frontmatter:
        errors.append("frontmatter missing name")
    if "description:" not in frontmatter:
        errors.append("frontmatter missing description")
    return errors


def validate_references(text: str) -> list[str]:
    errors: list[str] = []
    for ref in re.findall(r"`(references/[^`]+)`", text):
        path = ROOT / "skills" / "harness" / ref
        if not path.exists():
            errors.append(f"broken reference link: {ref}")
    return errors


def main() -> int:
    errors: list[str] = []
    if not SKILL.exists():
        errors.append(f"missing {SKILL}")
    else:
        text = SKILL.read_text(encoding="utf-8")
        errors.extend(validate_frontmatter(text))
        errors.extend(validate_references(text))
        if len(text.splitlines()) > 520:
            errors.append("SKILL.md exceeds 520 lines (target <500)")

    if REFS.is_dir():
        for md in REFS.glob("*.md"):
            if len(md.read_text(encoding="utf-8").splitlines()) > 650:
                errors.append(f"{md.name} exceeds 650 lines")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print("validate_skills: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
