# 워크플로우 레시피 — 스크립트 스켈레톤과 함정

워크플로우 오케스트레이션 모드(모드 A)로 하네스를 생성할 때 오케스트레이터 스킬에 넣을 스크립트 패턴. 스크립트는 순수 JavaScript이며 `Workflow` 도구의 `script` 파라미터로 전달한다.

---

## 목차

1. [기본 골격](#1-기본-골격)
2. [레시피: 팬아웃 + 적대적 검증](#2-레시피-팬아웃--적대적-검증)
3. [레시피: 심판 패널](#3-레시피-심판-패널)
4. [레시피: Loop-until-dry](#4-레시피-loop-until-dry)
5. [레시피: 버짓 연동 루프](#5-레시피-버짓-연동-루프)
6. [레시피: 커스텀 에이전트 + 구조화 출력](#6-레시피-커스텀-에이전트--구조화-출력)
7. [함정 목록 (검증 체크리스트)](#7-함정-목록-검증-체크리스트)

---

## 1. 기본 골격

모든 스크립트는 `meta` 리터럴로 시작한다. phase() 호출과 meta.phases의 title은 정확히 일치시킨다.

```javascript
export const meta = {
  name: 'domain-task',
  description: '한 줄 설명 (권한 다이얼로그에 표시)',
  phases: [
    { title: '수집', detail: '관점별 병렬 조사' },
    { title: '검증', detail: '발견별 적대적 검증' },
  ],
}

phase('수집')
const raw = await pipeline(ITEMS, item =>
  agent(`...${item}...`, { label: `collect:${item}`, phase: '수집', schema: COLLECT_SCHEMA }))

phase('검증')
// ...

return { result }   // 최종 반환값이 메인에 전달된다
```

**원칙:**
- **`pipeline()`이 기본, `parallel()`은 배리어가 정말 필요할 때만.** 배리어가 정당한 유일한 경우: 다음 단계가 이전 단계 **전체** 결과를 교차 참조해야 할 때 (dedup, 전체 0건이면 조기 종료, "다른 발견과 비교" 프롬프트)
- 항목 목록(ITEMS)은 스크립트에 하드코딩하지 말고 가능하면 `args`로 주입 — 메인이 정찰로 확정한 목록을 전달한다
- 타임스탬프가 필요하면 `args.now`로 주입 (`Date.now()` 사용 불가)

## 2. 레시피: 팬아웃 + 적대적 검증

관점별 발견 → 발견별 검증. 배리어 없이 관점 하나가 끝나는 즉시 그 관점의 발견들이 검증에 들어간다.

```javascript
export const meta = {
  name: 'review-fanout-verify',
  description: '관점별 리뷰 후 발견별 적대적 검증',
  phases: [{ title: 'Review' }, { title: 'Verify' }],
}

const FINDINGS = { type: 'object', required: ['findings'], properties: {
  findings: { type: 'array', items: { type: 'object',
    required: ['title', 'file', 'evidence'], properties: {
      title: { type: 'string' }, file: { type: 'string' }, evidence: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['refuted', 'reason'], properties: {
  refuted: { type: 'boolean' }, reason: { type: 'string' } } }

const results = await pipeline(
  args.dimensions,   // 예: [{key:'security', prompt:'...'}, {key:'perf', prompt:'...'}]
  d => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review', schema: FINDINGS }),
  review => parallel((review?.findings ?? []).map(f => () =>
    agent(`다음 발견을 반박하라. 불확실하면 refuted=true로 기울여라: ${JSON.stringify(f)}`,
      { label: `verify:${f.file}`, phase: 'Verify', schema: VERDICT })
      .then(v => ({ ...f, verdict: v }))))
)
const confirmed = results.flat().filter(Boolean).filter(f => f.verdict && !f.verdict.refuted)
log(`검증 통과 ${confirmed.length}건 / 전체 ${results.flat().filter(Boolean).length}건`)
return { confirmed }
```

검증 강도를 높이려면 발견 1건당 반박자 3명을 스폰하고 2표 이상 생존 시 통과로 바꾼다. 반박자마다 서로 다른 렌즈(정확성/보안/재현성)를 주면 중복보다 많이 잡는다.

## 3. 레시피: 심판 패널

해공간이 넓은 설계 작업. N개 독립 시안 → 병렬 심사 → 종합.

```javascript
export const meta = {
  name: 'design-judge-panel',
  description: 'N개 독립 시안 생성 후 심판 패널 채점, 승자 기반 종합',
  phases: [{ title: '시안' }, { title: '심사' }, { title: '종합' }],
}

const ANGLES = ['MVP 우선', '리스크 우선', '사용자 경험 우선']

phase('시안')
const drafts = (await parallel(ANGLES.map(a => () =>
  agent(`${a} 관점으로 독립 시안 작성: ${args.brief}`, { label: `draft:${a}` }))))
  .filter(Boolean)

phase('심사')   // 배리어 정당: 심사는 모든 시안을 상호 비교해야 한다
const SCORE = { type: 'object', required: ['scores'], properties: {
  scores: { type: 'array', items: { type: 'object',
    required: ['index', 'score', 'strengths'], properties: {
      index: { type: 'integer' }, score: { type: 'number' }, strengths: { type: 'string' } } } } } }
const judged = (await parallel([0, 1, 2].map(j => () =>
  agent(`다음 ${drafts.length}개 시안을 채점하라:\n${drafts.map((d, i) => `[${i}] ${d}`).join('\n---\n')}`,
    { label: `judge:${j}`, schema: SCORE })))).filter(Boolean)

phase('종합')
const totals = drafts.map((_, i) =>
  judged.reduce((s, r) => s + (r.scores.find(x => x.index === i)?.score ?? 0), 0))
const winner = totals.indexOf(Math.max(...totals))
return await agent(
  `승자 시안을 기반으로, 차점자들의 강점을 접목해 최종안을 작성하라.\n승자:\n${drafts[winner]}\n심사평:\n${JSON.stringify(judged)}`)
```

## 4. 레시피: Loop-until-dry

크기를 모르는 발견 작업. K라운드 연속 신규 0건까지 반복.

```javascript
const seen = new Set(), confirmed = []
let dry = 0
while (dry < 2) {
  const found = (await parallel(FINDERS.map(f => () =>
    agent(f.prompt, { phase: 'Find', schema: FINDINGS })))).filter(Boolean).flatMap(r => r.findings)
  const fresh = found.filter(b => !seen.has(key(b)))   // dedup은 seen 기준 — confirmed 기준이 아니다!
  if (!fresh.length) { dry++; continue }
  dry = 0
  fresh.forEach(b => seen.add(key(b)))
  const judged = await parallel(fresh.map(b => () =>
    agent(`반박 시도: ${b.title}`, { phase: 'Verify', schema: VERDICT })
      .then(v => ({ b, ok: v && !v.refuted }))))
  confirmed.push(...judged.filter(Boolean).filter(x => x.ok).map(x => x.b))
  log(`누적 확정 ${confirmed.length}건, 이번 라운드 신규 ${fresh.length}건`)
}
return { confirmed }
```

`seen`이 아니라 `confirmed` 기준으로 dedup하면, 심판에게 기각된 발견이 라운드마다 재등장하여 영원히 수렴하지 않는다.

## 5. 레시피: 버짓 연동 루프

사용자가 "+500k" 같은 토큰 목표를 준 세션에서 깊이를 자동 조절한다. `budget.total`이 없으면(무제한) `remaining()`은 Infinity이므로 반드시 `budget.total`을 가드한다.

```javascript
const findings = []
while (budget.total && budget.remaining() > 50_000) {
  const r = await agent('다음 탐색 라운드 수행...', { schema: FINDINGS })
  if (r) findings.push(...r.findings)
  log(`${findings.length}건 발견, 잔여 버짓 ${Math.round(budget.remaining() / 1000)}k`)
}
// 정적 규모 조절 변형: const FLEET = budget.total ? Math.floor(budget.total / 100_000) : 3
```

## 6. 레시피: 커스텀 에이전트 + 구조화 출력

하네스가 생성한 `.claude/agents/{name}.md` 정의를 워크플로우에서 그대로 사용한다.

```javascript
const r = await agent(
  `_workspace/02_draft.md를 검증하고 발견을 반환하라`,
  { agentType: 'qa-inspector',      // .claude/agents/qa-inspector.md
    schema: FINDINGS,               // 커스텀 에이전트에도 스키마 강제 가능
    effort: 'high' })               // 검증 단계는 추론 강도를 올릴 가치가 있다
```

- `agentType` 생략 시 기본 워크플로우 서브에이전트
- `model`은 단계별 업무 특성으로 선택 — 기계적 수집·변환 단계는 `sonnet`, 심층 검증·심판·설계 및 종합 계획·장기 실행 단계는 `opus` (상세: `model-selection-guide.md`)
- 병렬 파일 수정 에이전트에는 `isolation: 'worktree'` — 셋업 비용이 있으므로 정말 충돌하는 경우에만

## 7. 함정 목록 (검증 체크리스트)

하네스 Phase 6-2에서 워크플로우 스크립트를 검증할 때 이 목록을 확인한다.

| 함정 | 증상 | 예방 |
|------|------|------|
| `meta`에 변수/연산 사용 | 스크립트 파싱 실패 | meta는 순수 리터럴만 |
| TypeScript 문법 (`: string[]` 등) | 파싱 실패 | 순수 JavaScript로 작성 |
| `Date.now()` / `Math.random()` / `new Date()` | 런타임 에러 (resume 보호) | 타임스탬프·시드는 `args`로 주입, 무작위성은 인덱스로 프롬프트 변형 |
| `.filter(Boolean)` 누락 | 실패 에이전트의 `null`이 후속 단계에서 크래시 | parallel/pipeline 결과 소비 전 필터 |
| 불필요한 배리어 | 빠른 에이전트가 느린 에이전트를 대기 — 벽시계 낭비 | 교차 참조가 없으면 pipeline으로 재작성 |
| phase 제목 불일치 | 진행 표시 그룹핑 깨짐 | phase() 호출과 meta.phases의 title 일치 |
| 병렬 스테이지 내 전역 phase() 호출 | 진행 그룹 경합 | 스테이지 내부에서는 `opts.phase`로 명시 지정 |
| dedup을 confirmed 기준으로 | 기각 발견이 재등장, 루프 미수렴 | `seen` Set 기준 dedup |
| 버짓 루프에 `budget.total` 가드 누락 | 무제한 세션에서 에이전트 총량 캡까지 폭주 | `while (budget.total && ...)` |
| 커버리지 침묵 절단 | top-N만 처리하고 "전부 완료"로 보고 | 드랍 수를 `log()`로 명시 |
| 결과 진단 시 journal 미확인 | 캐시된 빈 결과를 성공으로 오독 | 완료 워크플로우 진단 전 transcript 디렉토리의 journal 확인 |
| 스크립트를 파일로 먼저 Write | 불필요한 우회 | `script` 인라인 전달 — 호출 시 자동으로 파일 보존되며, 반복 수정은 그 보존 파일을 Edit 후 `scriptPath`로 재호출 |
