# Research: Journal Replay & Crash Recovery

## Deterministic Resume Reconstruction
If `SESSION.md` or `NEXT.md` become corrupted due to a system crash or interrupted write, Bleu must be able to reconstruct the current state from the append-only `journal.md`.

### 1. Journal Playback Mechanism
- **Append-Only Principle:** Since `journal.md` is append-only, its last valid entry represents the most recent "known good" state.
- **State Reconstruction:** By parsing the last entry's "Outcome" and "Decisions made" sections, the system can re-derive the current phase, completed APs, and pending blockers.
- **Redundancy:** This provides a "Write-Ahead Log" (WAL) effect for the blueprint workspace.

### 2. Recovery Flow
- **Step 1: Checksum/Validate:** On session start, validate `SESSION.md`. If malformed or missing, trigger recovery.
- **Step 2: Parse Journal:** Read the tail of `journal.md`.
- **Step 3: Regenerate:** Use the journal data to rewrite a fresh `SESSION.md` and `NEXT.md`.
- **Step 4: Audit:** Force a human confirmation of the reconstructed state before proceeding.

### 3. Sources
- [Database Recovery Patterns (WAL/Checkpointing)](https://en.wikipedia.org/wiki/Write-ahead_logging)
- [Event Sourcing and State Reconstruction](https://martinfowler.com/eaaDev/EventSourcing.html)
