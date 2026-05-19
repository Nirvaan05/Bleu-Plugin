# AP-12: Deterministic DAG Sort

## Title
Implement stable topological ordering.

## Depends on
AP-03

## Files involved
- `scripts/bleu/dag_validator.py`: Modify

## Code flow
1. Update the `TopologicalSort` function in `dag_validator.py`.
2. In the Kahn's Algorithm loop, when selecting nodes with in-degree 0:
    - Sort the list of candidates lexicographically by their `ID`.
3. Ensure the final `ParallelExecutionGroups` output follows this stable order.

## Interfaces touched
- Handoff artifact generation order.

## Verification
- Run the validator on the same graph 5 times.
- Verify the output sort order is identical every time.

## Complexity
S - Simple tie-breaker logic.
