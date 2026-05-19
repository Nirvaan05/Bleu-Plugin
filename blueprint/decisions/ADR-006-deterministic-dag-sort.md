# ADR-006: Deterministic DAG Sort Order

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
Kahn's algorithm identifies *a* valid topological sort, but not a *unique* one. Parallel task groups can be sorted in multiple ways. Without a tie-breaker, execution artifacts (handoff docs) can change randomly between runs.

## Decision
Enforce **Lexicographical Tie-Breaking** in the DAG Validator.
- When multiple nodes have zero in-degree, sort them by their `ID` (e.g., `AP-01`, `AP-02`) before adding to the execution queue.
- This ensures that for a given graph, the handoff artifact is always identical.

## Alternatives considered
- **Probabilistic Sort:** Rejected; makes automated verification and execution unstable.

## Consequences
**Positive**:
- Deterministic and reproducible execution plans.
- Stable handoff artifacts.

**Negative**:
- None identified.
