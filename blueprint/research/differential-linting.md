# Research: Differential Linting & Graph-Aware Blast Radius

## Efficiency in Large Blueprints
As blueprints scale to 40+ files, re-linting the entire workspace becomes token-prohibitive. Bleu must shift to an incremental, graph-aware model.

### 1. Blast Radius Analysis (Reverse Dependencies)
- **Concept:** If File A changes, only File A and its transitive closure of dependents (rdeps) need re-validation.
- **Transitive Closure:** The set of all nodes reachable from the changed node in the *reverse* dependency graph.
- **Bleu Graph Integration:** Utilize `.graph/graph.json` as the operational infrastructure.
    - **Step 1:** Detect changes via `git diff`.
    - **Step 2:** Map file paths to node IDs.
    - **Step 3:** Perform a reverse-edge traversal to find the "Affected Subgraph."

### 2. Incremental Linting Patterns
- **Skyframe Model (Bazel):** Treats the build as a graph of functions. Invalidation is incremental.
- **Nx Affected:** Maps changed files to "Projects." Bleu maps changed files to "Components" or "Action Points."

### 3. Logical vs. Syntactic Impact
- **Syntactic:** File changed -> Re-lint file.
- **Logical (Bleu Speciality):** 
    - Change in `plan/01-architecture.md` (e.g., new interface constraint) has a "Maximum Blast Radius" affecting all components.
    - Change in `plan/03-components/auth.md` logic only affects APs that implement `auth`.

## Synthesis for Bleu
- **Engine:** A background script/MCP tool that reads `.graph/graph.json` and `git diff` to output a `lint-scope.json`.
- **Optimization:** The Linter agent receives *only* the content of the affected subgraph in its context, dramatically reducing token waste.

## Sources
- [Skyframe: Bazel's Incremental Eval](https://bazel.build/rules/skyframe)
- [Nx Affected Analysis](https://nx.dev/concepts/affected)
- [Turborepo Filtering](https://turbo.build/repo/docs/core-concepts/filtering)
