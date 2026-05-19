# Pipelines: Core Orchestration Flows

## 1. Safe Ingestion Pipeline
Ensures external data cannot contaminate the system architecture.

1. **Trigger:** File dropped into `blueprint/raw/`.
2. **AST Pass:** Python script parses Markdown to AST and strips executable patterns.
3. **Unicode Pass:** Script normalizes unicode to prevent homoglyph attacks.
4. **Queueing:** `FileChanged` hook adds path to `blueprint/.curator-pending/compile.queue`.

## 2. Differential Linting Pipeline
Optimizes token usage for large workspaces.

1. **Trigger:** `git diff` detected in `blueprint/plan/` or `action-points/`.
2. **Blast Radius Calculation:** Graph Engine identifies all downstream dependent nodes (rdeps). 
    - **Note:** If a Global file changed, all nodes are marked "Affected".
3. **Linter Pass:** Linter agent receives restricted context.

## 3. AP Validation & Handoff Pipeline
Guarantees execution safety and stability.

1. **Trigger:** Phase 5 completion / Sign-off request.
2. **Deterministic DAG Check:** Validator runs Kahn's Algorithm with lexicographical tie-breaking.
3. **Artifact Generation:** Write `handoff/` artifact using the unique, stable sort order.

## 4. Reflection Recovery Pipeline (The Circuit Breaker)
Prevents orchestration deadlocks with foundational safeguards.

1. **Trigger:** Auditor rejects a proposal.
2. **Atomic Counter:** `.reflection/counters.json` updated using atomic write.
3. **Ceiling Check (N=2):** 
    - **Leaf Node:** Partial Isolation (Quarantine node + rdeps).
    - **Root Node:** Global Hard Stop + Human Escalation.

## 5. Crash Recovery Pipeline
Self-heals corrupted workspace state.

1. **Trigger:** `SessionStart` detects corrupted `SESSION.md`.
2. **Journal Replay:** Recovery engine parses last valid `journal.md` entries.
3. **State Reconstruction:** `SESSION.md` and `NEXT.md` regenerated using atomic writes.
4. **Sign-off:** User confirms reconstructed state.
