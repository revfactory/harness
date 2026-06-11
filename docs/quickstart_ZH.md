# 快速上手 —— 5 分钟构建你的第一个 Harness

> **时间预算：5 分钟（严格）。** 如果 5 分钟内你还没走到 Step 5，请停下并提交 issue —— 那是本文档的 bug，不是你的问题。

<!-- TODO: Loom embed — 60s screen recording showing Steps 1→5 end-to-end. Replace this comment with the `<iframe>` once recorded. -->

**结束时你将拥有：** 一个可用的 `.claude/agents/` 目录，里面有 3-5 个领域专精的 agent —— 由一句话提示生成，可直接在示例任务上运行。

**前置条件（开始前请确认）：**
- Claude Code **v2.x 或更高版本**（`claude --version` 应返回 `2.x` 或更高）
- 一个能跨命令保留 `export` 的 shell（bash、zsh 或 fish）
- 可访问 `github.com` 与 `api.anthropic.com` 的网络

---

## Step 1 —— 添加 marketplace（60 秒）

```bash
claude plugin marketplace add revfactory/harness
```

**作用：** 注册 `harness` marketplace，使 Claude Code 能发现 `revfactory` 发布的插件。

**预期输出：** `Added marketplace: revfactory/harness`

---

## Step 2 —— 安装插件并启用实验性开关（40 秒）

```bash
claude plugin install harness@harness
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

*（要让该开关在多个 shell 会话间持久生效，把 `export` 这一行追加到 `~/.zshrc` 或 `~/.bashrc`。）*

**作用：** 从 `harness` marketplace 安装 `harness` 插件，然后启用 Agent Teams —— harness 用来编排多 agent 工作流的 Claude Code API。开关为何必需，见 [`docs/experimental-dependency.md`](./experimental-dependency.md)。

**失败 FAQ #1 —— `AGENT_TEAMS not found` / team 无法实例化**
**原因：** Claude Code 版本低于 v2.x（Agent Teams 在 v2.0 引入）。
**修复：** 运行 `claude --version`。若低于 2.0，通过 `npm i -g @anthropic-ai/claude-code`（或你所用发行版的安装器）升级，然后重复 Step 2。

---

## Step 3 —— 用一句话生成一个 harness（2 分钟）

```bash
claude "build a harness for a fintech risk-assessment team"
```

**作用：** 调用 `/harness:harness` 元 skill，它会分析你的领域描述，并把一支专精 agent 团队 + 它们的 skill 脚手架写入当前目录的 `.claude/agents/` 与 `.claude/skills/`。

**试试这些替代提示** —— 任意一条都有效：
- `claude "帮我配置 harness —— 金融科技风险评估团队"`（中文同样有效）
- `claude "하네스 구성해줘 — 핀테크 리스크 평가 팀"`（韩文同样有效）
- `claude "build a harness for an e-commerce fraud-detection workflow"`
- `claude "design an agent team for technical due diligence on open-source repos"`

**预期输出：** 一段流式计划，随后确认已写出 3-5 个 agent `.md` 文件及其 skill。

**失败 FAQ #2 —— 中文/韩文提示无响应，而英文提示成功**
**原因：** 区域设置或分词器误路由；harness 的 orchestrator 基于触发词匹配（如韩文「하네스 구성」），这些触发词内建于 skill 定义中。
**修复：** 若非英文提示失败，用上面的英文提示重试 —— 底层 skill 完全相同。若都失败，跳到失败 FAQ #3。

---

## Step 4 —— 校验生成的文件（30 秒）

```bash
ls -la .claude/agents/
ls -la .claude/skills/
```

**作用：** 确认元 skill 已把文件写入预期位置。

**预期输出：** 每个目录 3-5 个文件，文件名反映你的领域（如金融科技示例中的 `risk-analyst.md`、`compliance-reviewer.md`、`portfolio-monitor.md`）。

**失败 FAQ #3 —— "什么都没生成" / 目录为空**
**原因：** 插件实际未安装，或在当前项目中未激活。
**修复：** 运行 `claude plugin list`。若没有 `harness@harness`，重复 Step 2。若存在但未激活，运行 `claude plugin enable harness@harness`，然后重复 Step 3。

---

## Step 5 —— 让新团队跑一个示例任务（90 秒）

复制一条贴近真实的 Jira-工单式提示，交给你刚生成的团队：

```bash
claude "Ticket FIN-427: A new corporate customer (mid-cap manufacturer, \$80M revenue, South Korea) has applied for a \$5M working-capital line. Produce a risk assessment covering (1) credit-history red flags, (2) sector concentration vs. our existing book, (3) regulatory exposure (KFTC, FSC). Output: a 1-page memo with a go/no-go recommendation."
```

**作用：** Claude Code 检测到 `.claude/agents/` 中的新 agent，按 harness 生成的团队模式（风险类工作通常是 Producer-Reviewer 或 Expert-Pool）路由任务，并返回一份结构化备忘录。

**失败 FAQ #4 —— "团队不执行 / 只有一个 agent 响应"**
**原因：** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 在运行 Step 3 的 shell 中设置了，但运行 Step 5 的 shell 中没有（新开终端时常见）。
**修复：** 在当前 shell 重新 export：`export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`，然后重跑 Step 5。要永久生效，把该行加入你的 shell rc 文件。

**失败 FAQ #5 —— "API 调用太多 / 成本焦虑"**
**原因：** 多 agent 团队每个任务可能扇出 5 个以上并行 Claude 调用。单个复杂工单可消耗 50K-200K token。
**修复：** 每次运行限制为单个任务（不要用 `&&` 串联多次 harness 调用），若你的 Claude Code 版本支持，使用 `--max-turns` 标志。生产环境中，把 harness 调用置于成本感知的包装层之后 —— 见 `docs/cost-controls.md` *（待补）*。

---

## 完成

到这一步，你应该已经拥有：

- [x] 一个含领域专精 agent 的 `.claude/agents/` 目录
- [x] 一个含其支撑 skill 的 `.claude/skills/` 目录
- [x] 一次成功的示例任务执行
- [x] 一个可用的 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 环境

**下一步阅读：**
- [`docs/experimental-dependency.md`](./experimental-dependency.md) —— 为何需要这个开关，以及它变化时我们会怎么做
- [`revfactory/harness-100`](https://github.com/revfactory/harness-100) —— 100+ 预构建领域 harness 的目录，若你更想克隆而非生成
- [`revfactory/claude-code-harness`](https://github.com/revfactory/claude-code-harness) —— 我们用来在 15 个任务上测得 +60% 质量的 A/B 测试 harness

**如果你遇到本指南未覆盖的问题：** 提交一个带 `quickstart-gap` 标签的 issue，并附上：(a) 哪一步失败，(b) `claude --version`，(c) 准确的错误信息。quickstart-gap issue 的首次响应 SLA 为 **48 小时**（见 `CONTRIBUTING.md`）。
