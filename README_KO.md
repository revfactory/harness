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
  <a href="#카테고리--harness는-어디에-서-있나요"><img src="https://img.shields.io/badge/Layer-L3%20Meta--Factory-orange" alt="Layer"></a>
  <a href="#카테고리--harness는-어디에-서-있나요"><img src="https://img.shields.io/badge/Sub--layer-Team--Architecture%20Factory-teal" alt="Sub-layer"></a>
  <a href="#"><img src="https://img.shields.io/badge/README-EN%20%7C%20KO%20%7C%20JA-lightgrey" alt="i18n"></a>
</p>

# Harness — Claude Code를 위한 팀 아키텍처 팩토리

[English](README.md) | **한국어** | [日本語](README_JA.md)

> **Harness는 Claude Code용 팀 아키텍처 팩토리입니다.** **"하네스 구성해줘"** (한국어) · **"build a harness for this project"** (English) · **"ハーネスを構成して"** (日本語) 한 문장으로, 플러그인이 도메인 설명을 에이전트 팀과 그들이 쓸 스킬로 변환합니다 — 사전 정의된 6가지 팀 아키텍처 패턴 중 하나를 골라서요.

## 개요

Harness는 Claude Code의 에이전트 팀 시스템을 활용하여 복잡한 작업을 전문 에이전트 팀으로 분해·조율하는 아키텍처 도구다. "하네스 구성해줘"라고 말하면, 사용자의 도메인에 맞는 에이전트 정의(`.claude/agents/`)와 스킬(`.claude/skills/`)을 자동 생성한다.

## 카테고리 — Harness는 어디에 서 있나요

Harness는 Claude Code 생태계의 **L3 Meta-Factory** 층 — 다른 하네스들이 아니라 "다른 하네스들을 생성하는 층" — 에 자리합니다. 그 층 안에서 우리는 **Team-Architecture Factory** 서브 층을 선택합니다.

| 층위 | 하는 일 | 공존하는 이웃 |
|------|---------|---------------|
| **L3 — Meta-Factory / Team-Architecture Factory** (우리) | 도메인 설명 → 에이전트 팀 + 스킬, 6가지 사전 정의된 팀 패턴 | — |
| L3 — Meta-Factory / Runtime-Configuration Factory | 결정적(deterministic)·반복 가능한 런타임 설정 생성 | [coleam00/Archon](https://github.com/coleam00/Archon) |
| L3 — Meta-Factory / Codex Runtime Port | 같은 컨셉, Codex 런타임 | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) |
| L2 — Cross-Harness Workflow | 여러 하네스 위에서 스킬·규칙·훅을 표준화 | [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) |

> Archon은 결정적 런타임 설정을 뽑아냅니다. Harness는 팀 아키텍처(파이프라인·팬아웃/팬인·전문가 풀·생성-검증·감독자·계층적 위임)와 에이전트가 쓸 스킬을 뽑아냅니다. 같은 L3의 서로 다른 서브 층입니다. 런타임 결정성은 Archon, 팀 아키텍처는 Harness, 또는 둘을 조합해서 쓰세요.

## 핵심 기능

- **에이전트 팀 설계** — 파이프라인, 팬아웃/팬인, 전문가 풀, 생성-검증, 감독자, 계층적 위임 등 6가지 아키텍처 패턴 지원
- **스킬 생성** — Progressive Disclosure 패턴으로 컨텍스트를 효율 관리하는 스킬 자동 생성
- **오케스트레이션** — 에이전트 간 데이터 전달, 에러 핸들링, 팀 조율 프로토콜 포함
- **검증 체계** — 트리거 검증, 드라이런 테스트, With-skill vs Without-skill 비교 테스트

## 하네스 진화 메커니즘 (Harness Evolution Mechanism)

하네스 진화 메커니즘은 "무엇이 먹혔고 무엇이 안 먹혔는가"의 델타를 팩토리로 되먹여, 다음 세대가 측정 가능하게 더 나아지도록 합니다. 실제 프로젝트에서 생성된 하네스가 사용될 때, `/harness:evolve` 스킬이 초기 아키텍처와 최종 출시 아키텍처 간 변화량을 포착해 팩토리로 되먹입니다. 다음번 같은 도메인에 대한 생성은 이 되먹임을 반영해 "출시 상태에 더 가까운 초안"에서 시작합니다.

```
초기 하네스 ──▶ 실 프로젝트 사용 ──▶ 출시 하네스
                                          │
                                          ▼ (/harness:evolve 로 델타 포착)
                                    ┌───────────────┐
                                    │   팩토리      │◀── 더 나은 다음 세대 초안
                                    └───────────────┘
```

이것이 **하네스 진화 메커니즘 (Harness Evolution Mechanism; JA: ハーネス進化メカニズム)** 입니다.

## 워크플로우

```
Phase 1: 도메인 분석
    ↓
Phase 2: 팀 아키텍처 설계 (에이전트 팀 vs 서브 에이전트)
    ↓
Phase 3: 에이전트 정의 생성 (.claude/agents/)
    ↓
Phase 4: 스킬 생성 (.claude/skills/)
    ↓
Phase 5: 통합 및 오케스트레이션
    ↓
Phase 6: 검증 및 테스트
```

## 설치

### 마켓플레이스 등록 후 설치

#### 마켓플레이스 추가
```shell
/plugin marketplace add revfactory/harness
```

#### 플러그인 설치
```shell
/plugin install harness@harness
```

### 글로벌 스킬로 직접 설치

```shell
# skills 디렉토리를 ~/.claude/skills/harness/에 복사
cp -r skills/harness ~/.claude/skills/harness
```

## 플러그인 구조

```
harness/
├── .claude-plugin/
│   └── plugin.json                 # 플러그인 매니페스트
├── skills/
│   └── harness/
│       ├── SKILL.md                # 메인 스킬 정의 (6 Phase 워크플로우)
│       └── references/
│           ├── agent-design-patterns.md   # 6가지 아키텍처 패턴
│           ├── orchestrator-template.md   # 팀/서브에이전트 오케스트레이터 템플릿
│           ├── team-examples.md           # 실전 팀 구성 예시 5종
│           ├── skill-writing-guide.md     # 스킬 작성 가이드
│           ├── skill-testing-guide.md     # 테스트/평가 방법론
│           └── qa-agent-guide.md          # QA 에이전트 통합 가이드
└── README.md
```

## 사용법

Claude Code에서 다음과 같이 트리거한다:

```
하네스 구성해줘
하네스 설계해줘
이 프로젝트에 맞는 에이전트 팀 구축해줘
```

### 실행 모드

| 모드 | 설명 | 권장 상황 |
|------|------|----------|
| **에이전트 팀** (기본) | TeamCreate + SendMessage + TaskCreate | 2개 이상 에이전트, 협업 필요 |
| **서브 에이전트** | Agent 도구 직접 호출 | 단발성 작업, 통신 불필요 |

<p align="center">
  <img src="harness_team.png" alt="Harness Agent Team" width="500">
</p>

### 아키텍처 패턴

| 패턴 | 설명 |
|------|------|
| 파이프라인 | 순차 의존 작업 |
| 팬아웃/팬인 | 병렬 독립 작업 |
| 전문가 풀 | 상황별 선택 호출 |
| 생성-검증 | 생성 후 품질 검수 |
| 감독자 | 중앙 에이전트가 동적 분배 |
| 계층적 위임 | 상위→하위 재귀적 위임 |

## 산출물

하네스가 생성하는 파일:

```
프로젝트/
├── .claude/
│   ├── agents/          # 에이전트 정의 파일
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # 스킬 파일
│       ├── analyze/
│       │   └── SKILL.md
│       └── build/
│           ├── SKILL.md
│           └── references/
```

## 사용 사례 — 이 프롬프트를 그대로 사용하세요

Harness 설치 후 아래 프롬프트를 Claude Code에 복사해서 사용하세요:

**딥 리서치**
```
리서치 하네스를 구성해줘. 어떤 주제든 여러 각도에서 조사할 수 있는 에이전트 팀이
필요해 — 웹 검색, 학술 자료, 커뮤니티 반응 — 교차 검증 후 종합 보고서를 작성하는 팀.
```

**웹사이트 제작**
```
풀스택 웹사이트 개발 하네스를 구성해줘. 디자인, 프론트엔드(React/Next.js),
백엔드(API), QA 테스트를 와이어프레임부터 배포까지 파이프라인으로 조율하는 팀.
```

**웹툰 제작**
```
웹툰 에피소드 제작 하네스를 구성해줘. 스토리 작성, 캐릭터 디자인 프롬프트,
패널 레이아웃 기획, 대사 편집 에이전트가 필요하고 서로의 작업물을
스타일 일관성 관점에서 리뷰해야 해.
```

**유튜브 콘텐츠 기획**
```
유튜브 콘텐츠 제작 하네스를 구성해줘. 트렌드 조사, 대본 작성, 제목/태그 SEO 최적화,
썸네일 컨셉 기획을 감독자 에이전트가 조율하는 팀.
```

**코드 리뷰**
```
종합 코드 리뷰 하네스를 구성해줘. 아키텍처, 보안 취약점, 성능 병목, 코드 스타일을
병렬로 감사하는 에이전트들이 결과를 하나의 리포트로 통합하는 팀.
```

**기술 문서 작성**
```
이 코드베이스에서 API 문서를 자동 생성하는 하네스를 구성해줘. 엔드포인트 분석,
설명 작성, 사용 예제 생성, 완성도 리뷰를 파이프라인으로 처리하는 팀.
```

**데이터 파이프라인 설계**
```
데이터 파이프라인 설계 하네스를 구성해줘. 스키마 설계, ETL 로직, 데이터 검증 규칙,
모니터링 설정을 계층적으로 위임하는 에이전트 팀.
```

**마케팅 캠페인**
```
마케팅 캠페인 제작 하네스를 구성해줘. 타겟 시장 조사, 광고 카피 작성,
비주얼 컨셉 디자인, A/B 테스트 계획을 반복적 품질 리뷰와 함께 진행하는 팀.
```

## 공존 — Harness와 이웃 저장소들

Harness는 Claude Code / 에이전트 프레임워크 생태계에서 혼자가 아닙니다. 아래 저장소들은 인접한 층위에 위치하며, 모두 "X는 ···, Harness는 ···" 병렬 구조로 기술되어 있어 용도에 맞게 선택하거나 조합할 수 있습니다.

| 저장소 | 저장소의 포지션 | Harness와의 관계 |
|--------|-----------------|------------------|
| [coleam00/Archon](https://github.com/coleam00/Archon) | "harness builder" — 결정적·반복 가능한 런타임 설정 | **같은 L3, 이웃 서브 층.** Archon은 Runtime-Configuration Factory, Harness는 Team-Architecture Factory. 런타임 결정성은 Archon, 팀 아키텍처는 Harness, 또는 조합. |
| [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) | 같은 컨셉의 Codex 포트 | **같은 L3, 다른 런타임.** Claude Code에서는 Harness, Codex에서는 meta-harness. |
| [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) | "Agent harness performance & workflow layer" — 기존 하네스 위에 앉는 표준화 층 | **다른 층위.** ECC는 여러 하네스 위 표준화 층, Harness는 하네스를 생성하는 팩토리. 직렬 조합 가능. |
| [wshobson/agents](https://github.com/wshobson/agents) | 서브 에이전트 / 스킬 카탈로그 (182 agents, 149 skills) | **팩토리 ↔ 부품 공급.** wshobson은 "쇼핑할 카탈로그", Harness는 "팀 설계". Harness가 만든 팀에 wshobson 항목을 부품으로 흡수. |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 상태 그래프 오케스트레이션, LLM-agnostic | **다른 트랙.** 장기 실행·상태 복구가 핵심이면 LangGraph, Claude Code 네이티브의 빠른 팀 설계가 핵심이면 Harness. |

## Harness로 만든 프로젝트

### Harness 100

**[revfactory/harness-100](https://github.com/revfactory/harness-100)** — 10개 도메인, 100개의 프로덕션 레디 에이전트 팀 하네스 (한영 200패키지). 각 하네스에 4-5명의 전문 에이전트, 오케스트레이터 스킬, 도메인 특화 스킬이 포함되어 있으며, 모두 이 플러그인으로 생성되었습니다. 콘텐츠 제작, 소프트웨어 개발, 데이터/AI, 비즈니스 전략, 교육, 법률, 헬스케어 등 1,808개 마크다운 파일.

### 연구: Harness 적용 전후 A/B 테스트

**[revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)** — 15개 소프트웨어 엔지니어링 과제에 대한 통제 실험으로, 구조화된 사전 설정이 LLM 코드 에이전트 출력 품질에 미치는 영향을 측정했습니다.

| 지표 | Harness 미적용 | Harness 적용 | 개선 |
|------|:-:|:-:|:-:|
| 평균 품질 점수 | 49.5 | 79.3 | **+60%** |
| 승률 | — | — | **100%** (15/15) |
| 출력 분산 | — | — | **-32%** |

핵심 발견: 과제 난이도가 높을수록 개선 효과가 증대 (Basic +23.8, Advanced +29.6, Expert +36.2).

**어디에서나 이 문장을 그대로 사용하세요:** 평균 품질 +60% (49.5 → 79.3), 15/15 승률, 출력 분산 −32% (n=15, 저자 자체 측정 A/B, 제3자 재현 실험 진행 중).

> 논문 전문: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality.*

## 요구사항

- [에이전트 팀 기능 활성화](https://code.claude.com/docs/en/agent-teams): `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

## FAQ

<details>
<summary><b>Q1. "+60%"는 과대 포장 아닌가요?</b></summary>

**A.** +60%는 **저자 자체 A/B(n=15, 15개 과제, 자매 저장소 `claude-code-harness`에서 측정)** 결과입니다. 본 저장소는 이 수치를 인용할 때 언제나 "n=15, 저자 자체 측정, 제3자 재현 진행 중"을 같은 문장 안에 병기합니다. 조직 도입 시에는 2~4주 내부 파일럿으로 자체 수치를 측정할 것을 권장합니다.

**Evidence:**
- 저자 A/B: [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness)
- 논문: *Hwang, M. (2026). Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*
</details>

<details>
<summary><b>Q2. 왜 "harness builder"가 아니라 "harness factory"인가요? Archon과 경쟁하나요?</b></summary>

**A.** Archon은 결정적 런타임 설정을 생성하는 **Runtime-Configuration Factory** 성격, Harness는 에이전트 팀 아키텍처(팀 구조·메시지 프로토콜·리뷰 게이트)를 생성하는 **Team-Architecture Factory** 성격입니다. 둘은 **같은 L3 Meta-Factory 층의 이웃 서브 층**이며, 용도가 다릅니다. 결정적 런타임이 필요하면 Archon, 팀 아키텍처 6패턴 사전 정의가 필요하면 Harness. 조합 사용(아키텍처 설계 → 런타임 배포)도 가능합니다.

**Evidence:**
- Archon 자기 규정: [clawfit docs/reference-levels.md](https://github.com/hongsw/clawfit/blob/main/docs/reference-levels.md)
- 서브 층 선언: 본 README **카테고리 — Harness는 어디에 서 있나요** 섹션
- Archon 저장소: [github.com/coleam00/Archon](https://github.com/coleam00/Archon)
</details>

<details>
<summary><b>Q3. "Claude Code 전용"이 너무 좁은 것 아닌가요? Gemini·Codex는?</b></summary>

**A.** 현재 공식 런타임은 Claude Code 단일입니다. 같은 컨셉의 Codex 포트 [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)가 이미 공개되어 있어, 기존 Codex 팀은 그쪽에서 바로 시작할 수 있습니다. Harness는 "Claude Code 네이티브·깊게"를 택한 상태이며, 크로스 런타임 수요는 공존 저장소(meta-harness, harness-init, OpenRig)와의 연계 계획을 로드맵에 반영할 예정입니다.

**Evidence:**
- Codex 포트: [github.com/SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness)
- 크로스 런타임 스캐폴더: [github.com/Gizele1/harness-init](https://github.com/Gizele1/harness-init)
</details>

## 라이선스

Apache 2.0
