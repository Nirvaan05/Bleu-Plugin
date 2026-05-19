# Non-Functional Requirements: Industrial Grade

## Performance
- **Graph Rebuild:** Must complete in <2 seconds for 100-file blueprints.
- **DAG Validation:** Kahn's Sort must complete in <1 second for 50 APs.
- **Sanitization:** Must add <500ms latency to the `FileChanged` hook.

## Reliability
- **Determinism:** The Sanitizer and DAG Validator must produce identical outputs for identical inputs (pure functions).
- **Idempotency:** Re-running the Graph Engine on an unchanged blueprint must not change the `graph.json` hash.

## Token Economics
- **Differential Filtering:** Must reduce Linter context size by at least 50% for changes touching <3 files in a 20-file project.

## Security
- **Trust Boundaries:** LLM agents must be instructed to treat `<external_content>` tags as data, never as directives.
- **Isolation:** Sub-agents (Linter, Auditor) must run with read-only permissions to the `blueprint/` directory except for their specific `.reflection/` output paths.
