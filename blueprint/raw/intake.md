# Intake & Framing: Bleu Industrialization

## Restated Idea
The mission is to harden the Bleu-plugin into an industry-grade AI planning and orchestration system. This is a stabilization initiative, not a feature sprint. We will implement deterministic circuit breakers for agent loops, a strict DAG validator for task dependencies, a differential linting engine for token efficiency, and a robust sanitization layer for external inputs. The goal is to maximize reliability, scalability, and token economy while strictly preserving the "Plan First, Execute Later" markdown-backed philosophy.

## Unknowns & Constraints
- **Claude Code API Volatility:** How do we shield Bleu from breaking changes in the `.claude/hooks` schema?
- **Executor Handoff Standards:** What is the minimal contract required to ensure GSD, Superpowers, or raw Claude can consume Action Points without drift?
- **Performance Overhead:** How much latency does the DAG validator and differential linting add to the standard Curator loop?
- **Sanitization vs. Utility:** How do we mitigate prompt injection in `raw/` ingest without losing the ability to process complex user transcripts or technical docs?

## Sharp Questions for the User
1. **Circuit Breaker Strategy:** Should a "deadlock" (N-rejections) trigger a hard stop of the CLI session, or simply lock the blueprint into a "Needs Human Resolution" state while allowing other non-affected sub-tasks?
2. **DAG Enforcement:** If the validator detects a dependency cycle in Phase 5, should it attempt to auto-resolve (e.g., by merging APs) or stop and force the human to re-structure the component breakdown?
3. **Differential Scope:** Should the differential linter work solely on `git diff` (file-level) or should it parse the knowledge graph to identify *logical* downstream impacts even if files haven't changed?
4. **Sanitization Level:** Are we targeting "best-effort" LLM-based sanitization, or a strict "no-executable-content" deterministic parser for initial `raw/` ingest?

## Agreed Scope
- **Greenfield Hardening:** Implementing new core orchestration logic.
- **P0 Focus:** Circuit breakers, DAG validation, Differential linting, Input sanitization.
- **Excluded:** General feature expansion, Vector DB integration, Autonomous code execution.
- **Target Granularity:** ~15-20 Action Points for the implementation of these core systems.
