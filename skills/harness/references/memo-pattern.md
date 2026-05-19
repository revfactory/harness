# Memo 패턴 — 분산 슬롯 + 공유 헤더 (선택적 패턴)

장기 작업·세션 재개·자동 컴팩트로 인한 토큰 폭증과 컨텍스트 유실 문제를 완화하는 권장 패턴. **모든 하네스에 강제하지 않으며**, Phase 1의 도메인 분석에서 적용 여부를 판단한다.

## 목차

1. [언제 적용하고 언제 적용하지 않는가](#언제-적용하고-언제-적용하지-않는가)
2. [핵심 철학 — 독립성 + 협업 + 토큰 효율](#핵심-철학)
3. [구조 — 분산 슬롯 + 공유 헤더](#구조)
4. [쓰기/읽기 규칙](#쓰기읽기-규칙)
5. [마일스톤 갱신 정책](#마일스톤-갱신-정책)
6. [다른 메커니즘과의 역할 분리](#역할-분리)
7. [충돌 시 우선순위](#충돌-시-우선순위)
8. [압축·폴딩 정책](#압축폴딩-정책)
9. [세션 재개 시나리오](#세션-재개-시나리오)
10. [적용 예시](#적용-예시)
11. [흔한 안티패턴](#안티패턴)

---

## 언제 적용하고 언제 적용하지 않는가

| 적용 권장 | 적용 비권장 |
|----------|-----------|
| 작업이 **30분 이상** 이어질 가능성 | 단발성 자동화(파일 정리·스크립트 1회 실행) |
| `/clear`·세션 재개·다음날 이어 작업 가능성 | 한 번에 끝나는 산출물(보고서 1개 생성) |
| 에이전트 4명 이상 + Phase 3개 이상 | 에이전트 1~2명, 단일 Phase |
| 코드베이스 마이그레이션·장기 리서치·다단계 빌드 | 단일 도메인의 짧은 변환·요약 |
| 사용자가 명시적으로 토큰 절감을 요구 | 짧은 작업에 인프라 비용을 들이는 것이 군더더기인 경우 |

**default는 "적용 안 함"**이다. 적용 시 사용자에게 1줄로 알린다 — "이 하네스는 `<프로젝트>/.harness/`에 작업 메모를 남기며, 세션을 넘어 컨텍스트를 보존합니다."

---

## 핵심 철학

harness의 본래 철학을 그대로 지킨다:

1. **에이전트의 독립성** — 각 에이전트는 자기 영역에서 자율적으로 일한다.
2. **팀 통신을 통한 협업** — `SendMessage`/`TaskCreate`로 서로 협력한다.
3. **토큰 효율** — 위 두 가지를 최소 토큰으로 달성한다.

Memo 패턴은 위 셋을 *깨지 않으면서* 세션 영속성만 추가한다. 라이터를 한 명으로 강제하면 독립성이 깨지고, 매번 전체 동기화하면 토큰 효율이 깨진다. 그래서 분산 슬롯 + 공유 헤더 구조를 쓴다.

---

## 구조

```
<프로젝트>/.harness/
├── status.md                  ← 공유 헤더 (팀 전체 목표 + 합의된 핵심 결정만)
├── agents/
│   ├── {agent-1}.md           ← agent-1만 쓰는 자기 영역 (독립)
│   ├── {agent-2}.md           ← agent-2만 쓰는 자기 영역 (독립)
│   └── ...
└── archive/                   ← 압축된 옛날 내용 (필요 시)
```

### 공유 헤더 (`status.md`) 스키마

```markdown
# Project Status (Last Updated: {ISO-8601 timestamp})

## Objective
{팀 전체가 합의한 한 줄 목표. Phase 1 종료 후 확정. 이후 변경은 사용자 승인 필요.}

## Phase Progress
- Phase 1: ✅ Done ({yyyy-mm-dd})
- Phase 2: 🔄 In Progress
- Phase 3: ⏳ Pending

## Team Decisions
- {yyyy-mm-dd HH:MM} {결정 요약} — by {author}
- {yyyy-mm-dd HH:MM} [ERROR] {요약} — by {author}

## Active Agents
- agent-1 → see `agents/agent-1.md`
- agent-2 → see `agents/agent-2.md`
```

**Decisions 섹션은 append-only**다. 잘못된 결정도 지우지 않고 새 entry로 정정한다. 다음 세션에서 학습 가능하도록.

### 에이전트 슬롯 (`agents/{agent}.md`) 스키마

```markdown
# {agent-name} (Last Updated: {timestamp})

## Current Task
{지금 하고 있는 일 한 줄}

## Accomplishments
- {yyyy-mm-dd} {완료 항목 요약} → 산출물: `_workspace/...`

## Decisions
- {yyyy-mm-dd HH:MM} {내가 내린 결정 + 한 줄 근거}

## Search Discoveries (선택, search-efficiency.md 참조)
- `path/to/file.ts:45` — 토큰 검증 진입점
- `lib/auth/*` — 인증 모듈 군집

## Issues
- {yyyy-mm-dd} {차단된 항목 + 어떤 도움이 필요한지}
```

---

## 쓰기/읽기 규칙

| 액션 | 누가 | 어디에 |
|------|------|--------|
| 공유 헤더(`status.md`) 갱신 | **오케스트레이터/리더만** | Objective, Phase Progress, Team Decisions |
| 자기 슬롯(`agents/{self}.md`) 갱신 | **본인만** | 자유롭게 |
| 다른 에이전트의 슬롯 읽기 | **누구나** | 협업 필요 시에만 (SendMessage 알림 받으면) |
| 공유 헤더 읽기 | **누구나** | 작업 시작 시 항상 |

이 규칙으로 **lockfile이 불필요**하다. 라이터 경합이 구조적으로 발생하지 않는다.

---

## 마일스톤 갱신 정책

매 도구 호출 후 갱신은 금지한다. 매번 갱신하면 오히려 토큰을 더 소모한다. 다음 시점에만 갱신한다:

| 시점 | 누가 | 어디에 무엇을 |
|------|------|------------|
| 작업 시작 | 본인 | 자기 슬롯의 `Current Task` 1줄 |
| Phase 완료 | 본인 | 자기 슬롯 `Accomplishments`에 append + 리더에게 SendMessage |
| 팀 합의/Phase 전환 | 리더 | 공유 헤더 `Phase Progress` + `Team Decisions` |
| 에러 발생 | 본인 | 자기 슬롯 `Issues` + 리더에게 SendMessage |
| 일반 Edit/Read/Bash | — | **갱신 안 함** |

---

## 역할 분리

이미 있는 메커니즘과 중복하지 않도록 역할을 명확히 분리한다.

| 메커니즘 | 무엇을 다루나 | Memo와의 관계 |
|---------|------------|--------------|
| **TaskCreate / TaskUpdate** | 진행 중인 작업의 상태(pending/in_progress/completed) | Memo는 *완료 후* 핵심 산출만 요약. 작업 목록 자체는 TaskCreate에 둠 |
| **SendMessage** | 실시간 협업·요청·알림 | Memo는 영속 결정만. 실시간 대화는 SendMessage |
| **`_workspace/{phase}_{agent}.md`** | 중간 산출물의 *원본* | Memo는 산출물의 *포인터*만. 원본은 _workspace에 |
| **`MEMORY.md` (auto memory)** | 사용자/feedback/project/reference 영구 메모리 | Memo는 *프로젝트별·세션별*. MEMORY는 *사용자 보편적*. 같은 정보가 둘 다 들어가지 않게 |
| **git log / 코드 자체** | 구현 결정·변경 이력의 진정한 원본 | Memo는 결정의 *요약*만. 원본은 코드+git |

**원칙:** Memo에는 "이미 다른 곳에 있는 정보의 *위치 포인터 + 한 줄 요약*"만 둔다. 디테일을 복사하지 않는다.

---

## 충돌 시 우선순위

Memo의 내용이 다른 정보원과 충돌하면 다음 순위를 따른다:

```
코드 자체 > git log > TaskCreate 상태 > _workspace/ 산출물 > .harness/status.md
```

Memo는 **요약·캐시**이지 원본이 아니다. 충돌 시 코드를 신뢰하고, Memo를 정정한다.

---

## 압축·폴딩 정책

각 슬롯이 200줄을 넘어가면 압축을 시작한다:

1. **자동**: 슬롯 본인이 작업 종료 시 자기 슬롯 길이를 확인하고, 200줄 초과 시 오래된 `Accomplishments`(상위 50%)를 한 줄 요약으로 폴딩한다.
2. **수동**: 사용자가 "status 정리해줘"라고 요청하면 리더가 모든 슬롯 + 헤더를 점검하고 폴딩한다.
3. **아카이브**: 폴딩 직전 원본은 `archive/{agent}-{yyyy-mm-dd}.md`로 이동.

폴딩된 슬롯에는 다음 섹션이 추가된다:

```markdown
## Archived Summary
{yyyy-mm-dd}까지 N개 항목을 다음 한 줄로 요약: {핵심 진척}.
원본은 `archive/{agent}-{yyyy-mm-dd}.md` 참조.
```

---

## 세션 재개 시나리오

`/clear` 또는 다음날 새 세션에서 작업을 이어가는 흐름:

1. 사용자가 "이전 작업 이어가자"라고 말한다.
2. 오케스트레이터(또는 메인 에이전트)는 가장 먼저 다음 두 파일을 Read한다:
   - `<프로젝트>/.harness/status.md` (공유 헤더)
   - 자신의 슬롯 `agents/{self}.md` (있으면)
3. `Phase Progress`에서 다음 Phase를 식별한다.
4. `Team Decisions`에서 이전 세션의 핵심 결정을 흡수한다.
5. 자기 슬롯의 `Current Task`로 자기가 어디까지 했는지 확인한다.
6. 다른 팀원이 필요하면 그 슬롯을 추가로 Read한다.

이 흐름이 동작하지 않으면 Memo 패턴이 실패한 것이다. 통합 테스트의 핵심 시나리오로 둔다.

---

## 적용 예시

**도메인:** 대규모 코드베이스(20만 줄)에서 단계적 코드 마이그레이션 (예: Express → Fastify)

**에이전트팀:**
- `migrate-orchestrator` (리더, 공유 헤더 라이터)
- `dependency-analyst`
- `route-rewriter`
- `test-updater`
- `regression-checker`

**`.harness/status.md` (공유 헤더, 발췌):**
```markdown
## Objective
Express 4 라우트 320개를 Fastify 4로 단계적 이전. 회귀 0건 유지.

## Phase Progress
- Phase 1 (의존성 매핑): ✅ Done
- Phase 2 (라우트 변환 1/3 batch): 🔄 In Progress
- Phase 3 (테스트 정합): ⏳ Pending
- Phase 4 (회귀 검증): ⏳ Pending

## Team Decisions
- 2026-04-30 14:21 Fastify의 errorHandler를 라우트별이 아닌 전역으로 등록 — by migrate-orchestrator
- 2026-04-30 15:02 [ERROR] mongoose 버전 6 미지원 plugin 발견 → 회피 PR로 전환 — by dependency-analyst
```

**`.harness/agents/route-rewriter.md` (발췌):**
```markdown
## Current Task
batch-2의 /api/users 라우트군 변환

## Accomplishments
- 2026-04-30 batch-1 완료 (45개 라우트) → `_workspace/02_route-rewriter_batch-1.md`

## Search Discoveries
- `src/middleware/auth.ts:120` — 모든 라우트 진입점 공통 미들웨어
- `src/routes/users/*.ts` — 22개 파일이 동일 패턴 사용

## Issues
- 2026-04-30 file upload 라우트는 fastify-multipart 필요. orchestrator에 알림 보냄.
```

**다음 세션 재개 흐름:**
- 다음날 사용자: "어제 마이그레이션 이어가자"
- orchestrator: status.md 읽기 → "Phase 2 batch-2부터 재개" 판단
- route-rewriter 호출 시: 자기 슬롯 읽기 → "/api/users 라우트군부터" 즉시 재개
- 에러 entry로 file upload 이슈 인식 → orchestrator가 fastify-multipart 도입 결정을 새 Decisions로 추가

---

## 안티패턴

다음은 **하지 말 것**:

| 안티패턴 | 왜 금지 |
|---------|--------|
| 매 Edit/Bash 후 status 갱신 | 토큰 효율 깨짐. 마일스톤만 |
| 한 사람이 모든 슬롯을 갱신 | 독립성 깨짐. 자기 영역만 |
| Decisions 항목 삭제 (잘못된 결정 포함) | 학습 정보 손실. 정정 entry 추가로 |
| 산출물 본문을 status에 복사 | 중복. `_workspace/` 포인터만 |
| TaskCreate를 status로 대체 | 진행 상태는 TaskCreate가 SSOT |
| status에 사용자 보편적 사실 기록 | MEMORY.md의 영역. status는 프로젝트별 |
| `.harness/`를 git에 commit하지 않음 | 다음날 다른 머신에서 잃음. 적어도 헤더는 commit 권장 |
| `.harness/`에 secrets/credentials 기록 | 로그 파일이 됨. 절대 금지 |

---

## 적용 체크리스트 (생성된 하네스)

Memo 패턴을 적용한 하네스가 갖춰야 하는 것:

- [ ] `<프로젝트>/.harness/status.md` 초기 헤더 생성
- [ ] `<프로젝트>/.harness/agents/` 디렉토리 + 각 팀원 슬롯 빈 파일
- [ ] 모든 에이전트 정의의 `## 작업 원칙`에 다음 4줄 추가:
  - 작업 시작 시 `.harness/status.md`와 자기 슬롯 Read
  - 마일스톤(Phase 완료, 결정, 에러)에만 자기 슬롯 갱신
  - 공유 헤더는 리더만 갱신
  - 다른 에이전트 슬롯 Read는 협업 필요 시만
- [ ] 오케스트레이터에 `update_shared_header` 호출 지점 3개 명시 (Phase 시작/완료/에러)
- [ ] 세션 재개 테스트 시나리오 1개 작성
- [ ] `.gitignore`에 `_workspace/`는 추가, `.harness/status.md`와 `.harness/agents/`는 commit 권장 (팀 공유 시)
