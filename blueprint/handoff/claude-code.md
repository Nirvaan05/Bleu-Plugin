# Handoff for Raw Claude Code

## Instructions for Execution Agent
You are executing a locked architecture plan for the Bleu-plugin. 

1. **Read Order:** 
   - `blueprint/SESSION.md`
   - `blueprint/NEXT.md`
   - `blueprint/plan/01-architecture.md`
   - `blueprint/action-points/README.md`
2. **Execution:** Implement the APs exactly in the order specified in `blueprint/action-points/README.md`.
3. **Constraint:** The architecture is frozen. Do not introduce new libraries or patterns outside of those approved in `blueprint/decisions/`.
4. **Validation:** After each AP, verify it against the explicit "Verification" section inside the AP file.
5. **Progress:** Update `blueprint/progress.md` (or `SESSION.md`/`NEXT.md` if working iteratively) after completing each parallel execution group.

**Topological Execution Sequence:**
1. AP-01, AP-11
2. AP-05, AP-06, AP-02
3. AP-13, AP-03, AP-04, AP-15, AP-14
4. AP-07, AP-08, AP-09, AP-12
5. AP-10

Do not combine APs. Do not guess intent. If blocked, escalate to the user and reference the blocking AP.
