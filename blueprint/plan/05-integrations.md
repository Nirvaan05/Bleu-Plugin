# Integrations: External Tools & Environments

## Claude Code Hook System
Bleu's "Nervous System." We integrate via the following lifecycle events:
- **`FileChanged`:** Triggers the Deterministic Sanitizer on `raw/` and the Graph Engine on `plan/`.
- **`SubagentStop`:** Triggers the Circuit Breaker and Auditor for the Linter.
- **`SessionStart`:** Surfaces `BLOCKED` states and pending resolution ADRs.

## Git CLI
Used by the Differential Linter to compute `git diff HEAD` and identify the "seed" nodes for blast-radius analysis.

## Mermaid.js
Used for rendering the Action Point dependency graph and visualizing detected cycles in `action-points/README.md`.

## Python Standard Library
Used for the deterministic Sanitizer and DAG Validator scripts (avoiding heavy external dependencies to maintain portability).
