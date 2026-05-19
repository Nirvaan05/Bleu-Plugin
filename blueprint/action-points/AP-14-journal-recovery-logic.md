# AP-14: Journal Recovery Logic

## Title
Implement state reconstruction from the append-only log.

## Depends on
AP-11

## Files involved
- `scripts/bleu/recovery_engine.py`: Create
- `scripts/bleu/utils.py`: Modify

## Code flow
1. Implement a `JournalScanner` that reads the tail of `journal.md`.
2. Extract the "Current Phase" and "Status" fields from the last entry.
3. Implement a `reconstruct_state()` function that:
    - Regenerates `SESSION.md` and `NEXT.md`.
    - Marks any incomplete APs as "Pending".
4. Add a `verify_recovery` flag that requires human approval on the next session start.

## Interfaces touched
- Blueprint resume protocol.

## Verification
- Delete `SESSION.md`.
- Run the recovery engine.
- Verify that `SESSION.md` is reconstructed with the correct metadata from `journal.md`.

## Complexity
M - Requires parsing semi-structured text.
