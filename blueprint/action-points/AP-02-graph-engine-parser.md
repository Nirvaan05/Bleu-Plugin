# AP-02: Graph Engine Parser

## Title
Implement the Markdown-to-JSON dependency parser.

## Depends on
AP-01

## Files involved
- `scripts/bleu/graph_engine.py`: Modify
- `blueprint/.graph/graph.json`: Create (via script)

## Code flow
1. Implement a recursive directory walker for `plan/` and `action-points/`.
2. Use regex to extract:
    - Node IDs (from titles or filenames).
    - Edges from `Depends on:` lines in APs.
    - Edges from `@blueprint/` links in Component files.
3. Build an adjacency list in memory.
4. Serialize to `graph.json`.
5. Implement a simple "impact" query that returns all descendants of a given node.

## Interfaces touched
- `blueprint/.graph/graph.json` schema.

## Verification
- Create a test component with a link to another component.
- Run the graph engine.
- Verify the edge exists in `graph.json`.

## Complexity
M - Requires robust regex and graph traversal logic.
