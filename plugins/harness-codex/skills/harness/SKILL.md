---
name: harness
description: "Build, design, port, audit, extend, or maintain a Harness-style team architecture for Codex. Use when the user asks to build a harness, design an agent team/workflow, create project-specific skills, port revfactory/harness or a Claude Code harness to Codex, inspect harness drift, sync agents/skills, improve orchestration, or validate a generated harness."
---

# Harness for Codex -- Team Architecture & Skill Architect

Harness is a meta-skill that turns a domain or project description into a Codex-native team architecture: durable role/workflow skills, an orchestrator skill, concise `AGENTS.md` triggers, and `_workspace` handoff artifacts.

This Codex port preserves the behavior of `revfactory/harness`: analyze a domain, choose one of six team architecture patterns, define specialists, generate their skills, wire an orchestrator, validate triggers, and keep the harness evolving over time. The runtime surface changes from Claude Code agent files to Codex-native project files.

## Core Principles

1. Generate durable files, not just chat guidance.
2. Use Codex-native surfaces:
   - `.agents/skills/<skill-name>/SKILL.md` for specialist roles, workflows, and orchestrators.
   - `AGENTS.md` for the shortest possible harness pointer and change history.
   - `_workspace/` for intermediate artifacts and team handoffs.
3. Preserve Harness behavior: specialist decomposition, architecture-pattern selection, orchestration, validation, trigger testing, and continuous evolution.
4. Do not require Claude Code runtime primitives such as `TeamCreate`, `SendMessage`, `TaskCreate`, `Agent(...)`, `subagent_type`, `.claude/agents`, `.claude/skills`, or `CLAUDE.md`.
5. When porting from revfactory/harness, translate behavior and structure faithfully, but adapt file locations and execution mechanics to Codex.

## Runtime Translation

| revfactory/harness concept | Codex port |
| --- | --- |
| `.claude/agents/{agent}.md` | `.agents/skills/<role-or-agent>/SKILL.md` with role, protocol, inputs, outputs, and verification |
| `.claude/skills/{skill}/SKILL.md` | `.agents/skills/<skill>/SKILL.md` |
| Orchestrator skill | `.agents/skills/<domain-orchestrator>/SKILL.md` |
| `CLAUDE.md` pointer | concise `AGENTS.md` Harness section |
| Agent Team communication | Codex subagents when available; otherwise `_workspace` file handoffs and main-thread synthesis |
| `TeamCreate` / `TaskCreate` / `SendMessage` | explicit plan, role assignment, `_workspace` artifacts, review gates, and final synthesis |

## Reference Routing

Read only the reference needed for the current phase:

- `references/agent-design-patterns.md` -- six patterns, execution modes, specialist split/reuse.
- `references/orchestrator-template.md` -- Codex orchestrator templates and handoff protocols.
- `references/team-examples.md` -- example team configurations translated to Codex.
- `references/skill-writing-guide.md` -- generated skill authoring rules.
- `references/skill-testing-guide.md` -- trigger, dry-run, and with/without skill testing.
- `references/qa-agent-guide.md` -- QA role design and boundary-crossing review.

## Workflow

### Phase 0: Current Harness Audit

Read the target project for:

- `.agents/skills/`
- `AGENTS.md`
- `_workspace/`
- legacy `.claude/agents/`, `.claude/skills/`, `CLAUDE.md`
- relevant README, docs, tests, release notes, package scripts, and domain files

Classify the run:

- **New Build:** no useful harness exists.
- **Extension:** existing Codex harness exists and needs new roles, skills, or workflow branches.
- **Port:** a Claude/revfactory harness exists and must be translated to Codex.
- **Maintenance:** existing harness needs audit, repair, sync, simplification, or drift correction.

For extension and maintenance, use the existing harness rather than generating duplicates.

### Phase 1: Domain Analysis

Identify:

1. project/domain goal
2. recurring task types: generation, review, editing, release, research, QA, data handling, localization, operations
3. expected inputs and outputs
4. target user's technical level and communication style
5. project risks requiring specialists or review gates
6. existing commands, tests, release paths, schemas, resource files, or safety constraints
7. existing skills that can be reused

### Phase 2: Team Architecture Design

Choose one primary pattern from revfactory/harness:

| Pattern | Use When |
| --- | --- |
| Pipeline | sequential dependent tasks |
| Fan-out/Fan-in | independent specialists work in parallel before synthesis |
| Expert Pool | the right specialist depends on the request |
| Producer-Reviewer | generation needs quality review |
| Supervisor | one coordinator routes dynamic work |
| Hierarchical Delegation | broad tasks decompose into nested workflows |

Use `references/agent-design-patterns.md` for selection rules.

Then choose a Codex execution mode:

- **Subagent-capable team:** use Codex subagents for independent work when the session exposes them.
- **File-handoff team:** emulate the team with role skills and `_workspace` artifacts when subagents are unavailable.
- **Hybrid:** use subagents for independent research/review and file handoffs for durable state.

State the chosen pattern and execution mode before writing files.

### Phase 3: Specialist Definition

In Codex, specialists are durable skills. Create each specialist as:

```text
.agents/skills/<specialist-name>/SKILL.md
```

Each specialist skill must include:

- frontmatter with `name` and trigger-focused `description`
- core role
- working principles
- inputs and outputs
- process
- collaboration or handoff protocol
- verification criteria
- when to stop and ask the user

Before adding a specialist, inspect existing `.agents/skills/` entries to avoid duplicate roles.

### Phase 4: Skill Generation

Generate any workflow/helper skills that specialists need. Use `references/skill-writing-guide.md`.

Generated skills must:

- be lean in the main `SKILL.md`
- use `references/` only for conditional detail
- include scripts only for repeated deterministic work
- explain why important rules exist
- include project-specific paths and commands only after verifying they fit the target repository

### Phase 5: Integration & Orchestration

Generate or update one orchestrator skill when the harness needs routing or multi-role coordination.

The orchestrator must define:

- context check: previous `_workspace` artifacts, current user request, and changed files
- task classification matrix
- chosen architecture pattern and execution mode
- role assignment
- handoff artifacts in `_workspace/`
- error handling
- retry and partial-result rules
- follow-up behavior such as "rerun", "update", "fix only this part", and "use previous result"
- normal and error test scenarios

Use `references/orchestrator-template.md`.

Update `AGENTS.md` with only a pointer:

```markdown
## Harness: <domain>

Use the generated `.agents/skills/...` harness when the request involves <trigger scope>.
For simple factual questions or tiny lookups, answer directly.

Architecture pattern: <pattern>. <one sentence on routing>.

**Change history**
| Date | Change | Scope | Reason |
| --- | --- | --- | --- |
| YYYY-MM-DD | Initial Codex harness | `.agents/skills`, `AGENTS.md`, `_workspace` | User requested a harness |
```

### Phase 6: Validation & Testing

Use `references/skill-testing-guide.md` and validate:

1. structure: files exist where promised
2. frontmatter: every generated skill has `name` and `description`
3. trigger quality: should-trigger and should-not-trigger prompts
4. orchestration: no dead handoff paths
5. Codex-native surface: no required Claude-only primitives
6. project fit: paths, tests, release assets, locales, and safety gates match the target
7. QA: reviewer skill exists when quality, security, release, storage, localization, or integration risk is meaningful

Practical Claude-only search:

```powershell
Select-String -Path .agents\skills\*\SKILL.md,AGENTS.md -Pattern "TeamCreate|SendMessage|TaskCreate|Agent\(|subagent_type|CLAUDE.md|\.claude"
```

Those terms are allowed only in migration notes that explain what was translated.

### Phase 7: Harness Evolution

Harness is not static. When the user gives feedback or repeated failures appear:

1. classify the feedback: output quality, role design, workflow order, team composition, trigger gap, validation gap
2. update the affected skill or orchestrator, not every file
3. update the `AGENTS.md` change history
4. rerun the relevant validation checks

For maintenance requests, audit the current `.agents/skills/` and `AGENTS.md` first, report drift, then patch only what is needed.

## Completion Report

When done, report:

- classification: New Build, Extension, Port, or Maintenance
- chosen architecture pattern and Codex execution mode
- files created or changed
- validation performed
- any remaining gaps or user decisions needed
