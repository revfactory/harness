# Producer-Reviewer Team Template

## 아키텍처: 생성-검증 (Producer-Reviewer)

생성 에이전트와 검증 에이전트가 쌍으로 동작.

```
[생성] → [검증] → (문제시) → [생성] 재실행
```

## 적합한 경우

- 산출물의 품질 보장이 중요하고 객관적 검증 기준이 존재
- 예시: 웹툰 — artist 생성 → reviewer 검수 → 문제 패널 재생성

## 주의

- 무한 루프 방지를 위해 최대 재시도 횟수(2~3회) 설정 필수.
- 에이전트 팀이 유용. SendMessage로 생성자↔검증자 간 실시간 피드백 교환.

## 실행 모드 권장

- **에이전트 팀** — 생성자↔검증자 간 실시간 피드백으로 재작업 최소화
- **서브 에이전트** — 통신 오버헤드가 과할 때 (2개뿐이고 단순 전달)

## 에이전트 구성 예시

| 팀원 | 역할 | 출력 |
|------|------|------|
| producer | 초안/산출물 생성 | `_workspace/{artifact}_draft.md` |
| reviewer | 품질 검증, 수정 지시 | `_workspace/{artifact}_review.md` |

## 오케스트레이터 워크플로우

```
Phase 0: 컨텍스트 확인

Phase 1: 준비
  - _workspace/ 생성

Phase 2: 생성
  - Agent(producer) 또는 TeamCreate(producer)
  - 초안 생성 → `_workspace/draft.md`

Phase 3: 검증
  - Agent(reviewer) 또는 팀 내 reviewer에게 할당
  - 검증 기준 적용 → `_workspace/review.md`
  - 판정: PASS / FIX / REDO

Phase 4: 재작업 (조건부)
  - FIX: producer가 부분 수정
  - REDO: producer가 전면 재생성 (최대 2회)
  - PASS: Phase 5로 진행

Phase 5: 최종 확정
  - 오케스트레이터가 _workspace/ 내용을 취합하여 {output-path}/에 최종 산출물 생성
  - _workspace/ 보존
```

## 검증 기준 예시 (웹툰)

```markdown
## Panel {N}
- 판정: PASS | FIX | REDO
- 사유: [구체적 이유]
- 수정 지시: [FIX/REDO인 경우 구체적 수정 방향]
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| REDO 2회 후에도 불합격 | 경고와 함께 PASS 처리 (최종 보고서에 명시) |
| 생성자/검증자 간 기준 불일치 | 사용자에게 중재 요청 |
| producer가 reviewer의 지시를 이해 못 함 | 구체적 예시를 포함한 재지시 |

## 재시도 정책

```
max_retries: 2
retry_trigger: REDO 판정
fallback: 2회 초과 시 강제 PASS + 보고서에 "품질 이슈" 명시
```
