#!/usr/bin/env bash
# Bleu Hook Adapter: SubagentStop (AP-08)
# Matched on kb-linter. Forwards the deterministic circuit-breaker logic.
#
# Reads the SubagentStop JSON payload from STDIN and extracts the agent name.
set -euo pipefail

INPUT=$(cat 2>/dev/null || echo '{}')
AGENT_NAME=$(printf '%s' "$INPUT" | jq -r '.agent_name // .subagent_type // ""')

# Portable interpreter: python3 on most Unix, python on Windows / many distros.
PY="${PYTHON:-$(command -v python3 || command -v python)}"

cd "${CLAUDE_PROJECT_DIR:-.}"
"$PY" scripts/bleu/harness.py --hook subagent_stop --agent "$AGENT_NAME"
