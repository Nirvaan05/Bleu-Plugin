# Research: Implicit Architectural Dependencies

## Modeling Global Constraints
Standard graph engines model explicit links (File A -> File B). "Industrial" Bleu must also handle implicit dependencies where a change in a global constraint propagates to all relevant nodes.

### 1. Dependency Classes
- **Explicit:** `@blueprint/` links, `Depends on:`.
- **Implicit (Global):**
    - **Architecture Invariants:** Performance targets, security models.
    - **System-wide Schemas:** Data models referenced by multiple components.
    - **External API Contracts:** Integrations used across pipelines.

### 2. Implementation Strategies
- **Global Broadcast:** Any change to a file tagged `class: global` (e.g., `00-vision.md`, `01-architecture.md`) automatically adds all nodes to the blast radius.
- **Concept Tags:** Use metadata tags (e.g., `requires: auth-contract`) to link components to a shared concept without requiring explicit file paths.
- **Semantic Blast Radius:** The Graph Engine identifies the "Class" of a change and expands the `rdeps` set based on that class.

### 3. Sources
- [Bazel: Configurations and Build Graphs](https://bazel.build/extending/config)
- [Software Architecture: Semantic Dependency Analysis](https://en.wikipedia.org/wiki/Dependency_analysis)
