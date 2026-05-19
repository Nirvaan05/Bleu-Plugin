# AP-06: Circuit Breaker Logic

## Title
Implement the N=2 reflection loop guard.

## Depends on
AP-01

## Files involved
- `scripts/bleu/circuit_breaker.py`: Create
- `blueprint/.reflection/counters.json`: Create (via script)

## Code flow
1. Implement a script that accepts a proposal ID and a verdict (`APPROVE`|`REJECT`).
2. If `REJECT`, increment the counter in `counters.json`.
3. If `counter == 2`, return a non-zero exit code and output a `BLOCK_SIGNAL`.
4. Implement the isolation logic:
    - Rewrite `SESSION.md` to mark the node as `BLOCKED`.
    - Update `NEXT.md` to quarantine the node.

## Interfaces touched
- `.reflection/counters.json` schema.
- `SESSION.md` / `NEXT.md` update logic.

## Verification
- Manually run the script with `REJECT` twice for the same ID.
- Verify that `SESSION.md` is updated to include the `BLOCKED` status.

## Complexity
M - Requires stateful tracking and workspace mutation.
