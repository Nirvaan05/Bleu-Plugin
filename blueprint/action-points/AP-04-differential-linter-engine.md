# AP-04: Differential Linter Engine

## Title
Implement graph-aware blast radius calculation.

## Depends on
AP-02

## Files involved
- `scripts/bleu/diff_linter.py`: Create
- `.claude/bleu/lint-config.json`: Create

## Code flow
1. Run `git diff HEAD --name-only blueprint/`.
2. For each changed file, look up its node ID in `graph.json`.
3. Compute the **Transitive Closure** (all reachable downstream nodes) using BFS.
4. Filter out any nodes that are not within the `plan/` or `action-points/` directories.
5. Generate a JSON list of files that constitute the "Affected Subgraph."

## Interfaces touched
- Integration between Git and Graph Engine.

## Verification
- Modify one component file.
- Run the diff linter.
- Verify that only that component and its dependents are listed in the output.

## Complexity
M - Integration task with graph traversal.
