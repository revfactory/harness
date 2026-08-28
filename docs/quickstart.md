# Quickstart — 5분 만에 첫 하네스

**끝났을 때 갖게 되는 것:** 한 문장 프롬프트로 생성된, 도메인 특화 에이전트 3~5개와 스킬이 담긴 `.claude/agents/` + `.claude/skills/` 디렉토리, 그리고 샘플 태스크 1회 실행 결과.

**사전 요구사항:**
- Claude Code 최신 버전 (`claude --version`)
- `github.com` 네트워크 접근

> v1과 달리 **환경 변수나 실험 플래그가 필요 없다.** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`를 봤다면 그건 v1 문서다.

---

## Step 1 — 마켓플레이스 추가 (30초)

```
/plugin marketplace add revfactory/harness
```

## Step 2 — 플러그인 설치 (30초)

```
/plugin install harness@harness
```

**실패 FAQ — 설치가 안 보임:** `/plugin list`로 확인. 없으면 Step 1부터 재실행, 있는데 비활성이면 `/plugin enable harness@harness`.

## Step 3 — 한 문장으로 하네스 생성 (2분)

```
claude "핀테크 리스크 평가 팀 하네스 구성해줘"
```

다른 예시 (전부 동작한다):
- `claude "build a harness for an e-commerce fraud-detection workflow"`
- `claude "오픈소스 저장소 기술 실사(due diligence)용 에이전트 팀 설계해줘"`

**기대 출력:** 현황 감사(Phase 0) 보고 → 실행 모드/아키텍처 제안 → 에이전트 3~5개 파일 + 스킬 + 오케스트레이터 생성 확인.

## Step 4 — 생성 파일 확인 (30초)

```bash
ls -la .claude/agents/ .claude/skills/
```

**실패 FAQ — 아무것도 생성 안 됨:** 플러그인 활성 여부 확인(Step 2 FAQ). 활성인데도 스킬이 트리거되지 않으면 "하네스 구성해줘"처럼 트리거 키워드를 명시.

## Step 5 — 샘플 태스크 실행 (90초)

실제 티켓 스타일 프롬프트를 새 팀에 넘겨본다:

```
claude "Ticket FIN-427: 신규 법인 고객(중견 제조사, 매출 $80M, 한국)이 $5M 운전자금
한도를 신청했다. (1) 신용 이력 적신호, (2) 기존 포트폴리오 대비 섹터 집중도,
(3) 규제 노출(공정위, 금융위)을 다룬 리스크 평가를 수행하고, go/no-go 권고가 담긴
1페이지 메모를 산출하라."
```

오케스트레이터 스킬이 트리거되어 생성된 팀 패턴(리스크 업무라면 보통 생성-검증 또는 전문가 풀)으로 라우팅된다.

**비용 주의:** 멀티에이전트 실행은 태스크당 수만~수십만 토큰을 소비할 수 있다. 생성된 오케스트레이터는 기본 규모를 절제하도록 설계되며, "철저히/전수" 요청 시에만 확장된다. 토큰 목표를 직접 주고 싶으면 프롬프트에 "+500k" 같은 버짓 지시를 포함하라 — 워크플로우 모드 하네스는 이에 연동해 규모를 조절한다.

## 다음 단계

- 결과가 아쉬우면: `"하네스 회고해줘"` → `/harness:evolve`가 피드백을 일반화해 반영
- v1 하네스가 있는 프로젝트면: `"하네스 점검해줘"` → 마이그레이션 자동 제안 ([migration-v1-to-v2.md](migration-v1-to-v2.md))
