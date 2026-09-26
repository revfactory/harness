# 워크플로 활용 예시 — 스크립트 기본 틀과 주의할 점

하네스를 워크플로 조율 모드(모드 A)로 만들 때 조율 스킬에 넣을 수 있는 스크립트 패턴을 설명한다. 스크립트는 순수 JavaScript로 작성하며 `Workflow` 도구의 `script` 매개변수로 전달한다.

---

## 목차

1. [기본 틀](#1-기본-틀)
2. [분산 실행(팬아웃) + 적대적 검증](#2-분산-실행팬아웃--적대적-검증)
3. [심사위원단](#3-심사위원단)
4. [새 항목이 없을 때까지 반복(Loop-until-dry)](#4-새-항목이-없을-때까지-반복loop-until-dry)
5. [토큰 예산 연동 반복](#5-토큰-예산-연동-반복)
6. [사용자 정의 유형 + 구조화 출력](#6-사용자-정의-유형--구조화-출력)
7. [주의할 점(검증 목록)](#7-주의할-점검증-목록)

---

## 1. 기본 틀

실행 가능한 전체 스크립트는 `meta` 리터럴로 시작한다. `phase()` 호출에 쓴 제목은 `meta.phases`의 `title`과 정확히 일치해야 한다.

```javascript
export const meta = {
  name: 'domain-task',
  description: '한 줄 설명(권한 대화 상자에 표시)',
  phases: [
    { title: '수집', detail: '관점마다 병렬로 조사한다' },
    { title: '검증', detail: '발견한 항목마다 반박할 근거를 찾아 검증한다' },
  ],
}

phase('수집')
const raw = await pipeline(args.items, item =>
  agent(`...${item}...`, { label: `수집:${item}`, phase: '수집', schema: COLLECT_SCHEMA }))

phase('검증')
// ...

return { result }   // 최종 반환값이 메인 에이전트에 전달된다
```

**원칙:**
- **기본적으로 `pipeline()`을 쓰고, 동기화 장벽이 꼭 필요할 때만 `parallel()`을 쓴다.** 다음 단계에서 이전 단계의 결과 **전체**를 서로 비교해야 할 때만 동기화 장벽이 필요하다. 중복 제거, 전체 결과가 0건일 때의 조기 종료, "다른 발견과 비교"하라는 프롬프트가 이에 해당한다.
- 항목 목록의 값을 스크립트에 직접 적지 않는다. 가능하면 메인 에이전트가 사전 조사로 확정한 목록을 `args.items`로 전달한다.
- 타임스탬프가 필요하면 `args.now`로 전달한다. `Date.now()`는 사용할 수 없다.

## 2. 분산 실행(팬아웃) + 적대적 검증

각 관점에서 검토 결과를 수집한 뒤, 결과를 하나씩 검증한다. 다른 관점의 조사가 끝날 때까지 기다리지 않고, 한 관점의 조사가 끝나는 즉시 해당 관점에서 나온 결과를 검증한다.

```javascript
export const meta = {
  name: 'review-fanout-verify',
  description: '관점마다 검토한 뒤 발견한 항목마다 반박할 근거를 찾아 검증한다',
  phases: [{ title: '검토' }, { title: '검증' }],
}

const FINDINGS = { type: 'object', required: ['findings'], properties: {
  findings: { type: 'array', items: { type: 'object',
    required: ['title', 'file', 'evidence'], properties: {
      title: { type: 'string' }, file: { type: 'string' }, evidence: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['status', 'reason'], properties: {
  status: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
  reason: { type: 'string' } } }

const results = await pipeline(
  args.dimensions,   // 예: [{key:'security', prompt:'...'}, {key:'perf', prompt:'...'}]
  d => agent(d.prompt, { label: `검토:${d.key}`, phase: '검토', schema: FINDINGS }),
  review => parallel((review?.findings ?? []).map(f => () =>
    agent(`다음 검토 결과를 검증하라. 근거가 충분하면 confirmed, 명백히 반박되면 refuted, 판단하기 어려우면 uncertain으로 판정하라: ${JSON.stringify(f)}`,
      { label: `검증:${f.file}`, phase: '검증', schema: VERDICT })
      .then(v => ({ ...f, verdict: v }))))
)
const confirmed = results.flat().filter(Boolean)
  .filter(f => f.verdict?.status === 'confirmed')
log(`전체 ${results.flat().filter(Boolean).length}건 중 ${confirmed.length}건이 검증을 통과했습니다.`)
return { confirmed }
```

검증을 더 엄격하게 하려면 발견한 항목 한 건마다 적대적 검증 에이전트 세 명을 실행한다. 이 가운데 두 명 이상이 근거가 충분하다고 `confirmed`로 판정한 항목만 통과시킨다. 각 에이전트에 정확성, 보안, 재현성처럼 서로 다른 검증 기준을 주면 같은 기준으로 반복해서 검사할 때보다 더 다양한 문제를 찾을 수 있다.

## 3. 심사위원단

가능한 해법이 많은 설계 작업에 쓰는 패턴이다. 서로 독립적인 시안 N개를 만든 뒤 병렬로 심사하고, 심사 결과를 바탕으로 최종안을 만든다.

```javascript
export const meta = {
  name: 'design-judge-panel',
  description: '독립 시안 N개를 만든 뒤 심사하고 최고점 시안을 바탕으로 최종안을 작성한다',
  phases: [{ title: '시안' }, { title: '심사' }, { title: '종합' }],
}

const angles = args.angles?.length
  ? args.angles
  : ['MVP를 우선하는', '위험 관리를 우선하는', '사용자 경험을 우선하는']
const judgeCount = args.judgeCount ?? 3

phase('시안')
const drafts = (await parallel(angles.map(a => () =>
  agent(`${a} 관점에서 독립적으로 시안을 작성하라: ${args.brief}`,
    { label: `시안:${a}`, phase: '시안' }))))
  .filter(Boolean)
log(`시안 ${angles.length}개 중 ${drafts.length}개를 만들었습니다.`)
if (!drafts.length) return { error: '완성된 시안이 없습니다.', drafts: [] }

phase('심사')   // 동기화 장벽 필요: 모든 시안을 서로 비교해야 한다
const SCORE = { type: 'object', required: ['scores'], properties: {
  scores: { type: 'array', items: { type: 'object',
    required: ['index', 'score', 'strengths'], properties: {
      index: { type: 'integer' }, score: { type: 'number' }, strengths: { type: 'string' } } } } } }
const judged = (await parallel(Array.from({ length: judgeCount }, (_, j) => () =>
  agent(`다음 ${drafts.length}개 시안을 채점하라:\n${drafts.map((d, i) => `[${i}] ${d}`).join('\n---\n')}`,
    { label: `심사:${j}`, phase: '심사', schema: SCORE })))).filter(Boolean)
log(`심사위원 ${judgeCount}명 중 ${judged.length}명의 결과를 받았습니다.`)
if (!judged.length) return { error: '완료된 심사 결과가 없습니다.', drafts }

phase('종합')
const ranked = drafts.map((_, i) => {
  const scores = judged.flatMap(r =>
    r.scores.filter(x => x.index === i).map(x => x.score)).filter(Number.isFinite)
  return scores.length
    ? { index: i, average: scores.reduce((sum, score) => sum + score, 0) / scores.length }
    : null
}).filter(Boolean)
if (!ranked.length) return { error: '유효한 시안별 점수가 없습니다.', drafts, judged }
const winner = ranked.reduce((best, item) =>
  item.average > best.average ? item : best).index
const finalDraft = await agent(
  `가장 높은 점수를 받은 시안을 바탕으로 최종안을 작성하라. 다른 시안의 장점도 필요한 부분에 반영하라.\n최고점 시안:\n${drafts[winner]}\n심사평:\n${JSON.stringify(judged)}`,
  { phase: '종합' })
if (!finalDraft) {
  log('최종안을 작성하지 못했습니다.')
  return { error: '최종안을 작성하지 못했습니다.', drafts, judged, winner }
}
return finalDraft
```

## 4. 새 항목이 없을 때까지 반복(Loop-until-dry)

찾아야 할 항목이 몇 개인지 미리 알 수 없는 작업에 쓴다. 새로운 항목이 K회 연속으로 나오지 않을 때까지 탐색을 반복한다.

4~6절의 코드는 1절의 기본 틀에 넣는 코드 조각이다. 전체 스크립트로 사용할 때는 맨 앞에 `meta`를 두고, 사용하는 단계 제목과 스키마를 함께 정의한다.

```javascript
const finders = args.finders ?? []
const dryLimit = args.dryRuns ?? 2
const findingKey = finding => JSON.stringify([
  finding.file ?? '', finding.title ?? '', finding.evidence ?? ''
])
const seen = new Set(), confirmed = []
if (!finders.length) return { confirmed, error: '탐색 기준이 없습니다.' }
let dry = 0
while (dry < dryLimit) {
  const found = (await parallel(finders.map(f => () =>
    agent(f.prompt, { phase: '탐색', schema: FINDINGS })))).filter(Boolean).flatMap(r => r.findings)
  const fresh = found.filter(b => !seen.has(findingKey(b)))   // 중복 여부는 seen을 기준으로 판단한다. confirmed를 기준으로 삼으면 안 된다.
  if (!fresh.length) { dry++; continue }
  dry = 0
  fresh.forEach(b => seen.add(findingKey(b)))
  const judged = await parallel(fresh.map(b => () =>
    agent(`다음 검토 결과를 검증하라. 근거가 충분하면 confirmed, 명백히 반박되면 refuted, 판단하기 어려우면 uncertain으로 판정하라: ${JSON.stringify(b)}`,
      { phase: '검증', schema: VERDICT })
      .then(v => ({ b, ok: v?.status === 'confirmed' }))))
  confirmed.push(...judged.filter(Boolean).filter(x => x.ok).map(x => x.b))
  log(`확정된 항목은 지금까지 ${confirmed.length}건이며, 이번 반복에서 ${fresh.length}건을 새로 찾았습니다.`)
}
return { confirmed }
```

`confirmed`를 기준으로 중복을 제거하면 검증에서 기각된 항목이 매회 다시 나타나므로 반복이 끝나지 않는다. 이미 한 번이라도 발견한 항목을 담는 `seen`을 기준으로 중복을 제거해야 한다.

## 5. 토큰 예산 연동 반복

사용자가 "+500k"처럼 토큰 예산을 지정한 세션에서는 남은 예산에 따라 탐색 범위를 자동으로 조절할 수 있다. `budget.total`이 없는 무제한 세션에서는 `remaining()`이 `Infinity`를 반환하므로, 조건문에서 반드시 `budget.total`이 있는지 먼저 확인한다.

```javascript
const findings = []
while (budget.total && budget.remaining() > 50_000) {
  const r = await agent('다음 탐색 작업을 진행하라.', { schema: FINDINGS })
  if (r) findings.push(...r.findings)
  log(`지금까지 ${findings.length}건을 찾았고, 남은 토큰 예산은 ${Math.round(budget.remaining() / 1000)}k입니다.`)
}
// 작업 규모를 미리 정하는 방식: const FLEET = budget.total ? Math.floor(budget.total / 100_000) : 3
```

## 6. 사용자 정의 유형 + 구조화 출력

하네스가 만든 `.claude/agents/{name}.md` 정의를 워크플로에서 그대로 사용한다.

```javascript
const r = await agent(
  `_workspace/02_draft.md 파일을 검증하고 발견한 항목을 반환하라`,
  { agentType: 'qa-inspector',      // .claude/agents/qa-inspector.md
    schema: FINDINGS,               // 사용자 정의 유형도 지정한 스키마에 맞는 결과만 반환
    effort: 'high' })               // 검증 단계에서는 추론 강도를 높이는 것이 좋다
```

- `agentType`을 생략하면 기본 워크플로 서브에이전트를 사용한다.
- `model`은 각 단계의 업무 특성에 따라 고른다. 반복적인 수집·변환 단계에는 `sonnet`, 깊이 있는 검증·심사·설계 단계에는 `opus`, 전체 계획·장기 실행 단계에는 `fable`을 쓴다. 자세한 기준은 `model-selection-guide.md`를 참고한다.
- 여러 에이전트가 파일을 동시에 수정해 충돌할 수 있다면 `isolation: 'worktree'`를 지정한다. 작업 환경을 준비하는 데 비용이 드므로 실제로 충돌할 가능성이 있을 때만 쓴다.

## 7. 주의할 점(검증 목록)

하네스의 6-2단계에서 워크플로 스크립트를 검증할 때 아래 목록을 확인한다.

| 주의할 점 | 나타나는 문제 | 예방법 |
|------|------|------|
| `meta`에 변수나 연산 사용 | 스크립트를 파싱할 수 없다. | `meta`에는 리터럴만 넣는다. |
| TypeScript 문법 사용(`: string[]` 등) | 스크립트를 파싱할 수 없다. | 순수 JavaScript로 작성한다. |
| `Date.now()` / `Math.random()` / `new Date()` 사용 | 실행 재개 보호 기능 때문에 오류가 발생한다. | 타임스탬프와 시드는 `args`로 전달하고, 무작위성이 필요하면 인덱스에 따라 프롬프트를 다르게 작성한다. |
| `.filter(Boolean)` 누락 | 실패한 에이전트가 반환한 `null` 때문에 다음 단계가 중단된다. | `parallel()`이나 `pipeline()`의 결과를 사용하기 전에 `.filter(Boolean)`을 적용한다. |
| 불필요한 동기화 장벽 | 빨리 끝난 에이전트가 느린 에이전트를 기다리므로 전체 실행 시간이 늘어난다. | 결과 전체를 서로 비교할 필요가 없다면 `pipeline()`으로 다시 작성한다. |
| `phase` 제목 불일치 | 진행 상황이 의도한 묶음으로 표시되지 않는다. | `phase()` 호출과 `meta.phases`의 `title`을 일치시킨다. |
| 병렬 단계 안에서 전역 `phase()` 호출 | 진행 상황을 표시할 묶음이 서로 충돌한다. | 단계 안에서는 `opts.phase`를 명시적으로 지정한다. |
| `confirmed`를 기준으로 중복 제거 | 기각된 항목이 다시 나타나 반복이 끝나지 않는다. | `seen` 집합을 기준으로 중복을 제거한다. |
| 토큰 예산 반복에 `budget.total` 확인 누락 | 무제한 세션에서 `agent()` 호출 횟수가 워크플로당 상한에 이를 때까지 계속 실행된다. | `while (budget.total && ...)` 조건을 사용한다. |
| 처리 범위를 알리지 않고 일부만 처리 | 상위 N개만 처리하고도 "전부 완료"했다고 보고한다. | 처리하지 않은 항목 수를 `log()`에 명시한다. |
| 결과를 진단할 때 실행 기록(`journal`) 미확인 | 캐시에서 가져온 빈 결과를 성공으로 잘못 판단한다. | 완료된 워크플로를 진단하기 전에 실행 내역(`transcript`) 디렉터리의 `journal`을 확인한다. |
| 스크립트를 먼저 파일로 작성 | 필요 없는 단계를 거치게 된다. | 스크립트 내용을 `script`에 직접 전달한다. 호출할 때 파일이 자동으로 보존되며, 반복해서 수정할 때는 보존된 파일을 `Edit`한 뒤 `scriptPath`로 다시 호출한다. |
