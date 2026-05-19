# Research: DAG Validation & Cycle Detection

## Algorithms for Dependency Validation
To ensure architectural integrity in Phase 5 Action Points, Bleu must implement a deterministic Directed Acyclic Graph (DAG) validator.

### 1. Cycle Detection (The "Compiler Error" Model)
- **Kahn's Algorithm (Topological Sort):** An O(V+E) algorithm that either returns a valid execution order or identifies that a cycle exists. It works by repeatedly removing nodes with zero in-degree.
- **Tarjan's/DFS with Coloring:** Uses three states (Unvisited, Visiting, Visited). If a traversal encounters a "Visiting" node, a cycle is detected.
- **Bleu Implementation:** Kahn's is preferred for Phase 5 because it naturally generates the "Parallel Execution Groups" required by the Action Point template.

### 2. Orphan & Reachability Analysis
- **Orphan APs:** Nodes with no incoming or outgoing edges (in a multi-node project) suggest disconnected intent.
- **Root/Sink Analysis:** Identifying the "Entry" (APs with no deps) and "Exit" (APs that depend on everything) points to validate against the Phase 2 Pipeline sequence.

### 3. Build System Parallels
- **Bazel/Turborepo:** These systems treat the task graph as immutable during a build run. Bleu should adopt this: the DAG is validated *before* any AP is handed off to an executor.

## Synthesis for Bleu
- **Strict Mode:** Cycle detection is a blocking error.
- **Diagnostic Output:** If a cycle exists, Bleu will output the path (e.g., `AP-01 -> AP-04 -> AP-01`) using the coloring state from the DFS traversal.
- **Visual Validation:** Use Mermaid.js to render the graph in `action-points/README.md` to help the human re-structure the dependency loop.

## Sources
- [Bazel Query - Graph Theory](https://github.com/bazelbuild/bazel)
- [Kahn's Algorithm for Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm)
- [Turborepo Task Graph](https://turborepo.org/docs/core-concepts/monorepos/task-graph)
