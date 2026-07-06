# Codex Plugin Port Design

## Goal

Add a Codex-ready distribution path for Harness without replacing the existing Claude Code plugin.
The port should let Codex discover and install Harness as a local plugin, then use a Codex-native
skill to design project harnesses.

## Approach

Use a repo-local Codex plugin under `plugins/harness-codex/`.

- Keep the current `.claude-plugin/` and `skills/harness/` files intact.
- Add `plugins/harness-codex/.codex-plugin/plugin.json`.
- Add `plugins/harness-codex/skills/harness/SKILL.md`.
- Add repo marketplace metadata at `.agents/plugins/marketplace.json`.
- Add a short Codex quickstart document.

This keeps the Claude Code package stable while giving Codex a native install surface.

## Codex Mapping

Claude Code concepts map to Codex concepts as follows:

- `.claude/skills/` -> `.agents/skills/`
- `CLAUDE.md` -> `AGENTS.md`
- `TeamCreate`, `SendMessage`, `TaskCreate` -> Codex subagents or file-based orchestration
- Claude Code plugin manifest -> Codex `.codex-plugin/plugin.json`

The Codex skill should describe team architecture as reusable project guidance and skill files.
It must not depend on Claude-only Agent Teams primitives.

## Output Contract

When the Codex Harness skill runs in a target project, it should create or update:

- `.agents/skills/<skill-name>/SKILL.md` for generated workflows
- `AGENTS.md` with a concise trigger pointer and change history
- `_workspace/` for intermediate analysis artifacts when needed

It may propose role-specific subagent prompts, but durable behavior should live in checked-in skills
and project guidance rather than only in a single prompt.

## Validation

Validate the plugin manifest and skill structure with Codex plugin and skill validation tools where
available. Also inspect trigger wording to make sure the Codex skill is clearly scoped to Harness
generation, updates, audits, and maintenance.
