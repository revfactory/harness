---
inclusion: always
---

# 하네스 (Kiro 포팅)

**목표:** 도메인/프로젝트에 맞는 전문 Kiro 에이전트(`.kiro/agents/*.json`)와 스킬(`.kiro/skills/`)을 설계·생성하는 메타 스킬을 운영한다.

**트리거:** "하네스 구성/구축/설계", "에이전트 팀/세트 만들어줘", "에이전트/스킬 추가·수정", "하네스 점검/감사/현황/동기화", "하네스 업데이트/재구성" 등의 요청 시 `harness` 스킬(`.kiro/skills/harness/SKILL.md`)을 사용하라. 단순 질문은 직접 응답 가능.

**참고:** 아키텍처 패턴·예시 전문은 클론된 원본 `skills/harness/references/`에 있다. Claude Code 전용 도구(TeamCreate/SendMessage 등)는 Kiro에 없으므로 harness 스킬의 "Kiro 매핑" 표에 따라 치환해 읽는다.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-06-11 | 초기 구성 (Claude Code 하네스 → Kiro 네이티브 포팅) | .kiro/skills/harness, .kiro/steering/harness.md | Kiro에서 하네스 사용 |
