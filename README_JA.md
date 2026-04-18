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
  <a href="#カテゴリー--harness-はどこに位置するか"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#カテゴリー--harness-はどこに位置するか"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA-lightgrey" alt="i18n"></a>
</p>

# Harness — Claude Code のためのチームアーキテクチャファクトリー

[English](README.md) | [한국어](README_KO.md) | **日本語**

> **Harness は Claude Code 向けのチームアーキテクチャファクトリーです。** **「ハーネスを構成して」** (日本語) ·  **"build a harness for this project"** (English) · **"하네스 구성해줘"** (한국어) と伝えるだけで、プラグインがドメイン記述をエージェントチームとそのチームが使うスキルへと変換します — あらかじめ定義された 6 種類のチームアーキテクチャパターンから 1 つを選んで。

## 概要

Harnessは、Claude Codeのエージェントチームシステムを活用し、複雑なタスクを専門エージェントチームに分解・統制するアーキテクチャツールです。「ハーネスを構成して」と伝えるだけで、ドメインに適したエージェント定義（`.claude/agents/`）とスキル（`.claude/skills/`）を自動生成します。

## カテゴリー — Harness はどこに位置するか

Harness は Claude Code エコシステムの **L3 Meta-Factory** 層 — 他のハーネスそのものではなく「他のハーネスを生成する層」 — に位置します。その層の中で、**Team-Architecture Factory** というサブ層を選択します。

| 層 | 担当領域 | 共存する隣人 |
|----|----------|--------------|
| **L3 — Meta-Factory / Team-Architecture Factory** (当プロジェクト) | ドメイン記述 → エージェントチーム + スキル、事前定義された 6 種のチームパターン経由 | — |
| L3 — Meta-Factory / Runtime-Configuration Factory | 決定的で再現可能なランタイム構成 | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Codex Runtime Port | 同一コンセプトの Codex ランタイム版 | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | 複数ハーネスにまたがるスキル・ルール・フックの標準化 | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon は決定的なランタイム構成を生成します。Harness はチームアーキテクチャ（パイプライン・ファンアウト/ファンイン・エキスパートプール・プロデューサー-レビューア・スーパーバイザー・階層的委任）と、エージェントが使うスキルを生成します。同じ L3 の異なるサブ層です。ランタイムの決定性が欲しければ Archon、チームアーキテクチャが欲しければ Harness、あるいは両者を組み合わせて利用できます。

## 主な機能

- **エージェントチーム設計** — パイプライン、ファンアウト/ファンイン、エキスパートプール、プロデューサー-レビューア、スーパーバイザー、階層的委任の6種アーキテクチャパターンに対応
- **スキル生成** — Progressive Disclosureパターンによるコンテキストの効率的管理を備えたスキルを自動生成
- **オーケストレーション** — エージェント間のデータ受け渡し、エラーハンドリング、チーム連携プロトコルを内蔵
- **検証体制** — トリガー検証、ドライランテスト、With-skill vs Without-skill 比較テスト

## ハーネス進化メカニズム (Harness Evolution Mechanism)

ハーネス進化メカニズムは「何が効いて、何が効かなかったか」のデルタをファクトリーへフィードバックし、次世代が測定可能なかたちで改善されるようにします。生成されたハーネスが実プロジェクトで使用されると、`/harness:evolve` スキルが初期アーキテクチャとリリース時アーキテクチャのデルタを捕捉し、ファクトリーへ戻します。次回、同様のドメインでの生成は、このフィードバックを反映して「リリース状態により近いドラフト」から始まります。

```
初期ハーネス ──▶ 実プロジェクト利用 ──▶ リリース版ハーネス
                                              │
                                              ▼ (/harness:evolve によるデルタ取得)
                                        ┌───────────────┐
                                        │  ファクトリー │◀── より良い次世代ドラフト
                                        └───────────────┘
```

これを **ハーネス進化メカニズム (Harness Evolution Mechanism; KR: 하네스 진화 메커니즘)** と呼びます。

## ワークフロー

```
Phase 1: ドメイン分析
    ↓
Phase 2: チームアーキテクチャ設計（Agent Teams vs サブエージェント）
    ↓
Phase 3: エージェント定義の生成（.claude/agents/）
    ↓
Phase 4: スキル生成（.claude/skills/）
    ↓
Phase 5: 統合とオーケストレーション
    ↓
Phase 6: 検証とテスト
```

## インストール

### マーケットプレイス経由

#### マーケットプレイスの追加
```shell
/plugin marketplace add revfactory/harness
```

#### プラグインのインストール
```shell
/plugin install harness@harness
```

### グローバルスキルとして直接インストール

```shell
# skillsディレクトリを ~/.claude/skills/harness/ にコピー
cp -r skills/harness ~/.claude/skills/harness
```

## プラグイン構成

```
harness/
├── .claude-plugin/
│   └── plugin.json                 # プラグインマニフェスト
├── skills/
│   └── harness/
│       ├── SKILL.md                # メインスキル定義（6フェーズワークフロー）
│       └── references/
│           ├── agent-design-patterns.md   # 6種のアーキテクチャパターン
│           ├── orchestrator-template.md   # チーム/サブエージェント オーケストレーターテンプレート
│           ├── team-examples.md           # 実践チーム構成例 5種
│           ├── skill-writing-guide.md     # スキル作成ガイド
│           ├── skill-testing-guide.md     # テスト・評価方法論
│           └── qa-agent-guide.md          # QAエージェント統合ガイド
└── README.md
```

## 使い方

Claude Codeで以下のように呼び出します：

```
Build a harness for this project
Design an agent team for this domain
Set up a harness
```

### 実行モード

| モード | 説明 | 推奨ケース |
|--------|------|------------|
| **Agent Teams**（デフォルト） | TeamCreate + SendMessage + TaskCreate | エージェント2名以上、コラボレーションが必要な場合 |
| **サブエージェント** | Agentツール直接呼び出し | 単発タスク、エージェント間通信不要の場合 |

<p align="center">
  <img src="harness_team.png" alt="Harness Agent Team" width="500">
</p>

### アーキテクチャパターン

| パターン | 説明 |
|----------|------|
| パイプライン | 順次依存タスク |
| ファンアウト/ファンイン | 並列独立タスク |
| エキスパートプール | 状況に応じた選択的呼び出し |
| プロデューサー-レビューア | 生成後の品質レビュー |
| スーパーバイザー | 中央エージェントによる動的タスク分配 |
| 階層的委任 | 上位→下位への再帰的委任 |

## 出力

Harnessが生成するファイル：

```
your-project/
├── .claude/
│   ├── agents/          # エージェント定義ファイル
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # スキルファイル
│       ├── analyze/
│       │   └── SKILL.md
│       └── build/
│           ├── SKILL.md
│           └── references/
```

## ユースケース — そのまま使えるプロンプト

Harnessインストール後、以下のプロンプトをClaude Codeにコピーしてお使いください：

**ディープリサーチ**
```
Build a harness for deep research. I need an agent team that can investigate
any topic from multiple angles — web search, academic sources, community
sentiment — then cross-validate findings and produce a comprehensive report.
```

**ウェブサイト制作**
```
Build a harness for full-stack website development. The team should handle
design, frontend (React/Next.js), backend (API), and QA testing in a
coordinated pipeline from wireframe to deployment.
```

**ウェブトゥーン制作**
```
Build a harness for webtoon episode production. I need agents for story
writing, character design prompts, panel layout planning, and dialogue
editing. They should review each other's work for style consistency.
```

**YouTube コンテンツ企画**
```
Build a harness for YouTube content creation. The team should research
trending topics, write scripts, optimize titles/tags for SEO, and plan
thumbnail concepts — all coordinated by a supervisor agent.
```

**コードレビュー**
```
Build a harness for comprehensive code review. I want parallel agents
checking architecture, security vulnerabilities, performance bottlenecks,
and code style — then merging all findings into a single report.
```

**技術ドキュメント作成**
```
Build a harness that generates API documentation from this codebase.
Agents should analyze endpoints, write descriptions, generate usage
examples, and review for completeness.
```

**データパイプライン設計**
```
Build a harness for designing data pipelines. I need agents for schema
design, ETL logic, data validation rules, and monitoring setup that
delegate sub-tasks hierarchically.
```

**マーケティングキャンペーン**
```
Build a harness for marketing campaign creation. The team should research
the target market, write ad copy, design visual concepts, and set up
A/B test plans with iterative quality review.
```

## 共存 — Harness と隣人たち

Harness は Claude Code / エージェントフレームワークのエコシステムで一人ではありません。以下のリポジトリは隣接する層に位置しており、いずれも「X は ···、Harness は ···」という並列構造で記述されているため、用途に応じて選んだり、複数を組み合わせて利用できます。

| リポジトリ | 相手のポジション | Harness との関係 |
|------------|------------------|------------------|
| [coleam00/Archon](https://github.com/coleam00/Archon) | "harness builder" — 決定的で再現可能なランタイム構成 | **同じ L3、隣のサブ層。** Archon は Runtime-Configuration Factory、Harness は Team-Architecture Factory。ランタイム決定性は Archon、チームアーキテクチャは Harness、または両者の組み合わせ。 |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | 同一コンセプトの Codex 移植 | **同じ L3、異なるランタイム。** Claude Code では Harness、Codex では meta-harness。 |
| [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) | "Agent harness performance & workflow layer" — 既存ハーネスの上に乗る標準化層 | **異なる層。** ECC は複数ハーネスの上の標準化層、Harness はハーネスを生成するファクトリー。直列的に組み合わせ可能。 |
| [wshobson/agents](https://github.com/wshobson/agents) | サブエージェント / スキルカタログ (182 agents, 149 skills) | **ファクトリー ↔ 部品供給。** wshobson は「ショッピングするカタログ」、Harness は「チーム設計」。Harness が生成したチーム内に wshobson のエントリを部品として取り込み可能。 |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | ステートグラフ・オーケストレーション、LLM-agnostic | **異なるトラック。** 長時間実行・状態復元が要なら LangGraph、Claude Code ネイティブでの素早いチーム設計が要なら Harness。 |

## Harnessで構築されたプロジェクト

### Harness 100

**[revfactory/harness-100](https://github.com/revfactory/harness-100)** — 10ドメイン、100のプロダクションレディなエージェントチームハーネス（英韓200パッケージ）。各ハーネスには4〜5名の専門エージェント、オーケストレータースキル、ドメイン特化スキルが含まれており、すべて本プラグインで生成されました。コンテンツ制作、ソフトウェア開発、データ/AI、ビジネス戦略、教育、法律、ヘルスケアなど1,808のMarkdownファイル。

### 研究：Harness適用前後のA/Bテスト

**[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)** — 15のソフトウェアエンジニアリング課題を対象とした統制実験で、構造化された事前設定がLLMコードエージェントの出力品質に与える影響を測定しました。

| 指標 | Harness未適用 | Harness適用 | 改善 |
|------|:-:|:-:|:-:|
| 平均品質スコア | 49.5 | 79.3 | **+60%** |
| 勝率 | — | — | **100%** (15/15) |
| 出力分散 | — | — | **-32%** |

主な発見：課題の難易度が高いほど改善効果が増大（Basic +23.8、Advanced +29.6、Expert +36.2）。

**あらゆる場面でこの文をそのままお使いください:** 平均品質 +60% (49.5 → 79.3)、15/15 勝率、出力分散 −32% (n=15、著者測定 A/B、第三者再現実験は進行中)。

> 論文全文：*Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.*

## 要件

- [Agent Teams機能の有効化](https://code.claude.com/docs/en/agent-teams)：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## FAQ

<details>
<summary><b>Q1. "+60%" は誇張では？</b></summary>

**A.** +60% は **著者自身による A/B（n=15、15 タスク、姉妹リポジトリ `claude-code-harness` で計測）** の結果です。本リポジトリでは、この数値を引用する際は必ず「n=15、著者測定、第三者再現実験は進行中」を同じ文の中に併記しています。組織導入時には、2〜4 週間の社内パイロットで独自の数値を測定することを推奨します。

**Evidence:**
- 著者 A/B: [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- 論文: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*
</details>

<details>
<summary><b>Q2. なぜ "harness builder" ではなく "harness factory" なのですか？ Archon と競合しませんか？</b></summary>

**A.** Archon は決定的なランタイム構成を生成する **Runtime-Configuration Factory** であり、Harness はエージェントチームアーキテクチャ（チーム構造・メッセージプロトコル・レビューゲート）を生成する **Team-Architecture Factory** です。両者は **同じ L3 Meta-Factory 層の隣接するサブ層** で、用途が異なります。決定的なランタイムが必要なら Archon、6 つのチームアーキテクチャパターンの事前定義が必要なら Harness。両者を組み合わせる（アーキテクチャ設計 → ランタイム配置）ことも可能です。

**Evidence:**
- Archon 自己定義: [clawfit docs/reference-levels.md](https://github.com/hongsw/clawfit/blob/main/docs/reference-levels.md)
- サブ層宣言: 本 README の **カテゴリー — Harness はどこに位置するか** セクション
- Archon リポジトリ: [github.com/coleam00/Archon](https://github.com/coleam00/Archon)
</details>

<details>
<summary><b>Q3. 「Claude Code 専用」は狭すぎませんか？ Gemini・Codex は？</b></summary>

**A.** 現時点で公式のランタイムは Claude Code のみです。同一コンセプトの Codex 移植 [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) がすでに公開されており、既存の Codex チームはそちらから開始できます。Harness は「Claude Code ネイティブ・深く」を選択しており、クロスランタイムの需要は共存リポジトリ（meta-harness、harness-init、OpenRig）との連携計画としてロードマップに反映される予定です。

**Evidence:**
- Codex 移植: [github.com/SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)
- クロスランタイム・スキャフォルダー: [github.com/Gizele1/harness-init](https://github.com/Gizele1/harness-init)
</details>

## ライセンス

Apache 2.0
