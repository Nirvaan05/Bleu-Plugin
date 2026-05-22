#!/usr/bin/env bash
# Bleu Hook Adapter: FileChanged (AP-07)
# Wires the deterministic harness into Claude Code's FileChanged event.
#
# Claude Code delivers hook input as a JSON object on STDIN (not argv).
# See plugins/bleu/skills/bleu/references/claude-code-integration.md for the contract.
set -euo pipefail

INPUT=$(cat 2>/dev/null || echo '{}')
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.file_path // ""')

[ -z "$FILE_PATH" ] && exit 0

# Portable interpreter: python3 on most Unix, python on Windows / many distros.
PY="${PYTHON:-$(command -v python3 || command -v python)}"

cd "${CLAUDE_PROJECT_DIR:-.}"
"$PY" scripts/bleu/harness.py --hook file_changed --file "$FILE_PATH"
