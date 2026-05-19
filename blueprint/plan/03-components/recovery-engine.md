# Component: Recovery Engine

## Purpose
Ensures blueprint survivability by reconstructing current state from the append-only journal in the event of file corruption.

## Responsibilities
- Detect corrupted or missing `SESSION.md` / `NEXT.md`.
- Parse `journal.md` to extract the last valid project state.
- Re-derive:
    - Current Phase.
    - Status of all Action Points (Completed/Pending).
    - Blocked/Waiting nodes.
- Generate a reconstructed `SESSION.md` and `NEXT.md`.

## Logic
- **Tail Scan:** Reads the last 500 lines of `journal.md`.
- **Semantic Extraction:** Uses regex or LLM-assisted parsing to find the "Did" and "Decisions" sections of the last entry.
- **Cross-Reference:** Verifies journal claims against the existence of files on disk.

## Interfaces
- **Input:** `journal.md` file.
- **Output:** Reconstructed `SESSION.md` and `NEXT.md`.

## Failure Modes
- **Corrupted Journal:** The journal itself is malformed.
    - *Handle:* Hard stop. Blueprint is unrecoverable without manual git rollback.
- **Ambiguous Entry:** Last entry doesn't clearly state the phase.
    - *Handle:* Scan previous entries until a valid state is found.
