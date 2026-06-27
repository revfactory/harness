# Nội dung Ra mắt Harness — Đa nền tảng

> **Lưu ý:** Nội dung bài đăng dưới đây (trong các code block) được viết bằng tiếng Anh có chủ đích, vì đây là nội dung dùng để đăng trực tiếp lên các nền tảng tiếng Anh (Hacker News, Reddit, Twitter/X, Dev.to). Chỉ phần tiêu đề mục và ghi chú cấu trúc được dịch sang tiếng Việt.

---

## 1. Hacker News (Show HN)

### Tiêu đề

```
Show HN: Harness – A Claude Code plugin that designs AI agent teams from a single prompt
```

### Nội dung

```
I've been using Claude Code's agent teams for months, and the same problem kept coming up: every time I set up a multi-agent workflow, I was reinventing the wheel. Defining agent roles, writing skill files, figuring out which coordination pattern to use, wiring up data passing between agents — it was a 2-hour yak shave before the actual work could start.

So I built Harness. It's a Claude Code plugin — a "meta-skill" — that automates the entire process. You say "build a harness for this project" and it runs a 6-phase pipeline:

  1. Analyzes your domain and codebase
  2. Selects from 6 architecture patterns (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation)
  3. Generates agent definition files (.claude/agents/)
  4. Generates skills with Progressive Disclosure (.claude/skills/)
  5. Wires up orchestration with data-passing protocols and error handling
  6. Validates with trigger testing and with/without-skill A/B comparisons

I ran a controlled experiment across 15 software engineering tasks at three difficulty levels. Results:

  - +60% average quality score (49.5 → 79.3)
  - 100% win rate — the harnessed version won all 15 comparisons
  - 32% less output variance
  - Effect scales with task complexity: +23.8 on basic, +29.6 on advanced, +36.2 on expert tasks

The insight is straightforward: LLM code agents are capable but directionless. Give them structured pre-configuration — who does what, how they coordinate, what "done" looks like — and output quality jumps dramatically.

I also generated 100 production-ready harness configurations across 10 domains (content creation, software dev, data/AI, business strategy, education, etc.) and open-sourced them as a companion repo. 1,808 files total.

The plugin works with Claude Code's experimental Agent Teams system. Install via the plugin marketplace or copy the skill files directly.

GitHub: https://github.com/revfactory/harness
100 ready-made harnesses: https://github.com/revfactory/harness-100
A/B test results & paper: https://github.com/revfactory/claude-code-harness

Happy to answer questions about the architecture patterns, the research methodology, or how the meta-skill generation loop works.
```

---

## 2. Reddit

### 2a. r/ClaudeAI

**Tiêu đề:** `I built a Claude Code plugin that designs agent teams for you — 60% quality improvement in A/B tests`

**Nội dung:**

```
I kept running into the same friction with Claude Code's agent teams: setting up agents, writing skills, choosing coordination patterns, and wiring orchestration was taking longer than the actual task.

So I built **Harness** — a meta-skill (Claude Code Plugin) that does all of that from a single prompt.

**How it works:**

You say "build a harness for this project" and it runs a 6-phase pipeline:
- Analyzes your codebase and domain
- Picks an architecture pattern (6 options: Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation)
- Generates `.claude/agents/` and `.claude/skills/` files
- Sets up orchestration with inter-agent communication
- Validates with trigger tests and A/B comparisons

**What surprised me — the research results:**

I ran controlled A/B tests across 15 software engineering tasks:
- **+60% quality improvement** (avg score went from 49.5 → 79.3)
- **100% win rate** — harnessed version won every single comparison
- **The harder the task, the bigger the gain** — expert-level tasks saw +36.2 point improvements

This makes intuitive sense: you wouldn't throw a team of contractors at a house without blueprints. Same logic applies to AI agents.

**Companion resource:**

I generated [100 ready-made harnesses](https://github.com/revfactory/harness-100) across 10 domains (1,808 files). Content creation, software dev, data/AI, marketing, education, legal, health — each with 4-5 specialist agents and orchestrator skills.

**Getting started:**

```
/plugin marketplace add revfactory/harness
/plugin install harness@harness
```

Then just say: "Build a harness for [your domain]"

GitHub: https://github.com/revfactory/harness

Requires Agent Teams enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

Would love feedback from anyone using Claude Code's agent teams. What domains are you building for?
```

### 2b. r/MachineLearning

**Tiêu đề:** `[P] Harness: Structured Pre-Configuration for LLM Code Agents — +60% Quality, 100% Win Rate in A/B Tests`

**Nội dung:**

```
**TL;DR:** Structured pre-configuration (defining agent roles, coordination patterns, and skill specifications before execution) improves LLM code agent output quality by +60% with 100% win rate across 15 tasks.

---

**Problem:** LLM-based code agents (Claude Code, Cursor, etc.) are increasingly capable but produce inconsistent quality. The same model with the same task can give a 40/100 or an 80/100 depending on how the work is structured. There's no systematic way to reduce this variance.

**Approach:** I built **Harness**, a "meta-skill" for Claude Code that automates structured pre-configuration. Given a domain/project, it:

1. Analyzes the task space
2. Selects from 6 multi-agent architecture patterns (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation)
3. Generates agent definitions with role boundaries and communication protocols
4. Creates skills with Progressive Disclosure (3-tier context loading)
5. Wires orchestration and error handling
6. Validates with trigger testing and with/without comparison

**Experimental results** (controlled A/B across 15 SE tasks, 3 difficulty levels):

| Metric | Without | With | Delta |
|--------|---------|------|-------|
| Avg Quality Score | 49.5 | 79.3 | **+60%** |
| Win Rate | — | — | **15/15 (100%)** |
| Output Variance | — | — | **-32%** |

Key finding: **effect scales with task complexity**.
- Basic tasks: +23.8
- Advanced: +29.6
- Expert: +36.2

This aligns with the hypothesis that structured decomposition matters most when the search space is large and the agent needs to maintain coherence across multiple subtasks.

**Artifacts:**
- Plugin (meta-skill): https://github.com/revfactory/harness
- 100 generated harness configs across 10 domains: https://github.com/revfactory/harness-100
- Experimental methodology & results: https://github.com/revfactory/claude-code-harness

Paper reference: Hwang, M. (2026). "Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality."

Happy to discuss the experimental design, pattern selection heuristics, or the progressive disclosure mechanism.
```

### 2c. r/programming

**Tiêu đề:** `Show r/programming: A plugin that auto-generates multi-agent AI teams from your codebase — with A/B tested results`

**Nội dung:**

```
I've been working with Claude Code's agent teams — think of it as spawning multiple AI "workers" that coordinate on complex tasks. The problem: setting up these teams is tedious. You need to define roles, write skill files, pick a coordination pattern, wire data passing, handle errors. Every. Single. Time.

**Harness** is a Claude Code plugin that automates all of it. One prompt → full agent team.

**What it actually generates:**

```
your-project/
├── .claude/
│   ├── agents/          # Agent definitions (roles, protocols, comms)
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # What each agent knows how to do
│       ├── analyze/
│       │   └── skill.md
│       └── build/
│           ├── skill.md
│           └── references/
```

**The 6 architecture patterns it picks from:**

- **Pipeline** — A → B → C (code gen → review → test → deploy)
- **Fan-out/Fan-in** — parallel agents, merged results (multi-reviewer code audit)
- **Expert Pool** — dynamically pick the right specialist
- **Producer-Reviewer** — one builds, one QAs
- **Supervisor** — central coordinator dispatching tasks
- **Hierarchical Delegation** — recursive top-down decomposition

**Does it actually work?**

Ran a controlled experiment. 15 tasks. 3 difficulty levels. With-harness vs without-harness.

- +60% quality score
- 100% win rate (15/15)
- 32% less output variance
- Expert tasks benefited most (+36.2 points)

The companion repo has 100 pre-built harnesses across 10 domains: https://github.com/revfactory/harness-100

**Install:**

```
/plugin marketplace add revfactory/harness
/plugin install harness@harness
```

Then: "Build a harness for this project"

Source: https://github.com/revfactory/harness

Requires Claude Code with Agent Teams enabled.
```

---

## 3. Chuỗi Twitter/X

### Tweet 1 — Hook

```
I built a tool that designs AI agent teams.

Not individual agents — entire coordinated teams with roles, skills, communication protocols, and orchestration.

One prompt. Full team. 60% quality improvement in A/B tests.

It's called Harness, and it's open source.

🧵👇
```

### Tweet 2 — Vấn đề

```
The problem with AI code agents:

They're capable but directionless.

Same model, same task → wildly different quality. Sometimes 40/100, sometimes 80/100.

The missing piece isn't intelligence. It's structure.

[IMAGE: Side-by-side comparison showing scattered vs. organized agent output]
```

### Tweet 3 — Giải pháp

```
Harness is a Claude Code Plugin — a "meta-skill" that designs multi-agent teams.

Say "build a harness for this project" and it runs a 6-phase pipeline:

1. Domain Analysis
2. Architecture Design (6 patterns)
3. Agent Definition Generation
4. Skill Generation
5. Orchestration
6. Validation & Testing

[IMAGE: Workflow diagram showing the 6 phases]
```

### Tweet 4 — Mẫu kiến trúc

```
6 battle-tested coordination patterns:

→ Pipeline: sequential (gen → review → test)
⟐ Fan-out/Fan-in: parallel then merge
♠ Expert Pool: pick the right specialist
⇄ Producer-Reviewer: build then QA
◆ Supervisor: central dispatch
△ Hierarchical: recursive delegation

It picks the right one for your domain.

[IMAGE: Visual of the 6 architecture pattern cards]
```

### Tweet 5 — Nghiên cứu

```
I didn't just ship it — I measured it.

15 software engineering tasks. 3 difficulty levels. Controlled A/B tests.

Results:
• +60% average quality score
• 100% win rate (15/15 tasks)
• -32% output variance
• Harder tasks = bigger gains

The effect SCALES with complexity.

[IMAGE: Bar chart from landing page showing Basic/Advanced/Expert results]
```

### Tweet 6 — Phát hiện về quy mô

```
This is the key insight:

Basic tasks: +23.8 improvement
Advanced tasks: +29.6
Expert tasks: +36.2

The more complex the task, the more structure matters.

You wouldn't send contractors to build a house without blueprints. Same principle — for AI agents.
```

### Tweet 7 — Harness 100

```
To prove it generalizes, I generated 100 production-ready harness configurations across 10 domains:

• Content Creation
• Software Development
• Data & AI
• Business Strategy
• Education
• Marketing
• Legal, Health, and more

1,808 files. All open source.

github.com/revfactory/harness-100
```

### Tweet 8 — Demo: Bắt đầu

```
Getting started takes 30 seconds:

/plugin marketplace add revfactory/harness
/plugin install harness@harness

Then try:

"Build a harness for deep research"
"Build a harness for full-stack website development"
"Build a harness for code review"

It analyzes your project and generates a custom agent team.

[GIF: Screen recording of running "build a harness" in Claude Code]
```

### Tweet 9 — CTA

```
Harness is Apache 2.0 licensed.

⭐ Plugin: github.com/revfactory/harness
📦 100 harnesses: github.com/revfactory/harness-100
📄 Research: github.com/revfactory/claude-code-harness

If you're using Claude Code, try it.
If you're building with AI agents, the architecture patterns alone are worth reading.

Stars welcome — helps others find it.
```

---

## 4. Bài viết Dev.to

### Tiêu đề

```
How I Built a Meta-Skill That Designs AI Agent Teams — and Proved It Works with A/B Tests
```

### Tags

`#ai #claude #agents #opensource`

### Nội dung

```markdown
## The problem nobody talks about

AI code agents are getting remarkably capable. Claude Code, Cursor, Copilot — they can write functions, refactor code, even build entire features. But there's a dirty secret: **output quality is wildly inconsistent**.

The same model, given the same task, can produce a 40/100 result or an 80/100 result depending on... what, exactly? Luck? Context window state? The phase of the moon?

I've been using Claude Code's experimental Agent Teams feature for months — spawning multiple AI "workers" that coordinate on complex tasks. And I kept hitting the same wall: **setting up these teams was harder than the work itself**.

Every time I wanted a multi-agent workflow, I had to:

1. Figure out which agents I needed
2. Write agent definition files with roles and protocols
3. Create skill files for each agent
4. Choose a coordination pattern
5. Wire up data passing and error handling
6. Test that triggers fired correctly

This 2-hour yak shave happened before a single line of productive work.

So I built a tool to automate it.

## What Harness does

**Harness** is a Claude Code Plugin — specifically, a "meta-skill" that designs domain-specific agent teams, defines specialized agents, and generates the skills they use.

You say one thing:

```
Build a harness for this project
```

And it runs a structured 6-phase pipeline.

### Phase 1: Domain Analysis

Harness reads your codebase and conversation context to understand:

- What domain you're working in
- What types of tasks are involved (generation, validation, editing, analysis)
- What existing agents/skills exist (to avoid conflicts)
- Your technical expertise level (adjusts communication accordingly)

### Phase 2: Team Architecture Design

This is where it gets interesting. Harness selects from **6 architecture patterns**:

| Pattern | When to use |
|---------|-------------|
| **Pipeline** | Sequential dependent tasks (code gen → review → test → deploy) |
| **Fan-out/Fan-in** | Parallel independent tasks (multi-reviewer code audit) |
| **Expert Pool** | Dynamic specialist selection based on context |
| **Producer-Reviewer** | Generate then quality-check |
| **Supervisor** | Central agent with dynamic task distribution |
| **Hierarchical Delegation** | Top-down recursive decomposition |

It also decides between Agent Teams (multiple agents communicating directly via `SendMessage`) and Subagents (one-off tasks with no inter-agent communication).

### Phase 3: Agent Definition Generation

Each agent gets a definition file at `.claude/agents/{name}.md` with:

- Core role and responsibilities
- Operating principles
- Input/output protocols
- Error handling strategies
- Team communication contracts (who talks to whom)

### Phase 4: Skill Generation

Skills are the "how" — each agent's capabilities. Generated at `.claude/skills/{name}/skill.md` with:

- YAML frontmatter (name, aggressive trigger description)
- Markdown body (< 500 lines)
- Progressive Disclosure: metadata always loaded, body loaded on trigger, references loaded on demand

The trigger description is deliberately "pushy" — Claude tends to be conservative about firing skills, so the description over-specifies when the skill should activate.

### Phase 5: Integration & Orchestration

The orchestrator skill wires everything together:

- **Message-based** data passing (`SendMessage` for real-time coordination)
- **Task-based** tracking (`TaskCreate`/`TaskUpdate` for dependencies)
- **File-based** artifacts (structured output in `_workspace/` directory)
- Error handling: retry once, then proceed without and note the gap

### Phase 6: Validation & Testing

This is where most agent frameworks stop — but it's where quality actually lives:

- Structure checks (files in right places, frontmatter valid)
- Trigger verification (should-trigger and should-NOT-trigger queries)
- **With-skill vs without-skill A/B comparison** — spawns two subagents, one with the skill and one without, then compares output
- Dry-run testing of the full orchestration pipeline
- Iterative refinement loop

## The research: does it actually work?

I didn't want to just ship vibes. I ran a **controlled A/B experiment** across 15 software engineering tasks at three difficulty levels.

### Setup

- 15 tasks spanning basic, advanced, and expert complexity
- Each task run twice: once with Harness pre-configuration, once without
- Quality scored on a standardized rubric

### Results

| Metric | Without Harness | With Harness | Improvement |
|--------|:-:|:-:|:-:|
| Average Quality Score | 49.5 | 79.3 | **+60%** |
| Win Rate | — | — | **100% (15/15)** |
| Output Variance | — | — | **-32%** |

### The scaling insight

The most interesting finding: **effectiveness scales with task complexity**.

- Basic tasks: +23.8 point improvement
- Advanced tasks: +29.6
- Expert tasks: +36.2

This makes intuitive sense. For a simple task, the agent can stumble into a decent solution. For a complex task with many interdependent parts, the probability of maintaining coherence drops — unless you give it structure.

It's the same reason construction projects need blueprints and film productions need shot lists. The more complex the output, the more structure the process needs.

## 100 ready-made harnesses

To prove this generalizes beyond my own projects, I generated **100 production-ready harness configurations** across 10 domains:

- Content Creation (blog posts, social media, video scripts)
- Software Development (full-stack, mobile, DevOps)
- Data & AI (pipelines, ML ops, analytics)
- Business Strategy (market analysis, competitive intel)
- Education (curriculum design, assessment)
- Marketing (campaigns, SEO, brand)
- Legal, Health, Finance, and more

That's **1,808 markdown files** total — each harness with 4-5 specialist agents, an orchestrator skill, and domain-specific skills. All available in English and Korean (200 packages).

Repository: [revfactory/harness-100](https://github.com/revfactory/harness-100)

## Getting started

### Install

```shell
# Add the marketplace
/plugin marketplace add revfactory/harness

# Install the plugin
/plugin install harness@harness
```

### Requirements

- Claude Code with Agent Teams enabled:
  ```
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
  ```

### Use it

Just say any of these in Claude Code:

```
Build a harness for this project
Design an agent team for deep research
Set up a harness for code review
Build a harness for full-stack website development
```

Harness analyzes your context and generates a complete agent team tailored to your domain.

### What you get

```
your-project/
├── .claude/
│   ├── agents/          # Agent definitions
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # Skill files
│       ├── analyze/
│       │   └── skill.md
│       └── build/
│           ├── skill.md
│           └── references/
```

## What I learned building this

**1. Trigger descriptions need to be aggressive.** Claude is conservative about activating skills. Writing "PDF processing skill" means it almost never fires. Writing "Use this skill for ANY task involving .pdf files including reading, extracting, merging, splitting..." actually works.

**2. Progressive Disclosure is essential for context management.** Loading everything upfront wastes the context window. The 3-tier system (metadata always → body on trigger → references on demand) keeps things lean.

**3. The "who" and "how" should be separate files.** Agent definitions (who does what) and skills (how to do it) are different concerns. Coupling them makes reuse impossible. Separating them means you can mix and match.

**4. Validation is where the value actually lives.** Generating agent files is table stakes. The trigger testing, A/B comparisons, and iterative refinement loop are what make the output production-quality rather than demo-quality.

**5. Effect scales with complexity.** This was the most surprising and most important finding. Simple tasks don't need much structure. Complex tasks need a lot. Harness adds the most value exactly where you need it most.

## Links

- **Harness plugin**: [github.com/revfactory/harness](https://github.com/revfactory/harness)
- **100 ready-made harnesses**: [github.com/revfactory/harness-100](https://github.com/revfactory/harness-100)
- **A/B test research**: [github.com/revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- **Paper**: Hwang, M. (2026). "Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality."

Apache 2.0 licensed. Stars and feedback welcome.
```

---

## 5. Lịch nội dung — Kế hoạch ra mắt phối hợp

Mọi thời gian theo **UTC**. Thiết kế để khuếch đại tối đa đa nền tảng trong khung 48 giờ.

### Ngày 1 (Ngày ra mắt)

| Giờ (UTC) | Nền tảng | Nội dung | Ghi chú |
|------------|----------|---------|-------|
| 08:00 | **Hacker News** | Bài Show HN | Đăng sáng sớm giờ US West Coast. Traffic HN đạt đỉnh 9-11h sáng PT. |
| 08:30 | **Twitter/X** | Chuỗi tweet (Tweet 1-9) | Đăng toàn bộ chuỗi ngay lập tức. Pin Tweet 1. |
| 09:00 | **r/ClaudeAI** | Bài Reddit | Cộng đồng chính. Đối tượng tiếp nhận tốt nhất. |
| 10:00 | **r/programming** | Bài Reddit | Đối tượng developer rộng hơn. Đợi 1 giờ để tránh bị đánh dấu spam. |
| 12:00 | **Dev.to** | Bài viết đầy đủ | Nội dung dài hơn cho tìm kiếm & khám phá. |

### Ngày 2 (Theo dõi tiếp)

| Giờ (UTC) | Nền tảng | Nội dung | Ghi chú |
|------------|----------|---------|-------|
| 08:00 | **r/MachineLearning** | Bài Reddit | Đối tượng tập trung nghiên cứu. Dẫn bằng phương pháp luận. |
| 10:00 | **Twitter/X** | Chuỗi quote-tweet với góc nhìn mới | "Kết quả nghiên cứu khiến tôi bất ngờ..." — nhấn vào phát hiện về quy mô. |
| 14:00 | **Hacker News** | Trả lời comment | Tương tác sâu. Câu trả lời kỹ thuật giúp tăng ranking. |

### Ngày 3+ (Duy trì)

| Giờ (UTC) | Nền tảng | Nội dung | Ghi chú |
|------------|----------|---------|-------|
| Liên tục | **Twitter/X** | Trả lời quote/mention | Tương tác với mọi người chia sẻ lại. |
| Liên tục | **GitHub** | Trả lời issue/star | Phản hồi issue nhanh báo hiệu duy trì chủ động. |
| +3 ngày | **Twitter/X** | Bài đăng riêng "100 harnesses" | Nội dung riêng cho repo song hành. |
| +5 ngày | **Dev.to** | Bài theo dõi: "5 architecture patterns for AI agent teams" | Nội dung lâu bền dẫn về repo. |
| +7 ngày | **Twitter/X** | Cập nhật mốc quan trọng | "500 stars trong một tuần" hoặc bằng chứng xã hội tương tự. |

### Checklist ra mắt

- [ ] README GitHub đã hoàn thiện với badge, banner, hướng dẫn cài đặt rõ ràng
- [ ] Landing page (index.html) đã live và được link từ README
- [ ] Repo harness-100 công khai với README rõ ràng
- [ ] claude-code-harness (repo nghiên cứu) công khai
- [ ] Mọi repo GitHub có topic/tag phù hợp để dễ tìm thấy
- [ ] Bio profile Twitter đã cập nhật nhắc đến Harness
- [ ] Chuẩn bị 2-3 GIF/screenshot demo cho chuỗi Twitter
- [ ] Đã soạn trước câu trả lời cho các câu hỏi HN khả dĩ (phương pháp luận, hạn chế, so sánh với công cụ khác)

---

## Ghi chú tối ưu theo từng nền tảng

### Hacker News
- Tiêu đề bắt đầu bằng "Show HN:" — bắt buộc cho bài Show HN
- Chỉ plain text, không render markdown
- Dẫn bằng vấn đề, không dẫn bằng giải pháp
- Đưa số liệu cụ thể vào sớm
- Kết bằng "Happy to answer questions" — báo hiệu sẵn sàng tương tác

### Reddit
- Mỗi subreddit có góc nhìn khác nhau: r/ClaudeAI (thực tế/hướng dẫn), r/MachineLearning (nghiên cứu/phương pháp luận), r/programming (kỹ thuật/khoe sản phẩm)
- Không bao giờ cross-post — mỗi bài là nội dung gốc
- Không nói "my project" quá nhiều lần — tập trung vào vấn đề của người đọc

### Twitter/X
- Tweet hook là tất cả — phải dừng được hành vi lướt
- Chuỗi tweet phải vẫn hiểu được nếu ai đó chỉ đọc tweet 1 và 9
- Đánh dấu vị trí ảnh/GIF — nội dung hình ảnh tăng tương tác 3 lần
- Kết bằng CTA và link rõ ràng

### Dev.to
- Bài dài cho SEO — sẽ rank cho "AI agent teams", "Claude Code plugin", "multi-agent orchestration"
- Bao gồm code block — người đọc Dev.to mong đợi độ sâu kỹ thuật
- Section "What I learned" thúc đẩy tương tác và lượt chia sẻ
- Tag quyết định khả năng phân phối — dùng tag có traffic cao
