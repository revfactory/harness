# Pipeline Team Template

## 아키텍처: 파이프라인 (Pipeline)

순차적 작업 흐름. 이전 에이전트의 출력이 다음 에이전트의 입력.

```
[분석] → [설계] → [구현] → [검증]
```

## 적합한 경우

- 각 단계가 이전 단계의 산출물에 강하게 의존
- 예시: 소설 집필 — 세계관 → 캐릭터 → 플롯 → 집필 → 편집

## 주의

- 병목이 전체 파이프라인을 지연시킴. 각 단계를 가능한 독립적으로 설계할 것.
- 순차 의존이 강해 팀 모드의 이점이 제한적. 단, 파이프라인 내 병렬 구간이 있으면 팀 모드 유용.

## 실행 모드 권장

- **기본**: 서브 에이전트 (순차 실행, 결과 전달만 필요)
- **변형**: 파이프라인 내 병렬 구간이 있으면 해당 구간만 에이전트 팀

## 에이전트 구성 예시

| 단계 | 에이전트 | 역할 | 입력 | 출력 |
|------|---------|------|------|------|
| 1 | analyst | 요구사항 분석 | 사용자 입력 | `_workspace/01_analyst_requirements.md` |
| 2 | designer | 아키텍처 설계 | analyst 출력 | `_workspace/02_designer_architecture.md` |
| 3 | implementer | 구현 | designer 출력 | `_workspace/03_implementer_code.md` |
| 4 | verifier | 검증 | implementer 출력 | `_workspace/04_verifier_report.md` |

## 오케스트레이터 워크플로우

```
Phase 0: 컨텍스트 확인
  - _workspace/ 존재 여부 확인 → 초기/부분 재실행/새 실행 분기

Phase 1: 준비
  - 사용자 입력 분석
  - _workspace/ 생성

Phase 2: 순차 실행
  - Agent(analyst) → 결과 저장
  - Agent(designer, 입력=analyst 결과) → 결과 저장
  - Agent(implementer, 입력=designer 결과) → 결과 저장
  - Agent(verifier, 입력=implementer 결과) → 결과 저장

Phase 3: 통합
  - 최종 산출물 생성 (필요 시)

Phase 4: 정리
  - _workspace/ 보존
  - 결과 요약 보고
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 단계 N 실패 | 해당 단계 1회 재시도. 재실패 시 이전 단계로 롤백 또는 사용자 확인 |
| 연쇄 지연 | 타임아웃 설정. 초과 시 부분 결과 반환 |

## 팀 재구성

파이프라인의 각 단계는 독립적이므로 Phase 간 팀 재구성이 필요 없음. 서브 에이전트를 순차 호출.
