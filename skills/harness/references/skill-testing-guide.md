# Skill Testing Guide

Systematic eval methodology for skills: write prompts → run test vs baseline → grade assertions → iterate.

## 1. Test Prompts
Use concrete, natural user queries with real parameters, constraints, and varied phrasing.
- **Good:** `"다운로드 폴더의 'Q4_매출_v2.xlsx'에서 C열(매출)과 D열(비용)로 영업이익률 열을 추가하고 내림차순 정렬해줘."`
- **Bad:** `"엑셀 파일 처리해줘."` (Too vague to evaluate).

Prepare 2–3 initial prompts: 1 standard case, 1 edge case, 1 composite/multistep case.

## 2. With-Skill vs Baseline
Run parallel evaluations to measure added value:
- **With-Skill:** Prompt executed with skill loaded. Output to `_workspace/iteration-N/eval-{name}/with_skill/`.
- **Baseline:** Same prompt executed without skill (or against pre-edit version). Output to `_workspace/iteration-N/eval-{name}/without_skill/`.

Capture `total_tokens` and `duration_ms` immediately upon subagent completion.

## 3. Objective Assertion Grading
Write deterministic, verifiable assertions:
- **Valid:** `"Column 'profit_margin_pct' exists at column E"`, `"Exit code is 0"`.
- **Invalid:** `"Output is well formatted"` (Subjective), `"File created"` (Too trivial).

Sample `grading.json`:
```json
{
  "expectations": [
    { "text": "profit margin column added", "passed": true, "evidence": "Column E contains calculated percentage" },
    { "text": "sorted descending by margin", "passed": true, "evidence": "Row 2 margin (35%) > Row 3 margin (28%)" }
  ],
  "summary": { "passed": 2, "failed": 0, "total": 2, "pass_rate": 1.0 }
}
```

## 4. Evaluator Roles
- **Grader:** Evaluates objective pass/fail criteria with explicit evidence.
- **Comparator:** Conducts blind A/B comparison between with-skill and baseline outputs.
- **Analyzer:** Detects non-discriminating assertions, high-variance evals, and token cost tradeoffs.

## 5. Iteration Cycle
1. Run test suite.
2. Review failed assertions and agent transcripts.
3. Apply generalized fixes to `SKILL.md` (avoid overfitting to one specific test).
4. Bundle recurring helper code into `scripts/`.
5. Retest in `_workspace/iteration-N+1/`.

## 6. Trigger Validation (20 Queries)
Evaluate semantic routing accuracy with 20 test queries:
- **10 Should-Trigger:** Diverse phrasing, implicit intents, technical and casual terms.
- **10 Should-NOT-Trigger (Near-Misses):** Adjacent domains, ambiguous keywords, overlapping tasks intended for other skills.

*Check for collisions:* Ensure should-trigger queries do not inadvertently activate unrelated skills.

## 7. Workspace Structure

```
{skill-name}-workspace/
├── iteration-1/
│   ├── eval-01-basic/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/     (outputs/, timing.json, grading.json)
│   │   └── without_skill/  (outputs/, timing.json, grading.json)
│   └── benchmark.json
└── iteration-2/
```
Never overwrite prior iteration directories. Retain runs for regression analysis.
