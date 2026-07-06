# Skill Writing Guide

Use this guide when generating `.agents/skills/<name>/SKILL.md`.

## Structure

Each generated skill must include:

- YAML frontmatter with `name` and `description`
- purpose
- inputs
- outputs
- process
- verification
- stop-and-ask conditions

## Description

Descriptions are trigger surfaces. Include:

- domain/project name
- concrete verbs
- common user phrasing
- follow-up words when relevant: rerun, update, fix, review, release, localize, validate
- near-boundary context to avoid stealing unrelated requests

## Body Style

Write direct, operational instructions.

Good skill bodies:

- explain why important rules exist
- stay lean
- use project-specific paths only after verifying them
- include clear verification commands
- say when to ask the user

Avoid:

- generic role descriptions without process
- copied paths from another project
- huge examples in the main file
- Claude Code-only runtime snippets

## Progressive Disclosure

Keep the main `SKILL.md` focused. Move detail into `references/` when:

- examples are long
- provider/release/platform variants are conditional
- a command catalog is large
- a domain table is useful but not always needed

Reference files should be read only when the main skill says they are relevant.

## Reuse Design

Before creating a skill:

1. inspect existing `.agents/skills/`
2. compare purpose and trigger boundary
3. update the existing skill if it is the same durable role
4. create a new skill only for a distinct recurring workflow or specialist

## Stop And Ask

Add stop-and-ask conditions for:

- destructive operations
- credential or private-log needs
- ambiguous product choices
- release/version mismatch
- missing required release notes or artifacts
- storing or displaying secrets
- translation choices that cannot be inferred
