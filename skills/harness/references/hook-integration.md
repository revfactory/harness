# Hook 통합 가이드 — Memo 패턴 자동화 (선택)

`SessionStart`/`PreCompact`/`Stop` hook을 활용하여 Memo 패턴(`memo-pattern.md`)의 status 운영을 자동화하는 가이드. **사용자 명시 승인 없이 적용하지 않는다.** harness 스킬이 자동으로 settings.json을 패치하지 않으며, 이 문서는 사용자가 검토·복사하기 위한 참고 자료다.

## 목차

1. [언제 이 문서를 사용하는가](#언제-이-문서를-사용하는가)
2. [중요 경고](#중요-경고)
3. [Hook 메커니즘 요약](#hook-메커니즘-요약)
4. [패턴 1 — SessionStart로 status 자동 주입](#패턴-1)
5. [패턴 2 — PreCompact로 status 강제 갱신](#패턴-2)
6. [패턴 3 — Stop으로 마지막 동기화](#패턴-3)
7. [settings.json 통합 예시](#settingsjson-통합-예시)
8. [Windows / Bash / 프록시 환경 주의사항](#환경-주의사항)
9. [검토 체크리스트](#검토-체크리스트)
10. [Hook 없이도 동작하는가](#hook-없이도-동작하는가)

---

## 언제 이 문서를 사용하는가

다음 두 조건을 **모두** 만족할 때만 hook 적용을 사용자에게 *제안*한다:

1. Memo 패턴(`memo-pattern.md`)이 적용된 하네스를 생성했다.
2. 사용자가 명시적으로 "자동으로 status를 읽어줘", "세션 재개 자동화", "컴팩트 시 자동 저장" 같은 요구를 했다.

위 두 조건을 만족하지 않으면 이 문서를 끌어들이지 않는다. **자동화는 위험한 책임**이며 default가 아니다.

---

## 중요 경고

| 위험 | 설명 |
|------|------|
| **settings.json 직접 수정 금지** | harness는 절대 사용자 settings.json을 직접 수정하지 않는다. `update-config` 스킬에 위임하거나, 사용자에게 패치 텍스트를 보여주고 본인이 적용하도록 한다. |
| **hook은 사용자 환경에서 실행됨** | 잘못된 hook은 모든 세션 시작·도구 호출에 영향을 미친다. 무한 루프·실패 시 차단도 가능. |
| **hook 출력은 컨텍스트에 주입됨** | 큰 출력은 매 세션마다 토큰을 잡아먹는다. status.md를 통째로 주입하지 말고 *공유 헤더만* 주입할 것. |
| **secrets/credentials 노출 위험** | hook 스크립트가 cwd 기반으로 동작할 때, `.env` 등을 실수로 읽지 않도록 경로를 명시적으로 제한. |
| **Windows 경로 차이** | bash 스크립트는 Unix 경로(`/`)를 쓰지만 사용자 환경은 Windows. `$CLAUDE_PROJECT_DIR`을 항상 따옴표로 감싸고, 경로 구분자에 주의. |

---

## Hook 메커니즘 요약

Claude Code의 hook은 settings.json의 `hooks` 객체에서 정의한다. 각 hook은 이벤트별로 trigger되며, stdin으로 JSON을 받고 stdout/exit code로 응답한다.

| 이벤트 | 발생 시점 | Memo 패턴 활용 |
|--------|---------|---------------|
| `SessionStart` (source: `startup`/`resume`/`clear`/`compact`) | 세션 시작 시 | status.md를 컨텍스트에 자동 주입 |
| `PreCompact` | 자동·수동 컴팩트 직전 | 강제로 자기 슬롯 갱신 후 컴팩트 진행 |
| `PostCompact` | 컴팩트 완료 직후 | (선택) 컴팩트 후 status 재로드 |
| `Stop` | Claude가 한 턴 응답을 마쳤을 때 | (선택) 마지막 동기화 |

각 hook은 다음 환경 변수를 받는다:
- `$CLAUDE_PROJECT_DIR` — 프로젝트 루트
- `$CLAUDE_PLUGIN_ROOT` / `$CLAUDE_PLUGIN_DATA` — plugin 사용 시
- `$CLAUDE_ENV_FILE` — SessionStart에서 환경 변수를 영속하려면 이 경로에 KEY=VALUE 형식으로 기록

stdin JSON 출력으로는 다음 필드를 활용:
```json
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "...status.md 내용..."
  }
}
```
`additionalContext`는 컨텍스트에 주입되는 텍스트다. 이 필드를 통해 status.md를 자동 로드할 수 있다.

---

## 패턴 1

**SessionStart 시 `.harness/status.md`(공유 헤더)를 컨텍스트에 주입.**

`<프로젝트>/.claude/hooks/session_start_status.sh` (예시):

```bash
#!/usr/bin/env bash
set -euo pipefail

STATUS_FILE="${CLAUDE_PROJECT_DIR}/.harness/status.md"

if [[ ! -f "$STATUS_FILE" ]]; then
  exit 0
fi

# 공유 헤더만 주입. 슬롯은 에이전트가 필요 시 직접 Read.
CONTENT=$(head -n 80 "$STATUS_FILE")

cat <<EOF
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "[Memo Pattern] .harness/status.md 공유 헤더가 자동 주입되었습니다. 자세한 슬롯은 .harness/agents/{name}.md를 직접 Read하세요.\n\n---\n${CONTENT}\n---"
  }
}
EOF
```

**원칙:**
- 공유 헤더만 주입. 슬롯 전체를 자동 주입하지 않는다 (토큰 폭증).
- 80줄 정도로 잘라 안전 가드.
- 파일이 없으면 조용히 종료 (Memo 미적용 프로젝트 보호).

---

## 패턴 2

**PreCompact 직전에 자기 슬롯의 핵심을 강제 append.**

이 패턴은 hook만으로 처리하기 어렵다. 컴팩트는 *Claude의 결정*이고 hook은 외부 스크립트이기 때문에, 슬롯에 *지금 무엇을 했는지*를 모르는 상태로 호출된다.

따라서 다음 두 가지 중 하나로 처리한다:

**옵션 A — Hook은 알림만, 갱신은 에이전트가:**
PreCompact hook이 `additionalContext`로 "곧 컴팩트가 일어납니다. 자기 슬롯에 핵심 진척을 1줄 append하세요" 메시지를 컨텍스트에 주입한다. Claude(에이전트)가 그 메시지를 보고 직접 갱신한다.

```bash
#!/usr/bin/env bash
cat <<'EOF'
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "[Memo Pattern] 곧 컨텍스트 컴팩트가 발생합니다. 본인이 에이전트라면 .harness/agents/{self}.md의 ## Accomplishments에 마지막 진척을 1줄 append한 뒤 진행하세요."
  }
}
EOF
```

**옵션 B — Hook이 자동 timestamp 한 줄 추가:**
모든 활성 슬롯에 "{timestamp} pre-compact triggered" 한 줄을 자동 append. 정보량은 적지만 손실 방지에는 도움.

옵션 A가 더 강력하다. 옵션 B는 덮어쓰기 위험을 낮추는 안전망.

---

## 패턴 3

**Stop hook으로 마지막 동기화 (선택).**

Claude가 한 턴 응답을 마쳤을 때 마지막으로 status를 점검할 기회를 준다. 이 패턴은 토큰 비용이 추가로 발생할 수 있으므로 사용자가 명시적으로 원할 때만.

```bash
#!/usr/bin/env bash
# 매 턴 종료 시 status.md의 Last Updated만 새로 찍는다.
# 본문 갱신은 에이전트가 마일스톤 시점에 직접.
STATUS_FILE="${CLAUDE_PROJECT_DIR}/.harness/status.md"
[[ -f "$STATUS_FILE" ]] || exit 0
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# In-place 단순 변경(macOS/Linux 차이 회피용 대체)
tmp=$(mktemp)
sed "s/^# Project Status (Last Updated: .*/# Project Status (Last Updated: ${TS})/" "$STATUS_FILE" > "$tmp" && mv "$tmp" "$STATUS_FILE"
exit 0
```

이 hook은 *어떤 컨텍스트도 주입하지 않는다*. timestamp만 갱신.

---

## settings.json 통합 예시

사용자에게 보여줄 패치(이미 사용자의 settings.json이 있다고 가정):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "resume|startup|clear",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session_start_status.sh"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre_compact_status.sh"
          }
        ]
      }
    ]
  }
}
```

> 이 패치는 **사용자가 직접 적용**한다. harness/Claude는 절대 settings.json에 자동 쓰지 않는다. 사용자가 자동 적용을 원하면 `update-config` 스킬을 호출하라고 안내한다.

---

## 환경 주의사항

| 환경 | 주의점 |
|------|--------|
| Windows + Git Bash | hook 스크립트는 `bash` 스크립트로 작성(POSIX). `.sh` 확장자 유지. CRLF 대신 LF 라인엔딩 |
| Windows 경로 | `$CLAUDE_PROJECT_DIR`이 `C:/Users/...` 형태로 들어옴. `head`/`sed`는 forward slash 그대로 사용 가능 |
| Proxy 환경 (사용자 환경) | hook 스크립트 자체는 네트워크를 쓰지 않으므로 proxy 영향 없음. 단, hook에서 git 등을 쓴다면 사용자 git config의 proxy를 따름 |
| Permissions 환경 | hook 스크립트는 `Bash` 권한과 별개로 hook 시스템이 직접 실행. 허용 목록과 무관하게 동작하나, Bash 도구 호출은 별도 권한 |
| 무한 루프 방지 | hook 안에서 Claude를 호출하지 말 것. 외부 도구만 사용 |

---

## 검토 체크리스트

사용자에게 hook 적용을 제안하기 전 본인(Claude/하네스)이 점검:

- [ ] Memo 패턴이 실제 적용된 하네스인가?
- [ ] hook 스크립트가 `secret`/`credential`/`*.env` 파일을 읽지 않도록 경로 제한되었는가?
- [ ] `additionalContext`가 80줄 이하로 잘려 있는가?
- [ ] `set -euo pipefail` 등으로 hook 실패 시 빠르게 종료하는가?
- [ ] 파일이 없을 때 조용히 종료(`exit 0`)하는가?
- [ ] hook 동작을 사용자가 끌 수 있는 방법(주석 처리/조건 변수)이 있는가?
- [ ] 사용자에게 패치 텍스트를 보여주고 명시적 승인을 받았는가?

---

## Hook 없이도 동작하는가

**예.** Memo 패턴 자체는 hook 없이도 동작한다.

- 에이전트 정의에 "작업 시작 시 .harness/status.md를 Read" 지침이 있으면, hook 없이도 에이전트가 직접 읽는다.
- PreCompact 자동 갱신이 없어도, 에이전트가 마일스톤 시점에 자기 슬롯에 append한다.
- hook은 *자동화의 편의*이지 *기능의 필수 조건*이 아니다.

따라서 hook 적용은 **있으면 좋고 없어도 동작**하는 옵션. 사용자가 망설이면 끄고 시작하고, 익숙해지면 켜는 단계적 도입이 안전하다.

---

## 자동 적용 요청 시 처리

사용자가 "settings.json에 자동으로 적용해줘"라고 명시 요청하면:
1. 패치 내용을 화면에 보여주고 1번 더 확인을 받는다.
2. `update-config` 스킬을 호출하여 적용한다 (harness가 직접 settings.json을 쓰지 않는다).
3. 적용 후 hook 스크립트(`<프로젝트>/.claude/hooks/*.sh`)는 사용자가 별도로 작성하도록 안내한다 (이 문서의 예시 코드를 그대로 사용 가능).
