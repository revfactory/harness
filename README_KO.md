<p align="center">
  <img src="https://img.shields.io/badge/Version-2.1.0-brightgreen.svg" alt="Version">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/실행모드-3종-teal.svg" alt="3 Execution Modes">
  <img src="https://img.shields.io/badge/패턴-6+품질패턴-orange.svg" alt="Patterns">
</p>

# Harness v2 — Claude Code를 위한 팀 아키텍처 팩토리

[English](README.md) | **한국어**

> **Harness는 Claude Code용 팀 아키텍처 팩토리입니다.** **"하네스 구성해줘"** 한 문장으로, 플러그인이 도메인 설명을 에이전트 팀과 그들이 쓸 스킬로 변환합니다.

## v2에서 달라진 것

v2는 현행 Claude Code 멀티에이전트 런타임에 맞춰 바닥부터 재구축했습니다:

- **3중 네이티브 실행 모드.** v1은 이제 존재하지 않는 실험적 `TeamCreate` API 위에 지어져 있었습니다. v2는 실제로 출시된 프리미티브를 대상으로 합니다:
  1. **워크플로우 오케스트레이션** — 결정적 스크립트(`pipeline()` / `parallel()` / 스키마 / 버짓)로 팬아웃·검증 루프·대규모 실행
  2. **퍼시스턴트 에이전트 협업** — 이름 붙인 에이전트 + `SendMessage` + 공유 태스크, 턴을 넘어 컨텍스트 유지
  3. **서브에이전트 위임** — 경량 단발 병렬 호출
- **워크플로우 네이티브 품질 패턴.** 적대적 검증, 심판 패널, loop-until-dry, 다각 스윕, 완전성 비평가 — 생성된 하네스가 "그럴듯하지만 틀린" 산출물을 걸러내도록 체계화.
- **실험 플래그 완전 제거.** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 의존성이 사라졌습니다.
- **합리적 모델 정책.** v1은 모든 에이전트를 `model: "opus"`로 고정했습니다. v2는 업무의 복잡도·작업 기간·자율성·응답 속도에 따라 에이전트별로 opus/sonnet 티어를 선택하며, 무근거 일괄 지정을 금지합니다.
- **`/harness:evolve` 실제 출시.** v1이 문서로만 약속했던 진화 메커니즘이 실제 스킬로 제공됩니다: 초기 구성과 현재 상태의 델타를 포착하고, 피드백을 일반화하여 에이전트·스킬·오케스트레이터에 되먹입니다.
- **v1 마이그레이션 내장.** 팩토리가 v1 산출물(`TeamCreate`, `TeamDelete`, 실험 플래그)을 감지하면 기계적 마이그레이션 경로를 제안합니다.

## 핵심 기능

- **에이전트 팀 설계** — 6가지 아키텍처 패턴(파이프라인, 팬아웃/팬인, 전문가 풀, 생성-검증, 감독자, 계층적 위임), 각 패턴에 최적 실행 모드 매핑
- **스킬 생성** — Progressive Disclosure로 컨텍스트를 효율 관리하는 스킬 자동 생성
- **오케스트레이션** — 데이터 전달 프로토콜(구조화 스키마, 파일, 메시지, 태스크), 에러 핸들링, resume 지원
- **검증 체계** — 트리거 검증, 드라이런, With-skill vs Without-skill A/B 테스트 (A/B 자체를 워크플로우로 구성 가능)
- **진화** — `/harness:evolve`가 사용 피드백을 측정 가능한 다음 세대 개선으로 변환

## 워크플로우

```
Phase 0: 현황 감사 (신규/확장/유지보수 분기 — v1 산출물 감지 포함)
Phase 1: 도메인 분석 (작업의 제어 흐름 형태 포함)
Phase 2: 실행 모드 & 팀 아키텍처 설계
Phase 3: 에이전트 정의 생성 (.claude/agents/)
Phase 4: 스킬 생성 (.claude/skills/)
Phase 5: 오케스트레이션 통합 & CLAUDE.md 포인터
Phase 6: 검증 및 테스트
Phase 7: 운영/유지보수 — 진화는 /harness:evolve
```

## 설치

### 마켓플레이스 설치

```shell
/plugin marketplace add revfactory/harness
/plugin install harness@harness-marketplace
```

### 글로벌 스킬로 직접 설치

```shell
cp -r skills/harness ~/.claude/skills/harness
cp -r skills/evolve ~/.claude/skills/harness-evolve
```

환경 변수나 실험 플래그가 필요 없습니다.

## 사용법

```
하네스 구성해줘
하네스 설계해줘
이 프로젝트에 맞는 에이전트 팀 구축해줘
```

생성된 하네스를 사용한 후:

```
하네스 회고해줘 / 이 피드백 하네스에 반영해줘
```

### 실행 모드 선택

| 모드 | 프리미티브 | 언제 |
|------|-----------|------|
| **워크플로우 오케스트레이션** | `Workflow` 스크립트 | 제어 흐름이 결정적: 열거 가능한 팬아웃, 검증 루프, 대규모, 구조화 출력 |
| **퍼시스턴트 에이전트** | `Agent(name:)` + `SendMessage` + 태스크 | 컨텍스트를 유지하는 장기 전문가, 반복 피드백·협상 |
| **서브에이전트 위임** | 단발 `Agent` 호출 | 결과만 필요한 병렬 위임 |

팩토리는 팀 크기가 아니라 **제어 흐름의 형태**로 모드를 선택하며, Phase별로 모드를 섞는 하이브리드도 지원합니다.

## 산출물

```
프로젝트/
├── .claude/
│   ├── agents/          # 에이전트 정의 (누가)
│   │   ├── analyst.md
│   │   ├── builder.md
│   │   └── qa.md
│   └── skills/          # 스킬 (어떻게) + 오케스트레이터 1개 (누가 언제 어떤 순서로)
│       ├── analyze/SKILL.md
│       └── build/SKILL.md
└── CLAUDE.md            # 최소 포인터: 트리거 규칙 + 변경 이력
```

## v1에서 마이그레이션

[docs/migration-v1-to-v2.md](docs/migration-v1-to-v2.md) 참조. 요약: `TeamCreate`/`TeamDelete`/브로드캐스트/플래그 참조 제거 → 팬아웃을 워크플로우 스크립트로 전환 → 남은 협업을 이름 붙인 에이전트 + `SendMessage`로 재작성 → 일괄 `model: "opus"` 고정 해제. 팩토리가 v1 산출물을 감지하면 이 과정을 자동화합니다 (Phase 0).

## 선행 연구 결과 (v1)

15개 소프트웨어 엔지니어링 과제에 대한 통제 A/B로 구조화된 사전 설정이 LLM 코드 에이전트 출력 품질에 미치는 영향을 측정: 평균 품질 49.5 → 79.3 (+60%), 승률 15/15, 출력 분산 −32% (n=15, 저자 자체 측정, [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness) 참조). 저자 측정 수치이므로 도입 결정 시에는 자체 파일럿 측정을 권장합니다.

## 라이선스

Apache 2.0
