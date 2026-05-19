# ADR-005: Atomic State Management

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
Bleu relies on several critical JSON and Markdown files (`SESSION.md`, `graph.json`, `counters.json`) that are updated via hooks. Rapid file changes can trigger multiple concurrent writes, leading to partial writes or silent corruption.

## Decision
Implement **Atomic State Management** for all protected blueprint files.
1.  **Write-to-Temp:** Write changes to a temporary file in the same directory.
2.  **Atomic Replace:** Use `os.replace` (on Python) or equivalent to overwrite the target file in a single syscall.
3.  **File Locking:** Use `.lock` files during the write operation to prevent concurrent modification by multiple hooks.

## Alternatives considered
- **Direct Write:** Rejected; prone to corruption during crashes or concurrency.
- **SQLite:** Rejected; markdown files must remain directly human-readable.

## Consequences
**Positive**:
- Guarantees file integrity.
- Safe for high-concurrency hook environments.

**Negative**:
- Slight performance overhead for disk I/O.
