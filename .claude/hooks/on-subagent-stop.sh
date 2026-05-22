#!/usr/bin/env bash
# Bleu Hook Adapter: SubagentStop (AP-08)
# Matched on kb-linter. Forwards the deterministic circuit-breaker logic.
#
# Reads the SubagentStop JSON payload from STDIN and extracts the agent name.
set -euo pipefail

INPUT=$(cat 2>/dev/null || echo '{}')
AGENT_NAME=$(printf '%s' "$INPUT" | jq -r '.agent_name // .subagent_type // ""')

cd "${CLAUDE_PROJECT_DIR:-.}"
python3 scripts/bleu/harness.py --hook subagent_stop --agent "$AGENT_NAME"
