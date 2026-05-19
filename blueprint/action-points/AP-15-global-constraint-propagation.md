# AP-15: Global Constraint Propagation

## Title
Implement implicit dependency broadcasting in the Graph Engine.

## Depends on
AP-02

## Files involved
- `scripts/bleu/graph_engine.py`: Modify

## Code flow
1. Define a list of `GLOBAL_FILES` (e.g., `plan/01-architecture.md`, `plan/06-non-functional.md`).
2. In the `find_rdeps` function:
    - If the "seed" node is a Global File, return *every* node in the graph as a reverse dependency.
3. Update `graph.json` to include an `is_global` flag for these nodes.

## Interfaces touched
- Differential linting blast radius.

## Verification
- Modify `01-architecture.md`.
- Run the Diff Linter.
- Verify that all blueprint files are included in the lint context.

## Complexity
S - Simple logic change in the graph traversal.
