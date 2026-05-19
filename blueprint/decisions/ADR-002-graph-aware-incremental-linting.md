# ADR-002: Graph-Aware Incremental Linting

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture

## Context
Full workspace linting on every change is token-prohibitive as blueprints scale. We need a way to only lint the "affected" files.

## Decision
Implement a **Graph-Aware Blast Radius** engine. Use the `.graph/graph.json` to compute the transitive closure of reverse dependencies (rdeps) for any changed file.

## Alternatives considered
- **File-only linting:** Missing downstream impacts (e.g., changing a component's interface without re-linting the APs that implement it).
- **Full re-lint:** Too expensive (O(N²) context growth).

## Consequences
**Positive**:
- 60-80% token reduction in large blueprints.
- Faster reasoning loops.

**Negative**:
- Requires maintaining a valid knowledge graph in sync with markdown.

## Sources
- [Bazel Skyframe](https://bazel.build/rules/skyframe)
