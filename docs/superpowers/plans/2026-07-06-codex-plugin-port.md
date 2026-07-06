# Codex Plugin Port Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repo-local Codex plugin package for Harness while preserving the existing Claude Code plugin.

**Architecture:** Create a new `plugins/harness-codex/` plugin containing one Codex-native Harness skill. Expose it through a repo-local `.agents/plugins/marketplace.json` and document installation in `docs/codex-quickstart.md`.

**Tech Stack:** Codex plugin manifest JSON, Agent Skills Markdown, repo-local Codex marketplace metadata.

---

### Task 1: Codex Plugin Manifest

**Files:**
- Create: `plugins/harness-codex/.codex-plugin/plugin.json`

- [ ] **Step 1: Create the manifest**

Create a minimal Codex plugin manifest that points to the bundled skills directory:

```json
{
  "name": "harness-codex",
  "version": "1.2.0",
  "description": "Codex-ready Harness port that designs project-specific skill and guidance harnesses without Claude Code Agent Teams primitives.",
  "skills": "./skills/"
}
```

- [ ] **Step 2: Inspect the manifest**

Run: `Get-Content -LiteralPath plugins\harness-codex\.codex-plugin\plugin.json`

Expected: Valid JSON with `name`, `version`, `description`, and `skills`.

### Task 2: Codex Harness Skill

**Files:**
- Create: `plugins/harness-codex/skills/harness/SKILL.md`

- [ ] **Step 1: Write Codex-native skill instructions**

Create a skill named `harness` with a trigger description covering harness generation, updates, audits, and Codex porting.

The skill body must instruct Codex to:

- Audit existing `.agents/skills`, `AGENTS.md`, and `_workspace`.
- Choose one of six team architecture patterns.
- Generate durable `.agents/skills/<name>/SKILL.md` files.
- Add only a concise pointer and change history to `AGENTS.md`.
- Use Codex subagents or file-based orchestration instead of Claude-only `TeamCreate`, `SendMessage`, and `TaskCreate`.

- [ ] **Step 2: Inspect trigger wording**

Run: `Select-String -LiteralPath plugins\harness-codex\skills\harness\SKILL.md -Pattern "TeamCreate|SendMessage|TaskCreate|.agents|AGENTS.md"`

Expected: The Claude-only primitives appear only as things to avoid or translate.

### Task 3: Repo Marketplace

**Files:**
- Create: `.agents/plugins/marketplace.json`

- [ ] **Step 1: Add marketplace entry**

Create a repo-local marketplace pointing to the plugin:

```json
{
  "name": "harness-local",
  "interface": {
    "displayName": "Harness Local"
  },
  "plugins": [
    {
      "name": "harness-codex",
      "source": {
        "source": "local",
        "path": "./plugins/harness-codex"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

- [ ] **Step 2: Inspect marketplace JSON**

Run: `Get-Content -LiteralPath .agents\plugins\marketplace.json`

Expected: Entry includes `policy.installation`, `policy.authentication`, and `category`.

### Task 4: Codex Quickstart

**Files:**
- Create: `docs/codex-quickstart.md`

- [ ] **Step 1: Document local installation and usage**

Document that this repo now contains a Codex plugin at `plugins/harness-codex`, exposed by `.agents/plugins/marketplace.json`.

Include:

- Restart Codex or refresh plugins after adding the repo.
- Install `harness-codex` from the `Harness Local` marketplace.
- Invoke with `$harness` or prompts like "Build a Codex harness for this project".
- Generated project outputs use `.agents/skills`, `AGENTS.md`, and `_workspace`.

- [ ] **Step 2: Inspect docs for stale Claude-only instructions**

Run: `Select-String -LiteralPath docs\codex-quickstart.md -Pattern ".claude|TeamCreate|CLAUDE.md"`

Expected: No matches.

### Task 5: Validation

**Files:**
- Validate: `plugins/harness-codex/.codex-plugin/plugin.json`
- Validate: `plugins/harness-codex/skills/harness/SKILL.md`
- Validate: `.agents/plugins/marketplace.json`

- [ ] **Step 1: Run plugin validation**

Run: `python C:\Users\splion\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py plugins\harness-codex`

Expected: Validation passes.

- [ ] **Step 2: Run skill validation**

Run: `python C:\Users\splion\.codex\skills\.system\skill-creator\scripts\quick_validate.py plugins\harness-codex\skills\harness`

Expected: Validation passes.

- [ ] **Step 3: Check git diff**

Run: `git diff -- docs/superpowers/specs/2026-07-06-codex-plugin-port-design.md docs/superpowers/plans/2026-07-06-codex-plugin-port.md plugins/harness-codex .agents/plugins/marketplace.json docs/codex-quickstart.md`

Expected: Diff contains only Codex port additions.
