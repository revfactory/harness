# Context-Harness

[English](README.md) | **한국어**

> Claude Code용 컨텍스트 기반 팀 아키텍처 팩토리. [Harness](reference/harness/)를 확장하여 프로젝트 컨텍스트 자동 초기화와 세션 관리를 추가했습니다.

## 특징

- **컨텍스트 자동 생성** — `/harness` 호출 시 `context/`, `outputs/`, `BRIEF.md`, `HANDOFF.md`, `ROADMAP.md`, `CLAUDE.md` 자동 생성
- **에이전트 팀 설계** — 6가지 아키텍처 패턴
- **스킬 생성** — Progressive Disclosure로 효율적인 컨텍스트 관리
- **워크스페이스 분리** — 소스(`skills/`)와 런타임(`_workspace/`) 분리로 깔끔한 git 히스토리

## 설치

> **Private repo입니다.** 직접 설치만 가능합니다. Marketplace는 지원되지 않습니다.

### 방법 1: SSH Clone (권장)

```bash
git clone git@github.com:AMOSA-DEV/harness.git
cp -r harness/skills/harness ~/.claude/skills/harness
```

### 방법 2: PAT로 HTTPS Clone

```bash
# https://github.com/settings/tokens 에서 'repo' 스코프를 가진 PAT 생성
git clone https://<TOKEN>@github.com/AMOSA-DEV/harness.git
cp -r harness/skills/harness ~/.claude/skills/harness
```

### 방법 3: 직접 다운로드

```bash
# GitHub에서 ZIP 다운로드 후 압축 해제, 그리고:
cp -r harness/skills/harness ~/.claude/skills/harness
```

## 사용법

```
하네스 구성해줘
Build a harness for this project
```

## 아키텍처 패턴

### 1. 파이프라인 (Pipeline)
순차적 의존 작업. 이전 에이전트의 출력이 다음 에이전트의 입력이 됩니다.

```
[분석] → [설계] → [구현] → [검증]
```

**적합한 경우:** 단계 간 강한 순차 의존성
**예시:** 소설 집필 — 세계관 → 캐릭터 → 플롯 → 집필 → 편집

### 2. 팬아웃/팬인 (Fan-out/Fan-in)
병렬 독립 작업 후 결과 통합.

```
         ┌→ [전문가A] ─┐
[입력] ─┼→ [전문가B] ─┼→ [통합]
         └→ [전문가C] ─┘
```

**적합한 경우:** 동일 입력에 대해 여러 관점 필요
**예시:** 종합 리서치 — 공식/미디어/커뮤니티/배경 병렬 조사 → 통합 보고서

### 3. 전문가 풀 (Expert Pool)
상황에 따라 적절한 전문가를 선택 호출.

```
[라우터] → { 전문가A | 전문가B | 전문가C }
```

**적합한 경우:** 입력 유형에 따라 다른 처리 필요
**예시:** 코드 리뷰 — 해당 영역 전문가만 호출 (보안/성능/아키텍처)

### 4. 생성-검증 (Producer-Reviewer)
생성과 품질 검증이 쌍으로 동작.

```
[생성] → [검증] → (문제 있으면) → [생성] 재시도
```

**적합한 경우:** 산출물 품질 보장이 중요하고 객관적 기준 존재
**예시:** 웹툰 — 작가 생성 → 검수자 확인 → 문제 패널 재생성

### 5. 감독자 (Supervisor)
중앙 에이전트가 작업 상태를 관리하며 동적으로 분배.

```
         ┌→ [워커A]
[감독자] ─┼→ [워커B]    ← 감독자가 모니터링하고 조정
         └→ [워커C]
```

**적합한 경우:** 작업량 가변적이거나 런타임에 분배 결정 필요
**예시:** 대규모 코드 마이그레이션 — 감독자가 파일 목록 분석 후 워커 배치

### 6. 계층적 위임 (Hierarchical Delegation)
상위 에이전트가 하위 에이전트에 재귀적으로 위임.

```
[총괄] → [팀장A] → [실무자A1]
                  → [실무자A2]
       → [팀장B] → [실무자B1]
```

**적합한 경우:** 문제가 자연스럽게 계층적으로 분해되는 구조
**예시:** 풀스택 앱 — 총괄 → 프론트엔드팀장 → (UI/로직/테스트) + 백엔드팀장 → (API/DB/테스트)

## 프로젝트 구조

```
context-harness/
├── skills/harness/          # 소스 (git 추적)
│   ├── SKILL.md
│   ├── references/
│   └── team-architecture-templates/
├── _workspace/              # 런타임 산출물 (git 제외)
├── reference/harness/       # 원작자 Harness (git 제외)
├── LICENSE
├── NOTICE
└── README.md
```

## 라이선스

Apache 2.0 — 원작자 [robin](https://github.com/revfactory/harness)의 Harness를 기반으로 합니다.
