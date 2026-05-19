# Handoff to Superpowers Plugin

**Invoke via:** `@superpowers execute this plan`

This document defines the implementation plan for the **Bleu Stabilization & Industrialization** project. Superpowers will track checkpoints and verify each step against the `blueprint/` workspace.

## Context
The goal is to harden Bleu orchestration via deterministic guardrails: Atomic State Management, AST Sanitization, DAG Validation, and a Root-Aware Circuit Breaker.

## Plan

1. **Scaffold Infrastructure**
   - Execute `@blueprint/action-points/AP-01-scaffold-scripts.md`
   - Execute `@blueprint/action-points/AP-11-atomic-state-management.md`
   - *Checkpoint:* Verify thread-safe I/O primitives exist.

2. **Deterministic Engines**
   - Execute `@blueprint/action-points/AP-05-sanitizer-regex-suite.md`
   - Execute `@blueprint/action-points/AP-13-ast-sanitizer-core.md`
   - Execute `@blueprint/action-points/AP-06-circuit-breaker-logic.md`
   - Execute `@blueprint/action-points/AP-02-graph-engine-parser.md`
   - *Checkpoint:* Run deterministic scripts manually to ensure no LLM logic is present.

3. **Advanced Algorithms**
   - Execute `@blueprint/action-points/AP-03-dag-validator-core.md`
   - Execute `@blueprint/action-points/AP-12-deterministic-dag-sort.md`
   - Execute `@blueprint/action-points/AP-04-differential-linter-engine.md`
   - Execute `@blueprint/action-points/AP-15-global-constraint-propagation.md`
   - Execute `@blueprint/action-points/AP-14-journal-recovery-logic.md`
   - *Checkpoint:* Validate sorting and differential filtering outputs.

4. **Harness Integration**
   - Execute `@blueprint/action-points/AP-07-hook-integration-curator.md`
   - Execute `@blueprint/action-points/AP-08-hook-integration-linter.md`
   - Execute `@blueprint/action-points/AP-09-recovery-adr-template.md`
   - *Checkpoint:* Hooks are wired and `.claude/settings.json` is updated.

5. **E2E Verification**
   - Execute `@blueprint/action-points/AP-10-e2e-stabilization-test.md`
   - *Checkpoint:* 100% test pass rate.
