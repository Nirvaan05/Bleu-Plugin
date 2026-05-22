import argparse
import sys
import os
import re
import json
import unicodedata
from datetime import datetime
from utils import read_file, write_file_atomic

def load_config(config_path):
    if not os.path.exists(config_path):
        return {"patterns": []}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class RegexSanitizer:
    """
    Deterministic input sanitizer (AP-13).

    Two deterministic stages, applied in order:
      1. Unicode normalization (NFKC) + stripping of invisible control chars,
         which neutralizes homoglyph and zero-width-character evasion.
      2. Configurable regex redaction over the whole normalized text.

    Note: block-scoped redaction over a parsed markdown AST is a planned
    enhancement (it would let us treat code fences differently from prose),
    but the shipped implementation is whole-text regex. The class is named
    for what it does today, not for the AP-13 aspiration.
    """
    def __init__(self, config):
        self.config = config
        self.redactions = 0
        self.messages = []

    def normalize_text(self, text: str) -> str:
        """ADR-004: Unicode normalization and hidden character stripping."""
        # Normalize to NFKC to resolve homoglyph-like variations
        text = unicodedata.normalize('NFKC', text)
        # Strip common hidden/invisible control characters except newline and tab
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in "\n\t")
        return text

    def apply_regex(self, text: str) -> str:
        """Apply configured regex patterns to a block of text."""
        for pattern in self.config.get("patterns", []):
            regex = pattern.get("regex")
            pid = pattern.get("id")
            
            matches = list(re.finditer(regex, text))
            if matches:
                self.redactions += len(matches)
                text = re.sub(regex, f"[REDACTED: {pid}]", text)
                self.messages.append(f"{pid}: {pattern.get('message')}")
        return text

    def sanitize(self, content: str) -> str:
        # Stage 1: deterministic Unicode normalization + control-char stripping.
        content = self.normalize_text(content)
        # Stage 2: regex redaction over the whole normalized text. Instruction
        # overrides (S-02) and shell directives (S-01) must be caught anywhere,
        # so whole-text matching is intentional rather than block-scoped.
        return self.apply_regex(content)

def main():
    parser = argparse.ArgumentParser(description="Bleu Deterministic Sanitizer (AP-13)")
    parser.add_argument("file", help="File to sanitize")
    parser.add_argument("--config", default=".claude/bleu/sanitizer-config.json", help="Path to config")
    parser.add_argument("--trust", default="low", choices=["high", "low"], help="Source trust level")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.", file=sys.stderr)
        sys.exit(1)

    config = load_config(args.config)
    original_content = read_file(args.file)

    sanitizer = RegexSanitizer(config)
    sanitized_content = sanitizer.sanitize(original_content)
    
    # Prepend Metadata Block (ADR-004)
    header = f"""---
bleu_trust_level: {args.trust}
bleu_sanitized_at: {datetime.now().isoformat()}
bleu_redaction_count: {sanitizer.redactions}
---
"""
    if sanitizer.messages:
        unique_messages = sorted(list(set(sanitizer.messages)))
        header += "<!-- Sanitization Messages:\n" + "\n".join(unique_messages) + "\n-->\n"
        
    final_output = f"{header}\n<trust_boundary>\n{sanitized_content}\n</trust_boundary>"
    
    write_file_atomic(args.file, final_output)
    print(f"Sanitization complete for {args.file}. Redactions: {sanitizer.redactions}")

if __name__ == "__main__":
    main()
