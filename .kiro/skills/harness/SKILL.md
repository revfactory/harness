---
name: harness
description: >-
  Kiro용 하네스를 구성합니다. 도메인/프로젝트에 맞는 전문 Kiro 에이전트(.kiro/agents/*.json)와
  스킬(.kiro/skills/)을 설계·생성하는 메타 스킬. (1) '하네스 구성/구축/설계해줘', (2) '에이전트 팀
  만들어줘', '전문 에이전트 세트 만들어줘', (3) 새 도메인에 대한 자동화 체계 구축, (4) 하네스 재구성/확장,
  (5) '하네스 점검/감사/현황', '에이전트/스킬 동기화' 등 운영·유지보수 요청 시 사용. '다시 구성', '재실행',
  '에이전트 추가', '스킬 추가/수정', '하네스 업데이트' 같은 후속 요청에도 반드시 사용한다.
---

# Harness (Kiro) — Agent & Skill Architect

도메인/프로젝트에 맞는 하네스를 구성하고, 각 에이전트의 역할을 정의하며, 에이전트가 사용할 스킬을 생성하는 메타 스킬.
**Claude Code용 원본을 Kiro 네이티브 구조(JSON 에이전트 + skill:// + steering)로 포팅한 버전이다.**

**핵심 원칙:**
1. 에이전트 정의(`.kiro/agents/*.json`)와 스킬(`.kiro/skills/`)을 분리해 생성한다 — 에이전트는 "누가", 스킬은 "어떻게".
2. **다중 전문 에이전트가 기본 실행 모드다.** Kiro에는 Claude Code의 에이전트 팀(`TeamCreate`/`SendMessage`/`TaskCreate`)이 없으므로, 대신 (a) 전문 에이전트 여러 개를 만들어 `/agent`로 전환하거나, (b) 오케스트레이터 에이전트가 순차 위임한다. 데이터는 `_workspace/` 파일로 주고받는다.
3. **`.kiro/steering/harness.md`에 하네스 포인터를 등록한다.** — steering은 kiro_default가 매 세션 자동 로드하므로, 트리거 규칙 + 변경 이력만 최소 기록한다 (Claude Code의 CLAUDE.md 대체).
4. **하네스는 진화하는 시스템이다.** — 매 실행 후 피드백을 반영하고, 에이전트·스킬·steering을 지속 갱신한다.

> 아키텍처 패턴/에이전트 분리 기준/예시 전문은 클론된 원본 `skills/harness/references/`를 참고한다
> (`agent-design-patterns.md`, `team-examples.md`, `orchestrator-template.md`, `skill-writing-guide.md`,
> `skill-testing-guide.md`, `qa-agent-guide.md`). Claude 전용 도구 명칭은 아래 "Kiro 매핑"으로 치환해 읽는다.

## Kiro 매핑 (원본 reference를 읽을 때 치환)

| 원본(Claude Code) | Kiro 대응 |
|---|---|
| `.claude/agents/{name}.md` (마크다운) | `.kiro/agents/{name}.json` (JSON 설정) |
| `.claude/skills/{name}/SKILL.md` | `.kiro/skills/{name}/SKILL.md` (동일 형식, frontmatter 필수) |
| `CLAUDE.md` 포인터 | `.kiro/steering/harness.md` |
| `TeamCreate` / `SendMessage` / `TaskCreate` (팀 자체조율) | **없음** → 전문 에이전트 다수 + `/agent` 전환, 또는 오케스트레이터 순차 위임 |
| `Agent(subagent_type, run_in_background)` | **문서화된 멀티에이전트 도구 없음** → `_workspace/` 파일 핸드오프 + 사용자가 에이전트 전환 |
| builtin 타입 `Explore`/`Plan`(읽기전용) | `tools: ["read","grep","glob"]` + 동일 `allowedTools` (write 미부여) |
| builtin 타입 `general-purpose` | `tools`에 read/write/shell/web 등 필요한 도구 부여 |
| `model: "opus"` | `model` 필드에 모델 ID 지정(미지정 시 기본 모델) |

## 워크플로우

### Phase 0: 현황 감사
하네스가 트리거되면 가장 먼저 기존 현황을 확인한다.
1. `.kiro/agents/`, `.kiro/skills/`, `.kiro/steering/harness.md`, `_workspace/`를 읽는다.
2. 실행 모드 분기:
   - **신규 구축**: agents/skills 비어있음 → Phase 1부터 전체 실행
   - **기존 확장**: 하네스 존재 + 에이전트/스킬 추가 요청 → 필요한 Phase만 실행
   - **운영/유지보수**: 감사·수정·동기화 요청 → Phase 7-5로 이동
3. 기존 에이전트/스킬 목록과 steering 기록을 대조해 불일치(drift)를 감지한다.
4. 감사 결과를 요약 보고하고 실행 계획을 확인받는다.

### Phase 1: 도메인 분석
1. 요청에서 도메인/프로젝트와 핵심 작업 유형(생성·검증·편집·분석 등)을 파악한다.
2. 코드베이스를 탐색해 기술 스택·데이터 모델·주요 모듈을 파악한다.
3. 기존 에이전트/스킬과의 충돌·중복을 분석한다.
4. **사용자 숙련도 감지** — 대화 단서로 기술 수준을 파악하고 톤을 조절한다.

### Phase 2: 아키텍처 설계
1. 작업을 전문 영역으로 분해하고, 6개 패턴 중 적합한 것을 고른다
   (파이프라인 / 팬아웃·팬인 / 전문가 풀 / 생성-검증 / 감독자 / 계층적 위임 — `references/agent-design-patterns.md`).
2. **Kiro 실행 모드 선택:**
   - **순차 파이프라인**(권장 기본): 오케스트레이터 에이전트가 단계별로 `_workspace/`에 산출물을 쌓으며 진행. 한 에이전트가 이전 단계 파일을 Read해 다음 단계 수행.
   - **전문가 세트 + 수동 전환**: 영역별 전문 에이전트를 만들고, 사용자가 `/agent <name>`으로 전환하며 사용. `keyboardShortcut`로 빠른 전환 지원.
   - 둘을 혼합할 수 있다(오케스트레이터 1 + 전문가 N).
3. 에이전트 분리 기준(전문성/병렬성/컨텍스트/재사용성)으로 에이전트 수를 결정한다. 3~5개 집중 에이전트가 산만한 7개보다 낫다.

### Phase 3: 에이전트 정의 생성 (.kiro/agents/*.json)

신규 생성 전 기존 에이전트와 중복을 확인한다(역할 완전 포함 시 재사용, 부분 포함이면 일반화 검토).

**모든 에이전트는 `.kiro/agents/{name}.json` 파일로 정의한다.** 파일로 존재해야 다음 세션에서 `/agent`로 재사용 가능하다. 표준 구조:

```json
{
  "name": "analyst",
  "description": "요구사항을 분석하고 _workspace에 산출물을 남기는 분석 전문가",
  "prompt": "당신은 [도메인] 분석 전문가입니다.\n\n## 핵심 역할\n1. ...\n## 작업 원칙\n- ...\n## 입력/출력 프로토콜\n- 입력: _workspace/ 의 이전 단계 산출물(있으면 Read)\n- 출력: _workspace/01_analyst_*.md\n## 이전 산출물 처리\n- 이전 결과 파일이 있으면 읽고 개선점을 반영한다\n- 사용자 피드백이 주어지면 해당 부분만 수정한다\n## 에러 핸들링\n- 1회 재시도, 재실패 시 누락을 명시하고 진행",
  "tools": ["read", "write", "grep", "glob"],
  "allowedTools": ["read", "grep", "glob"],
  "resources": [
    "file://_workspace/**/*.md",
    "skill://.kiro/skills/**/SKILL.md"
  ]
}
```

규칙:
- **읽기전용 역할**(분석·리뷰·계획)은 `tools`에서 `write`/`shell`을 빼서 안전하게 한다(원본 Explore/Plan 대체).
- **구현 역할**은 `read`,`write`,`shell`,`code` 등 필요한 도구를 부여한다.
- 각 에이전트의 스킬은 `resources`에 `skill://`로 등록한다.
- 모델을 고정하려면 `model` 필드에 모델 ID를 명시한다(생략 시 기본 모델).
- 생성 후 검증: `kiro-cli agent validate --path .kiro/agents/{name}.json`.

**QA 에이전트 포함 시:** QA는 검증 스크립트 실행이 필요하므로 `shell` 도구를 부여한다(읽기전용 금지). 핵심은 "존재 확인"이 아니라 **경계면 교차 비교**(예: API 응답과 프론트 훅을 동시에 Read해 shape 비교). 전체 완성 후 1회가 아니라 모듈 완성 직후 **점진적**으로 실행한다. 상세: `references/qa-agent-guide.md`.

### Phase 4: 스킬 생성 (.kiro/skills/*/SKILL.md)

신규 생성 전 기존 스킬과 중복을 확인한다. 각 스킬은 `.kiro/skills/{name}/SKILL.md`에 만든다(구조: SKILL.md 필수 + 선택적 `scripts/`·`references/`·`assets/`).

- **Frontmatter 필수**(`name`, `description`) — Kiro가 `skill://`로 메타데이터를 startup에 로드하고 본문은 on-demand 로드한다(progressive disclosure).
- **description은 적극적("pushy")으로** — 스킬이 하는 일 + 구체적 트리거 상황을 모두 기술하고, 유사하지만 트리거하면 안 되는 경우와 구분한다. **후속 작업 키워드("다시 실행","수정","보완")도 포함**한다.
- **본문 작성:** Why를 설명(강압 지시 대신 이유), lean하게(<500줄, 초과 시 `references/` 분리·포인터만 남김), 일반화(오버피팅 금지), 반복 코드는 `scripts/`에 번들링, 명령형 어조.
- 에이전트가 스킬을 쓰게 하려면 해당 에이전트 JSON의 `resources`에 `skill://.kiro/skills/{name}/SKILL.md`를 추가한다.

> 상세: `references/skill-writing-guide.md`.

### Phase 5: 통합 및 오케스트레이션

팀 자체조율 도구가 없으므로 Kiro에서는 **오케스트레이터 에이전트** 또는 **steering 규칙**이 워크플로우를 엮는다.

**5-1. 오케스트레이터 에이전트(권장):** `.kiro/agents/{domain}-orchestrator.json`을 만든다. prompt에 Phase 순서·각 단계 산출물 경로·다음 단계로의 핸드오프를 명시한다. 이 에이전트가 단계별로 직접 작업하거나, 사용자에게 다음에 어떤 전문 에이전트로 전환할지 안내한다.

**5-2. 데이터 전달(파일 기반):**
- 작업 디렉토리 하위에 `_workspace/`를 만들어 중간 산출물 저장.
- 파일명 컨벤션: `{phase}_{agent}_{artifact}.{ext}` (예: `01_analyst_requirements.md`).
- 최종 산출물만 사용자 지정 경로에 출력, 중간 파일은 `_workspace/`에 보존(감사 추적용).

**5-3. 에러 핸들링:** 1회 재시도 후 재실패 시 해당 결과 없이 진행(보고서에 누락 명시). 상충 데이터는 삭제하지 않고 출처 병기.

**5-4. steering 포인터 등록:** `.kiro/steering/harness.md`에 최소 포인터(트리거 규칙 + 변경 이력)만 기록한다. 에이전트/스킬 목록·디렉토리 구조는 넣지 않는다(파일 시스템·이 스킬에서 관리되므로 중복). 템플릿:

```markdown
## 하네스: {도메인명}
**목표:** {핵심 목표 한 줄}
**트리거:** {도메인} 관련 작업 요청 시 harness 스킬 또는 `{orchestrator}` 에이전트를 사용하라. 단순 질문은 직접 응답.
**에이전트 전환:** /agent {name} 로 전문 에이전트 전환.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| {YYYY-MM-DD} | 초기 구성 | 전체 | - |
```

**5-5. 후속 작업 지원:** 오케스트레이터 prompt Phase 1에 컨텍스트 확인 단계를 둔다 — `_workspace/` 존재 + 부분 수정 요청 → 해당 에이전트만 재실행 / `_workspace/` 존재 + 새 입력 → 기존을 `_workspace_prev/`로 이동 후 새 실행 / 미존재 → 초기 실행.

### Phase 6: 검증 및 테스트
- **구조 검증:** 모든 에이전트 JSON이 `.kiro/agents/`에 있고 `kiro-cli agent validate`를 통과하는가. 스킬 frontmatter(name/description)가 유효한가. `skill://` 경로가 실제 파일과 일치하는가.
- **트리거 검증:** 각 스킬 description에 대해 should-trigger 쿼리(8~10개)와 should-NOT-trigger near-miss 쿼리(8~10개, 경계가 모호한 것)를 작성해 점검한다. 기존 스킬과의 트리거 충돌도 확인.
- **드라이런:** 오케스트레이터 Phase 순서가 논리적인지, 데이터 전달 경로에 빈 구간(dead link)이 없는지, 각 에이전트 입력이 이전 단계 출력과 매칭되는지 확인.
- **실행 테스트:** 각 스킬에 현실적 프롬프트 2~3개로 실행, 가능하면 with-skill vs without-skill 비교로 부가가치 확인. 문제 발견 시 피드백을 **일반화**해 수정 후 재테스트.
- 상세: `references/skill-testing-guide.md`.

### Phase 7: 하네스 진화
- **7-1. 실행 후 피드백 수집:** 매 실행 후 개선점·구성 변경 희망을 가볍게 묻는다(강요 금지).
- **7-2. 반영 경로:** 결과 품질→해당 스킬 / 역할→에이전트 JSON / 워크플로우 순서→오케스트레이터 / 트리거 누락→스킬 description.
- **7-3. 변경 이력:** 모든 변경을 `.kiro/steering/harness.md` 변경 이력 테이블에 기록(퇴행 방지).
- **7-4. 진화 트리거:** 같은 피드백 2회 이상 반복, 에이전트 반복 실패, 사용자가 오케스트레이터 우회 시 진화를 제안한다.
- **7-5. 운영/유지보수:** (1) 현황 감사로 불일치 목록 생성 → 보고, (2) 한 번에 하나씩 추가/수정/삭제, (3) steering 변경 이력 갱신, (4) 구조·트리거 검증.

## 산출물 체크리스트
- `.kiro/agents/*.json` — 에이전트 정의(읽기전용 역할은 write/shell 미부여), `kiro-cli agent validate` 통과
- `.kiro/skills/*/SKILL.md` — frontmatter(name/description) 유효, description "pushy" + 후속 키워드 포함, 본문 <500줄
- 각 에이전트 JSON `resources`에 사용할 스킬 `skill://` 등록
- 오케스트레이터 에이전트 1개(파일 기반 핸드오프 + 컨텍스트 확인 + 에러 핸들링)
- `_workspace/` 파일명 컨벤션 적용, 중간 산출물 보존
- `.kiro/steering/harness.md` 포인터(트리거 규칙 + 변경 이력) 등록·갱신
- 신규 에이전트/스킬 생성 전 중복 검토 완료
- 트리거 검증(should / should-NOT) 완료
- `.kiro/commands/` 류는 생성하지 않음
