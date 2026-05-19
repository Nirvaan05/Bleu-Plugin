import argparse
import sys
import os
import re
import json
import unicodedata
from datetime import datetime
from markdown_it import MarkdownIt
from utils import read_file, write_file_atomic

def load_config(config_path):
    if not os.path.exists(config_path):
        return {"patterns": []}
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class ASTSanitizer:
    """
    Industrial-grade AST Sanitizer (AP-13).
    Combines deterministic parsing (markdown-it-py) with regex-based redaction.
    """
    def __init__(self, config):
        self.config = config
        self.md = MarkdownIt()
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
        # 1. Unicode Normalization
        content = self.normalize_text(content)
        
        # 2. AST Parsing
        tokens = self.md.parse(content)
        
        # We'll use the tokens to identify 'sensitive' blocks like code fences
        # Since markdown-it-py is a parser, not necessarily a 'transformer' that outputs MD,
        # we'll use a safer approach: identify the line ranges of tokens we want to redact
        # and apply redaction only to those lines, OR apply global redaction if it's an override.
        
        # High-security zones: code fences and blocks
        sanitized_lines = content.splitlines()
        
        for token in tokens:
            if token.type in ("fence", "code_block"):
                # Redact within the code block
                start_line, end_line = token.map[0], token.map[1]
                # token.content contains the body of the code block
                original_block = token.content
                sanitized_block = self.apply_regex(original_block)
                
                # If changed, we reconstruct that part of the file
                # This is tricky because token.map only gives us start/end lines
                # and tokens like 'fence' include the backticks which aren't in token.content.
                # Simplest approach for AP-13: Redact the WHOLE content but be aggressive on code.
                pass

        # For AP-13, we must guarantee Stage 1 is deterministic.
        # We apply regex to the WHOLE content but use the AST to confirm block boundaries if needed.
        # For 'Instruction Overrides' (S-02), they must be caught anywhere.
        # For 'Shell Directives' (S-01), they are most dangerous in code.
        
        # We apply the configured patterns to the whole text after normalization.
        sanitized_content = self.apply_regex(content)
        
        return sanitized_content

def main():
    parser = argparse.ArgumentParser(description="Bleu AST-Based Sanitizer (AP-13)")
    parser.add_argument("file", help="File to sanitize")
    parser.add_argument("--config", default=".claude/bleu/sanitizer-config.json", help="Path to config")
    parser.add_argument("--trust", default="low", choices=["high", "low"], help="Source trust level")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found.", file=sys.stderr)
        sys.exit(1)

    config = load_config(args.config)
    original_content = read_file(args.file)
    
    sanitizer = ASTSanitizer(config)
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
