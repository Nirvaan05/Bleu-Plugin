# ADR-008: Implicit Dependency Propagation

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
The graph engine only models explicit file-to-file links. Global changes (e.g., to architecture invariants) can affect all components without being caught by simple `rdeps`.

## Decision
Introduce **Implicit Dependency Classes** in the Graph Engine.
1.  **Global Class:** Mark foundational files (`00-vision.md`, `01-architecture.md`, `06-non-functional.md`) as "Global".
2.  **Broadcasting:** A change to any "Global" file automatically adds all nodes in the workspace to the linting/validation blast radius.
3.  **Inheritance:** Components can optionally "inherit" from global constraints, making the link explicit in the graph.

## Alternatives considered
- **Explicit Linking Only:** Rejected; humans inevitably forget to link every component to the architecture doc, leading to drift.

## Consequences
**Positive**:
- Guarantees that global architectural changes propagate to implementations.
- Automates the "Maximum Blast Radius" case.

**Negative**:
- Increases the number of nodes pulled into context for global changes.
