# Team Examples

These examples mirror revfactory/harness team designs, translated to Codex-native skills and `_workspace` handoffs.

## Deep Research

Pattern: Fan-out/Fan-in.

Skills:

- `research-source-finder`
- `research-evidence-reviewer`
- `research-synthesizer`
- `research-qa-reviewer`

Handoffs:

- `_workspace/01_source_finder_sources.md`
- `_workspace/02_evidence_reviewer_notes.md`
- `_workspace/03_synthesizer_report.md`
- `_workspace/04_qa_findings.md`

## Website Development

Pattern: Pipeline + Producer-Reviewer.

Skills:

- `web-product-planner`
- `web-frontend-builder`
- `web-backend-builder`
- `web-qa-reviewer`

Handoffs:

- plan -> implementation -> QA -> final summary

## Code Review

Pattern: Fan-out/Fan-in.

Skills:

- `review-architecture`
- `review-security`
- `review-performance`
- `review-tests`
- `review-synthesizer`

Each reviewer writes a separate finding file, then synthesizer merges findings by severity.

## Documentation Generation

Pattern: Pipeline.

Skills:

- `docs-api-analyzer`
- `docs-writer`
- `docs-example-author`
- `docs-reviewer`

The orchestrator preserves source references and requires review before final docs are delivered.

## Release Workflow

Pattern: Supervisor + Producer-Reviewer.

Skills:

- `release-coordinator`
- `release-packager`
- `release-notes-writer`
- `release-qa-reviewer`

The coordinator owns destructive gates, version checks, artifact checks, and final user confirmation.
