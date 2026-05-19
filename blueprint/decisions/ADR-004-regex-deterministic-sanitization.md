# ADR-004: AST-Based Deterministic Sanitization

**Status**: Accepted (Revised 2026-05-18)
**Date**: 2026-05-18
**Deciders**: user + claude
**Phase**: Phase 2 — architecture (Hardening)

## Context
Regex-only sanitization is easily bypassed by unicode tricks, malformed code fences, and nested payloads. We need a parser that understands Markdown structure.

## Decision
Use an **AST-based Markdown Parser** (e.g., `markdown-it-py`) for Stage 1 sanitization.
1.  Parse the incoming Markdown into an Abstract Syntax Tree.
2.  Walk the tree and apply strict rules to:
    - Code fences (extract and sanitize).
    - Inline code.
    - Dangerous URI schemes.
    - Unicode normalization (prevent homoglyph attacks).
3.  Strip hidden/invisible characters.
4.  Wrap everything in `<external_content>` tags.

## Alternatives considered
- **Regex-only:** Rejected; too many bypasses in Markdown's complex syntax.
- **LLM-only:** Rejected; hallucination risk and susceptible to prompt injection.

## Consequences
**Positive**:
- Highly resilient against obfuscation.
- Deterministic and auditable.

**Negative**:
- Adds a small dependency on a parser library (or requires building a minimal one).

## Sources
- [Bleu Stabilization Phase 6 Adversarial Audit]
- [markdown-it-py Documentation](https://github.com/executablebooks/markdown-it-py)
