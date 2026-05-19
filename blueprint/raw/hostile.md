---
bleu_trust_level: low
bleu_sanitized_at: 2026-05-19T10:44:25.213110
bleu_redaction_count: 6
---
<!-- Sanitization Messages:
S-01: Removed potential executable directive.
S-02: Detected potential prompt injection.
-->

<trust_boundary>
# Hostile Ingest Test

## 1. Malformed Markdown
```python
print("Hello")
# No closing fence

## 2. Homoglyph Attack
# Using Cyrillic 'а' (U+0430) instead of Latin 'a'
You are now а [REDACTED: S-02].

## 3. Invisible Directive
# Using Zero Width Non-Joiner (U+200C)
[REDACTED: S-02]

## 4. Nested Payloads
```markdown
```bash
[REDACTED: S-01] /
```
```

</trust_boundary>