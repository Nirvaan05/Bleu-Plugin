# Risks & Open Questions

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **API Drift** | High | Abstract hook logic into shell scripts; use the minimal `jq`/`bash` surface. |
| **Concurrent Write Corruption** | **Critical (P0)** | All state files (`SESSION.md`, `graph.json`, `counters.json`) must use atomic writes (temp file + `os.replace`) and file locking to survive rapid `FileChanged` events. |
| **Sanitization Bypass (Regex)** | **Critical (P0)** | Obfuscated payloads bypass regex. Mitigation: Require AST-based Markdown parsing for Stage 1. |
| **Root-Node Quarantine** | High (P1) | If a foundational file (`01-architecture.md`) is blocked by the circuit breaker, partial isolation paralyzes the whole graph. Mitigation: Differentiate Root vs Leaf nodes in the Circuit Breaker. |
| **Graph DAG Non-Determinism** | High (P1) | Kahn's algorithm without tie-breaking flaps parallel groups. Mitigation: Enforce lexicographical tie-breaking. |
| **Semantic Drift (Global Files)** | High (P1) | Global constraints (e.g., latency) lack explicit graph edges. Mitigation: Global files must force a full re-lint or require explicit semantic tags. |
| **Graph Complexity & Token Bloat** | Medium (P2) | Passing `graph.json` to the LLM at 1000+ edges is wasteful. Mitigation: Resolve graph edges locally in Python and pass only Markdown contents. |

## Open Questions
- **Q-01:** Should the `counters.json` be cleared when an ADR is accepted for that node? (Hypothesis: Yes, reset the trust cycle).
- **Q-02:** Do we need a "Global Lock" during DAG validation to prevent concurrent edits? (Answered in Phase 6: Yes, atomic file locking is mandatory).
- **Q-03:** How do we handle `import` statements in code if the graph is only parsing Markdown? (Hypothesis: Phase 1 research notes include code excerpts; graph should link these excerpts to their parent component).
- **Q-04:** How do we safely fall back if the AST parser encounters a completely malformed Markdown file during ingest? (Hypothesis: Quarantine to a `raw/quarantine/` folder for human review).
