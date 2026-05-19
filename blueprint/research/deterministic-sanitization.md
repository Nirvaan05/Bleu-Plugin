# Research: Deterministic Sanitization & Input Hardening

## Securing the Ingest Pipeline
External data in `raw/` (transcripts, docs, PRs) is a primary vector for prompt injection and architectural drift.

### 1. Multi-Stage Ingestion
- **Stage 1 (Deterministic):** Non-LLM pass. 
    - **Markdown Normalization:** Stripping HTML tags, dangerous URI schemes (`javascript:`), and non-standard markdown extensions.
    - **Pattern Matching:** Detecting "Ignore previous instructions" or "System Role" override strings via regex.
    - **Trust Tagging:** Labeling the source (e.g., `trust: high` for local files, `trust: low` for web fetches).
- **Stage 2 (Semantic):** LLM-based summary. The LLM is instructed to *describe* the content rather than *execute* it.

### 2. Trust Boundaries
- **Isolate External Instructions:** Wrapping ingested text in unique XML tags (e.g., `<external_content>`) and instructing the Curator to never treat text within these tags as a directive.
- **Read-Only Ingestion:** The Curator reads from `raw/` but never executes shell commands or modifies `plan/` based *solely* on `raw/` content without a link to an ADR or user confirmation.

### 3. Safe Parsing Architecture
- **Bleu Implementation:** The `FileChanged` hook triggers a deterministic Python script to sanitize the file *before* the Curator sees it.

## Synthesis for Bleu
- **Strip Executable Directives:** Regex-based removal of shell-like syntax or common injection strings.
- **Schema Validation:** Ensure ingested JSON/Markdown matches expected structure before it reaches the reasoning layer.

## Sources
- [OWASP: Prompt Injection Mitigation](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Anthropic: Context Engineering Best Practices](https://docs.anthropic.com/claude/docs/context-engineering)
- [Markdown Sanitization Libraries (Bleach, DOMPurify)](https://github.com/mozilla/bleach)
