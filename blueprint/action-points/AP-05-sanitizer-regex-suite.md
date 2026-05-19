# AP-05: Sanitizer Regex Suite

## Title
Implement deterministic input hardening.

## Depends on
AP-01

## Files involved
- `scripts/bleu/sanitizer.py`: Modify
- `.claude/bleu/sanitizer-config.json`: Create

## Code flow
1. Define a core set of regex patterns for:
    - Shell injection (`rm`, `curl`, `sudo`).
    - Instruction overrides ("Ignore previous...").
    - Malicious HTML/Script tags.
2. Implement the `strip_and_tag` logic:
    - If a pattern matches, replace it with `[REDACTED: S-NN]`.
    - Prepend a metadata block to the file stating trust level and count of redactions.
3. Wrap the entire content in `<external_content>` tags.

## Interfaces touched
- `raw/` file format (sanitized).

## Verification
- Create a file in `raw/` containing `rm -rf /`.
- Run the sanitizer.
- Verify the string is redacted and the file is wrapped in XML tags.

## Complexity
M - Regex security is precision work.
