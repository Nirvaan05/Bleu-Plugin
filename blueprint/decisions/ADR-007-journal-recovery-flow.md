# ADR-007: Journal Replay Recovery Flow

**Status**: Accepted
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
If `SESSION.md` is corrupted or deleted, the system loses its current-state pointer. We need a way to self-heal.

## Decision
Implement a **Journal Replay Recovery** mechanism.
1.  On session start, if `SESSION.md` is invalid, read the append-only `journal.md`.
2.  Parse the most recent session entries to re-derive:
    - Current Phase.
    - Completed APs.
    - Blocked/Waiting nodes.
3.  Reconstruct `SESSION.md` and `NEXT.md` from the journal data.
4.  Require human sign-off on the reconstructed state.

## Alternatives considered
- **Manual Reset:** Rejected; too much data loss for long projects.

## Consequences
**Positive**:
- Blueprint survivability across catastrophic file failures.
- Deterministic self-healing.

**Negative**:
- Requires parsing natural language (or semi-structured) entries in the journal.
