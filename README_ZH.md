<p align="center">
  <img src="harness_banner.png" alt="Harness Banner" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.2.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Patterns-6_Architectures-orange.svg" alt="6 Architecture Patterns">
  <img src="https://img.shields.io/badge/Mode-Agent_Teams-green.svg" alt="Agent Teams">
  <a href="https://github.com/revfactory/harness/stargazers"><img src="https://img.shields.io/github/stars/revfactory/harness?style=social" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#类别--harness-所处的位置"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#类别--harness-所处的位置"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA%20%7C%20ZH-lightgrey" alt="i18n"></a>
</p>

# Harness — Claude Code 的团队架构工厂

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | **中文**

> **Harness 是面向 Claude Code 的团队架构工厂。** 只需说一句 **"build a harness for this project"**（English）、**"하네스 구성해줘"**（한국어）、**"ハーネスを構成して"**（日本語）或 **"帮我配置 harness"**（中文），插件就会把你的领域描述转化为一支 agent team 以及它们所用的 skill —— 从六种预定义的团队架构模式中挑选其一。

## 概述

Harness 借助 Claude Code 的 agent team 系统，把复杂任务分解为协同工作的专家 agent 团队。说一句 "build a harness for this project"，它就会自动生成贴合你领域的 agent 定义（`.claude/agents/`）与 skill（`.claude/skills/`）。

## 类别 — Harness 所处的位置

Harness 位于 Claude Code 生态的 **L3 Meta-Factory** 层 —— 这一层生成其他 harness，而非自身作为一个 harness。在 L3 内部，我们选择了一个具体的子层：**Team-Architecture Factory**。

| 层级 | 它做什么 | 共存的邻居 |
|-------|--------------|---------------------------|
| **L3 — Meta-Factory / Team-Architecture Factory**（我们） | 一句领域描述 → agent team + skill，经由 6 种预定义团队模式 | — |
| L3 — Meta-Factory / Runtime-Configuration Factory | 确定性、可复现的运行时配置 | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Codex Runtime Port | 相同理念，Codex 运行时 | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | 在多个 harness 之间统一 skill/规则/hook | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon 生成确定性的运行时配置。Harness 生成团队架构（pipeline、fan-out/fan-in、expert pool、producer-reviewer、supervisor、hierarchical delegation）以及 agent 所用的 skill。二者是同属 L3 的不同子层。需要运行时确定性就选 Archon，需要团队架构就选 Harness，也可以组合使用。

## Star History

<a href="https://www.star-history.com/?repos=revfactory%2Fharness&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=revfactory/harness&type=date&legend=top-left" />
 </picture>
</a>


## 核心特性

- **Agent Team 设计** —— 6 种架构模式：Pipeline、Fan-out/Fan-in、Expert Pool、Producer-Reviewer、Supervisor、Hierarchical Delegation
- **Skill 生成** —— 自动生成带 Progressive Disclosure 的 skill，实现高效的上下文管理
- **编排（Orchestration）** —— agent 间数据传递、错误处理与团队协调协议
- **校验（Validation）** —— 触发验证、dry-run 测试，以及「带 skill / 不带 skill」对比测试


## 工作流

```
Phase 1: 领域分析
    ↓
Phase 2: 团队架构设计（Agent Team vs Subagent）
    ↓
Phase 3: 生成 Agent 定义（.claude/agents/）
    ↓
Phase 4: 生成 Skill（.claude/skills/）
    ↓
Phase 5: 集成与编排
    ↓
Phase 6: 校验与测试
```

## 安装

### 通过 Marketplace 安装

#### 添加 marketplace
```shell
/plugin marketplace add revfactory/harness
```

#### 安装插件
```shell
/plugin install harness@harness-marketplace
```

### 作为全局 Skill 直接安装

```shell
# 将 skills 目录复制到 ~/.claude/skills/harness/
cp -r skills/harness ~/.claude/skills/harness
```

## 插件结构

```
harness/
├── .claude-plugin/
│   └── plugin.json                 # 插件清单
├── skills/
│   └── harness/
│       ├── SKILL.md                # 主 skill 定义（6-Phase 工作流）
│       └── references/
│           ├── agent-design-patterns.md   # 6 种架构模式
│           ├── orchestrator-template.md   # 团队/subagent 编排模板
│           ├── team-examples.md           # 5 个真实团队配置
│           ├── skill-writing-guide.md     # Skill 编写指南
│           ├── skill-testing-guide.md     # 测试与评估方法论
│           └── qa-agent-guide.md          # QA agent 集成指南
└── README.md
```

## 用法

在 Claude Code 中用类似下面的提示触发：

```
Build a harness for this project
Design an agent team for this domain
Set up a harness
帮我配置 harness
```

### 执行模式

| 模式 | 说明 | 推荐场景 |
|------|-------------|-----------------|
| **Agent Team**（默认） | TeamCreate + SendMessage + TaskCreate | 需要 2 个以上 agent 协作 |
| **Subagent** | 直接调用 Agent 工具 | 一次性任务，无需 agent 间通信 |

<p align="center">
  <img src="harness_team.png" alt="Harness Agent Team" width="500">
</p>

### 架构模式

| 模式 | 说明 |
|---------|-------------|
| Pipeline | 顺序、相互依赖的任务 |
| Fan-out/Fan-in | 并行、相互独立的任务 |
| Expert Pool | 依上下文选择性调用 |
| Producer-Reviewer | 先生成，再做质量评审 |
| Supervisor | 中心 agent 动态分配任务 |
| Hierarchical Delegation | 自顶向下递归委派 |

## 产出

Harness 生成的文件：

```
your-project/
├── .claude/
│   ├── agents/          # Agent 定义文件
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # Skill 文件
│       ├── analyze/
│       │   └── SKILL.md
│       └── build/
│           ├── SKILL.md
│           └── references/
```

## 应用场景 —— 试试这些提示

安装 Harness 后，把下面任意提示复制到 Claude Code 中：

**深度调研（Deep Research）**
```
Build a harness for deep research. I need an agent team that can investigate
any topic from multiple angles — web search, academic sources, community
sentiment — then cross-validate findings and produce a comprehensive report.
```

**网站开发**
```
Build a harness for full-stack website development. The team should handle
design, frontend (React/Next.js), backend (API), and QA testing in a
coordinated pipeline from wireframe to deployment.
```

**Webtoon / 漫画制作**
```
Build a harness for webtoon episode production. I need agents for story
writing, character design prompts, panel layout planning, and dialogue
editing. They should review each other's work for style consistency.
```

**YouTube 内容策划**
```
Build a harness for YouTube content creation. The team should research
trending topics, write scripts, optimize titles/tags for SEO, and plan
thumbnail concepts — all coordinated by a supervisor agent.
```

**代码评审与重构**
```
Build a harness for comprehensive code review. I want parallel agents
checking architecture, security vulnerabilities, performance bottlenecks,
and code style — then merging all findings into a single report.
```

**技术文档**
```
Build a harness that generates API documentation from this codebase.
Agents should analyze endpoints, write descriptions, generate usage
examples, and review for completeness.
```

**数据管线设计**
```
Build a harness for designing data pipelines. I need agents for schema
design, ETL logic, data validation rules, and monitoring setup that
delegate sub-tasks hierarchically.
```

**营销活动**
```
Build a harness for marketing campaign creation. The team should research
the target market, write ad copy, design visual concepts, and set up
A/B test plans with iterative quality review.
```

## 共存 —— Harness 与它的邻居

在 Claude Code / agent 框架生态里，Harness 并不孤单。以下仓库分布在相邻层级；每一项都以并列的「X 是……，Harness 是……」形式描述，方便你挑选合适的一个，或组合多个使用。

| 仓库 | 它的定位 | 与 Harness 的关系 |
|------|----------------|-------------------------|
| [coleam00/Archon](https://github.com/coleam00/Archon) | "harness builder" —— 确定性、可复现的运行时配置 | **同属 L3，邻接子层。** Archon 是 Runtime-Configuration Factory，Harness 是 Team-Architecture Factory。需要运行时确定性选 Archon，需要团队架构选 Harness，或组合使用。 |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | 相同理念的 Codex 移植版 | **同属 L3，不同运行时。** 在 Claude Code 上用 Harness，在 Codex 上用 meta-harness。 |
| [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) | "Agent harness 性能与工作流层"（位于现有 harness 之上） | **不同层级。** ECC 是跨 harness 的标准化层；Harness 是生成 harness 的工厂。可串联组合。 |
| [wshobson/agents](https://github.com/wshobson/agents) | Subagent / skill 目录（182 个 agent，149 个 skill） | **工厂 ↔ 零件供应。** wshobson 是可选购的目录；Harness 设计团队。把 wshobson 的条目作为零件吸收进 Harness 生成的团队中。 |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 状态图编排，与 LLM 无关 | **不同赛道。** LangGraph 面向长时运行、状态可恢复的编排；Harness 面向快速、Claude-Code 原生的团队设计。 |

## 用 Harness 构建的成果

### Harness 100

**[revfactory/harness-100](https://github.com/revfactory/harness-100)** —— 覆盖 10 个领域的 100 个生产级 agent team harness，提供英文与韩文两版（共 200 个包）。每个 harness 配有 4-5 个专家 agent、一个 orchestrator skill 以及领域专属 skill —— 全部由本插件生成。1808 个 markdown 文件，涵盖内容创作、软件开发、数据/AI、商业战略、教育、法律、健康等领域。

### 研究：Harness 有效性的 A/B 测试

**[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)** —— 一项覆盖 15 个软件工程任务的对照实验，衡量结构化预配置对 LLM 代码 agent 产出质量的影响。

| 指标 | 不用 Harness | 用 Harness | 提升 |
|--------|:-:|:-:|:-:|
| 平均质量分 | 49.5 | 79.3 | **+60%** |
| 胜率 | — | — | **100%**（15/15） |
| 产出方差 | — | — | **-32%** |

关键发现：有效性随任务复杂度递增 —— 任务越难，提升越大（Basic +23.8，Advanced +29.6，Expert +36.2）。

**各处统一使用的表述：** +60% 平均质量（49.5 → 79.3）、15/15 胜率、−32% 方差（n=15，作者自测 A/B，第三方复现待补）。

> 完整论文：*Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.*

## 依赖要求

- [启用 Agent Teams](https://code.claude.com/docs/en/agent-teams)：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## 常见问题（FAQ）

<details>
<summary><b>Q1. "+60%" 是不是夸大了？</b></summary>

**答：** +60% 这个数字来自**作者自测的 A/B（n=15，15 个任务，在姊妹仓库 `claude-code-harness` 上测量）**。本仓库中每一处引用都在同一句里附上披露说明「n=15，作者自测，第三方复现待补」。对于采纳决策，我们建议先做 2-4 周的内部试点，测量你自己的数据。

**证据：**
- 作者 A/B：[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- 论文：*Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*
</details>

<details>
<summary><b>Q2. 为什么是 "harness factory" 而不是 "harness builder"？这不是在和 Archon 竞争吗？</b></summary>

**答：** Archon 生成确定性的运行时配置 —— 它是 **Runtime-Configuration Factory**。Harness 生成 agent team 架构（团队结构、消息协议、评审关卡）—— 它是 **Team-Architecture Factory**。二者是**同属一个 L3 Meta-Factory 的邻接子层**，服务于不同需求。需要运行时确定性选 Archon，需要团队架构模式选 Harness，或组合使用（用 Harness 设计架构 → 用 Archon 部署运行时）。

**证据：**
- Archon 的自我定义：[clawfit docs/reference-levels.md](https://github.com/hongsw/clawfit/blob/main/docs/reference-levels.md)
- 子层声明：见上文 **类别 — Harness 所处的位置** 一节
- Archon 仓库：[github.com/coleam00/Archon](https://github.com/coleam00/Archon)
</details>

<details>
<summary><b>Q3. "仅支持 Claude Code" 是不是太窄了？Gemini/Codex 怎么办？</b></summary>

**答：** 目前官方运行时仅支持 Claude Code。相同理念的 Codex 移植版 —— [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) —— 已经公开，Codex 团队可以从那里开始。Harness 选择了「Claude-Code 原生、深入」而非「多运行时、浅尝」；与姊妹仓库（meta-harness、harness-init、OpenRig）的跨运行时协作已列入路线图。

**证据：**
- Codex 移植版：[github.com/SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)
- 跨运行时脚手架：[github.com/Gizele1/harness-init](https://github.com/Gizele1/harness-init)
</details>

## 许可证

Apache 2.0
