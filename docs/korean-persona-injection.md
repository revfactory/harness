# Korean Persona Injection — 한국어 페르소나 주입

`harness` 플러그인의 한국어·한국 문화 특화 분기. 임의 도메인의 에이전트 팀을 만들 때, 추상적 "전문가" 대신 **실재성 있는 한국어 페르소나**(Nemotron-Personas-Korea 100만 행 합성 데이터)를 동적 매핑하여 한국 업무 매너·존댓말·산업 어휘가 살아있는 에이전트 정의를 출력한다.

## 구성 요소

이 보강은 3개의 새 스킬로 구성된다 (기존 `harness` 스킬 비침습):

```
skills/
├── harness/                      # 기존 (변경 없음)
├── korean-persona-search/        # 신규 — 데이터셋 검색 스킬
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── download.py           # HF에서 Parquet shard 캐시
│   │   └── search.py             # Parquet predicate pushdown 필터 + 다양성 샘플링
│   └── references/
│       ├── schema.md             # 26개 필드 스키마
│       └── filter-cookbook.md    # 검색 패턴 예시
├── korean-voice-adapter/         # 신규 — 화법·업무문화 어댑터
│   ├── SKILL.md
│   └── references/
│       ├── honorifics.md         # 합쇼체/해요체 결정 매트릭스
│       ├── workplace-culture.md  # 보고 라인, 회의 매너, 세대·지역 보정
│       └── industry-tone.md      # 13개 산업 어휘 사전
└── korean-persona-harness/       # 신규 — 메타 오케스트레이터
    ├── SKILL.md
    └── references/
        └── agents/                # 5개 sub-agent 프롬프트 템플릿
            ├── scenario-analyst.md
            ├── persona-curator.md
            ├── voice-adapter.md
            ├── definition-builder.md
            └── diversity-qa.md
```

## 사용

```
사용자: 한국 푸드테크 스타트업의 신규 배달 앱을 위한 5인 페르소나 팀 만들어줘 — PO, 디자이너, 백엔드 개발자, CS 리드, 마케터
```

`korean-persona-harness` 오케스트레이터가 트리거되어:
1. **시나리오 분석** — 5개 역할 식별, 각 역할의 검색 사양 도출
2. **퍼소나 큐레이션** — `korean-persona-search`로 역할별 후보 검색, 다양성 보장하며 선별
3. **화법 어댑팅** — `korean-voice-adapter`로 각 페르소나에 합쇼/해요/캐주얼 톤 + 산업 어휘 입힘
4. **에이전트 빌드** — 5개 `.md` 파일 생성, 한국어 직무명을 영문 kebab-case로
5. **다양성 QA** — 성별/연령/지역/직업/톤 분포 점검, 편향 시 자동 회귀

산출물은 `.claude/agents/` 또는 사용자 지정 경로.

## 설치 (Claude Code + Codex CLI 양쪽)

스킬은 **두 런타임에서 동일하게 작동**한다 (SKILL.md 포맷 호환). 자세한 설치는 [install-korean-persona.md](./install-korean-persona.md) 참조.

**한 줄 설치**:
```bash
./scripts/install-korean-persona.sh --target both    # Claude Code + Codex 모두
./scripts/install-korean-persona.sh --target codex   # Codex만
./scripts/install-korean-persona.sh --target claude-code   # Claude Code만
```

**Codex skill-installer로 GitHub에서 직접**:
```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
    --repo hongsw/harness --ref main \
    --path skills/korean-persona-search \
    --path skills/korean-voice-adapter \
    --path skills/korean-persona-harness
```

## 사전 준비

```bash
# 의존성 (양 런타임 공통)
pip install huggingface_hub pyarrow

# 데이터셋 캐시 (수 GB, 최초 1회 — Claude Code/Codex 공유)
python3 $SKILL_DIR/korean-persona-search/scripts/download.py

# 빠른 테스트용
python3 $SKILL_DIR/korean-persona-search/scripts/download.py --shards 1
```

캐시 경로: `~/.cache/korean-persona-search/` (환경변수 `KOREAN_PERSONA_CACHE_DIR`로 변경).

## 일반 `harness`와의 관계

| 사용 시점 | 어떤 스킬 |
|----------|----------|
| 기술 아키텍처 (멀티 에이전트 설계, 리뷰어/빌더 등) | `harness` |
| 한국 사용자/시장 대상 페르소나 시뮬레이션, 인터뷰, 콘텐츠 팀 | `korean-persona-harness` |
| 둘 다 필요 | `harness`로 구조 잡고, `korean-persona-harness`로 페르소나 입히기 (또는 그 반대) |

`korean-persona-harness`는 `harness`의 상위 호환이 아니라 **분기**다. 두 스킬의 description이 구분되도록 작성되어 있어 자동 트리거 시 충돌은 드물지만, 사용자 의도가 모호하면 직접 명시하라.

## 라이선스 및 출처

페르소나 데이터: [NVIDIA Nemotron-Personas-Korea](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea) — **CC BY 4.0**.

생성된 모든 에이전트 정의의 하단 "Korean Persona Source" 섹션에 uuid + attribution이 자동 삽입된다. 에이전트 정의를 외부에 공유할 때 해당 표기를 유지하라.

## 한계

- **합성 데이터** — 실존 인물이 아니다. 윤리적/법적 이슈는 감소하지만, 통계적 분포가 한국의 *현실*을 반영하므로 희소한 직업·지역·연령 조합은 검색 결과가 비어있을 수 있다.
- **편향 인식** — 데이터셋이 인구 분포에 가까우므로 "30대 남성 IT 종사자"는 흔하고, "70대 여성 개발자"는 거의 없다. QA가 잡지만, 시나리오 설계 시 미리 인식하라.
- **언어 한정** — 한국어 화자만. 영어/일본어 페르소나 필요 시 별도 데이터셋·스킬 필요.
