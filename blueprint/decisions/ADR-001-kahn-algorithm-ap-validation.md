# ADR-001: Kahn's Algorithm for AP Validation

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture

## Context
Bleu needs a way to guarantee that the generated Action Points form a valid, executable sequence. Circular dependencies currently cause execution deadlocks.

## Decision
Use **Kahn's Algorithm** for topological sorting of Action Points. It is O(V+E) and provides a clear signal of whether the graph is a DAG.

## Alternatives considered
- **DFS with coloring:** Also O(V+E), but harder to extract parallel execution groups from the traversal.
- **LLM-based validation:** Too non-deterministic; prone to missing subtle cycles in large graphs.

## Consequences
**Positive**:
- Deterministic PASS/FAIL signal.
- Automatically generates parallelizable task groups.

**Negative**:
- Requires a structured dependency parser (Regex).

## Sources
- [Topological Sorting - Kahn's Algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm)
