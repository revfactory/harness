# Experimental 依赖 — Agent Teams 标志

Harness 当前依赖 Claude Code 的 **Experimental Agent Teams** API。

## 必需环境变量

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

未设置时，多 agent 团队可能无法实例化（仅单 agent 响应）。

## 为什么需要

Harness 的默认执行模式使用 `TeamCreate`、`SendMessage`、`TaskCreate`。这些 API 在 Agent Teams experimental 通道下可用。

## 标志变更时

若 Anthropic 将 Agent Teams 提升为 stable：

1. 本仓库 README 将在 **72 小时内** 更新（见 CONTRIBUTING SLA）
2. 生成的 harness 文件结构不变；仅运行时标志可能移除

## 验证

```bash
claude --version          # 需 2.x+
claude plugin list        # 需 harness@harness
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # 需为 1
```

## 相关链接

- [Claude Code Agent Teams 文档](https://code.claude.com/docs/en/agent-teams)
- 英文版：[`experimental-dependency.md`](./experimental-dependency.md)
