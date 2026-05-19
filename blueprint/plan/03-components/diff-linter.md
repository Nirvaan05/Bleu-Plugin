# Component: Differential Linter

## Purpose
Implements incremental validation to minimize token waste and reasoning latency in large blueprints.

## Responsibilities
- Detect changed files using `git diff --name-only`.
- Interface with the Graph Engine to identify the "Affected Subgraph."
- Filter the context passed to the Linter Agent to include *only* relevant nodes.
- Generate a `LINT_SCOPE.md` file for the Linter.

## Logic
- **Diff Phase:** `git diff HEAD` restricted to `blueprint/`.
- **Expansion Phase:** For every changed file, fetch its `rdeps` from the Graph Engine.
- **Filter Phase:** Concatenate only the affected files into the LLM context (or provide a prioritized file list).

## Interfaces
- **Input:** Git status; `graph.json`.
- **Output:** List of file paths for the Linter context.

## Failure Modes
- **Under-scoping:** Missing a logical dependency not captured in the graph.
    - *Handle:* "Global" files (Architecture, Vision) always trigger a full lint pass.
- **Git State Out of Sync:** Unstaged changes not detected.
    - *Handle:* Checks both staged and unstaged changes.
