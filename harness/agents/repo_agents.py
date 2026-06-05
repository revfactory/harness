
"""Repository-specific agent implementations for the harness.

Each function receives (params, input_payload) and returns JSON-serializable findings.
"""
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)


def _read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        logger.debug("Failed to read file %s", path, exc_info=True)
        return None


def repo_inspector(params, input_payload):
    logger.debug("repo_inspector start")
    root = os.getcwd()
    files = sorted([f for f in os.listdir(root) if os.path.isfile(f)])
    dirs = sorted([d for d in os.listdir(root) if os.path.isdir(d)])
    important = {"README.md": os.path.exists("README.md"), "CHANGELOG.md": os.path.exists("CHANGELOG.md"), "LICENSE": os.path.exists("LICENSE")}
    return {"files": files, "dirs": dirs, "important": important, "timestamp": datetime.utcnow().isoformat()}


def dependency_checker(params, input_payload):
    logger.debug("dependency_checker start")
    roots = {"requirements.txt": os.path.exists("requirements.txt"), "package.json": os.path.exists("package.json"), "pyproject.toml": os.path.exists("pyproject.toml")}
    details = {}
    if roots.get("requirements.txt"):
        content = _read_file("requirements.txt") or ""
        details["requirements.txt"] = content[:200]
    if roots.get("package.json"):
        pj_text = _read_file("package.json") or "{}"
        try:
            details["package.json"] = json.loads(pj_text)
        except Exception:
            logger.debug("package.json parse failed", exc_info=True)
            details["package.json"] = {}
    return {"manifests": roots, "details_preview": details, "timestamp": datetime.utcnow().isoformat()}


def changelog_auditor(params, input_payload):
    logger.debug("changelog_auditor start")
    text = _read_file("CHANGELOG.md")
    if not text:
        return {"found": False, "issues": ["CHANGELOG.md missing"], "timestamp": datetime.utcnow().isoformat()}
    recent_lines = text.strip().splitlines()[:20]
    return {"found": True, "recent_preview": "\n".join(recent_lines), "timestamp": datetime.utcnow().isoformat()}


def docs_checker(params, input_payload):
    logger.debug("docs_checker start")
    docs = {}
    check_files = ["docs/quickstart.md", "docs/experimental-dependency.md", "README.md", "privacy.html"]
    for p in check_files:
        docs[p] = os.path.exists(p)
    todos = []
    if os.path.isdir("docs"):
        for root, _, files in os.walk("docs"):
            for f in files:
                path = os.path.join(root, f)
                content = _read_file(path) or ""
                if "TODO" in content:
                    todos.append({"file": path, "snippet": content[:120]})
    return {"checks": docs, "todos": todos, "timestamp": datetime.utcnow().isoformat()}


def release_planner(params, input_payload):
    logger.debug("release_planner start")
    history = input_payload.get("history", [])
    issues = []
    for h in history:
        r = h.get("result", {})
        if isinstance(r, dict) and r.get("issues"):
            issues.extend(r.get("issues"))
    plan = ["bump-version", "update-changelog", "run-tests", "publish"]
    if issues:
        plan.insert(0, "address-issues")
    return {"plan": plan, "issues": issues, "timestamp": datetime.utcnow().isoformat()}


def local_tester(params, input_payload):
    logger.debug("local_tester start")
    hints = {"has_pytest": False, "has_test_script": False}
    if os.path.exists("requirements.txt"):
        req = _read_file("requirements.txt") or ""
        hints["has_pytest"] = "pytest" in req
    if os.path.exists("package.json"):
        try:
            pj = json.loads(_read_file("package.json") or "{}")
            scripts = pj.get("scripts", {})
            hints["has_test_script"] = "test" in scripts
        except Exception:
            logger.debug("package.json parse failed in local_tester", exc_info=True)
    return {"hints": hints, "timestamp": datetime.utcnow().isoformat()}
