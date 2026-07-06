# Codex Orchestrator Template

Use this template for generated orchestrator skills.

## Frontmatter

```markdown
---
name: <domain>-orchestrator
description: "Route and coordinate <domain> work. Use for <main triggers>, follow-ups such as rerun/update/fix, and multi-step workflows that require specialist skills."
---
```

## Required Sections

### Purpose

State the workflow this orchestrator coordinates and the architecture pattern.

### Phase 0: Context Check

Check:

- `git status --short`
- existing `_workspace/` artifacts
- relevant changed files or user-provided inputs
- whether this is initial run, follow-up, partial rerun, or maintenance

### Phase 1: Task Classification

Use a matrix:

| Trigger | Task Type | Specialist | Follow-up |
| --- | --- | --- | --- |
| <keywords> | <type> | <skill> | <next step> |

### Phase 2: Role Assignment

For subagent-capable sessions:

- assign independent work to subagents with clear role prompts
- require each subagent to write durable output under `_workspace/`

For file-handoff sessions:

- run specialist skills sequentially
- write `_workspace/<phase>_<role>_<artifact>.md`

### Phase 3: Integration

Read specialist artifacts, resolve conflicts, and synthesize the final output.

When findings conflict:

- preserve both sources
- state the conflict
- choose only when evidence supports the choice
- ask the user when a product decision is required

### Error Handling

Default rule:

- retry once when a specialist or command fails for an incidental reason
- if it fails again, continue only when the missing result is non-blocking
- report missing or skipped outputs explicitly
- never delete conflicting or partial artifacts silently

### Follow-up Behavior

Support:

- "rerun"
- "update"
- "fix only this part"
- "use previous result"
- "continue from workspace"

If `_workspace/` exists and the request is partial, reuse relevant artifacts instead of restarting.

### Verification

List commands and checks specific to the target project.

### Test Scenarios

Include:

- normal flow
- partial rerun
- error or ambiguity flow

## Data Handoff Convention

Use:

```text
_workspace/<phase>_<role>_<artifact>.md
```

Examples:

- `_workspace/01_researcher_sources.md`
- `_workspace/02_builder_plan.md`
- `_workspace/03_qa_findings.md`
- `_workspace/04_orchestrator_summary.md`

Final outputs may live outside `_workspace/` when they are user-facing deliverables.
