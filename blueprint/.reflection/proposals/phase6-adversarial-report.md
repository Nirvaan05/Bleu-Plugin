# Phase 6 Adversarial Lint Report: Blueprint Survivability

**Date:** 2026-05-18
**Type:** adversarial-lint-verdict
**Scope:** Full Blueprint (`plan/`, `action-points/`, `decisions/`, `scripts/`)

## 1. Confirmed Strengths
- **Proposer-Validator Isolation:** The structural boundary between the Linter and Auditor prevents the LLM "self-praise" hallucination loop.
- **Transitive Closure (rdeps) Linting:** Moving from full-workspace to graph-aware blast-radius linting correctly identifies the mathematical dependencies between files.
- **DAG Enforcement via Kahn's:** Ensuring Action Points form a DAG is a mathematically sound way to prevent execution deadlocks.

## 2. Architectural Weak Points
- **Sanitization Bypass (Regex is Insufficient):** Regex cannot parse Markdown reliably. Obfuscated payloads (e.g., `eval $(echo "...")`, unicode homoglyphs, malformed code fences) will bypass Stage 1 Regex and execute during Curator compilation.
- **Semantic vs. Syntactic Graph Drift:** Transitive closure only catches explicit links. If a global file (e.g., `06-non-functional.md`) changes a latency requirement from 100ms to 50ms, it affects *all* APs, but the graph will show zero downstream dependencies unless every AP explicitly links to `06-non-functional.md`.
- **Topological Sort Non-Determinism:** Kahn's Algorithm does not guarantee a unique sort order. Without tie-breaking, parallel AP groups may flap between runs, causing handoff artifacts to change randomly and confusing the executor.

## 3. Deterministic Failure Scenarios
- **Concurrent Write Corruption:** The `FileChanged` hook can fire rapidly if multiple files are downloaded or generated. Without atomic writes and file locking, `graph.json`, `counters.json`, `SESSION.md`, and `NEXT.md` will suffer race conditions and silent corruption.
- **Root-Node Quarantine Paralyzes System:** If the Circuit Breaker hits N=2 on `plan/01-architecture.md` (a root node), marking it `[BLOCKED]` will cascade the `[WAITING]` state to the entire graph. The "Partial Isolation" becomes a "Global Freeze" anyway.

## 4. Unresolved Risks & Scalability Concerns
- **Token Bloat in Scale:** If `graph.json` grows to 1000+ edges, appending it to the Linter's context will cause token exhaustion. The Differential Linter must resolve the graph *locally in Python* and only pass the relevant `.md` file contents, never the raw `graph.json` structure.
- **Unbounded Graph Depth:** In a 500+ AP system, computing deep `rdeps` could pull 80% of the project into context. There is no decay factor for weak vs. strong dependencies.

## 5. Recovery Limitations
- If `SESSION.md` is half-written due to a crash, the resume protocol fails. There is no journal playback mechanism to rebuild a corrupted `SESSION.md` or `NEXT.md`.

## 6. Recommended Modifications & Additions

### Recommended ADR Modifications
- **MODIFY ADR-003 (Circuit Breaker):** Introduce a "Root vs. Leaf" distinction. If a node with >50% of the graph as downstream dependents is blocked, immediately trigger a Global Hard Stop and human escalation. Partial isolation is only safe for leaf/mid-tier nodes.
- **MODIFY ADR-004 (Sanitization):** Abandon regex-only logic. Stage 1 must use an AST-based Markdown parser (e.g., `markdown-it-py`) to extract plaintext and strictly sanitize code fences.

### Recommended AP Additions
- **ADD AP-11 (Atomic State Management):** Implement POSIX atomic writes (write-to-temp, `os.replace`) and `.lock` files for `graph.json`, `counters.json`, `SESSION.md`, and `NEXT.md`.
- **ADD AP-12 (Deterministic DAG Sort):** Implement lexicographical tie-breaking in Kahn's algorithm to ensure reproducible execution artifact generation.
- **ADD AP-13 (AST Sanitizer Core):** Implement the AST-based Markdown parser for `raw/` ingest.

## 7. Severity Classification

| Finding | Classification | Reason |
|---|---|---|
| Concurrent Write Corruption | **P0 (Critical)** | Silent destruction of blueprint state; unrecoverable. |
| AST Sanitization Bypass | **P0 (Critical)** | Complete compromise of the Planner agent boundary. |
| Root-Node Quarantine Paralyzes System | **P1 (High)** | Fails the stated goal of avoiding orchestration paralysis. |
| Topological Sort Non-Determinism | **P1 (High)** | Execution handoff artifacts mutate randomly. |
| Global Constraints Missed by Graph | **P1 (High)** | High risk of architectural drift for non-functional requirements. |
| Token Bloat from graph.json | **P2 (Medium)** | Costly, but doesn't technically break functionality. |
