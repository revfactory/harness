# 스킬 테스트 & 반복 개선 가이드

하네스에서 생성한 스킬의 품질을 검증하고 반복적으로 개선하는 방법론. SKILL.md Phase 6의 보충 레퍼런스.

---

## 목차

1. [테스트 프레임워크 개요](#1-테스트-프레임워크-개요)
2. [테스트 프롬프트 작성법](#2-테스트-프롬프트-작성법)
3. [실행 테스트: With-skill vs Baseline](#3-실행-테스트-with-skill-vs-baseline)
4. [워크플로우 기반 A/B (v2)](#4-워크플로우-기반-ab-v2)
5. [정량적 평가: Assertion 기반 채점](#5-정량적-평가-assertion-기반-채점)
6. [전문 에이전트 활용](#6-전문-에이전트-활용)
7. [반복 개선 루프](#7-반복-개선-루프)
8. [Description 트리거 검증](#8-description-트리거-검증)
9. [워크스페이스 구조](#9-워크스페이스-구조)

---

## 1. 테스트 프레임워크 개요

스킬 품질 검증은 **정성적 평가**와 **정량적 평가**의 조합이다.

| 평가 유형 | 방법 | 적합한 스킬 |
|----------|------|-----------|
| **정성적** | 사용자가 산출물을 직접 리뷰 | 문체, 디자인, 창작물 등 주관적 품질 |
| **정량적** | assertion 기반 자동 채점 | 파일 생성, 데이터 추출, 코드 생성 등 객관적 검증 가능 |

핵심 루프: **작성 → 테스트 실행 → 평가 → 개선 → 재테스트**

## 2. 테스트 프롬프트 작성법

### 원칙

테스트 프롬프트는 **실제 사용자가 입력할 법한 구체적이고 자연스러운 문장**이어야 한다. 추상적이거나 인공적인 프롬프트는 테스트 가치가 낮다.

**나쁜 예:** `"PDF를 처리하라"`, `"데이터를 추출하라"`

**좋은 예:**
```
"다운로드 폴더에 있는 'Q4_매출_최종_v2.xlsx'에서 C열(매출)과 D열(비용)을
사용해서 이익률(%) 열을 추가해줘. 그리고 이익률 기준으로 내림차순 정렬."
```

### 프롬프트 다양성

- **공식적 / 캐주얼** 톤 혼합
- **명시적 / 암시적** 의도 혼합 (파일 형식을 직접 말하는 경우 vs 맥락으로 추론해야 하는 경우)
- **단순 / 복잡** 작업 혼합, 일부는 약어·오타·캐주얼 표현 포함

### 커버리지

2~3개 프롬프트로 시작하되: 핵심 사용 사례 1개 + 엣지 케이스 1개 + (선택) 복합 작업 1개.

## 3. 실행 테스트: With-skill vs Baseline

### 3-1. 비교 실행 구조

각 테스트 프롬프트에 대해 두 개의 서브에이전트를 **동시에**(단일 메시지에서 병렬) 스폰한다:

- **With-skill**: 스킬을 읽고 작업 수행 → `_workspace/iteration-N/eval-{id}/with_skill/outputs/`
- **Baseline**: 같은 프롬프트를 스킬 없이 수행 → `_workspace/iteration-N/eval-{id}/without_skill/outputs/`

### 3-2. Baseline 선택

| 상황 | Baseline |
|------|----------|
| 새 스킬 생성 | 스킬 없이 같은 프롬프트 실행 |
| 기존 스킬 개선 | 수정 전 스킬 버전 (스냅샷 보존) |

### 3-3. 타이밍 데이터 캡처

서브에이전트 완료 알림에서 `total_tokens`와 `duration_ms`를 **즉시** 저장한다. 이 데이터는 알림 시점에만 접근 가능하고 이후 복구할 수 없다.

## 4. 워크플로우 기반 A/B (v2)

테스트 케이스가 3개 이상이거나 반복(iteration) 검증이 잦으면, A/B 자체를 워크플로우 스크립트로 구성한다. 사용자가 테스트 실행에 동의한 경우에 사용한다.

```javascript
export const meta = {
  name: 'skill-ab-test',
  description: '스킬 유무 A/B 실행 + 블라인드 채점',
  phases: [{ title: 'Run' }, { title: 'Grade' }],
}
const GRADE = { type: 'object', required: ['expectations'], properties: {
  expectations: { type: 'array', items: { type: 'object',
    required: ['text', 'passed', 'evidence'], properties: {
      text: { type: 'string' }, passed: { type: 'boolean' }, evidence: { type: 'string' } } } } } }

const results = await pipeline(
  args.evals,   // [{id, prompt, assertions, skillPath}]
  e => parallel([
    () => agent(`${e.prompt}\n\n먼저 ${e.skillPath}를 읽고 따르라. 산출물은 ${args.ws}/${e.id}/with/에 저장.`,
      { label: `with:${e.id}`, phase: 'Run' }),
    () => agent(`${e.prompt}\n\n산출물은 ${args.ws}/${e.id}/without/에 저장.`,
      { label: `base:${e.id}`, phase: 'Run' }),
  ]),
  (runs, e) => agent(
    `${args.ws}/${e.id}/의 with/, without/ 산출물을 A/B 익명 순서로 각각 채점하라. assertions: ${JSON.stringify(e.assertions)}`,
    { label: `grade:${e.id}`, phase: 'Grade', schema: GRADE })
)
return { results: results.filter(Boolean) }
```

장점: 케이스별로 실행 완료 즉시 채점이 시작되고(배리어 없음), 채점이 스키마로 강제되며, 스킬 수정 후 `resumeFromRunId`로 재실행하면 변경 없는 케이스는 캐시로 건너뛴다.

## 5. 정량적 평가: Assertion 기반 채점

### 5-1. Assertion 작성

**좋은 assertion:** 객관적으로 참/거짓 판별 가능, 서술적 이름, 스킬의 핵심 가치를 검증
**나쁜 assertion:** 스킬 유무와 무관하게 항상 통과 (예: "출력이 존재한다"), 주관적 판단 필요 (예: "잘 작성되었다")

### 5-2. 프로그래밍 가능한 검증

assertion이 코드로 검증 가능하면 스크립트로 작성한다. 눈으로 확인하는 것보다 빠르고 신뢰성 있으며, iteration마다 재사용 가능.

### 5-3. Non-discriminating assertion 주의

"두 구성 모두에서 100% 통과"하는 assertion은 스킬의 차별적 가치를 측정하지 못한다. 발견하면 제거하거나 더 도전적인 assertion으로 교체한다.

### 5-4. 채점 결과 스키마

`skill-writing-guide.md`의 grading.json 표준(`text`/`passed`/`evidence` + summary)을 따른다.

## 6. 전문 에이전트 활용

| 역할 | 하는 일 | 활용 시점 |
|------|--------|----------|
| **Grader (채점자)** | assertion별 판정 + 근거 제시, 산출물의 사실 주장 교차 검증, eval 자체 품질 피드백 | 매 iteration |
| **Comparator (블라인드 비교자)** | 두 산출물을 A/B 익명화하여 스킬 사용 여부를 모른 채 품질 판정 | "새 버전이 정말 더 나은가"를 엄밀히 확인할 때 |
| **Analyzer (분석자)** | non-discriminating assertion, 고분산 eval, 시간/토큰 트레이드오프 등 통계 패턴 분석 | 3 iteration 이상 축적 후 |

## 7. 반복 개선 루프

### 7-1. 개선 원칙

1. **피드백을 일반화하라** — 테스트 예시에만 맞는 좁은 수정은 오버피팅이다. 원리 수준에서 수정한다.
2. **무게를 벌지 않는 것은 제거하라** — 트랜스크립트를 읽고, 스킬이 에이전트에게 비생산적인 작업을 시키고 있다면 삭제한다.
3. **Why를 설명하라** — 피드백이 간결하더라도 왜 중요한지 이해하고 그 이해를 스킬에 반영한다.
4. **반복 작업은 번들링하라** — 모든 테스트에서 동일한 헬퍼 스크립트가 생성되면 `scripts/`에 포함한다.

### 7-2. 반복 절차

```
1. 스킬 수정
2. 새 iteration-N+1/ 디렉토리에 모든 테스트 케이스 재실행
3. 사용자에게 결과 제시 (이전 iteration과 비교)
4. 피드백 수집 → 수정 → 반복
```

**종료 조건:** 사용자 만족 / 피드백 전부 비어 있음 / 의미 있는 개선이 더 이상 없음

### 7-3. 초안 → 재검토 패턴

스킬 수정 시 초안을 작성한 후 **새로운 시각으로 다시 읽고** 개선한다. 한 번에 완벽하게 쓰려 하지 않는다.

## 8. Description 트리거 검증

### 8-1. 트리거 Eval 쿼리 작성

20개의 eval 쿼리 — should-trigger 10개 + should-NOT-trigger 10개.

**쿼리 품질 기준:**
- 실제 사용자가 입력할 법한 구체적이고 자연스러운 문장
- 파일 경로, 개인적 맥락, 열 이름, 회사명 등 구체적 디테일 포함
- 명확한 정답보다 **경계 케이스**에 집중

**Should-trigger:** 다양한 표현의 같은 의도, 유형을 명시하지 않지만 분명히 필요한 경우, 비주류 사용 사례, 다른 스킬과 경쟁하지만 이겨야 하는 경우
**Should-NOT-trigger:** **Near-miss가 핵심** — 키워드가 유사하지만 다른 도구/스킬이 적합한 쿼리. 명백히 무관한 쿼리는 테스트 가치 없음.

### 8-2. 기존 스킬 충돌 검증

1. 기존 스킬 목록의 description을 수집
2. 새 스킬의 should-trigger 쿼리가 기존 스킬을 잘못 트리거하지 않는지 확인
3. 충돌 발견 시 description의 경계 조건을 더 명확히 기술

### 8-3. 자동 최적화 (선택적 고급 기능)

1. 20개 eval 쿼리를 Train(60%) / Test(40%) split
2. 현재 description으로 트리거 정확도 측정
3. 실패 케이스를 분석하여 개선된 description 생성
4. **Test set 기준**으로 best description 선택 (Train 기준 선택은 과적합)
5. 최대 5회 반복

> 헤드리스 실행(`claude -p`) 자동화 스크립트로 수행한다. 토큰 비용이 높으므로 스킬이 충분히 안정화된 후 최종 단계에서 실행한다.

## 9. 워크스페이스 구조

```
{skill-name}-workspace/
├── iteration-1/
│   ├── eval-descriptive-name-1/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/    (outputs/ + timing.json + grading.json)
│   │   └── without_skill/ (outputs/ + timing.json + grading.json)
│   └── benchmark.json
├── iteration-2/
└── evals/evals.json
```

**규칙:**
- eval 디렉토리는 숫자가 아닌 **서술적 이름** 사용 (예: `eval-multi-page-table-extraction`)
- 각 iteration은 독립 디렉토리에 보존 (이전 iteration 덮어쓰기 금지)
- `_workspace/`는 삭제하지 않음 — 사후 검증 및 감사 추적용
