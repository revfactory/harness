# Supervisor Team Template

## 아키텍처: 감독자 (Supervisor)

중앙 에이전트가 작업 상태를 관리하며 하위 에이전트에 동적으로 작업을 분배.

```
         ┌→ [워커A]
[감독자] ─┼→ [워커B]    ← 감독자가 상태를 보고 동적 분배
         └→ [워커C]
```

## 적합한 경우

- 작업량이 가변적이거나 런타임에 작업 분배를 결정해야 할 때
- 예시: 대규모 코드 마이그레이션 — 감독자가 파일 목록을 분석하고 워커들에게 배치 할당

## 주의

- 감독자가 병목이 되지 않도록 위임 단위를 충분히 크게 설정.
- 팬아웃과의 차이: 팬아웃은 사전에 작업을 고정 분배, 감독자는 진행 상황을 보며 동적 조정

## 실행 모드 권장

- **에이전트 팀** — 공유 작업 목록이 감독자 패턴과 자연스럽게 매칭. TaskCreate로 작업 등록, 팀원들이 자체 요청(claim).

## 에이전트 구성 예시

| 팀원 | 역할 |
|------|------|
| supervisor (리더) | 파일 분석, 배치 분배, 진행 관리 |
| worker-1 ~ worker-N | 할당된 작업 수행 |

## 오케스트레이터 워크플로우

```
Phase 0: 컨텍스트 확인

Phase 1: 준비
  - 전체 대상 작업 목록 수집
  - _workspace/ 생성

Phase 2: 팀 구성
  - TeamCreate(team_name: "supervisor-team", members: [supervisor, worker-1, worker-2, ...])
  - supervisor가 작업 목록 분석

Phase 3: 동적 분배
  - supervisor가 TaskCreate로 작업 등록 (의존성 포함)
  - 팀원들이 자체적으로 작업 요청 (claim)
  - supervisor가 TaskGet으로 진행 상황 모니터링

Phase 4: 진행 관리
  - 팀원이 TaskUpdate로 완료 보고 시:
    - 성공 → 다음 작업 자동 요청
    - 실패 → supervisor가 SendMessage로 원인 확인 → 재할당
  - 새 작업 발견 시 동적으로 TaskCreate 추가

Phase 5: 통합
  - 모든 작업 완료 → supervisor가 통합/최종 검증

Phase 6: 정리
  - 팀 정리
  - _workspace/ 보존
```

## 동적 분배 로직

```
1. 전체 대상 파일/작업 목록 수집
2. 복잡도 추정 (파일 크기, import 수, 의존성)
3. TaskCreate로 작업 등록 (의존성 포함)
4. 팀원들이 자체적으로 작업 요청 (claim)
5. 팀원이 TaskUpdate로 완료 보고 시:
   - 성공 → 다음 작업 자동 요청
   - 실패 → 리더가 SendMessage로 원인 확인 → 재할당 또는 다른 팀원에게 배정
6. 모든 작업 완료 → 리더가 통합 테스트 실행
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 워커 1명 실패 | supervisor가 원인 파악 → 동일 워커 재시도 또는 다른 워커에게 재할당 |
| 워커 과반 실패 | 작업 단위가 너무 큼 → 작업 분할 후 재분배 |
| supervisor 과부하 | 작업 단위를 더 크게 조정, 워커 자율성 확대 |
| 작업 목록 런타임 변경 | supervisor가 새 TaskCreate로 동적 추가 |
