# ADR-003: Root vs. Leaf Quarantine Circuit Breaker

**Status**: Accepted (Revised 2026-05-18)
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
Partial isolation is intended to prevent orchestration paralysis. However, if the failing node is a "root" or "foundational" file (e.g., `01-architecture.md`), proceeding on other branches while the root is contested leads to corrupted architectural assumptions.

## Decision
Implement a **Root vs. Leaf Awareness** in the Circuit Breaker.
1.  **Leaf/Mid-tier Nodes:** Default to **Partial Isolation** (quarantine node + rdeps).
2.  **Root/Foundational Nodes:** Trigger a **Deterministic Global Hard Stop**.
    - Foundational files include: `00-vision.md`, `01-architecture.md`, `04-data-model.md`, and any file marked `class: global`.
    - If a foundational file reaches N=2 rejections, freeze all autonomous execution and escalate to human review immediately.

## Alternatives considered
- **Universal Partial Isolation:** Rejected; leads to "false continuity" where branches proceed on invalid foundations.
- **Universal Global Stop:** Rejected; too fragile for large independent graphs.

## Consequences
**Positive**:
- Prevents systemic drift on corrupted assumptions.
- Maintains progress on truly independent branches.

**Negative**:
- Adds logic to differentiate node "importance" in the graph.

## Sources
- [Bleu Stabilization Phase 6 Adversarial Audit]
