# Component: Graph Engine (Implicit-Aware)

## Purpose
Maintains the logical topology of the blueprint, supporting blast-radius analysis and implicit dependency propagation.

## Responsibilities
- Parse explicit links (`Depends on:`, `@blueprint/`).
- Handle **Implicit Dependency Classes** (Global files).
- Compute Transitive Closure (`rdeps`) for blast radius.
- Maintain `graph.json` with node metadata (status, importance).
- **Atomic State:** Write `graph.json` using temp-replace + locking.

## Logic
- **Global Broadcast:** If a file is in the "Global" list (`plan/00`, `plan/01`, `plan/04`, `plan/06`), any change to it marks *all* graph nodes as "Affected".
- **Topological Metadata:** Identifies "Root" nodes (nodes with 0 incoming edges but many outgoing edges) for the Circuit Breaker.

## Interfaces
- **Input:** Workspace files.
- **Output:** `graph.json` file.

## Failure Modes
- **Concurrent Rebuild:** Multiple hooks triggering rebuild simultaneously.
    - *Handle:* Atomic file locking on `graph.json`.
