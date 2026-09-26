# 실전 팀 구성 예시

각 예시는 작업에 맞는 실행 모드를 고르는 기준과 Harness v2 문법의 기본 형태를 보여 준다. 모드별 정의는 `execution-modes.md`, 워크플로 스크립트 작성법은 `workflow-recipes.md`에서 확인한다.

---

## 예시 1: 종합 조사 팀 — 워크플로 조율

**구성:** 분산·통합(팬아웃/팬인) + 적대적 검증

**선택 이유:** 조사할 관점을 미리 나열할 수 있고, 주장마다 검증하는 절차를 코드로 정할 수 있다.

```
[메인] 사전 조사: 조사 관점 확정(공식 자료·언론·커뮤니티·배경)
     → Workflow(script, args: {axes, topic, ws})
         phase '조사': pipeline(axes, axis => agent(..., {schema: FINDINGS}))
         phase '검증': 주장별 적대적 검증 에이전트 실행 → 과반이 confirmed로 판정한 주장만 통과
         phase '종합': 누락 검토자 1명 실행 → 빠진 관점이 있으면 추가 조사
     → 메인이 반환된 구조화 결과로 종합 보고서 작성
```

조사 원칙과 구조화 출력 형식은 `.claude/agents/researcher.md`에, 반박을 우선하는 검증 원칙은 `.claude/agents/fact-checker.md`에 정의한다. 워크플로에서는 `agentType`으로 두 에이전트를 지정한다.

서로 충돌하는 정보는 한쪽을 임의로 버리지 않는다. 반환 스키마에 출처와 함께 담는다.

## 예시 2: SF 소설 집필 팀 — 지속형 에이전트 중심의 혼합 모드

**구성:** 파이프라인 + 생성·검증

**선택 이유:** 세계관, 인물, 줄거리가 서로 어긋나지 않도록 실시간으로 조정해야 하므로 각 전문가가 이전 대화 맥락을 기억해야 한다. 반면 검토자는 서로 독립된 관점으로 결과만 전달하면 되므로 서브에이전트로 충분하다.

```
1단계(지속형 에이전트): Agent(name: "worldbuilder") + Agent(name: "character-designer")
               + Agent(name: "plot-architect") 병렬 실행
               → TaskCreate(세계관·인물·줄거리, 서로의 의존 관계 명시)
               → 리더가 중계: worldbuilder가 사회 구조 확정
                 → SendMessage로 character-designer에 전달
                 → 인물의 직업군이 세계관과 충돌하면 SendMessage로
                   worldbuilder에 조정 요청
                 이전 맥락이 남아 있으므로 "아까 정한 계급 구조에서
                 상인 계층만 수정"처럼 일부만 고치라고 지시할 수 있다.
2단계(서브에이전트): prose-stylist 한 번 호출 → _workspace/에 저장된 산출물 세 개를 읽고 집필
3단계(서브에이전트 병렬): science-consultant + continuity-manager가 각각 검토
4단계(지속형 에이전트): 한 번만 호출한 prose-stylist에는 SendMessage를 보낼 수 없다.
                 2단계에서 name을 붙여 실행했다면 검토 결과를 반영하라고 지시할 수 있다.
                 수정이 반복될 것으로 보이면 처음부터 name을 붙인다.
```

수정 요청을 다시 보낼 가능성이 있는 에이전트에는 처음 실행할 때부터 `name`을 붙인다. 한 번만 호출한 에이전트는 이전 대화 맥락을 이어서 사용할 수 없다.

## 예시 3: 종합 코드 검토 — 워크플로 조율

**구성:** 분산·통합 + 적대적 검증

**선택 이유:** 보안·성능·구조·테스트처럼 검토 관점을 미리 정할 수 있고, 찾은 항목을 각각 다시 검증하는 절차도 코드로 표현할 수 있다.

```javascript
// 관점별 검토 → 찾은 항목마다 적대적 검증
// 전체 검토를 기다리지 않는다. 보안 검토가 끝나면 성능 검토가 진행 중이어도
// 보안 영역에서 찾은 문제를 바로 검증한다.
const FINDINGS = { type: 'object', required: ['findings'], properties: {
  findings: { type: 'array', items: { type: 'object',
    required: ['title', 'file', 'evidence'], properties: {
      title: { type: 'string' }, file: { type: 'string' }, evidence: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['status', 'reason'], properties: {
  status: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
  reason: { type: 'string' } } }
const results = await pipeline(
  [
    { key: 'security', prompt: '보안 관점에서 검토하라.' },
    { key: 'perf', prompt: '성능 관점에서 검토하라.' },
    { key: 'arch', prompt: '구조 관점에서 검토하라.' },
    { key: 'test', prompt: '테스트 관점에서 검토하라.' },
  ],
  d => agent(d.prompt, { phase: '검토', schema: FINDINGS }),
  r => parallel((r?.findings ?? []).map(f => () =>
    agent(`다음 발견을 검증하라. 근거가 충분하면 confirmed, 명백히 반박되면 refuted, 판단하기 어려우면 uncertain으로 판정하라: ${JSON.stringify(f)}`,
      { phase: '검증', schema: VERDICT })
      .then(verdict => ({ ...f, verdict }))))
)
const confirmed = results.flat().filter(Boolean)
  .filter(f => f.verdict?.status === 'confirmed')
```

v1에서는 검토자끼리 `SendMessage`로 발견을 공유하는 지속형 팀을 썼다. 위 예시처럼 발견한 항목 한 건만으로 검증할 수 있으면 해당 항목의 근거를 프롬프트에 충분히 담아 곧바로 검증한다. 다른 관점의 발견과 비교해야 한다면 전체 검토 결과를 모은 뒤 동기화 장벽을 두고 검증한다. 설계 방향을 두고 토론해야 하는 등 실시간 대화가 꼭 필요한 경우에만 지속형 에이전트를 쓴다.

## 예시 4: 대규모 코드 마이그레이션 — 지속형 감독자 협업 또는 워크플로 조율

**구성:** 미리 나눌 수 있으면 분산·통합, 진행 중 다시 나눠야 하면 감독자

**선택 기준:** 작업 묶음을 미리 나눌 수 있는지에 따라 실행 모드를 고른다.

작업 묶음을 미리 정할 수 있으면 워크플로를 쓴다.

```javascript
const MIGRATION_RESULT = { type: 'object', required: ['worktreePath', 'changedFiles'], properties: {
  worktreePath: { type: 'string', minLength: 1 },
  changedFiles: { type: 'array', minItems: 1, uniqueItems: true,
    items: { type: 'string', minLength: 1 } } } }
const MIGRATION_VERDICT = { type: 'object', required: ['status', 'reason'], properties: {
  status: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
  reason: { type: 'string' } } }
const migrated = await pipeline(args.batches,   // 사전 조사로 복잡도를 추정한 뒤 작업 묶음을 확정한다
  b => agent(`다음 작업 묶음을 마이그레이션하고, 격리 작업 트리의 절대 경로와 실제 변경 파일 목록을 반환하라: ${b.files.join(', ')}`,
    { agentType: 'migrator', isolation: 'worktree', schema: MIGRATION_RESULT }),
  (r, b) => r && agent(
    `격리 작업 트리 ${r.worktreePath}에서 마이그레이션 대상과 실제 변경 파일을 대조해 누락과 오류를 검증하라. 원래 대상: ${b.files.join(', ')}. 실제 변경: ${r.changedFiles.join(', ')}`,
    { agentType: 'qa-inspector', schema: MIGRATION_VERDICT })
    .then(verdict => ({ ...r, verdict })))
const confirmed = migrated.filter(Boolean)
  .filter(r => r.verdict?.status === 'confirmed')
return { confirmed }
```

적대적 검증 에이전트에는 마이그레이션 결과가 있는 격리 작업 트리 경로를 반드시 전달한다. 워크플로가 끝나면 메인 에이전트가 `confirmed` 결과의 `worktreePath`를 하나씩 확인해 변경을 기준 브랜치에 병합하거나 필요한 커밋만 선별 적용한다. 충돌이 생기면 다음 작업 트리를 합치기 전에 해결하고, 통합 테스트를 통과한 뒤에만 다음 변경을 적용한다. `refuted`나 `uncertain` 결과는 병합하지 않고 누락 사유를 보고한다.

진행 상황에 따라 작업을 다시 나눠야 하면 지속형 에이전트를 쓴다.

```
리더가 TaskCreate로 작업 묶음 등록(depends_on 포함)
→ Agent(name: "migrator-1"), Agent(name: "migrator-2"), Agent(name: "migrator-3") 병렬 실행
→ 완료 알림을 받을 때마다 결과 확인
→ 실패한 작업은 SendMessage로 원인을 확인한 뒤 TaskUpdate로 다시 배정
→ 모두 끝나면 통합 테스트
```

## 예시 5: 웹툰 제작 — 지속형 생성자와 단발 검토자

**구성:** 생성·검증

**선택 이유:** 생성자 한 명과 검토자 한 명만 필요하다. 검토 결과를 생성자에게 최대 두 번 돌려보내면 되므로 가벼운 혼합 모드로 충분하다.

```
1단계: Agent(name: "artist") → 패널 생성 → _workspace/panels/
2단계: Agent(subagent_type: "webtoon-reviewer", prompt: "패널을 검토하라") 한 번 호출 → PASS/FIX/REDO 판정
       → _workspace/review_report.md
3단계: REDO 판정을 받은 패널만 SendMessage({to: "artist"})로 재생성 지시
       최대 두 번 반복한다. artist가 이전 맥락을 기억하므로
       "3번 패널의 구도만 수정"처럼 범위를 좁혀 지시할 수 있다.
재시도 방침: 두 번 수정해도 통과하지 못하면 미해결 상태와 원인을 사용자에게 알린다.
             전체 패널의 50% 이상이 REDO이면 사용자에게 프롬프트 수정을 제안한다.
```

---

## 산출물 저장 방식

- **에이전트 정의:** `프로젝트/.claude/agents/{name}.md`에 만든다. 핵심 역할, 작업 원칙, 입력·출력 규칙, 재호출 방법, 오류 처리, 협업 방법을 반드시 적는다. 지속형 에이전트에는 통신 규칙을, 워크플로에서 쓸 에이전트에는 구조화 출력 형식을 추가한다.
- **스킬:** `프로젝트/.claude/skills/{name}/SKILL.md`에 만들고, 필요하면 `references/`와 `scripts/`를 둔다.
- **오케스트레이터:** 실행 모드를 반드시 적는다. `orchestrator-template.md`의 템플릿을 사용한다.
- **중간 산출물:** `_workspace/{phase}_{agent}_{artifact}.{ext}` 형식으로 저장하고 검증이 끝난 뒤에도 남긴다.
