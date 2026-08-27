# Agent Design Patterns

## Execution Modes

Check active session tools before design. `TeamCreate`/`TaskCreate`/`TeamDelete` are workspace-gated.

### Subagents (Default)
Main agent issues `Agent` calls. Multiple calls in one message execute concurrently. Results return to main.
```
[main] ──┬──> [subagent A] ──> result
         ├──> [subagent B] ──> result
         └──> [subagent C] ──> result
```
- Resume named agents via `SendMessage` to preserve context.
- Fast, low overhead, context-isolated. Main handles all coordination.
- Subagents cannot communicate peer-to-peer mid-run.

### Workflow (Deterministic Control Flow)
Runs a script with `pipeline()`/`parallel()`/`phase()`. Use when flow is code-driven (fan-out over a list, per-item verification, loop-until-dry). Requires explicit user opt-in ("workflow", "ultracode"). Prefer `pipeline()` over `parallel()` to avoid barrier latency.

### Agent Teams (Workspace-Gated)
Leader spawns members with `TeamCreate`; members coordinate peer-to-peer via `SendMessage` and a shared task list (`TaskCreate`/`TaskUpdate`).
- High token cost, fixed leader, max one active team per session.

### Decision Matrix
```
Multiple agents?
├── No  ──> Single subagent
└── Yes ──> Need deterministic flow (loops, per-item verify, strict pipeline)?
            ├── Yes + user opt-in ──> Workflow
            └── No  ──> Parallel Agent calls; resume via SendMessage if needed
                        (Agent team only if tools explicitly available)
```

## Model Selection
Default: Omit `model` parameter so agents inherit session model.
Override only when justified:
- `haiku`: Cheap, fast, structured mechanical tasks (parsing, scraping, simple format transform).
- High-tier (`opus`/`sonnet`): Complex reasoning, difficult architecture design, or adversarial review.

## Architecture Patterns

| Pattern | Topology | Description & Use Case |
|---------|----------|------------------------|
| **Pipeline** | `A → B → C` | Sequential dependent stages (e.g., worldbuilding → characters → plot → writing). |
| **Fan-out / Fan-in** | `split → {A,B,C} → merge` | Parallel multi-angle analysis on same input (e.g., multi-source research). |
| **Expert Pool** | `router → {A \| B \| C}` | Dynamic routing to dedicated specialists based on task type (e.g., code review). |
| **Producer-Reviewer** | `produce ⇄ review` | Quality gate with objective criteria. **Cap retries at 2–3** to prevent infinite loops. |
| **Supervisor** | `super ──> {workers}` | Dynamic batching and dispatch based on runtime state (e.g., codebase migration). |
| **Hierarchical** | `lead → sub-leads → workers` | Nested domain decomposition. Keep to **max 2 levels** to prevent context loss. |

### Composite Patterns
- **Fan-out + Producer-Reviewer:** Parallel generation followed by per-item verification (e.g., multi-language translation + native review).
- **Pipeline + Fan-out:** Sequential preparation, parallel execution middle, integrated summary.
- **Supervisor + Expert Pool:** Dynamic triage and routing to specialist agents.

## Agent Types

| Type | Capabilities | Best for |
|------|--------------|----------|
| `general-purpose` | Full tools (file, bash, web search/fetch) | General tasks, web research, QA running tests/scripts |
| `Explore` | Read-only tools | Fast codebase searches, locating symbols/files |
| `Plan` | Read-only tools | Architectural planning, design analysis |
| Custom (`.claude/agents/*.md`) | Full tools + custom prompt/role | Domain-specific reusable roles |

*Always write `.claude/agents/{name}.md` even when using built-in types* to ensure persistent agent configuration across sessions.

## Agent Definition Template

```markdown
---
name: agent-name
description: "1-2 sentence role summary. Clear trigger keywords."
---

# Agent Name — One-line Role

You are a {role} specialist in {domain}.

## Role & Responsibilities
1. ...
2. ...

## Working Principles
- ...

## Input / Output Protocol
- Input: {source path / format}
- Output: {destination path / format}
- Format: {markdown structure / json schema}

## On Re-invocation
- If prior artifact exists at {path}, read it and update only requested delta.
- If user feedback is provided, target changes specifically to feedback points.

## Error Handling & Fallback
- On missing input / failure: ...
- Fallback strategy: ...

## Collaboration
- Upstream: Consumes output from {agent}.
- Downstream: Feeds artifact to {agent}.
```

## Split & Merge Criteria

| Axis | Split into Multiple Agents | Merge into Single Agent |
|------|----------------------------|-------------------------|
| **Expertise** | Distinct, deep domain specializations | Closely overlapping skills |
| **Parallelism** | Can run concurrently | Strictly sequential execution |
| **Context Load** | Heavy context requirements | Light, fast operations |
| **Reusability** | Reused across multiple workflows | Single-use specific step |

## Skills vs Agents

| Dimension | Skill (`.claude/skills/`) | Agent (`.claude/agents/`) |
|-----------|---------------------------|---------------------------|
| **Nature** | Procedural knowledge ("How") | Role identity & principles ("Who") |
| **Trigger** | Semantic match on description | Explicit `Agent` invocation |
| **Binding** | Invoked via Skill tool or referenced in prompt | Declared as subagent in orchestrator |
