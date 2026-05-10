# Expert Pool Team Template

## 아키텍처: 전문가 풀 (Expert Pool)

상황에 따라 적절한 전문가를 선택 호출.

```
[라우터] → { 전문가A | 전문가B | 전문가C }
```

## 적합한 경우

- 입력 유형에 따라 다른 처리가 필요
- 예시: 코드 리뷰 — 보안/성능/아키텍처 전문가 중 해당 영역만 호출

## 주의

- 라우터의 분류 정확도가 핵심.
- 상시 팀이 불필요하므로 서브 에이전트가 더 적합.

## 실행 모드 권장

- **서브 에이전트 (기본)** — 필요한 전문가만 호출
- **에이전트 팀 (변형)** — 복합 문제에서 여러 전문가가 동시에 필요할 때

## 에이전트 구성 예시

| 에이전트 | 역할 | 트리거 조건 |
|---------|------|-----------|
| router | 입력 분류, 전문가 선택 | 모든 요청 |
| security-expert | 보안 취약점 분석 | 보안 관련 코드/설정 |
| performance-expert | 성능 병목 분석 | 성능 관련 코드/쿼리 |
| architecture-expert | 구조/설계 검토 | 아키텍처 변경/리뷰 |

## 오케스트레이터 워크플로우

```
Phase 0: 컨텍스트 확인

Phase 1: 라우팅
  - Agent(router)가 입력 분석 → 필요한 전문가 목록 결정
  - 출력: `_workspace/01_router_plan.md`

Phase 2: 선택적 병렬 실행
  - router가 결정한 전문가들만 Agent로 병렬 호출 (run_in_background: true)
  - 예: 보안 + 성능만 필요 → security-expert, performance-expert 호출

Phase 3: 결과 수집
  - 각 전문가의 반환값/파일 수집
  - 필요 시 종합 보고서 생성

Phase 4: 정리
  - _workspace/ 보존
```

## 라우터 프롬프트 예시

```
당신은 입력을 분석하여 어떤 전문가가 필요한지 결정하는 라우터입니다.

분류 규칙:
- 보안 취약점, 인증, 권한 → security-expert
- 성능, 쿼리 최적화, 리소스 사용 → performance-expert
- 구조 변경, 모듈 분리, 설계 결정 → architecture-expert

출력 형식:
```
needed_experts:
  - security-expert
  - performance-expert
reason: "사용자가 인증 API의 성능 문제를 제기함"
```
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 라우터 분류 오류 | 사용자에게 분류 결과 확인 요청 |
| 전문가 1명 실패 | 나머지 결과로 진행, 실패 영역 누락 명시 |
| 모든 전문가 불필요 | 사용자에게 재분류 또는 직접 처리 제안 |
