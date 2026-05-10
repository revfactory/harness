# Fan-out/Fan-in Team Template

## 아키텍처: 팬아웃/팬인 (Fan-out/Fan-in)

병렬 처리 후 결과 통합. 독립적 작업을 동시 수행.

```
         ┌→ [전문가A] ─┐
[분배] → ├→ [전문가B] ─┼→ [통합]
         └→ [전문가C] ─┘
```

## 적합한 경우

- 동일 입력에 대해 서로 다른 관점/영역의 분석이 필요
- 예시: 종합 리서치 — 공식/미디어/커뮤니티/배경 동시 조사 → 통합 보고

## 주의

- 통합 단계의 품질이 전체 품질을 결정.
- **반드시 에이전트 팀으로 구성해야 한다.** 팀원들이 서로 발견을 공유하고 도전하며, 한 에이전트의 발견이 다른 에이전트의 조사 방향을 실시간으로 수정할 수 있어 단독 조사 대비 품질이 크게 향상된다.

## 실행 모드 권장

- **에이전트 팀 (필수)** — 팀원 간 발견 공유, 상충 정보 실시간 토론

## 에이전트 구성 예시

| 팀원 | 에이전트 타입 | 역할 | 출력 |
|------|-------------|------|------|
| researcher-a | general-purpose | 공식 문서/블로그 조사 | `_workspace/02_researcher_a.md` |
| researcher-b | general-purpose | 미디어/투자 동향 조사 | `_workspace/02_researcher_b.md` |
| researcher-c | general-purpose | 커뮤니티/SNS 반응 조사 | `_workspace/02_researcher_c.md` |
| researcher-d | general-purpose | 배경/경쟁/학술 조사 | `_workspace/02_researcher_d.md` |
| (리더) | — | 통합 보고서 작성 | `{output-path}/final_report.md` |

## 오케스트레이터 워크플로우

```
Phase 0: 컨텍스트 확인
  - _workspace/ 존재 여부 확인

Phase 1: 준비
  - 사용자 입력 분석 (주제, 조사 모드)
  - _workspace/ 생성

Phase 2: 팀 구성
  - TeamCreate(team_name: "research-team", members: [researcher-a, b, c, d])
  - TaskCreate(4개 조사 작업 할당)

Phase 3: 병렬 조사
  - 팀원들이 자체 조율하며 독립 조사
  - 흥미로운 발견은 SendMessage로 공유
  - 상충 정보는 팀원 간 직접 토론
  - 완료 시 파일 저장 + 리더에게 알림

Phase 4: 통합
  - 리더가 4개 산출물 Read
  - 종합 보고서 생성
  - 상충 정보는 출처 병기

Phase 5: 정리
  - 팀 정리
  - _workspace/ 보존
```

## 팀 통신 패턴

```
researcher-a ──SendMessage──→ researcher-d  (관련 공식 발표 공유)
researcher-b ──SendMessage──→ researcher-d  (투자/인수 정보 공유)
researcher-c ──SendMessage──→ researcher-b  (커뮤니티 반응 중 미디어 관련)
모든 팀원 ──TaskUpdate──→ 공유 작업 목록  (진행률)
리더 ←───── 유휴 알림 ──── 완료된 팀원
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 팀원 1명 실패 | 리더가 감지 → SendMessage로 상태 확인 → 재시작 또는 대체 팀원 |
| 팀원 과반 실패 | 사용자에게 알리고 진행 여부 확인 |
| 통합 단계 데이터 충돌 | 출처 명시 후 병기, 삭제하지 않음 |
