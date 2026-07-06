# QA Specialist Guide

Use this guide when a generated harness needs a reviewer or QA specialist.

## When To Add QA

Add a QA/reviewer skill when the project has meaningful risk in:

- provider or API integration
- release packaging or publishing
- localization
- security, credentials, or secrets
- storage or migrations
- UI workflows
- generated content quality
- cross-module contracts

## QA Role

QA should verify behavior across boundaries, not just check that files exist.

Examples:

- API response shape versus UI parser
- localization keys versus resource files
- package script outputs versus README download names
- provider error handling versus user-facing status text
- stored settings versus secret-redaction policy

## Process

1. inspect the diff or generated artifacts
2. classify risk
3. read both sides of each boundary
4. run targeted checks where possible
5. report findings ordered by severity
6. include verification gaps

## Output Format

Use review style:

- findings first
- file and line references when possible
- severity ordering
- concise verification summary
- residual risks

## Stop And Ask

Ask the user when:

- QA depends on private logs or credentials
- a finding requires product policy input
- release approval or destructive action is involved
- expected behavior cannot be inferred from code or docs
