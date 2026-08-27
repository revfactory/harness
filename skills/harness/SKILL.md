---
name: harness
description: "하네스를 구성합니다. 전문 에이전트를 정의하며, 해당 에이전트가 사용할 스킬을 생성하는 메타 스킬. (1) '하네스 구성해줘', '하네스 구축해줘' 요청 시, (2) '하네스 설계', '하네스 엔지니어링' 요청 시, (3) 새로운 도메인/프로젝트에 대한 하네스 기반 자동화 체계를 구축할 때, (4) 하네스 구성을 재구성하거나 확장할 때, (5) '하네스 점검', '하네스 감사', '하네스 현황', '에이전트/스킬 동기화' 등 기존 하네스 운영/유지보수 요청 시 사용."
---

# Harness — Agent & Skill Architect

Build and maintain domain automation harnesses: agent definitions (`.claude/agents/`), skills (`.claude/skills/`), an orchestrator skill, and a pointer in `CLAUDE.md`.

## Execution Modes

Check active session tools before design. `TeamCreate`/`TaskCreate`/`TeamDelete` are workspace-gated and absent in most sessions.

| Mode | Tools | Best for |
|------|-------|----------|
| **Subagents** (default) | `Agent` (parallel calls in one turn), `SendMessage` (resume named agent) | Independent tasks, results return to main |
| **Workflow** | `Workflow` with `pipeline()`/`parallel()` | Deterministic flow, fan-out over lists, loops. Requires user opt-in |
| **Agent teams** | `TeamCreate` + `TaskCreate` + `SendMessage` | Only when tools are explicitly available |

Model selection: Omit `model` to inherit session model. Override only when justified (e.g., `haiku` for mechanical parsing, higher tier for hard verification).

## Workflow

### Phase 0: Audit
1. Inspect `.claude/agents/`, `.claude/skills/`, `CLAUDE.md`.
2. Branch:
   - **New build** (empty/missing) → Run Phases 1–6.
   - **Extend** (add agents/skills) → Follow Extend Matrix.
   - **Maintain** (audit/sync/fix) → Run Phase 7-5.
3. Compare file structure with `CLAUDE.md` and report drift. Confirm plan with user.

Extend Matrix:
| Target | P1 | P2 | P3 | P4 | P5 | P6 |
|--------|----|----|----|----|----|----|
| Add agent | skip | placement | yes | if needed | edit orchestrator | yes |
| Add/edit skill | skip | skip | skip | yes | if wiring changes | yes |
| Architecture change | skip | yes | affected | affected | yes | yes |

### Phase 1: Domain Analysis
- Identify domain, core tasks, stack, and key modules.
- Check naming/role collisions against existing agents and skills.

### Phase 2: Architecture
Select a core pattern (see `references/agent-design-patterns.md`):
- **Pipeline** (`A→B→C`): Sequential dependencies.
- **Fan-out/fan-in** (`split→N→merge`): Multi-perspective parallel analysis.
- **Expert pool** (`router→{A|B|C}`): Dynamic routing to specialists.
- **Producer-reviewer** (`produce→review→remake`): Quality gate (cap retries at 2–3).
- **Supervisor** (`dynamic batching`): Runtime workload distribution.
- **Hierarchical** (max 2 levels): Nested problem decomposition.

Split criteria: Split on expertise difference, parallel execution, heavy context, or cross-harness reuse. Merge when overlapping or strictly sequential.

### Phase 3: Agent Definitions
Write `.claude/agents/{name}.md` for every agent (including built-in types `general-purpose`, `Explore`, `Plan`).

Required sections:
1. `name` & `description` in YAML frontmatter.
2. Role & Core Principles.
3. Input/Output protocol (explicit paths & formats).
4. Re-invocation behavior (read prior artifact at `_workspace/` instead of restarting).
5. Error handling & fallback.
6. Collaboration links.

*Note on QA agents*: Use `general-purpose` (not read-only `Explore`). Verify boundary coherence by cross-reading producer/consumer pairs incrementally (see `references/qa-agent-guide.md`).

### Phase 4: Skills
Create `.claude/skills/{name}/SKILL.md` (optional: `scripts/`, `references/`, `assets/`).

Rules:
- **Description is the sole trigger:** Clearly define scope, concrete trigger keywords, and boundary exclusions in user's language.
- **Explain why:** Provide rationale so the model generalizes edge cases.
- **Stay lean:** Target <300 lines in `SKILL.md`. Move specialized docs to `references/`.
- **Bundle repeats:** Place recurring helper scripts into `scripts/`.
- **Use imperative style.**

Progressive disclosure: Metadata (always loaded) → `SKILL.md` body (on trigger) → `references/` (on-demand read).

### Phase 5: Orchestrator
Create `.claude/skills/{domain}-orchestrator/SKILL.md` to wire agents and skills (see `references/orchestrator-template.md`).

Data passing:
- Small results: `Agent` return values.
- Large/structured data: Files at `_workspace/{phase}_{agent}_{artifact}.{ext}`.
- Follow-ups: `SendMessage` to named agents.

Team sizing: 2–3 agents for simple flows; 3–5 for moderate; 5–7 for complex workflows.

Register pointer in `CLAUDE.md`:
````markdown
## 하네스: {도메인}

**목표:** {한 줄 요약}

**트리거:** {도메인} 관련 작업 요청 시 `{orchestrator-skill}` 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| {YYYY-MM-DD} | 초기 구성 | 전체 | - |
````

Support follow-ups:
- Add keywords to orchestrator description: 재실행, 다시 실행, 수정, 업데이트, 보완, 이전 결과 기반.
- Handle `_workspace/` in Phase 0: missing → fresh; exists + edit → re-invoke target agent; exists + new input → archive to `_workspace_prev/`.

### Phase 6: Verification
- **Structure:** Files in place, valid frontmatter, no files in `.claude/commands/`.
- **Wiring:** Input/output paths connect end-to-end.
- **Execution test:** Run 2–3 realistic task prompts.
- **Trigger test:** 8–10 should-trigger queries vs 8–10 should-not-trigger near-miss queries (see `references/skill-testing-guide.md`).
- **Dry run:** Verify happy path and error recovery. Include test scenarios in orchestrator.

### Phase 7: Evolution & Maintenance
- Collect feedback after execution.
- Route updates: Quality → Agent skill; Missing role → Add agent; Flow issue → Orchestrator phases.
- Log every modification in `CLAUDE.md`.

#### 7-5. Maintenance Workflow
1. Diff `.claude/agents/` and `.claude/skills/` against orchestrator declarations.
2. Fix mismatches and sync sequentially.
3. Update `CLAUDE.md` change table.
4. Verify structure, triggers, and execution.

## Checklist

- [ ] `.claude/agents/{name}.md` created for all agents (including built-ins).
- [ ] `.claude/skills/{name}/SKILL.md` created (<300 lines; references split).
- [ ] Orchestrator created with data flow, error handling, and test scenarios.
- [ ] Execution mode matches available session tools.
- [ ] No files created under `.claude/commands/`.
- [ ] Skill descriptions include boundary constraints and follow-up keywords.
- [ ] Execution test and trigger tests passed.
- [ ] `CLAUDE.md` pointer registered and change history logged.
- [ ] Orchestrator Phase 0 handles initial run vs re-invocation cleanly.

## References

- `references/agent-design-patterns.md` — Architectures, agent templates, split/merge rules.
- `references/team-examples.md` — Real-world harness implementations across patterns.
- `references/orchestrator-template.md` — Ready-to-use orchestrator templates.
- `references/skill-writing-guide.md` — Trigger optimization, styling, and eval schemas.
- `references/skill-testing-guide.md` — Eval methodology, assertions, and grading.
- `references/qa-agent-guide.md` — Integration boundary verification and QA patterns.
