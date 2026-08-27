# Orchestrator Templates

The orchestrator skill sequences agents and tools into an end-to-end workflow. Keep the frontmatter description in the user's language for reliable semantic triggering.

## Template A: Subagents (Default)

````markdown
---
name: {domain}-orchestrator
description: "{도메인} 전문 에이전트를 조율하는 오케스트레이터. {초기 실행 키워드}. 후속 작업: 결과 수정, 부분 재실행, 업데이트, 보완, 다시 실행, 이전 결과 개선 요청 시에도 이 스킬을 사용."
---

# {Domain} Orchestrator

## Execution Mode: Subagents

## Agent Lineup

| Agent | subagent_type | Role | Skill | Output Path |
|-------|---------------|------|-------|-------------|
| {agent-1} | {builtin/custom} | {role} | {skill} | `_workspace/02_{agent-1}_{artifact}.md` |
| {agent-2} | {builtin/custom} | {role} | {skill} | `_workspace/02_{agent-2}_{artifact}.md` |

## Workflow

### Phase 0: Context & State Check
1. Check if `_workspace/` exists:
   - **Missing:** Initial run → Proceed to Phase 1.
   - **Exists + Partial Edit:** Re-invoke only the affected agent, reading prior artifact.
   - **Exists + Fresh Input:** Archive `_workspace/` to `_workspace_prev/` → Phase 1.

### Phase 1: Prepare
1. Analyze user input and extract requirements.
2. Initialize `_workspace/` directory.
3. Write parsed input to `_workspace/00_input.md`.

### Phase 2: Parallel Execution
Issue all `Agent` calls concurrently in a single message.
```markdown
- Call Agent({agent-1}, prompt: "...")
- Call Agent({agent-2}, prompt: "...")
```
*Tip:* To perform follow-ups on a completed agent without losing context, resume by name using `SendMessage`.

### Phase 3: Integrate & Synthesize
1. Read generated artifacts from `_workspace/`.
2. Reconcile differences and synthesize final output.
3. Write final deliverable to `{output-path}`.

### Phase 4: Wrap-up & Audit
1. Retain `_workspace/` for auditing and follow-ups.
2. Present a concise final summary to the user.

## Error Handling

| Scenario | Recovery Strategy |
|----------|-------------------|
| Single agent failure | Retry once. If still failing, proceed with available results and note the gap in summary. |
| Critical / majority failure | Stop execution and prompt user for instructions. |
| Conflicting data | Retain both versions with source attribution; do not silently delete. |

## Test Scenarios

### Happy Path
1. User provides {valid input}.
2. Phase 1 sets up workspace.
3. Phase 2 executes {N} agents in parallel.
4. Phase 3 produces verified artifact at `{output-path}`.

### Error Path
1. {agent-2} fails in Phase 2.
2. Retry fails.
3. Phase 3 completes with partial data and logs missing coverage.
````

## Template B: Workflow (Deterministic Control Flow)

Use when flow logic is code-driven (fan-out over a list, per-item verification, loop-until-dry). Requires explicit user opt-in.

````markdown
---
name: {domain}-orchestrator
description: "{도메인} 워크플로우 오케스트레이터. {키워드}. 후속 작업: 재실행, 수정, 업데이트."
---

# {Domain} Workflow Orchestrator

## Script Definition

```javascript
export const meta = {
  name: '{domain}-run',
  description: '{one-line description}',
  phases: [{ title: 'Discover' }, { title: 'Process' }, { title: 'Verify' }],
}

// 1. Discovery phase
phase('Discover')
const items = await agent('{discovery prompt}', { schema: DISCOVERY_SCHEMA })

// 2. Pipelined execution & verification
const results = await pipeline(
  items.list,
  it => agent(`Process ${it.name}`, { label: `proc:${it.name}`, phase: 'Process', schema: PROCESS_SCHEMA }),
  (out, it) => agent(`Adversarially verify ${it.name}: ${out.summary}`,
                     { label: `verify:${it.name}`, phase: 'Verify', schema: VERDICT_SCHEMA })
              .then(v => ({ ...out, item: it.name, verdict: v }))
)

return { confirmed: results.filter(Boolean).filter(r => r.verdict?.isValid) }
```

### Script Rules
- Use `pipeline()` by default for continuous throughput. Use `parallel()` barrier only when cross-item aggregation is required.
- Pass timestamps via `args` (`Date.now()`/`Math.random()` are disabled to support resume).
- Filter out skipped/failed agents with `.filter(Boolean)`.
````

## Template C: Agent Teams (Workspace-Gated Only)

Only use if `TeamCreate` is explicitly listed in session tools.

````markdown
## Execution Mode: Agent Team

### Phase 1: Team Formation
Call `TeamCreate` with member definitions. Call `TaskCreate` to initialize the shared task list with dependencies.

### Phase 2: Autonomous Coordination
Members claim tasks, coordinate peer-to-peer via `SendMessage`, and update task statuses. Main monitors progress.

### Phase 3: Teardown
Call `TeamDelete` upon completion. Retain artifacts in `_workspace/`.
````

## Writing Rules
1. **Explicit Mode:** Always specify execution mode at the top.
2. **Explicit Paths:** Use structured relative paths anchored at `_workspace/`.
3. **Follow-up Keywords:** Always include re-run and modification keywords in the description (재실행, 다시 실행, 수정, 업데이트, 보완, 이전 결과 기반).
4. **Resilient Design:** Define explicit error handling and at least one failure recovery scenario.
