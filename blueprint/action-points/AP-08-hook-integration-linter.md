# AP-08: Hook Integration (Linter/Auditor)

## Title
Wire the Differential Linter and Circuit Breaker.

## Depends on
AP-04, AP-06

## Files involved
- `.claude/settings.json`: Modify
- `.claude/hooks/auditor-gate.sh`: Create

## Code flow
1. Register a `SubagentStop` hook matched on the `kb-linter`.
2. In the hook, invoke `circuit_breaker.py`.
3. If the circuit breaker returns a `BLOCK_SIGNAL`, intercept the Auditor spawn and escalate to the user.
4. Modify the Linter agent definition to use `diff_linter.py` for its context generation.

## Interfaces touched
- Subagent lifecycle hooks.

## Verification
- Simulate two Linter rejections.
- Verify the Auditor does not fire a third time and the user is notified of the block.

## Complexity
L - High impact but mostly configuration logic.
