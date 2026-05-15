# 검색 효율화 — Grep/Read 4-Step 탐색 프로토콜 (선택적 가이드)

코드 탐색 비중이 큰 도메인의 에이전트가 Grep과 Read로 토큰을 폭발시키지 않도록 안내하는 가이드. **모든 하네스에 강제하지 않으며**, Phase 1에서 코드 탐색이 큰 도메인이라고 판단된 경우에만 에이전트 정의에 인용한다.

## 목차

1. [언제 적용하는가](#언제-적용하는가)
2. [원칙: Cheap First, Expensive Later](#원칙)
3. [4-Step 탐색 프로토콜](#4-step-탐색-프로토콜)
4. [Claude Code Grep 도구 옵션 활용표](#claude-code-grep-도구-옵션-활용표)
5. [에이전트 정의 자동 주입 템플릿](#에이전트-정의-자동-주입-템플릿)
6. [Memo 패턴과의 시너지](#memo-패턴과의-시너지)
7. [흔한 안티패턴](#안티패턴)

---

## 언제 적용하는가

| 적용 권장 | 적용 비권장 |
|----------|-----------|
| 대규모 코드베이스(수만 줄+) 탐색 | 작은 단일 디렉토리 분석 |
| 다중 패턴 검색이 반복되는 작업 | 검색이 1~2회로 끝나는 작업 |
| 마이그레이션·리팩터·보안 감사 | 글쓰기·리서치(웹 기반)·문서 변환 |
| 에이전트가 코드를 *수정*하기 전 탐색 단계 | 단순 파일 1개 편집 |

**default는 "적용 안 함"**이다. 코드 탐색이 작업의 핵심이 아니면 이 가이드를 끌어들이지 않는다.

---

## 원칙

> **싸게 시작해서 점점 비싼 호출로 좁혀라 (Cheap First, Expensive Later).**

큰 검색을 한 번에 풀 콘텐츠로 받으면 결과 라인이 수백 줄이 된다. 이는 두 가지 비용을 발생시킨다:
1. **직접 비용**: 그 라인들이 곧장 컨텍스트에 들어가 토큰을 잡아먹음.
2. **간접 비용**: 잡음이 많아지면 에이전트의 추론 집중력이 흐려져 더 많은 후속 호출을 유발.

해결책은 **항상 가장 싼 모드로 시작**하고, 결과가 작거나 충분히 좁혀졌을 때만 비싼 모드(content + Read)로 전환하는 것이다.

---

## 4-Step 탐색 프로토콜

다음 순서를 지킨다. 한 단계가 충분하면 다음 단계로 넘어가지 않는다.

### Step 1 — Count부터 (가장 싸다)

**목적:** 검색 패턴이 코드베이스에 얼마나 흔한지 먼저 파악.

```
Grep(pattern: "useAuth", output_mode: "count")
→ "useAuth가 12개 파일에서 47회 매치"
```

**판단 기준:**
- 매치 < 5: 바로 Step 3 (의심 파일 Read)으로
- 매치 5~50: Step 2로
- 매치 50+: 패턴이 너무 광범위 → 패턴 자체를 더 좁히거나 Step 4(서브에이전트 위임)

### Step 2 — files_with_matches로 좁히기

**목적:** 어느 파일에 있는지만 확인. 라인 내용은 받지 않는다.

```
Grep(pattern: "useAuth", output_mode: "files_with_matches", head_limit: 20)
→ ["src/auth/useAuth.ts", "src/components/Login.tsx", ...]
```

**판단 기준:**
- 파일 1~3개: Step 3로
- 파일 5~10개: glob/path로 더 좁힐 수 있는지 확인 → 좁힌 후 Step 3
- 파일 10+개: Step 4

### Step 3 — Read with offset/limit (의심 파일만 부분 로드)

**목적:** 좁혀진 파일의 *해당 영역*만 읽는다. 절대 파일 전체를 읽지 않는다.

먼저 라인 번호를 얻는다:
```
Grep(pattern: "useAuth", path: "src/auth/useAuth.ts",
     output_mode: "content", -n: true, head_limit: 5)
→ "23: export function useAuth() {"
```

그 영역만 Read:
```
Read(file_path: "src/auth/useAuth.ts", offset: 18, limit: 30)
→ 18~47행만 받음
```

**원칙:**
- 컨텍스트 라인은 기본 0. 정말 필요할 때만 `-C 2` (3 이상은 거의 항상 과도)
- Read의 `limit`은 작게 시작. 부족하면 추가 Read.

### Step 4 — Explore 서브에이전트에 위임 (대용량의 최후 수단)

**목적:** 검색이 진정으로 광범위해야 하는 경우(예: "이 코드베이스 전체에서 모든 외부 API 호출 위치"), 메인 컨텍스트를 보호하기 위해 서브에이전트로 격리.

```
Agent(
  subagent_type: "Explore",
  model: "haiku-4-5",   ← 검색·요약은 가벼운 모델로 충분
  prompt: "이 패턴 X를 찾아 (1) 파일별 카운트 (2) 가장 의심되는 진입점 3개 (3) 한 줄 결론을 보고해. 매치 라인 본문은 절대 그대로 넘기지 마."
)
→ 메인은 압축된 결론(수십 토큰)만 받음
```

**원칙:**
- 서브에이전트 결과는 *결론 + 좌표*만. 매치 본문 전체를 받으면 위임의 의미가 없음.
- `Explore` 타입은 읽기 전용이라 안전.

---

## Claude Code Grep 도구 옵션 활용표

| 옵션 | 효과 | 토큰 영향 | 권장 사용 |
|------|------|----------|----------|
| `output_mode: "count"` | 매치 수만 반환 | **최저** | Step 1 항상 |
| `output_mode: "files_with_matches"` | 파일 경로만 반환 | 낮음 | Step 2 |
| `output_mode: "content"` | 라인 내용 반환 | 높음 | Step 3에서만 |
| `head_limit: N` | 첫 N개로 제한 | 비례 | content 모드에서 항상 명시 |
| `-n: true` | 라인 번호 표시 | 낮음 | Step 3 진입 직전 |
| `-C N` | 앞뒤 N줄 컨텍스트 | **2배~** | 0이 기본. 1~2까지만 |
| `glob` / `path` | 검색 범위 좁힘 | 큰 절감 | 가능하면 항상 명시 |
| `multiline: true` | 멀티라인 매칭 | 매우 높음 | 특수 패턴에만 |

**기억할 한 줄:** `output_mode`를 명시하지 않은 Grep 호출은 안티패턴이다.

---

## 에이전트 정의 자동 주입 템플릿

코드 탐색 도메인의 에이전트 정의 파일(`프로젝트/.claude/agents/{name}.md`)의 `## 작업 원칙` 또는 `## 도구 사용 정책`에 다음 블록을 추가한다:

```markdown
## 검색 4-Step (필수)

코드 탐색은 항상 다음 순서로 한다. 한 단계가 충분하면 다음으로 넘어가지 않는다.

1. **Count 먼저**: `Grep(output_mode: "count")` 또는 `output_mode: "files_with_matches"`. 결과 < 5건이면 바로 3단계로.
2. **파일 좁히기**: `output_mode: "files_with_matches"` + `glob` 또는 `path`로 범위 축소. head_limit 명시.
3. **부분 Read**: 의심 파일 1~3개를 `Grep(-n)`로 라인 식별 후 `Read(offset, limit)`로 ±15행만 로드. 파일 전체 Read 금지.
4. **위임(최후)**: 검색이 광범위하고 결론만 필요하면 `Agent(subagent_type:"Explore", model:"haiku-4-5")`로 격리. 결과는 결론 + 좌표만 받기.

원칙: `output_mode`를 명시하지 않은 Grep은 사용 금지. 컨텍스트 라인 `-C`는 0이 기본, 필요해도 2 이하.
```

---

## Memo 패턴과의 시너지

Memo 패턴(`memo-pattern.md`)을 함께 적용하면 검색 비용이 누적적으로 절감된다.

에이전트 슬롯(`.harness/agents/{agent}.md`)의 `## Search Discoveries` 섹션에 발견한 좌표를 한 줄로 기록한다:

```markdown
## Search Discoveries
- `src/auth/useAuth.ts:23` — useAuth 정의 위치
- `src/middleware/withAuth.ts:*` — 모든 라우트 진입점 공통 미들웨어
- `lib/auth/*.test.ts` — 인증 테스트 묶음 (12개 파일)
```

다음 세션에서는 같은 패턴을 다시 grep할 필요 없이 슬롯의 Discoveries만 읽으면 된다. **검색 결과를 캐싱**하는 효과.

Memo 패턴을 적용하지 않았더라도 서브에이전트 위임 시 결과를 메인이 별도 노트(`_workspace/discoveries.md`)로 한 번만 정리해두면 동일 효과를 얻을 수 있다.

---

## 안티패턴

다음은 **하지 말 것**:

| 안티패턴 | 왜 금지 | 대안 |
|---------|--------|------|
| 첫 호출에 `output_mode: "content"` | Step 1 건너뜀, 토큰 폭발 | count부터 |
| `head_limit` 없이 content 모드 | 결과가 수백 줄 들어옴 | head_limit 항상 명시 |
| `-C 5` 이상 | 컨텍스트 5배 폭증 | 0 또는 2 |
| 의심 파일 *전체* Read | 토큰 폭발 | offset+limit |
| 같은 패턴 반복 검색 | 토큰 낭비 | Discoveries에 좌표 캐싱 |
| 광범위 패턴(`function`, `import`)을 직접 grep | 매치 수천 건 | path/glob으로 범위 축소, 또는 더 구체적 패턴 |
| 서브에이전트가 매치 본문 전체를 메인에 반환 | 위임 의미 상실 | "결론 + 좌표만 보고" 명시 |

---

## 적용 체크리스트

검색 효율화를 적용한 하네스가 갖춰야 하는 것:

- [ ] 코드 탐색이 큰 도메인임을 Phase 1에서 명시
- [ ] 코드 탐색 담당 에이전트의 정의 파일에 `## 검색 4-Step` 블록 주입
- [ ] 오케스트레이터가 광범위 탐색이 필요한 경우 서브에이전트(Explore + haiku) 위임 패턴 사용
- [ ] (Memo 패턴 동시 적용 시) 슬롯 스키마에 `## Search Discoveries` 섹션 포함
- [ ] 안티패턴 7개를 코드 리뷰 시점에 점검
