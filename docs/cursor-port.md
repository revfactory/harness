# Cursor Port Guide — Using Harness Outside Claude Code

Harness is **Claude-Code-native** by design. This guide maps Harness outputs to **Cursor** (and similar IDEs) so you can reuse the same team architecture without Agent Teams APIs.

> For Codex runtime, see [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness).

---

## Path mapping

| Claude Code (Harness default) | Cursor equivalent |
|------------------------------|-------------------|
| `.claude/agents/{name}.md` | `.cursor/agents/{name}.md` or project rules |
| `.claude/skills/{name}/SKILL.md` | `.cursor/skills/{name}/SKILL.md` or `~/.cursor/skills-cursor/` |
| `CLAUDE.md` harness pointer | `.cursor/rules` or root `AGENTS.md` |
| `_workspace/` artifacts | Same — keep file-based handoff |

After Harness generates files under `.claude/`, copy or symlink:

```bash
mkdir -p .cursor/agents .cursor/skills
cp -r .claude/agents/* .cursor/agents/
cp -r .claude/skills/* .cursor/skills/
```

---

## Execution mode mapping

| Harness mode | Claude Code API | Cursor approach |
|--------------|-----------------|-----------------|
| **Agent Teams** (default) | `TeamCreate`, `SendMessage`, `TaskCreate` | Use **Task subagents** in parallel; file-based handoff via `_workspace/` |
| **Subagents** | `Agent` tool | Direct Task tool with `subagent_type` — closest match |
| **Hybrid** | Phase-level team/sub switching | Phase 1: parallel Task calls → Phase 2: single integrator agent |

Cursor does not expose `SendMessage` between subagents. **Compensate with:**

1. **File-based protocol** (Harness Phase 5-1) — each agent writes to `_workspace/{phase}_{agent}_{artifact}.ext`
2. **Orchestrator skill** — one skill reads all artifacts and spawns the next phase
3. **Explicit dependencies** in orchestrator Phase tables

---

## Trigger phrases in Cursor

Install the harness meta-skill globally:

```bash
cp -r skills/harness ~/.cursor/skills-cursor/harness
```

Then prompt:

```
帮我配置 harness：多源新闻情报团队
build a harness for this project
```

Cursor loads skills from `SKILL.md` frontmatter `description` — same trigger rules as Claude Code.

---

## Agent Teams flag

`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` applies to **Claude Code only**. Cursor users can ignore it; use subagent/Task patterns instead.

---

## Recommended workflow

1. Run Harness in Claude Code **or** copy the meta-skill to Cursor and say "build a harness for …"
2. Prefer **subagent + file handoff** orchestrator template (Template B) when targeting Cursor-only teams
3. Register a minimal pointer in `AGENTS.md`:

```markdown
## Harness: {domain}

**Trigger:** For {domain} tasks, use `{orchestrator-skill}` skill.
**Artifacts:** `_workspace/` (preserved between runs)
```

---

## Limitations

| Feature | Claude Code | Cursor |
|---------|-------------|--------|
| Live inter-agent messaging | Yes (`SendMessage`) | No — use files |
| Shared task board | Yes (`TaskCreate`) | Manual phase tables in orchestrator |
| Session team reconfigure | `TeamDelete` / `TeamCreate` | Re-run orchestrator phases |

For full Agent Teams fidelity, stay on Claude Code. For day-to-day IDE work, Template B + `_workspace/` is usually sufficient.

---

## See also

- [README FAQ Q3](../README.md) — multi-runtime roadmap
- [Gizele1/harness-init](https://github.com/Gizele1/harness-init) — cross-runtime scaffolder
- [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) — L2 workflow layer on top of harnesses
