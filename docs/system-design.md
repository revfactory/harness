<!-- markdownlint-disable MD013 MD060 -->

# Harness System Design Maps

> Status: draft architecture reference, not runtime canon.
> Scope: current `revfactory/harness` repository as of 2026-05-30.
> Audience: contributors who need to understand what Harness is, where the
> runtime boundary is, and what should be built or documented next.

## 1. Working Decision

Harness is a Claude Code meta-skill and plugin that turns a domain request into
project-local agent-team architecture.

It is not a standalone multi-agent runtime. The repo ships instructions,
reference patterns, and plugin metadata; Claude Code Agent Teams executes the
result.

| Type | Fact |
|---|---|
| Product/system | Harness — team-architecture factory for Claude Code |
| Kernel | `skills/harness/SKILL.md` |
| Reference modules | `skills/harness/references/*.md` |
| Distribution | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| Generated outputs | `.claude/agents/`, `.claude/skills/`, orchestrator skill, `CLAUDE.md` pointer, `_workspace/` artifacts |
| Primary runtime dependency | Claude Code v2.x Agent Teams with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

Assumptions and boundaries:

| Assumption | Confidence | How to verify |
|---|---:|---|
| Harness itself does not execute teams; Claude Code does. | High | Repo contains no standalone runtime code or workflow engine. |
| `_workspace/` is the durable run/audit surface. | High | `SKILL.md` and orchestrator template preserve it for handoff and reruns. |
| The six architecture patterns are conceptual templates, not compiled graph specs. | High | Patterns live as Markdown guidance. |
| Future cross-runtime support should be an adapter layer, not a rewrite of the concept. | Medium | Validate by prototyping a Hermes adapter from the existing skill. |

Non-goals for this document:

- Do not redesign Harness into a new product.
- Do not treat dashboards as value by themselves.
- Do not imply deterministic generation where the current repo relies on model
  instruction following.
- Do not promote Hermes translation work as current Harness functionality.

## 2. Product Definition

Harness is a design-time factory for building agent teams and their skills from
a compact domain description.

This is for:

- Claude Code users who want reusable, project-local specialist teams.
- Contributors reviewing or extending the Harness meta-skill.
- Runtime-adapter authors who need to port the concept to another agent system.

This is not:

- A generic LangGraph-style state machine runtime.
- A hosted orchestration service.
- A deterministic code generator with a typed compiler pipeline.

## 3. Core Properties and Planes

| Property | Requirement |
|---|---|
| Design-time factory | Generate durable project artifacts before repeated execution. |
| Runtime boundary clarity | Keep Harness distinct from Claude Code Agent Teams. |
| File-first memory | Preserve generated definitions and `_workspace/` artifacts. |
| Progressive disclosure | Keep the trigger skill lean; load references only when needed. |
| Drift-aware maintenance | Audit existing agents, skills, pointers, and workspace state first. |
| Explicit orchestration | Name agents, roles, inputs, outputs, and handoff paths. |
| Validation loop | Test structure, trigger behavior, dry-runs, and with-skill deltas. |
| Model policy visibility | State model assumptions and cost/runtime implications directly. |

| Plane | Components | Job |
|---|---|---|
| Data plane | Project files, user prompt, `_workspace/`, generated Markdown | Carry input, intermediate artifacts, and outputs. |
| Truth/control plane | `CLAUDE.md` pointer, change history, Phase 0 audit, validation checklist | Decide what exists, what changed, and what is safe to run. |
| Agent plane | Generated `.claude/agents/*.md`, orchestrator skill, QA agent guidance | Define who acts and what each agent may produce. |
| Model plane | Claude Code model calls, current `model: "opus"` policy | Route reasoning/execution through capable Claude models. |
| Product plane | Claude plugin, global skill install, README/quickstart | Let users install, trigger, and understand Harness. |
| Export/extension plane | Generated skills, references, future runtime adapters | Package the pattern for other domains and runtimes. |

## 4. Master Map

```mermaid
flowchart TB
  User["user prompt\n'build a harness for X'"]:::sensor

  subgraph Dist["distribution boundary"]
    Plugin["Claude plugin manifest\n.claude-plugin/plugin.json"]:::export
    Market["marketplace manifest\n.claude-plugin/marketplace.json"]:::export
    PublicDocs["README + docs"]:::surface
  end

  subgraph Harness["Harness design-time factory"]
    Skill["meta-skill\nskills/harness/SKILL.md"]:::agent
    Patterns["architecture patterns\nagent-design-patterns.md"]:::recall
    OrchTpl["orchestrator templates\norchestrator-template.md"]:::recall
    SkillGuide["skill-writing guide"]:::recall
    TestGuide["skill-testing guide"]:::recall
    QAGuide["QA agent guide"]:::recall
  end

  subgraph Claude["Claude Code runtime boundary"]
    Trigger["skill trigger\nname + description"]:::truth
    TeamAPI["Agent Teams API\nTeamCreate / SendMessage / TaskCreate"]:::bus
    AgentTool["Agent tool\nsubagent invocation"]:::worker
    ClaudeTools["Claude tools\nRead / Write / Edit / shell / web"]:::worker
    CloudModel["Claude model calls\ncurrent policy: opus"]:::modelCloud
  end

  subgraph Generated["generated project harness"]
    Agents[".claude/agents/*.md"]:::agent
    Skills[".claude/skills/*/SKILL.md"]:::agent
    Orchestrator["orchestrator skill"]:::truth
    Pointer["CLAUDE.md pointer\ntrigger + change history"]:::audit
    Workspace["_workspace/\nrun artifacts + handoffs"]:::store
  end

  User --> Trigger
  Dist --> Trigger
  Trigger --> Skill
  Skill --> Patterns
  Skill --> OrchTpl
  Skill --> SkillGuide
  Skill --> TestGuide
  Skill --> QAGuide
  Skill --> ClaudeTools
  ClaudeTools --> Agents
  ClaudeTools --> Skills
  ClaudeTools --> Orchestrator
  ClaudeTools --> Pointer
  Orchestrator --> TeamAPI
  Orchestrator --> AgentTool
  TeamAPI --> CloudModel
  AgentTool --> CloudModel
  TeamAPI --> Workspace
  AgentTool --> Workspace

  classDef sensor fill:#dbeafe,stroke:#2563eb,color:#111827;
  classDef adapter fill:#cffafe,stroke:#0891b2,color:#111827;
  classDef bus fill:#ffedd5,stroke:#f97316,color:#111827;
  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef store fill:#dcfce7,stroke:#16a34a,color:#111827;
  classDef raw fill:#f1f5f9,stroke:#64748b,color:#111827;
  classDef audit fill:#e5e7eb,stroke:#374151,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef recall fill:#ede9fe,stroke:#7c3aed,color:#111827;
  classDef security fill:#fee2e2,stroke:#dc2626,color:#111827;
  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef model fill:#e0e7ff,stroke:#4f46e5,color:#111827;
  classDef modelCloud fill:#fae8ff,stroke:#9333ea,color:#111827;
  classDef surface fill:#ccfbf1,stroke:#0f766e,color:#111827;
  classDef action fill:#fef3c7,stroke:#d97706,color:#111827;
  classDef external fill:#f8fafc,stroke:#475569,color:#111827;
  classDef export fill:#f5d0fe,stroke:#c026d3,color:#111827;
```

## 5. Layer Responsibilities

| Layer | Name | Owns | Does not own |
|---|---|---|---|
| L0 | Packaging | Plugin and marketplace metadata | Runtime behavior |
| L1 | Trigger skill | When Harness activates and which references to load | Agent execution state |
| L2 | Pattern library | Six team architecture patterns and selection guidance | Generated project truth |
| L3 | Generator workflow | Audit, analysis, agent/skill/orchestrator creation | Deterministic compilation guarantees |
| L4 | Generated harness | Project-local agents, skills, pointer, workspace | Global plugin distribution |
| L5 | Claude Code runtime | Team creation, message passing, task state, model calls | Harness documentation upkeep |
| L6 | Validation/evolution | Trigger checks, dry-runs, QA, change history | Hidden autonomous mutation |

## 6. Generation Flow

```mermaid
flowchart TD
  A["user asks for a harness"]:::sensor --> B["Harness skill triggers"]:::truth
  B --> C["Phase 0\naudit existing .claude/agents, .claude/skills, CLAUDE.md"]:::worker
  C --> D{"existing state?"}:::truth
  D -->|none| E["new build"]:::action
  D -->|existing + add/change| F["extension path"]:::action
  D -->|audit/sync/maintain| G["maintenance path"]:::action

  E --> H["Phase 1\ndomain + codebase analysis"]:::worker
  F --> H
  G --> Z["audit, sync, validate, update change history"]:::truth

  H --> I["Phase 2\nexecution mode + architecture pattern"]:::truth
  I --> J["Phase 3\ngenerate/reuse agent definitions"]:::agent
  J --> K["Phase 4\ngenerate/reuse skills"]:::agent
  K --> L["Phase 5\ngenerate/update orchestrator skill"]:::truth
  L --> M["register CLAUDE.md pointer"]:::audit
  M --> N["Phase 6\nstructure, trigger, dry-run validation"]:::worker
  N --> O["Phase 7\nfeedback and evolution loop"]:::truth

  classDef sensor fill:#dbeafe,stroke:#2563eb,color:#111827;
  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef action fill:#fef3c7,stroke:#d97706,color:#111827;
  classDef audit fill:#e5e7eb,stroke:#374151,color:#111827;
```

## 7. Runtime Execution Flow

```mermaid
flowchart TD
  A["later user task"]:::sensor --> B["CLAUDE.md pointer nudges orchestrator"]:::audit
  B --> C["orchestrator checks _workspace"]:::truth
  C --> D{"run mode"}:::truth
  D -->|initial| E["create fresh _workspace"]:::store
  D -->|partial rerun| F["reuse targeted prior artifacts"]:::store
  D -->|new input| G["archive old _workspace\nthen recreate"]:::store

  E --> H{"execution mode"}:::truth
  F --> H
  G --> H

  H -->|Agent Teams| T["TeamCreate members"]:::bus
  T --> U["TaskCreate shared tasks"]:::bus
  U --> V["agents coordinate\nSendMessage + TaskUpdate"]:::agent
  V --> W["agents write artifacts"]:::store
  W --> X["leader reads artifacts\nand integrates"]:::truth
  X --> Y["TeamDelete / cleanup"]:::action

  H -->|Subagents| S["Agent tool calls\nrun_in_background optional"]:::worker
  S --> S2["collect returns\nread file artifacts"]:::worker
  S2 --> X

  H -->|Hybrid| H2["alternate team and subagent phases"]:::truth
  H2 --> T
  H2 --> S

  Y --> Z["final deliverable + user summary"]:::surface

  classDef sensor fill:#dbeafe,stroke:#2563eb,color:#111827;
  classDef bus fill:#ffedd5,stroke:#f97316,color:#111827;
  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef store fill:#dcfce7,stroke:#16a34a,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef audit fill:#e5e7eb,stroke:#374151,color:#111827;
  classDef action fill:#fef3c7,stroke:#d97706,color:#111827;
  classDef surface fill:#ccfbf1,stroke:#0f766e,color:#111827;
```

## 8. Data and Truth Boundaries

```mermaid
flowchart LR
  Input["user prompt + project files"]:::sensor --> Analysis["domain/codebase analysis"]:::worker
  Analysis --> Plan["team pattern + execution plan"]:::truth

  Plan --> AgentDefs["agent definitions\n.claude/agents/*.md"]:::agent
  Plan --> SkillDefs["skill definitions\n.claude/skills/*/SKILL.md"]:::agent
  Plan --> Orch["orchestrator skill"]:::truth
  Orch --> Pointer["CLAUDE.md pointer\nminimal trigger + change log"]:::audit

  Input --> WS0["_workspace/00_input"]:::store
  WS0 --> Work["agent work"]:::worker
  Work --> Msg["SendMessage\nlightweight exchange"]:::bus
  Work --> Tasks["TaskCreate/TaskUpdate\nshared task state"]:::bus
  Work --> Artifacts["_workspace/phase_agent_artifact.md"]:::store
  Artifacts --> Integrate["orchestrator reads + integrates"]:::truth
  Integrate --> Final["final deliverable"]:::surface
  Integrate --> Trail["_workspace preserved\naudit / debug / partial rerun"]:::audit

  classDef sensor fill:#dbeafe,stroke:#2563eb,color:#111827;
  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef audit fill:#e5e7eb,stroke:#374151,color:#111827;
  classDef store fill:#dcfce7,stroke:#16a34a,color:#111827;
  classDef bus fill:#ffedd5,stroke:#f97316,color:#111827;
  classDef surface fill:#ccfbf1,stroke:#0f766e,color:#111827;
```

Truth rules:

| Object | Truth status | Notes |
|---|---|---|
| `skills/harness/SKILL.md` | Source for the current factory workflow | Human-authored meta-skill, not generated state. |
| Reference files | Source for pattern/detail guidance | Loaded conditionally by the skill. |
| `.claude/agents/*.md` | Generated project-local role specs | Must be audited before extension to avoid duplicates. |
| `.claude/skills/*/SKILL.md` | Generated project-local operating procedures | Skills are the reusable "how" for each agent. |
| Orchestrator skill | Generated project-local control plane | Owns who runs when and how artifacts move. |
| `CLAUDE.md` pointer | Minimal project entrypoint | Should not duplicate the whole team inventory. |
| `_workspace/` | Run evidence and handoff staging | Preserved for audit, partial reruns, and debugging. |
| SendMessage/task state | Runtime coordination state | Useful but less durable than files. |

## 9. Agent and Worker Contracts

Agents make judgments. Workers transform or validate artifacts.

| Agent/worker | Purpose | Reads | Writes | Authority |
|---|---|---|---|---|
| Harness meta-skill | Design a project harness | User prompt, project files, existing harness state, references | Generated agent/skill/orchestrator files | May create/update design artifacts after audit. |
| Generated orchestrator | Coordinate a domain team | `CLAUDE.md`, `_workspace/`, generated agent/skill files | `_workspace/`, final output, change history | Owns workflow sequencing and fallback. |
| Generated specialist agent | Perform a bounded domain role | Assigned input, prior artifacts, role skill | Assigned artifact path | Writes only its assigned artifact unless told otherwise. |
| QA agent | Cross-check output and boundary assumptions | Source files, API/UI shapes, generated output, tests | QA report, issue list, optional fixes if authorized | Verifies, does not rubber-stamp existence checks. |
| Trigger evaluator | Test skill descriptions and near misses | Candidate descriptions and eval prompts | Trigger pass/fail report | Recommends description changes. |

### Core generated artifact schemas

```yaml
agent_definition:
  path: .claude/agents/<agent-name>.md
  required_sections:
    - core_role
    - working_principles
    - input_output_protocol
    - error_handling
    - collaboration
    - team_communication_protocol_if_team_mode
```

```yaml
skill_definition:
  path: .claude/skills/<skill-name>/SKILL.md
  frontmatter:
    name: <skill-name>
    description: <trigger-rich description>
  body:
    - overview
    - workflow
    - outputs
    - pitfalls
    - verification
  optional_resources:
    - references/
    - scripts/
    - assets/
```

```yaml
run_artifact:
  root: _workspace/
  input_dir: _workspace/00_input/
  artifact_name: <phase>_<agent>_<artifact>.md
  final_output: <user-requested path or orchestrator default>
  preserve: true
```

## 10. Model Layer

Current Harness policy is Claude-specific: generated agent calls should use
`model: "opus"`. That is simple and quality-biased, but expensive and not
portable.

```mermaid
flowchart LR
  Context["agent prompt + project context"]:::recall --> Router["Claude Code model route"]:::model
  Router --> Opus["Claude model\ncurrent policy: opus"]:::modelCloud
  Opus --> Result["agent output"]:::agent
  Result --> Audit["artifact / summary / workspace trail"]:::audit

  Router --> Risk["cost + availability risk\n50K-200K token tasks possible"]:::security

  classDef recall fill:#ede9fe,stroke:#7c3aed,color:#111827;
  classDef model fill:#e0e7ff,stroke:#4f46e5,color:#111827;
  classDef modelCloud fill:#fae8ff,stroke:#9333ea,color:#111827;
  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef audit fill:#e5e7eb,stroke:#374151,color:#111827;
  classDef security fill:#fee2e2,stroke:#dc2626,color:#111827;
```

| Model class | Current use | Sensitive data policy | Gap |
|---|---|---|---|
| Claude Opus-class | All generated agents by policy | Governed by Claude Code runtime and user project context | No per-agent cost/fallback routing. |
| No-LLM deterministic checks | Markdown/YAML/frontmatter validation when scripted | Safe for local validation | Scripts are mostly methodology, not bundled automation. |
| Future adapter models | Hermes/Codex/DeepSeek/local routes | Must be explicit per adapter | Requires capability tiers, not hard-coded Claude names. |

## 11. Architecture Patterns

```mermaid
flowchart LR
  P1["Pipeline\nsequential dependency"]:::worker --> M1["Use when outputs feed next stage"]:::truth
  P2["Fan-out / Fan-in\nparallel perspectives"]:::worker --> M2["Best native Agent Teams fit"]:::truth
  P3["Expert Pool\nconditional expert routing"]:::worker --> M3["Often cheaper as subagents"]:::truth
  P4["Producer / Reviewer\ngenerate then verify"]:::worker --> M4["Team useful for feedback loop"]:::truth
  P5["Supervisor\ndynamic task allocation"]:::worker --> M5["Maps to shared task list"]:::truth
  P6["Hierarchical Delegation\nrecursive decomposition"]:::worker --> M6["Constraint: no nested teams\nflatten or team + subagents"]:::security

  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef security fill:#fee2e2,stroke:#dc2626,color:#111827;
```

## 12. External Dependency Loop

```mermaid
flowchart TD
  Harness["Harness v1.2.x"]:::agent --> ClaudeCode["Claude Code v2.x+"]:::external
  ClaudeCode --> Flag["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"]:::security
  Flag --> TeamCreate["TeamCreate"]:::bus
  Flag --> SendMessage["SendMessage"]:::bus
  Flag --> TaskCreate["TaskCreate / TaskUpdate"]:::bus
  ClaudeCode --> AgentTool["Agent tool"]:::worker
  ClaudeCode --> Anthropic["api.anthropic.com"]:::modelCloud
  Install["plugin install"]:::surface --> GitHub["GitHub marketplace repo"]:::external

  Flag --> Future{"upstream future"}:::truth
  Future --> A["Agent Teams GA\nremove flag path"]:::action
  Future --> B["Managed Agents GA\nadapter/export path"]:::action
  Future --> C["breaking API change\nhotfix + matrix"]:::security

  classDef agent fill:#fce7f3,stroke:#db2777,color:#111827;
  classDef external fill:#f8fafc,stroke:#475569,color:#111827;
  classDef security fill:#fee2e2,stroke:#dc2626,color:#111827;
  classDef bus fill:#ffedd5,stroke:#f97316,color:#111827;
  classDef worker fill:#fef9c3,stroke:#ca8a04,color:#111827;
  classDef modelCloud fill:#fae8ff,stroke:#9333ea,color:#111827;
  classDef surface fill:#ccfbf1,stroke:#0f766e,color:#111827;
  classDef truth fill:#ffe4e6,stroke:#e11d48,color:#111827;
  classDef action fill:#fef3c7,stroke:#d97706,color:#111827;
```

## 13. Pluggability Model

Harness already has the right conceptual split: patterns, generated agents,
generated skills, and orchestration. The missing abstraction is a runtime
adapter.

```yaml
runtime_adapter:
  id: claude-code-agent-teams
  status: current
  input:
    - domain_request
    - project_context
    - existing_harness_state
  outputs:
    - agent_definitions
    - skill_definitions
    - orchestrator_skill
    - project_pointer
    - workspace_manifest_optional
  primitives:
    create_team: TeamCreate
    message_agent: SendMessage
    create_task: TaskCreate
    invoke_subagent: Agent
  model_policy: opus
  audit_surface: _workspace/
```

A future adapter should implement the same conceptual contract without copying
Claude-specific tool names into the core design.

## 14. MVP Spine for the Next Build Slice

The next useful module is not a dashboard. It is a manifest-backed generated
harness contract.

Closest time-to-value:

| Feature | Why now | Depends on |
|---|---|---|
| `_workspace/run-manifest.json` | Makes reruns, audit, and partial execution deterministic. | Artifact naming contract. |
| Adapter contract doc | Separates Harness from Claude Code primitive names. | This system map. |
| Cost/model policy table | Makes `model: "opus"` explicit and overrideable later. | Runtime adapter boundary. |
| Validation script | Turns methodology into repeatable checks. | Markdown/frontmatter schema. |

Deferred:

- Hosted dashboard.
- Multi-user permission system.
- Runtime state database.
- Full cross-runtime implementation before the adapter contract is proven.

## 15. Open Questions

| Question | Why it matters | Default assumption |
|---|---|---|
| Should generated runs include a machine-readable manifest? | Without it, drift detection is model/manual. | Yes, add as a docs-backed convention first. |
| Should model policy stay hard-coded to Opus? | Cost and portability suffer. | Keep for Claude path, but add model class language. |
| Should Hermes/Codex support live in this repo or a sibling repo? | Avoid confusing current users. | Start as an adapter design doc, then prototype separately. |
| Should README link architecture docs in all languages? | Discoverability vs i18n maintenance. | Add docs first; update localized READMEs only if maintainers want parity. |

## 16. Design Verdict

Harness is strongest as a team-architecture compiler written in Markdown:
pattern selection, role definition, skill authoring, orchestration, and
validation are all legible.

The weak spot is pretending runtime details are generic. They are not. Today the
runtime is Claude Code Agent Teams. Future ports should keep the Harness factory
abstraction and swap the runtime adapter underneath it.

Build next: a manifest-backed adapter contract plus a validation script. That
turns the useful methodology into something contributors can test instead of
just admire.
