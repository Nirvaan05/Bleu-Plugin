# AP-09: Recovery ADR Template

## Title
Design the human-in-the-loop recovery artifact.

## Depends on
AP-06

## Files involved
- `blueprint/decisions/templates/resolution-adr.md`: Create

## Code flow
1. Create a specialized ADR template for resolving agent deadlocks.
2. Include sections for:
    - The rejected proposal description.
    - The Auditor's reasoning for rejection.
    - The Linter's justification for the proposal.
    - The Human's tie-breaking decision.
3. Instruct the Circuit Breaker to populate this template when a block occurs.

## Interfaces touched
- ADR format extensions.

## Verification
- Trigger a circuit break.
- Verify the populated resolution ADR exists in `decisions/`.

## Complexity
S - Documentation task.
