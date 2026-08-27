# QA Agent Guide

QA guidance for software engineering harnesses. Focuses on runtime boundary defects that bypass TypeScript compilation and static review.

## 1. Boundary Mismatch (Core Defect)

Components pass unit checks in isolation, but fail at module seams.

| Boundary | Mismatch Example | Why Static Analysis Misses It |
|----------|-------------------|-------------------------------|
| **API ↔ Hook** | API returns `{ projects: [] }`, hook expects `Project[]` | Generic type parameters (`fetchJson<T>`) bypass runtime validation. |
| **Field Naming** | API sends `thumbnailUrl`, interface declares `thumbnail_url` | Explicit type casting (`as Type`) silences the compiler. |
| **Routing** | Page at `/dashboard/items`, link targets `/items` | Route groups `(group)` or prefixes are omitted in hrefs. |
| **State Machine** | Transition declared in map, but update code is never called | Map existence is verified without tracing call sites. |
| **Endpoint ↔ Hook** | Endpoint implemented, but frontend never invokes it | Endpoints and hook calls are not mapped 1:1. |
| **Sync vs Async** | API returns `202 Accepted` `{ status }`, frontend reads result fields | Polling / async lifecycle shapes are conflated. |

## 2. Coherence Verification Procedure

### 2-1. API Response ↔ Frontend Hook Type
1. Inspect `NextResponse.json(...)` payload in route handlers.
2. Read the corresponding `fetchJson<T>` generic in the frontend hook.
3. Compare shape, field naming (`snake_case` vs `camelCase`), and unwrap logic (e.g., `.data`).

### 2-2. File Paths ↔ Router Links
1. Derive routes from `src/app/**/page.tsx` (strip `(group)` names, account for `[param]`).
2. Grep all `href=`, `router.push(`, and `redirect(` statements.
3. Verify every link targets an existing page route.

### 2-3. State Machine Completeness
1. Extract allowed states and transitions from the state map.
2. Grep all status update calls (e.g., `.update({ status: '...' })`).
3. Ensure all updates match declared transitions and no intermediate states hang indefinitely.

### 2-4. Endpoint ↔ Hook 1:1 Mapping
- Compare API routes against frontend service/hook calls. Flag orphaned endpoints or missing invocations.

## 3. QA Design Principles

- **Use `general-purpose` (not `Explore`):** QA must execute search tools, run linters/tests, and compare files. `Explore` is strictly read-only.
- **Cross-read both sides:** Never check a file in isolation. Read the producer and consumer files together in the same context.
- **Run incrementally:** Run QA immediately after each module implementation rather than once at the end.

## 4. Web App QA Checklist

```markdown
### Integration Coherence Checklist

#### API & Data Flow
- [ ] Route response shape matches frontend hook generic type
- [ ] Envelope unwrapping (e.g., `{ data: [...] }` -> `data`) handled properly
- [ ] Consistent property casing (`snake_case` vs `camelCase`) across boundaries
- [ ] Every endpoint has a matching frontend hook or caller

#### Routing & Navigation
- [ ] All `href` and `router.push` paths match real filesystem routes
- [ ] Route group segments `(group)` correctly omitted from URL paths
- [ ] Dynamic parameters `[id]` correctly populated at call sites

#### State Machine & Async
- [ ] All declared state transitions are implemented in code
- [ ] No intermediate state hangs without a final transition
- [ ] Async/polling endpoints distinguish 202 initial response from final payload
```

## 5. QA Agent Template

```markdown
---
name: qa-inspector
description: "QA 검증 전문가. 모듈 경계 정합성, 스펙 준수, 런타임 오류 방지를 검증."
---

# QA Inspector

## Role
Verify implementations with **module boundary coherence** as top priority.

## Priority Order
1. **Integration Coherence:** API ↔ Hook types, route paths, state transitions.
2. **Functional Spec:** Business logic, edge case handling.
3. **Code Quality:** Dead code, unsafe casting (`as any`), unhandled promises.

## Working Method: Read Both Sides Together
- Open route handler alongside its consuming hook.
- Compare filesystem routes against navigation link strings.
- Compare state machine declarations against update call sites.

## Reporting Protocol
- Reference findings with exact `file_path:line_number`.
- Provide concrete fix recommendations for both producer and consumer sides.
```
