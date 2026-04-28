#!/usr/bin/env bash
# install-korean-persona.sh — Korean Persona Injection 스킬 3종을 Claude Code 또는 Codex CLI에 설치
#
# 사용법:
#   ./scripts/install-korean-persona.sh --target codex        # ~/.codex/skills/ 에 설치
#   ./scripts/install-korean-persona.sh --target claude-code  # 현재 프로젝트 .claude/skills/ 에 설치
#   ./scripts/install-korean-persona.sh --target both
#   ./scripts/install-korean-persona.sh --target codex --from-github hongsw/harness
#
# 옵션:
#   --target {codex|claude-code|both}   설치 대상 (필수)
#   --from-github OWNER/REPO            GitHub에서 직접 설치 (Codex skill-installer 사용)
#   --ref BRANCH                        --from-github 와 함께. 기본 main
#   --claude-dest DIR                   Claude Code 설치 경로 (기본: ./.claude/skills)
#   --codex-dest DIR                    Codex 설치 경로 (기본: ${CODEX_HOME:-$HOME/.codex}/skills)
#   --skip-deps                         의존성 검사 생략
#   --dry-run                           실제 복사 없이 실행 계획만 출력
#   -h | --help                         도움말

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAMES=(korean-persona-search korean-voice-adapter korean-persona-harness)

TARGET=""
FROM_GITHUB=""
REF="main"
CLAUDE_DEST=""
CODEX_DEST=""
SKIP_DEPS=0
DRY_RUN=0

usage() {
    sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target) TARGET="$2"; shift 2 ;;
        --from-github) FROM_GITHUB="$2"; shift 2 ;;
        --ref) REF="$2"; shift 2 ;;
        --claude-dest) CLAUDE_DEST="$2"; shift 2 ;;
        --codex-dest) CODEX_DEST="$2"; shift 2 ;;
        --skip-deps) SKIP_DEPS=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done

if [[ -z "$TARGET" ]]; then
    echo "[error] --target 필요 (codex | claude-code | both)" >&2
    exit 2
fi

CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_DEST="${CLAUDE_DEST:-./.claude/skills}"
CODEX_DEST="${CODEX_DEST:-$CODEX_HOME_DIR/skills}"

run() {
    if [[ $DRY_RUN -eq 1 ]]; then
        echo "[dry-run] $*"
    else
        eval "$@"
    fi
}

check_deps() {
    [[ $SKIP_DEPS -eq 1 ]] && return 0
    local missing=()
    if ! command -v python3 >/dev/null 2>&1; then
        missing+=(python3)
    fi
    if ! python3 -c "import huggingface_hub, pyarrow" 2>/dev/null; then
        echo "[warn] Python 의존성 미설치: huggingface_hub, pyarrow"
        echo "       pip install huggingface_hub pyarrow"
        echo "       (또는) uv pip install huggingface_hub pyarrow"
        echo "       --skip-deps 로 이 검사를 건너뛸 수 있습니다."
    fi
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "[error] 누락: ${missing[*]}" >&2
        exit 1
    fi
}

install_local() {
    local dest_root="$1" label="$2"
    echo "[install:$label] dest=$dest_root"
    run "mkdir -p \"$dest_root\""
    for name in "${SKILL_NAMES[@]}"; do
        local src="$REPO_ROOT/skills/$name"
        local dst="$dest_root/$name"
        if [[ ! -d "$src" ]]; then
            echo "[error] 소스 부재: $src" >&2
            exit 1
        fi
        if [[ -e "$dst" ]]; then
            echo "[install:$label] 이미 존재 → 갱신: $dst"
            run "rm -rf \"$dst\""
        fi
        run "cp -R \"$src\" \"$dst\""
        echo "[install:$label] OK $name → $dst"
    done
}

install_codex_via_installer() {
    local repo="$1"
    local installer="$CODEX_HOME_DIR/skills/.system/skill-installer/scripts/install-skill-from-github.py"
    if [[ ! -x "$installer" && ! -f "$installer" ]]; then
        echo "[error] Codex skill-installer를 찾을 수 없습니다: $installer" >&2
        echo "        Codex CLI가 설치되어 있어야 합니다 (https://github.com/openai/codex)." >&2
        exit 1
    fi
    echo "[install:codex-gh] repo=$repo ref=$REF"
    local args=(--repo "$repo" --ref "$REF")
    for name in "${SKILL_NAMES[@]}"; do
        args+=(--path "skills/$name")
    done
    run "python3 \"$installer\" ${args[*]@Q}"
}

main() {
    check_deps

    case "$TARGET" in
        claude-code)
            install_local "$CLAUDE_DEST" "claude-code"
            ;;
        codex)
            if [[ -n "$FROM_GITHUB" ]]; then
                install_codex_via_installer "$FROM_GITHUB"
            else
                install_local "$CODEX_DEST" "codex"
            fi
            ;;
        both)
            install_local "$CLAUDE_DEST" "claude-code"
            if [[ -n "$FROM_GITHUB" ]]; then
                install_codex_via_installer "$FROM_GITHUB"
            else
                install_local "$CODEX_DEST" "codex"
            fi
            ;;
        *)
            echo "[error] 알 수 없는 --target: $TARGET" >&2
            exit 2
            ;;
    esac

    cat <<EOF

[done] 설치 완료.

다음 단계:
  1. 데이터셋 캐시 다운로드 (최초 1회, 수 GB):
       python3 \$DEST/korean-persona-search/scripts/download.py
     (개발 테스트용으론 --shards 1)
  2. 런타임 재시작:
       - Claude Code: 새 세션 시작 또는 /reload
       - Codex: 'Restart Codex to pick up new skills.'
  3. 사용 예: 한국어 페르소나로 5인 푸드테크 팀 만들어줘
EOF
}

main "$@"
