# Research: Agent Circuit Breakers & Deadlock Prevention

## Preventing Infinite Reflection Loops
Adversarial Proposer-Validator teams can enter infinite recursion if they disagree on a rule without a deterministic stop condition.

### 1. Circuit Breaker Patterns
- **Retry Ceilings:** Fixed limit (e.g., N=2) on consecutive rejections for the same entity.
- **Exponential Backoff (Semantic):** Not time-based, but "effort-based." After failure 1, provide more context. After failure 2, trigger human-in-the-loop.
- **Quarantine:** Isolate the failing node/file from the automated loop while allowing unrelated branches to proceed.

### 2. Orchestration Failure Recovery
- **Escalation States:** Moving from "Autonomous" to "Blocked/Human Required."
- **ADR Recommendations:** If a loop is caused by ambiguous architecture, the system should stop and suggest the human write an ADR to clarify the constraint.

### 3. Deterministic Stop Conditions
- **State Signatures:** Hashing the proposed change. If the Linter proposes the *exact same* change that was previously rejected, trigger an immediate circuit break.

## Synthesis for Bleu
- **Counter:** A hidden file/metadata (e.g., `.reflection/counters.json`) tracking rejection counts per node.
- **Isolation:** The `NEXT.md` file will mark the affected node as `[BLOCKED]` and the Curator will be instructed to skip it in automated cycles.
- **Partial Progress:** The graph traversal logic (BFS) will skip blocked nodes and their downstream dependents, but continue with independent branches.

## Sources
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/news/effective-harnesses-for-long-running-agents)
- [CoALA Cognitive Architecture](https://arxiv.org/abs/2309.02442)
- [Circuit Breaker Pattern in Microservices](https://martinfowler.com/bliki/CircuitBreaker.html)
