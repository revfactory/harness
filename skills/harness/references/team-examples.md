# Harness Real-World Examples

Practical architectures and agent setups across common domain patterns.

---

## 1. Research Harness (Fan-out / Fan-in, Subagents)

```
[main]
  ├── 4 concurrent Agent calls in one message
  ├── Collect & read 4 artifacts from _workspace/
  └── Synthesize comprehensive report
```

| Agent | subagent_type | Scope | Output Path |
|-------|---------------|-------|-------------|
| `official-researcher` | `general-purpose` | Docs, whitepapers, official blogs | `_workspace/02_official.md` |
| `media-researcher` | `general-purpose` | Tech news, press releases, funding | `_workspace/02_media.md` |
| `community-researcher` | `general-purpose` | Reddit, Hacker News, Dev forums | `_workspace/02_community.md` |
| `background-researcher`| `general-purpose` | History, competitive landscape | `_workspace/02_background.md` |

- **Execution:** Main issues all 4 `Agent` calls in a single turn.
- **Relay:** If one researcher uncovers a lead for another, main resumes the relevant agent by name using `SendMessage`.
- **Synthesis:** Main reconciles contradictions, attributing conflicting claims to their respective sources.

---

## 2. Creative Writing Harness (Pipeline + Fan-out)

```
Phase 1 (Parallel)  [worldbuilder] + [character-designer] + [plot-architect]
Phase 2 (Single)    [prose-stylist] drafts chapters from Phase 1 artifacts
Phase 3 (Parallel)  [science-consultant] + [continuity-manager] review draft
Phase 4 (Single)    [prose-stylist] applies review feedback
```

### Agent Definition Example: `worldbuilder.md`
```markdown
---
name: worldbuilder
description: "SF 세계관 설계 전문가. 물리 법칙, 기술 수준, 사회/경제 구조, 역사적 설정을 구축."
---

# Worldbuilder

You are a worldbuilding specialist for science fiction novels.

## Responsibilities
1. Define consistent physical laws and technology levels.
2. Structure political, economic, and social systems.
3. Establish historical lore and central conflicts.

## Input / Output Protocol
- Input: User concept & genre constraints.
- Output: `_workspace/01_worldbuilder_setting.md`.
- Format: Markdown (Physics / Society / Technology / History).

## On Re-invocation
- Read existing `_workspace/01_worldbuilder_setting.md` and modify only target sections.
```

---

## 3. Webtoon Production Harness (Producer-Reviewer)

```
Phase 1: Agent(webtoon-artist)   ──> Generate panel specifications
Phase 2: Agent(webtoon-reviewer) ──> Evaluate panels (PASS / FIX / REDO)
Phase 3: Agent(webtoon-artist)   ──> Regenerate flagged panels (max 2 cycles)
```

- **Verdict Schema:** `PASS` (proceed), `FIX` (minor textual/framing edit), `REDO` (regenerate panel prompt).
- **Termination:** Limit review/fix loop to **maximum 2 iterations** to avoid infinite cycles.

---

## 4. Code Review Harness (Fan-out with Workflow)

When user opts into multi-agent workflows, use `pipeline()` for per-finding adversarial verification:

```javascript
export const meta = {
  name: 'code-audit',
  description: 'Multi-dimensional code audit with adversarial verification',
  phases: [{ title: 'Review' }, { title: 'Verify' }],
}

const DIMENSIONS = [
  { key: 'security', prompt: 'Audit for injection, auth bypass, and secret leaks' },
  { key: 'perf', prompt: 'Audit for N+1 queries, memory leaks, and blocking IO' },
  { key: 'correctness', prompt: 'Audit for race conditions and edge case errors' },
]

const results = await pipeline(
  DIMENSIONS,
  d => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review', schema: FINDINGS_SCHEMA }),
  review => parallel(review.findings.map(f => () =>
    agent(`Adversarially refute finding: ${f.title}`,
          { label: `verify:${f.file}`, phase: 'Verify', schema: VERDICT_SCHEMA })
      .then(v => ({ ...f, verdict: v }))
  ))
)

return { confirmed: results.flat().filter(Boolean).filter(f => f.verdict?.isReal) }
```

---

## 5. Codebase Migration Harness (Supervisor)

```
[main] Analyzes file tree, estimates complexity, batches files
  ├── Agent(migrator, batch: simple, isolation: worktree)
  ├── Agent(migrator, batch: complex, isolation: worktree)
  └── Run validation suite across worktrees
```
- **Isolation:** Use `isolation: "worktree"` when subagents mutate files in parallel to prevent write conflicts.
