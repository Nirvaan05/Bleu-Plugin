# Vision: Bleu Stabilization & Industrialization

## Problem Statement
Bleu is currently a powerful but fragile orchestration system. As blueprints grow in complexity, the lack of deterministic guardrails leads to token-heavy O(N²) linting passes, infinite reflection deadlocks between agents, and vulnerability to architectural drift from unsanitized external inputs. To reach "industry-grade" status, Bleu must transition from vibe-based autonomy to a bounded, deterministic governance model.

## Goals
- **Token Efficiency:** Reduce linting costs by 60-80% for large blueprints through graph-aware incremental validation.
- **Reliability:** Eliminate infinite reflection loops with a root-aware circuit breaker and atomic state management.
- **Correctness:** Guarantee an executable task sequence through deterministic DAG validation and stable topological sorting.
- **Security:** Hardened ingestion pipeline via AST-based deterministic sanitization.
- **Survivability:** Ensure blueprints survive catastrophic file corruption via journal-replay recovery.

## Non-Goals
- Adding vector databases or RAG.
- Turning Bleu into a code-writing agent.
- Replacing markdown with a database.
- Building a complex multi-agent "swarm."

## Success Criteria
1. **Zero Deadlocks:** 100% of infinite reflection loops are caught and escalated to human within 3 cycles.
2. **Cycle-Free APs:** 100% of Phase 5 Action Point dependency cycles are detected and blocked before handoff.
3. **Recovery:** 100% of corrupted `SESSION.md` files are successfully reconstructed from `journal.md`.
4. **Injection Immunity:** AST-based sanitization strips 100% of known "Ignore instructions" strings from `raw/` ingest.
