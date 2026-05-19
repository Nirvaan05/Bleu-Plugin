# Component: Reflection Circuit Breaker (Root-Aware)

## Purpose
Prevents deadlocks by stopping infinite reflection loops, with special handling for foundational architecture.

## Responsibilities
- Track rejection counts in `.reflection/counters.json` (Atomic).
- **Root-Awareness:** Differentiate between Leaf and Root node failures.
- Trigger **Partial Isolation** for leaf nodes.
- Trigger **Global Hard Stop** for root/foundational nodes.

## Logic
- **Threshold (N=2):** 
    - If node is **Leaf**: Mark node as `BLOCKED`. Quarantine downstream rdeps.
    - If node is **Root** (Foundational): Mark entire project as `BLOCKED`. Escalate to human immediately.
- **Atomic Update:** Use temp-replace for `counters.json` and `SESSION.md`.

## Interfaces
- **Input:** Auditor verdict.
- **Output:** `counters.json` update; human-resolution ADR template.
