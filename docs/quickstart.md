# Quickstart — 5 Minutes to Your First Harness

> **Time budget: 5 minutes (strict).** If you are not at Step 5 within 5 minutes, stop and file an issue — that is a bug in this document, not a bug in you.

<!-- TODO: Loom embed — 60s screen recording showing Steps 1→5 end-to-end. Replace this comment with the `<iframe>` once recorded. -->

**What you will have at the end:** a working `.claude/agents/` directory with 3–5 domain-specialized agents, generated from a single-sentence prompt, ready to run on a sample task.

**Prerequisites (check before starting):**
- Claude Code **v2.x or later** (`claude --version` should return `2.x` or higher)
- A shell that persists `export` across commands (bash, zsh, or fish)
- Network access to `github.com` and `api.anthropic.com`

---

## Step 1 — Add the marketplace (60 seconds)

```bash
claude plugin marketplace add revfactory/harness
```

**What this does:** Registers the `harness` marketplace so Claude Code can discover plugins published by `revfactory`.

**Expected output:** `Added marketplace: revfactory/harness`

---

## Step 2 — Install the plugin and enable the Experimental flag (40 seconds)

```bash
claude plugin install harness@harness-marketplace
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

*(To persist the flag across shell sessions, append the `export` line to `~/.zshrc` or `~/.bashrc`.)*

**What this does:** Installs the `harness` plugin from the `harness` marketplace, then enables Agent Teams — the Claude Code API harness uses to orchestrate multi-agent workflows. See [`docs/experimental-dependency.md`](./experimental-dependency.md) for why the flag is required.

**Failure FAQ #1 — `AGENT_TEAMS not found` / teams don't instantiate**
**Cause:** Claude Code version is older than v2.x (Agent Teams was introduced in v2.0).
**Fix:** Run `claude --version`. If below 2.0, upgrade via `npm i -g @anthropic-ai/claude-code` (or your distribution's installer), then repeat Step 2.

---

## Step 3 — Generate a harness from one sentence (2 minutes)

```bash
claude "build a harness for a fintech risk-assessment team"
```

**What this does:** Invokes the `/harness:harness` meta-skill, which analyzes your domain sentence and scaffolds a team of specialized agents + their skills into `.claude/agents/` and `.claude/skills/` in the current directory.

**Try these alternate prompts** — any of them work:
- `claude "하네스 구성해줘 — 핀테크 리스크 평가 팀"` (Korean also works)
- `claude "build a harness for an e-commerce fraud-detection workflow"`
- `claude "design an agent team for technical due diligence on open-source repos"`

**Expected output:** A streaming plan, then confirmation that 3–5 agent `.md` files and their skills were written.

**Failure FAQ #2 — The Korean prompt returns nothing / the English one succeeds but Korean doesn't**
**Cause:** Locale or tokenizer misrouting; harness's orchestrator matches on Korean trigger words ("하네스 구성"), which are built into the skill definition.
**Fix:** If Korean fails, re-run with the English prompt above — the underlying skill is identical. If both fail, jump to Failure FAQ #3.

---

## Step 4 — Verify the generated files (30 seconds)

```bash
ls -la .claude/agents/
ls -la .claude/skills/
```

**What this does:** Confirms the meta-skill wrote files to the expected locations.

**Expected output:** 3–5 files per directory, with names reflecting your domain (e.g., `risk-analyst.md`, `compliance-reviewer.md`, `portfolio-monitor.md` for the fintech example).

**Failure FAQ #3 — "Nothing was generated" / directories are empty**
**Cause:** The plugin is not actually installed or is not active in the current project.
**Fix:** Run `claude plugin list`. If `harness@harness-marketplace` is absent, repeat Step 2. If present but inactive, run `claude plugin enable harness@harness-marketplace`, then repeat Step 3.

---

## Step 5 — Run a sample task against the new team (90 seconds)

Copy a realistic Jira-ticket-style prompt and hand it to your fresh team:

```bash
claude "Ticket FIN-427: A new corporate customer (mid-cap manufacturer, \$80M revenue, South Korea) has applied for a \$5M working-capital line. Produce a risk assessment covering (1) credit-history red flags, (2) sector concentration vs. our existing book, (3) regulatory exposure (KFTC, FSC). Output: a 1-page memo with a go/no-go recommendation."
```

**What this does:** Claude Code detects the new agents in `.claude/agents/`, routes the task through the team patterns harness generated (typically Producer-Reviewer or Expert-Pool for risk work), and returns a structured memo.

**Failure FAQ #4 — "The team doesn't execute / only one agent responds"**
**Cause:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` was set in the shell that ran Step 3 but not in the shell running Step 5 (happens when opening a new terminal).
**Fix:** Re-export in the current shell: `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, then re-run Step 5. To make permanent, add the line to your shell rc file.

**Failure FAQ #5 — "Too many API calls / cost anxiety"**
**Cause:** Multi-agent teams can fan out to 5+ parallel Claude calls per task. A single complex ticket can consume 50K–200K tokens.
**Fix:** Limit to a single task per run (don't chain `&&` multiple harness invocations), and use the `--max-turns` flag if your Claude Code version supports it. For production, gate harness invocations behind a cost-aware wrapper — see `docs/cost-controls.md` *(forthcoming)*.

---

## You're done

At this point you should have:

- [x] A `.claude/agents/` directory with domain-specialized agents
- [x] A `.claude/skills/` directory with their supporting skills
- [x] One successful sample-task execution
- [x] A working `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment

**Next reads:**
- [`docs/experimental-dependency.md`](./experimental-dependency.md) — Why the flag, and what we'll do when it changes
- [`revfactory/harness-100`](https://github.com/revfactory/harness-100) — Catalog of 100+ pre-built domain harnesses, if you'd rather clone than generate
- [`revfactory/claude-code-harness`](https://github.com/revfactory/claude-code-harness) — The A/B test harness we used to measure +60% quality on 15 tasks

**If you hit something this guide didn't cover:** open an issue with the `quickstart-gap` label and include: (a) which step failed, (b) `claude --version`, (c) the exact error message. The SLA for quickstart-gap issues is **48 hours** to first response (see `CONTRIBUTING.md`).
