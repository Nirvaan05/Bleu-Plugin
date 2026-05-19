# AP-13: AST Sanitizer Core

## Title
Implement parser-based Markdown ingestion hardening.

## Depends on
AP-05

## Files involved
- `scripts/bleu/sanitizer.py`: Modify

## Code flow
1. Integrate a Markdown AST parser (e.g., `markdown-it-py`).
2. Implement an AST walker that:
    - Identifies `code_block` and `fence` nodes.
    - Applies regex stripping specifically to these node contents.
3. Implement Unicode normalization (`unicodedata.normalize('NFKC', text)`).
4. Strip hidden control characters.
5. Re-assemble the sanitized Markdown.

## Interfaces touched
- `raw/` ingestion pipeline.

## Verification
- Feed the sanitizer an obfuscated payload (e.g., unicode homoglyphs in a code fence).
- Verify it is correctly normalized and redacted.

## Complexity
M - Integration with an AST library.
