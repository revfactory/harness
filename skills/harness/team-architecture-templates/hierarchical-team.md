# Hierarchical Team Template

## 아키텍처: 계층적 위임 (Hierarchical Delegation)

상위 에이전트가 하위 에이전트에 재귀적으로 위임. 복잡한 문제를 단계적으로 분해.

```
[총괄] → [팀장A] → [실무자A1]
                  → [실무자A2]
       → [팀장B] → [실무자B1]
```

## 적합한 경우

- 문제가 자연스럽게 계층적으로 분해되는 구조
- 예시: 풀스택 앱 개발 — 총괄 → 프론트엔드팀장 → (UI/로직/테스트) + 백엔드팀장 → (API/DB/테스트)

## 주의

- 깊이 3단계 이상은 지연과 컨텍스트 손실이 커짐. **2단계 이내 권장.**
- 에이전트 팀은 중첩 불가 (팀원이 팀 생성 불가). 1단계는 팀, 2단계는 서브 에이전트로 구현하거나, 평탄화하여 단일 팀으로 구성.

## 실행 모드 권장

- **1단계**: 에이전트 팀 (총괄 + 팀장들)
- **2단계**: 서브 에이전트 (팀장이 실무자를 Agent 도구로 호출)
- **또는 평탄화**: 단일 팀으로 구성 (총괄 + 팀장A + 팀장B + 실무자A1 + 실무자A2 + ...)

## 에이전트 구성 예시

| 계층 | 에이전트 | 역할 | 모드 |
|------|---------|------|------|
| L0 | director | 전체 조율, 최종 결정 | 팀 리더 |
| L1 | frontend-lead | 프론트엔드 전체 설계 | 팀원 (→ 서브 에이전트 호출) |
| L1 | backend-lead | 백엔드 전체 설계 | 팀원 (→ 서브 에이전트 호출) |
| L2 | ui-designer | UI 상세 설계 | 서브 에이전트 |
| L2 | api-developer | API 구현 | 서브 에이전트 |
| L2 | db-designer | DB 스키마 설계 | 서브 에이전트 |

## 오케스트레이터 워크플로우 (평탄화 버전)

```
Phase 0: 컨텍스트 확인

Phase 1: 준비
  - _workspace/ 생성

Phase 2: 팀 구성 (평탄화)
  - TeamCreate(team_name: "hierarchical-team",
      members: [director, frontend-lead, backend-lead, ui-designer, api-developer, db-designer])
  - director가 전체 작업 분해 → TaskCreate

Phase 3: 1단계 실행 (팀원 자체 조율)
  - frontend-lead, backend-lead가 각자 영역 설계
  - 필요 시 SendMessage로 director에게 결정 요청

Phase 4: 2단계 실행 (서브 에이전트 또는 팀 내 할당)
  - frontend-lead가 ui-designer에게 상세 작업 할당
  - backend-lead가 api-developer, db-designer에게 상세 작업 할당
  - (팀 내 TaskCreate로 처리)

Phase 5: 통합
  - director가 모든 산출물 수집
  - 최종 산출물 생성

Phase 6: 정리
  - 팀 정리
  - _workspace/ 보존
```

## 오케스트레이터 워크플로우 (중첩 버전)

```
Phase 1: 팀 구성 (L0-L1)
  - TeamCreate(team_name: "director-team", members: [director, frontend-lead, backend-lead])

Phase 2: L1 팀원들이 서브 에이전트 호출
  - frontend-lead가 Agent(ui-designer, run_in_background=true) 호출
  - backend-lead가 Agent(api-developer, run_in_background=true), Agent(db-designer, run_in_background=true) 호출

Phase 3: 결과 수집
  - L1 팀원들이 서브 에이전트 결과 수집
  - director가 L1 결과 종합

Phase 4: 정리
  - 팀 정리
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| L2 실패 | L1 팀원이 1회 재시도. 재실패 시 director에게 보고 |
| L1 실패 | director가 직접 대체 전략 수립 또는 사용자 확인 |
| 컨텍스트 손실 (깊이 3+) | 평탄화 권장. 2단계 이상은 서브 에이전트보다 팀 평탄화가 안정적 |

## 권장 팀 크기

| 작업 규모 | 권장 팀원 수 | 팀원당 작업 수 |
|----------|------------|--------------|
| 소규모 (5~10개 작업) | 2~3명 | 3~5개 |
| 중규모 (10~20개 작업) | 3~5명 | 4~6개 |
| 대규모 (20개+ 작업) | 5~7명 | 4~5개 |

> 팀원이 많을수록 조율 오버헤드가 커진다. 3명의 집중된 팀원이 5명의 산만한 팀원보다 낫다.
