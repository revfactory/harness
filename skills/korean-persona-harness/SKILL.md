---
name: korean-persona-harness
description: "한국어 퍼소나(Nemotron-Personas-Korea) 기반으로 임의 도메인의 에이전트 팀을 만들어주는 메타 하네스 오케스트레이터. 한국 업무·문화·언어 감각이 살아있는 에이전트가 필요할 때 사용한다. '한국어 페르소나로 팀 만들어줘', '한국인 캐릭터 에이전트 만들어줘', '한국 X 도메인 하네스 만들어줘', '한국 페르소나로 X 시나리오 에이전트 생성', '한국어 화법으로 다시 만들어줘', '페르소나 다시 뽑아서 팀 재구성', 후속 요청('업데이트', '재실행', '보완', '추가')에서도 트리거된다. 일반 harness와 달리 한국어·한국 문화 맥락에 특화."
---

# Korean Persona Harness — 한국어 퍼소나 메타 하네스

임의 도메인/시나리오에 대해 **한국어 화자**의 직무·세대·지역 다양성을 반영한 에이전트 팀을 자동 생성하는 메타 오케스트레이터. NVIDIA Nemotron-Personas-Korea(100만 행) 데이터셋을 런타임 검색하여 페르소나를 동적으로 매핑하고, 한국 업무 문화·존댓말·산업 어휘로 톤을 다듬어 `.claude/agents/`에 최종 에이전트 정의를 출력한다.

## 언제 사용하는가

이 스킬을 트리거하라:
- 한국어 응답·한국 사용자 대상 시나리오용 에이전트가 필요할 때
- 단순 "전문가" 추상이 아니라 **실재성 있는 한국 페르소나**(특정 직무·연령·지역)가 필요할 때
- 가상 인터뷰, UX 리서치, 마케팅 페르소나 시뮬레이션, 콘텐츠 제작팀 등

이 스킬을 *사용하지 마라*:
- 영어/일본어 등 다른 언어 페르소나 (다른 데이터셋 필요)
- 기술 아키텍처 설계처럼 페르소나가 부적절한 추상 작업 — `harness` 스킬을 직접 쓰라

## 일반 `harness`와의 차이

| 항목 | `harness` | `korean-persona-harness` |
|------|-----------|--------------------------|
| 산출물 | 임의 도메인 에이전트 팀 | 한국어 페르소나가 입혀진 에이전트 팀 |
| 데이터 근거 | 도메인 코드베이스·스킬셋 | + Nemotron-Personas-Korea 검색 결과 |
| Voice/Tone | 일반적 | 한국 직장 매너·존댓말·업종 어휘 |
| 의존 스킬 | — | `korean-persona-search`, `korean-voice-adapter` |

`harness`의 상위 호환이 아니라 **한국어 도메인에 특화된 분기**다. 두 스킬이 충돌하면 사용자 의도(한국어 페르소나가 핵심?)에 따라 선택하라.

## 워크플로우 (서브 에이전트 파이프라인)

5개 메타 에이전트를 **순차 파이프라인**으로 호출한다 (이 5명은 본 플러그인 내부 도구로, 사용자의 `.claude/agents/`에 설치되지 않는다 — 각 단계마다 `Agent` 도구로 ephemeral 호출). 각 단계의 산출물은 `_workspace/` 폴더에 파일로 보존한다.

```
[scenario-analyst] → [persona-curator] → [voice-adapter] → [definition-builder] → [diversity-qa]
       ↓                    ↓                  ↓                    ↓                 ↓
  01_scenario.md    02_personas.json    03_voiced.json     04_agents/*.md    05_qa_report.md
                          ↑ uses                ↑ uses                              ↓
                   korean-persona-search   korean-voice-adapter                  retry?
```

QA가 편향·중복을 발견하면 큐레이터 단계로 1회 되돌아가 재샘플링한다.

### Phase 0: 컨텍스트 확인

먼저 다음을 확인한다:

1. `_workspace/korean-persona-harness/` 폴더 존재 여부
   - 존재 + 사용자가 부분 수정 요청 → **부분 재실행** (해당 단계만 재호출)
   - 존재 + 사용자가 새 시나리오 제공 → 기존을 `_workspace/.../prev_{timestamp}/`로 archive 후 새 실행
   - 미존재 → **초기 실행**
2. 한국어 퍼소나 캐시 상태 점검:
   ```bash
   python skills/korean-persona-search/scripts/download.py --check
   ```
   캐시가 없으면 사용자에게 다운로드 안내(수 GB) 후 진행 결정.

### Phase 1: 시나리오 분석 (scenario-analyst)

`references/agents/scenario-analyst.md` 의 프롬프트로 `Agent(subagent_type: general-purpose, model: opus)` 호출.

**입력**: 사용자의 도메인/요청 원문
**출력 (`_workspace/korean-persona-harness/01_scenario.md`)**:
- 도메인 요약 (1~2문장)
- 필요한 에이전트 역할 N개 (각 역할 1~3문장 명세)
- 각 역할의 페르소나 요건 — 직무 키워드, 연령대, 지역(있으면), 가치관/스타일, 관계 모드
- 검색 쿼리 사양 — `korean-persona-search`에 던질 필터 셋 (역할별)

### Phase 2: 퍼소나 큐레이션 (persona-curator)

`references/agents/persona-curator.md` 프롬프트로 호출.

각 역할마다 Phase 1의 검색 사양을 가져와 `korean-persona-search` 스크립트를 실행, **다양성을 강조**하여 후보 1.5N을 받고 그중 N을 선별. 중복(같은 직업 카테고리·연령대 쏠림) 회피.

**출력 (`_workspace/.../02_personas.json`)**:
```json
{
  "scenario": "...",
  "agents": [
    {
      "role_id": "agent-1",
      "role_name": "...",
      "role_brief": "...",
      "persona_card": { /* korean-persona-search 출력 카드 */ },
      "selection_reason": "왜 이 퍼소나가 이 역할에 맞는지"
    },
    ...
  ]
}
```

### Phase 3: 화법·문화 어댑팅 (voice-adapter)

`references/agents/voice-adapter.md` 프롬프트로 호출. 각 카드에 `korean-voice-adapter` 스킬을 적용하여 voice 가이드 생성.

**출력 (`_workspace/.../03_voiced.json`)**:
Phase 2 구조 + 각 agent에 `voice_guide` (마크다운 블록) 추가.

다양성 — 5명이 모두 같은 톤이면 단조롭다. 합쇼체파 1, 해요체파 2~3, 캐주얼 1로 분산되도록 어댑터에 명시.

### Phase 4: 에이전트 정의 빌드 (definition-builder)

`references/agents/definition-builder.md` 프롬프트로 호출.

`harness` 스킬의 표준 에이전트 정의 포맷에 따라 각 에이전트의 `.md`를 생성, `_workspace/.../04_agents/{name}.md`에 저장.

필수 섹션: 핵심 역할, 작업 원칙, 입력/출력 프로토콜, 에러 핸들링, 협업, **Voice & Tone** (Phase 3의 voice_guide), **Korean Persona Source** (출처 표기 — uuid + CC BY 4.0 attribution).

이름은 영문 kebab-case (한국어 직무명을 영문화) — Claude Code 파일 컨벤션 준수.

### Phase 5: 다양성 QA (diversity-qa)

`references/agents/diversity-qa.md` 프롬프트로 호출. 5명 팀의 인구통계 분포·voice 다양성을 점검.

체크 항목:
- 성별 비율 (한쪽 100% 회피)
- 연령대 (전부 30대 회피)
- 지역 (전부 서울 회피, 단 시나리오가 서울 한정이면 OK)
- 직업 카테고리 (전부 동일 카테고리 회피, 단 의도된 동일 직군 팀이면 OK)
- 톤 다양성 (합쇼/해요/캐주얼 분포)
- 페르소나 출처 attribution 누락 여부

**출력 (`_workspace/.../05_qa_report.md`)**:
- pass/fail 항목별 결과
- 실패 시 어떤 페르소나를 어떤 조건으로 재샘플링하라는 권장
- pass 시 최종 산출물 위치 안내

QA fail이면 자동으로 Phase 2로 1회 회귀(재샘플링). 두 번째 fail이면 사용자에게 보고하고 중지.

### Phase 6: 사용자 출력

QA pass 후:
1. `_workspace/.../04_agents/*.md` → 적절한 에이전트 디렉토리로 복사:
   - **Claude Code 런타임**: 프로젝트의 `.claude/agents/`
   - **Codex CLI 런타임**: `${CODEX_HOME:-~/.codex}/agents/` (또는 프로젝트 단위로 사용자가 지정한 경로)
   - 사용자가 명시적으로 출력 경로를 지정하면 그곳 우선
   - 런타임 감지: `CODEX_HOME` 환경변수 존재 + Codex 컨텍스트 → Codex 경로, 그 외 → Claude Code
2. CLAUDE.md(또는 Codex의 `~/.codex/rules/`)에 하네스 변경 이력 한 줄 추가
3. 결과 보고 — 생성된 에이전트 목록, 각 페르소나의 한 줄 소개, 다음 추천 단계

## 데이터 전달 프로토콜

- **파일 기반** (주) — `_workspace/korean-persona-harness/` 하위에 단계별 산출물 저장. 후속 부분 재실행, 감사 추적용.
- **반환값 기반** — 각 sub-agent의 stdout 마지막 줄에 다음 단계 트리거용 요약 1줄.

## 후속 작업

다음 요청을 인식하라:
- "재실행", "다시" — 전체 재실행 (기존 _workspace를 prev로 archive)
- "X 부분만 다시" — 해당 Phase부터 재실행
- "페르소나 다시 뽑아줘" — Phase 2부터 재실행 (Phase 1 결과 재사용)
- "톤 다시 입혀줘" — Phase 3부터 재실행
- "다양성 더" — diversity 옵션 강화 + Phase 2 재실행

## 산출물 체크리스트

완료 시 확인:
- [ ] `_workspace/korean-persona-harness/01_scenario.md` 작성됨
- [ ] `02_personas.json`에 역할 수만큼 카드 포함, attribution 명시
- [ ] `03_voiced.json`에 각 voice_guide 5개 검사항목(자칭/존댓말/어조샘플/어휘/금기) 통과
- [ ] `04_agents/*.md` 각 파일이 harness 표준 섹션 모두 포함
- [ ] `05_qa_report.md` pass
- [ ] 최종 에이전트 정의가 `.claude/agents/`에 복사됨
- [ ] 출처 표기 (CC BY 4.0)가 각 정의 하단에 있음

## 런타임 호환

본 스킬은 **Claude Code**와 **Codex CLI** 두 런타임에서 동일하게 작동한다. 스킬 파일 포맷이 양쪽 호환이며, 의존 스크립트는 환경 변수만 다를 뿐 같다.

설치는 `scripts/install-korean-persona.sh --help` 참조 — `--target {codex|claude-code|both}` 옵션으로 양 런타임에 한 번에 배포 가능.

## 참조

- 메타 에이전트 프롬프트 템플릿: `references/agents/`
- 검색 스킬: `../korean-persona-search/SKILL.md`
- 화법 어댑터 스킬: `../korean-voice-adapter/SKILL.md`
- 데이터셋: https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea (CC BY 4.0)
- 설치 스크립트 (Claude Code + Codex): `../../scripts/install-korean-persona.sh`

## 테스트 시나리오

**정상 흐름**: "한국 푸드테크 스타트업의 신규 배달 앱을 위한 5인 페르소나 팀 만들어줘 — PO, 디자이너, 백엔드 개발자, CS 리드, 마케터"
→ Phase 1에서 5개 역할 식별 → Phase 2에서 각 역할 검색·선별 → Phase 3 voice 입힘 → Phase 4 정의 빌드 → Phase 5 다양성 통과 → Phase 6 출력

**에러 흐름**: 사용자가 너무 좁은 조건 요청 (예: "30대 여성, 제주도, 의사 5명") → Phase 2에서 결과 부족 → 큐레이터가 사용자에게 조건 완화 권장하고 중단
