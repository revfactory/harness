# 实验性开关依赖

> **状态：** Active · **负责人：** revfactory · **最后更新：** 2026-04-18 · **SLA：** 见 [监控承诺](#监控承诺)

本文档解释 `harness` 为何需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`、该开关三种可能的未来，以及本仓库在每种情况下会做什么 —— 并给出限时承诺，便于企业采纳者据此规划。

---

## 当前状态

### 为何需要这个开关

`harness` 是一个构建于 Claude Code **Agent Teams API** 之上的元 skill 工厂。每当用户运行 `claude "build a harness for <domain>"` 时，内部会调用三个 Claude Code 原语：

| 原语 | 用途 | 是否受开关限制 |
|-----------|---------|-------------|
| `TeamCreate` | 实例化一支共享上下文的多 agent 团队 | **是** |
| `SendMessage` | 在团队成员间路由消息（supervisor ↔ worker） | **是** |
| `TaskCreate` | 在团队内派生长时运行的子任务 | **是** |
| `Agent` 工具（invoke） | 单 agent 派发 | 否（GA） |

这三个受开关限制的原语都要求：

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

如果启动 `claude` 的 shell 中未设置该变量，harness 生成的团队会回退为单 agent 执行，从而悄然破坏 Pipeline / Fan-out-in / Supervisor / Hierarchical Delegation 模式。

### Anthropic 参考资料（提交 issue 前必读）

该开关的设计理由与路线图见三篇 Anthropic Engineering 博文。评估 harness 的采纳者至少应阅读第一篇：

1. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) —— 定义了 Anthropic 认可的 "harness" 类别与长时运行 agent 契约。
2. [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) —— `harness` 所固化的模式（Pipeline、Producer-Reviewer、Supervisor 等）。
3. [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) —— 可能取代实验性开关的前进路径（见场景 B）。

---

## 依赖图

```
harness (v1.2.0)
  └── Agent Teams API (Claude Code)
        ├── TeamCreate            ← EXPERIMENTAL_AGENT_TEAMS=1
        ├── SendMessage           ← EXPERIMENTAL_AGENT_TEAMS=1
        ├── TaskCreate            ← EXPERIMENTAL_AGENT_TEAMS=1
        └── Agent (invoke)        ← GA (与开关无关)
              └── Anthropic Roadmap
                    ├── Scenario A: Flag removed (GA promotion)
                    ├── Scenario B: Managed Agents GA (parallel path)
                    └── Scenario C: Breaking signature change
```

**自顶向下阅读此图：** harness 依赖 Agent Teams API，后者依赖单个实验性开关，而该开关又依赖 Anthropic 自己的路线图。任一上游节点变化时，本仓库都有义务在下文 SLA 内适配。

---

## 3 种场景

每种场景都列出**检测触发条件**（我们如何得知它发生）、本仓库承诺的 **T+24h / T+48h / T+72h 行动**，以及每个检查点的**用户可见产物**。

### 场景 A —— 开关移除（Agent Teams 晋升 GA）

**触发检测：** Anthropic Claude Code Changelog 发布 "Agent Teams is now GA"，**或** `claude-code` 二进制不再需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`（由 [P-13](#) 的 nightly CI 检测）。

**概率（主观）：** 高 —— 这是上述三篇博文所预示的路径。

| 检查点 | 行动 | 产物 |
|------------|--------|----------|
| **T+24h** | 开 `feat/drop-experimental-flag` 分支。从每个 README / docs / Quickstart 移除 `export` 行。在 `plugin.json` 中加入 `claude-code >= X.Y.Z` 下界。 | 分支 + PR（草稿） |
| **T+48h** | 发布 `docs/migrating-from-experimental.md`。把 `docs/experimental-dependency.md`（本文件）标题更新为 "no flag required as of vX.Y"。置顶 GitHub issue："Action required: drop the export line"。 | 迁移指南 + 置顶 issue |
| **T+72h** | 发布 **v1.3.0**，包含：(a) CHANGELOG 条目，(b) 带迁移说明的 `gh release create`，(c) HN 跟进帖："We dropped the experimental flag"。 | `v1.3.0` git tag + GH Release |

**采纳者影响：** 正面。企业审批阻力下降 —— "无实验性开关" 这一勾选项变得可满足。对 harness 用户代码无破坏性变更。

---

### 场景 B —— Managed Agents 进入 GA（并行路径）

**触发检测：** Anthropic 发布 "[Managed Agents](https://www.anthropic.com/engineering/managed-agents) is generally available"，并提供稳定的 `claude-agents` CLI 或 SDK 接口。

**概率（主观）：** 90 天内中-高。Managed Agents 是服务端执行模型；harness 的客户端团队编排**不会**自动迁移过去。

| 检查点 | 行动 | 产物 |
|------------|--------|----------|
| **T+24h** | 开 `feat/managed-agents-compat` PR。加入 `adapters/managed-agents/` 脚手架，把 harness 的 6 种团队模式映射到 Managed Agents 调用。识别不兼容的模式（很可能是 Hierarchical Delegation）。 | 兼容 PR（草稿） |
| **T+48h** | 发布博文：**"Harness + Managed Agents: one layer up, not replaced"**，发于 Dev.to 与本仓库。把 harness 重新定位为输出 Managed Agents 配置的**设计期**层，而非运行时竞品。 | 共存定位博文 |
| **T+72h** | 发布 `docs/managed-agents-migration.md`，附逐模式矩阵（6 种模式中哪些 1:1 映射、哪些需重写）。更新 README 姊妹仓库一节。 | 迁移指南 |

**战略说明：** harness 重新定位为 Managed Agents **之上的层** —— "Managed Agents 运行团队，harness 设计团队"。这是 GTM 计划 §4.2 中的共存框架。

**采纳者影响：** 中性偏正面。现有 harness 用户继续在实验性开关路径上工作；新用户可选择 Managed Agents 输出。

---

### 场景 C —— 破坏性变更（API 签名突变）

**触发检测：** Nightly CI（`.github/workflows/nightly-compat.yml`，路线图编号 P-13）对 Claude Code 最新 nightly 构建运行失败，**或** Changelog 宣布重命名的环境变量 / 变更的 `TeamCreate` 签名。

**概率（主观）：** 中。实验性 API 可能在无弃用窗口的情况下被重命名。

| 检查点 | 行动 | 产物 |
|------------|--------|----------|
| **T+0 至 T+24h** | Nightly CI 在 Slack/Discord 告警。作者开 `hotfix/compat-<date>` 分支，修补受影响的调用点。在新旧签名上单测通过（尽力而为）。 | Hotfix 分支 |
| **T+24h** | 合并 hotfix。推 `v1.2.x` 补丁 tag。更新 `docs/compatibility-matrix.md` 中受影响 Claude Code 版本的行。 | `v1.2.x` 补丁发布 |
| **T+72h** | 若变更非平凡（影响 harness 的公共契约），在仓库 Discussions 标签页 + X 发布简短通告。否则一条 CHANGELOG 条目即可。 | Discussions 帖（视情况） |

**采纳者影响：** 固定在旧版 Claude Code 的现有用户不受影响。使用最新版的用户会在同一周内获得补丁。

---

## 监控承诺

我们承诺以下**可观测 SLA**。未达成即构成提交带 `sla-breach` 标签 issue 的理由。

| 事件 | SLA | 度量方式 |
|-------|-----|-------------|
| Anthropic 在官方 Changelog 发布 Agent Teams / Managed Agents 变更 | 本文档在 **72 小时**内更新 | 对比 Changelog 帖时间戳与本文件 `最后更新` 行 |
| Nightly CI 检测到兼容性破坏 | **24 小时**内开 hotfix 分支 | GitHub Actions 运行时间戳 vs. 分支创建时间戳 |
| 新的 Claude Code 稳定版（minor 或 major） | **7 天**内为 `docs/compatibility-matrix.md` 添加对应行 | 兼容性矩阵 diff |

**我们主动监控的来源：**

- Claude Code 发布说明 —— 通过 [Anthropic Engineering 博客](https://www.anthropic.com/engineering) RSS 关注
- `anthropics/claude-code` GitHub Releases（nightly tag）
- Anthropic Discord `#claude-code` 频道（社区信号）

---

## 企业采纳者 FAQ

### Q1. 我们处于受监管行业（金融、医疗、公共部门），无法在生产中启用 `EXPERIMENTAL` 开关。如何采纳 harness？

**原因：** 许多合规框架（SOC 2 Type II、ISO 27001、K-ISMS）禁止在生产中使用不稳定 / 预览特性。
**行动：** **仅在设计期**使用 harness：在沙箱工作站上运行它来生成 `.claude/agents/` 与 `.claude/skills/` 文件，然后把生成的产物提交进你的生产仓库。生产环境的 Claude Code 永远不需要这个开关 —— 只有受开关限制的 `TeamCreate` 运行时才需要。生成的单 agent skill 与 GA 路径兼容。

### Q2. 如果 Agent Teams 进入 GA（场景 A），我现有的 harness 生成代码会坏吗？

**原因：** 在 Anthropic 的 Claude Code 中，GA 晋升对生成产物历来是非破坏性的；只是该开关不再被要求而已。
**行动：** 终端用户无需任何操作。你的 `.claude/agents/*.md` 与 `.claude/skills/*` 文件是纯 Markdown，仍然有效。GA 当天你即可 `unset CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`。我们会在 48 小时内发布迁移说明（见场景 A）。

### Q3. 你们有书面 SLA 保证吗？如果没达成会怎样？

**原因：** 企业在审批前需要一份合同级、或至少可观测的承诺。
**行动：** 上方 SLA 表即为**公开承诺**，由以下机制保障：(a) 一个 GitHub Action，在检测到 Changelog 事件 72 小时后若本文件 `最后更新` 行仍未更新则在本文件下评论，(b) 采纳者可施加的 `sla-breach` issue 标签，(c) `CONTRIBUTING.md` 中对任何违约的事后复盘义务。这不是付费 SLA —— 而是社区承诺。如需付费 SLA，请联系维护者（见仓库 README）。

---

**相关文档：**
- [`docs/quickstart.md`](./quickstart.md) —— 5 分钟安装演练
- [`docs/show-hn-launch-kit.md`](./show-hn-launch-kit.md) —— 公开发布套件
- `docs/compatibility-matrix.md` *（待补，P-13）* —— Claude Code × harness 版本对照表
