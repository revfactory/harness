# 快速上手 — 5 分钟生成第一个 Harness

> **时间预算：5 分钟。** 若 5 分钟内无法完成 Step 5，请提 issue — 这是文档问题，不是你的问题。

**完成后你将拥有：** 当前目录下 `.claude/agents/` 中 3–5 个领域专用 agent，以及对应 `.claude/skills/`，由一句话 prompt 生成。

**前置条件：**
- Claude Code **v2.x+**（`claude --version` 返回 `2.x` 或更高）
- 支持 `export` 的 shell（bash / zsh / fish）
- 可访问 `github.com` 与 `api.anthropic.com`

---

## Step 1 — 添加 marketplace（约 60 秒）

```bash
claude plugin marketplace add revfactory/harness
```

**预期输出：** `Added marketplace: revfactory/harness`

---

## Step 2 — 安装插件并启用 Experimental 标志（约 40 秒）

```bash
claude plugin install harness@harness
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

将 `export` 写入 `~/.zshrc` 或 `~/.bashrc` 以持久化。

详见 [`docs/experimental-dependency_ZH.md`](./experimental-dependency_ZH.md)。

---

## Step 3 — 一句话生成 harness（约 2 分钟）

```bash
claude "帮我配置 harness：金融科技风险评估团队"
```

**也可尝试：**
- `claude "build a harness for a fintech risk-assessment team"`（英文）
- `claude "하네스 구성해줘 — 핀테크 리스크 평가 팀"`（韩文）
- `claude "搭建 harness：电商欺诈检测工作流"`

**预期输出：** 流式计划，随后确认已写入 3–5 个 agent 与 skill 文件。

---

## Step 4 — 验证生成文件（约 30 秒）

```bash
ls -la .claude/agents/
ls -la .claude/skills/
```

---

## Step 5 — 用 sample task 跑团队（约 90 秒）

```bash
claude "Ticket FIN-427: 新客户申请 500 万美元营运资金额度。输出一页 risk memo，含 go/no-go 建议。"
```

**常见问题：** 新终端未 `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` → 重新 export 后再跑。

---

## 下一步

- [`docs/experimental-dependency_ZH.md`](./experimental-dependency_ZH.md)
- [harness-100](https://github.com/revfactory/harness-100) — 100+ 预构建 harness 目录
