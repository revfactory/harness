# v1 → v2 마이그레이션 가이드

harness v1(≤1.2.x)로 생성한 하네스 산출물을 v2 런타임에 맞게 전환하는 가이드. 팩토리(harness 스킬)가 Phase 0에서 v1 산출물을 감지하면 이 절차를 자동으로 제안·수행한다. 수동으로 진행할 때는 아래 순서를 따른다.

## 왜 마이그레이션이 필요한가

v1은 실험 플래그(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) 뒤의 `TeamCreate`/`SendMessage`/`TaskCreate` API를 전제로 했다. 현행 Claude Code에서는:

- `TeamCreate` / `TeamDelete` / `team_name`이 **제거**되었다 — 세션에 단일 암묵 팀이 있고, `Agent(name: ...)`으로 스폰한 에이전트가 곧 팀원이다
- `SendMessage`와 공유 태스크(`TaskCreate` 등)는 **플래그 없이** 동작한다
- 결정적 오케스트레이션을 위한 **`Workflow` 도구**가 추가되었다 — v1이 팀으로 흉내 내던 대규모 팬아웃·검증 루프의 상위 호환

v1 오케스트레이터를 그대로 실행하면 존재하지 않는 도구 호출을 시도하다 단일 에이전트 실행으로 조용히 퇴화한다. 이것이 v2를 만든 첫 번째 이유다.

## 변환 매핑

| v1 | v2 |
|----|----|
| `TeamCreate(team_name, members: [...])` | 단일 메시지에서 `Agent(name: "...", ...)` 병렬 스폰 |
| `TeamDelete` / "Phase N: 팀 정리" | 삭제 (자연 종료, 필요 시 `TaskStop`) |
| "세션당 한 팀만 활성" 제약 및 팀 재구성 절차 | 삭제 (제약 소멸) |
| `SendMessage({to: "all"})` 브로드캐스트 | 필요한 상대에게 개별 SendMessage |
| `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | 삭제 |
| 모든 에이전트 `model: "opus"` | 일괄 지정 해제 → 업무 특성(복잡도·기간·자율성·속도)별 opus/sonnet 재선택 (`references/model-selection-guide.md`) |
| 팀 기반 대규모 팬아웃/생성-검증 루프 | `Workflow` 스크립트 (`pipeline()` + `schema` + 적대적 검증) |
| Phase 0 컨텍스트 확인 (`_workspace/` 분기) | 유지 + 워크플로우 모드는 `resumeFromRunId` 추가 |
| `_workspace/` 파일 컨벤션, CLAUDE.md 포인터/변경 이력 | 그대로 유지 |

## 수동 마이그레이션 절차

1. **감사**: 오케스트레이터/에이전트 정의에서 `TeamCreate`, `TeamDelete`, `team_name`, `to: "all"`, `EXPERIMENTAL_AGENT_TEAMS`, `model: "opus"`를 grep한다
2. **모드 재판정**: 각 Phase에 대해 "작업 목록·검증 기준·반복 조건이 사전에 코드로 표현 가능한가?"를 묻는다
   - Yes → 워크플로우 모드로 전환 (harness 스킬의 `references/workflow-recipes.md` 레시피 활용)
   - No, 반복 협상 필요 → 퍼시스턴트 모드 문법으로 재작성 (`Agent(name:)` + SendMessage + Tasks)
   - No, 결과만 필요 → 서브에이전트 단발 호출로 단순화
3. **에이전트 정의 정리**: 일괄 `model: "opus"`를 업무 특성 기반 티어(opus/sonnet)로 재선택, `## 팀 통신 프로토콜` 섹션을 모드에 맞게 갱신 (워크플로우 전용 에이전트는 "구조화 출력" 섹션으로 교체), `## 재호출 지침` 추가
4. **문서 정리**: README/CLAUDE.md에서 실험 플래그 안내 제거
5. **검증**: harness 스킬 Phase 6 기준으로 구조 검증 + 드라이런. v1 유물 grep이 0건인지 최종 확인
6. **기록**: CLAUDE.md 변경 이력에 "v2 마이그레이션" 행 추가

## 자동 마이그레이션

프로젝트에서 그냥 이렇게 요청하면 된다:

```
하네스 점검해줘   (v1 산출물이 감지되면 마이그레이션을 제안한다)
```
