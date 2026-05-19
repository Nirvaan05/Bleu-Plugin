# AP-10: E2E Stabilization Test

## Title
Verify the entire hardened orchestration cycle.

## Depends on
AP-07, AP-08, AP-09, AP-12, AP-14

## Files involved
- `tests/bleu/e2e_stabilization.py`: Create

## Code flow
1. Script an E2E test that:
    - Ingests a malicious `raw/` file (verify sanitization).
    - Creates a cyclic AP graph (verify DAG validation).
    - Triggers a reflection loop (verify circuit breaker).
    - Modifies a component (verify differential linting).
2. Report PASS only if all deterministic guardrails fire correctly.

## Interfaces touched
- System-wide verification.

## Verification
- Run the test suite and achieve 100% pass rate.

## Complexity
L - Comprehensive verification.
