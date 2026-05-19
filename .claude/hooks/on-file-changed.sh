#!/bin/bash
# Bleu Hook Adapter: FileChanged (AP-07)
# Invokes the deterministic harness with recursion guards.

FILE_PATH="$1"
python3 scripts/bleu/harness.py --hook file_changed --file "$FILE_PATH"
