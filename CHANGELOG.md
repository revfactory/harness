# Changelog

이 프로젝트는 [Semantic Versioning](https://semver.org/)을 따릅니다.

## [Unreleased]

### Added

- **Korean Persona Injection** (3개 신규 스킬, 비침습) — `harness`의 한국어·한국 문화 분기. 임의 도메인 에이전트 팀에 NVIDIA Nemotron-Personas-Korea(100만 행, CC BY 4.0) 데이터셋을 동적 매핑하여 한국 업무 매너·존댓말·산업 어휘가 살아있는 페르소나 주입.
  - `skills/korean-persona-search/` — Parquet predicate pushdown 필터 + 다양성 샘플링. 스크립트 `download.py` (HF 캐시 다운로드), `search.py` (다축 필터·정규화 카드 출력). 26개 필드 스키마, 13개 산업 매핑 cookbook 동봉.
  - `skills/korean-voice-adapter/` — 합쇼체/해요체 매트릭스, 한국 직장 문화(보고 라인·회의 매너·세대·지역 보정), 13개 산업 어휘 사전.
  - `skills/korean-persona-harness/` — 메타 오케스트레이터 (서브 에이전트 5인 파이프라인). `references/agents/`에 시나리오 분석가, 퍼소나 큐레이터, 화법 어댑터, 에이전트 빌더, 다양성 QA 프롬프트 템플릿.
- **`docs/korean-persona-injection.md`** — 통합 사용 가이드.
- 의존성: `huggingface_hub`, `pyarrow` (lazy import + 누락 시 명확한 설치 안내).

### Notes

- 기존 `harness` 스킬은 변경 없음. 두 스킬은 description으로 자동 트리거 분기.
- 데이터 라이선스 CC BY 4.0 — 생성된 모든 에이전트 정의 하단에 uuid + attribution 자동 삽입.
- **Codex CLI 런타임 호환** — SKILL.md 포맷이 Claude Code와 Codex 양쪽에 동일하게 적용. 설치 스크립트 `scripts/install-korean-persona.sh` 추가 (`--target codex|claude-code|both`). Codex `skill-installer`로 GitHub 직접 설치 경로 지원. 설치 가이드 `docs/install-korean-persona.md` 신설.

## [1.2.1] - 2026-04-18

### Fixed

- **버전 정합성 동기화** — README.md / README_KO.md / README_JA.md 뱃지가 `v1.0.1`, `.claude-plugin/marketplace.json`이 `1.1.0`, `.claude-plugin/plugin.json`이 `1.2.0`으로 3중 불일치 → 모두 **v1.2.0**으로 통일 (plugin.json 기준)
- **태그드 릴리스 0건 상태 해소 준비** — v1.0.0 / v1.0.1 / v1.1.0 / v1.2.0 소급 태그 계획 작성 (`_workspace/release/audit-2026-04-18.md` §4 참조)

### Added

- **포지셔닝 선언: "harness factory"** — README 상단에 카테고리 자기 규정 문구를 도입. "에이전트 + 스킬을 도메인별로 찍어내는 하네스 팩토리"로 카테고리 선점 (단일 에이전트/프롬프트 프레임워크 대비 차별화)
- **CONTRIBUTING.md** — 기여 가이드 및 SLA 명시 (PR 1차 응답 72h, Issue triage 48h). 커뮤니티 온보딩 장벽 해소
- **docs/ 디렉토리** — 장기 문서(아키텍처, 마이그레이션, 패턴 카탈로그) 이전 공간 신설. README 비대화 방지 및 검색성 향상
- **Issue #3 응답 정책** — 커뮤니티 이슈에 대한 공식 응답 템플릿 및 트리아지 프로세스 추가

### Changed

- `.claude-plugin/marketplace.json` version: `1.1.0` → `1.2.0`
- README 뱃지 (EN/KO/JA 3종): `Version-1.0.1` → `Version-1.2.0`
- **`.claude-plugin/plugin.json` description 재작성** — `"Agent Team & Skill Architect — Meta-skill that designs..."` → `"The team-architecture factory for Claude Code — a meta-skill that turns a domain description into an agent team and the skills they use, with six pre-defined team-architecture patterns..."` (EN+KO 병기, L3 Meta-Factory 포지셔닝 반영)
- **`.claude-plugin/plugin.json` keywords 확장** — 5개 → 17개 (`harness-factory`, `team-architecture-factory`, `claude-code-plugin`, `agent-scaffolding`, `multi-agent`, 6패턴 키워드 6종 추가)

## [1.2.0] - 2026-04-08

### Changed

- **CLAUDE.md 등록 정책 간소화 (중복 제거)** — Phase 5-4 "컨텍스트 등록"을 "포인터 등록"으로 전환. 에이전트 목록·스킬 목록·디렉토리 구조·실행 규칙 상세를 CLAUDE.md에서 제거하고 **트리거 규칙 + 변경 이력**만 남김. 에이전트/스킬 목록은 `.claude/agents/`, `.claude/skills/` 및 오케스트레이터 스킬에서 단일 출처로 관리
- **Phase 3/4 임시 동기화 단계 삭제** — CLAUDE.md 동기화 부담을 줄이기 위해 Phase 3/4의 임시 동기화 지시 제거. 최종 포인터 등록은 Phase 5-4에서 1회만 수행
- **핵심 원칙 3번 재정의** — "CLAUDE.md에 하네스 컨텍스트를 등록한다" → "CLAUDE.md에 하네스 포인터를 등록한다"
- **CLAUDE.md vs 오케스트레이터 역할 분담표 삭제** — 포인터 정책으로 단순화되어 표 자체가 불필요해짐

### Added

- **Phase 2-1: 하이브리드 실행 모드** — 에이전트 팀 / 서브 에이전트에 더해 Phase별로 모드를 섞는 하이브리드 패턴 추가. 자주 쓰이는 조합(병렬 수집→합의 통합, 팀 생성→검증, Phase 간 팀 재구성) 명시
- **Phase 2-1 실행 모드 비교표** — 팀/서브/하이브리드 3종 특성 및 의사결정 순서 3단계 제공
- **Phase 5-0 하이브리드 오케스트레이터 패턴** — 하이브리드 구성 시 각 Phase 상단에 실행 모드를 명시하는 규칙
- **Phase 5-1 반환값 기반 데이터 전달** — 서브 에이전트 모드 전용 데이터 전달 전략 추가 (기존 메시지/태스크/파일 + 반환값)
- **Phase 5-1 권장 조합 (서브/하이브리드)** — 팀 모드 외 서브 모드와 하이브리드에서의 데이터 전달 권장 조합 명시

## [1.1.0] - 2026-04-05

### Added

- **Phase 0: 현황 감사** — 트리거 시 기존 하네스 상태를 먼저 확인하고 신규 구축/기존 확장/운영·유지보수 3분기로 라우팅
- **기존 확장 Phase 선택 매트릭스** — 에이전트 추가/스킬 추가/아키텍처 변경별 필요 Phase를 명시한 결정표
- **Phase 3/4 CLAUDE.md 임시 동기화** — 에이전트·스킬 생성 직후 CLAUDE.md에 즉시 반영 (세션 중단 내성)
- **Phase 5-4: CLAUDE.md 하네스 컨텍스트 등록** — 에이전트 팀 구조·스킬 목록·실행 규칙·디렉토리 구조·변경 이력을 기록. CLAUDE.md vs 오케스트레이터 역할 분담표 포함
- **Phase 5-5: 후속 작업 지원** — 오케스트레이터 description에 후속 키워드 필수 포함, Phase 0 컨텍스트 확인 단계로 초기/부분재실행/새실행 자동 판별
- **Phase 5 오케스트레이터 수정 경로** — 기존 확장 시 오케스트레이터를 새로 만들지 않고 수정하는 가이드
- **Phase 7: 하네스 진화 메커니즘** — 실행 후 피드백 수집 → 피드백 유형별 수정 대상 매핑 → 변경 이력 기록 → 자동 진화 트리거
- **Phase 7-5: 운영/유지보수 워크플로우** — 현황 감사→점진적 수정→CLAUDE.md 동기화→변경 검증 4단계
- **description에 운영/유지보수 트리거** — '하네스 점검', '하네스 감사', '하네스 현황', '에이전트/스킬 동기화' 키워드
- **산출물 체크리스트 강화** — CLAUDE.md 동기화 완료, 변경 이력 기록, Phase 0 컨텍스트 확인 항목 추가
- 오케스트레이터 템플릿에 Phase 0 (컨텍스트 확인) 추가 — 에이전트 팀/서브 에이전트 모드 모두 적용
- 오케스트레이터 description 템플릿에 후속 작업 키워드 패턴 포함

### Changed

- 핵심 원칙 2개 → 4개로 확장 (CLAUDE.md 등록, 진화 시스템 추가)
- **"진화 로그" → "변경 이력" 통일** — 이름과 스키마(4컬럼: 날짜/변경내용/대상/사유)를 전 섹션에서 일원화
- **Phase 1 Step 3** — Phase 0 감사 결과를 기반으로 충돌 분석하도록 변경 (중복 제거)
- **5-4 CLAUDE.md 템플릿 코드 블록** — 중첩 렌더링 깨짐 수정 (3백틱→4백틱)
- **역할 분담표 확장** — 스킬 목록, 디렉토리 구조, 변경 이력 행 추가
- **오케스트레이터 템플릿** — Phase 0 컨텍스트 확인 단계, 후속 작업 키워드 가이드 추가

## [1.0.1] - 2026-03-28

### Changed

- SKILL.md ↔ references 간 중복 내용 제거 (330줄 → 285줄)
  - Phase 2-1: 실행 모드 비교표/불릿 → 핵심 원칙 + agent-design-patterns.md 포인터
  - Phase 2-3: 에이전트 분리 기준 불릿 → 4축 요약 + agent-design-patterns.md 포인터
  - Phase 3: 에이전트 정의 템플릿 코드블록 → 필수 섹션 나열 + references 포인터
  - Phase 5-2: 에러 핸들링 5행 테이블 → 핵심 원칙 + orchestrator-template.md 포인터

## [1.0.0] - 2026-03-27

### Added

- 6 Phase 워크플로우 기반 하네스 구성 메타 스킬
- 6가지 에이전트 아키텍처 패턴 (파이프라인, 팬아웃/팬인, 전문가 풀, 생성-검증, 감독자, 계층적 위임)
- 에이전트 팀 / 서브 에이전트 실행 모드 지원
- Progressive Disclosure 기반 스킬 생성 가이드
- 오케스트레이터 템플릿 (에이전트 팀 모드 + 서브 에이전트 모드)
- QA 에이전트 통합 가이드 (실제 프로젝트 7개 버그 사례 기반)
- 스킬 테스트/평가 방법론 (With-skill vs Without-skill 비교)
- 실전 팀 구성 예시 5종 (리서치, 소설, 웹툰, 코드리뷰, 마이그레이션)
