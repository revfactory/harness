<p align="center">
  <img src="harness_banner.png" alt="Harness Banner" width="600">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.2.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Patterns-6_Architectures-orange.svg" alt="6 Architecture Patterns">
  <img src="https://img.shields.io/badge/Mode-Agent_Teams-green.svg" alt="Agent Teams">
</p>

<p align="center">
  <a href="#类别--harness-的定位"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#类别--harness-的定位"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA%20%7C%20ZH-lightgrey" alt="i18n"></a>
</p>

# Harness — Claude Code 的团队架构工厂

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | **中文**

> **Harness 是 Claude Code 的团队架构工厂。** 说 **「帮我配置 harness」**（中文）、**「build a harness for this project」**（英文）或 **「ハーネスを構成して」**（日文），插件会根据你的领域描述生成 agent team 及其 skills，并从 6 种预定义团队架构模式中选择。

## 概述

Harness 利用 Claude Code 的 agent team 系统将复杂任务分解为协调工作的专业 agent。说「帮我搭建 harness」即可自动生成 `.claude/agents/` 与 `.claude/skills/`。

## 类别 — Harness 的定位

Harness 位于 Claude Code 生态的 **L3 Meta-Factory** 层 — 生成其他 harness 的工厂。在 L3 内，我们专注 **Team-Architecture Factory** 子层。

| 层级 | 作用 | 相邻项目 |
|------|------|----------|
| **L3 — Meta-Factory / Team-Architecture Factory**（本项目） | 领域一句话 → agent team + skills，6 种团队模式 | — |
| L3 — Runtime-Configuration Factory | 确定性、可重复的运行时配置 | [Archon](https://github.com/coleam00/Archon) |
| L3 — Codex Runtime Port | 同概念，Codex 运行时 | [meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | 跨 harness 标准化 skills/rules/hooks | [ECC](https://github.com/affaan-m/everything-claude-code) |

## 核心特性

- **Agent Team 设计** — Pipeline、Fan-out/Fan-in、Expert Pool、Producer-Reviewer、Supervisor、Hierarchical Delegation
- **Skill 生成** — Progressive Disclosure，高效上下文管理
- **编排** — agent 间数据传递、错误处理、团队协调协议
- **验证** — 触发器验证、dry-run、with-skill vs without-skill 对比测试

## 工作流

```
Phase 1: 领域分析
    ↓
Phase 2: 团队架构设计
    ↓
Phase 3: Agent 定义 (.claude/agents/)
    ↓
Phase 4: Skill 生成 (.claude/skills/)
    ↓
Phase 5: 集成与编排
    ↓
Phase 6: 验证与测试
```

## 安装

### Marketplace

```shell
/plugin marketplace add revfactory/harness
/plugin install harness@harness-marketplace
```

### 全局 Skill

```shell
cp -r skills/harness ~/.claude/skills/harness
```

## 用法

触发示例：

```
帮我配置 harness
搭建 harness：深度研究团队
设计 agent team 用于多源新闻采集
Set up a harness for this project
```

## 架构模式

| 模式 | 说明 |
|------|------|
| Pipeline | 顺序依赖任务 |
| Fan-out/Fan-in | 并行独立任务后合并 |
| Expert Pool | 按上下文选择性调用专家 |
| Producer-Reviewer | 生成后质量审查 |
| Supervisor | 中央 agent 动态分派 |
| Hierarchical Delegation | 自上而下递归委派 |

## 用例 — 可复制 Prompt

**深度研究**
```
Build a harness for deep research. Parallel agents for web, academic,
and community sources — cross-validate and produce a report.
```

**多源新闻情报**
```
帮我搭建 harness：多源新闻情报。RSS、社交媒体、网页并行采集，
交叉验证后输出 JSON + markdown 简报。
```

**代码审查**
```
Build a harness for code review — parallel agents for architecture,
security, performance, style — merge into one report.
```

## 与相邻项目共存

| 项目 | 定位 | 与 Harness 关系 |
|------|------|----------------|
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 互联网接入安装/路由 | **工厂 ↔ 工具供应** — 研究/新闻 harness 的 CLI 层 |
| [wshobson/agents](https://github.com/wshobson/agents) | agent/skill 目录 | **工厂 ↔ 零件供应** |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 状态图编排 | **不同赛道** — 长期有状态编排 |

## 要求

- Agent Teams：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## 文档

- [快速上手（中文）](docs/quickstart_ZH.md)
- [Experimental 依赖（中文）](docs/experimental-dependency_ZH.md)

## License

Apache 2.0
