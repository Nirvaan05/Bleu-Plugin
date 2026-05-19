# Component: Deterministic Sanitizer (AST-Based)

## Purpose
Acts as the first-line defense (Stage 1) for the ingestion pipeline, ensuring external content cannot execute directives or cause architectural drift.

## Responsibilities
- Parse incoming Markdown into an AST (using `markdown-it-py`).
- Sanitize code fences by stripping dangerous shell directives and obfuscated payloads.
- Perform Unicode normalization to prevent homoglyph attacks.
- Remove hidden/invisible characters.
- Strip instruction-override patterns (e.g., "Ignore previous...").
- Wrap sanitized content in `<external_content>` tags.

## Logic
- **AST Pass:** Walks the tree nodes. If node type is `code_block` or `fence`, apply strict regex-based content stripping.
- **Text Pass:** Apply global regex for override patterns on the final output.
- **Metadata:** Prepend trust-level and redaction counts.

## Interfaces
- **Input:** Raw file path.
- **Output:** Sanitized Markdown content.

## Failure Modes
- **Malformed Markdown:** Parser fails to build AST.
    - *Handle:* Move file to `raw/quarantine/` and alert user.
- **Bypass:** Payloads hidden in non-code elements (e.g., malformed image ALT tags).
    - *Handle:* Auditor agent (Stage 2) performs semantic check.
