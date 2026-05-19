# Handoff to GSD (Get Stuff Done)

**Invoke via:** `/gsd:new-milestone`

## Milestone Objective
Implement the deterministic governance layer for the Bleu-plugin, replacing vibe-based autonomy with strict architectural guardrails.

## Source of Truth
The architecture is locked. Do not improvise. Refer to `@blueprint/plan/01-architecture.md` and `@blueprint/decisions/README.md`.

## Task Breakdown

### Phase 1: P0 Infrastructure
- [ ] Scaffold CLI scripts (`@blueprint/action-points/AP-01-scaffold-scripts.md`)
- [ ] Implement atomic temp-replace writers (`@blueprint/action-points/AP-11-atomic-state-management.md`)

### Phase 2: Input Hardening & Circuit Breakers
- [ ] Build Stage 1 Regex Sanitizer (`@blueprint/action-points/AP-05-sanitizer-regex-suite.md`)
- [ ] Upgrade to AST-Based Parser (`@blueprint/action-points/AP-13-ast-sanitizer-core.md`)
- [ ] Implement N=2 Counter Logic (`@blueprint/action-points/AP-06-circuit-breaker-logic.md`)

### Phase 3: Graph Engine & Validation
- [ ] Build Markdown Dependency Parser (`@blueprint/action-points/AP-02-graph-engine-parser.md`)
- [ ] Implement Implicit Dependency Broadcasting (`@blueprint/action-points/AP-15-global-constraint-propagation.md`)
- [ ] Implement Kahn's Algorithm Validator (`@blueprint/action-points/AP-03-dag-validator-core.md`)
- [ ] Add Lexicographical Tie-Breaking (`@blueprint/action-points/AP-12-deterministic-dag-sort.md`)
- [ ] Build Differential Lint Context Generator (`@blueprint/action-points/AP-04-differential-linter-engine.md`)

### Phase 4: Recovery & Harness
- [ ] Implement Journal Replay (`@blueprint/action-points/AP-14-journal-recovery-logic.md`)
- [ ] Wire FileChanged Hooks (`@blueprint/action-points/AP-07-hook-integration-curator.md`)
- [ ] Wire SubagentStop Hooks (`@blueprint/action-points/AP-08-hook-integration-linter.md`)
- [ ] Create ADR Recovery Template (`@blueprint/action-points/AP-09-recovery-adr-template.md`)

### Phase 5: Verification
- [ ] Build and Run E2E Stabilization Tests (`@blueprint/action-points/AP-10-e2e-stabilization-test.md`)
