# ADR-NNN: [NODE_PATH] Recovery Plan

**Status**: Proposed (Escalated from Circuit Breaker)
**Date**: [DATE]
**Deciders**: user (Tie-breaker)

## Context
This node reached the reflection ceiling (N=2 rejections). Autonomous execution has been paused for this branch to prevent orchestration deadlocks.

### Conflict Summary
- **Proposal ID**: [PROPOSAL_ID]
- **Linter Intent**: [SUMMARY_OF_CHANGE]
- **Auditor Concerns**: [REASON_FOR_REJECTION]

## Proposed Resolution
[Describe how the ambiguity should be resolved. Should the architecture be updated, or should the implementation be corrected?]

## Consequences
- **If Resolved**: Execution resumes for this node and dependents.
- **If Not Resolved**: Node remains quarantined.
