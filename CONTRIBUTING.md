# Contributing to Harness

Thanks for considering a contribution to **Harness** — a Claude Code meta-skill factory that designs agent teams and generates skills.

This document covers: response SLAs, how to contribute, development setup, PR conventions, commit message rules, code of conduct, and maintainer list.

---

## Response SLA (commitments)

These are the maintainer response targets for this repository. They are **conservative** so that a small maintainer team can realistically keep them while scaling.

| Surface | Target | Notes |
|---------|--------|-------|
| PR — 1st response | **< 72h** | Business days. A "1st response" means at minimum a label + one comment acknowledging the PR. |
| Issue triage & labeling | **< 48h** | Every new issue gets `needs-triage` removed and a type label (`bug` / `enhancement` / `question` / `discussion`) within 48h. |
| Bug resolve (P0 / P1) | **< 14d** | P0 = data loss / security / broken install. P1 = common path broken. P2/P3 tracked on roadmap without a hard SLA. |
| Security report | **< 7d** | Initial acknowledgement within 7 days. Patch target 30 days. Please see **Security** section below for the private channel. |
| Release cadence | **every 2 weeks** | Biweekly tag unless there is nothing shippable. P0 fixes may cut an off-schedule patch release. |

If we miss an SLA, please feel free to ping the issue/PR — that is not rude, it is the agreed feedback loop.

---

## How to Contribute

Different kinds of contributions go through different entry points. Pick the one that fits.

### Bug report

- Open an issue using the **Bug report** form (`.github/ISSUE_TEMPLATE/bug_report.yml`).
- Required: runtime, reproduction steps, expected vs actual, OS. Include the Claude Code version and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag state for Claude reports, or the Codex app/version and `harness-codex` install path for Codex reports.
- Small reproductions (< 30 lines) are ideal. If your repro needs a full project, link a public fork.

### Feature request

- Open an issue using the **Feature request** form.
- We expect a short "what problem does this solve" paragraph. If you have a proposal, put it in the PR-ready shape (which of the 6 team-architecture patterns does it extend / replace?).

### Question

- Open an issue using the **Question** form, **or** start a thread in [GitHub Discussions](https://github.com/revfactory/harness/discussions) if the matter is open-ended.

### Discussion (RFC-sized ideas)

- Prefer GitHub Discussions. Only promote to an issue once there is rough consensus on direction.

### Pull Request

- See **Pull Request Guidelines** below.
- Small PRs merge faster. Anything > 400 lines of diff should probably have been a Discussion first.

### Security

- Do **not** open a public issue for anything that could be abused.
- Email: `robin.hwang@kakaocorp.com` with subject prefix `[harness-security]`.
- We aim to acknowledge within 7 days (see SLA table).

---

## Development Setup

### Prerequisites

- Claude Code `v2.x` for the Claude plugin (Agent Teams API required)
- Codex for the local `harness-codex` plugin path
- Node.js `>= 18` (for local tooling used in CI)
- Git

### Environment flag

Harness currently requires Claude Code's experimental Agent Teams feature. Set the flag in your shell profile or per-session:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

This flag applies to the Claude Code plugin only. The Codex port does not use Claude Code Agent Teams primitives. We track the Claude dependency in `docs/experimental-dependency.md` (if Anthropic promotes the flag to stable, we update the README within 72h per the SLA above).

### Local plugin link

To test your changes in a local Claude Code session without publishing to the marketplace:

```bash
# From your checkout
claude plugin link ./harness

# Verify
claude plugin list | grep harness
```

Unlink with `claude plugin unlink harness` when you're done.

### Local Codex plugin

To test the Codex port, open this repository in Codex and install `harness-codex` from the `Harness Local` marketplace. The Codex plugin lives under `plugins/harness-codex/` and is exposed through `.agents/plugins/marketplace.json`; see `docs/codex-quickstart.md`.

### Running the meta-skill

```bash
claude "build a harness for a fintech risk-assessment team"
```

The Claude plugin scaffolds agents and skills under `.claude/agents/` and `.claude/skills/` in the target project. The Codex plugin generates `.agents/skills/`, `AGENTS.md`, and `_workspace/` artifacts instead.

### Tests & lints

- Markdown lint: `npx markdownlint '**/*.md'`
- YAML lint (issue templates & workflows): `npx yaml-lint .github/`
- Skill metadata validation: `python scripts/validate_skills.py` (if present)

CI runs these on every PR. Local execution is encouraged but not required — we won't block on CI-caught issues that are trivial to fix on merge.

---

## Pull Request Guidelines

### Branch naming

Use the `type/short-description` shape:

| Prefix | Use for | Example |
|--------|---------|---------|
| `feat/` | New user-visible capability | `feat/expert-pool-variance-mode` |
| `fix/` | Bug fix | `fix/agent-teams-flag-detection` |
| `docs/` | Docs-only changes | `docs/quickstart-gemini-section` |
| `refactor/` | Internal structure, no behavior change | `refactor/skill-loader-split` |
| `chore/` | Build, deps, housekeeping | `chore/upgrade-markdownlint` |
| `test/` | Tests only | `test/fan-out-fan-in-e2e` |

### Commit message language

- **Korean and English are both accepted.** Write in whichever you are more precise in.
- If the change will appear in the CHANGELOG or release notes, please also provide an English title in the PR description so downstream readers can follow.

### PR template

Every PR body is pre-filled from `.github/PULL_REQUEST_TEMPLATE.md`. Please fill in:

- **Summary** (what & why, 2–4 sentences)
- **Motivation** (link issue, reference research, or 1-line rationale)
- **Scope of change** (checklist of touched surfaces)
- **Tests** (what you ran / added)
- **CHANGELOG** (did you update `CHANGELOG.md`? Y/N/NA)
- **SemVer impact** (patch / minor / major — see next section)

### Review expectation

- One approving review from a maintainer is required.
- We try to respond on PRs within 72h (see SLA). If you're blocked, ping.

---

## Commit Message Convention

We follow a light variant of **Conventional Commits** that maps directly to SemVer.

```
<type>(<scope>)!: <short summary>

<body — optional>

<footer — optional>
```

### Types & SemVer mapping

| Commit type | SemVer impact | Example |
|-------------|---------------|---------|
| `feat!:` or `BREAKING CHANGE:` in footer | **major** (e.g. 1.x → 2.0) | `feat!: rename primary pattern "Supervisor" → "Orchestrator"` |
| `feat:` | **minor** (e.g. 1.2 → 1.3) | `feat: add Producer-Reviewer variance metric` |
| `fix:` | **patch** (e.g. 1.2.3 → 1.2.4) | `fix: correct flag detection on zsh` |
| `docs:` / `chore:` / `refactor:` / `test:` | no release bump | `docs: clarify Gemini roadmap` |

- Korean summaries are fine: `feat: 전문가 풀 패턴에 분산 지표 추가`.
- The `!` suffix (or `BREAKING CHANGE:` footer) is the **only** canonical major-version trigger. Please do not set it lightly.

### Release tagging

- Releases are cut every 2 weeks (see SLA).
- Tagging happens from `main` after CI passes and CHANGELOG is updated.
- Tags follow `vMAJOR.MINOR.PATCH` (e.g. `v1.3.0`).

---

## Code of Conduct

This project adheres to the **Contributor Covenant v1.4** — in short:

- Be welcoming and inclusive. Assume good intent.
- No harassment, no personal attacks, no discriminatory language.
- Critique ideas, not people. Back claims with references where possible.
- Maintainers may moderate, edit, or remove comments/commits/issues/PRs that violate these principles, and may ban offenders.

Full text: <https://www.contributor-covenant.org/version/1/4/code-of-conduct/>

Report Code of Conduct violations privately to `robin.hwang@kakaocorp.com` with subject prefix `[harness-coc]`.

---

## Maintainers

| Role | Handle | Area |
|------|--------|------|
| Lead maintainer | [@revfactory](https://github.com/revfactory) | Project direction, releases, final review |
| Contributor | [@hnts03](https://github.com/hnts03) | Skill templates, Korean documentation |
| Contributor | [@JunghwanNA](https://github.com/JunghwanNA) | Agent patterns, integration tests |
| Contributor | [@shaun0927](https://github.com/shaun0927) | Tooling, CI, infra |

New contributors become listed here after sustained contribution (not a single PR). Drop a note in a Discussion if you'd like to discuss a maintainer path.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as this repository (see [`LICENSE`](./LICENSE)).
