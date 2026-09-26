# 스킬 테스트와 반복 개선 가이드

하네스로 만든 스킬의 품질을 검증하고 여러 차례 개선하는 방법을 설명한다. `SKILL.md` 6단계를 보충하는 참고 자료다.

---

## 목차

1. [테스트 방식 개요](#1-테스트-프레임워크-개요)
2. [테스트 프롬프트 작성법](#2-테스트-프롬프트-작성법)
3. [스킬 적용 실행(With-skill)과 기준 실행(Baseline) 비교](#3-실행-테스트-with-skill-vs-baseline)
4. [워크플로로 A/B 테스트 실행(v2)](#4-워크플로우-기반-ab-v2)
5. [검증 조건(assertion)으로 정량 평가](#5-정량적-평가-assertion-기반-채점)
6. [전문 에이전트 활용](#6-전문-에이전트-활용)
7. [반복 개선 절차](#7-반복-개선-루프)
8. [`description` 호출 조건 검증](#8-description-트리거-검증)
9. [테스트 작업 디렉터리 구조](#9-워크스페이스-구조)

---

<a id="1-테스트-프레임워크-개요"></a>

## 1. 테스트 방식 개요

스킬의 품질은 **사람이 산출물을 판단하는 정성 평가**와 **검증 조건으로 채점하는 정량 평가**를 함께 사용해 확인한다.

| 평가 방식 | 방법 | 알맞은 스킬 |
|----------|------|-----------|
| **정성 평가** | 사용자가 산출물을 직접 검토한다. | 문체, 디자인, 창작물처럼 품질 판단에 사람의 평가가 필요한 스킬 |
| **정량 평가** | 검증 조건에 따라 자동으로 채점한다. | 파일 생성, 데이터 추출, 코드 생성처럼 결과를 객관적으로 확인할 수 있는 스킬 |

**작성 → 테스트 실행 → 평가 → 개선 → 다시 테스트** 순서로 진행한다.

## 2. 테스트 프롬프트 작성법

### 작성 원칙

테스트 프롬프트는 **실제 사용자가 입력할 법한 구체적이고 자연스러운 문장**으로 작성한다. 추상적이거나 일부러 꾸민 프롬프트로는 실제 사용 상황에서 스킬이 잘 작동하는지 알기 어렵다.

**좋지 않은 예:** `"PDF를 처리하라"`, `"데이터를 추출하라"`

**좋은 예:**

```
"다운로드 폴더에 있는 'Q4_매출_최종_v2.xlsx'에서 C열(매출)과 D열(비용)을
사용해서 이익률(%) 열을 추가해 줘. 그리고 이익률을 기준으로 내림차순 정렬해 줘."
```

### 프롬프트를 다양하게 구성하는 방법

- 격식을 갖춘 말투와 편한 말투를 섞는다.
- 의도를 직접 밝힌 요청과 문맥에서 의도를 파악해야 하는 요청을 섞는다. 예를 들어 파일 형식을 직접 말하는 경우와 문맥으로 추론해야 하는 경우를 모두 넣는다.
- 간단한 작업과 복잡한 작업을 섞고, 일부 프롬프트에는 약어·오타·일상적인 표현을 넣는다.

### 사용 사례 포함 범위

프롬프트 두세 개로 시작한다. 핵심 사용 사례 한 가지와 예외 상황 한 가지를 반드시 넣고, 필요하면 여러 작업을 한 번에 요청하는 사례 한 가지를 더한다.

<a id="3-실행-테스트-with-skill-vs-baseline"></a>

## 3. 스킬 적용 실행(With-skill)과 기준 실행(Baseline) 비교

### 3-1. 두 실행을 비교하는 방법

테스트 프롬프트마다 서브에이전트 두 명을 한 메시지에서 **동시에 실행**한다.

- **스킬 적용 실행(With-skill)**: 스킬을 읽은 뒤 작업하고 결과를 `_workspace/iteration-N/eval-{id}/with_skill/outputs/`에 저장한다.
- **기준 실행(Baseline)**: 같은 프롬프트를 스킬 없이 처리하고 결과를 `_workspace/iteration-N/eval-{id}/without_skill/outputs/`에 저장한다.

### 3-2. 기준 실행을 정하는 방법

| 상황 | 기준 실행 |
|------|----------|
| 새 스킬을 만드는 경우 | 스킬 없이 같은 프롬프트를 실행한다. |
| 기존 스킬을 개선하는 경우 | 수정 전 스킬을 별도 사본으로 보존해 사용한다. |

### 3-3. 실행 시간과 토큰 사용량 기록

서브에이전트의 완료 알림이 오면 `total_tokens`와 `duration_ms`를 **곧바로** 저장한다. 두 값은 완료 알림을 받는 시점에만 확인할 수 있으며 나중에는 복구할 수 없다.

<a id="4-워크플로우-기반-ab-v2"></a>

## 4. 워크플로로 A/B 테스트 실행(v2)

테스트 사례가 세 건 이상이거나 여러 차례 반복해서 검증해야 한다면 A/B 테스트 자체를 워크플로 스크립트로 만든다. 사용자가 테스트 실행에 동의했을 때만 사용한다.

```javascript
export const meta = {
  name: 'skill-ab-test',
  description: '스킬 적용 실행과 기준 실행을 마친 뒤 익명으로 채점한다',
  phases: [{ title: '실행' }, { title: '채점' }],
}
const RUN_RESULT = { type: 'object', required: ['saved', 'files'], properties: {
  saved: { type: 'boolean' },
  files: { type: 'array', minItems: 2, items: { type: 'string', minLength: 1 } } } }
const SLOT_GRADE = { type: 'object', required: ['expectations', 'summary'], properties: {
  expectations: { type: 'array', items: { type: 'object',
    required: ['text', 'passed', 'evidence'], properties: {
      text: { type: 'string' }, passed: { type: 'boolean' }, evidence: { type: 'string' } } } },
  summary: { type: 'object', required: ['passed', 'failed', 'total', 'pass_rate'], properties: {
    passed: { type: 'integer' }, failed: { type: 'integer' }, total: { type: 'integer' },
    pass_rate: { type: 'number' } } } } }
const GRADE = { type: 'object', required: ['A', 'B', 'comparison'], properties: {
  A: SLOT_GRADE,
  B: SLOT_GRADE,
  comparison: { type: 'object', required: ['preferred', 'reason'], properties: {
    preferred: { type: 'string', enum: ['A', 'B', 'tie'] },
    reason: { type: 'string' } } } } }

const results = await pipeline(
  args.evals,   // [{id, prompt, assertions, skillPath, withSkillSlot: 'A' | 'B'}]
  e => {
    const withSkillSlot = e.withSkillSlot === 'B' ? 'B' : 'A'
    const baselineSlot = withSkillSlot === 'A' ? 'B' : 'A'
    return parallel([
      () => agent(
        `${e.prompt}\n\n먼저 ${e.skillPath}를 읽고 따르라. 산출물은 ${args.ws}/${e.id}/with_skill/outputs/에 저장하고, 같은 파일을 ${args.ws}/${e.id}/blind/${withSkillSlot}/outputs/에도 저장하라. 저장한 파일 경로를 모두 반환하라.`,
        { label: `적용:${e.id}`, phase: '실행', schema: RUN_RESULT }),
      () => agent(
        `${e.prompt}\n\n산출물은 ${args.ws}/${e.id}/without_skill/outputs/에 저장하고, 같은 파일을 ${args.ws}/${e.id}/blind/${baselineSlot}/outputs/에도 저장하라. 저장한 파일 경로를 모두 반환하라.`,
        { label: `기준:${e.id}`, phase: '실행', schema: RUN_RESULT }),
    ])
  },
  (runs, e) => {
    const completed = (runs ?? []).filter(Boolean)
    if (completed.length !== 2 || completed.some(r => !r.saved || r.files.length < 2)) {
      log(`${e.id}: 스킬 적용 실행과 기준 실행의 산출물이 모두 준비되지 않아 채점을 건너뜁니다.`)
      return null
    }
    return agent(
      `${args.ws}/${e.id}/blind/A/outputs/와 ${args.ws}/${e.id}/blind/B/outputs/의 산출물이 모두 있는지 먼저 확인하라. 두 경로 중 하나라도 비어 있으면 채점하지 말고 실패 이유를 보고하라. 두 산출물이 모두 있으면 A와 B를 각각 채점하고 더 나은 쪽을 A, B, tie 가운데 하나로 판정하라. 익명성을 지키기 위해 eval_metadata.json, with_skill/, without_skill/은 열지 마라. 검증 조건: ${JSON.stringify(e.assertions)}`,
      { label: `채점:${e.id}`, phase: '채점', schema: GRADE })
      .then(grade => {
        if (!grade) log(`${e.id}: 익명 채점 결과를 받지 못해 이 사례를 건너뜁니다.`)
        return grade
      })
  }
)
const mapped = results.map((grade, index) => {
  if (!grade) return null
  const e = args.evals[index]
  const withSkillSlot = e.withSkillSlot === 'B' ? 'B' : 'A'
  const baselineSlot = withSkillSlot === 'A' ? 'B' : 'A'
  return {
    evalId: e.id,
    withSkill: grade[withSkillSlot],
    baseline: grade[baselineSlot],
    comparison: {
      preferred: grade.comparison.preferred === 'tie'
        ? 'tie'
        : grade.comparison.preferred === withSkillSlot ? 'with_skill' : 'baseline',
      reason: grade.comparison.reason,
    },
  }
}).filter(Boolean)
return { results: mapped }
```

메인 에이전트는 테스트 사례마다 `withSkillSlot`을 A와 B로 번갈아 지정한다. 채점자는 중립적인 `blind/A/`와 `blind/B/` 경로만 읽으므로 어느 쪽에 스킬을 적용했는지 알 수 없다. 두 실행의 산출물이 모두 준비된 사례만 채점하며, 채점이 끝나면 메인 에이전트가 A/B 결과를 스킬 적용 실행과 기준 실행에 다시 대응시킨다. 대응시킨 결과는 각 실행 디렉터리의 `grading.json`에 저장한다. 테스트 사례 한 건이 끝나는 즉시 채점을 시작하므로 모든 사례가 끝날 때까지 기다릴 필요도 없다. 스킬을 수정한 뒤 `resumeFromRunId`로 다시 실행하면 변경되지 않은 사례는 캐시 결과를 사용해 건너뛴다.

<a id="5-정량적-평가-assertion-기반-채점"></a>

## 5. 검증 조건(assertion)으로 정량 평가

### 5-1. 검증 조건 작성법

**좋은 검증 조건**은 참과 거짓을 객관적으로 가릴 수 있고, 조건의 문구만 읽어도 무엇을 검사하는지 알 수 있으며, 스킬을 적용했을 때 개선되어야 하는 결과를 측정한다. 스킬을 쓰지 않아도 언제나 통과하는 조건(예: “출력이 존재한다”)이나 사람의 주관적 판단이 필요한 조건(예: “잘 작성되었다”)은 좋지 않다.

### 5-2. 코드로 검사할 수 있는 조건

코드로 확인할 수 있는 검증 조건은 스크립트로 작성한다. 눈으로 확인하는 것보다 빠르고 결과를 더 신뢰할 수 있으며, 반복 회차가 바뀌어도 같은 스크립트를 다시 쓸 수 있다.

### 5-3. 구분력이 없는 검증 조건에 주의한다

스킬 적용 실행과 기준 실행이 모두 100% 통과하는 검증 조건은 스킬을 사용했을 때 생기는 차이를 측정하지 못한다. 이런 조건을 발견하면 삭제하거나, 두 실행의 차이를 드러낼 만큼 까다로운 조건으로 바꾼다.

### 5-4. 채점 결과 스키마

`skill-writing-guide.md`에서 정한 `grading.json` 형식(`text`/`passed`/`evidence`와 `summary`)을 따른다.

## 6. 전문 에이전트 활용

| 역할 | 하는 일 | 사용할 시점 |
|------|--------|------------|
| **채점자(Grader)** | 각 검증 조건의 통과 여부와 근거를 기록하고, 산출물에 담긴 사실 주장을 교차 검증하며, 검증 조건 자체의 품질도 점검한다. | 반복 회차마다 |
| **익명 비교자(Comparator)** | 두 산출물의 스킬 적용 여부를 가리고 A/B 순서를 섞은 뒤 품질을 비교한다. | 새 버전이 실제로 더 나은지 엄밀하게 확인할 때 |
| **분석자(Analyzer)** | 구분력이 없는 검증 조건, 결과 편차가 큰 평가 사례, 시간과 토큰 사용량의 상충 관계 등 통계적 패턴을 분석한다. | 반복 결과가 세 차례 이상 쌓인 뒤 |

<a id="7-반복-개선-루프"></a>

## 7. 반복 개선 절차

### 7-1. 개선 원칙

1. **피드백을 일반화한다.** 테스트 사례 한 건에만 맞춰 수정하면 과적합이 생긴다. 다른 사례에도 적용할 수 있는 원칙으로 고친다.
2. **도움이 되지 않는 지시는 삭제한다.** 에이전트의 작업 기록을 읽고, 스킬 때문에 불필요한 작업을 하고 있다면 그 지시를 없앤다.
3. **이유를 설명한다.** 짧은 피드백이라도 왜 중요한지 파악한 뒤, 그 이유가 드러나도록 스킬을 고친다.
4. **반복 작업에 필요한 도구를 미리 넣는다.** 모든 테스트에서 같은 보조 스크립트를 새로 만든다면 해당 스크립트를 `scripts/`에 넣는다.

### 7-2. 반복 순서

```
1. 스킬을 수정한다.
2. 새 `iteration-{N+1}/` 디렉터리에서 모든 테스트 사례를 다시 실행한다.
3. 이전 반복 회차와 비교한 결과를 사용자에게 제시한다.
4. 피드백을 받아 다시 수정하고 같은 순서를 반복한다.
```

**종료 조건:** 사용자가 만족하거나, 반영할 피드백이 없거나, 더 이상 의미 있게 개선할 수 없을 때 종료한다.

### 7-3. 초안을 새 관점에서 다시 검토한다

스킬을 수정할 때는 먼저 초안을 만든다. 그런 다음 초안을 처음 읽는 검토자라고 생각하고 처음부터 다시 읽으며 고친다. 처음부터 완벽하게 쓰려고 하지 않는다.

<a id="8-description-트리거-검증"></a>

## 8. `description` 호출 조건 검증

### 8-1. 호출 여부를 평가할 요청 작성

평가 요청 20개를 만든다. 스킬이 실행되어야 하는 `should-trigger` 요청 10개와 실행되지 않아야 하는 `should-NOT-trigger` 요청 10개로 구성한다.

**평가 요청 작성 기준:**

- 실제 사용자가 입력할 법한 구체적이고 자연스러운 문장으로 쓴다.
- 파일 경로, 사용자의 상황, 열 이름, 회사명처럼 구체적인 정보를 넣는다.
- 답이 뻔한 사례보다 스킬 적용 여부를 판단하기 어려운 **경계 사례**에 집중한다.

**`should-trigger`:** 같은 의도를 여러 방식으로 표현한 요청, 파일 유형을 명시하지 않았지만 해당 스킬이 분명히 필요한 요청, 흔하지 않은 사용 사례, 다른 스킬과 겹치지만 이 스킬을 선택해야 하는 요청을 포함한다.

**`should-NOT-trigger`:** **표현은 비슷하지만 적용 대상이 아닌 경계 사례(near miss)가 중요하다.** 사용하는 단어는 비슷해도 다른 도구나 스킬이 더 알맞은 요청을 넣는다. 명백히 관련 없는 요청은 테스트할 가치가 없다.

### 8-2. 기존 스킬과 충돌하는지 확인

1. 기존 스킬의 `description`을 모두 수집한다.
2. 새 스킬의 `should-trigger` 요청이 기존 스킬을 잘못 실행하지 않는지 확인한다.
3. 충돌이 생기면 `description`에 적용 범위와 제외 조건을 더 분명하게 적는다.

### 8-3. 자동 최적화(선택 사항·고급 기능)

1. 평가 요청 20개를 학습용(Train) 60%와 시험용(Test) 40%로 나눈다.
2. 현재 `description`의 호출 정확도를 측정한다.
3. 실패한 사례를 분석해 `description`을 개선한다.
4. **시험용 데이터(Test set)**의 결과를 기준으로 성능이 가장 좋은 `description`을 고른다. 학습용 데이터의 결과를 기준으로 고르면 과적합이 생긴다.
5. 이 과정을 최대 다섯 차례 반복한다.

> 화면 없이 실행하는 헤드리스 방식(`claude -p`)을 자동화한 스크립트로 검사한다. 토큰을 많이 사용하므로 스킬이 충분히 안정된 뒤 마지막 단계에서 실행한다.

<a id="9-워크스페이스-구조"></a>

## 9. 테스트 작업 디렉터리 구조

```
_workspace/
├── iteration-1/
│   ├── eval-descriptive-name/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/    (outputs/ + timing.json + grading.json)
│   │   ├── without_skill/ (outputs/ + timing.json + grading.json)
│   │   └── blind/         (A/outputs/ + B/outputs/)
│   └── benchmark.json
├── iteration-2/
└── evals/evals.json
```

**보관 규칙:**

- `eval` 디렉터리에는 번호 대신 내용을 알 수 있는 이름을 붙인다(예: `eval-multi-page-table-extraction`).
- 반복 회차마다 독립된 디렉터리를 만들고, 이전 `iteration` 디렉터리를 덮어쓰지 않는다.
- 사후 검증과 변경 이력 추적에 필요하므로 `_workspace/`는 삭제하지 않는다.
