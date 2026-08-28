<p align="center">
  <img src="https://img.shields.io/badge/Version-2.1.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Execution_Modes-3-teal.svg" alt="3 Execution Modes">
  <img src="https://img.shields.io/badge/Patterns-6+Quality-orange.svg" alt="Patterns">
</p>

# Harness v2 — The Team-Architecture Factory for Claude Code

**English** | [한국어](README_KO.md)

> **Harness is a team-architecture factory for Claude Code.** One sentence — **"build a harness for this project"** · **"하네스 구성해줘"** — and the plugin turns your domain description into an agent team and the skills they use.

## What's new in v2

v2 is a ground-up rebuild for the current Claude Code multi-agent runtime:

- **Three native execution modes.** v1 knew two modes built on the experimental `TeamCreate` API, which no longer exists. v2 targets what actually ships today:
  1. **Workflow orchestration** — deterministic scripts (`pipeline()` / `parallel()` / schemas / budgets) for fan-outs, verification loops, and large-scale runs
  2. **Persistent agent collaboration** — named agents + `SendMessage` + shared task lists, with context retained across turns
  3. **Sub-agent delegation** — lightweight one-shot parallel dispatch
- **Workflow-native quality patterns.** Adversarial verification, judge panels, loop-until-dry, multi-modal sweeps, completeness critics — codified so generated harnesses filter out plausible-but-wrong output.
- **No experimental flags.** The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` dependency is gone entirely.
- **Sane model policy.** v1 pinned every agent to `model: "opus"`. v2 selects a tier per agent — opus / sonnet — based on the task's complexity, duration, autonomy, and latency needs, and forbids unjustified blanket pins.
- **`/harness:evolve` actually ships.** The evolution mechanism v1 only documented is now a real skill: it captures the delta between your initial and current harness, generalizes feedback, and feeds it back into agents/skills/orchestrators.
- **v1 migration built in.** The factory detects v1 artifacts (`TeamCreate`, `TeamDelete`, experimental flags) and offers a mechanical migration path.

## Core features

- **Agent team design** — six architecture patterns (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation), each mapped to its best v2 execution mode
- **Skill generation** — context-efficient skills via Progressive Disclosure, with reuse checks before generating duplicate agents or skills
- **Orchestration** — data-passing protocols (structured schemas, files, messages, tasks), error handling, resume support
- **Verification** — trigger evals, dry runs, with-skill vs. without-skill A/B testing (optionally as a workflow itself)
- **Evolution** — `/harness:evolve` turns usage feedback into measurable next-generation improvements

## Category — Where Harness Sits

Harness lives at the **L3 Meta-Factory** layer of the Claude Code ecosystem — the layer that generates other harnesses rather than being one. Inside L3, it occupies the **Team-Architecture Factory** sub-layer.

| Layer | What it does | Neighbors we coexist with |
|-------|--------------|---------------------------|
| **L3 — Meta-Factory / Team-Architecture Factory** (us) | Domain sentence → agent team + skills, via six pre-defined team patterns | — |
| L3 — Meta-Factory / Runtime-Configuration Factory | Deterministic, repeatable runtime configurations | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Codex Runtime Port | Same concept, Codex runtime | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | Standardize skills/rules/hooks across multiple harnesses | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon generates deterministic runtime configurations. Harness generates team architectures plus the skills agents use. Pick Archon for runtime determinism, Harness for team architecture, or combine them.

## Star History

<a href="https://www.star-history.com/?repos=revfactory%2Fharness&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
 </picture>
</a>

## Workflow

```
Phase 0: Audit existing harness (new / extend / maintain — v1 artifacts detected here)
Phase 1: Domain analysis (incl. control-flow shape of the work)
Phase 2: Execution mode & team architecture design
Phase 3: Agent definitions (.claude/agents/)
Phase 4: Skill generation (.claude/skills/)
Phase 5: Orchestration & CLAUDE.md pointer
Phase 6: Verification & testing
Phase 7: Maintenance — evolution via /harness:evolve
```

## Install

### Via marketplace

```shell
/plugin marketplace add revfactory/harness
/plugin install harness@harness-marketplace
```

### As global skills

```shell
cp -r skills/harness ~/.claude/skills/harness
cp -r skills/evolve ~/.claude/skills/harness-evolve
```

No environment variables or experimental flags required.

## Usage

```
하네스 구성해줘
build a harness for this project
design an agent team for <domain>
```

After using a generated harness:

```
하네스 회고해줘 / evolve the harness with this feedback
```

### Choosing an execution mode

| Mode | Primitive | When |
|------|-----------|------|
| **Workflow orchestration** | `Workflow` scripts | Control flow is deterministic: enumerable fan-outs, verification loops, large scale, structured outputs |
| **Persistent agents** | `Agent(name:)` + `SendMessage` + tasks | Long-lived specialists that keep context; iterative feedback and negotiation |
| **Sub-agent delegation** | one-shot `Agent` calls | Fire-and-forget parallel work; results only |

The factory picks the mode from the **shape of the control flow**, not from team size — and mixes modes per phase when that fits better.

## Generated artifacts

```
your-project/
├── .claude/
│   ├── agents/          # agent definitions (who)
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # skills (how) + one orchestrator (who-when-in-what-order)
│       ├── analyze/SKILL.md
│       └── build/SKILL.md
└── CLAUDE.md            # minimal pointer: trigger rule + change history
```

## Migrating from v1

See [docs/migration-v1-to-v2.md](docs/migration-v1-to-v2.md). Summary: remove `TeamCreate`/`TeamDelete`/broadcast/flag references, convert fan-outs to Workflow scripts, rewrite remaining collaboration with named agents + `SendMessage`, drop blanket `model: "opus"` pins. The factory automates this when it detects v1 artifacts (Phase 0).

## Prior results (v1)

A controlled A/B on 15 software-engineering tasks measured the effect of structured pre-configuration on LLM code-agent output quality: mean quality 49.5 → 79.3 (+60%), 15/15 win rate, −32% output variance (n=15, author-run, see [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)). Treat these as author-measured numbers; run your own pilot for adoption decisions.

## License

Apache 2.0
