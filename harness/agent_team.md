# Agent team design for this domain


Team overview

- **Orchestrator**: coordinates the workflow, schedules agents, and aggregates results.
- **RepoInspector**: inspects repository structure and key files (README, LICENSE, CHANGELOG, docs).
- **DependencyChecker**: finds dependency manifests (requirements.txt, package.json, pyproject.toml) and reports potential issues.
- **ChangelogAuditor**: parses `CHANGELOG.md` and release notes for recency and formatting hints.
- **DocsChecker**: validates presence of key docs (quickstart, experimental notes) and extracts TODOs.
- **ReleasePlanner**: suggests a next-release checklist based on findings.
- **LocalTester**: runs lightweight smoke checks (existence of test commands, basic lint heuristics).
- **Strategist / ContentGenerator / QA**: as previously defined to plan, generate artifacts, and validate.

Interaction patterns

- Orchestrator invokes Scout -> Auditor -> Strategist -> ContentGenerator -> QA in a pipeline for each work item.
- Agents exchange structured JSON payloads; each agent reads the previous step's output and appends `result` and `metadata`.
- The Orchestrator keeps an audit log and can re-run or branch tasks for parallel experimentation.

Data contracts

- Input: {"id": "<task-id>", "payload": {...}, "history": [...]}
- Agent output: {"id": "<task-id>", "result": {...}, "metadata": {"agent":"<name>","timestamp":"..."}}

Failure and retries

- Agents should return exit codes and error objects; Orchestrator retries transient failures with exponential backoff.
- Critical failures are surfaced to a human reviewer via the Orchestrator's notification hook.

Extensibility

- Add new agents by registering them in the config and implementing `run(config, input)`.
- Support for remote agents (HTTP/gRPC) can be added by providing an adapter layer behind the same interface.
