# Skill Writing Guide

Best practices for writing modular, token-efficient skills.

## 1. Description Rules (Trigger Engine)
The YAML frontmatter `description` is the only trigger mechanism. Claude selects skills based solely on name and description.
- Keep description in the user's primary working language.
- State core capabilities **and** explicit triggering conditions.
- Specify boundary conditions against near-miss cases.
- Use assertive phrasing (Claude triggers conservatively).

### Examples
```yaml
# Good: Concrete actions, keywords, and boundaries
description: "PDF 텍스트/표 추출, 병합, 분할, 회전, 워터마크, OCR 등 모든 PDF 조작. .pdf 파일 언급이나 PDF 산출물 생성 요청 시 반드시 이 스킬을 사용할 것. 단순 요약이 아닌 구조적 편집/추출 작업에 사용."

# Bad: Vague, no trigger scenarios
description: "PDF 파일을 처리하는 유용한 스킬."
```

## 2. Body Writing Style
- **Explain why, not just what:** Providing rationale helps the model generalize to edge cases that static rules cannot anticipate.
- **Generalize principles:** Address the underlying failure mode rather than patching one specific input instance.
- **Use imperative voice:** Skills are instruction sets, not documentation.
- **Token efficiency:** Omit common background knowledge. Favor short templates and tables over descriptive paragraphs.

## 3. Structural Design

### Explicit Output Templates
Provide the exact markdown/JSON structure when output format matters:
```markdown
## Output Schema
# [Document Title]
## Executive Summary
## Key Findings
- [Point 1]
## Action Items
```

### Progressive Disclosure
Keep `SKILL.md` under 300 lines. Offload conditional details to `references/`:
```
skill-directory/
├── SKILL.md            # Entry point & core workflow
├── scripts/            # Deterministic, reusable execution scripts
└── references/         # Conditionally loaded deep-dive guides
    ├── topic-a.md
    └── topic-b.md
```

## 4. Script Bundling Criteria
Move logic to `scripts/` when:
- Multiple subagents write the same bash/python helper during execution.
- Complex data parsing requires exact, deterministic execution.
- Shell commands involve long multi-line piping prone to hallucination.

## 5. Evaluation Data Schemas

Standard JSON schemas for skill testing and benchmarking.

### `eval_metadata.json`
```json
{
  "eval_id": 1,
  "eval_name": "table-extraction-multi-page",
  "prompt": "Extract all tables from doc.pdf into clean CSV format",
  "assertions": [
    "Output contains 3 table blocks",
    "Headers match original columns"
  ]
}
```

### `grading.json`
Use exact keys: `text`, `passed`, `evidence`.
```json
{
  "expectations": [
    {
      "text": "Header contains 'Revenue'",
      "passed": true,
      "evidence": "Column 2 header is 'Revenue (USD)'"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

### `timing.json`
Capture immediately upon agent completion:
```json
{
  "total_tokens": 12450,
  "duration_ms": 5200,
  "total_duration_seconds": 5.2
}
```

## 6. What to Exclude
- General tutorials or introductory explanations.
- Version change logs and installation instructions.
- Redundant guidelines on standard tools that Claude already masters.
