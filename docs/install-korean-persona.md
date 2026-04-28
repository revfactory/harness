# 설치 가이드 — Korean Persona Injection

`korean-persona-search`, `korean-voice-adapter`, `korean-persona-harness` 3개 스킬을 **Claude Code**와 **Codex CLI** 두 런타임에 설치하는 방법.

두 런타임의 스킬 파일 포맷이 동일(`SKILL.md` + frontmatter + 본문 + `references/`/`scripts/`)이므로, 같은 소스를 양쪽에 그대로 설치할 수 있다.

## 의존성 (양 런타임 공통)

```bash
pip install huggingface_hub pyarrow
# 또는
uv pip install huggingface_hub pyarrow
```

스크립트는 lazy import 하므로 검색을 실제로 실행하기 직전에만 필요하다. 미설치 시 명확한 안내 메시지 출력.

## A. 한 줄 설치 (권장) — `install-korean-persona.sh`

리포 클론 후:

```bash
# Claude Code 프로젝트에 설치
./scripts/install-korean-persona.sh --target claude-code

# Codex (전역 ~/.codex/skills/)
./scripts/install-korean-persona.sh --target codex

# 둘 다
./scripts/install-korean-persona.sh --target both

# Codex skill-installer로 GitHub에서 직접 (포크에서 설치 예시)
./scripts/install-korean-persona.sh --target codex --from-github hongsw/harness

# 미리보기만
./scripts/install-korean-persona.sh --target both --dry-run
```

옵션:
- `--claude-dest DIR` Claude Code 대상 (기본 `./.claude/skills`)
- `--codex-dest DIR` Codex 대상 (기본 `${CODEX_HOME:-~/.codex}/skills`)
- `--ref BRANCH` `--from-github`와 함께. 기본 `main`
- `--skip-deps` 의존성 검사 생략
- `--dry-run` 실제 복사 없이 계획만 출력

## B. Claude Code — 플러그인 마켓플레이스로 설치

이 리포는 Claude Code 플러그인 패키지(`/.claude-plugin/`)를 포함한다. 플러그인이 머지·릴리스되면 사용자는:

```
/plugin add revfactory/harness
```

또는 포크에서:

```
/plugin add hongsw/harness
```

플러그인 설치 시 3개 신규 스킬 모두 자동 등록된다.

## C. Codex CLI — `skill-installer` 직접 사용

Codex는 `~/.codex/skills/.system/skill-installer/`를 통해 GitHub 리포의 스킬을 직접 설치한다:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
    --repo hongsw/harness \
    --ref main \
    --path skills/korean-persona-search \
    --path skills/korean-voice-adapter \
    --path skills/korean-persona-harness
```

설치 후 메시지: **"Restart Codex to pick up new skills."**

## D. 수동 설치 (참고)

리포 클론 후 디렉토리를 직접 복사:

**Claude Code (프로젝트 단위)**:
```bash
cp -R skills/korean-persona-search   path/to/your/project/.claude/skills/
cp -R skills/korean-voice-adapter    path/to/your/project/.claude/skills/
cp -R skills/korean-persona-harness  path/to/your/project/.claude/skills/
```

**Codex (전역)**:
```bash
mkdir -p ~/.codex/skills
cp -R skills/korean-persona-search ~/.codex/skills/
cp -R skills/korean-voice-adapter ~/.codex/skills/
cp -R skills/korean-persona-harness ~/.codex/skills/
```

## 데이터셋 캐시 (최초 1회)

설치 위치(`$SKILL_DIR`)에서:

```bash
# 전체 다운로드 (수 GB)
python3 $SKILL_DIR/korean-persona-search/scripts/download.py

# 빠른 테스트 (첫 1개 shard만)
python3 $SKILL_DIR/korean-persona-search/scripts/download.py --shards 1

# 캐시 상태 확인
python3 $SKILL_DIR/korean-persona-search/scripts/download.py --check
```

캐시 경로 기본: `~/.cache/korean-persona-search/`. 환경변수 `KOREAN_PERSONA_CACHE_DIR`로 변경.

> 💡 캐시는 **양 런타임이 공유**한다. 한 번 받으면 Claude Code/Codex 어디서나 같은 데이터 사용.

## 사용 — 양 런타임 공통

설치 + 캐시 준비 후:

```
한국어 페르소나로 푸드테크 스타트업 5인 팀 만들어줘 — PO, 디자이너, 백엔드 개발자, CS 리드, 마케터
```

`korean-persona-harness` 오케스트레이터가 트리거되어 5단계 파이프라인 실행. 산출물:

- **Claude Code**: 프로젝트의 `.claude/agents/{name}.md` 5개
- **Codex**: `~/.codex/agents/{name}.md` 5개 (전역) 또는 사용자 지정 경로

> 오케스트레이터의 출력 디렉토리는 자동 감지되며, 사용자가 명시적으로 경로를 지정하면 그곳에 저장된다.

## 트러블슈팅

| 증상 | 원인 / 해결 |
|------|------------|
| `[korean-persona-search] 누락된 의존성: pyarrow` | `pip install pyarrow` |
| `[error] 캐시 없음: ~/.cache/korean-persona-search/` | `download.py` 먼저 실행 |
| Codex가 새 스킬을 찾지 못함 | Codex 재시작 필요 |
| Claude Code가 새 스킬을 찾지 못함 | 새 세션 시작 또는 `/reload` |
| `결과 0건` | 필터 조건이 너무 좁음 — `references/filter-cookbook.md` 참조하여 완화 |
| Codex skill-installer 부재 | Codex CLI를 최신 버전으로 업데이트 (`codex --version`) |

## 제거

설치된 skill 디렉토리를 삭제:

```bash
# Codex
rm -rf ~/.codex/skills/korean-persona-{search,voice-adapter,harness}

# Claude Code (프로젝트)
rm -rf ./.claude/skills/korean-persona-{search,voice-adapter,harness}

# 데이터셋 캐시 (선택)
rm -rf ~/.cache/korean-persona-search
```

## 라이선스 참고

- 본 스킬: 부모 리포 (`harness`) 라이선스 따름 (Apache-2.0)
- 데이터셋: NVIDIA Nemotron-Personas-Korea **CC BY 4.0** — 상용 OK, 저작자 표기 필수
- 생성된 에이전트 정의 하단에 자동 attribution 삽입됨. 외부 공개 시 해당 표기 유지.
