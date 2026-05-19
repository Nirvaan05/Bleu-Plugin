#!/bin/bash
# Bleu Hook Adapter: SubagentStop (AP-08)
# Matched on kb-linter. Triggers circuit breaker and auditor logic.

AGENT_NAME="$1"
python3 scripts/bleu/harness.py --hook subagent_stop --agent "$AGENT_NAME"
