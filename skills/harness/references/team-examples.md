# 실전 팀 구성 예시 (v2)

각 예시는 실행 모드 선택의 근거와 v2 문법 골격을 보여준다. 모드 정의는 `execution-modes.md`, 스크립트 상세는 `workflow-recipes.md` 참조.

---

## 예시 1: 종합 리서치 팀 — 워크플로우 오케스트레이션

**패턴:** 팬아웃/팬인 + 적대적 검증 | **모드 근거:** 조사 축이 사전 열거 가능(결정적 팬아웃), 주장별 검증 루프가 코드로 표현 가능

```
[메인] 정찰: 조사 축 확정 (공식/미디어/커뮤니티/배경)
     → Workflow(script, args: {axes, topic, ws})
         phase '조사':  pipeline(axes, axis => agent(..., {schema: FINDINGS}))
         phase '검증':  주장별 반박자 스폰 → 과반 반박 시 기각
         phase '종합':  완전성 비평가 1명 → 빠진 축 발견 시 추가 라운드
     → 반환된 구조화 결과로 메인이 종합 보고서 작성
```

에이전트 정의: `.claude/agents/researcher.md` (조사 원칙 + 구조화 출력 shape), `.claude/agents/fact-checker.md` (반박 우선 원칙). 워크플로우에서 `agentType`으로 사용.

상충 정보는 기각하지 않고 출처 병기로 반환 스키마에 포함시킨다.

## 예시 2: SF 소설 집필 팀 — 하이브리드 (퍼시스턴트 중심)

**패턴:** 파이프라인 + 생성-검증 | **모드 근거:** 세계관↔캐릭터↔플롯 간 실시간 일관성 협상이 품질을 좌우 — 컨텍스트를 유지하는 퍼시스턴트 전문가가 필수. 리뷰는 관점이 독립적이라 서브에이전트로 충분

```
Phase 1 (퍼시스턴트): Agent(name:"worldbuilder") + Agent(name:"character-designer")
                      + Agent(name:"plot-architect") 병렬 스폰
                      → TaskCreate(세계관/캐릭터/플롯, 상호 의존성 명시)
                      → 리더가 중계: worldbuilder의 사회 구조 확정 → SendMessage로
                        character-designer에 전달 → 캐릭터 직업군이 세계관과 충돌하면
                        SendMessage로 worldbuilder에 조정 요청 (컨텍스트 유지 덕에
                        "아까 그 계급 구조에서 상인 계층만 수정" 같은 지시가 통한다)
Phase 2 (서브):       prose-stylist 단발 호출 — _workspace/의 3개 산출물을 읽고 집필
Phase 3 (서브 병렬):  science-consultant + continuity-manager 독립 리뷰
Phase 4 (퍼시스턴트): SendMessage({to:"prose-stylist"}는 불가(단발이었음) →
                      Phase 2를 name 붙여 스폰했다면 여기서 리뷰 반영 지시 가능.
                      수정 반복이 예상되면 처음부터 name을 붙여라.
```

교훈: **수정 루프가 예상되는 에이전트는 처음부터 `name`을 붙여 퍼시스턴트로 스폰한다.** 단발로 부른 에이전트는 컨텍스트가 사라진다.

## 예시 3: 종합 코드 리뷰 — 워크플로우 오케스트레이션

**패턴:** 팬아웃 + 적대적 검증 | **모드 근거:** 리뷰 차원이 사전 열거 가능, 발견별 검증이 결정적 루프

```javascript
// 차원별 리뷰 → 발견별 반박 검증 (배리어 없음 — 보안 리뷰가 끝나면
// 성능 리뷰가 진행 중이어도 보안 발견들은 즉시 검증에 들어간다)
const results = await pipeline(
  [{ key: 'security', ... }, { key: 'perf', ... }, { key: 'arch', ... }, { key: 'test', ... }],
  d => agent(d.prompt, { phase: 'Review', schema: FINDINGS }),
  r => parallel((r?.findings ?? []).map(f => () =>
    agent(`반박하라: ${f.title}. 불확실하면 refuted=true.`, { phase: 'Verify', schema: VERDICT })
      .then(v => ({ ...f, v }))))
)
```

v1은 이 사례를 퍼시스턴트 팀(리뷰어 간 SendMessage 교차 공유)으로 구성했다. v2에서는 교차 영역 이슈를 "검증 단계에서 다른 차원의 발견 목록을 프롬프트에 포함"하는 방식으로 처리하는 편이 저렴하고 재현 가능하다. 리뷰어 간 실시간 토론이 정말 필요한 경우(설계 논쟁 등)에만 퍼시스턴트를 쓴다.

## 예시 4: 대규모 코드 마이그레이션 — 감독자 (퍼시스턴트) 또는 워크플로우

**패턴:** 감독자 | **모드 분기 기준:** 배치 분배가 사전에 결정 가능한가?

**(a) 분배가 결정적이면 → 워크플로우:**
```javascript
await pipeline(args.batches,   // 정찰로 복잡도 추정 후 배치 확정
  b => agent(`배치 마이그레이션: ${b.files.join(', ')}`,
    { agentType: 'migrator', isolation: 'worktree' }),   // 병렬 파일 수정 → worktree 격리
  (r, b) => agent(`배치 검증: ${b.files.join(', ')}`, { agentType: 'qa-inspector', schema: VERDICT }))
```

**(b) 진행 상황을 보며 동적 재분배가 필요하면 → 퍼시스턴트:**
```
리더가 TaskCreate로 배치 작업 등록 (depends_on 포함)
→ Agent(name:"migrator-1..3") 스폰 → 완료 알림마다 결과 확인
→ 실패 배치는 SendMessage로 원인 확인 후 TaskUpdate로 재할당
→ 전체 완료 후 통합 테스트
```

## 예시 5: 웹툰 제작 — 생성-검증 (서브에이전트 순차)

**패턴:** 생성-검증 | **모드 근거:** 에이전트 2개, 결과 전달이 핵심, 루프 최대 2회 고정 — 가장 가벼운 모드로 충분

```
Phase 1: Agent(name:"artist") → 패널 생성 → _workspace/panels/
Phase 2: Agent(webtoon-reviewer 단발) → PASS/FIX/REDO 판정 → _workspace/review_report.md
Phase 3: REDO 패널만 SendMessage({to:"artist"})로 재생성 지시 (최대 2회 루프,
         artist가 컨텍스트를 유지하므로 "3번 패널만 구도 수정" 지시가 정확히 통한다)
재시도 정책: 2회 루프 후 강제 PASS, 전체의 50% 이상 REDO면 사용자에게 프롬프트 수정 제안
```

---

## 산출물 패턴 요약

- **에이전트 정의**: `프로젝트/.claude/agents/{name}.md` — 필수 섹션: 핵심 역할, 작업 원칙, 입력/출력 프로토콜, 재호출 지침, 에러 핸들링, 협업 (+퍼시스턴트면 통신 프로토콜, 워크플로우면 구조화 출력)
- **스킬**: `프로젝트/.claude/skills/{name}/SKILL.md` (+ references/, scripts/)
- **오케스트레이터**: 실행 모드 명시 필수. 템플릿: `orchestrator-template.md`
- **중간 산출물**: `_workspace/{phase}_{agent}_{artifact}.{ext}`, 보존 원칙
