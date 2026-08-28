# Contributing to Harness

기여를 환영합니다. 이 문서는 짧습니다 — 규칙보다 원칙을 따릅니다.

## 원칙

1. **스킬은 에이전트를 위한 지시서다.** 사용자용 설명서·마케팅 문구·Claude가 이미 아는 일반 지식은 스킬에 넣지 않는다.
2. **컨텍스트는 공공재다.** SKILL.md 본문 500줄 이내, 세부는 `references/`로. 모든 문장이 토큰 비용을 정당화해야 한다.
3. **Why를 설명한다.** "ALWAYS/NEVER" 대신 이유를 쓴다. 이유를 알면 엣지 케이스에서도 올바르게 판단한다.
4. **현행 런타임만 참조한다.** 실험 플래그, 제거된 API(`TeamCreate` 등), 특정 모델 하드코딩을 PR에 넣지 않는다. 런타임 변경으로 문서가 깨지면 그것이 최우선 수정 대상이다.

## PR 체크리스트

- [ ] 변경이 SKILL.md와 관련 references 간에 일관되는가 (한쪽만 고치지 않았는가)
- [ ] 트리거에 영향을 주는 description 변경이면 should-trigger / near-miss 쿼리로 검증했는가
- [ ] CHANGELOG.md에 항목을 추가했는가
- [ ] 버전 정합성: `plugin.json` = `marketplace.json` = README 뱃지

## 이슈

- 버그: 재현 프롬프트 + 기대/실제 동작 + `claude --version`
- 런타임 호환성 깨짐: `compat` 라벨 — 최우선 처리

## 응답 목표

- PR 1차 응답: 72시간 이내
- Issue 트리아지: 48시간 이내

커뮤니티 약속이며 유료 SLA가 아닙니다.
