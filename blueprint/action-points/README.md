# Action Points: Bleu Stabilization

## Dependency Graph

```mermaid
graph TD
    AP01[AP-01: Scaffold Scripts] --> AP02[AP-02: Graph Parser]
    AP01 --> AP05[AP-05: Sanitizer]
    AP01 --> AP06[AP-06: Circuit Breaker]
    AP01 --> AP11[AP-11: Atomic Management]
    
    AP02 --> AP03[AP-03: DAG Validator]
    AP02 --> AP04[AP-04: Diff Linter]
    AP02 --> AP15[AP-15: Global Prop]
    
    AP03 --> AP12[AP-12: Deterministic Sort]
    
    AP05 --> AP13[AP-13: AST Sanitizer]
    
    AP11 --> AP14[AP-14: Journal Recovery]
    
    AP02 --> AP07[AP-07: Curator Hooks]
    AP13 --> AP07
    
    AP04 --> AP08[AP-08: Linter Hooks]
    AP06 --> AP08
    AP15 --> AP08
    
    AP06 --> AP09[AP-09: Recovery ADR]
    
    AP07 --> AP10[AP-10: E2E Test]
    AP08 --> AP10
    AP12 --> AP10
    AP09 --> AP10
    AP14 --> AP10
```

## Recommended Execution Order
1. **Infrastructure (P0):** AP-01, AP-11
2. **Deterministic Engines:** AP-02, AP-05, AP-06, AP-13
3. **Algorithms:** AP-03, AP-04, AP-12, AP-15
4. **Harness Integration:** AP-07, AP-08, AP-09, AP-14
5. **Verification:** AP-10
