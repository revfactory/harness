# Codex Quickstart

This repository now includes a Codex-ready Harness plugin alongside the original Claude Code plugin.
The Codex port lives at `plugins/harness-codex/` and is exposed through the repo-local marketplace
at `.agents/plugins/marketplace.json`.

## License

Harness is licensed under Apache-2.0. The Codex plugin keeps the same license metadata and includes
a copy of the license at `plugins/harness-codex/LICENSE` so the plugin can be redistributed with the
required license text.

## Install Locally

1. Open this repository in Codex.
2. Restart Codex or refresh the plugin directory so the repo-local marketplace is discovered.
3. In the plugin directory, choose the `Harness Local` marketplace.
4. Install `harness-codex`.

## Use

Invoke the bundled skill explicitly:

```text
$harness Build a Codex harness for this project.
```

You can also use natural prompts such as:

```text
Build a Codex harness for a documentation review workflow.
Design a skill-based agent workflow for this repository.
Audit and improve the existing Codex harness.
```

## Generated Outputs

The Codex port generates Codex-native files:

- `.agents/skills/<name>/SKILL.md`
- `AGENTS.md`
- `_workspace/<phase>_<role>_<artifact>.md`

The skill may use Codex subagents when available. If subagents are not available, it coordinates
roles through file-based handoffs in `_workspace/`.
