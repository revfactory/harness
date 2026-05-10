# Context System Guide

## 개요

harness v2의 핵심 개선사항 중 하나는 **프로젝트 컨텍스트 자동 초기화**이다. `/harness` 호출 시 프로젝트 루트에 표준 컨텍스트 구조를 자동 생성하여, 사용자가 매번 수동으로 설정할 필요를 없앤다.

## 자동 생성 구조

`/harness` 호출 시 다음 구조가 프로젝트 루트에 생성된다 (이미 존재하면 건너뜀):

```
{project-root}/
├── context/              # 글로벌 컨텍스트
│   ├── ABOUT-ME.md       # 사용자 신원, 역할, 커뮤니케이션 선호도
│   ├── BRAND-VOICE.md    # 톤, 언어, 금지 패턴
│   ├── WORKING-RULES.md  # 작업 규칙 (MUST/SHOULD)
│   ├── GLOSSARY.md       # 도메인 용어집
│   └── LESSONS.md        # 학습 사항 기록
├── BRIEF.md              # 현재 작업 브리프
├── HANDOFF.md            # 세션 전달 노트
├── ROADMAP.md            # 작업 로드맵
└── CLAUDE.md             # 워크스페이스 헌법 + context 참조 규칙
```

## Context 파일 역할

| 파일 | 목적 | 언제 읽는가 |
|------|------|-----------|
| `ABOUT-ME.md` | 사용자 신원, 역할, 선호도 | 세션 시작 시 |
| `BRAND-VOICE.md` | 톤, 언어, 금지 패턴 | 세션 시작 시 |
| `WORKING-RULES.md` | MUST/SHOULD 규칙 | 작업 수행 전 |
| `GLOSSARY.md` | 도메인 용어, 파일 정의 | 용어 확인 필요 시 |
| `LESSONS.md` | 과거 학습 사항 | 작업 완료 후 (기록) |
| `BRIEF.md` | **이번 세션의 구체적 목표** (ROADMAP의 한 조각) | 작업 수행 전 |
| `HANDOFF.md` | **세션 간 연결** (완료 작업 → 다음 세션 할 일) | 작업 완료 후 (업데이트) |
| `ROADMAP.md` | **장기 계획** (BRIEF들이 모여 이루는 큰 그림) | 로드맵 참조 시 |
| `CLAUDE.md` | 워크스페이스 헌법 + context 참조 규칙 | 항상 (세션 시작 시 자동 로드) |

## Context 참조 규칙

에이전트/스킬이 자동으로 컨텍스트를 활용하도록 CLAUDE.md에 명시한다:

```markdown
## Context Reference Rules

1. **Session start**: Read `context/ABOUT-ME.md` + `context/BRAND-VOICE.md`
2. **Before work**: Read `BRIEF.md` + `context/WORKING-RULES.md`
3. **Domain terms**: Reference `context/GLOSSARY.md`
4. **After work**: Record learnings in `context/LESSONS.md`, update `HANDOFF.md`
```

## 산출물 관리

에이전트 실행 중 생성되는 파일은 두 가지로 구분된다:

- **중간 산출물**: `_workspace/` 디렉토리에 저장. 파일명 컨벤션 `{phase}_{agent}_{artifact}.{ext}` 적용 (예: `01_planner_plan.md`, `02_writer_draft.md`). 사후 검증·감사 추적용으로 보존한다.
- **최종 산출물**: 오케스트레이터가 `_workspace/` 내용을 취합·가공하여 사용자 지정 경로(`{output-path}`)에 생성한다. 경로는 프로젝트 성격에 따라 다를 수 있으며 하드코딩하지 않는다.

`_workspace/` 폴더는 오케스트레이터가 Phase 1 준비 단계에서 직접 생성한다. 상세 생성 로직은 `references/orchestrator-template.md`의 "Phase 1: 준비" 참조.

## 작성 템플릿

각 context 파일의 작성 예시는 `references/context-writing-templates.md`를 참조한다.

## Phase 1에서의 Context 초기화 흐름

1. `context/` 폴더 존재 여부 확인
2. 없으면 `ABOUT-ME.md`, `BRAND-VOICE.md`, `WORKING-RULES.md`, `GLOSSARY.md`, `LESSONS.md` 생성 (템플릿 기반)
3. `BRIEF.md`, `HANDOFF.md`, `ROADMAP.md` 생성 (템플릿 기반)
4. `CLAUDE.md` 생성/업데이트 (context 참조 규칙 포함)
5. 사용자에게 "context 파일들을 자신의 상황에 맞게 채워달라"고 안내
