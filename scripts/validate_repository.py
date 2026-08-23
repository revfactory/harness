#!/usr/bin/env python3
"""Validate the Harness repository's publishable plugin and skill assets.

This deliberately avoids strict Markdown style linting. The repository has a
large amount of existing long-form/localized Markdown, so this gate focuses on
trust checks that are stable and non-invasive for incoming PRs:

- required plugin/skill files are present
- JSON manifests parse and contain expected metadata
- the Harness skill has basic frontmatter and all backtick reference paths exist
- relative Markdown link/image warnings surface existing missing local files
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "skills/harness/SKILL.md",
]

REQUIRED_PLUGIN_FIELDS = [
    "name",
    "description",
    "version",
    "author",
    "homepage",
    "repository",
    "license",
]
REFERENCE_RE = re.compile(r"`(references/[^`\n]+)`")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{rel(path)} is invalid JSON: {exc}")
    except OSError as exc:
        fail(errors, f"{rel(path)} cannot be read: {exc}")
    return {}


def validate_required_files(errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file():
            fail(errors, f"missing required file: {name}")


def validate_plugin_manifests(errors: list[str]) -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    if not plugin_path.is_file() or not marketplace_path.is_file():
        return

    plugin = load_json(plugin_path, errors)
    marketplace = load_json(marketplace_path, errors)
    if not plugin or not marketplace:
        return

    for field in REQUIRED_PLUGIN_FIELDS:
        if not plugin.get(field):
            fail(errors, f"plugin.json missing required field: {field}")

    if plugin.get("name") != "harness":
        fail(errors, "plugin.json name must be 'harness'")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail(errors, "marketplace.json must contain at least one plugin entry")
        return

    harness_entries = [entry for entry in plugins if entry.get("name") == "harness"]
    if not harness_entries:
        fail(errors, "marketplace.json missing plugin entry named 'harness'")
        return

    entry = harness_entries[0]
    if entry.get("version") != plugin.get("version"):
        fail(errors, "marketplace harness version must match plugin.json version")
    if entry.get("source") != "./":
        fail(errors, "marketplace harness source must be './'")


def validate_skill(errors: list[str]) -> None:
    skill_path = ROOT / "skills" / "harness" / "SKILL.md"
    if not skill_path.is_file():
        return

    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, "skills/harness/SKILL.md missing YAML frontmatter")
    else:
        frontmatter_end = text.find("\n---", 4)
        if frontmatter_end == -1:
            fail(errors, "skills/harness/SKILL.md frontmatter is not closed")
        else:
            frontmatter = text[4:frontmatter_end]
            for field in ("name:", "description:"):
                if field not in frontmatter:
                    fail(errors, f"skills/harness/SKILL.md frontmatter missing {field}")

    for ref in REFERENCE_RE.findall(text):
        target = ROOT / "skills" / "harness" / ref
        if not target.is_file():
            fail(errors, f"broken harness skill reference: {ref}")


def should_skip_link(raw_url: str) -> bool:
    raw_url = raw_url.strip()
    if not raw_url or raw_url == "#" or raw_url.startswith("#"):
        return True
    parsed = urlparse(raw_url)
    return bool(parsed.scheme or parsed.netloc)


def validate_markdown_links(warnings: list[str]) -> None:
    for md in ROOT.rglob("*.md"):
        if any(part in {".git", "node_modules"} for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        for raw_url in MARKDOWN_LINK_RE.findall(text):
            if should_skip_link(raw_url):
                continue
            clean = raw_url.split("#", 1)[0]
            clean = clean.split("?", 1)[0]
            clean = unquote(clean).strip()
            if not clean:
                continue
            target = (md.parent / clean).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not target.exists():
                warnings.append(f"{rel(md)} links to missing local path: {raw_url}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    validate_required_files(errors)
    validate_plugin_manifests(errors)
    validate_skill(errors)
    validate_markdown_links(warnings)

    if warnings:
        print("Repository validation warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"- {warning}", file=sys.stderr)

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
