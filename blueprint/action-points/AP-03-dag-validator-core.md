# AP-03: DAG Validator Core

## Title
Implement Kahn's Algorithm for AP cycle detection.

## Depends on
AP-02

## Files involved
- `scripts/bleu/dag_validator.py`: Modify

## Code flow
1. Load the adjacency list from `graph.json`.
2. Filter nodes to only include those of type `ap` (Action Point).
3. Implement Kahn's Algorithm:
    - Track in-degree of all AP nodes.
    - Queue nodes with in-degree 0.
    - Topologically sort.
4. If a cycle is detected, use a DFS search on the residual nodes to trace the exact path of the loop.
5. Output a Mermaid-formatted string representing the loop.

## Interfaces touched
- DAG validation output format.

## Verification
- Create a cycle: `AP-A -> AP-B -> AP-A`.
- Run the validator.
- Verify it fails and correctly identifies the cycle path.

## Complexity
M - Algorithmic implementation with error tracing.
