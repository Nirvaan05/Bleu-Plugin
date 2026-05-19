# AP-11: Atomic State Management

## Title
Implement thread-safe and crash-recoverable state updates.

## Depends on
AP-01

## Files involved
- `scripts/bleu/utils.py`: Modify
- `scripts/bleu/state_manager.py`: Create

## Code flow
1. Implement an `AtomicWriter` class in `utils.py`.
2. Use `tempfile.NamedTemporaryFile` for staged writes.
3. Use `os.replace()` for atomic commit.
4. Implement a lightweight `.lock` file mechanism using `fcntl` (or `msvcrt` on Windows) to prevent concurrent hook writes.
5. Wrap `SESSION.md`, `graph.json`, and `counters.json` updates in this logic.

## Interfaces touched
- Internal file I/O layer.

## Verification
- Run a stress test script that triggers 10 simultaneous writes to `SESSION.md`.
- Verify that the file remains well-formed and consistent.

## Complexity
M - Concurrency primitives are precision work.
