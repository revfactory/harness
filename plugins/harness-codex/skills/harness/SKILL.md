---
name: harness
description: "Design, create, audit, update, or maintain a Codex-native project harness: generate Agent Skills under .agents/skills, concise AGENTS.md trigger guidance, _workspace artifacts, role workflows, and architecture patterns from a domain or project description. Use when the user asks to build a harness, design an agent team/workflow, port a Claude Code harness to Codex, improve an existing harness, or coordinate specialist roles in Codex without Claude Code Agent Teams."
---

# Harness for Codex

Harness turns a project or domain description into durable Codex working structure:

- Agent Skills in `.agents/skills/`
- concise project guidance in `AGENTS.md`
- intermediate artifacts in `_workspace/`
- role workflows that Codex can execute with subagents when available, or file-based orchestration when not

This is a Codex port of Harness and is distributed under Apache-2.0. Preserve the repository license
and attribution when copying, modifying, or redistributing generated plugin files.

## Core Rules

1. Generate durable files. Do not leave the harness only in a chat response.
2. Prefer Codex-native surfaces: `.agents/skills/`, `AGENTS.md`, `_workspace/`, Codex subagents, plans, and verification steps.
3. Do not require Claude Code-only primitives such as `TeamCreate`, `SendMessage`, or `TaskCreate`.
4. Keep `AGENTS.md` short: add only trigger rules, scope notes, and a change history.
5. Put detailed workflow instructions in generated skills, not in `AGENTS.md`.
6. Before adding a new skill, inspect existing `.agents/skills/` entries to avoid duplicates.
7. Treat a harness as evolving infrastructure. When updating it, audit current skills and guidance first.

## Workflow

### Phase 0: Audit Existing Harness

Read the target project for:

- `.agents/skills/`
- `AGENTS.md`
- `_workspace/`
- relevant README or domain docs

Classify the request:

- **New harness:** no matching skills or guidance exist.
- **Extension:** existing harness exists, and the user wants new roles, domains, or workflow steps.
- **Maintenance:** user asks to audit, fix, simplify, sync, or evolve an existing harness.

Report the classification briefly before writing files.

### Phase 1: Domain Analysis

Identify:

- the project/domain goal
- common task types
- expected inputs and outputs
- risks requiring review or QA
- whether the user is technical or non-technical, and adjust wording accordingly

### Phase 2: Architecture Pattern

Choose one pattern:

| Pattern | Use When |
| --- | --- |
| Pipeline | tasks are sequential and dependent |
| Fan-out/Fan-in | independent specialists can work in parallel before synthesis |
| Expert Pool | the right specialist depends on the request |
| Producer-Reviewer | generation needs strong quality review |
| Supervisor | one coordinator should route dynamic work |
| Hierarchical Delegation | a broad task decomposes into nested sub-workflows |

State the chosen pattern and why. If Codex subagents are available, use them for independent roles.
If not, emulate the team with role-specific sections and file handoffs in `_workspace/`.

### Phase 3: Generate Skills

Create each role or workflow as:

```text
.agents/skills/<skill-name>/SKILL.md
```

Each generated skill must include:

- YAML frontmatter with `name` and a trigger-focused `description`
- role or workflow purpose
- inputs and outputs
- step-by-step process
- verification or review criteria
- when to stop and ask the user

Keep generated `SKILL.md` files focused. Move long examples or domain references into
`references/` only when they are needed.

### Phase 4: Add Project Guidance

Create or update `AGENTS.md` with a concise pointer:

```markdown
## Harness: <domain>

Use the generated `.agents/skills/...` harness when the request involves <trigger scope>.
For simple factual questions, answer directly.

**Change history**
| Date | Change | Scope | Reason |
| --- | --- | --- | --- |
| YYYY-MM-DD | Initial Codex harness | .agents/skills, AGENTS.md | User requested a harness |
```

Do not list every generated skill in `AGENTS.md` unless the list is essential for triggering.

### Phase 5: Orchestrate Work

For Codex subagent-capable sessions:

- assign independent work to subagents with clear role prompts
- keep durable outputs in `_workspace/`
- synthesize results in the main thread

For sessions without subagents:

- create `_workspace/<phase>_<role>_<artifact>.md`
- process roles sequentially
- explicitly record dependencies between artifacts

### Phase 6: Validate

Before finishing:

- confirm every generated skill has valid frontmatter
- check that `AGENTS.md` points to the harness without duplicating full instructions
- search for accidental Claude-only runtime requirements
- run available repository checks when the harness modifies executable project files

Use this search when practical:

```powershell
Select-String -Path .agents\skills\*\SKILL.md,AGENTS.md -Pattern "TeamCreate|SendMessage|TaskCreate|CLAUDE.md|.claude"
```

Claude-only terms are acceptable only in migration notes that explain what was translated.
