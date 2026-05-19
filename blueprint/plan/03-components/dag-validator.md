# Component: DAG Validator (Deterministic)

## Purpose
Enforces structural governance on Action Points with stable, reproducible results.

## Responsibilities
- Run Kahn's Algorithm on `action-points/`.
- **Deterministic Sort:** Use lexicographical tie-breaking for zero in-degree nodes.
- Detect cycles and identify the exact path.
- Generate Mermaid visualization of the graph/loop.

## Logic
- **Lexicographical Sort:** `sorted(zero_in_degree_nodes, key=lambda x: x.id)` before processing.
- **Topological Sorting:** Produces a unique sequence of parallel task groups.

## Interfaces
- **Input:** Action Point files.
- **Output:** Deterministic topological sort.
